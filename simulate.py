#! /bin/python3

import argparse

from simulator import VAL_Simulator, Plan

def run(domain_file, problem_file, plan_file):

    simulator = VAL_Simulator(domain_file, problem_file)

    plan = Plan.from_file(plan_file)

    print(f"Plan length: {len(plan)}")

    simulator.init_plan_simulation(plan)

    executed_plan, trace, status = simulator.simulate_plan()

    print(status)
    print(f"num executed actions: {len(executed_plan)}")
    print(f"Last action: {executed_plan[-1]}")
    print("Last state:")
    print(trace[-1])


if __name__ == '__main__':

    parser = argparse.ArgumentParser(prog='Plan Simulator')

    parser.add_argument('domain')
    parser.add_argument('problem')  
    parser.add_argument('plan')  

    args = parser.parse_args()

    run(args.domain, args.problem, args.plan)