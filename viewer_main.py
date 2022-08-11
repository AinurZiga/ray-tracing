import viewer as viewer
from PySide2 import QtGui, QtCore, QtWidgets
import numpy as np

import sys
import functions
import rt
 

def double_bounce(cls, p1, p2):
    fc = 5.6*10**9
    n_walls, faces, segments, DRs, face_ps, face_vs = functions.walls_to_arrays(cls.walls_list)
    
    ray_tracing = rt.Ray_tracing(p1, cls.walls_list, cls.materials,
            n_walls, faces, segments, 
            DRs, face_ps, face_vs, fc,
            'image', 'rigorous')
    (cr_points2, d_facets, materials, type_reflections, 
            idx_walls) = ray_tracing._image_method_outer_loop(p1, p2)
    print(len(cr_points2))
    cls.draw_rt_2_bounce(p1, p2, cr_points2)
    return

def single_bounce(cls, p1, p2):
    cls.draw_p1_p2([p1, p2])

    fc = 5.6*10**9
    n_walls, faces, segments, DRs, face_ps, face_vs = functions.walls_to_arrays(cls.walls_list)
    
    ray_tracing = rt.Ray_tracing(p1, cls.walls_list, cls.materials,
            n_walls, faces, segments, 
            DRs, face_ps, face_vs, fc,
            'image', 'rigorous')
    (cr_points, d_facets, materials, type_reflections, 
            idx_walls) = ray_tracing._image_method(p1, p2)
    print(len(cr_points))
    cls.draw_rt_1_bounce(p1, p2, cr_points)
    rays1 = ray_tracing._calc_single_bounce_refl(p1, p2, cr_points, d_facets,
            materials, type_reflections)
    return

def single_and_double(cls, p1, p2):
    #cls.draw_p1_p2([p1, p2])
    fc = 5.6*10**9
    n_walls, faces, segments, DRs, face_ps, face_vs = functions.walls_to_arrays(cls.walls_list)

    ray_tracing = rt.Ray_tracing(p1, cls.walls_list, cls.materials,
        n_walls, faces, segments, 
        DRs, face_ps, face_vs, fc,
        'image', 'rigorous')

    ray0 = ray_tracing._calc_direct_ray(p1, p2)
    print("ray0:", np.abs(ray0))

    (cr_points1, d_facets1, materials1, type_reflections1, 
        idx_walls1) = ray_tracing._image_method(p1, p2)

    rays1 = ray_tracing._calc_single_bounce_refl(p1, p2, cr_points1, d_facets1,
            materials1, type_reflections1)


    (cr_points2, d_facets2, materials2, type_reflections2, 
    		idx_walls2) = ray_tracing._image_method_outer_loop(p1, p2)

    rays2 = ray_tracing._calc_double_bounce_refl(p1, p2, cr_points2, d_facets2,
    			materials2, type_reflections2)

    max_ampl = max(np.abs(ray0), np.max(np.abs(rays1)), np.max(np.abs(rays2)))

    print(20*np.log10(np.abs(ray0)/max_ampl))
    print(np.sort(20*np.log10(np.abs(rays1)/max_ampl)))
    print(np.sort(20*np.log10(np.abs(rays2)/max_ampl)))

    idxs1 = np.where(20*np.log10(np.abs(rays1)/max_ampl) > -25)[0]
    idxs2 = np.where(20*np.log10(np.abs(rays2)/max_ampl) > -25)[0]

    cls.draw_rt_2_bounce(p1, p2, cr_points2, list(idxs2))
    cls.draw_rt_1_bounce(p1, p2, cr_points1, list(idxs1))
    if 20*np.log10(np.abs(ray0)/max_ampl) > -25:
        cls.draw_direct_line(p1, p2)

def draw_cr_points(cls, p1, p2):
    fc = 5.6*10**9
    n_walls, faces, segments, DRs, face_ps, face_vs = functions.walls_to_arrays(cls.walls_list)

    ray_tracing = rt.Ray_tracing(p1, cls.walls_list, cls.materials,
        n_walls, faces, segments, 
        DRs, face_ps, face_vs, fc,
        'image', 'rigorous')

    cr_points = ray_tracing._find_cr_points(p1, p2)
    for p in cr_points:
        cls.draw_p(p)

def get_p1_p2():
    p1 = [54.0, 35.0, 2.5]   # far
    p2 = [59.0, 74.0, 1.0]

    #p1 = [56.5, 69.0, 2.0]   # both in 504
    #p2 = [58.0, 73.0, 1.0]

    #p1 = [53.7, 73.8, 1.5]   # 504  (case 2)
    #p2 = [56.7, 73.0, 1.5]

    #p1 = [53.9, 39.35, 1.85]   # holl  (case 1)
    #p2 = [53.0, 44.75, 1.85]

    #p1 = [52.0, 50.0, 1.0]
    #p2 = [58.0, 55.0, 1.0]
    return p1, p2

def draw_walls(cls):
    filter_idx = []
    cls.draw_walls()
    return

def main_fun(cls):
    p1, p2 = get_p1_p2()
    cls.draw_p1_p2([p1,p2])
    draw_cr_points(cls, p1, p2)
    #single_and_double(cls, p1, p2)
    draw_walls(cls)
    #cls.draw_p([57.66858974358974, 63.61500000000001, 1.3994230769230769])
    return


if __name__ == '__main__':
    print('file planner:', __name__)
    app = QtWidgets.QApplication(sys.argv)
    window = viewer.Window()
    window.show()
    window.center.graphicView.task1('./maps/RTS1.map')
    sys.exit(app.exec_())