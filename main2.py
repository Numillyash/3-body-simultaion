import concurrent.futures

from body import *
import numpy
from time import *
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

n = 8

planets = [];
for x in [a for a in range(2*n) if a%2 == 0]:
    for y in [b for b in range(2*n) if b%2 == 0]:
        for z in [c for c in range(2*n) if c%2 == 0]:
            planets.append(Body(1, np.array([x,y,z])))
#planets = [Body(7.35*10**22, np.array([29063906000 - 29406302000,-24153000-8637000,148855195000-148999465000]), np.array([-28300,-15.4,4930])), Body(5.97*10**24, np.array([0,0,0]), np.array([-28700,0.198,5880]))]
deltaTime = 100;

def acceleretion(obj: Body, c_pl):
    acceler = np.zeros(3);
    force = np.zeros(3);
    for i in c_pl:
        force += obj.forceCount(i);
    acceler = force / obj.mass;
    return acceler;

def Verlet(obj: Body):
    cur_pl = [];
    for i in planets:
        if obj != i:
            cur_pl.append(i);
    newPos = np.zeros(3);
    if(obj.stop):
        newPos = obj.position + deltaTime * obj.speed + (deltaTime ** 2) * acceleretion(obj,cur_pl);
        obj.stop = False;
    else:
        newPos = 2 * obj.position - obj.old_position + (deltaTime ** 2) * acceleretion(obj,cur_pl);
    return newPos;


pos = [[planets[j].position] for j in range(n**3)];
s = time();
print("Genered");
for a in range(1000):
    ans = []
    print("============================================")
    s = time()
    with concurrent.futures.ProcessPoolExecutor() as executor:
        ans = [i for i in executor.map(Verlet, planets)]
    print(time()-s)
    for i, l in zip(ans, range(len(ans))):
        pos[l].append(i);
    #s = time()
    #for i in range(len(planets)):
    #    newPos = Verlet(planets[i]);
    #    pos[i].append(newPos);
    #print(time() - s)
    for i in range(len(planets)):
        planets[i].changePosition(pos[i][-1]);
print(time()-s, "done");
fig = plt.figure();
ax = fig.add_subplot(111, projection='3d');
for j in range(n**3):
    ax.plot([i[0] for i in pos[j]], [i[1] for i in pos[j]], [i[2] for i in pos[j]]);

size_num = 10**-1;
ax.set_zlim(-size_num,size_num);
ax.set_ylim(-size_num,size_num);
ax.set_xlim(-size_num,size_num);
ax.set_title('Движение тел');
ax.legend();

fig.tight_layout();
plt.savefig('nonSolar.png', format='png', dpi=1000);
print(time()-s);
plt.show();