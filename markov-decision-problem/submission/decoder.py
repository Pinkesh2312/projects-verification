import numpy as np
from copy import deepcopy
import random
import argparse
import sys
parser = argparse.ArgumentParser()

def generate_states(input_file):

    num_states = 0
    state_to_id = {}
    id_to_state = {}
    i = 0
    file_ = open(input_file, 'r')
    lines = file_.readlines()

    for line in lines:
        line = line.split()
        num_states += 2
        state_to_id[line[0]+"0"] = i
        state_to_id[line[0]+"1"] = i+1
        id_to_state[i] = line[0]+"0"
        id_to_state[i+1] = line[0]+"1"
        i += 2

    num_states += 3
    state_to_id["99990"] = i
    id_to_state[i] = "99990"
    state_to_id["99991"] = i+1
    id_to_state[i+1] = "99991"
    state_to_id["00000"] = i+2
    id_to_state[i+2] = "00000"
    return num_states, state_to_id, id_to_state

def get_policy(input_file):
    file_ = open(input_file, 'r')
    lines = file_.readlines()
    value_function = []
    policy = []
    for line in lines:
        line = line.split()
        value_function.append(float(line[0]))
        policy.append(int(line[1]))
    
    return value_function, policy


if __name__ == "__main__":
    parser.add_argument("--states", type=str)
    parser.add_argument("--value-policy", type=str, default=None)

    args = parser.parse_args()
    state_filepath = args.states
    value_file = args.value_policy

    num_states, state_to_id, id_to_state = generate_states(state_filepath)
    value_function, policy = get_policy(value_file)

    action = {
        0:0,
        1:1,
        2:2,
        3:4,
        4:6
    }
    for i in range(num_states-3):
        state = id_to_state[i]
        if state[4]=="0":
            print(state[:4], action[policy[i]], value_function[i])
