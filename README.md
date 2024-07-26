# Horizon Planning

The idead is to split a planning task into samller tasks whose plan prefixes can then be concatitated to form a plan 
for the original task.

## Simulator

A basic simulator that is based on [VAL](https://github.com/KCL-Planning/VAL)

A plan is executed until an action fails or all actions have been executed.
All intermediate states can be accessed. 

The plan execution call result in the following status:
 - `GOAL_SATISFIED` : all actions are applicable and the plan satisfies the goal
 - `APPLICABLE_BUT_GOAL_NOT_SATISFIED`: all actions are applicable but the plan does not satisfie the goal
 - `APPLICATION_FAILED`: at least on action is not applicable

## Horizon Planning

Given original task `T(1...n)`

Iteratively:

- splitting up a earsier task `t(i...(i+h)` with limited horizon from `T_(i...n)`
- solving task `t(i...(i+h)` resulting in plan `plan_i`
- simulating plan `plan_i` in task `T_(i...n)` until fail
- executable part of `plan_i` is added to overall plan and the last reached state is used to generate a new task `T((i+h)...n)`

![horizon_planning](https://github.com/user-attachments/assets/733bcb0d-a507-42d9-b5b9-02c1b8473986)


## TODO
- implementation horizon planning
