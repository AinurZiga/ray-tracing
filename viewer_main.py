import planner as viewer
from PySide2 import QtGui, QtCore, QtWidgets
import sys
import functions
import rt


def main_fun(cls):
    foo1(cls)
    return 

def foo(cls):
    p1 = [56.5, 69.0, 2.0]   # both in 504
    p2 = [58.0, 73.0, 1.0]

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

def foo1(cls):
    p1 = [56.5, 69.0, 2.0]   # both in 504
    p2 = [58.0, 73.0, 1.0]

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
    cls.draw_rt_lines(p1, p2, cr_points)
    return

if __name__ == '__main__':
    print('file planner:', __name__)
    app = QtWidgets.QApplication(sys.argv)
    window = viewer.Window()
    window.show()
    window.center.graphicView.task1('./maps/RTS1.map')
    sys.exit(app.exec_())