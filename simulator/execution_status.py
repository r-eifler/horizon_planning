from enum import Enum

class PlanExecutionStatus(str, Enum):

    GOAL_SATISFIED = "GOAL_SATISFIED"
    APPLICATION_FAILED = "APPLICATION_FAILED"
    APPLICABLE_BUT_GOAL_NOT_SATISFIED = "APPLICABLE_BUT_GOAL_NOT_SATISFIED"


class ActionExecutionStatus:

    def __init__(self, applicable, fail_reason = []) -> None:
        self.applicable = applicable
        self.fail_reason = fail_reason