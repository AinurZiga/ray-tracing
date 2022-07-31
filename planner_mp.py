#coding = utf-8


from PySide2 import QtGui, QtCore, QtWidgets
import numpy as np
import multiprocessing

import os
import sys
import timeit
import operator
import values5 as values
import math
import local_eng as local

class Window(QtWidgets.QMainWindow):

    #resized = QtCore.Signal()

    def __init__(self):
        super().__init__()

        self.title = "Wi-Fi Planner"
        self.top = 150
        self.left = 150
        self.width = 800
        self.height = 600
        self.zoom = 0
        #self.showMaximized()
        #self.showFullScreen()
        #self.resized.connect(self.move_legend)
        #values.initVar("WIFi.log")
        self.InitWindow()

    def resizeEvent(self, event):
        #self.resized.emit()
        return super(Window, self).resizeEvent(event)

    def move_legend(self):
        print("move1")
        size = self.size()
        print(size)
        #self.center.graphicView.legend.setPosition(QtCore.QPoint(size))
        try:
            print("move2")
            #self.center.graphicView.legend.setPosition(QtCore.QPoint(size))
            self.center.graphicView.legend.move(self.size.width(),
                        self.size.height())
        except:
            print("exception")


    def InitWindow(self):
        #self.setWindowIcon(QtGui.QIcon("icon.png"))
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        print(self.size())

        #self.menubar = self.menuBar()
        self.menubar = self.menuBar()
        self.toolbar = self.addToolBar('Toolbar')
        self.createGraphicView()
        #self.statusBar().showMessage("Hello")

        # File
        self.fileMenu = self.menubar.addMenu(local.menu_file)

        self.openFileAction = QtWidgets.QAction(local.open_map, self)
        self.openFileAction.triggered.connect(self.center.graphicView.openFileNameDialog)
        self.fileMenu.addAction(self.openFileAction)

        self.openNet = QtWidgets.QAction(local.open_net, self)
        self.openNet.triggered.connect(self.center.graphicView.openNet)
        self.fileMenu.addAction(self.openNet)
        #self.openNet.setDisabled(True)

        self.importFileAction_img = QtWidgets.QAction(local.import_img, self)
        self.importFileAction_img.triggered.connect(
                        self.center.graphicView.openFileNameDialog_import_image)
        self.fileMenu.addAction(self.importFileAction_img)

        self.importFileAction_dxf = QtWidgets.QAction(local.import_dxf, self)
        self.importFileAction_dxf.triggered.connect(
                        self.center.graphicView.openFileNameDialog_import_dxf)
        self.fileMenu.addAction(self.importFileAction_dxf)

        #self.newFileAction = QtWidgets.QAction(local.new_map, self)
        #self.newFileAction.triggered.connect(self.center.graphicView.task2)
        #self.fileMenu.addAction(self.newFileAction)

        self.saveFileAction = QtWidgets.QAction(local.save_map, self)
        self.saveFileAction.triggered.connect(self.center.graphicView.saveFile)
        self.fileMenu.addAction(self.saveFileAction)
        #self.saveFileAction.setDisabled(True)

        self.saveNet = QtWidgets.QAction(local.save_net, self)
        self.saveNet.triggered.connect(self.center.graphicView.saveNet)
        self.fileMenu.addAction(self.saveNet)
        #self.saveNet.setDisabled(True)

        #self.newNet = QtWidgets.QAction(local.new_net, self)
        #self.newNet.triggered.connect(self.center.graphicView.newNet)
        #self.fileMenu.addAction(self.newNet)
        #self.newNet.setDisabled(True)

        self.file_parameters = QtWidgets.QAction(local.parameters, self)
        self.file_parameters.triggered.connect(self.center.graphicView.file_parameters)
        self.fileMenu.addAction(self.file_parameters)
        #self.file_parameters.setDisabled(True)

        self.file_exit = QtWidgets.QAction(local.exit, self)
        self.file_exit.triggered.connect(self.center.graphicView.file_exit)
        self.fileMenu.addAction(self.file_exit)
        #self.file_exit.setDisabled(True)

        # Edit
        self.editMenu = self.menubar.addMenu(local.menu_edit)

        self.coverage_area = QtWidgets.QAction(local.service_zone, self)
        self.coverage_area.triggered.connect(self.center.graphicView.add_coverage_area)
        self.editMenu.addAction(self.coverage_area)
        #self.coverage_area.setDisabled(True)

        self.rect_wall = QtWidgets.QAction(local.wall, self)
        #self.rect.setIcon(QIcon("rect.jpg"))
        self.rect_wall.triggered.connect(self.center.graphicView.add_wall)
        self.editMenu.addAction(self.rect_wall)
        #self.rect_wall.setDisabled(True)

        self.rect_window = QtWidgets.QAction(local.window, self)
        #self.rect.setIcon(QIcon("rect.jpg"))
        self.rect_window.triggered.connect(self.center.graphicView.add_window)
        self.editMenu.addAction(self.rect_window)
        #self.rect_window.setDisabled(True)

        self.rect_door = QtWidgets.QAction(local.door, self)
        #self.rect.setIcon(QIcon("rect.jpg"))
        self.rect_door.triggered.connect(self.center.graphicView.add_door)
        self.editMenu.addAction(self.rect_door)
        #self.rect_door.setDisabled(True)

        self.polygon = QtWidgets.QAction(local.polygon, self)
        #self.polygon.setIcon(QIcon("poly.jpg"))
        self.polygon.triggered.connect(self.center.graphicView.add_poly)
        self.editMenu.addAction(self.polygon)
        #self.polygon.setDisabled(True)

        self.edit_parameters = QtWidgets.QAction(local.edit_parameters, self)
        self.edit_parameters.triggered.connect(self.center.graphicView.edit_parameters)
        self.editMenu.addAction(self.edit_parameters)
        #self.edit_parameters.setDisabled(True)

        self.enableEditing = QtWidgets.QAction(local.en_editing, self)
        self.enableEditing.setCheckable(True)
        self.enableEditing.triggered.connect(self.center.graphicView.enableEditing)
        self.center.graphicView.isEditing = False
        self.editMenu.addAction(self.enableEditing)

        self.show_image = QtWidgets.QAction(local.del_img, self)
        self.show_image.setCheckable(True)
        self.show_image.triggered.connect(self.center.graphicView.change_image_state)
        self.editMenu.addAction(self.show_image)
        #self.show_image.setDisabled(True)

        # Planning
        self.planningMenu = self.menubar.addMenu(local.menu_planning)
        #self.planningMenu.setDisabled(True)

        self.analyse_points_update = QtWidgets.QAction(local.get_map_point, self)
        self.analyse_points_update.triggered.connect(self.center.graphicView.analyse_points_update)
        self.planningMenu.addAction(self.analyse_points_update)
        #self.analyse_points_update.setDisabled(True)

        self.new_AP_menu = self.planningMenu.addMenu(local.placement_ap)
        #self.new_AP_menu.setDisabled(True)

        self.new_AP = QtWidgets.QAction(local.manual_placement, self)
        self.new_AP.triggered.connect(self.center.graphicView.add_AP)
        self.new_AP_menu.addAction(self.new_AP)

        self.clear_AP = QtWidgets.QAction(local.clear, self)
        self.clear_AP.triggered.connect(self.center.graphicView.clear_AP)
        self.new_AP_menu.addAction(self.clear_AP)


        self.new_userMenu = self.planningMenu.addMenu(local.placement_user)
        #self.new_userMenu.setDisabled(True)

        self.new_user_auto = QtWidgets.QAction(local.auto, self)
        self.new_user_auto.triggered.connect(self.center.graphicView.add_new_user_auto)
        self.new_userMenu.addAction(self.new_user_auto)

        self.new_user_uniform = QtWidgets.QAction(local.uniform, self)
        self.new_user_uniform.triggered.connect(self.center.graphicView.add_new_user_uniform)
        self.new_userMenu.addAction(self.new_user_uniform)

        self.new_user_manually = QtWidgets.QAction(local.manual, self)
        self.new_user_manually.triggered.connect(self.center.graphicView.add_new_user_manually)
        self.new_userMenu.addAction(self.new_user_manually)

        self.clear_user = QtWidgets.QAction(local.clear, self)
        self.clear_user.triggered.connect(self.center.graphicView.clear_user)
        self.new_userMenu.addAction(self.clear_user)


        self.planning_parameters = QtWidgets.QAction(local.plan_parameters, self)
        self.planning_parameters.triggered.connect(self.center.graphicView.planning_parameters)
        self.planningMenu.addAction(self.planning_parameters)
        #self.planning_parameters.setDisabled(True)

        self.helping_panel = QtWidgets.QAction(local.pop_up, self)
        self.helping_panel.setCheckable(True)
        self.helping_panel.triggered.connect(self.center.right.right_change_state)
        self.planningMenu.addAction(self.helping_panel)
        #self.helping_panel.setDisabled(True)

        self.show_hide_points = QtWidgets.QAction(local.hide_anp, self)
        self.show_hide_points.setCheckable(True)
        self.show_hide_points.triggered.connect(self.center.graphicView.changePointsState)
        self.planningMenu.addAction(self.show_hide_points)
        #self.show_hide_points.setDisabled(True)




        # analyse
        self.analyseMenu = self.menubar.addMenu(local.menu_analysis)

        #self.start_analyse = QtWidgets.QAction('Run', self)
        #self.start_analyse.triggered.connect(self.center.graphicView.start_analyse)
        #self.analyseMenu.addAction(self.start_analyse)

        self.get_map = QtWidgets.QAction(local.get_map, self)
        self.get_map.triggered.connect(self.center.graphicView.get_map)
        self.analyseMenu.addAction(self.get_map)

        self.analyse_parameters = QtWidgets.QAction(local.an_parameters, self)
        self.analyse_parameters.triggered.connect(self.center.graphicView.analyse_parameters)
        self.analyseMenu.addAction(self.analyse_parameters)

        # Report
        self.reportMenu = self.menubar.addMenu(local.menu_report)

        self.report_on_map = QtWidgets.QAction(local.on_map, self)
        self.report_on_map.triggered.connect(self.center.graphicView.get_map)
        self.reportMenu.addAction(self.report_on_map)

        self.report_window = QtWidgets.QAction(local.report, self)
        self.report_window.triggered.connect(self.center.graphicView.report_window)
        self.reportMenu.addAction(self.report_window)
        #self.output_window.setDisabled(True)

        self.report_parameters = QtWidgets.QAction(local.rep_parameters, self)
        self.report_parameters.triggered.connect(self.center.graphicView.report_parameters)
        self.reportMenu.addAction(self.report_parameters)

        # Help
        #self.helpMenu = self.menubar.addMenu(local.help)

        self.show()
        self.disable_beginning_actions()
        self.add_toolbar()

    def add_toolbar(self):
        self.__file_toolbar()
        self.__edit_toolbar()
        self.__planning_toolbar()
        self.__analyse_toolbar()
        self.__report_toolbar()
        self.__automation_toolbar()

    def __file_toolbar(self):
        # creating tollbuttons
        self.open_toolbutton = QtWidgets.QToolButton(self)
        self.open_toolbutton.setPopupMode(QtWidgets.QToolButton.InstantPopup)
        self.toolbar.addWidget(self.open_toolbutton)
        self.open_toolbutton.setIcon(QtGui.QIcon("./icons/open.png"))

        self.save_toolbutton = QtWidgets.QToolButton(self)
        self.save_toolbutton.setPopupMode(QtWidgets.QToolButton.InstantPopup)
        self.toolbar.addWidget(self.save_toolbutton)
        self.save_toolbutton.setIcon(QtGui.QIcon("./icons/save.png"))

        self.import_toolbutton = QtWidgets.QToolButton(self)
        self.import_toolbutton.setPopupMode(QtWidgets.QToolButton.InstantPopup)
        self.toolbar.addWidget(self.import_toolbutton)
        self.import_toolbutton.setIcon(QtGui.QIcon("./icons/import.png"))

        # creating menus for toolbuttons
        self.open_toolbutton_menu = QtWidgets.QMenu(self)
        self.open_toolbutton_menu.addAction(self.openFileAction)
        self.open_toolbutton_menu.addAction(self.openNet)
        self.open_toolbutton.setMenu(self.open_toolbutton_menu)

        self.save_toolbutton_menu = QtWidgets.QMenu(self)
        self.save_toolbutton_menu.addAction(self.saveFileAction)
        self.save_toolbutton_menu.addAction(self.saveNet)
        self.save_toolbutton.setMenu(self.save_toolbutton_menu)

        self.import_toolbutton_menu = QtWidgets.QMenu(self)
        self.import_toolbutton_menu.addAction(self.importFileAction_img)
        self.import_toolbutton_menu.addAction(self.importFileAction_dxf)
        self.import_toolbutton_menu.addAction(self.show_image)
        self.import_toolbutton.setMenu(self.import_toolbutton_menu)

        self.toolbar.addSeparator()

    def __edit_toolbar(self):
        # creating tollbuttons
        self.rect_toolbutton = QtWidgets.QToolButton(self)
        self.rect_toolbutton.setPopupMode(QtWidgets.QToolButton.InstantPopup)
        self.toolbar.addWidget(self.rect_toolbutton)
        self.rect_toolbutton.setIcon(QtGui.QIcon("./icons/rect.png"))

        self.poly_toolbutton = QtWidgets.QToolButton(self)
        self.poly_toolbutton.setPopupMode(QtWidgets.QToolButton.InstantPopup)
        self.toolbar.addWidget(self.poly_toolbutton)
        self.poly_toolbutton.setIcon(QtGui.QIcon("./icons/poly.png"))

        # creating menus for toolbuttons
        self.rect_toolbutton_menu = QtWidgets.QMenu(self)
        self.rect_toolbutton_menu.addAction(self.rect_wall)
        self.rect_toolbutton_menu.addAction(self.rect_window)
        self.rect_toolbutton_menu.addAction(self.rect_door)
        self.rect_toolbutton.setMenu(self.rect_toolbutton_menu)

        self.poly_toolbutton_menu = QtWidgets.QMenu(self)
        self.poly_toolbutton_menu.addAction(self.coverage_area)
        self.poly_toolbutton_menu.addAction(self.polygon)
        self.poly_toolbutton.setMenu(self.poly_toolbutton_menu)

        self.toolbar.addSeparator()

    def __planning_toolbar(self):
        # creating tollbuttons
        self.points_toolbutton = QtWidgets.QToolButton(self)
        self.points_toolbutton.setPopupMode(QtWidgets.QToolButton.InstantPopup)
        self.toolbar.addWidget(self.points_toolbutton)
        self.points_toolbutton.setIcon(QtGui.QIcon("./icons/dots.png"))

        self.ap_toolbutton = QtWidgets.QToolButton(self)
        self.ap_toolbutton.setPopupMode(QtWidgets.QToolButton.InstantPopup)
        self.toolbar.addWidget(self.ap_toolbutton)
        self.ap_toolbutton.setIcon(QtGui.QIcon("./icons/ap.png"))

        self.user_toolbutton = QtWidgets.QToolButton(self)
        self.user_toolbutton.setPopupMode(QtWidgets.QToolButton.InstantPopup)
        self.toolbar.addWidget(self.user_toolbutton)
        self.user_toolbutton.setIcon(QtGui.QIcon("./icons/user.png"))

        # creating menus for toolbuttons
        self.points_toolbutton_menu = QtWidgets.QMenu(self)
        self.points_toolbutton_menu.addAction(self.analyse_points_update)
        self.points_toolbutton_menu.addAction(self.planning_parameters)
        self.points_toolbutton.setMenu(self.points_toolbutton_menu)

        self.ap_toolbutton_menu = QtWidgets.QMenu(self)
        self.ap_toolbutton_menu.addAction(self.new_AP)
        self.ap_toolbutton_menu.addAction(self.clear_AP)
        self.ap_toolbutton.setMenu(self.ap_toolbutton_menu)

        self.user_toolbutton_menu = QtWidgets.QMenu(self)
        self.user_toolbutton_menu.addAction(self.new_user_auto)
        self.user_toolbutton_menu.addAction(self.new_user_uniform)
        self.user_toolbutton_menu.addAction(self.new_user_manually)
        self.user_toolbutton_menu.addAction(self.clear_user)
        self.user_toolbutton.setMenu(self.user_toolbutton_menu)

        self.toolbar.addSeparator()

    def __analyse_toolbar(self):
        # creating tollbuttons
        self.analyse_toolbutton = QtWidgets.QToolButton(self)
        self.analyse_toolbutton.setPopupMode(QtWidgets.QToolButton.InstantPopup)
        self.toolbar.addWidget(self.analyse_toolbutton)
        self.analyse_toolbutton.setIcon(QtGui.QIcon("./icons/analysis.png"))

        # creating menus for toolbuttons
        self.analyse_toolbutton_menu = QtWidgets.QMenu(self)
        #self.analyse_toolbutton_menu.addAction(self.start_analyse)
        self.analyse_toolbutton_menu.addAction(self.get_map)
        self.analyse_toolbutton_menu.addAction(self.analyse_parameters)
        self.analyse_toolbutton.setMenu(self.analyse_toolbutton_menu)

        self.toolbar.addSeparator()

    def __report_toolbar(self):
        # creating tollbuttons
        self.report_toolbutton = QtWidgets.QToolButton(self)
        self.report_toolbutton.setPopupMode(QtWidgets.QToolButton.InstantPopup)
        self.toolbar.addWidget(self.report_toolbutton)
        self.report_toolbutton.setIcon(QtGui.QIcon("./icons/report.png"))

        # creating menus for toolbuttons
        self.report_toolbutton_menu = QtWidgets.QMenu(self)
        #self.report_toolbutton_menu.addAction(self.get_map)
        self.report_toolbutton_menu.addAction(self.report_window)
        self.report_toolbutton_menu.addAction(self.report_parameters)
        self.report_toolbutton.setMenu(self.report_toolbutton_menu)

    def __automation_toolbar(self):
        self.automation_toolbutton = QtWidgets.QToolButton(self)
        self.automation_toolbutton.setPopupMode(QtWidgets.QToolButton.InstantPopup)
        #self.toolbar.addWidget(self.automation_toolbutton)  todo
        #self.automation_toolbutton.setIcon(QtGui.QIcon("./icons/report.png"))
        self.automation_action = QtWidgets.QAction("Auto")
        self.automation_action.triggered.connect(
                                self.center.graphicView.automation_on)
        #self.automation_toolbutton.triggered.connect(
        #                        self.center.graphicView.automation_on)
        self.automation_action.setIcon(QtGui.QIcon("./icons/automation.png"))
        self.toolbar.addAction(self.automation_action)
        self.automation_toolbutton.addAction(self.automation_action)


    def disable_beginning_actions(self):
        self.saveFileAction.setDisabled(True)
        self.saveNet.setDisabled(True)
        #self.newNet.setDisabled(True)
        self.openNet.setDisabled(True)
        #self.file_parameters.setDisabled(True)
        #self.file_exit.setDisabled(True)
        self.coverage_area.setDisabled(True)
        self.rect_wall.setDisabled(True)
        self.rect_window.setDisabled(True)
        self.rect_door.setDisabled(True)
        self.polygon.setDisabled(True)
        self.edit_parameters.setDisabled(True)
        self.enableEditing.setDisabled(True)
        self.new_AP_menu.setDisabled(True)
        self.new_AP.setDisabled(True)
        self.clear_AP.setDisabled(True)
        self.new_user_auto.setDisabled(True)
        self.new_user_uniform.setDisabled(True)
        self.new_user_manually.setDisabled(True)
        self.clear_user.setDisabled(True)
        self.new_userMenu.setDisabled(True)
        self.planning_parameters.setDisabled(True)
        self.analyse_points_update.setDisabled(True)
        self.helping_panel.setDisabled(True)
        self.show_hide_points.setDisabled(True)
        self.show_image.setDisabled(True)  ###
        self.get_map.setDisabled(True)
        #self.start_analyse.setDisabled(True)
        self.analyse_parameters.setDisabled(True)
        self.report_on_map.setDisabled(True)
        self.report_window.setDisabled(True)
        self.report_parameters.setDisabled(True)

    def update_actions(self):
        if self.center.graphicView.isImageShow:
            self.show_image.setEnabled(True)

        if self.center.graphicView.isCoverageDone:
            self.saveFileAction.setEnabled(True)
            self.saveNet.setEnabled(True)
            #self.newNet.setEnabled(True)
            self.openNet.setEnabled(True)
            self.file_parameters.setEnabled(True)
            self.file_exit.setEnabled(True)

            self.coverage_area.setEnabled(True)
            self.rect_wall.setEnabled(True)
            self.rect_window.setEnabled(True)
            self.rect_door.setEnabled(True)
            self.polygon.setEnabled(True)
            self.edit_parameters.setEnabled(True)
            self.enableEditing.setEnabled(True)

            self.new_AP_menu.setEnabled(True)
            self.new_userMenu.setEnabled(True)
            self.new_AP.setEnabled(True)
            self.clear_AP.setEnabled(True)
            self.new_user_auto.setEnabled(True)
            self.new_user_uniform.setEnabled(True)
            self.new_user_manually.setEnabled(True)
            self.clear_user.setEnabled(True)
            self.planning_parameters.setEnabled(True)
            self.analyse_points_update.setEnabled(True)
            self.helping_panel.setEnabled(True)
            self.show_hide_points.setEnabled(True)

            #self.start_analyse.setEnabled(True)
            self.get_map.setEnabled(True)
            self.analyse_parameters.setEnabled(True)
            self.report_on_map.setEnabled(True)
            self.report_window.setEnabled(True)
            self.report_parameters.setEnabled(True)

            self.get_map.setEnabled(True)
            self.analyse_parameters.setEnabled(True)
            self.report_on_map.setEnabled(True)
            self.report_window.setEnabled(True)
            self.report_parameters.setEnabled(True)

    def createGraphicView(self):
        self.center = CentralWidget(self)
        self.setCentralWidget(self.center)
        self.greenBrush = QtGui.QBrush(QtCore.Qt.green)
        self.grayBrush = QtGui.QBrush(QtCore.Qt.gray)

        self.pen = QtGui.QPen(QtCore.Qt.green)

        self.myMessage = QtWidgets.QLabel()
        self.myMessage.setText("Hello")
        self.statusBar().addWidget(self.myMessage)
        self.center.toolbar_label()

    def show_status_bar(self):
        self.myMessage.setText("")
        if self.center.graphicView.addition == 'AP':
            self.myMessage.setText(local.sb_ap)
        elif self.center.graphicView.addition == 'user':
            self.myMessage.setText(local.sb_user)
        elif self.center.graphicView.isImage:
            self.myMessage.setText(local.sb_rect_start)
        elif self.center.graphicView.isImaging:
            self.myMessage.setText(local.sb_rect_finish)
        elif self.center.graphicView.isRect:
            self.myMessage.setText(local.sb_rect_start)
        elif self.center.graphicView.isRecting:
            self.myMessage.setText(local.sb_rect_finish)
        elif self.center.graphicView.isPoly:
            self.myMessage.setText(local.sb_poly_start)
        elif self.center.graphicView.isPolying:
            self.myMessage.setText(local.sb_poly_continue)
        elif self.center.graphicView.isMoving:
            self.myMessage.setText(local.sb_move)
        else:
            self.myMessage.setText("")
        return



class CentralWidget(QtWidgets.QWidget):
    def __init__(self, parent):
        self.parent = parent
        super().__init__()
        layout = QtWidgets.QHBoxLayout(self)
        #self.standards = ['802.11a', '802.11ac', '802.11ax']
        #self.standards = values.GetStandarts()
        self.materials = [local.brick, local.concrete, local.drywall,
                    local.metall, local.wood]
        self.right = Right(self)
        self.graphicView = GraphicsView(self, self.right)


        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(3)
        self.graphicView.setSizePolicy(sizePolicy)

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        self.right.setSizePolicy(sizePolicy)

        layout.addWidget(self.graphicView)
        layout.addWidget(self.right)
        #layout.addWidget(self.legend)
        self.setLayout(layout)

    def toolbar_label(self):
        self.lbl = QtWidgets.QLabel()
        self.parent.statusBar().addPermanentWidget(self.lbl)
        self.lbl.setFixedSize(1000, 25)
        print("lbl added")

class Right(QtWidgets.QWidget):
    def __init__(self, parent):
        super().__init__()

        self.parent = parent
        self.state = False
        self.hide()
        self.isFirstRow_user = False
        self.isFirstRow_ap = False

        self.layout = QtWidgets.QVBoxLayout(self)
        self.tabs = QtWidgets.QTabWidget()

        self.tab_ap = QtWidgets.QScrollArea()
        self.tab_ap.content = QtWidgets.QWidget()
        self.tab_ap.setWidget(self.tab_ap.content)
        self.tab_ap.setWidgetResizable(True)

        self.tab_user = QtWidgets.QScrollArea()
        self.tab_user.content = QtWidgets.QWidget()
        self.tab_user.setWidget(self.tab_user.content)
        self.tab_user.setWidgetResizable(True)

        self.tabs.addTab(self.tab_ap, local.ap)
        self.tabs.addTab(self.tab_user, local.users)

        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)


        self.sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum,
                                        QtWidgets.QSizePolicy.Minimum)
        #self.sizePolicy.setHorizontalStretch(1)

        self.lines_ap = []
        self.lines_user = []

        self.tab_ap.grid_ap = QtWidgets.QGridLayout(self.tab_ap.content)
        self.tab_ap.grid_ap.setSpacing(0)
        self.tab_ap.grid_ap.setContentsMargins(0, 0, 0, 0)

        self.tab_user.grid_user = QtWidgets.QGridLayout(self.tab_user.content)
        self.tab_user.grid_user.setSpacing(0)
        self.tab_user.grid_user.setContentsMargins(0, 0, 0, 0)


        self.ap_box_base = QtWidgets.QComboBox()
        #self.ap_box_base.addItems(self.parent.standards)
        self.ap_boxes = []

        self.tab_ap.grid_ap.setRowStretch(100, 1)
        self.tab_ap.grid_ap.setColumnStretch(0,1)
        self.tab_ap.grid_ap.setSpacing(2)

        self.tab_user.grid_user.setRowStretch(100, 1)
        self.tab_user.grid_user.setColumnStretch(0,1)
        self.tab_user.grid_user.setSpacing(2)

    def add_first_row_ap(self):
        print("create")
        self.isFirstRow_ap = True
        self.btn_update_ap = QtWidgets.QPushButton(local.update)
        self.btn_update_ap.clicked.connect(self.ap_update)
        self.tab_ap.grid_ap.addWidget(self.btn_update_ap, 0, 3, 1, 1,
                            alignment=(QtCore.Qt.AlignTop | QtCore.Qt.AlignRight))

        self.btn_discard_ap = QtWidgets.QPushButton(local.discard)
        self.btn_discard_ap.clicked.connect(self.ap_discard)
        self.tab_ap.grid_ap.addWidget(self.btn_discard_ap, 0, 4, 1, 1)
        label1 = QtWidgets.QLabel(local.nomer)
        label2 = QtWidgets.QLabel(local.ap)
        label3 = QtWidgets.QLabel(local.x)
        label4 = QtWidgets.QLabel(local.y)
        label5 = QtWidgets.QLabel(local.h)
        label6 = QtWidgets.QLabel(local.height)
        label7 = QtWidgets.QLabel(local.freq)
        self.tab_ap.grid_ap.addWidget(label1, 1, 0)
        self.tab_ap.grid_ap.addWidget(label2, 1, 2)
        self.tab_ap.grid_ap.addWidget(label3, 1, 3)
        self.tab_ap.grid_ap.addWidget(label4, 1, 4)
        self.tab_ap.grid_ap.addWidget(label5, 1, 5)
        self.tab_ap.grid_ap.addWidget(label6, 1, 6)
        self.tab_ap.grid_ap.addWidget(label7, 1, 7)

    def add_first_row_user(self):
        self.isFirstRow_user = True
        self.btn_update_user = QtWidgets.QPushButton(local.update)
        self.btn_update_user.clicked.connect(self.user_update)
        self.tab_user.grid_user.addWidget(self.btn_update_user, 0, 2, 1, 1,
                            alignment=(QtCore.Qt.AlignTop | QtCore.Qt.AlignRight))

        self.btn_discard_user = QtWidgets.QPushButton(local.discard)
        self.btn_discard_user.clicked.connect(self.user_discard)
        self.tab_user.grid_user.addWidget(self.btn_discard_user, 0, 3, 1, 1)
        label1 = QtWidgets.QLabel(local.nomer)
        label2 = QtWidgets.QLabel(local.x)
        label3 = QtWidgets.QLabel(local.y)
        label4 = QtWidgets.QLabel(local.h)
        label5 = QtWidgets.QLabel(local.height)
        label6 = QtWidgets.QLabel(local.dl)
        label7 = QtWidgets.QLabel(local.ul)
        self.tab_user.grid_user.addWidget(label1, 1, 0)
        self.tab_user.grid_user.addWidget(label2, 1, 2)
        self.tab_user.grid_user.addWidget(label3, 1, 3)
        self.tab_user.grid_user.addWidget(label4, 1, 4)
        self.tab_user.grid_user.addWidget(label5, 1, 5)
        self.tab_user.grid_user.addWidget(label6, 1, 6)
        self.tab_user.grid_user.addWidget(label7, 1, 7)

    def ap_discard(self):
        self.fill_LE_aps(self.parent.graphicView.access_points)

    def user_discard(self):
        self.fill_LE_users(self.parent.graphicView.users)


    def right_change_state(self):
        if self.state:
            self.hide()
            self.state = False
        else:
            self.show()
            self.state = True

    def clear_AP(self):
        for i in reversed(range(2, self.tab_ap.grid_ap.count())):
            self.tab_ap.grid_ap.itemAt(i).widget().setParent(None)
        self.lines_ap = []

    def clear_AK(self):
        for i in reversed(range(2, self.tab_user.grid_user.count())):
            self.tab_user.grid_user.itemAt(i).widget().setParent(None)
        self.lines_user = []

    def ap_update(self):
        self.parent.graphicView.ap_update()

    def add_LE_ap(self, ap, ap_type = 1):
        #if len(self.parent.graphicView.access_points) == 1:
        #    self.add_first_row_ap()
        print(self.isFirstRow_ap)
        if not self.isFirstRow_ap:
            self.add_first_row_ap()

        if len(self.parent.graphicView.access_points) > len(self.lines_ap):
            self.line1 = QtWidgets.QDoubleSpinBox()
            self.line1.setRange(-999.99, 999.99)
            self.line1.setSizePolicy(self.sizePolicy)
            self.line2 = QtWidgets.QDoubleSpinBox()
            self.line2.setRange(-999.99, 999.99)
            self.line3 = QtWidgets.QDoubleSpinBox()
            self.line3.setRange(-99.99, 99.99)
            self.line4 = QtWidgets.QDoubleSpinBox()
            self.line4.setRange(-99.99, 99.99)
            self.line5 = QtWidgets.QDoubleSpinBox()
            self.line5.setRange(0, 9999)

            self.lines_ap.append([self.line1, self.line2, self.line3, self.line4, self.line5])

        #i = len(self.parent.graphicView.access_points)-1
        i = len(self.lines_ap) - 1
        self.ap_box = QtWidgets.QComboBox()
        #self.standards = ['802.11a', '802.11ac', '802.11ax']
        #self.ap_box.addItems(self.parent.standards)
        self.ap_box.setCurrentIndex(ap[5])
        self.ap_boxes.append(self.ap_box)

        self.tab_ap.grid_ap.addWidget(QtWidgets.QLabel(str(i+1)+'.'), i+2, 1)
        self.tab_ap.grid_ap.addWidget(self.ap_boxes[i], i+2, 2)
        self.tab_ap.grid_ap.addWidget(self.lines_ap[i][0], i+2, 3, alignment=QtCore.Qt.AlignTop)
        self.tab_ap.grid_ap.addWidget(self.lines_ap[i][1], i+2, 4, alignment=QtCore.Qt.AlignTop)
        self.tab_ap.grid_ap.addWidget(self.lines_ap[i][2], i+2, 5, alignment=QtCore.Qt.AlignTop)
        self.tab_ap.grid_ap.addWidget(self.lines_ap[i][3], i+2, 6, alignment=QtCore.Qt.AlignTop)
        self.tab_ap.grid_ap.addWidget(self.lines_ap[i][4], i+2, 7, alignment=QtCore.Qt.AlignTop)
        print(ap)

        self.fill_LE_ap(ap, i)

    def fill_LE_ap(self, ap, idx):
        self.lines_ap[idx][0].setValue(round(ap[0], 2))
        self.lines_ap[idx][1].setValue(round(ap[1], 2))
        self.lines_ap[idx][2].setValue(round(ap[2], 2))
        self.lines_ap[idx][3].setValue(round(ap[3], 2))
        self.lines_ap[idx][4].setValue(round(ap[4], 2))


    def fill_LE_aps(self, access_points):
        length = len(access_points)
        for i in range(length):
            self.lines_ap[i][0].setValue(round(access_points[i][0], 2))
            self.lines_ap[i][1].setValue(round(access_points[i][1], 2))
            self.lines_ap[i][2].setValue(round(access_points[i][2], 2))
            self.lines_ap[i][3].setValue(round(access_points[i][3], 2))
            self.lines_ap[i][4].setValue(round(access_points[i][4], 2))

    def user_update(self):
        self.parent.graphicView.user_update()

    def add_LE_user(self, user):
        if not self.isFirstRow_user:
            self.add_first_row_user()

        if len(self.parent.graphicView.users) > len(self.lines_user):
            self.line1 = QtWidgets.QDoubleSpinBox()
            self.line1.setRange(-999.99, 999.99)
            self.line2 = QtWidgets.QDoubleSpinBox()
            self.line2.setRange(-999.99, 999.99)
            self.line3 = QtWidgets.QDoubleSpinBox()
            self.line3.setRange(-99.99, 99.99)
            self.line4 = QtWidgets.QDoubleSpinBox()
            self.line4.setRange(-99.99, 99.99)
            self.line5 = QtWidgets.QDoubleSpinBox()
            self.line5.setRange(0, 999)
            self.line6 = QtWidgets.QDoubleSpinBox()
            self.line6.setRange(0, 999)



            self.lines_user.append([self.line1, self.line2, self.line3, self.line4, self.line5, self.line6])

        i = len(self.lines_user) -1

        self.tab_user.grid_user.addWidget(QtWidgets.QLabel(str(i+1)+'.'), i+2, 1)
        self.tab_user.grid_user.addWidget(self.lines_user[i][0], i+2, 2, alignment=QtCore.Qt.AlignTop)
        self.tab_user.grid_user.addWidget(self.lines_user[i][1], i+2, 3, alignment=QtCore.Qt.AlignTop)
        self.tab_user.grid_user.addWidget(self.lines_user[i][2], i+2, 4, alignment=QtCore.Qt.AlignTop)
        self.tab_user.grid_user.addWidget(self.lines_user[i][3], i+2, 5, alignment=QtCore.Qt.AlignTop)
        self.tab_user.grid_user.addWidget(self.lines_user[i][4], i+2, 6, alignment=QtCore.Qt.AlignTop)
        self.tab_user.grid_user.addWidget(self.lines_user[i][5], i+2, 7, alignment=QtCore.Qt.AlignTop)

        self.fill_LE_user(user, i)

    def fill_LE_user(self, user, idx):
        self.lines_user[idx][0].setValue(round(user[0], 2))
        self.lines_user[idx][1].setValue(round(user[1], 2))
        self.lines_user[idx][2].setValue(round(user[2], 2))
        self.lines_user[idx][3].setValue(round(user[3], 2))
        self.lines_user[idx][4].setValue(round(user[4], 2))
        self.lines_user[idx][5].setValue(round(user[5], 2))

    def fill_LE_users(self, users):
        length = len(users)
        for i in range(length):
            self.lines_user[i][0].setValue(round(users[i][0], 2))
            self.lines_user[i][1].setValue(round(users[i][1], 2))
            self.lines_user[i][2].setValue(round(users[i][2], 2))
            self.lines_user[i][3].setValue(round(users[i][3], 2))
            self.lines_user[i][4].setValue(round(users[i][4], 2))
            self.lines_user[i][5].setValue(round(users[i][5], 2))



class GraphicsView(QtWidgets.QGraphicsView):

    resized = QtCore.Signal()

    def __init__(self, parent, right):
        super(GraphicsView, self).__init__(parent)
        self.resized.connect(self.move_legend)
        #self.main = main
        #self.toolbar = toolbar
        self.parent = parent
        self.addition = None
        #self.scene = QtWidgets.QGraphicsScene(self)
        self.scene = GraphicsScene(self)
        self.setScene(self.scene)
        self.sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding,
                                    QtWidgets.QSizePolicy.Expanding)
        #self.setSizePolicy(self.sizePolicy)
        #self.setMouseTracking(True)
        #self.setViewportUpdateMode(QtWidgets.QGraphicsView.FullViewportUpdate)
        #self.setCacheMode(QtWidgets.QGraphicsView.CacheBackground);
        #self.setRenderHint(QtGui.QPainter.Antialiasing)
        #self.setInteractive(True)
        #self.setViewport(QtOpenGL.QGLWidget())

        #self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        #self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)

        self.setTransformationAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)

        #self.setTransformationAnchor(QtWidgets.QGraphicsView.AnchorViewCenter)
        #self.setResizeAnchor(QtWidgets.QGraphicsView.AnchorViewCenter)

        #self.setTransformationAnchor(QtWidgets.QGraphicsView.NoAnchor)
        #self.setResizeAnchor(QtWidgets.QGraphicsView.NoAnchor)

        #self.setFrameShape(QtWidgets.QFrame.NoFrame)

        self.setDragMode(QtWidgets.QGraphicsView.NoDrag)
        #self.view_transform = QtGui.QTransform()
        #self.view_transform.rotate(90)
        #self.setTransform(self.view_transform)
        #self.standards = ['802.11a', '802.11ac', '802.11ax']
        #self.standards = values.GetStandarts()


        self.greenBrush = QtGui.QBrush(QtCore.Qt.green)
        self.blackBrush = QtGui.QBrush(QtCore.Qt.black)
        self.redBrush = QtGui.QBrush(QtCore.Qt.red)

        self.greenPen = QtGui.QPen(QtCore.Qt.green)
        self.blackPen = QtGui.QPen(QtCore.Qt.black, 2)
        self.redPen = QtGui.QPen(QtCore.Qt.red, 2)
        self.cyanPen = QtGui.QPen(QtCore.Qt.cyan)
        self.yellowPen = QtGui.QPen(QtCore.Qt.yellow)
        self.bluePen = QtGui.QPen(QtCore.Qt.blue, 2)

        self.right = right

        self.items_ap = []
        self.items_user = []
        self.scene_lines = []
        self.scene_pols = []
        self.changed = False
        self.isPointShow = True
        self.rect_type = None
        self.step = 1
        self.point_items = []

        self.icons()
        self.colors_for_get_map()
        self.create_legend()
        #self.begin()
        self.clear_all()
        self.define_colors()
        self.define_thickness()
        self.initialize()

    def resizeEvent(self, event):
        self.resized.emit()
        return super(GraphicsView, self).resizeEvent(event)

    def begin(self):
        self.isCoverageDone = False
        self.is_obstacles_done = False
        self.is_analyse_points = False
        self.is_ap_done = False
        self.is_users_done = False
        self.is_map_painted = False
        self.isImageShow = False
        self.init_done = False
        self.is_moving_object = False
        self.is_copied_item = False
        self.analyse_points = []
        self.access_points = []
        self.users = []
        self.power_values = []
        self.rate_values = []
        self.snr_values = []
        self.inr_values = []
        self.point_items = []
        self.power_items = []
        self.rate_items = []
        self.snr_items = []
        self.inr_items = []
        self.current_coverage_index = 0
        self.current_wall_index = 0
        self.addition = None
        self.automation = Automation(self)
        self.set_keys_unpressed()
        #self.isRunDone = False

    def set_keys_unpressed(self):
        self.is_key_ctrl = False
        self.is_key_shift = False
        return

    def clear_all(self):
        self.scene.clear()
        self.begin()
        #self.clear_AP()
        #self.clear_user()
        self.legend.hide()

    def clear_all2(self): # remove
        [self.scene.removeItem(item) for item in self.power_items]
        [self.scene.removeItem(item) for item in self.rate_items]
        [self.scene.removeItem(item) for item in self.snr_items]
        [self.scene.removeItem(item) for item in self.inr_items]
        [self.scene.removeItem(item) for item in self.point_items]
        [self.scene.removeItem(item) for item in self.scene_pols]
        self.clear_AP()
        self.clear_user()

    def define_colors(self):
        self.color_wall = QtGui.QColor("black")
        #self.color_wall = QtGui.QColor(120, 0, 0)
        self.color_door = QtGui.QColor("gray")
        self.color_window = QtGui.QColor("cyan")
        self.color_coverage = QtGui.QColor("green")
        self.color_edit = QtGui.QColor("red")
        self.color_analyse_points = QtGui.QColor("green")
        self.color_ap = QtGui.QColor("blue")
        self.color_user = QtGui.QColor("darkRed")
        self.color_image_rect = QtGui.QColor("darkCyan")

        #self.setPen(QtGui.QPen(QtGui.QColor("green"), 2))

    def define_thickness(self):
        self.thick_wall = 2
        self.thick_door = 2
        self.thick_window = 2
        self.thick_coverage = 3
        self.thick_edit = 1
        self.thick_image_rect = 2

    def create_legend(self):
        self.legend = Legend(self)
        self.legend.hide()
        self.parent.parent.move_legend()

    def move_legend(self):
        print("move3")
        window_size = self.size()
        legend_size = self.legend.size()
        #self.legend.setPosition(QtCore.QPoint(size))
        self.legend.move(window_size.width() - legend_size.width(),
                         window_size.height() - legend_size.height()-20)

    def initialize(self):
        #self.rect_type = None
        self.isRect = False
        self.isRecting = False
        self.isPoly = False
        self.isPolying = False
        self.isCoverage = False
        #self.isCoverageDone = False
        self.isImage = False
        self.isImaging = False
        self.isMoving = False
        self.move_object = None
        #self.isImageShow = False
        self.addition = False
        #self.automation = Automation(self)
        #self.parent.parent.show_status_bar()
        #self.isEditing = False
        return

    def cross_cursor(self):
        self.setCursor(QtCore.Qt.CrossCursor)
        #QtWidgets.QApplication.setOverrideCursor(QtCore.Qt.CrossCursor)

    def wait_cursor_global(self):
        #self.setCursor(QtCore.Qt.WaitCursor)
        QtWidgets.QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)

    def default_cursor(self):
        self.setCursor(QtCore.Qt.ArrowCursor)
        #QtWidgets.QApplication.setOverrideCursor(QtCore.Qt.ArrowCursor)

    def default_cursor_global(self):
        QtWidgets.QApplication.setOverrideCursor(QtCore.Qt.ArrowCursor)

    def openFileNameDialog(self):
        self.initialize()
        self.parent.parent.show_status_bar()
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(self,
                    "QFileDialog.getOpenFileName()", "","Map files (*.map)",
                    options=options)
        if filename:
            #self.init_flag = values.FileInit(filename)
            #print('init_flag:', self.init_flag)
            self.clear_all()
            #values.SetParameters(self.step, -100,4)
            if self.init_flag:
                self.task1(filename)

    def openFileNameDialog_import_image(self):
        self.initialize()
        self.parent.parent.show_status_bar()
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(self,
                    "QFileDialog.getOpenFileName()", "",
                    "Image Files (*.jpg *.bmp *.png)",
                    options=options)
        if filename:
            self.import_image(filename)

    def import_image(self, filename):
        #self.image = Canvas(filename, self)
        self.clear_all()
        self.initialize()
        self.init_done = True
        self.parent.parent.show_status_bar()
        self.image = QtGui.QPixmap(filename)
        self.image_item = QtWidgets.QGraphicsPixmapItem(self.image)
        self.scene.addItem(self.image_item)
        self.setSceneRect(self.scene.itemsBoundingRect())
        #self.vesx = 10
        #self.vesy = 10
        self.step = 2
        self.walls_list = []
        self.analyse_points = []
        self.isImageShow = True
        self.parent.parent.coverage_area.setEnabled(True)
        self.imageProcessing = ImageProcessing(self)
        #self.imageProcessing.image_two_points()
        #self.setDragMode(QGraphicsView.ScrollHandDrag)

    def openFileNameDialog_import_dxf(self):
        self.initialize()
        self.parent.parent.show_status_bar()
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(self,
                    "QFileDialog.getOpenFileName()", "","DXF files (*.dxf)",
                    options=options)
        if filename:
            self.import_dxf(filename)

    def import_dxf(self, filename):
        self.clear_all()
        self.initialize()
        self.init_done = True
        self.parent.parent.show_status_bar()
        self.init_flag = values.DXFImport(filename)
        if self.init_flag:
            self.task1()

    def icons(self):
        self.icon_ap_items = []
        self.icon_user_items = []
        pass

    def add_ap_icon(self, offset):
        print('offset:', offset)
        print('ves:', self.vesy, self.vesx)
        #self.icon_ap_item = QtWidgets.QGraphicsPixmapItem()
        self.icon_ap_item = Icon_ap(self, offset)
        #self.icon_ap_item.setPixmap(self.icon_ap)
        #self.icon_ap_item.setZValue(10)
        self.icon_ap_items.append(self.icon_ap_item)
        size = self.icon_ap_item.icon_ap.size()
        #print(self.icon_ap_item.x(), self.icon_ap_item.x())
        #self.icon_ap_item.setOffset(self.vesy * offset[1] - size.width()/2,
        #    -self.vesx * offset[0] - size.height()/2)
        #self.icon_ap_item.setPos(self.vesy * offset[1] - size.width()/2,
        #    -self.vesx * offset[0] - size.height()/2)
        self.scene.addItem(self.icon_ap_item)
        self.icon_ap_item.setPos(self.vesy * offset[1] - size.width()/2,
            -self.vesx * offset[0] - size.height()/2)
        #self.icon_ap_item.moveBy(self.vesy * offset[1] - size.width()/2,
        #    -self.vesx * offset[0] - size.height()/2)
        print('icon item:', self.icon_ap_item)
        print('icon items coords:', self.icon_ap_item.scenePos())
        #print('icon items coords:', self.icon_ap_item.x(), self.icon_ap_item.y())
        #print('icon items coords:', self.vesy * offset[1], -self.vesx * offset[0])
        #print("ap icon added")

    def add_user_icon(self, coord):
        self.icon_user_item = Icon_user(self, coord)
        self.icon_user_items.append(self.icon_user_item)
        size = self.icon_user_item.icon_user.size()
        self.scene.addItem(self.icon_user_item)
        self.icon_user_item.setPos(self.vesy * coord[1] - size.width()/2,
            -self.vesx * coord[0] - size.height()/2)
        pass


    def saveFile(self):
        self.initialize()
        self.parent.parent.show_status_bar()
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        filename, _ = QtWidgets.QFileDialog.getSaveFileName(self,
                    "QFileDialog.getOpenFileName()", "","Map files (*.map)",
                    options=options)
        if filename:
            print(filename)
            if filename[-4:] != '.map':
                filename += '.map'
                #print(filename)
            values.saveFile(filename)

    def newNet(self):
        pass

    def saveNet(self):
        self.initialize()
        self.parent.parent.show_status_bar()
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        filename, _ = QtWidgets.QFileDialog.getSaveFileName(self,
                    "QFileDialog.getOpenFileName()", "","Net files (*.net)",
                    options=options)
        if filename:
            print(filename)
            if filename[-4:] != '.net':
                filename += '.net'
                print(filename)
            values.saveNet(self.access_points, self.users, filename)

    def openNet(self):
        self.initialize()
        self.parent.parent.show_status_bar()
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(self,
                    "QFileDialog.getOpenFileName()", "","Net files (*.net)",
                    options=options)
        self.access_points, self.users = values.openNet(filename)
        #self.analyse_points = values.get_map_points()
        #self.draw_analyse_points()
        #tmp_access_points = []
        #for i in range(len(self.access_points)):
        self.wait_cursor_global()
        for point in self.access_points:
            #tmp_access_points.append(point)
            self.show_point_AP(point)
            self.parent.right.add_LE_ap(point)
            self.call_AP_lib(point)
        for point in self.users:
            print(point)
            self.show_point_user(point)
            self.parent.right.add_LE_user(point)
            self.call_user_lib(point)
        self.default_cursor_global()

    def file_parameters(self):
        pass

    def file_exit(self):
        res = False
        print('Call')
        res = values.go_exit()
        print('Exit:', res)
        sys.exit(app.exec_())

    def area_clear(self):
        self.initialize()
        self.scene.removeItem(self.coverage_item)
        values.delphi_lib.ClearAreas()
        pass

    def add_coverage_area(self):
        self.initialize()
        self.parent.parent.show_status_bar()
        if self.isCoverageDone:
            self.new_coverage_question()
        else:
            #self.initialize()
            #self.parent.parent.show_status_bar()
            self.isPoly = True
            self.isCoverage = True
            self.cross_cursor()
            self.parent.parent.show_status_bar()


    def new_coverage_question(self):
        self.initialize()
        self.window = SecondWindow()
        self.label = (QtWidgets.QLabel
                    (local.new_coverage_question))
        self.window.grid.addWidget(self.label, 0, 0, 1, 3)

        self.question_btn_repaint = QtWidgets.QPushButton(local.repaint)
        self.question_btn_repaint.clicked.connect(self.repaint_coverage)
        self.window.grid.addWidget(self.question_btn_repaint, 1, 0)

        self.question_btn_edit = QtWidgets.QPushButton(local.edit)
        self.question_btn_edit.clicked.connect(self.edit_coverage)
        self.window.grid.addWidget(self.question_btn_edit, 1, 1)

        self.question_btn_cancel = QtWidgets.QPushButton(local.cancel)
        self.question_btn_cancel.clicked.connect(self.cancel_coverage)
        self.window.grid.addWidget(self.question_btn_cancel, 1, 2)

        #self.isPoly = False
        #self.default_cursor()

    def repaint_coverage(self):
        self.isPoly = True
        self.cross_cursor()

        self.window.close()
        self.area_clear()
        #self.scene.removeItem(self.coverage_item)
        self.isCoverage = True
        self.isCoverageDone = False
        self.add_coverage_area()

    def edit_coverage(self):
        self.window.close()
        self.move_object = Movement(self, self.coverage_item)

    def cancel_coverage(self):
        self.window.close()

    def add_poly(self):
        if self.isPoly:
            self.isPoly = False
            self.default_cursor()
            return
        self.initialize()
        self.parent.parent.show_status_bar()
        self.isPoly = True
        self.cross_cursor()
        self.parent.parent.show_status_bar()

    def add_wall(self):
        if self.isRect:
            self.isRect = False
            self.default_cursor()
            return
        self.initialize()
        self.rect_type = "wall"
        self.add_rect()

    def add_door(self):
        self.initialize()
        self.rect_type = "door"
        self.add_rect()

    def add_window(self):
        self.initialize()
        self.rect_type = "window"
        self.add_rect()

    def add_rect(self):
        self.initialize()
        self.parent.parent.show_status_bar()
        self.isRect = True
        self.cross_cursor()
        self.parent.parent.show_status_bar()

    def edit_parameters(self):
        self.parent.initialize()
        self.parent.parent.show_status_bar()
        self.second_window = SecondWindow(self)
        label1 = QLabel(local.grid_step)
        label1.setLayout(grid)

    def enableEditing(self):
        self.initialize()
        if self.isEditing:
            self.isEditing = False
            try:
                self.move_object.exit()
            except:
                pass
        else:
            self.isEditing = True

    # Grid step
    def planning_parameters(self):
        self.initialize()
        self.parent.parent.show_status_bar()

        self.window = SecondWindow(self)

        par_label = QtWidgets.QLabel(local.parameter)
        self.window.grid.addWidget(par_label, 0, 0, 1, 2)

        self.window.grid.addWidget(
                QtWidgets.QLabel(local.grid_step), 1, 0)

        self.planning_parameter_spin_box = QtWidgets.QDoubleSpinBox()
        self.planning_parameter_spin_box.setValue(self.step)
        self.planning_parameter_spin_box.setRange(0.01, 100.0)
        self.window.grid.addWidget(self.planning_parameter_spin_box, 1, 1)

        #btn_ok_update = QtWidgets.QPushButton(local.ok_update)
        #btn_ok_update.clicked.connect(self.planning_parameters_window_ok_update)
        #self.window.grid.addWidget(btn_ok_update, 2, 0)

        btn_ok = QtWidgets.QPushButton(local.ok)
        btn_ok.clicked.connect(self.planning_parameters_window_ok_update)
        self.window.grid.addWidget(btn_ok, 2, 0)

        btn_cancel = QtWidgets.QPushButton(local.cancel)
        btn_cancel.clicked.connect(self.planning_parameters_window_cancel)
        self.window.grid.addWidget(btn_cancel, 2, 1)

        self.window.grid.setRowStretch(3, 1)
        self.window.grid.setColumnStretch(2,1)
        self.window.grid.setSpacing(10)

    def planning_parameters_window_ok_update(self):
        self.step = self.planning_parameter_spin_box.value()
        values.SetParameters(self.step, -100, 4)
        self.window.close()
        self.analyse_points_update()
        if self.automation.is_automation:
            self.automation_on()

    def planning_parameters_window_ok(self):
        self.step = self.planning_parameter_spin_box.value()
        values.SetParameters(self.step, -100, 4)
        self.window.close()

    def planning_parameters_window_cancel(self):
        self.window.close()

    def colors_for_get_map(self):
        self.col1 = [72, 61, 139]
        self.col2 = [255, 0, 0]
        self.col3 = [255, 0, 255]
        self.col4 = [255, 255, 0]
        self.col5 = [189, 183, 107]
        self.col6 = [0, 100, 0]
        self.col7 = [32, 178, 170]
        self.col8 = [0, 255, 0]
        self.colors = [self.col1, self.col2, self.col3, self.col4, self.col5,
                        self.col6, self.col7, self.col8]

    def get_map(self):
        self.initialize()
        self.parent.parent.show_status_bar()

        self.get_map_window = SecondWindow(self)
        self.get_map_window.grid.addWidget(
                    QtWidgets.QLabel(local.what_parameter), 0, 0)
        self.map_box = QtWidgets.QComboBox()
        self.map_box.addItems([local.p, local.v, local.snr, local.inr])
        self.get_map_window.grid.addWidget(self.map_box, 0, 1)
        btn_ok = QtWidgets.QPushButton(local.ok)
        btn_ok.clicked.connect(self.get_map_window_ok)
        self.get_map_window.grid.addWidget(btn_ok, 1, 0)

    def get_map_window_ok(self):
        self.get_map_window.close()
        option = self.map_box.currentIndex()
        output_values = []
        self.wait_cursor_global()
        #print(self.addition)
        num_objects = values.GetMapLength(option)
        for i in range(num_objects):
            value = values.GetMapPoint(i, 0)
            output_values.append(value)
        self.max_par = max(output_values, key = operator.itemgetter(2))
        self.max_par = self.max_par[2]
        self.min_par = min(output_values, key = operator.itemgetter(2))
        self.min_par = self.min_par[2]
        #self.max_par = 215
        #self.min_par = 15
        print('params1:', self.min_par, self.max_par)
        self.step_value = 5*math.ceil((self.max_par - self.min_par)/40)
        if self.step_value == 0:
            self.step_value = 1
        self.min_par = 5*round((self.max_par + self.min_par)/10)
        self.max_par = self.min_par + 4*self.step_value
        self.min_par = self.min_par - 4*self.step_value
        print(self.min_par,self.max_par,self.step_value)
        if (option == 1) and (self.min_par<0):
            self.min_par=0
        self.legend.set_par(self.min_par, self.max_par, self.step_value)
        if option == 0:
            self.power_values = output_values
            self.paint_map_power()
        if option == 1:
            if (self.min_par<0):
                self.min_par=0
            self.rate_values = output_values
            self.paint_map_rate()
        if option == 2:
            self.snr_values = output_values
            self.paint_map_snr()
        if option == 3:
            self.inr_values = output_values
            self.paint_map_inr()
        self.default_cursor_global()

    def paint_map_power(self):
        self.power_items = self.paint_map(self.power_values)

    def paint_map_rate(self):
        self.rate_items = self.paint_map(self.rate_values)

    def paint_map_snr(self):
        self.snr_items = self.paint_map(self.snr_values)

    def paint_map_inr(self):
        self.inr_items = self.paint_map(self.inr_values)

    def paint_map(self, output_values):
        print('params2:', self.min_par, self.max_par)
        self.legend.show()
        self.hide_get_map_points()
        data_items = []
        sh1 = self.vesy*self.step
        sh2 = self.vesx*self.step
        for value in output_values:
            sh = math.floor((value[2] - self.min_par) / self.step_value)
            #print(sh)
            if sh > 7:
                sh = 7
            if sh < 0:
                sh = 0
            color = QtGui.QColor(*self.colors[sh])
            data_items.append(self.scene.addRect(
                        self.vesy*value[1]-sh1/2,
                        -self.vesx * value[0] - sh2/2,
                        sh1, sh2, color,
                         color))
        return data_items

    def hide_get_map_points(self):
        self.analyse_points_hide()
        [item.hide() for item in self.power_items]
        [item.hide() for item in self.rate_items]
        [item.hide() for item in self.snr_items]
        [item.hide() for item in self.inr_items]

    def analyse_parameters(self):
        self.analyse_parameters_window = SecondWindow(self)
        self.dspin = QtWidgets.QDoubleSpinBox()
        self.dspin.setValue(self.step)
        self.dspin.setRange(0.01, 100.0)
        self.model_box = QtWidgets.QComboBox()
        self.model_box.addItems(['REC-1238'])
        self.model = 'REC-1238'
        self.model_box.activated[str].connect(self.analyse_parameters_onActivatedText)
        btn_ok = QtWidgets.QPushButton(local.ok)
        btn_ok.clicked.connect(self.analyse_parameters_window_ok)

        self.analyse_parameters_window.grid.addWidget(
                QtWidgets.QLabel(local.parameters), 0, 0, 1, 2)
        self.analyse_parameters_window.grid.addWidget(
                QtWidgets.QLabel(local.grid_step), 1, 0)
        self.analyse_parameters_window.grid.addWidget(
                QtWidgets.QLabel(local.propagation_model), 2, 0)
        self.analyse_parameters_window.grid.addWidget(self.dspin, 1, 1)
        self.analyse_parameters_window.grid.addWidget(self.model_box, 2, 1)
        self.analyse_parameters_window.grid.addWidget(btn_ok, 3, 0)

    @QtCore.Slot(str)
    def analyse_parameters_onActivatedText(self, text):
        self.model = text

    def analyse_parameters_window_ok(self):
        self.analyse_step = self.dspin.value()
        values.SetParameters(self.analyse_step, -100, 4)
        #values.SetParameters(self.analyse_step, -100, self.model)

    def report_on_map(self):
        pass

    def report_parameters(self):
        pass

    def report_window(self):
        self.report = Report(self)
        self.report.report_ap()
        self.report.report_users()
        self.report.report_analyse_points()
        if self.power_values:
            self.report.report_power()
        if self.rate_values:
            self.report.report_rate()
        if self.snr_values:
            self.report.report_snr()
        if self.inr_values:
            self.report.report_inr()

    def is_ap_done(self):
        if self.access_points:
            return True
        return False

    def is_users_done(self):
        if self.users:
            return True
        return False

    def automation_on(self):
        #self.automation = Automation(self)
        print("automation_on")
        self.automation.close_all_windows()
        self.default_cursor()
        if not self.init_done:
            print("init")
            self.automation.show_starting_window()
        elif self.isImageShow and not self.isCoverageDone:
            self.automation.plot_coverage()
        elif not self.is_obstacles_done and not self.analyse_points:
            print("plot obstacles")
            self.automation.plot_obstacles()
        elif not self.analyse_points:  # todo
            if self.automation.is_set_parameters:
            #if not self.is_analyse_points:
                self.automation.set_parameters()
            else:
                self.automation.plot_analyse_points()
        elif not self.access_points: #todo
            self.automation.set_ap()
        elif not self.users:  # todo
            self.automation.set_users()
        else:   # todo
            try:
                self.automation.paint_map()
            except:
                pass


    def clear_actions(self):
        self.addition = None

    def add_AP(self):
        if self.addition == 'AP':
            self.clear_actions()
            self.parent.parent.show_status_bar()
            return
        self.clear_actions()
        self.addition = 'AP'
        self.parent.parent.show_status_bar()
        self.changed = False

    def add_new_user_auto(self):
        self.window = SecondWindow(self)
        self.window.grid.addWidget(QtWidgets.QLabel(local.num_users), 0, 0)
        self.window.grid.addWidget(QtWidgets.QLabel(local.height_users), 1, 0)
        self.window.grid.addWidget(QtWidgets.QLabel(local.dl_users), 2, 0)
        self.window.grid.addWidget(QtWidgets.QLabel(local.ul_users), 3, 0)
        self.window.grid.addWidget(QtWidgets.QLabel(local.what_method), 4, 0)
        self.spin_number = QtWidgets.QSpinBox()
        self.spin_h = QtWidgets.QDoubleSpinBox()
        self.spin_h.setRange(-99.99, 99.99)
        self.spin_vd = QtWidgets.QDoubleSpinBox()
        self.spin_vd.setRange(0, 999.99)
        self.spin_vu = QtWidgets.QDoubleSpinBox()
        self.spin_vu.setRange(0, 999.99)
        self.method_box = QtWidgets.QComboBox()
        self.method_box.addItems([local.min_p, local.min_v])
        self.method = 'Min Power'
        self.window.grid.addWidget(self.spin_number, 0, 1)
        self.window.grid.addWidget(self.spin_h, 1, 1)
        self.window.grid.addWidget(self.spin_vd, 2, 1)
        self.window.grid.addWidget(self.spin_vu, 3, 1)
        self.window.grid.addWidget(self.method_box, 4, 1)
        self.spin_vd.setValue(1.5)
        self.spin_vd.setValue(1)
        self.spin_vu.setValue(1)
        self.method_box.activated[str].connect(self.add_new_user_auto_onActivatedText)
        btn_ok = QtWidgets.QPushButton(local.ok)
        btn_ok.clicked.connect(self.add_new_user_auto_window_ok)
        self.window.grid.addWidget(btn_ok, 5, 0)

    @QtCore.Slot(str)
    def add_new_user_auto_onActivatedText(self, text):
        self.method = text

    def add_new_user_auto_window_ok(self):
        method = self.method_box.currentIndex()+1
        number = self.spin_number.value()
        h = self.spin_h.value()
        vd = self.spin_vd.value()
        vu = self.spin_vu.value()
        self.wait_cursor_global()
        nak = values.set_AK(method, number, h, vd,vu)
        self.window.close()
        ### TODO
        for i in reversed(range(nak)):
            AK = values.get_AK(i+1)
            self.show_point_user(AK)
            AK.append(h)
            AK.append(vd)
            AK.append(vu)
            self.users.append(AK)
            self.parent.right.add_LE_user(AK)
            #self.edit_user()
        self.default_cursor_global()
        if self.automation.is_automation:
            self.automation_on()


    def add_new_user_uniform(self):
        self.window = SecondWindow(self)
        self.window.grid.addWidget(QtWidgets.QLabel(local.num_users), 0, 0)
        self.window.grid.addWidget(QtWidgets.QLabel(local.height_users), 1, 0)
        self.window.grid.addWidget(QtWidgets.QLabel(local.dl_users), 2, 0)
        self.window.grid.addWidget(QtWidgets.QLabel(local.ul_users), 3, 0)
        self.spin_number = QtWidgets.QSpinBox()
        self.spin_h = QtWidgets.QDoubleSpinBox()
        self.spin_h.setRange(-99.99, 99.99)
        self.spin_vd = QtWidgets.QDoubleSpinBox()
        self.spin_vd.setRange(0, 999.99)
        self.spin_vu = QtWidgets.QDoubleSpinBox()
        self.spin_vu.setRange(0, 999.99)
        self.method_box = QtWidgets.QComboBox()
        self.method_box.addItems(['Min Power', 'Min Rate'])
        self.method = 'Min Power'
        self.window.grid.addWidget(self.spin_number, 0, 1)
        self.window.grid.addWidget(self.spin_h, 1, 1)
        self.window.grid.addWidget(self.spin_vd, 2, 1)
        self.window.grid.addWidget(self.spin_vu, 3, 1)
        self.spin_vd.setValue(1.5)
        self.spin_vd.setValue(1)
        self.spin_vu.setValue(1)
        self.method_box.activated[str].connect(self.add_new_user_auto_onActivatedText)
        btn_ok = QtWidgets.QPushButton("OK")
        btn_ok.clicked.connect(self.add_new_user_uniform_window_ok)
        self.window.grid.addWidget(btn_ok, 4, 0)


    def add_new_user_uniform_window_ok(self):
        number = self.spin_number.value()
        h = self.spin_h.value()
        vd = self.spin_vd.value()
        vu = self.spin_vu.value()
        self.wait_cursor_global()
        nak = values.set_AK(0, number, h, vd ,vu)
        self.window.close()
        for i in reversed(range(nak)):
            AK = values.get_AK(i+1)
            self.show_point_user(AK)
            AK.append(h)
            AK.append(vd)
            AK.append(vu)
            self.users.append(AK)
            self.parent.right.add_LE_user(AK)
            #self.edit_user()
        self.default_cursor_global()
        if self.automation.is_automation:
            self.automation_on()

    def add_new_user_manually(self):
        if self.addition == 'user':
            self.clear_actions()
            return
        self.clear_actions()
        self.addition = 'user'
        self.changed = False
        self.parent.parent.show_status_bar()

    def clear_AP(self):
        self.right.isFirstRow_ap = False
        self.access_points = []
        #[self.scene.removeItem(item) for item in self.items_ap]
        [self.scene.removeItem(item) for item in self.icon_ap_items]
        #self.btn_ok.setParent(None)
        self.wait_cursor_global()
        self.right.clear_AP()
        nbs = values.clear_BS()
        print(nbs)
        self.default_cursor_global()

    def clear_user(self):
        self.right.isFirstRow_user = False
        self.users = []
        [self.scene.removeItem(item) for item in self.items_user]
        [self.scene.removeItem(item) for item in self.icon_user_items]
        self.right.clear_AK()
        self.wait_cursor_global()
        nak = values.clear_AK()
        print(nak)
        self.default_cursor_global()

    def analyse_points_show(self):
        [point.show() for point in self.point_items]
        self.scene.update()

    def analyse_points_hide(self):
        [point.hide() for point in self.point_items]
        self.scene.update()

    def changePointsState(self):
        #self.isPointShow = not self.isPointShow
        if self.isPointShow:
            self.analyse_points_show()
            print('show analyse points')
            self.isPointShow = False
        else:
            self.analyse_points_hide()
            print('hide analyse points')
            self.isPointShow = True

    def image_hide(self):
        self.image_item.hide()
        self.setSceneRect(self.scene.itemsBoundingRect())
        #self.centerOn(self.coverage_item)

    def image_show(self):
        self.image_item.show()
        #self.setSceneRect(self.scene.itemsBoundingRect())
        self.centerOn(self.image_item)

    def change_image_state(self):
        if self.isImageShow:
            self.image_hide()
            self.isImageShow = False
        else:
            self.image_show()
            self.isImageShow = True
        pass

    def removeImage(self): #delete
        self.image_item.hide()
        return

    def mimo_rates_old(self):
        # рассчитать матрицы в каждой точке
        # тепловая карта
        from numpy.linalg import eig
        #import numpy as np

        p_BS = [54.0, 35.0, 3.0]
        self.draw_p(p_BS)
        N0 = 10**(-93/20)
        P = 10**(49/20)/3
        for i in range(3): #(len(self.analyse_points)):
            p1 = self.analyse_points[i]
            H = values.mimo_channel_matrix(p1, p_BS, self.walls_list)
            H = np.array(H)
            eig_values, _ = eig(np.dot(H, np.conj(H).T))
            eig_values = eig_values.real
            print(i, eig_values/np.max(eig_values), np.max(eig_values))

    def load_rates(self):
        with open('rates_rig1.npy', 'rb') as f:
        #with open('rates_hyb1.npy', 'rb') as f:
            rates0 = np.load(f)
        idx = 5  # 2...7 channels, rate, channels, rate, siso, demmel
        rates = np.array(rates0[:, [0,1,idx]], dtype=np.float64)
        #print(rates[:10])
        if idx == 7:
            limit = 2000
            idx_dem = np.where(rates[:, 2] > limit)  # for demmel (i = 7)
            rates[idx_dem, 2] = limit
            self.max_par = 0
            self.min_par = limit
        else:
            self.max_par = max(rates, key = operator.itemgetter(2))
            self.max_par = self.max_par[2]
            self.min_par = min(rates, key = operator.itemgetter(2))
            self.min_par = self.min_par[2]
        #self.step_value = 5*math.ceil((self.max_par - self.min_par)/40)
        self.step_value = (self.max_par - self.min_par) / 8
        if self.step_value == 0:
            self.step_value = 1
        self.legend.set_par(self.min_par, self.max_par, self.step_value)
        self.rate_values = rates
        self.paint_map_rate()
        p_BS = [54.0, 35.0, 2.5]
        self.draw_p(p_BS)
        return

    """    
    def mimo_rates_help(self, p1):
        fc = 5.6
        p_BS = [54.0, 35.0, 2.5]
        return values.mimo_channel_matrix(p1, p_BS, self.walls_list, 
                    self.n_walls, self.faces, self.segments, 
                    self.DRs, self.face_ps, self.face_vs, fc)

    @classmethod
    def foo(cls, x):
        return x**2
    """

    def fun(self, f, q_in, q_out):
        while True:
            i, x = q_in.get()
            if i is None:
                break
            print(i)
            q_out.put((i, f(x)))


    def parmap(self, f, X, nprocs=multiprocessing.cpu_count()-2):
        q_in = multiprocessing.Queue(1)
        q_out = multiprocessing.Queue()
        #print(nprocs)

        proc = [multiprocessing.Process(target=self.fun, 
                args=(f, q_in, q_out)) for _ in range(nprocs)]
        for p in proc:
            p.daemon = True
            p.start()

        sent = [q_in.put((i, x)) for i, x in enumerate(X)]
        [q_in.put((None, None)) for _ in range(nprocs)]
        res = [q_out.get() for _ in range(len(sent))]

        [p.join() for p in proc]

        return [x for i, x in sorted(res)]

    def mimo_rates_help(self, p1):
        p1 = list(p1)
        p1[2] = 1.0
        fc = 5.6 * 10**9
        c = 3 * 10**8
        lamda = c / fc
        p_BS = [54.0, 35.0, 2.5]
        p_rates = []
        H = values.mimo_channel_matrix_rig(p1, p_BS, self.walls_list, 
                    self.n_walls, self.faces, self.segments, 
                    self.DRs, self.face_ps, self.face_vs, fc)
        try:
            H = H * lamda / (4*np.pi) * 10**(119/20)
            eig_values, _ = np.linalg.eig(np.dot(H, np.conj(H).T))
            eig_values = eig_values.real
            eig_values = np.sort(eig_values)[::-1]
            p_rates += p1[:2]
            value1 = np.sum(eig_values/np.max(eig_values) > 0.05)
            value2 = np.sum(np.log2(1 + eig_values/3))
            value5 = np.log2(1 + np.abs(H[1,1])**2)
            value6 = np.sum(eig_values) / np.min(eig_values)  # Demmel
            gammas = self.waterpouring(3, H)
            #print("gammas:", gammas)
            value4 = np.sum(np.log2(1 + gammas*eig_values/3))
            value3 = np.sum(gammas > 0.01)
        except:
            print(H)
            p_rates += p1[:2]
            value1 = 1
            value2 = 1
            value3 = 1
            value4 = 1
            value5 = 1
            value6 = 10**4
        p_rates += value1,
        p_rates += value2,
        p_rates += value3,
        p_rates += value4,
        p_rates += value5,  # make sense for rt_rig
        p_rates += value6,
        return p_rates

    def mimo_rates(self):
        # рассчитать матрицы в каждой точке
        # тепловая карта
        #from numpy.linalg import eig

        #n_walls, faces, segments, DRs, face_ps, face_vs = values.walls_to_arrays(self.walls_list)
        (self.n_walls, self.faces, self.segments, self.DRs, self.face_ps, 
            self.face_vs) = values.walls_to_arrays(self.walls_list)


        p_BS = [54.0, 35.0, 2.5]
        self.draw_p(p_BS)
        #N0 = 10**(-93/20)
        #P = 10**(26/20)
        fc = 5.6*10**9
        c = 3*10**8
        lamda = c / fc
        #rates = []
        #threads = 2
        rates = []
        rates += self.parmap(self.mimo_rates_help, self.analyse_points[:20])

        #for i in range(10//threads + 1):#(len(self.analyse_points)):
        #    with Pool(threads) as pool:
        #        p_list = []
        #        for j in range(threads):
        #            p_list.append(list(self.analyse_points[2*i+j]))
        #            p_list[-1][2] = 1.0
                #p1_1 = list(self.analyse_points[2*i])
                #H_list = pool.map(self.mimo_rates_help, p_list)
        #    H_list = pool.map(self.foo, [1,2,3])
        #    return
            

            #p1 = list(self.analyse_points[i])
            #p1[2] = 1.0
            #cr_points, cf_faces, d_faces = values.ray_tracing(p1, p_BS, self.walls_list)
            #H = values.mimo_channel_matrix(p1, p_BS, self.walls_list, 
            #            n_walls, faces, segments, DRs, face_ps, face_vs)
            #H = values.mimo_channel_matrix(p1, p_BS, self.walls_list, 
            #            n_walls, faces, segments, DRs, face_ps, face_vs, fc)
        """for i,H in enumerate(H_list):
                try:
                    #H = H * 10**(119/20)
                    H = H * lamda / (4*np.pi) * 10**(119/20)
                    eig_values, _ = eig(np.dot(H, np.conj(H).T))
                    eig_values = eig_values.real
                    eig_values = np.sort(eig_values)[::-1]
                    rates.append([])
                    #rates[-1] += p1[:2]
                    rates += p_list[i][:2]
                    value1 = np.sum(eig_values/np.max(eig_values) > 0.05)
                    value2 = np.sum(np.log2(1 + eig_values/3))
                    #value2 = np.sum(np.log2(1 + P*eig_values/N0/3))
                    value5 = np.log2(1 + np.abs(H[1,1])**2)
                    value6 = np.sum(eig_values) / np.min(eig_values)  # Demmel
                    if value6 > 10**4:
                        value6 = 10**4
                    gammas = self.waterpouring(3, H)
                    print(gammas)
                    value4 = np.sum(np.log2(1 + gammas*eig_values/3))
                    #value4 = np.sum(np.log2(1 + gammas*P*eig_values/N0/3))
                    value3 = np.sum(gammas > 0.01)
                except:
                    print(H)
                    rates.append([])
                    rates[-1] += p1[:2]
                    value1 = 1
                    value2 = 1
                    value3 = 1
                    value4 = 1
                    value5 = 1
                    value6 = 10**4
                rates[-1] += value1,
                rates[-1] += value2,
                rates[-1] += value3,
                rates[-1] += value4,
                rates[-1] += value5,  # make sense for rt_rig
                rates[-1] += value6,
                print(i, eig_values/np.max(eig_values), np.max(eig_values), value1, 
                            value2, value3, value4, value5, value6)"""
        rates = np.array(rates, dtype=np.float64)
        #with open('rates_hyb2.npy', 'wb') as f:
        #with open('rates_rig1.npy', 'wb') as f:
        #    np.save(f, rates)
        #print("rates:", rates)
        self.max_par = max(rates, key = operator.itemgetter(2))
        self.max_par = self.max_par[2]
        self.min_par = min(rates, key = operator.itemgetter(2))
        self.min_par = self.min_par[2]
        #self.step_value = 5*math.ceil((self.max_par - self.min_par)/40)
        self.step_value = (self.max_par - self.min_par) / 8
        if self.step_value == 0:
            self.step_value = 1
        self.legend.set_par(self.min_par, self.max_par, self.step_value)
        self.rate_values = rates
        self.paint_map_rate()
        self.draw_p(p_BS)




    def task1(self, filename):  # open map
        print('task1')
        #self.mode = 'task1'
        self.init_done = True
        self.access_points = []
        self.users = []
        self.vesx = 30
        self.vesy = 30

        #self.sh1 = 0.3*self.vesy*self.step       # Recalculate if  self.step changes
        #self.sh2 = 0.3*self.vesx*self.step
        #self.walls_list = values.get_map_objects()
        self.analyse_points, self.walls_list = values.open_file(filename)
        #self.walls_list = [self.walls_list[25]]
        print('walls:', len(self.walls_list))
        self.draw_walls()
        #self.draw_analyse_points()
        #n_walls, faces, segments, DRs, face_ps, face_vs = values.walls_to_arrays(self.walls_list)

        #self.load_rates()
        self.mimo_rates()
        return

        #p1 = [6.05, 15.99, 1.0]  # rts old
        #p2 = [5.05, 18.99, 1.0]


        #p1 = [48.0, 15.0, 1.0]   # rts1
        #p2 = [53.0, 36.0, 1.0]

        p1 = [53.4, 39.35, 1.85]   # holl  (case 1)
        p2 = [53.0, 44.75, 1.85]

        #p1 = [52.0, 50.0, 1.0]
        #p2 = [58.0, 55.0, 1.0]

        #p1 = [53.0, 70.0, 1.0]   # 504
        #p2 = [58.0, 72.0, 1.5]

        #p1 = [53.7, 73.8, 1.5]   # 504  (case 2)
        #p2 = [56.7, 73.0, 1.5]

        #p1 = [57.0, 69.0, 2.0]   # both in 504
        #p2 = [58.0, 73.0, 1.0]

        #p1 = [54.0, 35.0, 2.5]
        #p2 = [52.0, 55.0, 1.0]

        #p1 = [54.0, 35.0, 2.5]   # far
        #p2 = [59.0, 74.0, 1.0]

        #p1 = [-224, -255, 20]   # BS  bonn
        #p2 = [-85, -65, 2]
        #p2 = [-104, -70, 2]     # bonn
        self.draw_p1_p2([p1, p2])
        #return
        n_walls, faces, segments, DRs, face_ps, face_vs = values.walls_to_arrays(self.walls_list)

        print(len(self.walls_list))
        cr_points, cf_faces, d_faces = values.ray_tracing(p1, p2, self.walls_list, 
                    n_walls, faces, segments, DRs, face_ps, face_vs)
        #self.draw_cr_faces(cf_faces)
        #cr_points, cf_faces, d_faces = values.ray_tracing(p1, p2, self.walls_list)
        self.draw_rt_lines(p1, p2, cr_points)
        #return


        #H = values.mimo_channel_matrix(p1, p2, self.walls_list)
        #R_list = []
        N = 100
        #fc = 5.6*10**9
        c = 3*10**8
        fc_list = np.linspace(5.59, 5.61, N) * 10**9
        value2_arr, value3_arr, value4_arr = [], [], []
        for fc in fc_list:
            H = values.mimo_channel_matrix(p1, p2, self.walls_list, 
                            n_walls, faces, segments, DRs, face_ps, face_vs, fc)
            #H = np.array(H)
            #print(H)
            lamda = c / fc
            H = H * lamda / (4*np.pi) * 10**(119/20)  # eig -> snr
            eig_values, _ = np.linalg.eig(np.dot(H, np.conj(H).T))
            eig_values = eig_values.real
            eig_values = np.sort(eig_values)[::-1]
            #print(H)
            value3 = np.sum(eig_values) / np.min(eig_values)
            if value3 > 5000:
                value3 = 5000
            value2_arr += np.sum(np.log2(1 + eig_values/3)),
            value3_arr += value3,  # Demmel cond number
            gammas = self.waterpouring(3, H)
            #print(gammas)
            value4_arr += np.sum(np.log2(1 + eig_values*gammas/3)),
            print(eig_values/np.max(eig_values), np.max(eig_values), 
                        value2_arr[-1], value3, value4_arr[-1])
            #H_norm = H / np.sqrt(self.frob(H)/9)
            #vec_H = H_norm.flatten()
            #R_list.append(np.outer(vec_H, np.conj(vec_H.T)))
            #print(np.var(R_list[-1]))
        print(np.sum(value2_arr) / N, np.sum(value3_arr) / N, np.sum(value4_arr)/N)
        #R = sum(R_list)/N
        #print("var", np.var(R))
        return


        self.isCoverageDone = True
        self.parent.parent.update_actions()
        self.parent.right.clear_AK()
        self.parent.right.clear_AP()

    def frob(self, H):
        return(np.sum(np.sum(np.abs(H)**2)))

    def waterpouring(self, Mt, H_chan):
        #SNR = 10**(SNR_dB/10)
        #H_norm = H / np.sqrt(frob(H)/9)
        #SNR = np.sqrt(self.frob(H_chan)/9)
        #SNR = np.sqrt(np.var(H_chan))
        #H_chan = np.array(H_chan) / SNR
        #r = np.linalg.matrix_rank(H_chan)
        r = Mt
        H_sq = np.dot(H_chan,np.matrix(H_chan, dtype=complex).H)
        lambdas = np.linalg.eigvals(H_sq) 
        lambdas = np.sort(lambdas)[::-1]
        #print("var:", np.var(H_chan), lambdas)
        p = 1
        gammas = np.zeros((r,1))
        flag = True
        while flag == True:
            lambdas_r_p_1 = lambdas[0:(r-p+1)]
            inv_lambdas_sum =  np.sum(1/lambdas_r_p_1)
            mu = ( Mt / (r - p + 1) ) * ( 1 + inv_lambdas_sum)
            for idx, item in enumerate(lambdas_r_p_1):
                gammas[idx] = mu - (Mt/(item))
            if gammas[r-p] < 0: #due to Python starts from 0
                gammas[r-p] = 0 #due to Python starts from 0
                p = p + 1
            else:
                flag = False
        res = []
        for gamma in gammas:
            res.append(float(gamma))
        return np.array(res)

    def waterpouring_old(self, Mt, H_chan):
        #SNR = 10**(SNR_dB/10)
        #H_norm = H / np.sqrt(frob(H)/9)
        SNR = np.sqrt(self.frob(H_chan)/9)
        SNR = np.sqrt(np.var(H_chan))
        H_chan = np.array(H_chan) / SNR
        r = np.linalg.matrix_rank(H_chan)
        H_sq = np.dot(H_chan,np.matrix(H_chan, dtype=complex).H)
        lambdas = np.linalg.eigvals(H_sq) 
        lambdas = np.sort(lambdas)[::-1]
        print("var:", np.var(H_chan), SNR, lambdas)
        p = 1
        gammas = np.zeros((r,1))
        flag = True
        while flag == True:
            lambdas_r_p_1 = lambdas[0:(r-p+1)]
            inv_lambdas_sum =  np.sum(1/lambdas_r_p_1)
            mu = ( Mt / (r - p + 1) ) * ( 1 + (1/SNR) * inv_lambdas_sum)
            for idx, item in enumerate(lambdas_r_p_1):
                gammas[idx] = mu - (Mt/(SNR*item))
            if gammas[r-p] < 0: #due to Python starts from 0
                gammas[r-p] = 0 #due to Python starts from 0
                p = p + 1
            else:
                flag = False
        res = []
        for gamma in gammas:
            res.append(float(gamma))
        return np.array(res)

    """
    def extract_data(self, filename):
        #global v_Npoints
        self.initialize()
        self.parent.parent.show_status_bar()
        self.scene.clear()

        #self.analyse_points, self.walls_list = values.open_file(filename)
        self.analyse_points, self.walls_list = values.getMAP()
        self.vesx = 10
        self.vesy = 10

        self.sh = 3
        self.isCoverageDone = True
        self.parent.parent.update_actions()
        self.draw_walls()
        self.draw_analyse_points()
        self.parent.right.clear_AK()
        self.parent.right.clear_AP()
    """

    def draw_cr_faces(self, draw_cr_faces):
        for i in range(len(draw_cr_faces)):
            floor_edge = draw_cr_faces[i][1]
            points = []
            for j in range(len(floor_edge) // 2):
                x1 = self.vesx*(floor_edge[2*j][1])
                y1 = -self.vesy*(floor_edge[2*j][0])
                points.append(QtCore.QPointF(x1, y1))
            pol = PolygonItem(self)
            pol.setZValue(6)
            self.scene.addItem(pol)
            pol.set_poly(points)
            pol.setPen(QtGui.QPen(self.color_window, self.thick_wall))
            pol.setPolygon(QtGui.QPolygonF(points))
            self.scene_pols.append(pol)

    def draw_rt_lines(self, p1, p2, cr_points):
        line_direct = self.scene.addLine(self.vesy*p1[1], -self.vesx*p1[0],
                self.vesy*p2[1], -self.vesx*p2[0], self.redPen)
        for point in cr_points:
            x1 = self.vesy*(point[1])
            y1 = self.vesx*(point[0])
            #x2 = x1 + self.vesx*(p2[0])
            #y2 = y1 + self.vesy*(p2[1])
            #line1 = self.scene.addLine(p1[0])
            line1 = self.scene.addLine(x1, -y1,
                self.vesy*p1[1], -self.vesx*p1[0], self.greenPen)
            line2 = self.scene.addLine(x1, -y1,
                self.vesy*p2[1], -self.vesx*p2[0], self.greenPen)

    def draw_p(self, p):
        sh1 = 0.3*self.vesy*self.step *2
        sh2 = 0.3*self.vesx*self.step*2
        self.scene.addRect(
                        self.vesy * p[1] - sh1/2,
                        -self.vesx * p[0] - sh2/2,
                        sh1, sh2, self.color_ap,
                         self.color_ap)
        return 

    def draw_p1_p2(self, points):
        sh1 = 0.3*self.vesy*self.step *4
        sh2 = 0.3*self.vesx*self.step*4
        #self.point_items = []
        for i, point in enumerate(points):
            self.scene.addRect(
                        self.vesy * point[1] - sh1/2,
                        -self.vesx * point[0] - sh2/2,
                        sh1, sh2, self.color_ap,
                         self.color_ap)
        self.scene.update()
        return

    def draw_analyse_points(self):
        print('draw anp')
        if self.point_items:
            [self.scene.removeItem(point) for point in self.point_items]
        sh1 = 0.3*self.vesy*self.step
        sh2 = 0.3*self.vesx*self.step
        self.point_items = []
        for i, point in enumerate(self.analyse_points):
            self.point_items.append(self.scene.addRect(
                        self.vesy * point[1] - sh1/2,
                        -self.vesx * point[0] - sh2/2,
                        sh1, sh2, self.color_analyse_points,
                         self.color_analyse_points))
        [point.setZValue(6) for point in self.point_items]
        self.scene.update()
        return

    def draw_analyse_points2(self):
        #self.sh = 0.3*(self.vesx+self.vesy)/2
        #sh1 = self.sh/2
        self.point_items = []
        for i in range(len(self.analyse_points)):
            self.point_items.append(self.scene.addRect(self.vesy*self.analyse_points[i][1]-sh1,
                        -self.vesx * self.analyse_points[i][0] - sh1,
                        self.sh, self.sh, self.color_analyse_points,
                         self.color_analyse_points))
        return

    def draw_walls(self):
        print('draw walls')
        #print(self.walls_list)
        for i in range(len(self.walls_list)):
            floor_edge = self.walls_list[i][0][1]
            points = []
            for j in range(len(floor_edge) // 2):
                x1 = self.vesx*(floor_edge[2*j][1])
                y1 = -self.vesy*(floor_edge[2*j][0])
                points.append(QtCore.QPointF(x1, y1))
            pol = PolygonItem(self)
            pol.setZValue(5)
            self.scene.addItem(pol)
            pol.set_poly(points)
            pol.setPen(QtGui.QPen(self.color_wall, self.thick_wall))
            pol.setPolygon(QtGui.QPolygonF(points))
            self.scene_pols.append(pol)
            if i == 0:
                self.coverage_item = pol
                #self.centerOn(self.coverage_item)
                #self.fitInView(self.coverage_item, QtCore.Qt.KeepAspectRatio)
                #self.ensureVisible(self.coverage_item)
                self.coverage_item.setPen(QtGui.QPen(self.color_coverage,
                                                    self.thick_coverage))
        #self.centerOn(self.coverage_item)
        #self.ensureVisible(self.coverage_item)
        #self.setSceneRect(self.coverage_item.boundingRect())
        self.setSceneRect(self.scene.itemsBoundingRect())
        return

    def draw_walls2(self):
        for i in range(len(self.walls_list)):
            floor_edge = self.walls_list[i][0][1]
            for j in range(len(floor_edge) // 2):
                x1 = self.vesy*(floor_edge[2*j][1])
                y1 = -self.vesx*(floor_edge[2*j][0])
                x2 = x1 + self.vesy*(floor_edge[2*j+1][1])
                y2 = y1 - self.vesx*(floor_edge[2*j+1][0])
                line = self.scene.addLine(x1, y1, x2, y2, self.blackPen)
                self.scene_lines.append(line)
        return

    def task2(self):
        polygon = QtWidgets.QAction(local.add_poly, self)
        polygon.triggered.connect(self.add_poly)
        self.toolbar.addAction(polygon)

    def add_poly_keyboard(self):
        polygon = Polygon(self)
        polygon.show()

    def add_poly_map(self):
        pass

    def analyse_points_update(self):
        self.is_analyse_points = True
        #print("is_analyse_points", self.)
        self.analyse_points = values.get_map_points()
        self.draw_analyse_points()

    def analyse_points_update2(self):
        [self.scene.removeItem(item) for item in self.point_items]
        self.analyse_points = []
        coverage_points = [self.walls_list[0][0][1][i] for i in range(0,
                len(self.walls_list[0][0][1]), 2)]
        min_y = min([coverage_points[i][1] for i in range(len(coverage_points))])
        max_y = max([coverage_points[i][1] for i in range(len(coverage_points))])
        min_x = min([coverage_points[i][0] for i in range(len(coverage_points))])
        max_x = max([coverage_points[i][0] for i in range(len(coverage_points))])
        y_range = int((max_y - min_y) / self.step)
        x_range = int((max_x - min_x) / self.step)

        for i in range(1, y_range):
            line_y = min_y + i*self.step
            coverage_crossing_points = []
            for p in range(len(coverage_points)):
                point = coverage_points[p]
                vector = self.walls_list[0][0][1][2*p+1]
                try:
                    k = vector[0] / vector[1]   # dx / dy
                except:
                    continue
                if k < 10**-6:
                    x_cr = point[0]
                    y_cr = line_y
                else:
                    x_cr = (line_y - point[1])*k + point[0]
                    y_cr = (x_cr - point[0])/k + point[1]
                dot = (x_cr - point[0])*vector[0] + (y_cr - point[1])*vector[1]
                if dot < 0:
                    coverage_crossing_points.append([x_cr, y_cr])
            for j in range(1, x_range):
                isInsideWall = False
                counter = 0
                for cov_point in coverage_crossing_points:
                    if min_x + j*self.step < cov_point[0]:
                        counter += 1
                if counter % 2 == 0:
                    continue
                for w in range(1, len(self.walls_list)):
                    wall_crossing_points = []
                    wall_points = [self.walls_list[w][0][1][i] for i in range(0,
                            len(self.walls_list[w][0][1]), 2)]

                    for p in range(len(wall_points)):
                        point = wall_points[p]
                        vector = self.walls_list[w][0][1][2*p+1]
                        try:
                            k = vector[0] / vector[1]   # dx / dy
                        except:
                            continue
                        if k < 10**-6:
                            x_cr = point[0]
                            y_cr = line_y
                        else:
                            x_cr = (line_y - point[1])*k + point[0]
                            y_cr = (x_cr - point[0])/k + point[1]
                        dot = (x_cr - point[0])*vector[0] + (y_cr - point[1])*vector[1]
                        if dot < 0:
                            wall_crossing_points.append([x_cr, y_cr])
                    counter = 0
                    for w_point in wall_crossing_points:
                        if min_x + j*self.step < w_point[0]:
                            counter += 1
                    if counter % 2 == 1: # Inside wall
                        isInsideWall = True
                        break
                if not isInsideWall:
                    self.analyse_points.append([min_x+j*self.step,
                        min_y + i*self.step, self.walls_list[1][0][1][0][2]])
        self.draw_analyse_points()


    def select_line(self, items):
        for item in items:
            for i in range(len(self.scene_lines)):
                if self.scene_lines[i] == item:
                    # Show 2nd window with 3D points
                    options = Options(i, self)
                    options.show()

    def add_point(self, item):
        if self.addition:
            self.coord = ([self.analyse_points[item][0],
                    self.analyse_points[item][1], self.analyse_points[item][2]])

            if self.addition == 'AP':
                self.access_points.append(self.coord)
                self.show_point_AP(self.coord)
                self.edit_AP()

            elif self.addition == 'user':
                self.users.append(self.coord)
                self.show_point_user(self.coord)
                self.edit_user()

    def show_point_AP(self, coord):
        self.coord = coord
        self.add_ap_icon(coord)
        """
        self.rect_item = QtWidgets.QGraphicsRectItem()
        self.rect_item.setZValue(6)
        self.rect_item.setPen(self.color_ap)
        self.rect_item.setBrush(self.color_ap)
        self.scene.addItem(self.rect_item)
        self.sh1 = 0.6*self.vesy*self.step
        self.sh2 = 0.6*self.vesx*self.step
        self.rect_item.setRect(self.vesy * self.coord[1] - self.sh1/2,
                    -self.vesx * self.coord[0] - self.sh2/2, self.sh1,
                    self.sh2)
        self.items_ap.append(self.rect_item)
        """
        return

    def edit_AP(self):
        """ Window with parameters"""

        self.second_window = SecondWindow()
        self.ap_boxes = []

        label1 = QtWidgets.QLabel(local.nomer)
        label2 = QtWidgets.QLabel(local.ap)
        label3 = QtWidgets.QLabel(local.x)
        label4 = QtWidgets.QLabel(local.y)
        label5 = QtWidgets.QLabel(local.height)
        label6 = QtWidgets.QLabel(local.freq)
        self.second_window.grid.addWidget(label1, 0, 0)
        self.second_window.grid.addWidget(label2, 0, 1)
        self.second_window.grid.addWidget(label3, 0, 2)
        self.second_window.grid.addWidget(label4, 0, 3)
        self.second_window.grid.addWidget(label5, 0, 4)
        self.second_window.grid.addWidget(label6, 0, 5)

        self.ap_box = QtWidgets.QComboBox()
        #self.ap_box.addItems(['WEP-12', 'WOP-12'])
        #self.ap_box.addItems(self.parent.standards)

        self.spin1 = QtWidgets.QDoubleSpinBox()
        self.spin2 = QtWidgets.QDoubleSpinBox()
        self.spin3 = QtWidgets.QDoubleSpinBox()
        self.spin4 = QtWidgets.QDoubleSpinBox()
        self.spin5 = QtWidgets.QSpinBox()
        self.spin1.setRange(-999.99, 999.99)
        self.spin2.setRange(-999.99, 999.99)
        self.spin3.setRange(-999.99, 999.99)
        self.spin4.setRange(-99.99, 99.99)
        self.spin5.setRange(0, 9999)
        self.second_window.grid.addWidget(self.ap_box, 1, 0)
        self.second_window.grid.addWidget(self.spin1, 1, 1)
        self.second_window.grid.addWidget(self.spin2, 1, 2)
        self.second_window.grid.addWidget(self.spin3, 1, 3)
        self.second_window.grid.addWidget(self.spin4, 1, 4)
        self.second_window.grid.addWidget(self.spin5, 1, 5)
        self.spin1.setValue(self.coord[0])
        self.spin2.setValue(self.coord[1])
        self.spin3.setValue(self.coord[2])
        self.spin4.setValue(3.0)
        self.spin5.setValue(5200)

        btn_ok = QtWidgets.QPushButton(local.ok)
        btn_ok.clicked.connect(self.ok_fun_edit_AP)
        btn_cancel = QtWidgets.QPushButton(local.cancel)
        btn_cancel.clicked.connect(self.cancel_fun_edit_AP)
        self.second_window.grid.addWidget(btn_ok, 2, 0)
        self.second_window.grid.addWidget(btn_cancel, 2, 1)

        self.second_window.grid.setRowStretch(100, 1)
        self.second_window.grid.setColumnStretch(1,1)
        self.second_window.grid.setSpacing(5)

    def ok_fun_edit_AP(self):
        self.coord[0] = self.spin1.value()
        self.coord[1] = self.spin2.value()
        self.coord[2] = self.spin3.value()
        self.access_points[-1] = self.coord

        self.height_accomodation_ap = self.spin4.value()
        self.access_points[-1].append(self.height_accomodation_ap)

        self.frequency = self.spin5.value()
        self.access_points[-1].append(self.frequency)

        self.ap_type = self.ap_box.currentIndex()
        self.access_points[-1].append(self.ap_type)
        print(self.ap_type)

        self.second_window.close()
        self.parent.right.add_LE_ap(self.access_points[-1],
                        self.ap_type)
        #self.call_AP_lib(self.access_points[-1])

    def call_AP_lib(self,access_point):
        nbs = values.add_BS(
                BSP = ([0.0, 0, 0.0, access_point[3], access_point[0],
                            access_point[1], access_point[2]]),
                FBS = access_point[4],     # MHz
                BSS = access_point[5]+1,
                AMn = 0,
                AMx = 360,
                HMn = 0,
                HMx = 10,
                PMn = 10,
                PMx = 20,
                EMn = 0,
                EMx = 180,
                NBP = 0  ,        # reserved
                IPBS = 10**5,     # reserved
                MSBS = 10**5 ,    # reserved
        )
        print(nbs)

    def cancel_fun_edit_AP(self):
        """ Remove AP from scene and from list (access_points)"""
        removing_point = self.icon_ap_items.pop()
        self.scene.removeItem(removing_point)
        self.access_points.pop()
        self.second_window.close()

    def show_point_user(self, coord):
        self.coord = coord
        self.add_user_icon(self.coord)
        """
        self.rect_item = QtWidgets.QGraphicsRectItem()
        self.rect_item.setZValue(6)
        self.rect_item.setPen(self.redPen)
        self.rect_item.setBrush(self.redBrush)
        self.scene.addItem(self.rect_item)
        self.sh1 = 0.6*self.vesy*self.step
        self.sh2 = 0.6*self.vesx*self.step
        self.rect_item.setRect(self.vesy * self.coord[1] - self.sh1/2,
                    -self.vesx * self.coord[0] - self.sh2/2, self.sh1,
                    self.sh2)
        self.items_user.append(self.rect_item)
        """
        return

    def edit_user(self):
        """ Window with parameters"""

        self.second_window = SecondWindow()
        self.user_boxes = []

        label1 = QtWidgets.QLabel(local.x)
        label2 = QtWidgets.QLabel(local.y)
        label3 = QtWidgets.QLabel(local.h)
        label4 = QtWidgets.QLabel(local.height)
        label5 = QtWidgets.QLabel(local.dl_users)
        label6 = QtWidgets.QLabel(local.ul_users)
        self.second_window.grid.addWidget(label1, 0, 0)
        self.second_window.grid.addWidget(label2, 0, 1)
        self.second_window.grid.addWidget(label3, 0, 2)
        self.second_window.grid.addWidget(label4, 0, 3)
        self.second_window.grid.addWidget(label5, 2, 0)
        self.second_window.grid.addWidget(label6, 3, 0)
        self.spin1 = QtWidgets.QDoubleSpinBox()
        self.spin2 = QtWidgets.QDoubleSpinBox()
        self.spin3 = QtWidgets.QDoubleSpinBox()
        self.spin4 = QtWidgets.QDoubleSpinBox()
        self.spin5 = QtWidgets.QDoubleSpinBox()
        self.spin6 = QtWidgets.QDoubleSpinBox()
        self.spin1.setRange(-999.99, 999.99)
        self.spin2.setRange(-999.99, 999.99)
        self.spin3.setRange(-999.99, 999.99)
        self.spin4.setRange(-99.99, 99.99)
        self.spin5.setRange(0, 999)
        self.spin6.setRange(0, 999)
        self.second_window.grid.addWidget(self.spin1, 1, 0)
        self.second_window.grid.addWidget(self.spin2, 1, 1)
        self.second_window.grid.addWidget(self.spin3, 1, 2)
        self.second_window.grid.addWidget(self.spin4, 1, 3)
        self.second_window.grid.addWidget(self.spin5, 2, 1)
        self.second_window.grid.addWidget(self.spin6, 3, 1)
        self.spin1.setValue(self.coord[0])
        self.spin2.setValue(self.coord[1])
        self.spin3.setValue(self.coord[2])
        self.spin4.setValue(0.0)
        self.spin5.setValue(1)
        self.spin6.setValue(1)

        btn_ok = QtWidgets.QPushButton(local.ok)
        btn_ok.clicked.connect(self.ok_fun_edit_user)
        btn_cancel = QtWidgets.QPushButton(local.cancel)
        btn_cancel.clicked.connect(self.cancel_fun_edit_user)
        self.second_window.grid.addWidget(btn_ok, 4, 0)
        self.second_window.grid.addWidget(btn_cancel, 4, 1)

        self.second_window.grid.setRowStretch(5, 1)
        self.second_window.grid.setColumnStretch(100,1)
        self.second_window.grid.setSpacing(5)

    def ok_fun_edit_user(self):
        self.coord[0] = self.spin1.value()
        self.coord[1] = self.spin2.value()
        self.coord[2] = self.spin3.value()
        self.users[-1] = self.coord

        self.users[-1].append(self.spin4.value())
        self.users[-1].append(self.spin5.value())
        self.users[-1].append(self.spin6.value())

        #self.parent.right.add_LE_user(self.users)
        self.parent.right.add_LE_user(self.users[-1])
        self.second_window.close()
        self.call_user_lib(self.users[-1])

    def cancel_fun_edit_user(self):
        """ Remove item from scene and from list (users)"""
        removing_point = self.icon_user_items.pop()
        self.scene.removeItem(removing_point)
        self.users.pop()
        self.second_window.close()

    def call_user_lib(self,user):
        nak = values.add_AK(user)

    def ap_update(self):
        #(self.parent.graphicView.v_Npoints)
        for i in range(len(self.right.lines_ap)):
            x_new = self.right.lines_ap[i][0].value()
            y_new = self.right.lines_ap[i][1].value()
            z_new = self.right.lines_ap[i][2].value()

            cond1 = abs(x_new - self.access_points[i][0]) > 10**-2
            cond2 = abs(y_new - self.access_points[i][1]) > 10**-2
            cond3 = abs(z_new - self.access_points[i][2]) > 10**-2

            if cond1 or cond2 or cond3:
                self.ap_update2(i, x_new, y_new, z_new)
        self.right.fill_LE_ap(self.access_points[i], i)

    def ap_update2(self, i, x_new, y_new, z_new): #continue
        for j in range(len(self.analyse_points)):
            cond1 = abs(self.analyse_points[j][0] - x_new) < 10**-1
            cond2 = abs(self.analyse_points[j][1] - y_new) < 10**-1
            if cond1 and cond2:
                # i - line of AP
                # j - point in map in map
                new_coord = self.analyse_points[j][:2]
                new_coord.append(z_new)
                self.access_points[i][:3] = list(new_coord)
                deleting_item = self.icon_ap_items[i]
                self.scene.removeItem(deleting_item)
                self.add_ap_icon(new_coord)


    def user_update(self):
        for i in range(len(self.right.lines_user)):
            x_new = self.right.lines_user[i][0].value()
            y_new = self.right.lines_user[i][1].value()
            z_new = self.right.lines_user[i][2].value()

            cond1 = abs(x_new - self.users[i][0]) > 10**-2
            cond2 = abs(y_new - self.users[i][1]) > 10**-2
            cond3 = abs(z_new - self.users[i][2]) > 10**-2

            if cond1 or cond2 or cond3:
                self.user_update2(i, x_new, y_new, z_new)
        self.right.fill_LE_user(self.users)

    def user_update2(self, i, x_new, y_new, z_new):
        for j in range(self.v_Npoints):
            cond1 = abs(self.v_points[j][0] - x_new) < 10**-1
            cond2 = abs(self.v_points[j][1] - y_new) < 10**-1
            if cond1 and cond2:
                # i - line of AP
                # j - point in map in map
                new_coord = self.v_points[j][:2]
                new_coord.append(z_new)
                self.users[i] = list(new_coord)
                deleting_item = self.items_user[i]
                self.scene.removeItem(deleting_item)
                sh2 = self.sh
                self.new_item2 = self.scene.addRect(self.vesx * self.v_points[j][0] - sh2,
                            self.vesy * self.v_points[j][1] - sh2, 2*sh2,
                            2*sh2, self.redPen, self.redBrush)
                self.items_user[i] = self.new_item2
                self.changed = False
                self.addition = None

    def wheelEvent(self, event):
        if self.is_key_ctrl:
            if event.angleDelta().y() > 0:
                factor = 1.25
                self.scale(factor, factor)
            else:
                factor = 0.8
                self.scale(factor, factor)
        elif self.is_key_shift:
            self.horizontalScrollBar().setValue(self.horizontalScrollBar().value()+
                                                event.angleDelta().y())
        else:
            self.verticalScrollBar().setValue(self.verticalScrollBar().value()-
                                                    event.angleDelta().y())

    def keyPressEvent(self, event):
        super(GraphicsView, self).keyPressEvent(event)
        if event.key() == QtCore.Qt.Key_Control:
            self.is_key_ctrl = True
            print("Key CTRL pressed")
        elif event.key() == QtCore.Qt.Key_Shift:
            self.is_key_shift = True
            print("Key SHIFT pressed")
        elif event.key() == QtCore.Qt.Key_P:
            #self.is_key_shift = True
            print("Key SHIFT pressed")
        elif self.isMoving:
            if event.key() == QtCore.Qt.Key_Escape:
                self.move_object.exit()
                self.move_object = None
            if event.key() == QtCore.Qt.Key_Space:
                self.move_object.rotation()

    def keyReleaseEvent(self, event):
        super(GraphicsView, self).keyReleaseEvent(event)
        self.set_keys_unpressed()
        print("Keys unpressed")

    def contextMenuEvent(self, event):
        if self.isMoving:
            contextMenu = QtWidgets.QMenu(self)

            exit_action = contextMenu.addAction(local.exit)
            copy_action = contextMenu.addAction(local.copy)
            paste_action = contextMenu.addAction(local.paste)

            action = contextMenu.exec_(self.mapToGlobal((event.pos())))
            if action == exit_action:
                self.move_object.exit()
            elif action == copy_action:
                self.move_object.copy_item()
            #else action == paste_action:
            #    self.move_object.paste_item()


class GraphicsScene(QtWidgets.QGraphicsScene):
    def __init__(self, parent=None):
        super(GraphicsScene, self).__init__(parent)
        self.parent = parent
        #self.setFocusOnTouch(True)

    def mousePressEvent(self, event):
        mouse_state = event.button()
        if mouse_state == QtCore.Qt.MouseButton.LeftButton:
            if self.parent.isRect:
                #self.parent.pos1 = self.mapToScene(event.pos())
                self.parent.pos1 = event.scenePos()
                #self.pos1 = event.pos()
                self.parent.isRecting = True
                self.parent.isRect = False
                self.parent.rect = Rect(self.parent, self.parent.pos1,
                                    self.parent.rect_type)
            elif self.parent.isRecting:
                print("rect")
                #self.parent.pos2 = self.mapToScene(event.pos())
                self.parent.pos2 = event.scenePos()
                self.parent.rect.position2(self.parent.pos1,
                                        self.parent.pos2)
                self.parent.isRecting = False
                #self.pos2 = event.pos()

            elif self.parent.isPoly:
                print("poly0")
                #pos1 = self.mapToScene(event.pos())
                #pos1 = self.scenePos()
                pos1 = event.scenePos()
                self.parent.isPolying = True
                self.parent.isPoly = False
                self.parent.parent.parent.show_status_bar()
                if self.parent.isCoverage:
                    print("coverage1")
                    self.parent.coverage_object = Polygon(self.parent, pos1)
                else:
                    print("poly1")
                    self.parent.poly = Polygon(self.parent, pos1)
            elif self.parent.isPolying:
                pos2 = event.scenePos()
                if self.parent.isCoverage:
                    self.parent.coverage_object.position2(pos2)
                else:
                    self.parent.poly.position2(pos2)
            elif self.parent.isImage:
                print('pos1')
                #self.parent.pos1 = self.mapToScene(event.pos())
                self.parent.pos1 = event.scenePos()
                self.parent.isImage = False
                self.parent.isImaging = True
                #self.initialize()
                self.parent.parent.parent.show_status_bar()
                self.parent.rect_image = Rect(self.parent, self.parent.pos1,
                                        rect_type = "image")
            elif self.parent.isImaging:
                print('pos2')
                #self.parent.pos2 = self.mapToScene(event.pos())
                self.parent.pos2 = event.scenePos()
                self.parent.rect_image.image_two_points(self.parent.pos2, end = True)
            else:
                item = self.items(event.scenePos())
                if item:
                    print(item, item[0].type())
                    if item[0].type() == 7: # image
                        self.parent.setDragMode(self.parent.ScrollHandDrag)
                    if item[0] == self.parent.coverage_item:
                        self.parent.setDragMode(self.parent.ScrollHandDrag)
                    elif item[0].type() == 5 and self.parent.isEditing:   # polygon (wall)
                        if not self.parent.isMoving:
                            self.parent.initialize()
                            self.parent.parent.parent.show_status_bar()
                            self.parent.isMoving = True
                            self.parent.parent.parent.show_status_bar()
                            if not self.parent.is_moving_object:
                                self.parent.move_object = Movement(self.parent, item[0])
                    elif self.parent.addition:
                        if item[0].type() == 3: # rect ap, user
                            for i in range(len(self.parent.point_items)):
                                if item[0] == self.parent.point_items[i]:
                                    self.parent.add_point(i)
                        else:
                            self.parent.setDragMode(self.parent.ScrollHandDrag)

                    elif item[0].type() == 6 and self.parent.isEditing: # line, rect
                        if not self.parent.isMoving:
                            self.parent.initialize()
                            self.parent.parent.parent.show_status_bar()
                            self.parent.isMoving = True
                            self.parent.parent.parent.show_status_bar()
                            self.parent.move_object = Movement(self.parent, item[0])
                    else:
                        print("drag1")
                        self.parent.setDragMode(self.parent.ScrollHandDrag)
                else:
                    print("drag2")
                    self.parent.setDragMode(self.parent.ScrollHandDrag)
        elif mouse_state == QtCore.Qt.MouseButton.RightButton:
            if self.parent.isPolying:
                #pos2 = self.mapToScene(event.pos())
                pos2 = event.scenePos()
                if self.parent.isCoverage:
                    self.parent.coverage_object.end_figure(pos2)
                    self.parent.coverage_item = self.parent.coverage_object.wall_pol
                else:
                    self.parent.poly.end_figure(pos2)
        super(GraphicsScene, self).mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.parent.isRecting:
            #pos = self.mapToScene(event.pos())
            pos = event.scenePos()
            self.parent.rect.display(pos)
        elif self.parent.isPolying:
            #pos = self.mapToScene(event.pos())
            pos = event.scenePos()
            if self.parent.isCoverage:
                self.parent.coverage_object.wall_pol.movePoint(
                                self.parent.coverage_object.qt_coordinates, pos)
            else:
                self.parent.poly.wall_pol.movePoint(
                                    self.parent.poly.qt_coordinates, pos)
        elif self.parent.isImaging:
            #pos = self.mapToScene(event.pos())
            pos = event.scenePos()
            self.parent.rect_image.image_two_points(pos)
        #elif self.parent.is_copied_item:

        super(GraphicsScene, self).mouseMoveEvent(event)

    def mouseReleaseEvent(self,event):
        self.parent.setDragMode(QtWidgets.QGraphicsView.NoDrag)
        super(GraphicsScene, self).mouseReleaseEvent(event)


class SecondWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(SecondWindow, self).__init__(parent)
        self.parent = parent

        self.title = "Wi-Fi Planner"
        self.top = 250
        self.left = 250
        self.width = 400
        self.height = 300
        self.InitWindow()

    def InitWindow(self):
        #self.setWindowIcon(QtGui.QIcon("icon.png"))
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.central = QtWidgets.QWidget()
        self.setCentralWidget(self.central)
        self.grid = QtWidgets.QGridLayout(self.central)
        self.central.setLayout(self.grid)
        self.show()



class Rect(QtCore.QObject):
    def __init__(self, parent, pos1, rect_type = None):
        super().__init__()
        self.parent = parent
        self.pos1 = pos1
        self.rect_type = rect_type
        print(self.rect_type)
        self.new_rect = None
        self.new_rect_image = None
        self.number = 4
        self.wall_pol = PolygonItem(self.parent)
        self.wall_pol.setZValue(5)
        self.parent.scene.addItem(self.wall_pol)

        if self.rect_type == "wall":
            self.color = self.parent.color_wall
            self.thickness = self.parent.thick_wall
        elif self.rect_type == "door":
            self.color = self.parent.color_door
            self.thickness = self.parent.thick_door
        elif self.rect_type == "window":
            self.color = self.parent.color_window
            self.thickness = self.parent.thick_window
        elif self.rect_type == "image":
            self.color = self.parent.color_image_rect
            self.thickness = self.parent.thick_image_rect

        self.wall_pol.setPen(QtGui.QPen(self.color, self.thickness))

    def display1(self):
        pass

    def image_two_points(self, pos2, end = False):
        """ Draw 2 points-rect on the image to
            specify the x- and y-sizes of the plan"""
        width = pos2.x() - self.pos1.x()
        height = pos2.y() - self.pos1.y()

        points = []
        points.append(QtCore.QPointF(self.pos1.x(), self.pos1.y()))
        points.append(QtCore.QPointF(self.pos1.x(), pos2.y()))
        points.append(QtCore.QPointF(pos2.x(), pos2.y()))
        points.append(QtCore.QPointF(pos2.x(), self.pos1.y()))

        self.wall_pol.setPolygon(QtGui.QPolygonF(points))
        self.parent.rotate(360)
        if end:
            self.pos2 = pos2
            self.parent.isImaging = False
            self.image_size()

    def image_size(self):
        self.parent.default_cursor()

        self.second_window = SecondWindow(self.parent)
        self.spin = []
        self.second_window.grid.addWidget(QtWidgets.QLabel(
                                    local.spec_dimens), 0, 0, 1, 2)

        self.second_window.grid.addWidget(QtWidgets.QLabel(local.po_x), 1,0)
        self.second_window.grid.addWidget(QtWidgets.QLabel(local.po_y), 2,0)

        self.line1 = QtWidgets.QDoubleSpinBox()
        self.line1.setMaximum(999.99)
        self.line1.setMinimum(-999.99)
        self.spin.append(self.line1)
        self.second_window.grid.addWidget(self.line1, 1, 1)

        self.line2 = QtWidgets.QDoubleSpinBox()
        self.line2.setMaximum(999.99)
        self.line2.setMinimum(-999.99)
        self.spin.append(self.line2)
        self.second_window.grid.addWidget(self.line2, 2, 1)

        self.image_btn_ok = QtWidgets.QPushButton(local.ok)
        self.second_window.grid.addWidget(self.image_btn_ok, 3, 1)
        self.image_btn_ok.clicked.connect(self.image_btn_ok_fun)

        self.second_window.grid.setRowStretch(4, 1)
        self.second_window.grid.setColumnStretch(2,1)
        self.second_window.grid.setSpacing(10)

    def image_btn_ok_fun(self):
        x = self.spin[0].value()
        y = self.spin[1].value()
        print('Ves calculated')
        self.parent.vesx = -(self.pos2.x() - self.pos1.x()) / x
        self.parent.vesy = (self.pos2.y() - self.pos1.y()) / y
        self.second_window.close()
        self.parent.imageProcessing.hideRect()

    def display(self, pos2):
        width = pos2.x() - self.pos1.x()
        height = pos2.y() - self.pos1.y()

        points = []
        points.append(QtCore.QPointF(self.pos1.x(), self.pos1.y()))
        points.append(QtCore.QPointF(self.pos1.x(), pos2.y()))
        points.append(QtCore.QPointF(pos2.x(), pos2.y()))
        points.append(QtCore.QPointF(pos2.x(), self.pos1.y()))

        self.wall_pol.setPolygon(QtGui.QPolygonF(points))
        self.parent.rotate(360)

        self.parent.show()


    def position2(self, pos1, pos2):
        self.pos2 = pos2
        self.parent.show()
        self.lines = []
        self.parent.isRecting = False
        self.parent.isRect = True

        width = self.pos2.x() - self.pos1.x()
        height = self.pos2.y() - self.pos1.y()

        points = []
        points.append(QtCore.QPointF(self.pos1.x(), self.pos1.y()))
        points.append(QtCore.QPointF(self.pos1.x(), self.pos2.y()))
        points.append(QtCore.QPointF(self.pos2.x(), self.pos2.y()))
        points.append(QtCore.QPointF(self.pos2.x(), self.pos1.y()))
        self.wall_pol.setPolygon(QtGui.QPolygonF(points))
        self.wall_pol.set_poly(points)
        self.parent.rotate(360)

        self.coordinates = [[-self.pos1.y()/self.parent.vesx, self.pos1.x()/self.parent.vesy],
                        [-self.pos2.y()/self.parent.vesx, self.pos1.x()/self.parent.vesy],
                        [-self.pos2.y()/self.parent.vesx, self.pos2.x()/self.parent.vesy],
                        [-self.pos1.y()/self.parent.vesx, self.pos2.x()/self.parent.vesy]]
        self.show_coordinates()

    def show_coordinates(self):
        self.parent.default_cursor()
        self.second_window = SecondWindow(self.parent)
        self.spin = []
        self.spinbox_changed = False

        self.second_window.grid.addWidget(QtWidgets.QLabel("x"), 1, 2)
        self.second_window.grid.addWidget(QtWidgets.QLabel("y"), 1, 3)
        for i in range(self.number):
            self.line1 = QtWidgets.QDoubleSpinBox()
            self.line1.setMaximum(999.99)
            self.line1.setMinimum(-999.99)
            self.line1.setValue(self.coordinates[i][0])
            self.line1.valueChanged[float].connect(self.change_value1)
            self.spin.append(self.line1)

            self.line2 = QtWidgets.QDoubleSpinBox()
            self.line2.setMaximum(999.99)
            self.line2.setMinimum(-999.99)
            self.line2.setValue(self.coordinates[i][1])
            self.line2.valueChanged[float].connect(self.change_value1)
            self.spin.append(self.line2)

            self.second_window.grid.addWidget(QtWidgets.QLabel("{}".format(i+1)),i+2, 1)
            self.second_window.grid.addWidget(self.line1, i+2, 2)
            self.second_window.grid.addWidget(self.line2, i+2, 3)

        self.height_line = QtWidgets.QDoubleSpinBox()
        self.height_line.setRange(-999.99, 999.99)
        self.height_line.setValue(3.0)  # высота по умолчанию
        self.spin.append(self.height_line)
        self.second_window.grid.addWidget(QtWidgets.QLabel("H:"), self.number+2, 2)
        self.second_window.grid.addWidget(self.height_line, self.number+2, 3)

        self.materials_box = QtWidgets.QComboBox()
        self.materials_box.addItems(self.parent.parent.materials)
        self.second_window.grid.addWidget(QtWidgets.QLabel(local.materials),
                                self.number+3, 2)
        self.second_window.grid.addWidget(self.materials_box,
                            self.number+3, 3)

        self.btn_ok = QtWidgets.QPushButton(local.ok)
        self.second_window.grid.addWidget(self.btn_ok, self.number+4, 2)
        self.btn_ok.clicked.connect(self.ok_fun)

        self.btn_cancel = QtWidgets.QPushButton(local.cancel)
        self.second_window.grid.addWidget(self.btn_cancel, self.number+4, 3)
        self.btn_cancel.clicked.connect(self.cancel_fun)

        self.second_window.grid.setRowStretch(self.number+5, 1)
        self.second_window.grid.setColumnStretch(4,1)
        self.second_window.grid.setSpacing(10)


    def change_value1(self):
        self.spinbox_changed = True

    def cancel_fun(self):
        self.second_window.close()
        self.parent.scene.removeItem(self.wall_pol)
        # or remove it in self.wall_pol.remove()
        self.parent.cross_cursor()

    def ok_fun(self):
        self.parent.cross_cursor()
        if not self.spinbox_changed:
            self.height = self.height_line.value()
            #self.material = self.materials_box.currentIndex()
            self.material = self.materials_box.currentText()
            self.add_Object_lib()
        else:
            self.coordinates = []
            for i in range(self.number):
                x = self.spin[2*i].value()
                y = self.spin[2*i+1].value()
                self.coordinates.append([x, y])
            self.height = self.height_line.value()
            #self.material = self.materials_box.currentIndex()
            self.material = self.materials_box.currentText()
            self.replot_rect()
            self.add_Object_lib()
        self.second_window.close()

    def replot_rect(self):
        self.qt_coordinates = []
        for coord in self.coordinates:
            self.qt_coordinates.append(QtCore.QPointF(
                        self.parent.vesx*coord[1],
                        -self.parent.vesy*coord[0]))
        self.wall_pol.setPolygon(QtGui.QPolygonF(self.qt_coordinates))

    def add_Object_lib(self):
        [self.coordinates[i].append(0.0) for i in range(4)]
        object_par = [0.0, # AP
                        0.0,  # HA
                        self.height, # HR
                        1, # Zone
                        *self.coordinates[0],
                        *[self.coordinates[2][j] - self.coordinates[0][j]
                                                for j in range(3)]
                        ]
        self.object_index = values.add_Object(object_par,self.material)
        print("object: ", self.object_index)
        print("number of lines: ", self.number)
        for i1 in range(6):
            self.add_Plane_lib(i1)

    def add_Plane_lib(self, i1):
        if i1 == 0:     # Floor
            print("save", i1)
            DR = [0.0, 0.0, -1.0]
            plane_index = values.add_Plane(self.object_index, DR)
            for i in range(self.number):
                if i != self.number - 1:
                    point1 = self.coordinates[i]
                    point2 = [self.coordinates[i+1][j] - self.coordinates[i][j]
                                for j in range(3)]
                    values.add_Line(self.object_index, plane_index,
                                    point1, point2)
                else:
                    point1 = [*self.coordinates[i], 0.0]
                    point2 = [self.coordinates[0][j] - self.coordinates[i][j]
                                for j in range(3)]
                    values.add_Line(self.object_index, plane_index,
                                    point1, point2)
        elif i1 == 1:   # Ceil
            print("save", i1)
            DR = [0.0, 0.0, 1.0]
            plane_index = values.add_Plane(self.object_index, DR)
            for i in range(self.number):
                if i != self.number - 1:
                    point1 = self.coordinates[i]
                    point1[2] = self.height
                    point2 = [self.coordinates[i+1][j] - self.coordinates[i][j]
                                for j in range(3)]
                    point2[2] = self.height
                    values.add_Line(self.object_index, plane_index,
                                    point1, point2)
                else:
                    point1 = [*self.coordinates[i], 0.0]
                    point2 = [self.coordinates[0][j] - self.coordinates[i][j]
                                for j in range(3)]
                    values.add_Line(self.object_index, plane_index,
                                    point1, point2)
        else:
            print("save", i1)
            if i1 != self.number+1:
                line = [self.coordinates[i1-2], self.coordinates[i1-1]]
            else:
                line = [self.coordinates[i1-2], self.coordinates[0]]
            line_h = list(line)
            line_h[0][2] = self.height
            line_h[1][2] = self.height
            try:
                DR = [1.0, -1*(line[1][0] - line[0][0])/(line[1][1] - line[1][0]),
                        0.0]
                DR = values.vector_normalized(DR)
            except:
                DR = [0.0, -1.0, 0.0]
            plane_index = values.add_Plane(self.object_index, DR)

            spoint = list(line[0])
            dir = [line[1][j] - line[0][j] for j in range(3)]
            values.add_Line(self.object_index, plane_index, spoint, dir)

            spoint = list(line[1])
            dir = [line_h[1][j] - line[1][j] for j in range(3)]
            values.add_Line(self.object_index, plane_index, spoint, dir)

            spoint = list(line_h[1])
            dir = [line_h[0][j] - line_h[1][j] for j in range(3)]
            values.add_Line(self.object_index, plane_index, spoint, dir)

            spoint = list(line_h[0])
            dir = [line[0][j] - line_h[0][j] for j in range(3)]
            values.add_Line(self.object_index, plane_index, spoint, dir)

    def cancel_fun2(self): #delete
        [self.parent.scene.removeItem(line) for line in self.lines]
        self.second_window.close()


class Polygon(QtCore.QObject):
    def __init__(self, parent, pos1):
        super().__init__()
        self.parent = parent
        self.new_pos = pos1
        self.old_pos = pos1
        self.new_rect = None
        self.number = 1
        self.lines = list()
        self.coordinates = []
        self.qt_coordinates = []
        self.wall_pol = PolygonItem(self.parent)
        self.wall_pol.setZValue(5)
        self.parent.scene.addItem(self.wall_pol)
        coord = [-1*self.new_pos.y()/self.parent.vesx,
                    self.new_pos.x()/self.parent.vesy]
        self.qt_coordinates.append(self.new_pos)
        self.qt_coordinates.append(self.new_pos)
        self.coordinates.append(coord)
        self.coordinates.append(coord)
        self.wall_pol.add_point(self.new_pos)
        self.wall_pol.add_point(self.new_pos)
        self.l_new = None
        if self.parent.isCoverage:
            self.wall_pol.setPen(QtGui.QPen(self.parent.color_coverage,
                                            self.parent.thick_coverage,))
        else:
            self.wall_pol.setPen(QtGui.QPen(self.parent.color_wall,
                                            self.parent.thick_wall))

    def position2(self, pos2):
        self.new_pos = pos2
        self.number += 1
        coord = [-1*self.new_pos.y()/self.parent.vesx,
                    self.new_pos.x()/self.parent.vesy]
        self.qt_coordinates.pop()
        self.qt_coordinates.append(self.new_pos)
        self.qt_coordinates.append(self.new_pos)
        self.coordinates.pop()
        self.coordinates.append(coord)
        self.coordinates.append(coord)
        self.wall_pol.remove_last_point()
        self.wall_pol.add_point(self.new_pos)
        self.wall_pol.add_point(self.new_pos)
        self.wall_pol.setPolygon(QtGui.QPolygonF(self.qt_coordinates))
        #self.wall_pol.set_poly(self.qt_coordinates)
        self.old_pos = self.new_pos

    def end_figure(self, pos2):
        coord = [-pos2.y()/self.parent.vesx, pos2.x()/self.parent.vesy]
        self.qt_coordinates.pop()
        self.coordinates.pop()
        self.wall_pol.remove_last_point()
        self.wall_pol.setPolygon(QtGui.QPolygonF(self.qt_coordinates))
        #self.wall_pol.set_poly(self.qt_coordinates)
        self.parent.isPolying = False
        self.parent.isPoly = True
        if self.parent.isCoverage:
            self.parent.isCoverageDone = True
            self.parent.isPoly = False
        self.parent.parent.parent.update_actions()
        self.show_coordinates()

    def add_area_lib(self):
        self.NS = 1
        self.NM = 100
        self.ID = 10**6
        self.IU = 10**6
        self.area_index = values.add_Area(self.NS, self.NM, self.ID, self.IU)
        self.add_area_points_lib()

    def add_area_points_lib(self):
        for point in self.coordinates:
            res = values.add_AreaPoints(self.area_index, [*point, 0.0])

    def add_Object_lib(self):
        [self.coordinates[i].append(0.0) for i in range(self.number)]
        object_par = [0.0, # AP
                        0.0,  # HA
                        self.height, # HR
                        1, # Zone
                        *self.coordinates[0],
                        *[self.coordinates[2][j] - self.coordinates[0][j]
                                                for j in range(3)],
                        ]
        self.object_index = values.add_Object(object_par, self.material)
        print("object: ", self.object_index)
        print("number of lines: ", self.number)
        for i in range(self.number+2):
            self.add_Plane_lib(i)

    def add_Plane_lib(self, i1):
        if i1 == 0:     # Floor
            print("save", i1)
            DR = [0.0, 0.0, -1.0]
            plane_index = values.add_Plane(self.object_index, DR)
            for i in range(self.number):
                if i != self.number - 1:
                    point1 = self.coordinates[i]
                    point2 = [self.coordinates[i+1][j] - self.coordinates[i][j]
                                for j in range(3)]
                    values.add_Line(self.object_index, plane_index,
                                    point1, point2)
                else:
                    point1 = [*self.coordinates[i], 0.0]
                    point2 = [self.coordinates[0][j] - self.coordinates[i][j]
                                for j in range(3)]
                    values.add_Line(self.object_index, plane_index,
                                    point1, point2)
        elif i1 == 1:   # Ceil
            print("save", i1)
            DR = [0.0, 0.0, 1.0]
            plane_index = values.add_Plane(self.object_index, DR)
            for i in range(self.number):
                if i != self.number - 1:
                    point1 = self.coordinates[i]
                    point1[2] = self.height
                    point2 = [self.coordinates[i+1][j] - self.coordinates[i][j]
                                for j in range(3)]
                    point2[2] = self.height
                    values.add_Line(self.object_index, plane_index,
                                    point1, point2)
                else:
                    point1 = [*self.coordinates[i], 0.0]
                    point2 = [self.coordinates[0][j] - self.coordinates[i][j]
                                for j in range(3)]
                    values.add_Line(self.object_index, plane_index,
                                    point1, point2)
        else:
            print("save", i1)
            if i1 != self.number+1:
                line = [self.coordinates[i1-2], self.coordinates[i1-1]]
            else:
                line = [self.coordinates[i1-2], self.coordinates[0]]
            line_h = list(line)
            line_h[0][2] = self.height
            line_h[1][2] = self.height
            try:
                DR = [1.0, -1*(line[1][0] - line[0][0])/(line[1][1] - line[1][0]),
                        0.0]
                DR = values.vector_normalized(DR)
            except:
                DR = [0.0, -1.0, 0.0]
            plane_index = values.add_Plane(self.object_index, DR)

            spoint = list(line[0])
            dir = [line[1][j] - line[0][j] for j in range(3)]
            values.add_Line(self.object_index, plane_index, spoint, dir)

            spoint = list(line[1])
            dir = [line_h[1][j] - line[1][j] for j in range(3)]
            values.add_Line(self.object_index, plane_index, spoint, dir)

            spoint = list(line_h[1])
            dir = [line_h[0][j] - line_h[1][j] for j in range(3)]
            values.add_Line(self.object_index, plane_index, spoint, dir)

            spoint = list(line_h[0])
            dir = [line[0][j] - line_h[0][j] for j in range(3)]
            values.add_Line(self.object_index, plane_index, spoint, dir)

    def show_coordinates(self):
        self.parent.default_cursor()
        self.second_window = SecondWindow(self.parent)
        self.spin = []
        self.spinbox_changed = False

        self.second_window.grid.addWidget(QtWidgets.QLabel("x"), 0, 1)
        self.second_window.grid.addWidget(QtWidgets.QLabel("y"), 0, 2)
        for i in range(self.number):
            self.second_window.grid.addWidget(
                                QtWidgets.QLabel("{}".format(i+1)),i+1, 0)

            self.line1 = QtWidgets.QDoubleSpinBox()
            self.line1.setMaximum(999.99)
            self.line1.setMinimum(-999.99)
            self.line1.setValue(self.coordinates[i][0])
            self.line1.valueChanged[float].connect(self.change_value1)
            self.spin.append(self.line1)

            self.line2 = QtWidgets.QDoubleSpinBox()
            self.line2.setMaximum(999.99)
            self.line2.setMinimum(-999.99)
            self.line2.setValue(self.coordinates[i][1])
            self.line2.valueChanged[float].connect(self.change_value1)
            self.spin.append(self.line2)

            self.second_window.grid.addWidget(self.line1, i+1, 1)
            self.second_window.grid.addWidget(self.line2, i+1, 2)

        if not self.parent.isCoverage:
            self.height_line = QtWidgets.QDoubleSpinBox()
            self.height_line.setRange(-999.99, 999.99)
            self.height_line.setValue(1.0)
            self.spin.append(self.height_line)
            self.second_window.grid.addWidget(QtWidgets.QLabel("H"), self.number+1, 1)
            self.second_window.grid.addWidget(self.height_line, self.number+1, 2)

            self.materials_box = QtWidgets.QComboBox()
            self.materials_box.addItems(self.parent.parent.materials)
            self.second_window.grid.addWidget(QtWidgets.QLabel(local.materials),
                                    self.number+2, 1)
            self.second_window.grid.addWidget(self.materials_box,
                                self.number+2, 2)

        self.btn_ok = QtWidgets.QPushButton(local.ok)
        self.second_window.grid.addWidget(self.btn_ok, self.number+3, 1)
        self.btn_ok.clicked.connect(self.ok_fun)

        self.btn_cancel = QtWidgets.QPushButton(local.cancel)
        self.second_window.grid.addWidget(self.btn_cancel, self.number+3, 2)
        self.btn_cancel.clicked.connect(self.cancel_fun)

        self.second_window.grid.setRowStretch(self.number+4, 1)
        self.second_window.grid.setColumnStretch(3,1)
        self.second_window.grid.setSpacing(10)

    def change_value1(self):
        self.spinbox_changed = True

    def ok_fun(self):
        self.parent.cross_cursor()
        if not self.parent.isCoverage:
            #self.material = self.materials_box.currentIndex()
            self.material = self.materials_box.currentText()
            print(self.material)
            self.height = self.height_line.value()
        if not self.spinbox_changed:
            #self.save_poly(self.coordinates)
            self.second_window.close()
            if self.parent.isCoverage:
                self.parent.isCoverageDone = True
                self.parent.default_cursor()
                self.add_area_lib()
            else:
                self.add_Object_lib()
        else:
            self.new_coordinates = []
            for i in range(self.number):
                x = self.spin[2*i+1].value()
                y = -self.spin[2*i].value()
                self.new_coordinates.append([x, y])
            #self.height = self.height_line.value()
            self.replot_poly()

    def cancel_fun(self):
        self.second_window.close()

    def replot_poly(self):
        self.qt_coordinates = []
        for i in range(len(self.new_coordinates)):
            self.qt_coordinates.append(QtCore.QPointF(
                        self.parent.vesy*self.new_coordinates[i][1],
                        -self.parent.vesx*self.new_coordinates[i][0]))
        self.wall_pol.setPolygon(QtGui.QPolygonF(self.qt_coordinates))
        if self.parent.isCoverage:
            self.parent.isCoverageDone = True
            self.add_area_lib()
        else:
            self.add_Object_lib()



class PolygonItem(QtWidgets.QGraphicsPolygonItem):
    def __init__(self, parent=None):
        super(PolygonItem, self).__init__()
        self.parent = parent
        self.setFlag(QtWidgets.QGraphicsItem.ItemSendsGeometryChanges, True)
        self.grip_items = []
        self.grip_points = []
        if self.parent.isCoverage:
            self.coverage_index = self.parent.current_coverage_index
            self.parent.current_coverage_index += 1
            print("coverage index: ", self.coverage_index)
        elif self.parent.isImage:
            pass
        else:
            self.wall_index = self.parent.current_wall_index
            self.parent.current_wall_index += 1
            #print("wall index: ", self.wall_index)

    def set_poly(self, points):
        self.coordinates = []
        for point in points:
            self.add_point(point)
        self.setPolygon(QtGui.QPolygonF(points))
        for item in self.grip_items:
            item.hide()
        pass

    def add_point(self, pos):
        gripItem = GripItem(self, len(self.grip_points))
        gripItem.hide()
        self.grip_points.append(pos)
        #self.scene().addItem(gripItem)
        self.scene().addItem(gripItem)
        self.grip_items.append(gripItem)
        gripItem.setPos(pos)

    def remove_last_point(self):
        if self.grip_points:
            self.grip_points.pop()
            self.setPolygon(QtGui.QPolygonF(self.grip_points))
            #self.setPolygon(QtGui.QPolygonF(self.poly_points))
            it = self.grip_items.pop()
            self.scene().removeItem(it)
            del it

    def movePoint(self, points, pos):
        points[-1] = pos
        self.setPolygon(QtGui.QPolygonF(points))

    def movePoint_any(self, index, pos):
        if 0 <= index < len(self.grip_points):
            self.grip_points[index] = self.mapFromScene(pos)
            self.setPolygon(QtGui.QPolygonF(self.grip_points))

    def move_item(self, index, pos):
        if 0 <= index < len(self.grip_items):
            item = self.grip_items[index]
            item.setEnabled(False)
            item.setPos(pos)
            #self.grip_points[index] = self.mapFromScene(pos)
            item.setEnabled(True)

    def itemChange(self, change, value):
        if change == QtWidgets.QGraphicsItem.ItemPositionHasChanged:
            for i, point in enumerate(self.grip_points):
                self.move_item(i, self.mapToScene(point))
        return super(PolygonItem, self).itemChange(change, value)

    def remove_all_grips(self):
        for grip in self.grip_items:
            self.scene().removeItem(grip)
            del grip


class GripItem(QtWidgets.QGraphicsPathItem):
    circle = QtGui.QPainterPath()
    circle.addEllipse(QtCore.QRectF(-2, -2, 4, 4))
    #coords = []

    def __init__(self, corresponding_item, index):
        super(GripItem, self).__init__()

        self.corresponding_item = corresponding_item
        self.grip_index = index
        self.setPath(GripItem.circle)
        self.setBrush(QtGui.QColor("green"))
        self.setPen(QtGui.QPen(QtGui.QColor("green"), 2))
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable, True)
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QtWidgets.QGraphicsItem.ItemSendsGeometryChanges, True)
        self.setZValue(16)

    def mouseReleaseEvent(self, event):
        self.setSelected(False)
        super(GripItem, self).mouseReleaseEvent(event)

    def itemChange(self, change, value):
        if change == QtWidgets.QGraphicsItem.ItemPositionChange and self.isEnabled():
            self.corresponding_item.movePoint_any(self.grip_index, value)
        return super(GripItem, self).itemChange(change, value)


    def itemChange_old(self, change, value):
        if change == QtWidgets.QGraphicsItem.ItemPositionChange and self.isEnabled():
            if self.parent.parent.isCoverage:
                self.corresponding_item.movePoint_any(
                            self.parent.qt_coordinates, value, self.grip_index, self)
            else:
                self.corresponding_item.movePoint_any(self.parent.qt_coordinates,
                                value, self.grip_index, self)
        return super(GripItem, self).itemChange(change, value)


class Save_object():
    @staticmethod
    def add_Object_lib(coordinates, number, height, material):
        [coordinates[i].append(0.0) for i in range(number)]
        object_par = [0.0, # AP
                        0.0,  # HA
                        height, # HR
                        1, # Zone
                        *coordinates[0],
                        *[coordinates[2][j] - coordinates[0][j]
                                                for j in range(3)],
                        material]
        object_index = values.add_Object(object_par)
        print("object: ", object_index)
        print("number of lines: ", number)
        for i in range(number+2):
            self.add_Plane_lib(coordinates, number, height, object_index, i)

    @staticmethod
    def change_planes(coordinates, num_points, height, object_index):
        for i in range(num_points+2):
            Save_object.add_Plane_lib(coordinates, num_points,
                            object_index, i)
        pass

    @staticmethod
    def add_Plane_lib(coordinates, number, object_index, i1):
        height = 3.0
        [coordinates[i].append(0.0) for i in range(number)]
        if i1 == 0:     # Floor
            print("save", i1)
            DR = [0.0, 0.0, -1.0]
            plane_index = values.add_Plane(object_index, DR)
            for i in range(number):
                print('i:', i)
                if i != number - 1:
                    point1 = coordinates[i]
                    point2 = [coordinates[i+1][j] - coordinates[i][j]
                                for j in range(3)]
                    values.add_Line(object_index, plane_index,
                                    point1, point2)
                else:
                    point1 = [*coordinates[i], 0.0]
                    point2 = [coordinates[0][j] - coordinates[i][j]
                                for j in range(3)]
                    values.add_Line(object_index, plane_index,
                                    point1, point2)
        elif i1 == 1:   # Ceil
            print("save", i1)
            DR = [0.0, 0.0, 1.0]
            plane_index = values.add_Plane(object_index, DR)
            for i in range(number):
                if i != number - 1:
                    point1 = coordinates[i]
                    point1[2] = height
                    point2 = [coordinates[i+1][j] - coordinates[i][j]
                                for j in range(3)]
                    point2[2] = height
                    values.add_Line(object_index, plane_index,
                                    point1, point2)
                else:
                    point1 = [*coordinates[i], 0.0]
                    point2 = [coordinates[0][j] - coordinates[i][j]
                                for j in range(3)]
                    values.add_Line(object_index, plane_index,
                                    point1, point2)
        else:
            print("save", i1)
            if i1 != number+1:
                line = [coordinates[i1-2], coordinates[i1-1]]
            else:
                line = [coordinates[i1-2], coordinates[0]]
            line_h = list(line)
            line_h[0][2] = height
            line_h[1][2] = height
            try:
                DR = [1.0, -1*(line[1][0] - line[0][0])/(line[1][1] - line[1][0]),
                        0.0]
                DR = values.vector_normalized(DR)
            except:
                DR = [0.0, -1.0, 0.0]
            plane_index = values.add_Plane(object_index, DR)

            spoint = list(line[0])
            dir = [line[1][j] - line[0][j] for j in range(3)]
            values.add_Line(object_index, plane_index, spoint, dir)

            spoint = list(line[1])
            dir = [line_h[1][j] - line[1][j] for j in range(3)]
            values.add_Line(object_index, plane_index, spoint, dir)

            spoint = list(line_h[1])
            dir = [line_h[0][j] - line_h[1][j] for j in range(3)]
            values.add_Line(object_index, plane_index, spoint, dir)

            spoint = list(line_h[0])
            dir = [line[0][j] - line_h[0][j] for j in range(3)]
            values.add_Line(object_index, plane_index, spoint, dir)


class Movement(QtCore.QObject):
    def __init__(self, parent, mov_object):
        super().__init__()
        self.parent = parent
        self.parent.is_moving_object = True
        self.mov_object = mov_object
        self.paste_item = None
        #self.old_coordinates = self.mov_object.coordinates
        self.old_coordinates = self.get_coords(self.mov_object.grip_points)
        print("Enter movement", self.mov_object.coordinates)
        self.stored_pen = self.mov_object.pen()
        self.mov_object.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable, True)
        self.mov_object.setZValue(15)
        self.mov_object.setPen(self.parent.redPen)
        self.parent.isMoving = True
        self.transform = QtGui.QTransform()
        self.grip_items_show()

    def get_coords(self, qt_points):
        self.num_planes = len(qt_points)
        print('num_planes', self.num_planes)
        coordinates = []  # 2D
        #item_shift = self.mov_object.mapToScene(self.mov_object.pos())
        item_shift = self.mov_object.scenePos()
        #print("item pos:", -item_shift.y() / self.parent.vesx,
        #                    item_shift.x() / self.parent.vesy)
        for point in qt_points:
            #print('point:', point)
            #point = self.parent.mapFromScene(point)
            coordinates.append([-(point.y()+item_shift.y()) / self.parent.vesx,
                                (point.x()+item_shift.x()) / self.parent.vesy])
        print('coordinates:', coordinates)
        return coordinates

    def rotation(self):
        self.transform.rotate(90)
        self.mov_object.setTransform(self.transform)
        return

    def grip_items_show(self):
        try:
            for item in self.mov_object.grip_items:
                item.show()
        except:
            print("No grips")

    def grip_items_hide(self):
        try:
            for item in self.mov_object.grip_items:
                item.hide()
        except:
            print("No grips")

    def show_parameters(self):
        """ TabWidget with common info about object
            and tabs to each plane """
        pass

    def copy_item(self):
        """ Store item to copied_item """
        self.parent.is_copied_item = True
        self.copied_item = self.move_object
        self.wall_pol = PolygonItem(self.parent)
        self.wall_pol.setZValue(5)

        self.wall_pol.setPolygon(QtGui.QPolygonF(self.move_object.grip_points))
        pass

    def paste_item(self):
        """ Create new item based on copied_item """
        pass

    def remove_item(self):
        pass

    def change_object(self):
        self.height = 3.0
        print('clear', values.ClearPlanes(self.mov_object.wall_index))
        Save_object.change_planes(self.new_coordinates, self.num_planes,
                self.height, self.mov_object.wall_index)
        pass

    def exit(self):
        self.new_coordinates = self.get_coords(self.mov_object.grip_points)
        self.change_object()   #todo
        print("new_coordinates", self.new_coordinates)
        #self.mov_object.setPen(self.parent.blackPen)
        self.parent.is_moving_object = False
        self.mov_object.setPen(self.stored_pen)
        self.mov_object.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable, False)
        self.parent.isMoving = False
        self.grip_items_hide()
        return



class Options(SecondWindow):
    def __init__(self, index, parent=None):
        super(Options, self).__init__(parent)
        self.index = index
        self.parent = parent
        self.central = QtWidgets.QWidget()
        self.setCentralWidget(self.central)
        self.parent.scene_lines[self.index].setPen(self.parent.redPen)

        self.grid = QtWidgets.QGridLayout()
        self.central.setLayout(self.grid)

        self.spin_tmp1 = QtWidgets.QDoubleSpinBox()
        self.spin_tmp1.setRange(-999.99, 999.99)
        self.spin_tmp2 = QtWidgets.QDoubleSpinBox()
        self.spin_tmp2.setRange(-999.99, 999.99)
        self.spin_tmp3 = QtWidgets.QDoubleSpinBox()
        self.spin_tmp3.setRange(-999.99, 999.99)
        self.spin_tmp4 = QtWidgets.QDoubleSpinBox()
        self.spin_tmp4.setRange(-999.99, 999.99)

        self.grid.addWidget(QtWidgets.QLabel("x1"), 0, 0, alignment=QtCore.Qt.AlignTop)
        self.grid.addWidget(self.spin_tmp1, 0, 1, alignment=QtCore.Qt.AlignTop)

        self.grid.addWidget(QtWidgets.QLabel("y1"), 0, 2, alignment=QtCore.Qt.AlignTop)
        self.grid.addWidget(self.spin_tmp2, 0, 3, alignment=QtCore.Qt.AlignTop)

        self.grid.addWidget(QtWidgets.QLabel("x2"), 1, 0, alignment=QtCore.Qt.AlignTop)
        self.grid.addWidget(self.spin_tmp3, 1, 1, alignment=QtCore.Qt.AlignTop)

        self.grid.addWidget(QtWidgets.QLabel("y2"), 1, 2, alignment=QtCore.Qt.AlignTop)
        self.grid.addWidget(self.spin_tmp4, 1, 3, alignment=QtCore.Qt.AlignTop)
        self.optionsShow()

    def optionsShow(self):
        for i in range(1, len(self.parent.scene_lines)):
            if self.parent.scene_lines[i] >= self.index:
                a = self.index - self.parent.scene_lines[i-1]
                b = i
                for j in range(1, len(self.parent.v_Faces)):
                    if self.parent.v_Faces[j] >= b:
                        break
                break

    def closeEvent(self, event):
        self.parent.scene_lines[self.index].setPen(self.parent.redPen)



class ImageProcessing():
    def __init__(self, parent = None):
        self.parent = parent
        self.image_two_points()

    def image_two_points(self):
        self.parent.isImage = True
        self.window = SecondWindow()
        label = QtWidgets.QLabel(local.img_rect)
        self.window.grid.addWidget(label, 0, 0, 2, 2)

        self.btn_ok = QtWidgets.QPushButton(local.ok)
        self.window.grid.addWidget(self.btn_ok, 2, 0)
        self.btn_ok.clicked.connect(self.fun_ok)

        self.btn_cancel = QtWidgets.QPushButton(local.cancel)
        self.window.grid.addWidget(self.btn_cancel, 2, 1)
        self.btn_cancel.clicked.connect(self.fun_cancel)

    def fun_ok(self):
        self.parent.cross_cursor()
        self.window.close()

    def fun_cancel(self):
        #self.parent.isImage = False
        self.parent.isImageShow = False
        self.parent.init_done = False
        self.parent.removeImage()
        self.window.close()

    def hideRect(self):
        #self.parent.scene.removeItem(self.parent.rect_image.wall_pol)
        self.parent.rect_image.wall_pol.hide()


class Report():
    def __init__(self, parent = None):
        self.parent = parent
        self.window = SecondWindow(self.parent)
        self.tabs = QtWidgets.QTabWidget()
        self.window.grid.addWidget(self.tabs, 0, 0)

    def report_ap(self):
        self.tab_table_ap = QtWidgets.QTableWidget(self.window)
        self.tabs.addTab(self.tab_table_ap, local.ap)
        self.tab_table_ap.setColumnCount(6)
        self.tab_table_ap.setRowCount(len(self.parent.access_points))
        self.tab_table_ap.setHorizontalHeaderLabels([local.type, local.x, local.y,
                                         local.h, local.height, local.freq])
        print(self.parent.access_points)
        for i in range(len(self.parent.access_points)):
            standard = self.parent.parent.standards[self.parent.access_points[i][5]]
            self.tab_table_ap.setItem(i, 0, QtWidgets.QTableWidgetItem(
                str(standard)))
            self.tab_table_ap.setItem(i, 1, QtWidgets.QTableWidgetItem(
                str(self.parent.access_points[i][0])))
            self.tab_table_ap.setItem(i, 2, QtWidgets.QTableWidgetItem(
                str(self.parent.access_points[i][1])))
            self.tab_table_ap.setItem(i, 3, QtWidgets.QTableWidgetItem(
                str(self.parent.access_points[i][2])))
            self.tab_table_ap.setItem(i, 4, QtWidgets.QTableWidgetItem(
                str(self.parent.access_points[i][3])))
            self.tab_table_ap.setItem(i, 5, QtWidgets.QTableWidgetItem(
                str(self.parent.access_points[i][4])))

    def report_users(self):
        self.tab_table_users = QtWidgets.QTableWidget(self.window)
        self.tabs.addTab(self.tab_table_users, local.users)

        self.tab_table_users.setColumnCount(5)
        self.tab_table_users.setRowCount(len(self.parent.users))

        self.tab_table_users.setHorizontalHeaderLabels([local.x, local.y,
                                         local.h, local.height, local.bs])
        for i in range(len(self.parent.users)):
            self.tab_table_users.setItem(i, 0, QtWidgets.QTableWidgetItem(
                str(round(self.parent.users[i][0], 2))))
            self.tab_table_users.setItem(i, 1, QtWidgets.QTableWidgetItem(
                str(round(self.parent.users[i][1], 2))))
            self.tab_table_users.setItem(i, 2, QtWidgets.QTableWidgetItem(
                str(round(self.parent.users[i][2], 2))))
            self.tab_table_users.setItem(i, 3, QtWidgets.QTableWidgetItem(
                str(round(self.parent.users[i][3], 2))))
            self.tab_table_users.setItem(i, 4, QtWidgets.QTableWidgetItem(
                str(0)))

    def report_analyse_points(self):
        self.tab_table_analyse_points = QtWidgets.QTableWidget(self.window)
        self.tabs.addTab(self.tab_table_analyse_points, local.anp)
        self.tab_table_analyse_points.setColumnCount(7)
        self.tab_table_analyse_points.setRowCount(len(self.parent.analyse_points))

        self.tab_table_analyse_points.setHorizontalHeaderLabels([local.x, local.y,
                    local.h, local.power, local.rate, local.snr, local.inr])
        for i, coord in enumerate(self.parent.analyse_points):
            self.tab_table_analyse_points.setItem(i, 0, QtWidgets.QTableWidgetItem(
                str(round(coord[0], 2))))
            self.tab_table_analyse_points.setItem(i, 1, QtWidgets.QTableWidgetItem(
                str(round(coord[1], 2))))
            self.tab_table_analyse_points.setItem(i, 2, QtWidgets.QTableWidgetItem(
                str(round(coord[2], 2))))


    def report_power(self):
        for i, value in enumerate(self.parent.power_values):
            self.tab_table_analyse_points.setItem(i, 3, QtWidgets.QTableWidgetItem(
                        str(round(value[2], 2))))

    def report_rate(self):
        for i, value in enumerate(self.parent.rate_values):
            self.tab_table_analyse_points.setItem(i, 4, QtWidgets.QTableWidgetItem(
                    str(round(value[2], 2))))

    def report_snr(self):
        for i, value in enumerate(self.parent.snr_values):
            self.tab_table_analyse_points.setItem(i, 5, QtWidgets.QTableWidgetItem(
                    str(round(value[2], 2))))

    def report_inr(self):
        for i, value in enumerate(self.parent.inr_values):
            self.tab_table_analyse_points.setItem(i, 6, QtWidgets.QTableWidgetItem(
                    str(round(value[2], 2))))



class Legend(QtWidgets.QWidget):
    def __init__(self, parent):
        super(Legend, self).__init__(parent)
        print("created")
        self.parent = parent
        #self.setGeometry(0, 0, 260, 30)
        #self.showMinimized()
        self.min = -100
        self.max = -40
        self.init_size()

    def init_size(self, step = 30):
        #self.start = 40
        #self.step = 20
        #self.s = 25
        #self.start = start
        self.s = step
        #self.stop = self.start + 8*self.s + 10
        self.setGeometry(0, 0, 25*self.s, self.s)
        self.show()

        #self.mPixmap = QPixmap()

    def paintEvent(self, event):
        #print("paint")
        qp = QtGui.QPainter(self)
        #i = 0
        for i in range(8):
            self.paint_rect(qp, i)

    def paint_rect(self, qp, i):
        pen = QtGui.QPen(QtGui.QColor(*self.parent.colors[i]))
        brush = QtGui.QBrush(QtGui.QColor(*self.parent.colors[i]))
        qp.setPen(pen)
        qp.setBrush(brush)
        qp.drawRect(i*3*self.s, 0 , 3*self.s, self.s)

        pen = QtGui.QPen(QtGui.QColor("black"))
        qp.setPen(pen)
        qp.drawText(i*3*self.s + 4, 2*self.s/3,
                        str(round(self.min + i*self.step_value, 1))+
                        " ... "+
                        str(round(self.min + (i+1)*self.step_value, 1)))

    def set_par(self, min, max, step):
        self.min = min
        self.max = max
        self.step_value = step
        self.update()
        return


class Icon_ap(QtWidgets.QGraphicsPixmapItem):
    def __init__(self, parent, coord):
        super(Icon_ap, self).__init__()
        #self.setFlag(QtWidgets.QGraphicsPixmapItem.ItemIsSelectable)
        #self.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable, True)
        #self.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable, True)
        self.parent = parent
        self.setAcceptHoverEvents(True)
        self.setZValue(20)

        self.icon_ap = QtGui.QPixmap(values.icon_ap)
        #self.icon_ap.setDevicePixelRatio(50.0)
        sh1 = 1.5*self.parent.vesy*self.parent.step
        sh2 = 1.5*self.parent.vesx*self.parent.step
        self.icon_ap = self.icon_ap.scaled(sh1, sh2,
                                QtCore.Qt.KeepAspectRatio,
                                QtCore.Qt.SmoothTransformation)
        #self.setScale(0.02)
        self.setPixmap(self.icon_ap)

        self.text = (local.ap + str(len(self.parent.access_points)) + '\n' +
                     "y = " + str(round(coord[0], 2)) + '\n'
                     "x = " + str(round(coord[1], 2)))
        self.setToolTip(self.text)
        self.update()

    def hoverEnterEvent(self, event):
        super(Icon_ap, self).hoverEnterEvent(event)

    def hoverLeaveEvent(self, event):
        super(Icon_ap, self).hoverLeaveEvent(event)

    def change_text(self, index, coord):
        self.text = (local.ap + str(index) + '\n' +
                     "y = " + str(round(coord[0], 2)) + '\n'
                     "x = " + str(round(coord[1], 2)))
        self.setToolTip(self.text)



class Icon_user(QtWidgets.QGraphicsPixmapItem):
    def __init__(self, parent, coord):
        super(Icon_user, self).__init__()
        self.parent = parent
        self.setAcceptHoverEvents(True)
        self.setZValue(20)

        self.icon_user = QtGui.QPixmap(values.icon_user)
        sh1 = 1.4*self.parent.vesy*self.parent.step
        sh2 = 1.4*self.parent.vesx*self.parent.step
        self.icon_user = self.icon_user.scaled(sh1, sh2,
                                QtCore.Qt.KeepAspectRatio,
                                QtCore.Qt.SmoothTransformation)
        self.setPixmap(self.icon_user)

        self.text = (local.user + str(len(self.parent.users)) + '\n' +
                     "y = " + str(round(coord[0], 2)) + '\n'
                     "x = " + str(round(coord[1], 2)))
        self.setToolTip(self.text)
        self.update()

    def hoverEnterEvent(self, event):
        super(Icon_user, self).hoverEnterEvent(event)

    def hoverLeaveEvent(self, event):
        super(Icon_user, self).hoverLeaveEvent(event)

    def change_text(self, index, coord):
        self.text = (local.user + str(index) + '\n' +
                     "y = " + str(round(coord[0], 2)) + '\n'
                     "x = " + str(round(coord[1], 2)))
        self.setToolTip(self.text)


class Automation():
    def __init__(self, parent):
        self.parent = parent
        self.is_set_parameters = False
        print("Automation is created")

    def close_all_windows(self):
        try:
            self.starting_window.close()
            self.obstacles_window.close()
            self.set_ap_window.close()
            self.set_users_window.close()
        except:
            pass

    def show_starting_window(self):
        """ Shows the choice: import dxf,
        import image or open map """
        self.is_automation = True
        self.starting_window = SecondWindow()
        self.label_ss = QtWidgets.QLabel(local.ss_start)
        self.starting_window.grid.addWidget(self.label_ss,
                            0, 0, 1, 3)
        self.btn_dxf = QtWidgets.QPushButton(local.dxf)
        self.btn_dxf.clicked.connect(self.import_dxf)
        self.starting_window.grid.addWidget(self.btn_dxf, 1, 0)

        self.btn_img = QtWidgets.QPushButton(local.img)
        self.btn_img.clicked.connect(self.parent.openFileNameDialog_import_image)
        self.starting_window.grid.addWidget(self.btn_img, 1, 1)

        self.btn_map = QtWidgets.QPushButton(local.map)
        self.btn_map.clicked.connect(self.open_map)
        self.starting_window.grid.addWidget(self.btn_map, 1, 2)

    def import_dxf(self):
        self.starting_window.close()
        self.parent.openFileNameDialog_import_dxf()
        self.parent.automation_on()

    def import_image(self):
        self.starting_window.close()
        self.parent.openFileNameDialog_import_image()
        self.parent.automation_on()

    def open_map(self):
        self.starting_window.close()
        self.parent.openFileNameDialog()
        self.parent.automation_on()

    def plot_coverage(self):
        """ Starts plotting the coverage area """
        self.is_automation = True
        self.coverage_window = SecondWindow()
        self.coverage_window.grid.addWidget(QtWidgets.QLabel
                            (local.ss_coverage),
                            0, 0, 1, 2)
        self.btn_coverage_ok = QtWidgets.QPushButton(local.ok)
        self.btn_coverage_ok.clicked.connect(self.coverage_ok)
        self.coverage_window.grid.addWidget(self.btn_coverage_ok, 1, 1)

    def coverage_ok(self):
        self.parent.add_coverage_area()
        self.coverage_window.close()
        #self.parent.automation_on()

    def plot_obstacles(self):
        """ Plot the obstacles or next """

        self.is_automation = True
        self.obstacles_window = SecondWindow()
        self.obstacles_window.grid.addWidget(QtWidgets.QLabel
                        (local.ss_obstacles), 0, 0, 1, 2)
        self.btn_wall = QtWidgets.QPushButton(local.wall)
        self.btn_wall.clicked.connect(self.add_wall)
        self.obstacles_window.grid.addWidget(self.btn_wall, 1, 0)

        self.btn_window = QtWidgets.QPushButton(local.window)
        self.btn_window.clicked.connect(self.add_window)
        self.obstacles_window.grid.addWidget(self.btn_window, 2, 0)

        self.btn_door = QtWidgets.QPushButton(local.door)
        self.btn_door.clicked.connect(self.add_door)
        self.obstacles_window.grid.addWidget(self.btn_door, 3, 0)

        self.btn_next = QtWidgets.QPushButton(local.next)
        self.btn_next.clicked.connect(self.set_parameters)
        self.obstacles_window.grid.addWidget(self.btn_next, 3, 1)

    def add_wall(self):
        self.parent.add_wall()
        self.obstacles_window.close()

    def add_window(self):
        self.parent.add_window()
        self.obstacles_window.close()

    def add_door(self):
        self.parent.add_door()
        self.obstacles_window.close()

    def set_parameters(self):
        self.is_automation = True
        self.parent.is_obstacles_done = True
        try:
            self.obstacles_window.close()
        except:
            pass
        self.parent.planning_parameters()
        #self.parent.automation_on()


    def set_parameters2(self): # old
        """ Set parameters of analyse points and
            paint them """
        try:
            self.obstacles_window.close()
        except:
            pass
        self.parent.is_obstacles_done = True
        self.is_set_parameters = True
        self.parameters_window = SecondWindow()
        self.parameters_window.grid.addWidget(QtWidgets.QLabel
                        (local.ss_anp),
                        0, 0, 1, 3)
        self.btn_ok = QtWidgets.QPushButton(local.ok)
        self.btn_ok.clicked.connect(self.fun_parameters_ok)
        self.parameters_window.grid.addWidget(self.btn_ok, 1, 2)

    def fun_parameters_ok(self): #old
        self.parameters_window.close()
        self.parent.planning_parameters()
        #self.parent.is_analyse_points = True

    def plot_analyse_points(self):
        #self.parent.is_analyse_points = True
        self.parent.analyse_points_update()

    def set_ap(self):
        self.is_automation = True
        self.set_ap_window = SecondWindow()
        self.set_ap_window.grid.addWidget(QtWidgets.QLabel
                        (local.ss_ap),
                        0, 0, 1, 3)
        self.btn_ap = QtWidgets.QPushButton(local.ap_manual)
        self.btn_ap.clicked.connect(self.add_AP)
        self.set_ap_window.grid.addWidget(self.btn_ap, 1, 0)

        self.btn_load_net = QtWidgets.QPushButton(local.load_net)
        self.btn_load_net.clicked.connect(self.load_net)
        self.set_ap_window.grid.addWidget(self.btn_load_net, 1, 2)

        #self.btn_ap_next = QtWidgets.QPushButton(local.next)
        #self.btn_ap_next.clicked.connect(self.btn_ap_next_fun)
        #self.set_ap_window.grid.addWidget(self.btn_ap_next, 1, 2)

    def add_AP(self):
        self.set_ap_window.close()
        self.parent.add_AP()

    def load_net(self):
        self.set_ap_window.close()
        self.parent.openNet()

    def btn_ap_next_fun(self): #old
        print("ap next")
        self.set_ap_window.close()
        self.parent.clear_actions()
        self.parent.is_ap_done = True
        self.set_users()

    def set_users(self):
        print("set users")
        self.is_automation = True
        self.set_users_window = SecondWindow()
        self.set_users_window.grid.addWidget(QtWidgets.QLabel
                            (local.ss_users),
                            0, 0, 1, 3)
        self.btn_user_auto = QtWidgets.QPushButton(local.us_auto)
        self.btn_user_auto.clicked.connect(self.add_new_user_auto)
        self.set_users_window.grid.addWidget(self.btn_user_auto, 1, 0)

        self.btn_user_uniform = QtWidgets.QPushButton(local.us_uniform)
        self.btn_user_uniform.clicked.connect(self.add_new_user_uniform)
        self.set_users_window.grid.addWidget(self.btn_user_uniform, 2, 0)

        self.btn_user_manually = QtWidgets.QPushButton(local.us_manual)
        self.btn_user_manually.clicked.connect(self.add_new_user_manually)
        self.set_users_window.grid.addWidget(self.btn_user_manually, 3, 0)

        self.btn_users_next = QtWidgets.QPushButton(local.next)
        self.btn_users_next.clicked.connect(self.paint_map)
        self.set_users_window.grid.addWidget(self.btn_users_next, 3, 2)


    def set_ap_users(self): #delete
        """ Set the ap or users by 3 methods """

        self.set_ap_users_window = SecondWindow()
        self.set_ap_users_window.grid.addWidget(QtWidgets.QLabel
                            ("Вы можете добавить точки доступа и пользователей"),
                            0, 0, 1, 3)
        self.btn_ap = QtWidgets.QPushButton("ТД вручную")
        self.btn_ap.clicked.connect(self.add_AP)
        self.set_ap_users_window.grid.addWidget(self.btn_ap, 3, 0)

        self.btn_user_auto = QtWidgets.QPushButton("Пользователей автоматически")
        self.btn_user_auto.clicked.connect(self.add_new_user_auto)
        self.set_ap_users_window.grid.addWidget(self.btn_user_auto, 1, 1)

        self.btn_user_uniform = QtWidgets.QPushButton("Пользователей равномерно")
        self.btn_user_uniform.clicked.connect(self.add_new_user_uniform)
        self.set_ap_users_window.grid.addWidget(self.btn_user_uniform, 2, 1)

        self.btn_user_manually = QtWidgets.QPushButton("Пользователей вручную")
        self.btn_user_manually.clicked.connect(self.add_new_user_manually)
        self.set_ap_users_window.grid.addWidget(self.btn_user_manually, 3, 1)

        self.btn_ap_users_next = QtWidgets.QPushButton("Дальше")
        self.btn_ap_users_next.clicked.connect(self.paint_map)
        self.set_ap_users_window.grid.addWidget(self.btn_ap_users_next, 3, 2)

    def add_new_user_auto(self):
        self.parent.is_users_done = True
        self.set_users_window.close()
        self.parent.add_new_user_auto()

    def add_new_user_uniform(self):
        self.parent.is_users_done = True
        self.set_users_window.close()
        self.parent.add_new_user_uniform()

    def add_new_user_manually(self):
        self.set_users_window.close()
        self.parent.add_new_user_manually()


    def paint_map(self):
        print("users next")
        try:
            self.set_users_window.close()
        except:
            pass
        self.parent.is_users_done = True
        self.parent.get_map()


if __name__ == '__main__':
    print('file planner:', __name__)
    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    window.show()
    window.center.graphicView.task1('./maps/RTS1.map')
    #window.center.graphicView.task1('bonn13.map')
    sys.exit(app.exec_())
