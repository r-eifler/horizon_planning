import os, sys, inspect

cmd_folder = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0]))
parent_folder = os.path.dirname(os.path.normpath(cmd_folder))
if parent_folder not in sys.path:
    sys.path.insert(0, parent_folder)

from simulator.execution_status import PlanExecutionStatus
from simulator.val_simulator import VAL_Simulator

import unittest


from simulator.plan import Plan

class TestPlanParseValid(unittest.TestCase):

    def test_valid_plan_no_time(self):
        plan = Plan.from_file("plans/valid_plan_1")
        self.assertEqual(len(plan), 20)

    def test_valid_plan_with_empty_lines(self):
        plan = Plan.from_file("plans/valid_plan_whitespace")
        self.assertEqual(len(plan), 20)

    def test_valid_plan_with_time(self):
        plan = Plan.from_file("plans/valid_plan_2")
        self.assertEqual(len(plan), 18)
        


class TestPlanParseNotValidFile(unittest.TestCase):

    def test_wrong_path(self):
        with self.assertRaises(AssertionError):
            Plan.from_file("plans/valid_pln")

    def test_empty_file(self):
        with self.assertRaises(AssertionError):
            Plan.from_file("plans/empty_plan")


class TestPlanParseBrokenActions(unittest.TestCase):

    def test_missing_brackets(self):
        with self.assertRaises(AssertionError):
            Plan.from_file("plans/broken_action_1")

        with self.assertRaises(AssertionError):
            Plan.from_file("plans/broken_action_2")

    def test_missing_brackets_and_time(self):
        with self.assertRaises(AssertionError):
            Plan.from_file("plans/broken_action_3")


class TestSimulatorInputValidation(unittest.TestCase):

    def test_wrong_path(self):

        domain_file = 'blocksworld/domain.pddl'
        problem_file = 'blocksworld/problem.pddl'

        with self.assertRaises(AssertionError):
            VAL_Simulator(domain_file + "f", problem_file)

        with self.assertRaises(AssertionError):
            VAL_Simulator(domain_file, problem_file + "f")


    def test_valid_problem_definition(self):

        domain_file = 'blocksworld/domain.pddl'
        problem_file_broken = 'broken/problem.pddl'
        problem_file_valid = 'blocksworld/problem.pddl'

        with self.assertRaises(AssertionError):
            VAL_Simulator(domain_file, problem_file_broken)

        simulator = VAL_Simulator(domain_file, problem_file_valid)

        self.assertEqual(len(simulator.initial_state.facts), 9)


    def test_successful_execution(self):

        domain_file = 'broken_instances/domain.pddl'
        problem_file = 'blocksworld/problem.pddl'
        plan_file = 'blocksworld/plan_suc'

        simulator = VAL_Simulator(domain_file, problem_file)

        plan = Plan.from_file(plan_file)

        with self.assertRaises(AssertionError):
            simulator.init_plan_simulation(plan)



class TestPlanSimulation(unittest.TestCase):

    def test_successful_execution(self):

        domain_file = 'blocksworld/domain.pddl'
        problem_file = 'blocksworld/problem.pddl'
        plan_file = 'blocksworld/plan_suc'

        simulator = VAL_Simulator(domain_file, problem_file)

        plan = Plan.from_file(plan_file)

        simulator.init_plan_simulation(plan)

        executed_plan, trace, status = simulator.simulate_plan()

        self.assertEqual(len(executed_plan), 20)

        self.assertEqual(len(trace), 21)

        self.assertEqual(status, PlanExecutionStatus.GOAL_SATISFIED)


    def test_not_applicable_action_execution(self):

        domain_file = 'blocksworld/domain.pddl'
        problem_file = 'blocksworld/problem.pddl'
        plan_file = 'blocksworld/plan_not_applicable'

        simulator = VAL_Simulator(domain_file, problem_file)

        plan = Plan.from_file(plan_file)

        simulator.init_plan_simulation(plan)

        executed_plan, trace, status = simulator.simulate_plan()

        self.assertEqual(len(executed_plan), 11)

        self.assertEqual(len(trace), 12)

        self.assertEqual(status, PlanExecutionStatus.APPLICATION_FAILED)


    def test_goal_not_satisfied(self):

        domain_file = 'blocksworld/domain.pddl'
        problem_file = 'blocksworld/problem.pddl'
        plan_file = 'blocksworld/plan_not_sat_goal'

        simulator = VAL_Simulator(domain_file, problem_file)

        plan = Plan.from_file(plan_file)

        simulator.init_plan_simulation(plan)

        executed_plan, trace, status = simulator.simulate_plan()

        self.assertEqual(len(executed_plan), 19)

        self.assertEqual(len(trace), 20)

        self.assertEqual(status, PlanExecutionStatus.APPLICABLE_BUT_GOAL_NOT_SATISFIED)

if __name__ == '__main__':
    unittest.main()