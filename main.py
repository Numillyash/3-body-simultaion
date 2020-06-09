import concurrent.futures

from body import *
import numpy
from time import *
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

planets = [Body(7.35*10**22,   np.array([28596758000, -24374000, 148936038000]),     np.array([-28300, -11.2, 4860])),
           Body(5.97*10**24,   np.array([28931264000, 8640000, 149095851000]),       np.array([-28800, 0.193, 5790])),
           Body(1.99*10**30,   np.array([0, 0, 0]),                                  np.array([-0.0000000675, -0.000000000887, 0.000000266])),
           Body(3.3 *10**23,   np.array([51324393000, 1308150000, 41624898000]),     np.array([-20700, -4820, 35700])),
           Body(4.87*10**24,   np.array([13676678000, -691724000, 107817729000]),    np.array([-34500, -2060, 4540])),
           Body(6.42*10**23,   np.array([-110228266000, 6444948000, 178021466133]),  np.array([-21500, -220, -14800]))
           ];
#planets = [Body(7.35*10**22, np.array([29063906000 - 29406302000,-24153000-8637000,148855195000-148999465000]), np.array([-28300,-15.4,4930])), Body(5.97*10**24, np.array([0,0,0]), np.array([-28700,0.198,5880]))]
deltaTime = 10000;

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

pos1 = [planets[0].position];
pos2 = [planets[1].position];
pos3 = [planets[2].position];
pos4 = [planets[3].position];
pos5 = [planets[4].position];
pos6 = [planets[5].position];
pos = [pos1,pos2,pos3,pos4,pos5,pos6];
s = time();

for a in range(100000):
    #ans = []
    #print("============================================")
    #s = time()
    #with concurrent.futures.ThreadPoolExecutor() as executor:
    #    ans = [i for i in executor.map(Verlet, planets)]
    #print(time()-s)
    #pos1.append(ans[0]);
    #pos2.append(ans[1]);
    #pos3.append(ans[2]);
    #pos4.append(ans[3]);
    #s = time()
    for i in range(len(planets)):
        newPos = Verlet(planets[i]);
        pos[i].append(newPos);
    #print(time() - s)
    for i in range(len(planets)):
        planets[i].changePosition(pos[i][-1]);
print(time()-s);
fig = plt.figure();
ax = fig.add_subplot(111, projection='3d');
ax.plot([i[0] for i in pos[0]], [i[1] for i in pos[0]], [i[2] for i in pos[0]], label="Луна", color = 'red');
ax.plot([i[0] for i in pos[1]], [i[1] for i in pos[1]], [i[2] for i in pos[1]], label="Земля", color = 'blue');
ax.plot([i[0] for i in pos[2]], [i[1] for i in pos[2]], [i[2] for i in pos[2]], label="Солнце", color = 'green');
ax.plot([i[0] for i in pos[3]], [i[1] for i in pos[3]], [i[2] for i in pos[3]], label="Меркурий", color = 'purple');
ax.plot([i[0] for i in pos[4]], [i[1] for i in pos[4]], [i[2] for i in pos[4]], label="Венера", color = 'yellow');
ax.plot([i[0] for i in pos[5]], [i[1] for i in pos[5]], [i[2] for i in pos[5]], label="Марс", color = 'pink');
size_num = 10**12;
ax.set_zlim(-size_num,size_num);
ax.set_ylim(-size_num,size_num);
ax.set_xlim(-size_num,size_num);
ax.set_title('Движение тел');
ax.legend();

fig.tight_layout();
plt.savefig('Solar.png', format='png', dpi=1000);
print(time()-s);
plt.show();