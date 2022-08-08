# walls_to_arrays

import sys, os
#sys.path.append("..")
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
import rt
import functions

_, walls, materials = functions.open_file('./maps/RTS1.map')

n_walls, faces, segments, DRs, face_ps, face_vs = functions.walls_to_arrays(walls)

assert len(walls) == n_walls

t1 = faces[:]
t2 = [0]
for i in range(len(walls)):
    t2 += (len(walls[i]) + t2[-1]),

assert t1 == t2
