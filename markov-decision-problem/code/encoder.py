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

    num_states += 2
    state_to_id["99990"] = i
    id_to_state[i] = "99990"
    # state_to_id["99991"] = i+1
    # id_to_state[i+1] = "99991"
    state_to_id["00000"] = i+1
    id_to_state[i+1] = "00000"
    return num_states, state_to_id, id_to_state

def get_parameters(input_file):
    file_ = open(input_file, 'r')
    lines = file_.readlines()
    i = 0
    parameters = {}
    for line in lines:
        if i != 0:
            line = line.split()
            parameters[int(line[0])] = []
            for j in line[1:]:
                parameters[int(line[0])].append(float(j))
        i += 1
    
    return parameters

def get_mdp(num_states, state_to_id, id_to_state, parameters, q):
    num_actions = 5
    mdp_type = "episodic"
    gamma = "1"
    actions = [0, 1, 2, 4, 6]
    outcomes = [-1, 0, 1, 2, 3, 4, 6]
    transitions = [[[0 for i in range(num_states)] for j in range(num_actions)] for k in range(num_states)]
    rewards = [[[0 for i in range(num_states)] for j in range(num_actions)] for k in range(num_states)]
    for state1 in range(num_states):
        s1 = int(id_to_state[state1])
        ball1 = s1//1000
        strike1 = s1%10
        runs1 = (s1//10)%100
        if runs1 == 99 or runs1 == 0:
            # for action in range(5):
            #     transitions[state1][action][state1] = 1
            #     rewards[state1][action][state1] = 0
            continue

        actions = [0,1,2,4,6]
        outcomes = [-1,0,1,2,3,4,6]
        if strike1 == 1:
            outcomes = [-1,0,1]
        
        for index1, action in enumerate(actions):
            for index2, outcome in enumerate(outcomes):
                p = 0
                r = 0
                if strike1 == 0:
                    p = parameters[action][index2]
                else:
                    if outcome == -1:
                        p = q
                    else:
                        p = (1-q)/2
                
                if outcome == -1:
                    state2 = state_to_id["99990"]
                    transitions[state1][index1][state2] += p
                    rewards[state1][index1][state2] = 0
                else:
                    ball2 = ball1 - 1
                    runs2 = runs1 - outcome
                    strike2 = strike1
                    s2 = ""
                    if runs2 <= 0:
                        state2 = state_to_id["00000"]
                        transitions[state1][index1][state2] += p
                        rewards[state1][index1][state2] = 1
                    elif ball2 == 0:
                        state2 = state_to_id["99990"]
                        transitions[state1][index1][state2] += p
                        rewards[state1][index1][state2] = 0
                    else:
                        if outcome == 1 or outcome == 3:
                            strike2 = 1 - strike2
                        if ball1%6 == 1:
                            strike2 = 1 - strike2
                        
                        ball2 = str(ball2)
                        runs2 = str(runs2)
                        strike2 = str(strike2)
                        if int(ball2) < 10:
                            ball2 = "0" + ball2
                        if int(runs2) < 10:
                            runs2 = "0" + runs2
                        
                        s2 = ball2 + runs2 + strike2
                        state2 = state_to_id[s2]
                        transitions[state1][index1][state2] += p
                        rewards[state1][index1][state2] = 0


        # if strike1 == 0:
        #     for action in range(5):
        #         for outcome in range(7):
        #             act = actions[action]
        #             out = outcomes[outcome]
        #             p = (parameters[act])[outcome]
        #             r = 0
        #             ball2 = ball1 - 1
        #             runs2 = 0
        #             if out != -1:
        #                 runs2 = max(runs1 - out, 0)
        #                 strike2 = strike1
        #                 if out == 1 or out == 3:
        #                     strike2 = 1 - strike2
        #                 if ball1%6 == 1:
        #                     strike2 = 1 - strike2
        #                 strike2 = str(strike2)
        #                 ball2 = str(ball2)
        #                 runs2 = str(runs2)
        #                 if int(ball2) < 10:
        #                     ball2 = "0" + ball2
        #                 if int(runs2) < 10:
        #                     runs2 = "0" + runs2
        #                 s2 = ball2 + runs2 + strike2
        #                 if(int(runs2)==0 and int(ball2)==0):
        #                     s2 = "00000"
        #                 elif (int(ball2)==0 and int(runs2)!=0):
        #                     s2 = "99990"
        #                 elif (int(ball2)!=0 and int(runs2)==0):
        #                     s2 = "00000"
        #                 state2 = state_to_id[s2]
        #                 if int(runs2) == 0:
        #                     r = 1
        #                 transitions[state1][action][state2] += p
        #                 rewards[state1][action][state2] = r
        #             else:
        #                 state2 = state_to_id["99990"]
        #                 transitions[state1][action][state2] += p
        #                 rewards[state1][action][state2] = 0
                    
        # else:
        #     for action in [0,1,2,3,4]:
        #         for out in [-1, 0, 1]:
        #             p = (1-q)/2
        #             if out == -1:
        #                 p = q
        #             r = 0
        #             ball2 = ball1 - 1
        #             runs2 = 0
        #             if out != -1:
        #                 runs2 = max(runs1 - out, 0)
        #                 strike2 = strike1
        #                 if out == 1 or out == 3:
        #                     strike2 = 1 - strike2
        #                 if ball1%6 == 1:
        #                     strike2 = 1 - strike2
        #                 strike2 = str(strike2)
        #                 ball2 = str(ball2)
        #                 runs2 = str(runs2)
        #                 if int(ball2) < 10:
        #                     ball2 = "0" + ball2
        #                 if int(runs2) < 10:
        #                     runs2 = "0" + runs2
        #                 s2 = ball2 + runs2 + strike2
        #                 if(int(runs2)==0 and int(ball2)==0):
        #                     s2 = "00000"
        #                 elif (int(ball2)==0 and int(runs2)!=0):
        #                     s2 = "99990"
        #                 elif (int(ball2)!=0 and int(runs2)==0):
        #                     s2 = "00000"
        #                 state2 = state_to_id[s2]
        #                 if int(runs2) == 0:
        #                     r = 1
        #                 transitions[state1][action][state2] += p
        #                 rewards[state1][action][state2] = r
        #             else:
        #                 state2 = state_to_id["99990"]
        #                 transitions[state1][action][state2] += p
        #                 rewards[state1][action][state2] = 0
                    
    tran = []
    for state1 in range(num_states):
        for action in range(num_actions):
            for state2 in range(num_states):
                tran.append([state1, action, state2, transitions[state1][action][state2], rewards[state1][action][state2]])
                # tran.append([id_to_state[state1], action, id_to_state[state2], transitions[state1][action][state2], rewards[state1][action][state2]])
    return num_states, num_actions, tran, mdp_type, gamma
            


def print_mdp(num_states, num_actions, transitions, mdp_type, gamma, id_to_state):
    print("numStates", num_states)
    print("numActions", num_actions)
    print("end", num_states-2, num_states-1)
    for transition in transitions:
        if transition[3] != 0:
            print("transition", transition[0], transition[1], transition[2], transition[4], transition[3])
    print("mdptype", mdp_type)
    print("discount", gamma)

if __name__ == "__main__":
    parser.add_argument("--states", type=str)
    parser.add_argument("--parameters", type=str, default=None)
    parser.add_argument("--q", type=float, default=0.25)

    args = parser.parse_args()
    state_filepath = args.states
    p1_parameters_file_path = args.parameters
    q = args.q

    num_states, state_to_id, id_to_state = generate_states(state_filepath)
    parameters = get_parameters(p1_parameters_file_path)
    num_states, num_actions, transitions, mdp_type, gamma = get_mdp(num_states=num_states, state_to_id=state_to_id, id_to_state=id_to_state, parameters=parameters, q=q)
    print_mdp(num_states, num_actions, transitions, mdp_type, gamma, id_to_state)