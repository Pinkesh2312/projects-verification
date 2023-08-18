import random,argparse,subprocess,os
parser = argparse.ArgumentParser()
import numpy as np
import matplotlib.pyplot as plt
random.seed(0)
np.random.seed(0)

q = 0.25
state = '1530'
runs = 10
balls = np.arange(start=15, stop=0, step=-1)

optim = []
rand = []

f = open('temp_cricket_states', 'w')
cmd = "python", "cricket_states.py", "--balls", "15", "--runs", "10"
subprocess.call(cmd, stdout=f)
f.close()

tbc = ['mdpfile', 'optim', 'rand', 'decOptim', 'decRand', 'temp_cricket_states']

f = open('mdpfile', 'w')
cmd = "python", "encoder.py", "--states", "temp_cricket_states", "--parameters", "data/cricket/sample-p1.txt", "--q", str(q)
subprocess.call(cmd, stdout=f)
f.close()

f = open('optim', 'w')
cmd = "python", "planner.py", "--mdp", "mdpfile"
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
    lines = f.readlines()
    for l in lines:
        l = l[:-1]
        l = l.split()
        if(l[0][2:] != '10'):
            continue

        optim.append(float(l[2]))

with open('decRand') as f:
    lines = f.readlines()
    for l in lines:
        l = l[:-1]
        l = l.split()
        if(l[0][2:] != '10'):
            continue

        rand.append(float(l[2]))

for ff in tbc:
    os.remove(ff)

plt.plot(list(balls), rand, '-b', label='Random')
plt.plot(list(balls), optim, '-r', label='Optimal')
plt.legend()
plt.title('Win probability vs. Balls to play')
plt.xlabel('Balls')
plt.ylabel('Win probability')
ax = plt.gca()
ax.set_xlim(ax.get_xlim()[::-1])
plt.savefig('rl_task2_ana3_mod.png')