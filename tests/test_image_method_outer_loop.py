
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

import rt
import functions
import numpy as np

_, walls, materials = functions.open_file('./maps/RTS1.map')

fc = 5.6*10**9
n_walls, faces, segments, DRs, face_ps, face_vs = functions.walls_to_arrays(walls)

p1 = [57.0, 69.0, 2.0]   # both in 504
p2 = [58.0, 73.0, 1.0]

ray_tracing = rt.Ray_tracing(p1, walls, materials, 
                n_walls, faces, segments, 
                DRs, face_ps, face_vs, fc,
                'image', 'rigorous')

(cr_points2, d_facets, materials, type_reflections, 
        idx_walls) = ray_tracing._image_method_outer_loop(p1, p2)
print(cr_points2[4], len(cr_points2))

assert len(cr_points2) == 608, print(len(cr_points2))