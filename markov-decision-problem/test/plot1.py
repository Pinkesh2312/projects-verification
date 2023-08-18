import random,argparse,subprocess,os
parser = argparse.ArgumentParser()
import numpy as np
import matplotlib.pyplot as plt
random.seed(0)
np.random.seed(0)

state = '1530'
# The win probability is the expected value of this state

q = np.arange(start=0, stop=1, step=0.1)
optim = []
rand = []

f = open('temp_cricket_states', 'w')
cmd = "python", "cricket_states.py", "--balls", "15", "--runs", "30"
subprocess.call(cmd, stdout=f)
f.close()

tbc = ['mdpfile', 'optim', 'rand', 'decOptim', 'decRand', 'temp_cricket_states']

for qVal in q:
    f = open('mdpfile', 'w')
    cmd = "python", "encoder.py", "--states", "temp_cricket_states", "--parameters", "data/cricket/sample-p1.txt", "--q", str(qVal)
    subprocess.call(cmd, stdout=f)
    f.close()
    f = open('optim', 'w')
    cmd = "python", "planner.py", "--mdp", "mdpfile", "--algorithm", "lp"
    subprocess.call(cmd, stdout=f)
    f.close()
    
    f = open('rand', 'w')
    cmd = "python", "planner.py", "--mdp", "mdpfile", "--policy", f"data/cricket/rand_pol_mod.txt"
    subprocess.call(cmd, stdout=f)
    f.close()
    f = open('decOptim', 'w')
    cmd = "python", "decoder.py", "--value-policy", "optim", "--states", "temp_cricket_states"
    subprocess.call(cmd, stdout=f)
    f.close()
    f = open('decRand', 'w')
    cmd = "python", "decoder.py", "--value-policy", "rand", "--states", "temp_cricket_states"
    subprocess.call(cmd, stdout=f)
    f.close()
    with open('decOptim') as f:
        optim.append(float(list(f.readline().split())[2][:-1]))
    
    with open('decRand') as f:
        rand.append(float(list(f.readline().split())[2][:-1]))

for ff in tbc:
    os.remove(ff)

plt.plot(list(q), rand, '-b', label='Random')
plt.plot(list(q), optim, '-r', label='Optimal')
plt.legend()
plt.title('Win probability vs. B\'s weakness')
plt.xlabel('q')
plt.ylabel('Win probability')
plt.savefig('rl_task2_ana1_mod.png')