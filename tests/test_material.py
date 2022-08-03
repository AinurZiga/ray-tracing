
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

import rt
import functions
import numpy as np

_, walls, materials = functions.open_file('./maps/RTS1.map')

assert materials[0] == "Brick"
assert materials[69] == "Flooring"
assert materials[70] == "Ceiling decking"
assert materials[71] == "Metal"

## 2
p1 = [53.7, 73.8, 1.85]   # 504  (case 2)
p2 = [56.7, 73.0, 1.5]

fc = 5.6*10**9
n_walls, faces, segments, DRs, face_ps, face_vs = functions.walls_to_arrays(walls)

ray_tracing = rt.Ray_tracing(p1, walls, materials, 
                n_walls, faces, segments, 
                DRs, face_ps, face_vs, fc,
                'image', 'rigorous')

cr_points, d_facets, materials, type_reflections, idx_walls = ray_tracing._image_method(p1,p2)

assert materials == ['Brick', 'Brick', 'Brick', 'Brick', 'Brick']
assert type_reflections == ['TE', 'TE', 'TE', 'TE', 'TE']
assert idx_walls == [0, 6, 20, 35, 42]

#print(materials)
#print(type_reflections, idx_walls)

## 3
p1 = [53.9, 39.35, 1.45]   # holl  (case 1)
p2 = [53.9, 48.3, 1.45]

cr_points, d_facets, materials, type_reflections, idx_walls = ray_tracing._image_method(p1,p2)

assert np.round(cr_points,2).tolist() == ([[54.75, 43.82,  1.45],
                                            [53.9,  22.9,   1.45],
                                            [53.9,  93.0,   1.45],
                                            [52.15, 43.82,  1.45],
                                            [53.9,  43.82,  0.0],
                                            [53.9,  43.82,  4.0]])

assert np.round(d_facets,2).tolist() == [0.07, 0.07, 0.05, 0.5,  0.3,  0.3 ]
assert materials == ['Brick', 'Brick', 'Brick', 'Metal']
assert type_reflections == ['TE', 'TE', 'TE', 'TE']
assert idx_walls == [7, 40, 45, 71]