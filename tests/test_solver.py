#!/usr/bin/env python3

import unittest

import numpy as np
from optimal_assign.optimization.solver import OptimalAssignConfig
from optimal_assign.optimization.solver import OptimalAssignInstance
from optimal_assign.optimization.solver import OptimalAssignGroupSolver


class TestOptimalAssignGroupSolver(unittest.TestCase):
    """Test class for OptimalAssignGroupSolver class"""

    def setUp(self) -> None:
        self.item_properties = np.array([
            [2, 0, 1, 0, 1],
            [0, 2, 1, 1, 1],
            [0, 2, 3, 0, 0],
            [0, 1, 1, 2, 2]
        ])
        self.group_properties = np.array([
            [1, 1, 0, 0, 0],
            [0, 1, 1, 0, 0],
            [0, 0, 0, 1, 1]]
        )
        self.group_min_sizes = np.ones(self.group_properties.shape[0], dtype=np.int32)

    def test_assignment_group1(self) -> None:
        """There is one possible assignment configuration without having to remove properties from groups"""
        instance = OptimalAssignInstance(self.item_properties, self.group_properties, self.group_min_sizes)
        config = OptimalAssignConfig()
        solver = OptimalAssignGroupSolver(instance, config)
        values_x, values_y = solver.solve()
        self.assertEqual(
            values_y,
            [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
        )
        self.assertEqual(
            values_x,
            [True, False, False, True, False, False, False, True, False, False, False, True]
        )

    def test_assignment_group2(self) -> None:
        """There is one possible assignment configuration one property needs to be removed from one group"""
        self.item_properties = np.array([
            [2, 0, 1, 0, 1],
            [0, 2, 1, 1, 1],
            [0, 2, 3, 0, 0],
            [0, 1, 1, 1, 2]
        ])
        instance = OptimalAssignInstance(self.item_properties, self.group_properties, self.group_min_sizes)
        config = OptimalAssignConfig()
        solver = OptimalAssignGroupSolver(instance, config)
        values_x, values_y = solver.solve()
        self.assertEqual(
            values_y,
            [False, False, False, False, False, False, False, False, False, False, False, False, False, True, False]
        )
        self.assertEqual(
            values_x,
            [True, False, False, True, False, False, False, True, False, False, False, True]
        )

if __name__ == "__main__":
    unittest.main()