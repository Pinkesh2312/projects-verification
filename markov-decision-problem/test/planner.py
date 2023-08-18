from pulp import *
import numpy as np
from copy import deepcopy
import random
import argparse
import sys
parser = argparse.ArgumentParser()


def generate_mdp(input_file):

    numStates = 0
    numActions = 0
    mdptype = ""
    gamma = 1

    file_ = open(input_file, 'r')
    lines = file_.readlines()

    for line in lines:
        line = line.split()
        if line[0] == "numStates":
            numStates = int(line[1])
        if line[0] == "numActions":
            numActions = int(line[1])
        if numStates != 0 and numActions != 0:
            break

    rewards = np.zeros((numStates, numActions, numStates), dtype=float)
    transition_prob = np.zeros((numStates, numActions, numStates), dtype=float)
    end = []

    for line in lines:
        line = line.split()
        if line[0] == "transition":
            rewards[int(line[1])][int(line[2])][int(line[3])] = float(line[4])
            transition_prob[int(line[1])][int(
                line[2])][int(line[3])] = float(line[5])
        if line[0] == "mdptype":
            mdptype = str(line[1])
        if line[0] == "discount":
            gamma = float(line[1])
        if line[0] == "end":
            end = [int(a) for a in line[1:]]

    return numStates, numActions, rewards, transition_prob, mdptype, gamma, end


def get_policy(input_file):
    file_ = open(input_file, 'r')
    lines = file_.readlines()
    policy = []

    for line in lines:
        line = line.split()
        policy.append(int(line[0]))

    return policy


def compare(v1, v2):
    for i in range(len(v1)):
        if abs(v1[i]-v2[i]) >= 1e-8:
            return False
    return True

def value_iteration(states, actions, rewards, transition, mdptype, gamma, end):
    nextV = np.zeros(states)
    currV = np.ones(states)
    optimal_policy = np.zeros(states)
    while(not compare(nextV, currV)):
        currV = deepcopy(nextV)
        # nextV = np.array([np.max([np.sum(np.array([transition[s][a][s1]*(rewards[s][a][s1] +
        #                                                                  gamma*currV[s1]) for s1 in range(states)])) for a in range(actions)]) for s in range(states)])
        # optimal_policy = np.array([np.argmax([np.sum(np.array([transition[s][a][s1]*(rewards[s][a][s1] +
        #                                                                              gamma*currV[s1]) for s1 in range(states)])) for a in range(actions)]) for s in range(states)])

        for s in range(states):
            value_for_action = []
            for a in range(actions):
                sum = 0
                for s1 in range(states):
                    sum += transition[s][a][s1] * \
                        (rewards[s][a][s1] + gamma*currV[s1])
                value_for_action.append(sum)
            nextV[s] = np.max(value_for_action)
            optimal_policy[s] = np.argmax(value_for_action)
    return nextV, optimal_policy


def howard_pi(states, actions, rewards, transition, mdptype, gamma, end):
    def update_policy(curr_policy):
        values, policy = calculate_value_func(
            states, actions, rewards, transition, mdptype, gamma, end, curr_policy)
        new_policy = deepcopy(curr_policy)
        for s in range(states):
            curr_val = values[s]
            for a in range(actions):
                val_with_a = np.sum(np.array([transition[s][a][s1]*(rewards[s][a][s1]+gamma*values[s1]) for s1 in range(states)]))
                if val_with_a > curr_val + 1e-6:
                    new_policy[s] = a
                    break
        return new_policy
    
    curr_policy = [0 for i in range(states)]
    new_policy = [1 for i in range(states)]
    while True:
        new_policy = update_policy(curr_policy)
        if new_policy == curr_policy:
            return calculate_value_func(states, actions, rewards, transition, mdptype, gamma, end, curr_policy)
        curr_policy = deepcopy(new_policy)

def linear_prog(states, actions, rewards, transition, mdptype, gamma, end):
    lp_problem = pulp.LpProblem("lp", LpMinimize)
    variables = []
    for s in range(states):
        var_name = "var"+str(s)
        var = pulp.LpVariable(var_name)
        variables.append(var)
        
    lp_problem += sum([v for v in variables])
    for s in range(states):
        for a in range(actions):
            lp_problem += variables[s] >= pulp.lpSum(((transition[s][a][s1])*(
            rewards[s][a][s1] + gamma*variables[s1])) for s1 in range(states))

    lp_problem.solve(PULP_CBC_CMD(msg=0))

    values = [pulp.value(v) for v in variables]
    policy = [0 for i in range(states)]

    for s in range(states):
        value_for_actions = np.zeros(actions)
        for a in range(actions):
            val = np.sum(np.array([transition[s][a][s1]*(rewards[s][a][s1]+gamma*values[s1]) for s1 in range(states)]))
            value_for_actions[a] = val
        policy[s] = np.argmax(value_for_actions)
        
    return values, policy


def calculate_value_func(states, actions, rewards, transition, mdptype, gamma, end, policy):
    lp_problem = pulp.LpProblem("Value_function")
    variables = pulp.LpVariable.dicts('var', [s for s in range(states)])

    for s in range(states):
        lp_problem += variables[s] == pulp.lpSum(((transition[s][policy[s]][s1])*(
            rewards[s][policy[s]][s1] + gamma*variables[s1])) for s1 in range(states))

    lp_problem.solve(PULP_CBC_CMD(msg=0))
    value_func = [pulp.value(variables[s]) for s in range(states)]
    return value_func, policy

def mdp_planner(algorithm, states, actions, rewards, transition, mdptype, gamma, end):

    if algorithm == 'vi':
        return value_iteration(states, actions, rewards, transition, mdptype, gamma, end)

    if algorithm == 'lp':
        return linear_prog(states, actions, rewards, transition, mdptype, gamma, end)

    if algorithm == 'hpi':
        return howard_pi(states, actions, rewards, transition, mdptype, gamma, end)


if __name__ == "__main__":
    parser.add_argument("--mdp", type=str)
    parser.add_argument("--policy", type=str, default=None)
    parser.add_argument("--algorithm", type=str, default="vi")

    args = parser.parse_args()
    mdp_filepath = args.mdp
    states, actions, rewards, transition, mdptype, gamma, end = generate_mdp(
        mdp_filepath)

    if args.policy == None:
        value_func, optimal_policy = mdp_planner(
            args.algorithm, states, actions, rewards, transition, mdptype, gamma, end)
        for s in range(states):
            print("{:.6f}".format(value_func[s]) +
                  '\t' + str(int(optimal_policy[s])))

    else:
        policy = get_policy(args.policy)
        value_function, policy = calculate_value_func(
            states, actions, rewards, transition, mdptype, gamma, end, policy)
        for s in range(states):
            print("{:.6f}".format(
                value_function[s]) + '\t' + str(int(policy[s])))
