from os import access, R_OK
from os.path import isfile
import os
import subprocess

from simulator.execution_status import PlanExecutionStatus
from simulator.states import State, StateChange

from .plan import Action, Plan
from .states import PDDLFact, PDDLNumericFluent, Trace
from .initial_state import InitialState


class VAL_Simulator:

    def __init__(self, domain_file, problem_file, initial_state = None):

        assert isfile(domain_file) and access(domain_file, R_OK), \
            f"File {domain_file} does not exist or is not readable"
        
        assert isfile(problem_file) and access(problem_file, R_OK), \
            f"File {problem_file} does not exist or is not readable"
                
        self.domain_file = domain_file
        self.problem_file = problem_file

        self.initial_state = initial_state
        if self.initial_state is None:
            self.initial_state = InitialState.from_pddl(self.problem_file)

        self.state_changes = []
        self.cost = None 
        self.plan_execution_status = None



    def init_plan_simulation(self, plan: Plan):

        self.plan = plan
        
        temp_plan_file = os.path.join(os.path.dirname(__file__), 'temp_plan')
        plan.to_file(temp_plan_file)

        self.get_state_changes(temp_plan_file)

        self.state_trace = Trace()
        self.state_trace.append(self.initial_state.facts)

        self.next_change = 0


    def has_next_action(self):
        return self.next_change < len(self.state_changes)


    def simulate_next_action(self) -> State:

        assert self.has_next_action(), "There are no more applicable actions."

        change = self.state_changes[self.next_change]
        action = self.plan[self.next_change]

        self.next_change += 1

        next_state = self.state_trace[-1].copy()
        # print("Current state:")
        # print(next_state)
        # print("DELETE")
        # print(change.deletes)
        # print("ADD")
        # print(change.adds)
        # print("----------------------------------")
        for d in change.deletes:
            next_state.remove(d)

        for a in change.adds:
            next_state.append(a)
        
        for fluent, value, op in change.updates:
            next_state.remove(fluent)
            fluent.update(op, value)
            next_state.append(fluent)
            
        self.state_trace.append(next_state)

        return action, next_state
        

    def simulate_plan(self) -> tuple[list[Action], Trace, PlanExecutionStatus]:
        while self.has_next_action():
            self.simulate_next_action()

        executed_plan = self.plan.get_prefix(self.next_change)

        return executed_plan, self.state_trace, self.plan_execution_status
           

    def run_val(self, plan_sas_file): 

        base = os.path.dirname(__file__)
        command = os.path.join(base, 'validate')
        args = [
            "-v",
            self.domain_file,
            self.problem_file,
            plan_sas_file
        ]

        p = subprocess.run([command] + args, capture_output=True, text=True)

        lines = p.stdout.splitlines()

        assert p.returncode == 0 or \
            any(['Plan failed' in l or 'Goal not satisfied' in l for l in lines]), \
            'VAL execution failed, return code: ' + str(p.returncode) + "\n" + str(lines)

        return lines

    def get_state_changes(self, plan_sas_file):


        lines = self.run_val(plan_sas_file)
        assert len(lines) > 0, "Val output corrupted."

        state_changes = []
        cost = None
        plan_execution_status = None
        line = lines.pop(0)
        while not line.startswith("-----------"):
            assert not line.startswith("The goal is not satisfied"), "PLAN NOT VALID: " + plan_sas_file
            assert len(lines) > 0, plan_sas_file
            line = lines.pop(0)

        while len(lines) > 0:
            line = lines.pop(0).replace("\n", "")

            if 'Plan failed to execute' in line:
                plan_execution_status = PlanExecutionStatus.APPLICATION_FAILED
                break

            if 'Goal not satisfied' in line:
                plan_execution_status = PlanExecutionStatus.APPLICABLE_BUT_GOAL_NOT_SATISFIED
                break

            if 'Plan valid' in line:
                plan_execution_status = PlanExecutionStatus.GOAL_SATISFIED
                break

            if line.startswith("Checking next happening"):
                state_changes.append(StateChange())
                continue
            
            # print(line)
            if line.startswith("Deleting"):
                fact_parts = line.replace("Deleting ", "").replace("(", "").replace(")", "").split(" ")
                fact = PDDLFact(fact_parts[0], *fact_parts[1:])
                state_changes[-1].deletes.append(fact)
                continue

            if line.startswith("Adding"):
                fact_parts = line.replace("Adding ", "").replace("(", "").replace(")", "").split(" ")
                fact = PDDLFact(fact_parts[0], *fact_parts[1:])
                state_changes[-1].adds.append(fact)
                continue

            if line.startswith("Updating"):
                all_parts = line.split(" ")
                match_iter = re.finditer("\(([\s\w-]+)\)", line)
                matches = [m.group(1) for m in match_iter]
                current_value = float(matches[1])
                fact_parts = matches[0].split(" ")
                update = [PDDLNumericFluent(fact_parts[0], current_value, *fact_parts[1:]), float(all_parts[-2]), all_parts[-1]]
                state_changes[-1].updates.append(update)

            # print(line)
            if line.startswith(("Final value:")):
                #print(line)
                #print(line.split(" "))
                cost = int(line.split(" ")[-1])
        # print("Cost: " + str(cost))

        if state_changes[-1].empty():
            state_changes.pop()


        self.state_changes = state_changes
        self.cost = cost 
        self.plan_execution_status = plan_execution_status
