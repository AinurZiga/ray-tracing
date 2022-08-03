# image method

import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

import rt
import functions
import numpy as np


p1 = [53.7, 73.8, 1.85]   # 504  (case 2)
p2 = [56.7, 73.0, 1.5]

_, walls, materials = functions.open_file('./maps/RTS1.map')

fc = 5.6*10**9
n_walls, faces, segments, DRs, face_ps, face_vs = functions.walls_to_arrays(walls)

ray_tracing = rt.Ray_tracing(p1, walls, materials, 
                n_walls, faces, segments, 
                DRs, face_ps, face_vs, fc,
                'image', 'rigorous')

#ray_tracing.mimo_channel_matrix()
cr_points, d_facets, materials, type_reflections, idx_walls = ray_tracing._image_method(p1,p2)

#print(d_facets, idx_walls)
assert idx_walls == [0, 6, 20, 35, 42]
