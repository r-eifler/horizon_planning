from os import access, R_OK
from os.path import isfile

import re


class Action:

    def __init__(self, name, *params) -> None:
        self.name = name
        self.param = list(params)

    def __repr__(self) -> str:
        "(" + self.name + " ".join(self.param) + ")"
        

class Plan:

    def __init_(self):
        super().__init__()

    def __repr__(self) -> str:
        return str(self.actions)

    def __getitem__(self, subscript):
        if isinstance(subscript, slice):
            return self.actions[subscript.start: subscript.stop: subscript.step]
        else:
            return self.actions[subscript]

    def get_prefix(self, count):
        prefix_plan = Plan()
        prefix_plan.actions = self.actions[:count]
        return prefix_plan

    @staticmethod
    def from_action_list(actions: list[str]) -> None:
        plan = Plan()
        plan.actions = actions
        return plan

    @staticmethod
    def from_file(plan_file: str) -> None:
        
        assert isfile(plan_file) and access(plan_file, R_OK), \
            f"File {plan_file} does not exist or is not readable"
        
        with open(plan_file) as fp:
            raw_actions = [a.strip() for a in fp.readlines()]

        actions = [a for a in raw_actions if not a.startswith(';') and len(a) > 0]

        assert len(raw_actions) > 0, 'Plan is empty!'

        for a in actions:
            m = re.match("(?:\d+:)*\s*\([\w\s-]+\)", a, re.IGNORECASE)
            assert m is not None, 'Syntax of action ' + a + ' is broken'

        actions = [re.sub("(?:\d+:)+\s*",'', a) for a in actions]

        plan = Plan()
        plan.actions = actions
        return plan


    def to_file(self, plan_file: str):

        with open(plan_file, 'w') as fp:
            fp.writelines([str(a) + "\n" for a in self.actions])


    def filter(self, condition):
        self.actions = [a for a in self.action if condition(a)]

    def map(self, transformation):
        self.actions = [transformation(a) for a in self.action]


    def __len__(self) -> int:
        return len(self.actions)
