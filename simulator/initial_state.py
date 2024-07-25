import re

from simulator.states import PDDLFact, PDDLNumericFluent, PDDLLiteral

class InitialState:
    def __init__(self):
        self.facts: set[PDDLLiteral] = set()
    

    @staticmethod
    def from_pddl(problem):

        with open(problem) as fp:
            problem_pddl_def = fp.read()


        match = re.search("\(:\s*INIT\s*((\([\w\s]+\)\s*)+)\)", problem_pddl_def, re.IGNORECASE)

        assert match, 'Problem definition not supported'

        fact_string = match.group(1)
        facts_raw = [f.strip().lower() for f in map(lambda f: f.replace('(',''), fact_string.split(')')) if len(f) > 0]

        facts = [PDDLFact(parts[0], *parts[1:]) for parts in [f.split() for f in facts_raw]]

        initial_state = InitialState()
        initial_state.facts = facts

        return initial_state

        
