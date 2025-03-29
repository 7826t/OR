#!/usr/bin/env python3

import logging
from dataclasses import dataclass

import numpy as np

from ortools.sat.python import cp_model

logger = logging.getLogger(__name__)


@dataclass
class OptimalAssignInstance:
    item_properties: np.ndarray
    group_properties: np.ndarray
    group_min_sizes: np.ndarray


@dataclass
class OptimalAssignConfig:
    n_iterations: int=100
    timeout_value: int=60


class OptimalAssignSolver:

    def __init__(self, instance: OptimalAssignInstance, config: OptimalAssignConfig) -> None:
        self.instance = instance
        self.config = config
        self.model = cp_model.CpModel()

        self.num_items = instance.item_properties.shape[0]
        self.num_groups = instance.group_properties.shape[0]
        self.num_properties = instance.item_properties.shape[1]
        self.num_levels = 4

        # Model variables definition
        # x is the assignment of item i to group j
        self.x = [
            [self.model.NewBoolVar(f"x[{i},{j}]") for j in range(self.num_groups)] for i in range(self.num_items)
        ]

    def _add_uniqueness_constraint(self) -> None:
        """Each item is assigned to exactly one group."""
        for i in range(self.num_items):
            self.model.Add(sum(self.x[i][j] for j in range(self.num_groups)) == 1)

    def _add_group_min_size_constraint(self) -> None:
        """Each group has a minimum size."""
        for j in range(self.num_groups):
            self.model.Add(sum(self.x[i][j] for i in range(self.num_items)) >= self.instance.group_min_sizes[j])


class OptimalAssignGroupSolver(OptimalAssignSolver):

    def __init__(self, instance: OptimalAssignInstance, config: OptimalAssignConfig) -> None:
        super().__init__(instance, config)

        self.costs = instance.group_properties

        self.properties_matrix = np.ones((self.num_levels, self.num_items, self.num_properties), dtype=int)
        for l in range(self.num_levels):
            self.properties_matrix[l] = (instance.item_properties >= l).astype(int)

        # Define model variables
        # y is the removal of property k from group j
        self.y = [[self.model.NewBoolVar(f"y[{j}, {k}]") for k in range(self.num_properties)] for j in range(self.num_groups)]

        # Build model and initialize solver
        self._build_model()
        self.solver = cp_model.CpSolver()

    def _add_property_removal_constraint(self) -> None:
        """Only required properties can be removed from a group"""
        for j in range(self.num_groups):
            for k in range(self.num_properties):
                self.model.Add(self.y[j][k] <= self.instance.group_properties[j, k])

    def _add_property_constraint(self) -> None:
        """
        For each group and each required property,
        at least one assigned item has this property with a level of 2 or better
        """
        for j in range(self.num_groups):
            for k in range(self.num_properties):
                if self.instance.group_properties[j, k] == 1:
                    self.model.Add(
                        sum(self.x[i][j] * self.properties_matrix[2, i, k] for i in range(self.num_items)) >= 1
                    ).OnlyEnforceIf(self.y[j][k].Not())

    def _add_objective(self) -> None:
        """Add the objective function"""
        objective_terms = [
            self.costs[j][k] * self.y[j][k] for j in range(self.num_groups) for k in range(self.num_properties)
        ]
        self.model.Minimize(sum(objective_terms))

    def _build_model(self) -> None:
        """Put together constraints and objective function"""
        self._add_uniqueness_constraint()
        self._add_group_min_size_constraint()
        self._add_property_removal_constraint()
        if np.sum(self.instance.group_properties) > 0:
            self._add_property_constraint()
        self._add_objective()

    def solve(self) -> tuple[list[int], list[int]]:
        """
        Solve model and find an optimal solution.

        Returns:
            The values for the main assignment problem (where to place items).
            The values for the secondary assignment problem (where to remove property).
        """
        self.solver.parameters.max_time_in_seconds = self.config.timeout_value
        status1 = self.solver.Solve(self.model)
        logger.info(f"Status = {self.solver.StatusName(status1)}")

        values_x = []
        values_y = []
        if status1 == cp_model.OPTIMAL:
            min_total_cost = round(self.solver.ObjectiveValue())
            logger.info(f"Total cost = {min_total_cost}")

            for i in range(self.num_items):
                for j in range(self.num_groups):
                    val = self.solver.BooleanValue(self.x[i][j])
                    values_x.append(val)

            for j in range(self.num_groups):
                for k in range(self.num_properties):
                    val = self.solver.BooleanValue(self.y[j][k])
                    values_y.append(val)
        else:
            if status1 in {cp_model.FEASIBLE, cp_model.UNKNOWN}:
                logger.info("No optimal solution could be found in the allotted time.")
            elif status1 == cp_model.INFEASIBLE:
                logger.info("There is no solution.")

        logger.info("Done!")

        return values_x, values_y
