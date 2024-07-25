from abc import ABC, abstractmethod

class StateChange:

    def __init__(self, action=None):
        self.action = action
        self.adds = []
        self.deletes = []
        self.updates = []

    def empty(self) -> bool:
        return len(self.adds) + len(self.deletes) + len(self.updates) == 0
    


class PDDLLiteral(ABC):

    def __repr__(self) -> str:
        pass
    

class PDDLFact(PDDLLiteral):

    def __init__(self, name: str, *params):
        self.name = name
        self.params = list(params)

    def __repr__(self):
        return self.name + "(" + ", " .join(self.params) + ")"

    def __eq__(self, fluent) -> bool:
            return str(self) == str(fluent)
    
    def __hash__(self) -> int:
        return str(self).__hash__()
    
    

class PDDLNumericFluent(PDDLLiteral):
    def __init__(self, value: int, function: str, *params):
        self.function = function
        self.value = value
        self.params = list(params)

    def __repr__(self) -> str:
        return self.function + "(" + ", " .join(self.params) + ") = " + str(self.value)
    
    def __eq__(self, fluent) -> bool:
        return str(self) == str(fluent)
    
    def __hash__(self) -> int:
        return str(self).__hash__()
    
    def __lt__(self, fluent: object) -> bool:
        if not type(fluent) == PDDLNumericFluent:
            return False
        return self.to_pddl().__lt__(fluent.to_pddl())
    

    def decrease(self,param):
            self.value -= param
    
    def increase(self,param):
            self.value += param

    def assign(self,param):
            self.value = param

        
class PDDLNumericOperation:
    def __init__(self, operation: str, fluent: PDDLNumericFluent, param: int):
        self.operation = operation
        self.fluent = fluent
        self.param = param

    def __repr__(self) -> str:
        return str(self.fluent) + " " + self.operation + " " + str(self.param)
    
    def __eq__(self, fluent) -> bool:
        return str(self) == str(fluent)
    
    def __hash__(self) -> int:
        return str(self).__hash__()
    
    def __lt__(self, fluent: object) -> bool:
        if not type(fluent) == PDDLNumericFluent:
            return False
        return self.to_pddl().__lt__(fluent.to_pddl())
    

    def update(self, operation, param):

        if operation == "decrease":
            self.fluent.decrease(param)
            return
        
        if operation == "increase":
            self.fluent.increase(param)
            return
        
        if operation == "assignment":
            self.fluent.assign(param)
            return



class State(set):

    def __init__(self):
        super().__init__()

    def copy(self):
        s = State()
        for v in self:
            s.append(v)
        return s

    def __repr__(self):
        return "[" + ", ".join([str(e) for e in self]) + "]"
    

    # def __eq__(self, other) -> bool:
    #     str_rep_s = [str(e) for e in self]
    #     str_rep_s.sort()
    #     allfacts_s = '_'.join(str_rep_s)

    #     str_rep_o = [str(e) for e in other]
    #     str_rep_o.sort()
    #     allfacts_o = '_'.join(str_rep_o)

    #     return allfacts_s == allfacts_o
    
    # def __hash__(self) -> int:
    #     return map(lambda f: f.__hash__(),  self)
    

class Trace(list):

    def __init__(self):
        super().__init__()
        self.cost = None

    def __repr__(self):
        return "\n".join(str(s) for s in self)
