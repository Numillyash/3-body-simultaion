import concurrent.futures
from functools import partial
import random
from body import *
import numpy
from time import *
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

deltaTime = 10;
planets = [];

# Print iterations progress
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█'):
    """
    Call in a loop to create terminal progress bar
    @params:
    iteration   - Required  : current iteration (Int)
    total       - Required  : total iterations (Int)
    prefix      - Optional  : prefix string (Str)
    suffix      - Optional  : suffix string (Str)
    decimals    - Optional  : positive number of decimals in percent complete (Int)
    length      - Optional  : character length of bar (Int)
    fill        - Optional  : bar fill character (Str)
    printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s ' % (prefix, bar, percent, suffix), end = '')#, end = printEnd)
    # Print New Line on Complete
    if iteration == total:
        print("")

def acceleretion(obj: Body, c_pl):
    acceler = np.zeros(3);
    force = np.zeros(3);
    for i in c_pl:
        force += obj.forceCount(i);
    acceler = force / obj.mass;
    return acceler;

def Verlet(obj: Body, pl):
    cur_pl = [];
    for i in pl:
        if obj != i:
            cur_pl.append(i);

    newPos = np.zeros(3);
    if(obj.stop):
        newPos = obj.position + deltaTime * obj.speed + (deltaTime ** 2) * acceleretion(obj,cur_pl);
        obj.stop = False;
    else:
        newPos = 2 * obj.position - obj.old_position + (deltaTime ** 2) * acceleretion(obj,cur_pl);
    return newPos;
    pass

def main():
    ans = []
    with concurrent.futures.ProcessPoolExecutor() as executor:
        ans = [i for i in executor.map(partial(Verlet, pl=planets), planets)]
    return ans

if __name__ == '__main__':
    n = 50
    for x in range(n):
        planets.append(Body(10**6, np.array([random.random()*20-10,random.random()*20-10,random.random()*20-10])))
        print(planets[-1])
    # planets = [Body(7.35*10**22, np.array([29063906000 - 29406302000,-24153000-8637000,148855195000-148999465000]), np.array([-28300,-15.4,4930])), Body(5.97*10**24, np.array([0,0,0]), np.array([-28700,0.198,5880]))]

    pos = [[planets[j].position] for j in range(n)];
    s = time();
    print("Genered");
    #bar = progressbar.ProgressBar().start();
    koeff = 1000
    for a in range(koeff):
        #bar.update(a/10);
        printProgressBar(a,koeff,prefix = 'Progress:', suffix = 'Complete', length = 50)
        ans = []
        #print("============================================")
        #s = time()
        ans = main();
        #print(time()-s)
        for i, l in zip(ans, range(len(ans))):
            pos[l].append(i);
        #s = time()
        #for i in range(len(planets)):
        #    newPos = Verlet(planets[i]);
        #    pos[i].append(newPos);
        #print(time() - s)
        for i in range(len(planets)):
            planets[i].changePosition(pos[i][-1]);
    printProgressBar(10, 10, prefix='Progress:', suffix='Complete', length=50)
    #bar.finish();
    print(time()-s, "done");
    fig = plt.figure();
    ax = fig.add_subplot(111, projection='3d');
    for j in range(n):
        ax.plot([i[0] for i in pos[j]], [i[1] for i in pos[j]], [i[2] for i in pos[j]]);
        #print([i[0] for i in pos[j]], [i[1] for i in pos[j]], [i[2] for i in pos[j]])

    size_num = 10**1;
    ax.set_zlim(-size_num,size_num);
    ax.set_ylim(-size_num,size_num);
    ax.set_xlim(-size_num,size_num);
    ax.set_title('Движение тел');
    ax.legend();

    fig.tight_layout();
    plt.savefig('nonSolar.png', format='png', dpi=1000);
    print(time()-s);
    plt.show();