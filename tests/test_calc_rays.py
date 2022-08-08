import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

import rt
import functions
import numpy as np


#p1 = [53.7, 73.8, 1.85]   # 504  (case 2)
#p2 = [56.7, 73.0, 1.5]

#p1 = [56.5, 69.0, 2.0]   # both in 504
#p2 = [58.0, 73.0, 1.0]

p1 = [54.0, 35.0, 2.5]   # far
p2 = [59.0, 74.0, 1.0]

_, walls, materials = functions.open_file('./maps/RTS1.map')

fc = 5.6*10**9
n_walls, faces, segments, DRs, face_ps, face_vs = functions.walls_to_arrays(walls)

ray_tracing = rt.Ray_tracing(p1, walls, materials, 
                n_walls, faces, segments, 
                DRs, face_ps, face_vs, fc,
                'image', 'rigorous')
#ray_tracing.is_ceil_reflection = True
#ray_tracing.is_floor_reflection = True

#(cr_points, d_facets, materials, type_reflections, 
#        idx_walls) = ray_tracing._image_method(p1, p2)
#print("materials:", materials)

ray0 = ray_tracing._calc_direct_ray(p1, p2)
print("ray0:", np.abs(ray0))

(cr_points1, d_facets1, materials1, type_reflections1, 
        idx_walls1) = ray_tracing._image_method(p1, p2)

rays1 = ray_tracing._calc_single_bounce_refl(p1, p2, cr_points1, d_facets1,
            materials1, type_reflections1)


#(cr_points2, d_facets2, materials2, type_reflections2, 
#        idx_walls2) = ray_tracing._image_method_outer_loop(p1, p2)

#rays2 = ray_tracing._calc_double_bounce_refl(p1, p2, cr_points2, d_facets2,
#            materials2, type_reflections2)

#max_ampl = max(np.abs(ray0), np.max(np.abs(rays1)))
max_ampl = np.abs(ray0)
#print(np.abs((ray0, rays1)/max_ampl))

print(20*np.log10(np.abs(rays1)/max_ampl))
#print(20*np.log10(np.abs(rays2)/max_ampl))