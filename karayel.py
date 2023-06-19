import sys
from PyQt5.QtCore import *
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtWidgets import *
from PyQt5 import QtCore,  uic, QtWidgets
from karayel_ui import Ui_KarayelWindow
from PyQt5.QtGui import *
from dronekit import Command, connect, VehicleMode, LocationGlobalRelative
import time
from pymavlink import mavutil
import cv2
import smtplib
from email.mime.text import MIMEText
import numpy as np
import folium # pip install folium
from folium.plugins import Draw ,MousePosition
import folium, io, sys, json
from folium import plugins
import mysql.connector
from encodings import search_function
from PyQt5 import QtWebEngineWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import pymysql as sql
import mysql.connector
import matplotlib.pyplot as plt
import sqlite3
from datetime import datetime
from encodings import search_function
import pymysql as sql
import folium # pip install folium
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout
from PyQt5 import QtWebEngineWidgets
from folium.plugins import Draw ,MousePosition
import folium, io, sys, json
from folium import plugins
import os
import math


conn = sql.connect(
                host = "localhost",
                user="root",
                password="root",
                database="karayel" )
im = conn.cursor()


connection_string="COM3"
baud_rate=9600
# Pixhawk ile bağlantıyı kur
vehicle = connect(connection_string, baud=9600, wait_ready=True)
home=vehicle.location.global_frame

class AnalogGauge_alt(QWidget):
    valueChanged = pyqtSignal(int)
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(100, 100)
        self.altTimer = QTimer()
        self.altTimer.start(10) # Saniyede bir güncelle
        self.altTimer.timeout.connect(self.update_alt)
        #self.altTimer.start(1000) # Saniyede bir güncelle
    
    def update_alt(self):
        while True:
            gaugeYukseklik = vehicle.location.global_relative_frame.alt
            self.value= gaugeYukseklik
            break

        self.use_timer_event = False
        self.setNeedleColor(0, 0, 0, 255)
        self.NeedleColorReleased = self.NeedleColor
        self.setNeedleColorOnDrag(255, 0, 00, 255)
        self.setScaleValueColor(0, 0, 0, 255)
        self.setDisplayValueColor(0, 0, 0, 255)
        self.set_CenterPointColor(0, 0, 0, 255)
        self.value_needle_count = 1
        self.value_needle = QObject
        self.minValue = 0
        self.maxValue = 10
        
        self.value_offset = 0

        self.valueNeedleSnapzone = 0.05
        self.last_value = 0
        self.gauge_color_outer_radius_factor = 1
        self.gauge_color_inner_radius_factor = 0.9

        self.center_horizontal_value = 0
        self.center_vertical_value = 0

        self.scale_angle_start_value = 135
        self.scale_angle_size = 270

        self.angle_offset = 0

        self.setScalaCount(10)
        self.scala_subdiv_count = 5

        self.pen = QPen(QColor(0, 0, 0))

        QFontDatabase.addApplicationFont(os.path.join(os.path.dirname(
            __file__), 'fonts/Orbitron/Orbitron-VariableFont_wght.ttf'))

        self.scale_polygon_colors = []

        self.bigScaleMarker = Qt.blue

        self.fineScaleColor = Qt.red

        self.setEnableScaleText(True)
        self.scale_fontname = "Orbitron"
        self.initial_scale_fontsize = 14
        self.scale_fontsize = self.initial_scale_fontsize
        self.enable_value_text = True
        self.value_fontname = "Orbitron"
        self.initial_value_fontsize = 40
        self.value_fontsize = self.initial_value_fontsize
        self.text_radius_factor = 0.5
        self.setEnableBarGraph(True)
        self.setEnableScalePolygon(True)
        self.enable_CenterPoint = True
        self.enable_fine_scaled_marker = True
        self.enable_big_scaled_marker = True
        self.needle_scale_factor = 0.8
        self.enable_Needle_Polygon = True

        self.setMouseTracking(False)
        self.units = "m/s"

        # QTimer sorgt für neu Darstellung alle X ms
        # evtl performance hier verbessern mit self.update() und self.use_timer_event = False
        # todo: self.update als default ohne ueberpruefung, ob self.use_timer_event gesetzt ist oder nicht
        # Timer startet alle 10ms das event paintEvent
        if self.use_timer_event:
            timer = QTimer(self)
            timer.timeout.connect(self.update)
            timer.start(10)
        else:
            self.update()

        self.setGaugeTheme(0)

        self.rescale_method()

    def setScaleFontFamily(self, font):
        self.scale_fontname = str(font)

    def setValueFontFamily(self, font):
        self.value_fontname = str(font)

    def setBigScaleColor(self, color):
        self.bigScaleMarker = QColor(color)

    def setFineScaleColor(self, color):
        self.fineScaleColor = QColor(color)

    def setGaugeTheme(self, Theme=1):
        if Theme == 0 or Theme == None:
            self.set_scale_polygon_colors([[.00, Qt.red],
                                           [.1, Qt.yellow],
                                           [.15, Qt.green],
                                           [1, Qt.transparent]])

            self.needle_center_bg = [
                                    [0, QColor(35, 40, 3, 255)],
                                    [0.16, QColor(30, 36, 45, 255)],
                                    [0.225, QColor(36, 42, 54, 255)],
                                    [0.423963, QColor(19, 23, 29, 255)],
                                    [0.580645, QColor(45, 53, 68, 255)],
                                    [0.792627, QColor(59, 70, 88, 255)],
                                    [0.935, QColor(30, 35, 45, 255)],
                                    [1, QColor(35, 40, 3, 255)]
            ]

            self.outer_circle_bg = [
                [0.0645161, QColor(30, 35, 45, 255)],
                [0.37788, QColor(57, 67, 86, 255)],
                [1, QColor(30, 36, 45, 255)]
            ]

        if Theme == 1:
            self.set_scale_polygon_colors([[.75, Qt.red],
                                           [.5, Qt.yellow],
                                           [.25, Qt.green]])

            self.needle_center_bg = [
                                    [0, QColor(35, 40, 3, 255)],
                                    [0.16, QColor(30, 36, 45, 255)],
                                    [0.225, QColor(36, 42, 54, 255)],
                                    [0.423963, QColor(19, 23, 29, 255)],
                                    [0.580645, QColor(45, 53, 68, 255)],
                                    [0.792627, QColor(59, 70, 88, 255)],
                                    [0.935, QColor(30, 35, 45, 255)],
                                    [1, QColor(35, 40, 3, 255)]
            ]

            self.outer_circle_bg = [
                [0.0645161, QColor(30, 35, 45, 255)],
                [0.37788, QColor(57, 67, 86, 255)],
                [1, QColor(30, 36, 45, 255)]
            ]

        if Theme == 2:
            self.set_scale_polygon_colors([[.25, Qt.red],
                                           [.5, Qt.yellow],
                                           [.75, Qt.green]])

            self.needle_center_bg = [
                                    [0, QColor(35, 40, 3, 255)],
                                    [0.16, QColor(30, 36, 45, 255)],
                                    [0.225, QColor(36, 42, 54, 255)],
                                    [0.423963, QColor(19, 23, 29, 255)],
                                    [0.580645, QColor(45, 53, 68, 255)],
                                    [0.792627, QColor(59, 70, 88, 255)],
                                    [0.935, QColor(30, 35, 45, 255)],
                                    [1, QColor(35, 40, 3, 255)]
            ]

            self.outer_circle_bg = [
                [0.0645161, QColor(30, 35, 45, 255)],
                [0.37788, QColor(57, 67, 86, 255)],
                [1, QColor(30, 36, 45, 255)]
            ]

        elif Theme == 3:
            self.set_scale_polygon_colors([[.00, Qt.white]])

            self.needle_center_bg = [
                                    [0, Qt.white],
            ]

            self.outer_circle_bg = [
                [0, Qt.white],
            ]

            self.bigScaleMarker = Qt.black
            self.fineScaleColor = Qt.black

        elif Theme == 4:
            self.set_scale_polygon_colors([[1, Qt.black]])

            self.needle_center_bg = [
                                    [0, Qt.black],
            ]

            self.outer_circle_bg = [
                [0, Qt.black],
            ]

            self.bigScaleMarker = Qt.white
            self.fineScaleColor = Qt.white

        elif Theme == 5:
            self.set_scale_polygon_colors([[1, QColor("#029CDE")]])

            self.needle_center_bg = [
                                    [0, QColor("#029CDE")],
            ]

            self.outer_circle_bg = [
                [0, QColor("#029CDE")],
            ]

        elif Theme == 6:
            self.set_scale_polygon_colors([[.75, QColor("#01ADEF")],
                                           [.5, QColor("#0086BF")],
                                           [.25, QColor("#005275")]])

            self.needle_center_bg = [
                                    [0, QColor(0, 46, 61, 255)],
                                    [0.322581, QColor(1, 173, 239, 255)],
                                    [0.571429, QColor(0, 73, 99, 255)],
                                    [1, QColor(0, 46, 61, 255)]
            ]

            self.outer_circle_bg = [
                [0.0645161, QColor(0, 85, 116, 255)],
                [0.37788, QColor(1, 173, 239, 255)],
                [1, QColor(0, 69, 94, 255)]
            ]

            self.bigScaleMarker = Qt.black
            self.fineScaleColor = Qt.black

        elif Theme == 7:
            self.set_scale_polygon_colors([[.25, QColor("#01ADEF")],
                                           [.5, QColor("#0086BF")],
                                           [.75, QColor("#005275")]])

            self.needle_center_bg = [
                                    [0, QColor(0, 46, 61, 255)],
                                    [0.322581, QColor(1, 173, 239, 255)],
                                    [0.571429, QColor(0, 73, 99, 255)],
                                    [1, QColor(0, 46, 61, 255)]
            ]

            self.outer_circle_bg = [
                [0.0645161, QColor(0, 85, 116, 255)],
                [0.37788, QColor(1, 173, 239, 255)],
                [1, QColor(0, 69, 94, 255)]
            ]

            self.bigScaleMarker = Qt.black
            self.fineScaleColor = Qt.black

        elif Theme == 8:
            self.setCustomGaugeTheme(
                color1="#ffaa00",
                color2="#7d5300",
                color3="#3e2900"
            )

            self.bigScaleMarker = Qt.black
            self.fineScaleColor = Qt.black

        elif Theme == 9:
            self.setCustomGaugeTheme(
                color1="#3e2900",
                color2="#7d5300",
                color3="#ffaa00"
            )

            self.bigScaleMarker = Qt.white
            self.fineScaleColor = Qt.white

        elif Theme == 10:
            self.setCustomGaugeTheme(
                color1="#ff007f",
                color2="#aa0055",
                color3="#830042"
            )

            self.bigScaleMarker = Qt.black
            self.fineScaleColor = Qt.black

        elif Theme == 11:
            self.setCustomGaugeTheme(
                color1="#830042",
                color2="#aa0055",
                color3="#ff007f"
            )

            self.bigScaleMarker = Qt.white
            self.fineScaleColor = Qt.white

        elif Theme == 12:
            self.setCustomGaugeTheme(
                color1="#ffe75d",
                color2="#896c1a",
                color3="#232803"
            )

            self.bigScaleMarker = Qt.black
            self.fineScaleColor = Qt.black

        elif Theme == 13:
            self.setCustomGaugeTheme(
                color1="#ffe75d",
                color2="#896c1a",
                color3="#232803"
            )

            self.bigScaleMarker = Qt.black
            self.fineScaleColor = Qt.black

        elif Theme == 14:
            self.setCustomGaugeTheme(
                color1="#232803",
                color2="#821600",
                color3="#ffe75d"
            )

            self.bigScaleMarker = Qt.white
            self.fineScaleColor = Qt.white

        elif Theme == 15:
            self.setCustomGaugeTheme(
                color1="#00FF11",
                color2="#00990A",
                color3="#002603"
            )

            self.bigScaleMarker = Qt.black
            self.fineScaleColor = Qt.black

        elif Theme == 16:
            self.setCustomGaugeTheme(
                color1="#002603",
                color2="#00990A",
                color3="#00FF11"
            )

            self.bigScaleMarker = Qt.white
            self.fineScaleColor = Qt.white

        elif Theme == 17:
            self.setCustomGaugeTheme(
                color1="#00FFCC",
                color2="#00876C",
                color3="#00211B"
            )

            self.bigScaleMarker = Qt.black
            self.fineScaleColor = Qt.black

        elif Theme == 18:
            self.setCustomGaugeTheme(
                color1="#00211B",
                color2="#00876C",
                color3="#00FFCC"
            )

            self.bigScaleMarker = Qt.white
            self.fineScaleColor = Qt.white

        elif Theme == 19:
            self.setCustomGaugeTheme(
                color1="#001EFF",
                color2="#001299",
                color3="#000426"
            )

            self.bigScaleMarker = Qt.black
            self.fineScaleColor = Qt.black

        elif Theme == 20:
            self.setCustomGaugeTheme(
                color1="#000426",
                color2="#001299",
                color3="#001EFF"
            )

            self.bigScaleMarker = Qt.white
            self.fineScaleColor = Qt.white

        elif Theme == 21:
            self.setCustomGaugeTheme(
                color1="#F200FF",
                color2="#85008C",
                color3="#240026"
            )

            self.bigScaleMarker = Qt.black
            self.fineScaleColor = Qt.black

        elif Theme == 22:
            self.setCustomGaugeTheme(
                color1="#240026",
                color2="#85008C",
                color3="#F200FF"
            )

            self.bigScaleMarker = Qt.white
            self.fineScaleColor = Qt.white

        elif Theme == 23:
            self.setCustomGaugeTheme(
                color1="#FF0022",
                color2="#080001",
                color3="#009991"
            )

            self.bigScaleMarker = Qt.white
            self.fineScaleColor = Qt.white

        elif Theme == 24:
            self.setCustomGaugeTheme(
                color1="#009991",
                color2="#080001",
                color3="#FF0022"
            )

            self.bigScaleMarker = Qt.white
            self.fineScaleColor = Qt.white

    def setCustomGaugeTheme(self, **colors):
        if "color1" in colors and len(str(colors['color1'])) > 0:
            if "color2" in colors and len(str(colors['color2'])) > 0:
                if "color3" in colors and len(str(colors['color3'])) > 0:

                    self.set_scale_polygon_colors([[.25, QColor(str(colors['color1']))],
                                                   [.5, QColor(
                                                       str(colors['color2']))],
                                                   [.75, QColor(str(colors['color3']))]])

                    self.needle_center_bg = [
                                            [0, QColor(str(colors['color3']))],
                                            [0.322581, QColor(
                                                str(colors['color1']))],
                                            [0.571429, QColor(
                                                str(colors['color2']))],
                                            [1, QColor(str(colors['color3']))]
                    ]

                    self.outer_circle_bg = [
                        [0.0645161, QColor(str(colors['color3']))],
                        [0.36, QColor(
                            str(colors['color1']))],
                        [1, QColor(str(colors['color2']))]
                    ]

                else:

                    self.set_scale_polygon_colors([[.5, QColor(str(colors['color1']))],
                                                   [1, QColor(str(colors['color2']))]])

                    self.needle_center_bg = [
                                            [0, QColor(str(colors['color2']))],
                                            [1, QColor(str(colors['color1']))]
                    ]

                    self.outer_circle_bg = [
                        [0, QColor(str(colors['color2']))],
                        [1, QColor(str(colors['color2']))]
                    ]

            else:

                self.set_scale_polygon_colors(
                    [[1, QColor(str(colors['color1']))]])

                self.needle_center_bg = [
                                        [1, QColor(str(colors['color1']))]
                ]

                self.outer_circle_bg = [
                    [1, QColor(str(colors['color1']))]
                ]

        else:

            self.setGaugeTheme(0)
            print("color1 is not defined")

    def setScalePolygonColor(self, **colors):
        if "color1" in colors and len(str(colors['color1'])) > 0:
            if "color2" in colors and len(str(colors['color2'])) > 0:
                if "color3" in colors and len(str(colors['color3'])) > 0:

                    self.set_scale_polygon_colors([[.25, QColor(str(colors['color1']))],
                                                   [.5, QColor(
                                                       str(colors['color2']))],
                                                   [.75, QColor(str(colors['color3']))]])

                else:

                    self.set_scale_polygon_colors([[.5, QColor(str(colors['color1']))],
                                                   [1, QColor(str(colors['color2']))]])

            else:

                self.set_scale_polygon_colors(
                    [[1, QColor(str(colors['color1']))]])

        else:
            print("color1 is not defined")

    def setNeedleCenterColor(self, **colors):
        if "color1" in colors and len(str(colors['color1'])) > 0:
            if "color2" in colors and len(str(colors['color2'])) > 0:
                if "color3" in colors and len(str(colors['color3'])) > 0:

                    self.needle_center_bg = [
                                            [0, QColor(str(colors['color3']))],
                                            [0.322581, QColor(
                                                str(colors['color1']))],
                                            [0.571429, QColor(
                                                str(colors['color2']))],
                                            [1, QColor(str(colors['color3']))]
                    ]

                else:

                    self.needle_center_bg = [
                                            [0, QColor(str(colors['color2']))],
                                            [1, QColor(str(colors['color1']))]
                    ]

            else:

                self.needle_center_bg = [
                                        [1, QColor(str(colors['color1']))]
                ]
        else:
            print("color1 is not defined")

    def setOuterCircleColor(self, **colors):
        if "color1" in colors and len(str(colors['color1'])) > 0:
            if "color2" in colors and len(str(colors['color2'])) > 0:
                if "color3" in colors and len(str(colors['color3'])) > 0:

                    self.outer_circle_bg = [
                        [0.0645161, QColor(str(colors['color3']))],
                        [0.37788, QColor(
                            str(colors['color1']))],
                        [1, QColor(str(colors['color2']))]
                    ]

                else:

                    self.outer_circle_bg = [
                        [0, QColor(str(colors['color2']))],
                        [1, QColor(str(colors['color2']))]
                    ]

            else:

                self.outer_circle_bg = [
                    [1, QColor(str(colors['color1']))]
                ]

        else:
            print("color1 is not defined")

    def rescale_method(self):
        if self.width() <= self.height():
            self.widget_diameter = self.width()
        else:
            self.widget_diameter = self.height()
        self.change_value_needle_style([QPolygon([
            QPoint(4, 30),
            QPoint(-4, 30),
            QPoint(-2, int(- self.widget_diameter / 2 * self.needle_scale_factor)),
            QPoint(0, int(- self.widget_diameter /
                   2 * self.needle_scale_factor - 6)),
            QPoint(2, int(- self.widget_diameter / 2 * self.needle_scale_factor))
        ])])

        self.scale_fontsize = int(
            self.initial_scale_fontsize * self.widget_diameter / 400)
        self.value_fontsize = int(
            self.initial_value_fontsize * self.widget_diameter / 400)

    def change_value_needle_style(self, design):
        # prepared for multiple needle instrument
        self.value_needle = []
        for i in design:
            self.value_needle.append(i)
        if not self.use_timer_event:
            self.update()

    def updateValue(self, value, mouse_controlled=False):
        # if not mouse_controlled:
        #     self.value = value
        #
        # if mouse_controlled:
        #     self.valueChanged.emit(int(value))

        if value <= self.minValue:
            self.value = self.minValue
        elif value >= self.maxValue:
            self.value = self.maxValue
        else:
            self.value = value
        # self.paintEvent("")
        self.valueChanged.emit(int(value))
        # print(self.value)

        # ohne timer: aktiviere self.update()
        if not self.use_timer_event:
            self.update()

    def updateAngleOffset(self, offset):
        self.angle_offset = offset
        if not self.use_timer_event:
            self.update()

    def center_horizontal(self, value):
        self.center_horizontal_value = value
        # print("horizontal: " + str(self.center_horizontal_value))

    def center_vertical(self, value):
        self.center_vertical_value = value
        # print("vertical: " + str(self.center_vertical_value))

    def setNeedleColor(self, R=50, G=50, B=50, Transparency=255):
        # Red: R = 0 - 255
        # Green: G = 0 - 255
        # Blue: B = 0 - 255
        # Transparency = 0 - 255
        self.NeedleColor = QColor(R, G, B, Transparency)
        self.NeedleColorReleased = self.NeedleColor

        if not self.use_timer_event:
            self.update()

    def setNeedleColorOnDrag(self, R=50, G=50, B=50, Transparency=255):
        # Red: R = 0 - 255
        # Green: G = 0 - 255
        # Blue: B = 0 - 255
        # Transparency = 0 - 255
        self.NeedleColorDrag = QColor(R, G, B, Transparency)

        if not self.use_timer_event:
            self.update()

    def setScaleValueColor(self, R=50, G=50, B=50, Transparency=255):
        # Red: R = 0 - 255
        # Green: G = 0 - 255
        # Blue: B = 0 - 255
        # Transparency = 0 - 255
        self.ScaleValueColor = QColor(R, G, B, Transparency)

        if not self.use_timer_event:
            self.update()

    def setDisplayValueColor(self, R=50, G=50, B=50, Transparency=255):
        # Red: R = 0 - 255
        # Green: G = 0 - 255
        # Blue: B = 0 - 255
        # Transparency = 0 - 255
        self.DisplayValueColor = QColor(R, G, B, Transparency)

        if not self.use_timer_event:
            self.update()

    def set_CenterPointColor(self, R=50, G=50, B=50, Transparency=255):
        self.CenterPointColor = QColor(R, G, B, Transparency)

        if not self.use_timer_event:
            self.update()

    def setEnableNeedlePolygon(self, enable=True):
        self.enable_Needle_Polygon = enable

        if not self.use_timer_event:
            self.update()

    def setEnableScaleText(self, enable=True):
        self.enable_scale_text = enable

        if not self.use_timer_event:
            self.update()

    def setEnableBarGraph(self, enable=True):
        self.enableBarGraph = enable

        if not self.use_timer_event:
            self.update()

    def setEnableValueText(self, enable=True):
        self.enable_value_text = enable

        if not self.use_timer_event:
            self.update()

    def setEnableCenterPoint(self, enable=True):
        self.enable_CenterPoint = enable

        if not self.use_timer_event:
            self.update()

    def setEnableScalePolygon(self, enable=True):
        self.enable_filled_Polygon = enable

        if not self.use_timer_event:
            self.update()

    def setEnableBigScaleGrid(self, enable=True):
        self.enable_big_scaled_marker = enable

        if not self.use_timer_event:
            self.update()

    def setEnableFineScaleGrid(self, enable=True):
        self.enable_fine_scaled_marker = enable

        if not self.use_timer_event:
            self.update()

    def setScalaCount(self, count):
        if count < 1:
            count = 1
        self.scalaCount = count

        if not self.use_timer_event:
            self.update()

    def setMinValue(self, min):
        if self.value < min:
            self.value = min
        if min >= self.maxValue:
            self.minValue = self.maxValue - 1
        else:
            self.minValue = min

        if not self.use_timer_event:
            self.update()

    def setMaxValue(self, max):
        if self.value > max:
            self.value = max
        if max <= self.minValue:
            self.maxValue = self.minValue + 1
        else:
            self.maxValue = max

        if not self.use_timer_event:
            self.update()

    def setScaleStartAngle(self, value):
        # Value range in DEG: 0 - 360
        self.scale_angle_start_value = value
        # print("startFill: " + str(self.scale_angle_start_value))

        if not self.use_timer_event:
            self.update()

    def setTotalScaleAngleSize(self, value):
        self.scale_angle_size = value
        # print("stopFill: " + str(self.scale_angle_size))

        if not self.use_timer_event:
            self.update()

    def setGaugeColorOuterRadiusFactor(self, value):
        self.gauge_color_outer_radius_factor = float(value) / 1000
        # print(self.gauge_color_outer_radius_factor)

        if not self.use_timer_event:
            self.update()

    def setGaugeColorInnerRadiusFactor(self, value):
        self.gauge_color_inner_radius_factor = float(value) / 1000
        # print(self.gauge_color_inner_radius_factor)

        if not self.use_timer_event:
            self.update()

    def set_scale_polygon_colors(self, color_array):
        # print(type(color_array))
        if 'list' in str(type(color_array)):
            self.scale_polygon_colors = color_array
        elif color_array == None:
            self.scale_polygon_colors = [[.0, Qt.transparent]]
        else:
            self.scale_polygon_colors = [[.0, Qt.transparent]]

        if not self.use_timer_event:
            self.update()

    ################################################################################################
    # GET MAXIMUM VALUE
    ################################################################################################
    def get_value_max(self):
        return self.maxValue

    def create_polygon_pie(self, outer_radius, inner_raduis, start, lenght, bar_graph=True):
        polygon_pie = QPolygonF()
        # start = self.scale_angle_start_value
        # start = 0
        # lenght = self.scale_angle_size
        # lenght = 180
        # inner_raduis = self.width()/4
        # print(start)
        n = 360     # angle steps size for full circle
        # changing n value will causes drawing issues
        w = 360 / n   # angle per step
        # create outer circle line from "start"-angle to "start + lenght"-angle
        x = 0
        y = 0

        # todo enable/disable bar graf here
        if not self.enableBarGraph and bar_graph:
            # float_value = ((lenght / (self.maxValue - self.minValue)) * (self.value - self.minValue))
            lenght = int(
                round((lenght / (self.maxValue - self.minValue)) * (self.value - self.minValue)))
            # print("f: %s, l: %s" %(float_value, lenght))
            pass

        # mymax = 0

        # add the points of polygon
        for i in range(lenght + 1):
            t = w * i + start - self.angle_offset
            x = outer_radius * math.cos(math.radians(t))
            y = outer_radius * math.sin(math.radians(t))
            polygon_pie.append(QPointF(x, y))
        # create inner circle line from "start + lenght"-angle to "start"-angle
        # add the points of polygon
        for i in range(lenght + 1):
            # print("2 " + str(i))
            t = w * (lenght - i) + start - self.angle_offset
            x = inner_raduis * math.cos(math.radians(t))
            y = inner_raduis * math.sin(math.radians(t))
            polygon_pie.append(QPointF(x, y))

        # close outer line
        polygon_pie.append(QPointF(x, y))
        return polygon_pie

    def draw_filled_polygon(self, outline_pen_with=0):
        if not self.scale_polygon_colors == None:
            painter_filled_polygon = QPainter(self)
            painter_filled_polygon.setRenderHint(QPainter.Antialiasing)
            # Koordinatenursprung in die Mitte der Flaeche legen
            painter_filled_polygon.translate(
                self.width() / 2, self.height() / 2)

            painter_filled_polygon.setPen(Qt.NoPen)

            self.pen.setWidth(outline_pen_with)
            if outline_pen_with > 0:
                painter_filled_polygon.setPen(self.pen)

            colored_scale_polygon = self.create_polygon_pie(
                ((self.widget_diameter / 2) - (self.pen.width() / 2)) *
                self.gauge_color_outer_radius_factor,
                (((self.widget_diameter / 2) - (self.pen.width() / 2))
                 * self.gauge_color_inner_radius_factor),
                self.scale_angle_start_value, self.scale_angle_size)

            gauge_rect = QRect(QPoint(0, 0), QSize(
                int(self.widget_diameter / 2 - 1), int(self.widget_diameter - 1)))
            grad = QConicalGradient(QPointF(0, 0), - self.scale_angle_size - self.scale_angle_start_value +
                                    self.angle_offset - 1)

            # todo definition scale color as array here
            for eachcolor in self.scale_polygon_colors:
                grad.setColorAt(eachcolor[0], eachcolor[1])
            # grad.setColorAt(.00, Qt.red)
            # grad.setColorAt(.1, Qt.yellow)
            # grad.setColorAt(.15, Qt.green)
            # grad.setColorAt(1, Qt.transparent)
            # self.brush = QBrush(QColor(255, 0, 255, 255))
            # grad.setStyle(Qt.Dense6Pattern)
            # painter_filled_polygon.setBrush(self.brush)
            painter_filled_polygon.setBrush(grad)

            painter_filled_polygon.drawPolygon(colored_scale_polygon)
            # return painter_filled_polygon

    def draw_icon_image(self):
        pass

    def draw_big_scaled_marker(self):
        my_painter = QPainter(self)
        my_painter.setRenderHint(QPainter.Antialiasing)
        # Koordinatenursprung in die Mitte der Flaeche legen
        my_painter.translate(self.width() / 2, self.height() / 2)

        # my_painter.setPen(Qt.NoPen)
        self.pen = QPen(self.bigScaleMarker)
        self.pen.setWidth(2)
        # # if outline_pen_with > 0:
        my_painter.setPen(self.pen)

        my_painter.rotate(self.scale_angle_start_value - self.angle_offset)
        steps_size = (float(self.scale_angle_size) / float(self.scalaCount))
        scale_line_outer_start = self.widget_diameter // 2
        scale_line_lenght = int((self.widget_diameter / 2) -
                                (self.widget_diameter / 20))
        # print(stepszize)
        for i in range(self.scalaCount + 1):
            my_painter.drawLine(scale_line_lenght, 0,
                                scale_line_outer_start, 0)
            my_painter.rotate(steps_size)

    def create_scale_marker_values_text(self):
        painter = QPainter(self)
        # painter.setRenderHint(QPainter.HighQualityAntialiasing)
        painter.setRenderHint(QPainter.Antialiasing)

        # Koordinatenursprung in die Mitte der Flaeche legen
        painter.translate(self.width() / 2, self.height() / 2)
        # painter.save()
        font = QFont(self.scale_fontname, self.scale_fontsize, QFont.Bold)
        fm = QFontMetrics(font)

        pen_shadow = QPen()

        pen_shadow.setBrush(self.ScaleValueColor)
        painter.setPen(pen_shadow)

        text_radius_factor = 0.8
        text_radius = self.widget_diameter / 2 * text_radius_factor

        scale_per_div = int((self.maxValue - self.minValue) / self.scalaCount)

        angle_distance = (float(self.scale_angle_size) /
                          float(self.scalaCount))
        for i in range(self.scalaCount + 1):
            # text = str(int((self.maxValue - self.minValue) / self.scalaCount * i))
            text = str(int(self.minValue + scale_per_div * i))
            w = fm.width(text) + 1
            h = fm.height()
            painter.setFont(QFont(self.scale_fontname,
                            self.scale_fontsize, QFont.Bold))
            angle = angle_distance * i + \
                float(self.scale_angle_start_value - self.angle_offset)
            x = text_radius * math.cos(math.radians(angle))
            y = text_radius * math.sin(math.radians(angle))
            # print(w, h, x, y, text)

            painter.drawText(int(x - w / 2), int(y - h / 2), int(w),
                             int(h), Qt.AlignCenter, text)
        # painter.restore()

    def create_fine_scaled_marker(self):
        #  Description_dict = 0
        my_painter = QPainter(self)

        my_painter.setRenderHint(QPainter.Antialiasing)
        # Koordinatenursprung in die Mitte der Flaeche legen
        my_painter.translate(self.width() / 2, self.height() / 2)

        my_painter.setPen(self.fineScaleColor)
        my_painter.rotate(self.scale_angle_start_value - self.angle_offset)
        steps_size = (float(self.scale_angle_size) /
                      float(self.scalaCount * self.scala_subdiv_count))
        scale_line_outer_start = self.widget_diameter // 2
        scale_line_lenght = int(
            (self.widget_diameter / 2) - (self.widget_diameter / 40))
        for i in range((self.scalaCount * self.scala_subdiv_count) + 1):
            my_painter.drawLine(scale_line_lenght, 0,
                                scale_line_outer_start, 0)
            my_painter.rotate(steps_size)

    def create_values_text(self):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.HighQualityAntialiasing)
        # painter.setRenderHint(QPainter.Antialiasing)

        painter.translate(self.width() / 2, self.height() / 2)
        font = QFont(self.value_fontname, self.value_fontsize, QFont.Bold)
        fm = QFontMetrics(font)

        pen_shadow = QPen()

        pen_shadow.setBrush(self.DisplayValueColor)
        painter.setPen(pen_shadow)

        text_radius = self.widget_diameter / 2 * self.text_radius_factor
        text = str(int(self.value))
        w = fm.width(text) + 1
        h = fm.height()
        painter.setFont(QFont(self.value_fontname,
                        self.value_fontsize, QFont.Bold))
        angle_end = float(self.scale_angle_start_value +
                          self.scale_angle_size - 360)
        angle = (angle_end - self.scale_angle_start_value) / \
            2 + self.scale_angle_start_value

        x = text_radius * math.cos(math.radians(angle))
        y = text_radius * math.sin(math.radians(angle))
        # print(w, h, x, y, text)
        painter.drawText(int(x - w / 2), int(y - h / 2), int(w),
                         int(h), Qt.AlignCenter, text)

    def create_units_text(self):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.HighQualityAntialiasing)
        # painter.setRenderHint(QPainter.Antialiasing)

        painter.translate(self.width() / 2, self.height() / 2)
        font = QFont(self.value_fontname, int(
            self.value_fontsize / 2.5), QFont.Bold)
        fm = QFontMetrics(font)

        pen_shadow = QPen()

        pen_shadow.setBrush(self.DisplayValueColor)
        painter.setPen(pen_shadow)

        text_radius = self.widget_diameter / 2 * self.text_radius_factor

        text = str(self.units)
        w = fm.width(text) + 1
        h = fm.height()
        painter.setFont(QFont(self.value_fontname, int(
            self.value_fontsize / 2.5), QFont.Bold))

        angle_end = float(self.scale_angle_start_value +
                          self.scale_angle_size + 180)
        angle = (angle_end - self.scale_angle_start_value) / \
            2 + self.scale_angle_start_value

        x = text_radius * math.cos(math.radians(angle))
        y = text_radius * math.sin(math.radians(angle))
        # print(w, h, x, y, text)
        painter.drawText(int(x - w / 2), int(y - h / 2), int(w),
                         int(h), Qt.AlignCenter, text)


    def draw_big_needle_center_point(self, diameter=30):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.translate(self.width() / 2, self.height() / 2)
        painter.setPen(Qt.NoPen)
        colored_scale_polygon = self.create_polygon_pie(
            ((self.widget_diameter / 8) - (self.pen.width() / 2)),
            0,
            self.scale_angle_start_value, 360, False)

        grad = QConicalGradient(QPointF(0, 0), 0)

        # todo definition scale color as array here
        for eachcolor in self.needle_center_bg:
            grad.setColorAt(eachcolor[0], eachcolor[1])
        painter.setBrush(grad)

        painter.drawPolygon(colored_scale_polygon)
    def draw_outer_circle(self, diameter=30):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        painter.translate(self.width() / 2, self.height() / 2)
        painter.setPen(Qt.NoPen)
        colored_scale_polygon = self.create_polygon_pie(
            ((self.widget_diameter / 2) - (self.pen.width())),
            (self.widget_diameter / 6),
            self.scale_angle_start_value / 10, 360, False)

        radialGradient = QRadialGradient(QPointF(0, 0), self.width())

        for eachcolor in self.outer_circle_bg:
            radialGradient.setColorAt(eachcolor[0], eachcolor[1])

        painter.setBrush(radialGradient)

        painter.drawPolygon(colored_scale_polygon)

    ################################################################################################
    # NEEDLE POINTER
    ################################################################################################

    def draw_needle(self):
        painter = QPainter(self)
        # painter.setRenderHint(QtGui.QPainter.HighQualityAntialiasing)
        painter.setRenderHint(QPainter.Antialiasing)
        # Koordinatenursprung in die Mitte der Flaeche legen
        painter.translate(self.width() / 2, self.height() / 2)
        painter.setPen(Qt.NoPen)
        painter.setBrush(self.NeedleColor)
        painter.rotate(((self.value - self.value_offset - self.minValue) * self.scale_angle_size /
                        (self.maxValue - self.minValue)) + 90 + self.scale_angle_start_value)

        painter.drawConvexPolygon(self.value_needle[0])

    ###############################################################################################
    # EVENTS
    ###############################################################################################

    ################################################################################################
    # ON WINDOW RESIZE
    ################################################################################################
    def resizeEvent(self, event):
        # self.resized.emit()
        # return super(self.parent, self).resizeEvent(event)
        # print("resized")
        # print(self.width())
        self.rescale_method()
        # self.emit(QtCore.SIGNAL("resize()"))
        # print("resizeEvent")

    ################################################################################################
    # ON PAINT EVENT
    ################################################################################################
    def paintEvent(self, event):
        # Main Drawing Event:
        # Will be executed on every change
        # vgl http://doc.qt.io/qt-4.8/qt-demos-affine-xform-cpp.html
        # print("event", event)

        self.draw_outer_circle()
        self.draw_icon_image()
        # colored pie area
        if self.enable_filled_Polygon:
            self.draw_filled_polygon()

        # draw scale marker lines
        if self.enable_fine_scaled_marker:
            self.create_fine_scaled_marker()
        if self.enable_big_scaled_marker:
            self.draw_big_scaled_marker()

        # draw scale marker value text
        if self.enable_scale_text:
            self.create_scale_marker_values_text()

        # Display Value
        if self.enable_value_text:
            self.create_values_text()
            self.create_units_text()

        # draw needle 1
        if self.enable_Needle_Polygon:
            self.draw_needle()

        # Draw Center Point
        if self.enable_CenterPoint:
            self.draw_big_needle_center_point(
                diameter=(self.widget_diameter / 6))

    ###############################################################################################
    # MOUSE EVENTS
    ###############################################################################################


    def setMouseTracking(self, flag):
        def recursive_set(parent):
            for child in parent.findChildren(QObject):
                try:
                    child.setMouseTracking(flag)
                except:
                    pass
                recursive_set(child)

        QWidget.setMouseTracking(self, flag)
        recursive_set(self)

    def mouseReleaseEvent(self, QMouseEvent):
        self.NeedleColor = self.NeedleColorReleased

        if not self.use_timer_event:
            self.update()
        pass

    ########################################################################
    # MOUSE LEAVE EVENT
    ########################################################################
    def leaveEvent(self, event):
        self.NeedleColor = self.NeedleColorReleased
        self.update()

    def mouseMoveEvent(self, event):
        x, y = event.x() - (self.width() / 2), event.y() - (self.height() / 2)
        # print(event.x(), event.y(), self.width(), self.height())
        if not x == 0:
            angle = math.atan2(y, x) / math.pi * 180
            # winkellaenge der anzeige immer positiv 0 - 360deg
            # min wert + umskalierter wert
            value = (float(math.fmod(angle - self.scale_angle_start_value + 720, 360)) /
                     (float(self.scale_angle_size) / float(self.maxValue - self.minValue))) + self.minValue
            temp = value
            fmod = float(
                math.fmod(angle - self.scale_angle_start_value + 720, 360))
            state = 0
            if (self.value - (self.maxValue - self.minValue) * self.valueNeedleSnapzone) <= \
                    value <= \
                    (self.value + (self.maxValue - self.minValue) * self.valueNeedleSnapzone):
                self.NeedleColor = self.NeedleColorDrag
                # todo: evtl ueberpruefen
                #
                state = 9
                # if value >= self.maxValue and self.last_value < (self.maxValue - self.minValue) / 2:
                if value >= self.maxValue and self.last_value < (self.maxValue - self.minValue) / 2:
                    state = 1
                    value = self.maxValue
                    self.last_value = self.minValue
                    self.valueChanged.emit(int(value))

                elif value >= self.maxValue >= self.last_value:
                    state = 2
                    value = self.maxValue
                    self.last_value = self.maxValue
                    self.valueChanged.emit(int(value))

                else:
                    state = 3
                    self.last_value = value
                    self.valueChanged.emit(int(value))

                self.updateValue(value)


########################################################################################################################################################! ALTTİTUDE END

###############################################################################################################################################! GROUNDSPEED START
class AnalogGauge_ground(QWidget):
    valueChanged = pyqtSignal(int)
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(100, 100)
        
        self.altTimer = QTimer()
        self.altTimer.start(10) # Saniyede bir güncelle
        self.altTimer.timeout.connect(self.update_ground)
    
    def update_ground(self):
        while True:
            groundSpeed = vehicle.groundspeed
            self.value= groundSpeed
            break
        
        self.use_timer_event = False
        self.setNeedleColor(0, 0, 0, 255)
        self.NeedleColorReleased = self.NeedleColor
        self.setNeedleColorOnDrag(255, 0, 00, 255)
        self.setScaleValueColor(0, 0, 0, 255)
        self.setDisplayValueColor(0, 0, 0, 255)
        self.set_CenterPointColor(0, 0, 0, 255)
        self.value_needle_count = 1
        self.value_needle = QObject
        self.minValue = 0
        self.maxValue = 100
        self.value_offset = 0

        self.valueNeedleSnapzone = 0.05
        self.last_value = 0
        self.gauge_color_outer_radius_factor = 1
        self.gauge_color_inner_radius_factor = 0.9

        self.center_horizontal_value = 0
        self.center_vertical_value = 0

        self.scale_angle_start_value = 135
        self.scale_angle_size = 270

        self.angle_offset = 0

        self.setScalaCount(10)
        self.scala_subdiv_count = 5

        self.pen = QPen(QColor(0, 0, 0))

        QFontDatabase.addApplicationFont(os.path.join(os.path.dirname(
            __file__), 'fonts/Orbitron/Orbitron-VariableFont_wght.ttf'))

        self.scale_polygon_colors = []

        self.bigScaleMarker = Qt.black

        self.fineScaleColor = Qt.black

        self.setEnableScaleText(True)
        self.scale_fontname = "Orbitron"
        self.initial_scale_fontsize = 14
        self.scale_fontsize = self.initial_scale_fontsize
        self.enable_value_text = True
        self.value_fontname = "Orbitron"
        self.initial_value_fontsize = 40
        self.value_fontsize = self.initial_value_fontsize
        self.text_radius_factor = 0.5
        self.setEnableBarGraph(True)
        self.setEnableScalePolygon(True)
        self.enable_CenterPoint = True
        self.enable_fine_scaled_marker = True
        self.enable_big_scaled_marker = True
        self.needle_scale_factor = 0.8
        self.enable_Needle_Polygon = True

        self.setMouseTracking(False)
        self.units = "m/s"

        # QTimer sorgt für neu Darstellung alle X ms
        # evtl performance hier verbessern mit self.update() und self.use_timer_event = False
        # todo: self.update als default ohne ueberpruefung, ob self.use_timer_event gesetzt ist oder nicht
        # Timer startet alle 10ms das event paintEvent
        if self.use_timer_event:
            timer = QTimer(self)
            timer.timeout.connect(self.update)
            timer.start(10)
        else:
            self.update()

        self.setGaugeTheme(0)

        self.rescale_method()

    def setScaleFontFamily(self, font):
        self.scale_fontname = str(font)

    def setValueFontFamily(self, font):
        self.value_fontname = str(font)

    def setBigScaleColor(self, color):
        self.bigScaleMarker = QColor(color)

    def setFineScaleColor(self, color):
        self.fineScaleColor = QColor(color)

    def setGaugeTheme(self, Theme=1):
        if Theme == 0 or Theme == None:
            self.set_scale_polygon_colors([[.00, Qt.red],
                                           [.1, Qt.yellow],
                                           [.15, Qt.green],
                                           [1, Qt.transparent]])

            self.needle_center_bg = [
                                    [0, QColor(35, 40, 3, 255)],
                                    [0.16, QColor(30, 36, 45, 255)],
                                    [0.225, QColor(36, 42, 54, 255)],
                                    [0.423963, QColor(19, 23, 29, 255)],
                                    [0.580645, QColor(45, 53, 68, 255)],
                                    [0.792627, QColor(59, 70, 88, 255)],
                                    [0.935, QColor(30, 35, 45, 255)],
                                    [1, QColor(35, 40, 3, 255)]
            ]

            self.outer_circle_bg = [
                [0.0645161, QColor(30, 35, 45, 255)],
                [0.37788, QColor(57, 67, 86, 255)],
                [1, QColor(30, 36, 45, 255)]
            ]

        if Theme == 1:
            self.set_scale_polygon_colors([[.75, Qt.red],
                                           [.5, Qt.yellow],
                                           [.25, Qt.green]])

            self.needle_center_bg = [
                                    [0, QColor(35, 40, 3, 255)],
                                    [0.16, QColor(30, 36, 45, 255)],
                                    [0.225, QColor(36, 42, 54, 255)],
                                    [0.423963, QColor(19, 23, 29, 255)],
                                    [0.580645, QColor(45, 53, 68, 255)],
                                    [0.792627, QColor(59, 70, 88, 255)],
                                    [0.935, QColor(30, 35, 45, 255)],
                                    [1, QColor(35, 40, 3, 255)]
            ]

            self.outer_circle_bg = [
                [0.0645161, QColor(30, 35, 45, 255)],
                [0.37788, QColor(57, 67, 86, 255)],
                [1, QColor(30, 36, 45, 255)]
            ]

        if Theme == 2:
            self.set_scale_polygon_colors([[.25, Qt.red],
                                           [.5, Qt.yellow],
                                           [.75, Qt.green]])

            self.needle_center_bg = [
                                    [0, QColor(35, 40, 3, 255)],
                                    [0.16, QColor(30, 36, 45, 255)],
                                    [0.225, QColor(36, 42, 54, 255)],
                                    [0.423963, QColor(19, 23, 29, 255)],
                                    [0.580645, QColor(45, 53, 68, 255)],
                                    [0.792627, QColor(59, 70, 88, 255)],
                                    [0.935, QColor(30, 35, 45, 255)],
                                    [1, QColor(35, 40, 3, 255)]
            ]

            self.outer_circle_bg = [
                [0.0645161, QColor(30, 35, 45, 255)],
                [0.37788, QColor(57, 67, 86, 255)],
                [1, QColor(30, 36, 45, 255)]
            ]

        elif Theme == 3:
            self.set_scale_polygon_colors([[.00, Qt.white]])

            self.needle_center_bg = [
                                    [0, Qt.white],
            ]

            self.outer_circle_bg = [
                [0, Qt.white],
            ]

            self.bigScaleMarker = Qt.black
            self.fineScaleColor = Qt.black

        elif Theme == 4:
            self.set_scale_polygon_colors([[1, Qt.black]])

            self.needle_center_bg = [
                                    [0, Qt.black],
            ]

            self.outer_circle_bg = [
                [0, Qt.black],
            ]

            self.bigScaleMarker = Qt.white
            self.fineScaleColor = Qt.white

        elif Theme == 5:
            self.set_scale_polygon_colors([[1, QColor("#029CDE")]])

            self.needle_center_bg = [
                                    [0, QColor("#029CDE")],
            ]

            self.outer_circle_bg = [
                [0, QColor("#029CDE")],
            ]

        elif Theme == 6:
            self.set_scale_polygon_colors([[.75, QColor("#01ADEF")],
                                           [.5, QColor("#0086BF")],
                                           [.25, QColor("#005275")]])

            self.needle_center_bg = [
                                    [0, QColor(0, 46, 61, 255)],
                                    [0.322581, QColor(1, 173, 239, 255)],
                                    [0.571429, QColor(0, 73, 99, 255)],
                                    [1, QColor(0, 46, 61, 255)]
            ]

            self.outer_circle_bg = [
                [0.0645161, QColor(0, 85, 116, 255)],
                [0.37788, QColor(1, 173, 239, 255)],
                [1, QColor(0, 69, 94, 255)]
            ]

            self.bigScaleMarker = Qt.black
            self.fineScaleColor = Qt.black

        elif Theme == 7:
            self.set_scale_polygon_colors([[.25, QColor("#01ADEF")],
                                           [.5, QColor("#0086BF")],
                                           [.75, QColor("#005275")]])

            self.needle_center_bg = [
                                    [0, QColor(0, 46, 61, 255)],
                                    [0.322581, QColor(1, 173, 239, 255)],
                                    [0.571429, QColor(0, 73, 99, 255)],
                                    [1, QColor(0, 46, 61, 255)]
            ]

            self.outer_circle_bg = [
                [0.0645161, QColor(0, 85, 116, 255)],
                [0.37788, QColor(1, 173, 239, 255)],
                [1, QColor(0, 69, 94, 255)]
            ]

            self.bigScaleMarker = Qt.black
            self.fineScaleColor = Qt.black

        elif Theme == 8:
            self.setCustomGaugeTheme(
                color1="#ffaa00",
                color2="#7d5300",
                color3="#3e2900"
            )

            self.bigScaleMarker = Qt.black
            self.fineScaleColor = Qt.black

        elif Theme == 9:
            self.setCustomGaugeTheme(
                color1="#3e2900",
                color2="#7d5300",
                color3="#ffaa00"
            )

            self.bigScaleMarker = Qt.white
            self.fineScaleColor = Qt.white

        elif Theme == 10:
            self.setCustomGaugeTheme(
                color1="#ff007f",
                color2="#aa0055",
                color3="#830042"
            )

            self.bigScaleMarker = Qt.black
            self.fineScaleColor = Qt.black

        elif Theme == 11:
            self.setCustomGaugeTheme(
                color1="#830042",
                color2="#aa0055",
                color3="#ff007f"
            )

            self.bigScaleMarker = Qt.white
            self.fineScaleColor = Qt.white

        elif Theme == 12:
            self.setCustomGaugeTheme(
                color1="#ffe75d",
                color2="#896c1a",
                color3="#232803"
            )

            self.bigScaleMarker = Qt.black
            self.fineScaleColor = Qt.black

        elif Theme == 13:
            self.setCustomGaugeTheme(
                color1="#ffe75d",
                color2="#896c1a",
                color3="#232803"
            )

            self.bigScaleMarker = Qt.black
            self.fineScaleColor = Qt.black

        elif Theme == 14:
            self.setCustomGaugeTheme(
                color1="#232803",
                color2="#821600",
                color3="#ffe75d"
            )

            self.bigScaleMarker = Qt.white
            self.fineScaleColor = Qt.white

        elif Theme == 15:
            self.setCustomGaugeTheme(
                color1="#00FF11",
                color2="#00990A",
                color3="#002603"
            )

            self.bigScaleMarker = Qt.black
            self.fineScaleColor = Qt.black

        elif Theme == 16:
            self.setCustomGaugeTheme(
                color1="#002603",
                color2="#00990A",
                color3="#00FF11"
            )

            self.bigScaleMarker = Qt.white
            self.fineScaleColor = Qt.white

        elif Theme == 17:
            self.setCustomGaugeTheme(
                color1="#00FFCC",
                color2="#00876C",
                color3="#00211B"
            )

            self.bigScaleMarker = Qt.black
            self.fineScaleColor = Qt.black

        elif Theme == 18:
            self.setCustomGaugeTheme(
                color1="#00211B",
                color2="#00876C",
                color3="#00FFCC"
            )

            self.bigScaleMarker = Qt.white
            self.fineScaleColor = Qt.white

        elif Theme == 19:
            self.setCustomGaugeTheme(
                color1="#001EFF",
                color2="#001299",
                color3="#000426"
            )

            self.bigScaleMarker = Qt.black
            self.fineScaleColor = Qt.black

        elif Theme == 20:
            self.setCustomGaugeTheme(
                color1="#000426",
                color2="#001299",
                color3="#001EFF"
            )

            self.bigScaleMarker = Qt.white
            self.fineScaleColor = Qt.white

        elif Theme == 21:
            self.setCustomGaugeTheme(
                color1="#F200FF",
                color2="#85008C",
                color3="#240026"
            )

            self.bigScaleMarker = Qt.black
            self.fineScaleColor = Qt.black

        elif Theme == 22:
            self.setCustomGaugeTheme(
                color1="#240026",
                color2="#85008C",
                color3="#F200FF"
            )

            self.bigScaleMarker = Qt.white
            self.fineScaleColor = Qt.white

        elif Theme == 23:
            self.setCustomGaugeTheme(
                color1="#FF0022",
                color2="#080001",
                color3="#009991"
            )

            self.bigScaleMarker = Qt.white
            self.fineScaleColor = Qt.white

        elif Theme == 24:
            self.setCustomGaugeTheme(
                color1="#009991",
                color2="#080001",
                color3="#FF0022"
            )

            self.bigScaleMarker = Qt.white
            self.fineScaleColor = Qt.white

    def setCustomGaugeTheme(self, **colors):
        if "color1" in colors and len(str(colors['color1'])) > 0:
            if "color2" in colors and len(str(colors['color2'])) > 0:
                if "color3" in colors and len(str(colors['color3'])) > 0:

                    self.set_scale_polygon_colors([[.25, QColor(str(colors['color1']))],
                                                   [.5, QColor(
                                                       str(colors['color2']))],
                                                   [.75, QColor(str(colors['color3']))]])

                    self.needle_center_bg = [
                                            [0, QColor(str(colors['color3']))],
                                            [0.322581, QColor(
                                                str(colors['color1']))],
                                            [0.571429, QColor(
                                                str(colors['color2']))],
                                            [1, QColor(str(colors['color3']))]
                    ]

                    self.outer_circle_bg = [
                        [0.0645161, QColor(str(colors['color3']))],
                        [0.36, QColor(
                            str(colors['color1']))],
                        [1, QColor(str(colors['color2']))]
                    ]

                else:

                    self.set_scale_polygon_colors([[.5, QColor(str(colors['color1']))],
                                                   [1, QColor(str(colors['color2']))]])

                    self.needle_center_bg = [
                                            [0, QColor(str(colors['color2']))],
                                            [1, QColor(str(colors['color1']))]
                    ]

                    self.outer_circle_bg = [
                        [0, QColor(str(colors['color2']))],
                        [1, QColor(str(colors['color2']))]
                    ]

            else:

                self.set_scale_polygon_colors(
                    [[1, QColor(str(colors['color1']))]])

                self.needle_center_bg = [
                                        [1, QColor(str(colors['color1']))]
                ]

                self.outer_circle_bg = [
                    [1, QColor(str(colors['color1']))]
                ]

        else:

            self.setGaugeTheme(0)
            print("color1 is not defined")

    def setScalePolygonColor(self, **colors):
        if "color1" in colors and len(str(colors['color1'])) > 0:
            if "color2" in colors and len(str(colors['color2'])) > 0:
                if "color3" in colors and len(str(colors['color3'])) > 0:

                    self.set_scale_polygon_colors([[.25, QColor(str(colors['color1']))],
                                                   [.5, QColor(
                                                       str(colors['color2']))],
                                                   [.75, QColor(str(colors['color3']))]])

                else:

                    self.set_scale_polygon_colors([[.5, QColor(str(colors['color1']))],
                                                   [1, QColor(str(colors['color2']))]])

            else:

                self.set_scale_polygon_colors(
                    [[1, QColor(str(colors['color1']))]])

        else:
            print("color1 is not defined")

    def setNeedleCenterColor(self, **colors):
        if "color1" in colors and len(str(colors['color1'])) > 0:
            if "color2" in colors and len(str(colors['color2'])) > 0:
                if "color3" in colors and len(str(colors['color3'])) > 0:

                    self.needle_center_bg = [
                                            [0, QColor(str(colors['color3']))],
                                            [0.322581, QColor(
                                                str(colors['color1']))],
                                            [0.571429, QColor(
                                                str(colors['color2']))],
                                            [1, QColor(str(colors['color3']))]
                    ]

                else:

                    self.needle_center_bg = [
                                            [0, QColor(str(colors['color2']))],
                                            [1, QColor(str(colors['color1']))]
                    ]

            else:

                self.needle_center_bg = [
                                        [1, QColor(str(colors['color1']))]
                ]
        else:
            print("color1 is not defined")

    def setOuterCircleColor(self, **colors):
        if "color1" in colors and len(str(colors['color1'])) > 0:
            if "color2" in colors and len(str(colors['color2'])) > 0:
                if "color3" in colors and len(str(colors['color3'])) > 0:

                    self.outer_circle_bg = [
                        [0.0645161, QColor(str(colors['color3']))],
                        [0.37788, QColor(
                            str(colors['color1']))],
                        [1, QColor(str(colors['color2']))]
                    ]

                else:

                    self.outer_circle_bg = [
                        [0, QColor(str(colors['color2']))],
                        [1, QColor(str(colors['color2']))]
                    ]

            else:

                self.outer_circle_bg = [
                    [1, QColor(str(colors['color1']))]
                ]

        else:
            print("color1 is not defined")

    def rescale_method(self):
        if self.width() <= self.height():
            self.widget_diameter = self.width()
        else:
            self.widget_diameter = self.height()
        self.change_value_needle_style([QPolygon([
            QPoint(4, 30),
            QPoint(-4, 30),
            QPoint(-2, int(- self.widget_diameter / 2 * self.needle_scale_factor)),
            QPoint(0, int(- self.widget_diameter /
                   2 * self.needle_scale_factor - 6)),
            QPoint(2, int(- self.widget_diameter / 2 * self.needle_scale_factor))
        ])])

        self.scale_fontsize = int(
            self.initial_scale_fontsize * self.widget_diameter / 400)
        self.value_fontsize = int(
            self.initial_value_fontsize * self.widget_diameter / 400)

    def change_value_needle_style(self, design):
        # prepared for multiple needle instrument
        self.value_needle = []
        for i in design:
            self.value_needle.append(i)
        if not self.use_timer_event:
            self.update()

    def updateValue(self, value, mouse_controlled=False):
        # if not mouse_controlled:
        #     self.value = value
        #
        # if mouse_controlled:
        #     self.valueChanged.emit(int(value))

        if value <= self.minValue:
            self.value = self.minValue
        elif value >= self.maxValue:
            self.value = self.maxValue
        else:
            self.value = value
        # self.paintEvent("")
        self.valueChanged.emit(int(value))
        # print(self.value)

        # ohne timer: aktiviere self.update()
        if not self.use_timer_event:
            self.update()

    def updateAngleOffset(self, offset):
        self.angle_offset = offset
        if not self.use_timer_event:
            self.update()

    def center_horizontal(self, value):
        self.center_horizontal_value = value
        # print("horizontal: " + str(self.center_horizontal_value))

    def center_vertical(self, value):
        self.center_vertical_value = value
        # print("vertical: " + str(self.center_vertical_value))

    def setNeedleColor(self, R=50, G=50, B=50, Transparency=255):
        # Red: R = 0 - 255
        # Green: G = 0 - 255
        # Blue: B = 0 - 255
        # Transparency = 0 - 255
        self.NeedleColor = QColor(R, G, B, Transparency)
        self.NeedleColorReleased = self.NeedleColor

        if not self.use_timer_event:
            self.update()

    def setNeedleColorOnDrag(self, R=50, G=50, B=50, Transparency=255):
        # Red: R = 0 - 255
        # Green: G = 0 - 255
        # Blue: B = 0 - 255
        # Transparency = 0 - 255
        self.NeedleColorDrag = QColor(R, G, B, Transparency)

        if not self.use_timer_event:
            self.update()

    def setScaleValueColor(self, R=50, G=50, B=50, Transparency=255):
        # Red: R = 0 - 255
        # Green: G = 0 - 255
        # Blue: B = 0 - 255
        # Transparency = 0 - 255
        self.ScaleValueColor = QColor(R, G, B, Transparency)

        if not self.use_timer_event:
            self.update()

    def setDisplayValueColor(self, R=50, G=50, B=50, Transparency=255):
        # Red: R = 0 - 255
        # Green: G = 0 - 255
        # Blue: B = 0 - 255
        # Transparency = 0 - 255
        self.DisplayValueColor = QColor(R, G, B, Transparency)

        if not self.use_timer_event:
            self.update()

    def set_CenterPointColor(self, R=50, G=50, B=50, Transparency=255):
        self.CenterPointColor = QColor(R, G, B, Transparency)

        if not self.use_timer_event:
            self.update()

    def setEnableNeedlePolygon(self, enable=True):
        self.enable_Needle_Polygon = enable

        if not self.use_timer_event:
            self.update()

    def setEnableScaleText(self, enable=True):
        self.enable_scale_text = enable

        if not self.use_timer_event:
            self.update()

    def setEnableBarGraph(self, enable=True):
        self.enableBarGraph = enable

        if not self.use_timer_event:
            self.update()

    def setEnableValueText(self, enable=True):
        self.enable_value_text = enable

        if not self.use_timer_event:
            self.update()

    def setEnableCenterPoint(self, enable=True):
        self.enable_CenterPoint = enable

        if not self.use_timer_event:
            self.update()

    def setEnableScalePolygon(self, enable=True):
        self.enable_filled_Polygon = enable

        if not self.use_timer_event:
            self.update()

    def setEnableBigScaleGrid(self, enable=True):
        self.enable_big_scaled_marker = enable

        if not self.use_timer_event:
            self.update()

    def setEnableFineScaleGrid(self, enable=True):
        self.enable_fine_scaled_marker = enable

        if not self.use_timer_event:
            self.update()

    def setScalaCount(self, count):
        if count < 1:
            count = 1
        self.scalaCount = count

        if not self.use_timer_event:
            self.update()

    def setMinValue(self, min):
        if self.value < min:
            self.value = min
        if min >= self.maxValue:
            self.minValue = self.maxValue - 1
        else:
            self.minValue = min

        if not self.use_timer_event:
            self.update()

    def setMaxValue(self, max):
        if self.value > max:
            self.value = max
        if max <= self.minValue:
            self.maxValue = self.minValue + 1
        else:
            self.maxValue = max

        if not self.use_timer_event:
            self.update()

    def setScaleStartAngle(self, value):
        # Value range in DEG: 0 - 360
        self.scale_angle_start_value = value
        # print("startFill: " + str(self.scale_angle_start_value))

        if not self.use_timer_event:
            self.update()

    def setTotalScaleAngleSize(self, value):
        self.scale_angle_size = value
        # print("stopFill: " + str(self.scale_angle_size))

        if not self.use_timer_event:
            self.update()

    def setGaugeColorOuterRadiusFactor(self, value):
        self.gauge_color_outer_radius_factor = float(value) / 1000
        # print(self.gauge_color_outer_radius_factor)

        if not self.use_timer_event:
            self.update()

    def setGaugeColorInnerRadiusFactor(self, value):
        self.gauge_color_inner_radius_factor = float(value) / 1000
        # print(self.gauge_color_inner_radius_factor)

        if not self.use_timer_event:
            self.update()

    def set_scale_polygon_colors(self, color_array):
        # print(type(color_array))
        if 'list' in str(type(color_array)):
            self.scale_polygon_colors = color_array
        elif color_array == None:
            self.scale_polygon_colors = [[.0, Qt.transparent]]
        else:
            self.scale_polygon_colors = [[.0, Qt.transparent]]

        if not self.use_timer_event:
            self.update()

    ################################################################################################
    # GET MAXIMUM VALUE
    ################################################################################################
    def get_value_max(self):
        return self.maxValue

    def create_polygon_pie(self, outer_radius, inner_raduis, start, lenght, bar_graph=True):
        polygon_pie = QPolygonF()
        # start = self.scale_angle_start_value
        # start = 0
        # lenght = self.scale_angle_size
        # lenght = 180
        # inner_raduis = self.width()/4
        # print(start)
        n = 360     # angle steps size for full circle
        # changing n value will causes drawing issues
        w = 360 / n   # angle per step
        # create outer circle line from "start"-angle to "start + lenght"-angle
        x = 0
        y = 0

        # todo enable/disable bar graf here
        if not self.enableBarGraph and bar_graph:
            # float_value = ((lenght / (self.maxValue - self.minValue)) * (self.value - self.minValue))
            lenght = int(
                round((lenght / (self.maxValue - self.minValue)) * (self.value - self.minValue)))
            # print("f: %s, l: %s" %(float_value, lenght))
            pass

        # mymax = 0

        # add the points of polygon
        for i in range(lenght + 1):
            t = w * i + start - self.angle_offset
            x = outer_radius * math.cos(math.radians(t))
            y = outer_radius * math.sin(math.radians(t))
            polygon_pie.append(QPointF(x, y))
        # create inner circle line from "start + lenght"-angle to "start"-angle
        # add the points of polygon
        for i in range(lenght + 1):
            # print("2 " + str(i))
            t = w * (lenght - i) + start - self.angle_offset
            x = inner_raduis * math.cos(math.radians(t))
            y = inner_raduis * math.sin(math.radians(t))
            polygon_pie.append(QPointF(x, y))

        # close outer line
        polygon_pie.append(QPointF(x, y))
        return polygon_pie

    def draw_filled_polygon(self, outline_pen_with=0):
        if not self.scale_polygon_colors == None:
            painter_filled_polygon = QPainter(self)
            painter_filled_polygon.setRenderHint(QPainter.Antialiasing)
            # Koordinatenursprung in die Mitte der Flaeche legen
            painter_filled_polygon.translate(
                self.width() / 2, self.height() / 2)

            painter_filled_polygon.setPen(Qt.NoPen)

            self.pen.setWidth(outline_pen_with)
            if outline_pen_with > 0:
                painter_filled_polygon.setPen(self.pen)

            colored_scale_polygon = self.create_polygon_pie(
                ((self.widget_diameter / 2) - (self.pen.width() / 2)) *
                self.gauge_color_outer_radius_factor,
                (((self.widget_diameter / 2) - (self.pen.width() / 2))
                 * self.gauge_color_inner_radius_factor),
                self.scale_angle_start_value, self.scale_angle_size)

            gauge_rect = QRect(QPoint(0, 0), QSize(
                int(self.widget_diameter / 2 - 1), int(self.widget_diameter - 1)))
            grad = QConicalGradient(QPointF(0, 0), - self.scale_angle_size - self.scale_angle_start_value +
                                    self.angle_offset - 1)

            # todo definition scale color as array here
            for eachcolor in self.scale_polygon_colors:
                grad.setColorAt(eachcolor[0], eachcolor[1])
            # grad.setColorAt(.00, Qt.red)
            # grad.setColorAt(.1, Qt.yellow)
            # grad.setColorAt(.15, Qt.green)
            # grad.setColorAt(1, Qt.transparent)
            # self.brush = QBrush(QColor(255, 0, 255, 255))
            # grad.setStyle(Qt.Dense6Pattern)
            # painter_filled_polygon.setBrush(self.brush)
            painter_filled_polygon.setBrush(grad)

            painter_filled_polygon.drawPolygon(colored_scale_polygon)
            # return painter_filled_polygon

    def draw_icon_image(self):
        pass

    def draw_big_scaled_marker(self):
        my_painter = QPainter(self)
        my_painter.setRenderHint(QPainter.Antialiasing)
        # Koordinatenursprung in die Mitte der Flaeche legen
        my_painter.translate(self.width() / 2, self.height() / 2)

        # my_painter.setPen(Qt.NoPen)
        self.pen = QPen(self.bigScaleMarker)
        self.pen.setWidth(2)
        # # if outline_pen_with > 0:
        my_painter.setPen(self.pen)

        my_painter.rotate(self.scale_angle_start_value - self.angle_offset)
        steps_size = (float(self.scale_angle_size) / float(self.scalaCount))
        scale_line_outer_start = self.widget_diameter // 2
        scale_line_lenght = int((self.widget_diameter / 2) -
                                (self.widget_diameter / 20))
        # print(stepszize)
        for i in range(self.scalaCount + 1):
            my_painter.drawLine(scale_line_lenght, 0,
                                scale_line_outer_start, 0)
            my_painter.rotate(steps_size)

    def create_scale_marker_values_text(self):
        painter = QPainter(self)
        # painter.setRenderHint(QPainter.HighQualityAntialiasing)
        painter.setRenderHint(QPainter.Antialiasing)

        # Koordinatenursprung in die Mitte der Flaeche legen
        painter.translate(self.width() / 2, self.height() / 2)
        # painter.save()
        font = QFont(self.scale_fontname, self.scale_fontsize, QFont.Bold)
        fm = QFontMetrics(font)

        pen_shadow = QPen()

        pen_shadow.setBrush(self.ScaleValueColor)
        painter.setPen(pen_shadow)

        text_radius_factor = 0.8
        text_radius = self.widget_diameter / 2 * text_radius_factor

        scale_per_div = int((self.maxValue - self.minValue) / self.scalaCount)

        angle_distance = (float(self.scale_angle_size) /
                          float(self.scalaCount))
        for i in range(self.scalaCount + 1):
            # text = str(int((self.maxValue - self.minValue) / self.scalaCount * i))
            text = str(int(self.minValue + scale_per_div * i))
            w = fm.width(text) + 1
            h = fm.height()
            painter.setFont(QFont(self.scale_fontname,
                            self.scale_fontsize, QFont.Bold))
            angle = angle_distance * i + \
                float(self.scale_angle_start_value - self.angle_offset)
            x = text_radius * math.cos(math.radians(angle))
            y = text_radius * math.sin(math.radians(angle))
            # print(w, h, x, y, text)

            painter.drawText(int(x - w / 2), int(y - h / 2), int(w),
                             int(h), Qt.AlignCenter, text)
        # painter.restore()

    def create_fine_scaled_marker(self):
        #  Description_dict = 0
        my_painter = QPainter(self)

        my_painter.setRenderHint(QPainter.Antialiasing)
        # Koordinatenursprung in die Mitte der Flaeche legen
        my_painter.translate(self.width() / 2, self.height() / 2)

        my_painter.setPen(self.fineScaleColor)
        my_painter.rotate(self.scale_angle_start_value - self.angle_offset)
        steps_size = (float(self.scale_angle_size) /
                      float(self.scalaCount * self.scala_subdiv_count))
        scale_line_outer_start = self.widget_diameter // 2
        scale_line_lenght = int(
            (self.widget_diameter / 2) - (self.widget_diameter / 40))
        for i in range((self.scalaCount * self.scala_subdiv_count) + 1):
            my_painter.drawLine(scale_line_lenght, 0,
                                scale_line_outer_start, 0)
            my_painter.rotate(steps_size)

    def create_values_text(self):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.HighQualityAntialiasing)
        # painter.setRenderHint(QPainter.Antialiasing)

        painter.translate(self.width() / 2, self.height() / 2)
        font = QFont(self.value_fontname, self.value_fontsize, QFont.Bold)
        fm = QFontMetrics(font)

        pen_shadow = QPen()

        pen_shadow.setBrush(self.DisplayValueColor)
        painter.setPen(pen_shadow)

        text_radius = self.widget_diameter / 2 * self.text_radius_factor
        text = str(int(self.value))
        w = fm.width(text) + 1
        h = fm.height()
        painter.setFont(QFont(self.value_fontname,
                        self.value_fontsize, QFont.Bold))
        angle_end = float(self.scale_angle_start_value +
                          self.scale_angle_size - 360)
        angle = (angle_end - self.scale_angle_start_value) / \
            2 + self.scale_angle_start_value

        x = text_radius * math.cos(math.radians(angle))
        y = text_radius * math.sin(math.radians(angle))
        # print(w, h, x, y, text)
        painter.drawText(int(x - w / 2), int(y - h / 2), int(w),
                         int(h), Qt.AlignCenter, text)

    def create_units_text(self):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.HighQualityAntialiasing)
        # painter.setRenderHint(QPainter.Antialiasing)

        painter.translate(self.width() / 2, self.height() / 2)
        font = QFont(self.value_fontname, int(
            self.value_fontsize / 2.5), QFont.Bold)
        fm = QFontMetrics(font)

        pen_shadow = QPen()

        pen_shadow.setBrush(self.DisplayValueColor)
        painter.setPen(pen_shadow)

        text_radius = self.widget_diameter / 2 * self.text_radius_factor

        text = str(self.units)
        w = fm.width(text) + 1
        h = fm.height()
        painter.setFont(QFont(self.value_fontname, int(
            self.value_fontsize / 2.5), QFont.Bold))

        angle_end = float(self.scale_angle_start_value +
                          self.scale_angle_size + 180)
        angle = (angle_end - self.scale_angle_start_value) / \
            2 + self.scale_angle_start_value

        x = text_radius * math.cos(math.radians(angle))
        y = text_radius * math.sin(math.radians(angle))
        # print(w, h, x, y, text)
        painter.drawText(int(x - w / 2), int(y - h / 2), int(w),
                         int(h), Qt.AlignCenter, text)


    def draw_big_needle_center_point(self, diameter=30):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.translate(self.width() / 2, self.height() / 2)
        painter.setPen(Qt.NoPen)
        colored_scale_polygon = self.create_polygon_pie(
            ((self.widget_diameter / 8) - (self.pen.width() / 2)),
            0,
            self.scale_angle_start_value, 360, False)

        grad = QConicalGradient(QPointF(0, 0), 0)

        # todo definition scale color as array here
        for eachcolor in self.needle_center_bg:
            grad.setColorAt(eachcolor[0], eachcolor[1])
        painter.setBrush(grad)

        painter.drawPolygon(colored_scale_polygon)
    def draw_outer_circle(self, diameter=30):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        painter.translate(self.width() / 2, self.height() / 2)
        painter.setPen(Qt.NoPen)
        colored_scale_polygon = self.create_polygon_pie(
            ((self.widget_diameter / 2) - (self.pen.width())),
            (self.widget_diameter / 6),
            self.scale_angle_start_value / 10, 360, False)

        radialGradient = QRadialGradient(QPointF(0, 0), self.width())

        for eachcolor in self.outer_circle_bg:
            radialGradient.setColorAt(eachcolor[0], eachcolor[1])

        painter.setBrush(radialGradient)

        painter.drawPolygon(colored_scale_polygon)

    ################################################################################################
    # NEEDLE POINTER
    ################################################################################################

    def draw_needle(self):
        painter = QPainter(self)
        # painter.setRenderHint(QtGui.QPainter.HighQualityAntialiasing)
        painter.setRenderHint(QPainter.Antialiasing)
        # Koordinatenursprung in die Mitte der Flaeche legen
        painter.translate(self.width() / 2, self.height() / 2)
        painter.setPen(Qt.NoPen)
        painter.setBrush(self.NeedleColor)
        painter.rotate(((self.value - self.value_offset - self.minValue) * self.scale_angle_size /
                        (self.maxValue - self.minValue)) + 90 + self.scale_angle_start_value)

        painter.drawConvexPolygon(self.value_needle[0])

    ###############################################################################################
    # EVENTS
    ###############################################################################################

    ################################################################################################
    # ON WINDOW RESIZE
    ################################################################################################
    def resizeEvent(self, event):
        # self.resized.emit()
        # return super(self.parent, self).resizeEvent(event)
        # print("resized")
        # print(self.width())
        self.rescale_method()
        # self.emit(QtCore.SIGNAL("resize()"))
        # print("resizeEvent")

    ################################################################################################
    # ON PAINT EVENT
    ################################################################################################
    def paintEvent(self, event):
        # Main Drawing Event:
        # Will be executed on every change
        # vgl http://doc.qt.io/qt-4.8/qt-demos-affine-xform-cpp.html
        # print("event", event)

        self.draw_outer_circle()
        self.draw_icon_image()
        # colored pie area
        if self.enable_filled_Polygon:
            self.draw_filled_polygon()

        # draw scale marker lines
        if self.enable_fine_scaled_marker:
            self.create_fine_scaled_marker()
        if self.enable_big_scaled_marker:
            self.draw_big_scaled_marker()

        # draw scale marker value text
        if self.enable_scale_text:
            self.create_scale_marker_values_text()

        # Display Value
        if self.enable_value_text:
            self.create_values_text()
            self.create_units_text()

        # draw needle 1
        if self.enable_Needle_Polygon:
            self.draw_needle()

        # Draw Center Point
        if self.enable_CenterPoint:
            self.draw_big_needle_center_point(
                diameter=(self.widget_diameter / 6))

    ###############################################################################################
    # MOUSE EVENTS
    ###############################################################################################

    def setMouseTracking(self, flag):
        def recursive_set(parent):
            for child in parent.findChildren(QObject):
                try:
                    child.setMouseTracking(flag)
                except:
                    pass
                recursive_set(child)

        QWidget.setMouseTracking(self, flag)
        recursive_set(self)

    def mouseReleaseEvent(self, QMouseEvent):
        self.NeedleColor = self.NeedleColorReleased

        if not self.use_timer_event:
            self.update()
        pass

    ########################################################################
    # MOUSE LEAVE EVENT
    ########################################################################
    def leaveEvent(self, event):
        self.NeedleColor = self.NeedleColorReleased
        self.update()

    def mouseMoveEvent(self, event):
        x, y = event.x() - (self.width() / 2), event.y() - (self.height() / 2)
        # print(event.x(), event.y(), self.width(), self.height())
        if not x == 0:
            angle = math.atan2(y, x) / math.pi * 180
            # winkellaenge der anzeige immer positiv 0 - 360deg
            # min wert + umskalierter wert
            value = (float(math.fmod(angle - self.scale_angle_start_value + 720, 360)) /
                     (float(self.scale_angle_size) / float(self.maxValue - self.minValue))) + self.minValue
            temp = value
            fmod = float(
                math.fmod(angle - self.scale_angle_start_value + 720, 360))
            state = 0
            if (self.value - (self.maxValue - self.minValue) * self.valueNeedleSnapzone) <= \
                    value <= \
                    (self.value + (self.maxValue - self.minValue) * self.valueNeedleSnapzone):
                self.NeedleColor = self.NeedleColorDrag
                # todo: evtl ueberpruefen
                #
                state = 9
                # if value >= self.maxValue and self.last_value < (self.maxValue - self.minValue) / 2:
                if value >= self.maxValue and self.last_value < (self.maxValue - self.minValue) / 2:
                    state = 1
                    value = self.maxValue
                    self.last_value = self.minValue
                    self.valueChanged.emit(int(value))

                elif value >= self.maxValue >= self.last_value:
                    state = 2
                    value = self.maxValue
                    self.last_value = self.maxValue
                    self.valueChanged.emit(int(value))

                else:
                    state = 3
                    self.last_value = value
                    self.valueChanged.emit(int(value))

                self.updateValue(value)


#!####################################################################################################################################################### GROUND END

###############################################################################################################################################! AİRSPEED START
class AnalogGauge_airSpeed(QWidget):
    valueChanged = pyqtSignal(int)
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(100, 100)
        
        self.altTimer = QTimer()
        self.altTimer.start(10) # Saniyede bir güncelle
        self.altTimer.timeout.connect(self.update_airSpeed)
    
    def update_airSpeed(self):
        while True:
            gaugeAirspeed = vehicle.airspeed
            self.value= gaugeAirspeed
            break
        
        self.use_timer_event = False
        self.setNeedleColor(0, 0, 0, 255)
        self.NeedleColorReleased = self.NeedleColor
        self.setNeedleColorOnDrag(255, 0, 00, 255)
        self.setScaleValueColor(0, 0, 0, 255)
        self.setDisplayValueColor(0, 0, 0, 255)
        self.set_CenterPointColor(0, 0, 0, 255)
        self.value_needle_count = 1
        self.value_needle = QObject
        self.minValue = 0
        self.maxValue = 100
        
        self.value_offset = 0

        self.valueNeedleSnapzone = 0.05
        self.last_value = 0
        self.gauge_color_outer_radius_factor = 1
        self.gauge_color_inner_radius_factor = 0.9

        self.center_horizontal_value = 0
        self.center_vertical_value = 0

        self.scale_angle_start_value = 135
        self.scale_angle_size = 270

        self.angle_offset = 0

        self.setScalaCount(10)
        self.scala_subdiv_count = 5

        self.pen = QPen(QColor(0, 0, 0))

        QFontDatabase.addApplicationFont(os.path.join(os.path.dirname(
            __file__), 'fonts/Orbitron/Orbitron-VariableFont_wght.ttf'))

        self.scale_polygon_colors = []

        self.bigScaleMarker = Qt.black

        self.fineScaleColor = Qt.black

        self.setEnableScaleText(True)
        self.scale_fontname = "Orbitron"
        self.initial_scale_fontsize = 14
        self.scale_fontsize = self.initial_scale_fontsize
        self.enable_value_text = True
        self.value_fontname = "Orbitron"
        self.initial_value_fontsize = 40
        self.value_fontsize = self.initial_value_fontsize
        self.text_radius_factor = 0.5
        self.setEnableBarGraph(True)
        self.setEnableScalePolygon(True)
        self.enable_CenterPoint = True
        self.enable_fine_scaled_marker = True
        self.enable_big_scaled_marker = True
        self.needle_scale_factor = 0.8
        self.enable_Needle_Polygon = True

        self.setMouseTracking(False)
        self.units = "m/s"

        # QTimer sorgt für neu Darstellung alle X ms
        # evtl performance hier verbessern mit self.update() und self.use_timer_event = False
        # todo: self.update als default ohne ueberpruefung, ob self.use_timer_event gesetzt ist oder nicht
        # Timer startet alle 10ms das event paintEvent
        if self.use_timer_event:
            timer = QTimer(self)
            timer.timeout.connect(self.update)
            timer.start(10)
        else:
            self.update()

        self.setGaugeTheme(0)

        self.rescale_method()

    def setScaleFontFamily(self, font):
        self.scale_fontname = str(font)

    def setValueFontFamily(self, font):
        self.value_fontname = str(font)

    def setBigScaleColor(self, color):
        self.bigScaleMarker = QColor(color)

    def setFineScaleColor(self, color):
        self.fineScaleColor = QColor(color)

    def setGaugeTheme(self, Theme=1):
        if Theme == 0 or Theme == None:
            self.set_scale_polygon_colors([[.00, Qt.red],
                                           [.1, Qt.yellow],
                                           [.15, Qt.green],
                                           [1, Qt.transparent]])

            self.needle_center_bg = [
                                    [0, QColor(35, 40, 3, 255)],
                                    [0.16, QColor(30, 36, 45, 255)],
                                    [0.225, QColor(36, 42, 54, 255)],
                                    [0.423963, QColor(19, 23, 29, 255)],
                                    [0.580645, QColor(45, 53, 68, 255)],
                                    [0.792627, QColor(59, 70, 88, 255)],
                                    [0.935, QColor(30, 35, 45, 255)],
                                    [1, QColor(35, 40, 3, 255)]
            ]

            self.outer_circle_bg = [
                [0.0645161, QColor(30, 35, 45, 255)],
                [0.37788, QColor(57, 67, 86, 255)],
                [1, QColor(30, 36, 45, 255)]
            ]

        if Theme == 1:
            self.set_scale_polygon_colors([[.75, Qt.red],
                                           [.5, Qt.yellow],
                                           [.25, Qt.green]])

            self.needle_center_bg = [
                                    [0, QColor(35, 40, 3, 255)],
                                    [0.16, QColor(30, 36, 45, 255)],
                                    [0.225, QColor(36, 42, 54, 255)],
                                    [0.423963, QColor(19, 23, 29, 255)],
                                    [0.580645, QColor(45, 53, 68, 255)],
                                    [0.792627, QColor(59, 70, 88, 255)],
                                    [0.935, QColor(30, 35, 45, 255)],
                                    [1, QColor(35, 40, 3, 255)]
            ]

            self.outer_circle_bg = [
                [0.0645161, QColor(30, 35, 45, 255)],
                [0.37788, QColor(57, 67, 86, 255)],
                [1, QColor(30, 36, 45, 255)]
            ]

        if Theme == 2:
            self.set_scale_polygon_colors([[.25, Qt.red],
                                           [.5, Qt.yellow],
                                           [.75, Qt.green]])

            self.needle_center_bg = [
                                    [0, QColor(35, 40, 3, 255)],
                                    [0.16, QColor(30, 36, 45, 255)],
                                    [0.225, QColor(36, 42, 54, 255)],
                                    [0.423963, QColor(19, 23, 29, 255)],
                                    [0.580645, QColor(45, 53, 68, 255)],
                                    [0.792627, QColor(59, 70, 88, 255)],
                                    [0.935, QColor(30, 35, 45, 255)],
                                    [1, QColor(35, 40, 3, 255)]
            ]

            self.outer_circle_bg = [
                [0.0645161, QColor(30, 35, 45, 255)],
                [0.37788, QColor(57, 67, 86, 255)],
                [1, QColor(30, 36, 45, 255)]
            ]

        elif Theme == 3:
            self.set_scale_polygon_colors([[.00, Qt.white]])

            self.needle_center_bg = [
                                    [0, Qt.white],
            ]

            self.outer_circle_bg = [
                [0, Qt.white],
            ]

            self.bigScaleMarker = Qt.black
            self.fineScaleColor = Qt.black

        elif Theme == 4:
            self.set_scale_polygon_colors([[1, Qt.black]])

            self.needle_center_bg = [
                                    [0, Qt.black],
            ]

            self.outer_circle_bg = [
                [0, Qt.black],
            ]

            self.bigScaleMarker = Qt.white
            self.fineScaleColor = Qt.white

        elif Theme == 5:
            self.set_scale_polygon_colors([[1, QColor("#029CDE")]])

            self.needle_center_bg = [
                                    [0, QColor("#029CDE")],
            ]

            self.outer_circle_bg = [
                [0, QColor("#029CDE")],
            ]

        elif Theme == 6:
            self.set_scale_polygon_colors([[.75, QColor("#01ADEF")],
                                           [.5, QColor("#0086BF")],
                                           [.25, QColor("#005275")]])

            self.needle_center_bg = [
                                    [0, QColor(0, 46, 61, 255)],
                                    [0.322581, QColor(1, 173, 239, 255)],
                                    [0.571429, QColor(0, 73, 99, 255)],
                                    [1, QColor(0, 46, 61, 255)]
            ]

            self.outer_circle_bg = [
                [0.0645161, QColor(0, 85, 116, 255)],
                [0.37788, QColor(1, 173, 239, 255)],
                [1, QColor(0, 69, 94, 255)]
            ]

            self.bigScaleMarker = Qt.black
            self.fineScaleColor = Qt.black

        elif Theme == 7:
            self.set_scale_polygon_colors([[.25, QColor("#01ADEF")],
                                           [.5, QColor("#0086BF")],
                                           [.75, QColor("#005275")]])

            self.needle_center_bg = [
                                    [0, QColor(0, 46, 61, 255)],
                                    [0.322581, QColor(1, 173, 239, 255)],
                                    [0.571429, QColor(0, 73, 99, 255)],
                                    [1, QColor(0, 46, 61, 255)]
            ]

            self.outer_circle_bg = [
                [0.0645161, QColor(0, 85, 116, 255)],
                [0.37788, QColor(1, 173, 239, 255)],
                [1, QColor(0, 69, 94, 255)]
            ]

            self.bigScaleMarker = Qt.black
            self.fineScaleColor = Qt.black

        elif Theme == 8:
            self.setCustomGaugeTheme(
                color1="#ffaa00",
                color2="#7d5300",
                color3="#3e2900"
            )

            self.bigScaleMarker = Qt.black
            self.fineScaleColor = Qt.black

        elif Theme == 9:
            self.setCustomGaugeTheme(
                color1="#3e2900",
                color2="#7d5300",
                color3="#ffaa00"
            )

            self.bigScaleMarker = Qt.white
            self.fineScaleColor = Qt.white

        elif Theme == 10:
            self.setCustomGaugeTheme(
                color1="#ff007f",
                color2="#aa0055",
                color3="#830042"
            )

            self.bigScaleMarker = Qt.black
            self.fineScaleColor = Qt.black

        elif Theme == 11:
            self.setCustomGaugeTheme(
                color1="#830042",
                color2="#aa0055",
                color3="#ff007f"
            )

            self.bigScaleMarker = Qt.white
            self.fineScaleColor = Qt.white

        elif Theme == 12:
            self.setCustomGaugeTheme(
                color1="#ffe75d",
                color2="#896c1a",
                color3="#232803"
            )

            self.bigScaleMarker = Qt.black
            self.fineScaleColor = Qt.black

        elif Theme == 13:
            self.setCustomGaugeTheme(
                color1="#ffe75d",
                color2="#896c1a",
                color3="#232803"
            )

            self.bigScaleMarker = Qt.black
            self.fineScaleColor = Qt.black

        elif Theme == 14:
            self.setCustomGaugeTheme(
                color1="#232803",
                color2="#821600",
                color3="#ffe75d"
            )

            self.bigScaleMarker = Qt.white
            self.fineScaleColor = Qt.white

        elif Theme == 15:
            self.setCustomGaugeTheme(
                color1="#00FF11",
                color2="#00990A",
                color3="#002603"
            )

            self.bigScaleMarker = Qt.black
            self.fineScaleColor = Qt.black

        elif Theme == 16:
            self.setCustomGaugeTheme(
                color1="#002603",
                color2="#00990A",
                color3="#00FF11"
            )

            self.bigScaleMarker = Qt.white
            self.fineScaleColor = Qt.white

        elif Theme == 17:
            self.setCustomGaugeTheme(
                color1="#00FFCC",
                color2="#00876C",
                color3="#00211B"
            )

            self.bigScaleMarker = Qt.black
            self.fineScaleColor = Qt.black

        elif Theme == 18:
            self.setCustomGaugeTheme(
                color1="#00211B",
                color2="#00876C",
                color3="#00FFCC"
            )

            self.bigScaleMarker = Qt.white
            self.fineScaleColor = Qt.white

        elif Theme == 19:
            self.setCustomGaugeTheme(
                color1="#001EFF",
                color2="#001299",
                color3="#000426"
            )

            self.bigScaleMarker = Qt.black
            self.fineScaleColor = Qt.black

        elif Theme == 20:
            self.setCustomGaugeTheme(
                color1="#000426",
                color2="#001299",
                color3="#001EFF"
            )

            self.bigScaleMarker = Qt.white
            self.fineScaleColor = Qt.white

        elif Theme == 21:
            self.setCustomGaugeTheme(
                color1="#F200FF",
                color2="#85008C",
                color3="#240026"
            )

            self.bigScaleMarker = Qt.black
            self.fineScaleColor = Qt.black

        elif Theme == 22:
            self.setCustomGaugeTheme(
                color1="#240026",
                color2="#85008C",
                color3="#F200FF"
            )

            self.bigScaleMarker = Qt.white
            self.fineScaleColor = Qt.white

        elif Theme == 23:
            self.setCustomGaugeTheme(
                color1="#FF0022",
                color2="#080001",
                color3="#009991"
            )

            self.bigScaleMarker = Qt.white
            self.fineScaleColor = Qt.white

        elif Theme == 24:
            self.setCustomGaugeTheme(
                color1="#009991",
                color2="#080001",
                color3="#FF0022"
            )

            self.bigScaleMarker = Qt.white
            self.fineScaleColor = Qt.white

    def setCustomGaugeTheme(self, **colors):
        if "color1" in colors and len(str(colors['color1'])) > 0:
            if "color2" in colors and len(str(colors['color2'])) > 0:
                if "color3" in colors and len(str(colors['color3'])) > 0:

                    self.set_scale_polygon_colors([[.25, QColor(str(colors['color1']))],
                                                   [.5, QColor(
                                                       str(colors['color2']))],
                                                   [.75, QColor(str(colors['color3']))]])

                    self.needle_center_bg = [
                                            [0, QColor(str(colors['color3']))],
                                            [0.322581, QColor(
                                                str(colors['color1']))],
                                            [0.571429, QColor(
                                                str(colors['color2']))],
                                            [1, QColor(str(colors['color3']))]
                    ]

                    self.outer_circle_bg = [
                        [0.0645161, QColor(str(colors['color3']))],
                        [0.36, QColor(
                            str(colors['color1']))],
                        [1, QColor(str(colors['color2']))]
                    ]

                else:

                    self.set_scale_polygon_colors([[.5, QColor(str(colors['color1']))],
                                                   [1, QColor(str(colors['color2']))]])

                    self.needle_center_bg = [
                                            [0, QColor(str(colors['color2']))],
                                            [1, QColor(str(colors['color1']))]
                    ]

                    self.outer_circle_bg = [
                        [0, QColor(str(colors['color2']))],
                        [1, QColor(str(colors['color2']))]
                    ]

            else:

                self.set_scale_polygon_colors(
                    [[1, QColor(str(colors['color1']))]])

                self.needle_center_bg = [
                                        [1, QColor(str(colors['color1']))]
                ]

                self.outer_circle_bg = [
                    [1, QColor(str(colors['color1']))]
                ]

        else:

            self.setGaugeTheme(0)
            print("color1 is not defined")

    def setScalePolygonColor(self, **colors):
        if "color1" in colors and len(str(colors['color1'])) > 0:
            if "color2" in colors and len(str(colors['color2'])) > 0:
                if "color3" in colors and len(str(colors['color3'])) > 0:

                    self.set_scale_polygon_colors([[.25, QColor(str(colors['color1']))],
                                                   [.5, QColor(
                                                       str(colors['color2']))],
                                                   [.75, QColor(str(colors['color3']))]])

                else:

                    self.set_scale_polygon_colors([[.5, QColor(str(colors['color1']))],
                                                   [1, QColor(str(colors['color2']))]])

            else:

                self.set_scale_polygon_colors(
                    [[1, QColor(str(colors['color1']))]])

        else:
            print("color1 is not defined")

    def setNeedleCenterColor(self, **colors):
        if "color1" in colors and len(str(colors['color1'])) > 0:
            if "color2" in colors and len(str(colors['color2'])) > 0:
                if "color3" in colors and len(str(colors['color3'])) > 0:

                    self.needle_center_bg = [
                                            [0, QColor(str(colors['color3']))],
                                            [0.322581, QColor(
                                                str(colors['color1']))],
                                            [0.571429, QColor(
                                                str(colors['color2']))],
                                            [1, QColor(str(colors['color3']))]
                    ]

                else:

                    self.needle_center_bg = [
                                            [0, QColor(str(colors['color2']))],
                                            [1, QColor(str(colors['color1']))]
                    ]

            else:

                self.needle_center_bg = [
                                        [1, QColor(str(colors['color1']))]
                ]
        else:
            print("color1 is not defined")

    def setOuterCircleColor(self, **colors):
        if "color1" in colors and len(str(colors['color1'])) > 0:
            if "color2" in colors and len(str(colors['color2'])) > 0:
                if "color3" in colors and len(str(colors['color3'])) > 0:

                    self.outer_circle_bg = [
                        [0.0645161, QColor(str(colors['color3']))],
                        [0.37788, QColor(
                            str(colors['color1']))],
                        [1, QColor(str(colors['color2']))]
                    ]

                else:

                    self.outer_circle_bg = [
                        [0, QColor(str(colors['color2']))],
                        [1, QColor(str(colors['color2']))]
                    ]

            else:

                self.outer_circle_bg = [
                    [1, QColor(str(colors['color1']))]
                ]

        else:
            print("color1 is not defined")

    def rescale_method(self):
        if self.width() <= self.height():
            self.widget_diameter = self.width()
        else:
            self.widget_diameter = self.height()
        self.change_value_needle_style([QPolygon([
            QPoint(4, 30),
            QPoint(-4, 30),
            QPoint(-2, int(- self.widget_diameter / 2 * self.needle_scale_factor)),
            QPoint(0, int(- self.widget_diameter /
                   2 * self.needle_scale_factor - 6)),
            QPoint(2, int(- self.widget_diameter / 2 * self.needle_scale_factor))
        ])])

        self.scale_fontsize = int(
            self.initial_scale_fontsize * self.widget_diameter / 400)
        self.value_fontsize = int(
            self.initial_value_fontsize * self.widget_diameter / 400)

    def change_value_needle_style(self, design):
        # prepared for multiple needle instrument
        self.value_needle = []
        for i in design:
            self.value_needle.append(i)
        if not self.use_timer_event:
            self.update()

    def updateValue(self, value, mouse_controlled=False):
        # if not mouse_controlled:
        #     self.value = value
        #
        # if mouse_controlled:
        #     self.valueChanged.emit(int(value))

        if value <= self.minValue:
            self.value = self.minValue
        elif value >= self.maxValue:
            self.value = self.maxValue
        else:
            self.value = value
        # self.paintEvent("")
        self.valueChanged.emit(int(value))
        # print(self.value)

        # ohne timer: aktiviere self.update()
        if not self.use_timer_event:
            self.update()

    def updateAngleOffset(self, offset):
        self.angle_offset = offset
        if not self.use_timer_event:
            self.update()

    def center_horizontal(self, value):
        self.center_horizontal_value = value
        # print("horizontal: " + str(self.center_horizontal_value))

    def center_vertical(self, value):
        self.center_vertical_value = value
        # print("vertical: " + str(self.center_vertical_value))

    def setNeedleColor(self, R=50, G=50, B=50, Transparency=255):
        # Red: R = 0 - 255
        # Green: G = 0 - 255
        # Blue: B = 0 - 255
        # Transparency = 0 - 255
        self.NeedleColor = QColor(R, G, B, Transparency)
        self.NeedleColorReleased = self.NeedleColor

        if not self.use_timer_event:
            self.update()

    def setNeedleColorOnDrag(self, R=50, G=50, B=50, Transparency=255):
        # Red: R = 0 - 255
        # Green: G = 0 - 255
        # Blue: B = 0 - 255
        # Transparency = 0 - 255
        self.NeedleColorDrag = QColor(R, G, B, Transparency)

        if not self.use_timer_event:
            self.update()

    def setScaleValueColor(self, R=50, G=50, B=50, Transparency=255):
        # Red: R = 0 - 255
        # Green: G = 0 - 255
        # Blue: B = 0 - 255
        # Transparency = 0 - 255
        self.ScaleValueColor = QColor(R, G, B, Transparency)

        if not self.use_timer_event:
            self.update()

    def setDisplayValueColor(self, R=50, G=50, B=50, Transparency=255):
        # Red: R = 0 - 255
        # Green: G = 0 - 255
        # Blue: B = 0 - 255
        # Transparency = 0 - 255
        self.DisplayValueColor = QColor(R, G, B, Transparency)

        if not self.use_timer_event:
            self.update()

    def set_CenterPointColor(self, R=50, G=50, B=50, Transparency=255):
        self.CenterPointColor = QColor(R, G, B, Transparency)

        if not self.use_timer_event:
            self.update()

    def setEnableNeedlePolygon(self, enable=True):
        self.enable_Needle_Polygon = enable

        if not self.use_timer_event:
            self.update()

    def setEnableScaleText(self, enable=True):
        self.enable_scale_text = enable

        if not self.use_timer_event:
            self.update()

    def setEnableBarGraph(self, enable=True):
        self.enableBarGraph = enable

        if not self.use_timer_event:
            self.update()

    def setEnableValueText(self, enable=True):
        self.enable_value_text = enable

        if not self.use_timer_event:
            self.update()

    def setEnableCenterPoint(self, enable=True):
        self.enable_CenterPoint = enable

        if not self.use_timer_event:
            self.update()

    def setEnableScalePolygon(self, enable=True):
        self.enable_filled_Polygon = enable

        if not self.use_timer_event:
            self.update()

    def setEnableBigScaleGrid(self, enable=True):
        self.enable_big_scaled_marker = enable

        if not self.use_timer_event:
            self.update()

    def setEnableFineScaleGrid(self, enable=True):
        self.enable_fine_scaled_marker = enable

        if not self.use_timer_event:
            self.update()

    def setScalaCount(self, count):
        if count < 1:
            count = 1
        self.scalaCount = count

        if not self.use_timer_event:
            self.update()

    def setMinValue(self, min):
        if self.value < min:
            self.value = min
        if min >= self.maxValue:
            self.minValue = self.maxValue - 1
        else:
            self.minValue = min

        if not self.use_timer_event:
            self.update()

    def setMaxValue(self, max):
        if self.value > max:
            self.value = max
        if max <= self.minValue:
            self.maxValue = self.minValue + 1
        else:
            self.maxValue = max

        if not self.use_timer_event:
            self.update()

    def setScaleStartAngle(self, value):
        # Value range in DEG: 0 - 360
        self.scale_angle_start_value = value
        # print("startFill: " + str(self.scale_angle_start_value))

        if not self.use_timer_event:
            self.update()

    def setTotalScaleAngleSize(self, value):
        self.scale_angle_size = value
        # print("stopFill: " + str(self.scale_angle_size))

        if not self.use_timer_event:
            self.update()

    def setGaugeColorOuterRadiusFactor(self, value):
        self.gauge_color_outer_radius_factor = float(value) / 1000
        # print(self.gauge_color_outer_radius_factor)

        if not self.use_timer_event:
            self.update()

    def setGaugeColorInnerRadiusFactor(self, value):
        self.gauge_color_inner_radius_factor = float(value) / 1000
        # print(self.gauge_color_inner_radius_factor)

        if not self.use_timer_event:
            self.update()

    def set_scale_polygon_colors(self, color_array):
        # print(type(color_array))
        if 'list' in str(type(color_array)):
            self.scale_polygon_colors = color_array
        elif color_array == None:
            self.scale_polygon_colors = [[.0, Qt.transparent]]
        else:
            self.scale_polygon_colors = [[.0, Qt.transparent]]

        if not self.use_timer_event:
            self.update()

    ################################################################################################
    # GET MAXIMUM VALUE
    ################################################################################################
    def get_value_max(self):
        return self.maxValue

    def create_polygon_pie(self, outer_radius, inner_raduis, start, lenght, bar_graph=True):
        polygon_pie = QPolygonF()
        # start = self.scale_angle_start_value
        # start = 0
        # lenght = self.scale_angle_size
        # lenght = 180
        # inner_raduis = self.width()/4
        # print(start)
        n = 360     # angle steps size for full circle
        # changing n value will causes drawing issues
        w = 360 / n   # angle per step
        # create outer circle line from "start"-angle to "start + lenght"-angle
        x = 0
        y = 0

        # todo enable/disable bar graf here
        if not self.enableBarGraph and bar_graph:
            # float_value = ((lenght / (self.maxValue - self.minValue)) * (self.value - self.minValue))
            lenght = int(
                round((lenght / (self.maxValue - self.minValue)) * (self.value - self.minValue)))
            # print("f: %s, l: %s" %(float_value, lenght))
            pass

        # mymax = 0

        # add the points of polygon
        for i in range(lenght + 1):
            t = w * i + start - self.angle_offset
            x = outer_radius * math.cos(math.radians(t))
            y = outer_radius * math.sin(math.radians(t))
            polygon_pie.append(QPointF(x, y))
        # create inner circle line from "start + lenght"-angle to "start"-angle
        # add the points of polygon
        for i in range(lenght + 1):
            # print("2 " + str(i))
            t = w * (lenght - i) + start - self.angle_offset
            x = inner_raduis * math.cos(math.radians(t))
            y = inner_raduis * math.sin(math.radians(t))
            polygon_pie.append(QPointF(x, y))

        # close outer line
        polygon_pie.append(QPointF(x, y))
        return polygon_pie

    def draw_filled_polygon(self, outline_pen_with=0):
        if not self.scale_polygon_colors == None:
            painter_filled_polygon = QPainter(self)
            painter_filled_polygon.setRenderHint(QPainter.Antialiasing)
            # Koordinatenursprung in die Mitte der Flaeche legen
            painter_filled_polygon.translate(
                self.width() / 2, self.height() / 2)

            painter_filled_polygon.setPen(Qt.NoPen)

            self.pen.setWidth(outline_pen_with)
            if outline_pen_with > 0:
                painter_filled_polygon.setPen(self.pen)

            colored_scale_polygon = self.create_polygon_pie(
                ((self.widget_diameter / 2) - (self.pen.width() / 2)) *
                self.gauge_color_outer_radius_factor,
                (((self.widget_diameter / 2) - (self.pen.width() / 2))
                 * self.gauge_color_inner_radius_factor),
                self.scale_angle_start_value, self.scale_angle_size)

            gauge_rect = QRect(QPoint(0, 0), QSize(
                int(self.widget_diameter / 2 - 1), int(self.widget_diameter - 1)))
            grad = QConicalGradient(QPointF(0, 0), - self.scale_angle_size - self.scale_angle_start_value +
                                    self.angle_offset - 1)

            # todo definition scale color as array here
            for eachcolor in self.scale_polygon_colors:
                grad.setColorAt(eachcolor[0], eachcolor[1])
            # grad.setColorAt(.00, Qt.red)
            # grad.setColorAt(.1, Qt.yellow)
            # grad.setColorAt(.15, Qt.green)
            # grad.setColorAt(1, Qt.transparent)
            # self.brush = QBrush(QColor(255, 0, 255, 255))
            # grad.setStyle(Qt.Dense6Pattern)
            # painter_filled_polygon.setBrush(self.brush)
            painter_filled_polygon.setBrush(grad)

            painter_filled_polygon.drawPolygon(colored_scale_polygon)
            # return painter_filled_polygon

    def draw_icon_image(self):
        pass

    def draw_big_scaled_marker(self):
        my_painter = QPainter(self)
        my_painter.setRenderHint(QPainter.Antialiasing)
        # Koordinatenursprung in die Mitte der Flaeche legen
        my_painter.translate(self.width() / 2, self.height() / 2)

        # my_painter.setPen(Qt.NoPen)
        self.pen = QPen(self.bigScaleMarker)
        self.pen.setWidth(2)
        # # if outline_pen_with > 0:
        my_painter.setPen(self.pen)

        my_painter.rotate(self.scale_angle_start_value - self.angle_offset)
        steps_size = (float(self.scale_angle_size) / float(self.scalaCount))
        scale_line_outer_start = self.widget_diameter // 2
        scale_line_lenght = int((self.widget_diameter / 2) -
                                (self.widget_diameter / 20))
        # print(stepszize)
        for i in range(self.scalaCount + 1):
            my_painter.drawLine(scale_line_lenght, 0,
                                scale_line_outer_start, 0)
            my_painter.rotate(steps_size)

    def create_scale_marker_values_text(self):
        painter = QPainter(self)
        # painter.setRenderHint(QPainter.HighQualityAntialiasing)
        painter.setRenderHint(QPainter.Antialiasing)

        # Koordinatenursprung in die Mitte der Flaeche legen
        painter.translate(self.width() / 2, self.height() / 2)
        # painter.save()
        font = QFont(self.scale_fontname, self.scale_fontsize, QFont.Bold)
        fm = QFontMetrics(font)

        pen_shadow = QPen()

        pen_shadow.setBrush(self.ScaleValueColor)
        painter.setPen(pen_shadow)

        text_radius_factor = 0.8
        text_radius = self.widget_diameter / 2 * text_radius_factor

        scale_per_div = int((self.maxValue - self.minValue) / self.scalaCount)

        angle_distance = (float(self.scale_angle_size) /
                          float(self.scalaCount))
        for i in range(self.scalaCount + 1):
            # text = str(int((self.maxValue - self.minValue) / self.scalaCount * i))
            text = str(int(self.minValue + scale_per_div * i))
            w = fm.width(text) + 1
            h = fm.height()
            painter.setFont(QFont(self.scale_fontname,
                            self.scale_fontsize, QFont.Bold))
            angle = angle_distance * i + \
                float(self.scale_angle_start_value - self.angle_offset)
            x = text_radius * math.cos(math.radians(angle))
            y = text_radius * math.sin(math.radians(angle))
            # print(w, h, x, y, text)

            painter.drawText(int(x - w / 2), int(y - h / 2), int(w),
                             int(h), Qt.AlignCenter, text)
        # painter.restore()

    def create_fine_scaled_marker(self):
        #  Description_dict = 0
        my_painter = QPainter(self)

        my_painter.setRenderHint(QPainter.Antialiasing)
        # Koordinatenursprung in die Mitte der Flaeche legen
        my_painter.translate(self.width() / 2, self.height() / 2)

        my_painter.setPen(self.fineScaleColor)
        my_painter.rotate(self.scale_angle_start_value - self.angle_offset)
        steps_size = (float(self.scale_angle_size) /
                      float(self.scalaCount * self.scala_subdiv_count))
        scale_line_outer_start = self.widget_diameter // 2
        scale_line_lenght = int(
            (self.widget_diameter / 2) - (self.widget_diameter / 40))
        for i in range((self.scalaCount * self.scala_subdiv_count) + 1):
            my_painter.drawLine(scale_line_lenght, 0,
                                scale_line_outer_start, 0)
            my_painter.rotate(steps_size)

    def create_values_text(self):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.HighQualityAntialiasing)
        # painter.setRenderHint(QPainter.Antialiasing)

        painter.translate(self.width() / 2, self.height() / 2)
        font = QFont(self.value_fontname, self.value_fontsize, QFont.Bold)
        fm = QFontMetrics(font)

        pen_shadow = QPen()

        pen_shadow.setBrush(self.DisplayValueColor)
        painter.setPen(pen_shadow)

        text_radius = self.widget_diameter / 2 * self.text_radius_factor
        text = str(int(self.value))
        w = fm.width(text) + 1
        h = fm.height()
        painter.setFont(QFont(self.value_fontname,
                        self.value_fontsize, QFont.Bold))
        angle_end = float(self.scale_angle_start_value +
                          self.scale_angle_size - 360)
        angle = (angle_end - self.scale_angle_start_value) / \
            2 + self.scale_angle_start_value

        x = text_radius * math.cos(math.radians(angle))
        y = text_radius * math.sin(math.radians(angle))
        # print(w, h, x, y, text)
        painter.drawText(int(x - w / 2), int(y - h / 2), int(w),
                         int(h), Qt.AlignCenter, text)

    def create_units_text(self):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.HighQualityAntialiasing)
        # painter.setRenderHint(QPainter.Antialiasing)

        painter.translate(self.width() / 2, self.height() / 2)
        font = QFont(self.value_fontname, int(
            self.value_fontsize / 2.5), QFont.Bold)
        fm = QFontMetrics(font)

        pen_shadow = QPen()

        pen_shadow.setBrush(self.DisplayValueColor)
        painter.setPen(pen_shadow)

        text_radius = self.widget_diameter / 2 * self.text_radius_factor

        text = str(self.units)
        w = fm.width(text) + 1
        h = fm.height()
        painter.setFont(QFont(self.value_fontname, int(
            self.value_fontsize / 2.5), QFont.Bold))

        angle_end = float(self.scale_angle_start_value +
                          self.scale_angle_size + 180)
        angle = (angle_end - self.scale_angle_start_value) / \
            2 + self.scale_angle_start_value

        x = text_radius * math.cos(math.radians(angle))
        y = text_radius * math.sin(math.radians(angle))
        # print(w, h, x, y, text)
        painter.drawText(int(x - w / 2), int(y - h / 2), int(w),
                         int(h), Qt.AlignCenter, text)


    def draw_big_needle_center_point(self, diameter=30):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.translate(self.width() / 2, self.height() / 2)
        painter.setPen(Qt.NoPen)
        colored_scale_polygon = self.create_polygon_pie(
            ((self.widget_diameter / 8) - (self.pen.width() / 2)),
            0,
            self.scale_angle_start_value, 360, False)

        grad = QConicalGradient(QPointF(0, 0), 0)

        # todo definition scale color as array here
        for eachcolor in self.needle_center_bg:
            grad.setColorAt(eachcolor[0], eachcolor[1])
        painter.setBrush(grad)

        painter.drawPolygon(colored_scale_polygon)
    def draw_outer_circle(self, diameter=30):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        painter.translate(self.width() / 2, self.height() / 2)
        painter.setPen(Qt.NoPen)
        colored_scale_polygon = self.create_polygon_pie(
            ((self.widget_diameter / 2) - (self.pen.width())),
            (self.widget_diameter / 6),
            self.scale_angle_start_value / 10, 360, False)

        radialGradient = QRadialGradient(QPointF(0, 0), self.width())

        for eachcolor in self.outer_circle_bg:
            radialGradient.setColorAt(eachcolor[0], eachcolor[1])

        painter.setBrush(radialGradient)

        painter.drawPolygon(colored_scale_polygon)

    ################################################################################################
    # NEEDLE POINTER
    ################################################################################################

    def draw_needle(self):
        painter = QPainter(self)
        # painter.setRenderHint(QtGui.QPainter.HighQualityAntialiasing)
        painter.setRenderHint(QPainter.Antialiasing)
        # Koordinatenursprung in die Mitte der Flaeche legen
        painter.translate(self.width() / 2, self.height() / 2)
        painter.setPen(Qt.NoPen)
        painter.setBrush(self.NeedleColor)
        painter.rotate(((self.value - self.value_offset - self.minValue) * self.scale_angle_size /
                        (self.maxValue - self.minValue)) + 90 + self.scale_angle_start_value)

        painter.drawConvexPolygon(self.value_needle[0])

    ###############################################################################################
    # EVENTS
    ###############################################################################################

    ################################################################################################
    # ON WINDOW RESIZE
    ################################################################################################
    def resizeEvent(self, event):
        # self.resized.emit()
        # return super(self.parent, self).resizeEvent(event)
        # print("resized")
        # print(self.width())
        self.rescale_method()
        # self.emit(QtCore.SIGNAL("resize()"))
        # print("resizeEvent")

    ################################################################################################
    # ON PAINT EVENT
    ################################################################################################
    def paintEvent(self, event):
        # Main Drawing Event:
        # Will be executed on every change
        # vgl http://doc.qt.io/qt-4.8/qt-demos-affine-xform-cpp.html
        # print("event", event)

        self.draw_outer_circle()
        self.draw_icon_image()
        # colored pie area
        if self.enable_filled_Polygon:
            self.draw_filled_polygon()

        # draw scale marker lines
        if self.enable_fine_scaled_marker:
            self.create_fine_scaled_marker()
        if self.enable_big_scaled_marker:
            self.draw_big_scaled_marker()

        # draw scale marker value text
        if self.enable_scale_text:
            self.create_scale_marker_values_text()

        # Display Value
        if self.enable_value_text:
            self.create_values_text()
            self.create_units_text()

        # draw needle 1
        if self.enable_Needle_Polygon:
            self.draw_needle()

        # Draw Center Point
        if self.enable_CenterPoint:
            self.draw_big_needle_center_point(
                diameter=(self.widget_diameter / 6))

    ###############################################################################################
    # MOUSE EVENTS
    ###############################################################################################

    def setMouseTracking(self, flag):
        def recursive_set(parent):
            for child in parent.findChildren(QObject):
                try:
                    child.setMouseTracking(flag)
                except:
                    pass
                recursive_set(child)

        QWidget.setMouseTracking(self, flag)
        recursive_set(self)

    def mouseReleaseEvent(self, QMouseEvent):
        self.NeedleColor = self.NeedleColorReleased

        if not self.use_timer_event:
            self.update()
        pass

    ########################################################################
    # MOUSE LEAVE EVENT
    ########################################################################
    def leaveEvent(self, event):
        self.NeedleColor = self.NeedleColorReleased
        self.update()

    def mouseMoveEvent(self, event):
        x, y = event.x() - (self.width() / 2), event.y() - (self.height() / 2)
        # print(event.x(), event.y(), self.width(), self.height())
        if not x == 0:
            angle = math.atan2(y, x) / math.pi * 180
            # winkellaenge der anzeige immer positiv 0 - 360deg
            # min wert + umskalierter wert
            value = (float(math.fmod(angle - self.scale_angle_start_value + 720, 360)) /
                     (float(self.scale_angle_size) / float(self.maxValue - self.minValue))) + self.minValue
            temp = value
            fmod = float(
                math.fmod(angle - self.scale_angle_start_value + 720, 360))
            state = 0
            if (self.value - (self.maxValue - self.minValue) * self.valueNeedleSnapzone) <= \
                    value <= \
                    (self.value + (self.maxValue - self.minValue) * self.valueNeedleSnapzone):
                self.NeedleColor = self.NeedleColorDrag
                # todo: evtl ueberpruefen
                #
                state = 9
                # if value >= self.maxValue and self.last_value < (self.maxValue - self.minValue) / 2:
                if value >= self.maxValue and self.last_value < (self.maxValue - self.minValue) / 2:
                    state = 1
                    value = self.maxValue
                    self.last_value = self.minValue
                    self.valueChanged.emit(int(value))

                elif value >= self.maxValue >= self.last_value:
                    state = 2
                    value = self.maxValue
                    self.last_value = self.maxValue
                    self.valueChanged.emit(int(value))

                else:
                    state = 3
                    self.last_value = value
                    self.valueChanged.emit(int(value))

                self.updateValue(value)


#!####################################################################################################################################################### AİRSPEED END

###############################################################################################################################################! ROLL START
class AnalogGauge_roll(QWidget):
    valueChanged = pyqtSignal(int)
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(100, 100)
        
        self.altTimer = QTimer()
        self.altTimer.start(10) # Saniyede bir güncelle
        self.altTimer.timeout.connect(self.update_roll)
    
    def update_roll(self):
        while True:
            gaugeRoll = vehicle.attitude.roll
            self.value= gaugeRoll
            break
        
        self.use_timer_event = False
        self.setNeedleColor(0, 0, 0, 255)
        self.NeedleColorReleased = self.NeedleColor
        self.setNeedleColorOnDrag(255, 0, 00, 255)
        self.setScaleValueColor(0, 0, 0, 255)
        self.setDisplayValueColor(0, 0, 0, 255)
        self.set_CenterPointColor(0, 0, 0, 255)
        self.value_needle_count = 1
        self.value_needle = QObject
        self.minValue = 0
        self.maxValue = 3
        self.value_offset = 0

        self.valueNeedleSnapzone = 0.05
        self.last_value = 0
        self.gauge_color_outer_radius_factor = 1
        self.gauge_color_inner_radius_factor = 0.9

        self.center_horizontal_value = 0
        self.center_vertical_value = 0

        self.scale_angle_start_value = 135
        self.scale_angle_size = 270

        self.angle_offset = 0

        self.setScalaCount(3)
        self.scala_subdiv_count = 5

        self.pen = QPen(QColor(0, 0, 0))

        QFontDatabase.addApplicationFont(os.path.join(os.path.dirname(
            __file__), 'fonts/Orbitron/Orbitron-VariableFont_wght.ttf'))

        self.scale_polygon_colors = []

        self.bigScaleMarker = Qt.black

        self.fineScaleColor = Qt.black

        self.setEnableScaleText(True)
        self.scale_fontname = "Orbitron"
        self.initial_scale_fontsize = 14
        self.scale_fontsize = self.initial_scale_fontsize
        self.enable_value_text = True
        self.value_fontname = "Orbitron"
        self.initial_value_fontsize = 40
        self.value_fontsize = self.initial_value_fontsize
        self.text_radius_factor = 0.5
        self.setEnableBarGraph(True)
        self.setEnableScalePolygon(True)
        self.enable_CenterPoint = True
        self.enable_fine_scaled_marker = True
        self.enable_big_scaled_marker = True
        self.needle_scale_factor = 0.8
        self.enable_Needle_Polygon = True

        self.setMouseTracking(False)
        self.units = "m/s"

        # QTimer sorgt für neu Darstellung alle X ms
        # evtl performance hier verbessern mit self.update() und self.use_timer_event = False
        # todo: self.update als default ohne ueberpruefung, ob self.use_timer_event gesetzt ist oder nicht
        # Timer startet alle 10ms das event paintEvent
        if self.use_timer_event:
            timer = QTimer(self)
            timer.timeout.connect(self.update)
            timer.start(10)
        else:
            self.update()

        self.setGaugeTheme(0)

        self.rescale_method()

    def setScaleFontFamily(self, font):
        self.scale_fontname = str(font)

    def setValueFontFamily(self, font):
        self.value_fontname = str(font)

    def setBigScaleColor(self, color):
        self.bigScaleMarker = QColor(color)

    def setFineScaleColor(self, color):
        self.fineScaleColor = QColor(color)

    def setGaugeTheme(self, Theme=1):
        if Theme == 0 or Theme == None:
            self.set_scale_polygon_colors([[.00, Qt.red],
                                           [.1, Qt.yellow],
                                           [.15, Qt.green],
                                           [1, Qt.transparent]])

            self.needle_center_bg = [
                                    [0, QColor(35, 40, 3, 255)],
                                    [0.16, QColor(30, 36, 45, 255)],
                                    [0.225, QColor(36, 42, 54, 255)],
                                    [0.423963, QColor(19, 23, 29, 255)],
                                    [0.580645, QColor(45, 53, 68, 255)],
                                    [0.792627, QColor(59, 70, 88, 255)],
                                    [0.935, QColor(30, 35, 45, 255)],
                                    [1, QColor(35, 40, 3, 255)]
            ]

            self.outer_circle_bg = [
                [0.0645161, QColor(30, 35, 45, 255)],
                [0.37788, QColor(57, 67, 86, 255)],
                [1, QColor(30, 36, 45, 255)]
            ]

        if Theme == 1:
            self.set_scale_polygon_colors([[.75, Qt.red],
                                           [.5, Qt.yellow],
                                           [.25, Qt.green]])

            self.needle_center_bg = [
                                    [0, QColor(35, 40, 3, 255)],
                                    [0.16, QColor(30, 36, 45, 255)],
                                    [0.225, QColor(36, 42, 54, 255)],
                                    [0.423963, QColor(19, 23, 29, 255)],
                                    [0.580645, QColor(45, 53, 68, 255)],
                                    [0.792627, QColor(59, 70, 88, 255)],
                                    [0.935, QColor(30, 35, 45, 255)],
                                    [1, QColor(35, 40, 3, 255)]
            ]

            self.outer_circle_bg = [
                [0.0645161, QColor(30, 35, 45, 255)],
                [0.37788, QColor(57, 67, 86, 255)],
                [1, QColor(30, 36, 45, 255)]
            ]

        if Theme == 2:
            self.set_scale_polygon_colors([[.25, Qt.red],
                                           [.5, Qt.yellow],
                                           [.75, Qt.green]])

            self.needle_center_bg = [
                                    [0, QColor(35, 40, 3, 255)],
                                    [0.16, QColor(30, 36, 45, 255)],
                                    [0.225, QColor(36, 42, 54, 255)],
                                    [0.423963, QColor(19, 23, 29, 255)],
                                    [0.580645, QColor(45, 53, 68, 255)],
                                    [0.792627, QColor(59, 70, 88, 255)],
                                    [0.935, QColor(30, 35, 45, 255)],
                                    [1, QColor(35, 40, 3, 255)]
            ]

            self.outer_circle_bg = [
                [0.0645161, QColor(30, 35, 45, 255)],
                [0.37788, QColor(57, 67, 86, 255)],
                [1, QColor(30, 36, 45, 255)]
            ]

        elif Theme == 3:
            self.set_scale_polygon_colors([[.00, Qt.white]])

            self.needle_center_bg = [
                                    [0, Qt.white],
            ]

            self.outer_circle_bg = [
                [0, Qt.white],
            ]

            self.bigScaleMarker = Qt.black
            self.fineScaleColor = Qt.black

        elif Theme == 4:
            self.set_scale_polygon_colors([[1, Qt.black]])

            self.needle_center_bg = [
                                    [0, Qt.black],
            ]

            self.outer_circle_bg = [
                [0, Qt.black],
            ]

            self.bigScaleMarker = Qt.white
            self.fineScaleColor = Qt.white

        elif Theme == 5:
            self.set_scale_polygon_colors([[1, QColor("#029CDE")]])

            self.needle_center_bg = [
                                    [0, QColor("#029CDE")],
            ]

            self.outer_circle_bg = [
                [0, QColor("#029CDE")],
            ]

        elif Theme == 6:
            self.set_scale_polygon_colors([[.75, QColor("#01ADEF")],
                                           [.5, QColor("#0086BF")],
                                           [.25, QColor("#005275")]])

            self.needle_center_bg = [
                                    [0, QColor(0, 46, 61, 255)],
                                    [0.322581, QColor(1, 173, 239, 255)],
                                    [0.571429, QColor(0, 73, 99, 255)],
                                    [1, QColor(0, 46, 61, 255)]
            ]

            self.outer_circle_bg = [
                [0.0645161, QColor(0, 85, 116, 255)],
                [0.37788, QColor(1, 173, 239, 255)],
                [1, QColor(0, 69, 94, 255)]
            ]

            self.bigScaleMarker = Qt.black
            self.fineScaleColor = Qt.black

        elif Theme == 7:
            self.set_scale_polygon_colors([[.25, QColor("#01ADEF")],
                                           [.5, QColor("#0086BF")],
                                           [.75, QColor("#005275")]])

            self.needle_center_bg = [
                                    [0, QColor(0, 46, 61, 255)],
                                    [0.322581, QColor(1, 173, 239, 255)],
                                    [0.571429, QColor(0, 73, 99, 255)],
                                    [1, QColor(0, 46, 61, 255)]
            ]

            self.outer_circle_bg = [
                [0.0645161, QColor(0, 85, 116, 255)],
                [0.37788, QColor(1, 173, 239, 255)],
                [1, QColor(0, 69, 94, 255)]
            ]

            self.bigScaleMarker = Qt.black
            self.fineScaleColor = Qt.black

        elif Theme == 8:
            self.setCustomGaugeTheme(
                color1="#ffaa00",
                color2="#7d5300",
                color3="#3e2900"
            )

            self.bigScaleMarker = Qt.black
            self.fineScaleColor = Qt.black

        elif Theme == 9:
            self.setCustomGaugeTheme(
                color1="#3e2900",
                color2="#7d5300",
                color3="#ffaa00"
            )

            self.bigScaleMarker = Qt.white
            self.fineScaleColor = Qt.white

        elif Theme == 10:
            self.setCustomGaugeTheme(
                color1="#ff007f",
                color2="#aa0055",
                color3="#830042"
            )

            self.bigScaleMarker = Qt.black
            self.fineScaleColor = Qt.black

        elif Theme == 11:
            self.setCustomGaugeTheme(
                color1="#830042",
                color2="#aa0055",
                color3="#ff007f"
            )

            self.bigScaleMarker = Qt.white
            self.fineScaleColor = Qt.white

        elif Theme == 12:
            self.setCustomGaugeTheme(
                color1="#ffe75d",
                color2="#896c1a",
                color3="#232803"
            )

            self.bigScaleMarker = Qt.black
            self.fineScaleColor = Qt.black

        elif Theme == 13:
            self.setCustomGaugeTheme(
                color1="#ffe75d",
                color2="#896c1a",
                color3="#232803"
            )

            self.bigScaleMarker = Qt.black
            self.fineScaleColor = Qt.black

        elif Theme == 14:
            self.setCustomGaugeTheme(
                color1="#232803",
                color2="#821600",
                color3="#ffe75d"
            )

            self.bigScaleMarker = Qt.white
            self.fineScaleColor = Qt.white

        elif Theme == 15:
            self.setCustomGaugeTheme(
                color1="#00FF11",
                color2="#00990A",
                color3="#002603"
            )

            self.bigScaleMarker = Qt.black
            self.fineScaleColor = Qt.black

        elif Theme == 16:
            self.setCustomGaugeTheme(
                color1="#002603",
                color2="#00990A",
                color3="#00FF11"
            )

            self.bigScaleMarker = Qt.white
            self.fineScaleColor = Qt.white

        elif Theme == 17:
            self.setCustomGaugeTheme(
                color1="#00FFCC",
                color2="#00876C",
                color3="#00211B"
            )

            self.bigScaleMarker = Qt.black
            self.fineScaleColor = Qt.black

        elif Theme == 18:
            self.setCustomGaugeTheme(
                color1="#00211B",
                color2="#00876C",
                color3="#00FFCC"
            )

            self.bigScaleMarker = Qt.white
            self.fineScaleColor = Qt.white

        elif Theme == 19:
            self.setCustomGaugeTheme(
                color1="#001EFF",
                color2="#001299",
                color3="#000426"
            )

            self.bigScaleMarker = Qt.black
            self.fineScaleColor = Qt.black

        elif Theme == 20:
            self.setCustomGaugeTheme(
                color1="#000426",
                color2="#001299",
                color3="#001EFF"
            )

            self.bigScaleMarker = Qt.white
            self.fineScaleColor = Qt.white

        elif Theme == 21:
            self.setCustomGaugeTheme(
                color1="#F200FF",
                color2="#85008C",
                color3="#240026"
            )

            self.bigScaleMarker = Qt.black
            self.fineScaleColor = Qt.black

        elif Theme == 22:
            self.setCustomGaugeTheme(
                color1="#240026",
                color2="#85008C",
                color3="#F200FF"
            )

            self.bigScaleMarker = Qt.white
            self.fineScaleColor = Qt.white

        elif Theme == 23:
            self.setCustomGaugeTheme(
                color1="#FF0022",
                color2="#080001",
                color3="#009991"
            )

            self.bigScaleMarker = Qt.white
            self.fineScaleColor = Qt.white

        elif Theme == 24:
            self.setCustomGaugeTheme(
                color1="#009991",
                color2="#080001",
                color3="#FF0022"
            )

            self.bigScaleMarker = Qt.white
            self.fineScaleColor = Qt.white

    def setCustomGaugeTheme(self, **colors):
        if "color1" in colors and len(str(colors['color1'])) > 0:
            if "color2" in colors and len(str(colors['color2'])) > 0:
                if "color3" in colors and len(str(colors['color3'])) > 0:

                    self.set_scale_polygon_colors([[.25, QColor(str(colors['color1']))],
                                                   [.5, QColor(
                                                       str(colors['color2']))],
                                                   [.75, QColor(str(colors['color3']))]])

                    self.needle_center_bg = [
                                            [0, QColor(str(colors['color3']))],
                                            [0.322581, QColor(
                                                str(colors['color1']))],
                                            [0.571429, QColor(
                                                str(colors['color2']))],
                                            [1, QColor(str(colors['color3']))]
                    ]

                    self.outer_circle_bg = [
                        [0.0645161, QColor(str(colors['color3']))],
                        [0.36, QColor(
                            str(colors['color1']))],
                        [1, QColor(str(colors['color2']))]
                    ]

                else:

                    self.set_scale_polygon_colors([[.5, QColor(str(colors['color1']))],
                                                   [1, QColor(str(colors['color2']))]])

                    self.needle_center_bg = [
                                            [0, QColor(str(colors['color2']))],
                                            [1, QColor(str(colors['color1']))]
                    ]

                    self.outer_circle_bg = [
                        [0, QColor(str(colors['color2']))],
                        [1, QColor(str(colors['color2']))]
                    ]

            else:

                self.set_scale_polygon_colors(
                    [[1, QColor(str(colors['color1']))]])

                self.needle_center_bg = [
                                        [1, QColor(str(colors['color1']))]
                ]

                self.outer_circle_bg = [
                    [1, QColor(str(colors['color1']))]
                ]

        else:

            self.setGaugeTheme(0)
            print("color1 is not defined")

    def setScalePolygonColor(self, **colors):
        if "color1" in colors and len(str(colors['color1'])) > 0:
            if "color2" in colors and len(str(colors['color2'])) > 0:
                if "color3" in colors and len(str(colors['color3'])) > 0:

                    self.set_scale_polygon_colors([[.25, QColor(str(colors['color1']))],
                                                   [.5, QColor(
                                                       str(colors['color2']))],
                                                   [.75, QColor(str(colors['color3']))]])

                else:

                    self.set_scale_polygon_colors([[.5, QColor(str(colors['color1']))],
                                                   [1, QColor(str(colors['color2']))]])

            else:

                self.set_scale_polygon_colors(
                    [[1, QColor(str(colors['color1']))]])

        else:
            print("color1 is not defined")

    def setNeedleCenterColor(self, **colors):
        if "color1" in colors and len(str(colors['color1'])) > 0:
            if "color2" in colors and len(str(colors['color2'])) > 0:
                if "color3" in colors and len(str(colors['color3'])) > 0:

                    self.needle_center_bg = [
                                            [0, QColor(str(colors['color3']))],
                                            [0.322581, QColor(
                                                str(colors['color1']))],
                                            [0.571429, QColor(
                                                str(colors['color2']))],
                                            [1, QColor(str(colors['color3']))]
                    ]

                else:

                    self.needle_center_bg = [
                                            [0, QColor(str(colors['color2']))],
                                            [1, QColor(str(colors['color1']))]
                    ]

            else:

                self.needle_center_bg = [
                                        [1, QColor(str(colors['color1']))]
                ]
        else:
            print("color1 is not defined")

    def setOuterCircleColor(self, **colors):
        if "color1" in colors and len(str(colors['color1'])) > 0:
            if "color2" in colors and len(str(colors['color2'])) > 0:
                if "color3" in colors and len(str(colors['color3'])) > 0:

                    self.outer_circle_bg = [
                        [0.0645161, QColor(str(colors['color3']))],
                        [0.37788, QColor(
                            str(colors['color1']))],
                        [1, QColor(str(colors['color2']))]
                    ]

                else:

                    self.outer_circle_bg = [
                        [0, QColor(str(colors['color2']))],
                        [1, QColor(str(colors['color2']))]
                    ]

            else:

                self.outer_circle_bg = [
                    [1, QColor(str(colors['color1']))]
                ]

        else:
            print("color1 is not defined")

    def rescale_method(self):
        if self.width() <= self.height():
            self.widget_diameter = self.width()
        else:
            self.widget_diameter = self.height()
        self.change_value_needle_style([QPolygon([
            QPoint(4, 30),
            QPoint(-4, 30),
            QPoint(-2, int(- self.widget_diameter / 2 * self.needle_scale_factor)),
            QPoint(0, int(- self.widget_diameter /
                   2 * self.needle_scale_factor - 6)),
            QPoint(2, int(- self.widget_diameter / 2 * self.needle_scale_factor))
        ])])

        self.scale_fontsize = int(
            self.initial_scale_fontsize * self.widget_diameter / 400)
        self.value_fontsize = int(
            self.initial_value_fontsize * self.widget_diameter / 400)

    def change_value_needle_style(self, design):
        # prepared for multiple needle instrument
        self.value_needle = []
        for i in design:
            self.value_needle.append(i)
        if not self.use_timer_event:
            self.update()

    def updateValue(self, value, mouse_controlled=False):
        # if not mouse_controlled:
        #     self.value = value
        #
        # if mouse_controlled:
        #     self.valueChanged.emit(int(value))

        if value <= self.minValue:
            self.value = self.minValue
        elif value >= self.maxValue:
            self.value = self.maxValue
        else:
            self.value = value
        # self.paintEvent("")
        self.valueChanged.emit(int(value))
        # print(self.value)

        # ohne timer: aktiviere self.update()
        if not self.use_timer_event:
            self.update()

    def updateAngleOffset(self, offset):
        self.angle_offset = offset
        if not self.use_timer_event:
            self.update()

    def center_horizontal(self, value):
        self.center_horizontal_value = value
        # print("horizontal: " + str(self.center_horizontal_value))

    def center_vertical(self, value):
        self.center_vertical_value = value
        # print("vertical: " + str(self.center_vertical_value))

    def setNeedleColor(self, R=50, G=50, B=50, Transparency=255):
        # Red: R = 0 - 255
        # Green: G = 0 - 255
        # Blue: B = 0 - 255
        # Transparency = 0 - 255
        self.NeedleColor = QColor(R, G, B, Transparency)
        self.NeedleColorReleased = self.NeedleColor

        if not self.use_timer_event:
            self.update()

    def setNeedleColorOnDrag(self, R=50, G=50, B=50, Transparency=255):
        # Red: R = 0 - 255
        # Green: G = 0 - 255
        # Blue: B = 0 - 255
        # Transparency = 0 - 255
        self.NeedleColorDrag = QColor(R, G, B, Transparency)

        if not self.use_timer_event:
            self.update()

    def setScaleValueColor(self, R=50, G=50, B=50, Transparency=255):
        # Red: R = 0 - 255
        # Green: G = 0 - 255
        # Blue: B = 0 - 255
        # Transparency = 0 - 255
        self.ScaleValueColor = QColor(R, G, B, Transparency)

        if not self.use_timer_event:
            self.update()

    def setDisplayValueColor(self, R=50, G=50, B=50, Transparency=255):
        # Red: R = 0 - 255
        # Green: G = 0 - 255
        # Blue: B = 0 - 255
        # Transparency = 0 - 255
        self.DisplayValueColor = QColor(R, G, B, Transparency)

        if not self.use_timer_event:
            self.update()

    def set_CenterPointColor(self, R=50, G=50, B=50, Transparency=255):
        self.CenterPointColor = QColor(R, G, B, Transparency)

        if not self.use_timer_event:
            self.update()

    def setEnableNeedlePolygon(self, enable=True):
        self.enable_Needle_Polygon = enable

        if not self.use_timer_event:
            self.update()

    def setEnableScaleText(self, enable=True):
        self.enable_scale_text = enable

        if not self.use_timer_event:
            self.update()

    def setEnableBarGraph(self, enable=True):
        self.enableBarGraph = enable

        if not self.use_timer_event:
            self.update()

    def setEnableValueText(self, enable=True):
        self.enable_value_text = enable

        if not self.use_timer_event:
            self.update()

    def setEnableCenterPoint(self, enable=True):
        self.enable_CenterPoint = enable

        if not self.use_timer_event:
            self.update()

    def setEnableScalePolygon(self, enable=True):
        self.enable_filled_Polygon = enable

        if not self.use_timer_event:
            self.update()

    def setEnableBigScaleGrid(self, enable=True):
        self.enable_big_scaled_marker = enable

        if not self.use_timer_event:
            self.update()

    def setEnableFineScaleGrid(self, enable=True):
        self.enable_fine_scaled_marker = enable

        if not self.use_timer_event:
            self.update()

    def setScalaCount(self, count):
        if count < 1:
            count = 1
        self.scalaCount = count

        if not self.use_timer_event:
            self.update()

    def setMinValue(self, min):
        if self.value < min:
            self.value = min
        if min >= self.maxValue:
            self.minValue = self.maxValue - 1
        else:
            self.minValue = min

        if not self.use_timer_event:
            self.update()

    def setMaxValue(self, max):
        if self.value > max:
            self.value = max
        if max <= self.minValue:
            self.maxValue = self.minValue + 1
        else:
            self.maxValue = max

        if not self.use_timer_event:
            self.update()

    def setScaleStartAngle(self, value):
        # Value range in DEG: 0 - 360
        self.scale_angle_start_value = value
        # print("startFill: " + str(self.scale_angle_start_value))

        if not self.use_timer_event:
            self.update()

    def setTotalScaleAngleSize(self, value):
        self.scale_angle_size = value
        # print("stopFill: " + str(self.scale_angle_size))

        if not self.use_timer_event:
            self.update()

    def setGaugeColorOuterRadiusFactor(self, value):
        self.gauge_color_outer_radius_factor = float(value) / 1000
        # print(self.gauge_color_outer_radius_factor)

        if not self.use_timer_event:
            self.update()

    def setGaugeColorInnerRadiusFactor(self, value):
        self.gauge_color_inner_radius_factor = float(value) / 1000
        # print(self.gauge_color_inner_radius_factor)

        if not self.use_timer_event:
            self.update()

    def set_scale_polygon_colors(self, color_array):
        # print(type(color_array))
        if 'list' in str(type(color_array)):
            self.scale_polygon_colors = color_array
        elif color_array == None:
            self.scale_polygon_colors = [[.0, Qt.transparent]]
        else:
            self.scale_polygon_colors = [[.0, Qt.transparent]]

        if not self.use_timer_event:
            self.update()

    ################################################################################################
    # GET MAXIMUM VALUE
    ################################################################################################
    def get_value_max(self):
        return self.maxValue

    def create_polygon_pie(self, outer_radius, inner_raduis, start, lenght, bar_graph=True):
        polygon_pie = QPolygonF()
        # start = self.scale_angle_start_value
        # start = 0
        # lenght = self.scale_angle_size
        # lenght = 180
        # inner_raduis = self.width()/4
        # print(start)
        n = 360     # angle steps size for full circle
        # changing n value will causes drawing issues
        w = 360 / n   # angle per step
        # create outer circle line from "start"-angle to "start + lenght"-angle
        x = 0
        y = 0

        # todo enable/disable bar graf here
        if not self.enableBarGraph and bar_graph:
            # float_value = ((lenght / (self.maxValue - self.minValue)) * (self.value - self.minValue))
            lenght = int(
                round((lenght / (self.maxValue - self.minValue)) * (self.value - self.minValue)))
            # print("f: %s, l: %s" %(float_value, lenght))
            pass

        # mymax = 0

        # add the points of polygon
        for i in range(lenght + 1):
            t = w * i + start - self.angle_offset
            x = outer_radius * math.cos(math.radians(t))
            y = outer_radius * math.sin(math.radians(t))
            polygon_pie.append(QPointF(x, y))
        # create inner circle line from "start + lenght"-angle to "start"-angle
        # add the points of polygon
        for i in range(lenght + 1):
            # print("2 " + str(i))
            t = w * (lenght - i) + start - self.angle_offset
            x = inner_raduis * math.cos(math.radians(t))
            y = inner_raduis * math.sin(math.radians(t))
            polygon_pie.append(QPointF(x, y))

        # close outer line
        polygon_pie.append(QPointF(x, y))
        return polygon_pie

    def draw_filled_polygon(self, outline_pen_with=0):
        if not self.scale_polygon_colors == None:
            painter_filled_polygon = QPainter(self)
            painter_filled_polygon.setRenderHint(QPainter.Antialiasing)
            # Koordinatenursprung in die Mitte der Flaeche legen
            painter_filled_polygon.translate(
                self.width() / 2, self.height() / 2)

            painter_filled_polygon.setPen(Qt.NoPen)

            self.pen.setWidth(outline_pen_with)
            if outline_pen_with > 0:
                painter_filled_polygon.setPen(self.pen)

            colored_scale_polygon = self.create_polygon_pie(
                ((self.widget_diameter / 2) - (self.pen.width() / 2)) *
                self.gauge_color_outer_radius_factor,
                (((self.widget_diameter / 2) - (self.pen.width() / 2))
                 * self.gauge_color_inner_radius_factor),
                self.scale_angle_start_value, self.scale_angle_size)

            gauge_rect = QRect(QPoint(0, 0), QSize(
                int(self.widget_diameter / 2 - 1), int(self.widget_diameter - 1)))
            grad = QConicalGradient(QPointF(0, 0), - self.scale_angle_size - self.scale_angle_start_value +
                                    self.angle_offset - 1)

            # todo definition scale color as array here
            for eachcolor in self.scale_polygon_colors:
                grad.setColorAt(eachcolor[0], eachcolor[1])
            # grad.setColorAt(.00, Qt.red)
            # grad.setColorAt(.1, Qt.yellow)
            # grad.setColorAt(.15, Qt.green)
            # grad.setColorAt(1, Qt.transparent)
            # self.brush = QBrush(QColor(255, 0, 255, 255))
            # grad.setStyle(Qt.Dense6Pattern)
            # painter_filled_polygon.setBrush(self.brush)
            painter_filled_polygon.setBrush(grad)

            painter_filled_polygon.drawPolygon(colored_scale_polygon)
            # return painter_filled_polygon

    def draw_icon_image(self):
        pass

    def draw_big_scaled_marker(self):
        my_painter = QPainter(self)
        my_painter.setRenderHint(QPainter.Antialiasing)
        # Koordinatenursprung in die Mitte der Flaeche legen
        my_painter.translate(self.width() / 2, self.height() / 2)

        # my_painter.setPen(Qt.NoPen)
        self.pen = QPen(self.bigScaleMarker)
        self.pen.setWidth(2)
        # # if outline_pen_with > 0:
        my_painter.setPen(self.pen)

        my_painter.rotate(self.scale_angle_start_value - self.angle_offset)
        steps_size = (float(self.scale_angle_size) / float(self.scalaCount))
        scale_line_outer_start = self.widget_diameter // 2
        scale_line_lenght = int((self.widget_diameter / 2) -
                                (self.widget_diameter / 20))
        # print(stepszize)
        for i in range(self.scalaCount + 1):
            my_painter.drawLine(scale_line_lenght, 0,
                                scale_line_outer_start, 0)
            my_painter.rotate(steps_size)

    def create_scale_marker_values_text(self):
        painter = QPainter(self)
        # painter.setRenderHint(QPainter.HighQualityAntialiasing)
        painter.setRenderHint(QPainter.Antialiasing)

        # Koordinatenursprung in die Mitte der Flaeche legen
        painter.translate(self.width() / 2, self.height() / 2)
        # painter.save()
        font = QFont(self.scale_fontname, self.scale_fontsize, QFont.Bold)
        fm = QFontMetrics(font)

        pen_shadow = QPen()

        pen_shadow.setBrush(self.ScaleValueColor)
        painter.setPen(pen_shadow)

        text_radius_factor = 0.8
        text_radius = self.widget_diameter / 2 * text_radius_factor

        scale_per_div = int((self.maxValue - self.minValue) / self.scalaCount)

        angle_distance = (float(self.scale_angle_size) /
                          float(self.scalaCount))
        for i in range(self.scalaCount + 1):
            # text = str(int((self.maxValue - self.minValue) / self.scalaCount * i))
            text = str(int(self.minValue + scale_per_div * i))
            w = fm.width(text) + 1
            h = fm.height()
            painter.setFont(QFont(self.scale_fontname,
                            self.scale_fontsize, QFont.Bold))
            angle = angle_distance * i + \
                float(self.scale_angle_start_value - self.angle_offset)
            x = text_radius * math.cos(math.radians(angle))
            y = text_radius * math.sin(math.radians(angle))
            # print(w, h, x, y, text)

            painter.drawText(int(x - w / 2), int(y - h / 2), int(w),
                             int(h), Qt.AlignCenter, text)
        # painter.restore()

    def create_fine_scaled_marker(self):
        #  Description_dict = 0
        my_painter = QPainter(self)

        my_painter.setRenderHint(QPainter.Antialiasing)
        # Koordinatenursprung in die Mitte der Flaeche legen
        my_painter.translate(self.width() / 2, self.height() / 2)

        my_painter.setPen(self.fineScaleColor)
        my_painter.rotate(self.scale_angle_start_value - self.angle_offset)
        steps_size = (float(self.scale_angle_size) /
                      float(self.scalaCount * self.scala_subdiv_count))
        scale_line_outer_start = self.widget_diameter // 2
        scale_line_lenght = int(
            (self.widget_diameter / 2) - (self.widget_diameter / 40))
        for i in range((self.scalaCount * self.scala_subdiv_count) + 1):
            my_painter.drawLine(scale_line_lenght, 0,
                                scale_line_outer_start, 0)
            my_painter.rotate(steps_size)

    def create_values_text(self):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.HighQualityAntialiasing)
        # painter.setRenderHint(QPainter.Antialiasing)

        painter.translate(self.width() / 2, self.height() / 2)
        font = QFont(self.value_fontname, self.value_fontsize, QFont.Bold)
        fm = QFontMetrics(font)

        pen_shadow = QPen()

        pen_shadow.setBrush(self.DisplayValueColor)
        painter.setPen(pen_shadow)

        text_radius = self.widget_diameter / 2 * self.text_radius_factor
        text = str(int(self.value))
        w = fm.width(text) + 1
        h = fm.height()
        painter.setFont(QFont(self.value_fontname,
                        self.value_fontsize, QFont.Bold))
        angle_end = float(self.scale_angle_start_value +
                          self.scale_angle_size - 360)
        angle = (angle_end - self.scale_angle_start_value) / \
            2 + self.scale_angle_start_value

        x = text_radius * math.cos(math.radians(angle))
        y = text_radius * math.sin(math.radians(angle))
        # print(w, h, x, y, text)
        painter.drawText(int(x - w / 2), int(y - h / 2), int(w),
                         int(h), Qt.AlignCenter, text)

    def create_units_text(self):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.HighQualityAntialiasing)
        # painter.setRenderHint(QPainter.Antialiasing)

        painter.translate(self.width() / 2, self.height() / 2)
        font = QFont(self.value_fontname, int(
            self.value_fontsize / 2.5), QFont.Bold)
        fm = QFontMetrics(font)

        pen_shadow = QPen()

        pen_shadow.setBrush(self.DisplayValueColor)
        painter.setPen(pen_shadow)

        text_radius = self.widget_diameter / 2 * self.text_radius_factor

        text = str(self.units)
        w = fm.width(text) + 1
        h = fm.height()
        painter.setFont(QFont(self.value_fontname, int(
            self.value_fontsize / 2.5), QFont.Bold))

        angle_end = float(self.scale_angle_start_value +
                          self.scale_angle_size + 180)
        angle = (angle_end - self.scale_angle_start_value) / \
            2 + self.scale_angle_start_value

        x = text_radius * math.cos(math.radians(angle))
        y = text_radius * math.sin(math.radians(angle))
        # print(w, h, x, y, text)
        painter.drawText(int(x - w / 2), int(y - h / 2), int(w),
                         int(h), Qt.AlignCenter, text)


    def draw_big_needle_center_point(self, diameter=30):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.translate(self.width() / 2, self.height() / 2)
        painter.setPen(Qt.NoPen)
        colored_scale_polygon = self.create_polygon_pie(
            ((self.widget_diameter / 8) - (self.pen.width() / 2)),
            0,
            self.scale_angle_start_value, 360, False)

        grad = QConicalGradient(QPointF(0, 0), 0)

        # todo definition scale color as array here
        for eachcolor in self.needle_center_bg:
            grad.setColorAt(eachcolor[0], eachcolor[1])
        painter.setBrush(grad)

        painter.drawPolygon(colored_scale_polygon)
    def draw_outer_circle(self, diameter=30):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        painter.translate(self.width() / 2, self.height() / 2)
        painter.setPen(Qt.NoPen)
        colored_scale_polygon = self.create_polygon_pie(
            ((self.widget_diameter / 2) - (self.pen.width())),
            (self.widget_diameter / 6),
            self.scale_angle_start_value / 10, 360, False)

        radialGradient = QRadialGradient(QPointF(0, 0), self.width())

        for eachcolor in self.outer_circle_bg:
            radialGradient.setColorAt(eachcolor[0], eachcolor[1])

        painter.setBrush(radialGradient)

        painter.drawPolygon(colored_scale_polygon)

    ################################################################################################
    # NEEDLE POINTER
    ################################################################################################

    def draw_needle(self):
        painter = QPainter(self)
        # painter.setRenderHint(QtGui.QPainter.HighQualityAntialiasing)
        painter.setRenderHint(QPainter.Antialiasing)
        # Koordinatenursprung in die Mitte der Flaeche legen
        painter.translate(self.width() / 2, self.height() / 2)
        painter.setPen(Qt.NoPen)
        painter.setBrush(self.NeedleColor)
        painter.rotate(((self.value - self.value_offset - self.minValue) * self.scale_angle_size /
                        (self.maxValue - self.minValue)) + 90 + self.scale_angle_start_value)

        painter.drawConvexPolygon(self.value_needle[0])

    ###############################################################################################
    # EVENTS
    ###############################################################################################

    ################################################################################################
    # ON WINDOW RESIZE
    ################################################################################################
    def resizeEvent(self, event):
        # self.resized.emit()
        # return super(self.parent, self).resizeEvent(event)
        # print("resized")
        # print(self.width())
        self.rescale_method()
        # self.emit(QtCore.SIGNAL("resize()"))
        # print("resizeEvent")

    ################################################################################################
    # ON PAINT EVENT
    ################################################################################################
    def paintEvent(self, event):
        # Main Drawing Event:
        # Will be executed on every change
        # vgl http://doc.qt.io/qt-4.8/qt-demos-affine-xform-cpp.html
        # print("event", event)

        self.draw_outer_circle()
        self.draw_icon_image()
        # colored pie area
        if self.enable_filled_Polygon:
            self.draw_filled_polygon()

        # draw scale marker lines
        if self.enable_fine_scaled_marker:
            self.create_fine_scaled_marker()
        if self.enable_big_scaled_marker:
            self.draw_big_scaled_marker()

        # draw scale marker value text
        if self.enable_scale_text:
            self.create_scale_marker_values_text()

        # Display Value
        if self.enable_value_text:
            self.create_values_text()
            self.create_units_text()

        # draw needle 1
        if self.enable_Needle_Polygon:
            self.draw_needle()

        # Draw Center Point
        if self.enable_CenterPoint:
            self.draw_big_needle_center_point(
                diameter=(self.widget_diameter / 6))

    ###############################################################################################
    # MOUSE EVENTS
    ###############################################################################################

    def setMouseTracking(self, flag):
        def recursive_set(parent):
            for child in parent.findChildren(QObject):
                try:
                    child.setMouseTracking(flag)
                except:
                    pass
                recursive_set(child)

        QWidget.setMouseTracking(self, flag)
        recursive_set(self)

    def mouseReleaseEvent(self, QMouseEvent):
        self.NeedleColor = self.NeedleColorReleased

        if not self.use_timer_event:
            self.update()
        pass

    ########################################################################
    # MOUSE LEAVE EVENT
    ########################################################################
    def leaveEvent(self, event):
        self.NeedleColor = self.NeedleColorReleased
        self.update()

    def mouseMoveEvent(self, event):
        x, y = event.x() - (self.width() / 2), event.y() - (self.height() / 2)
        # print(event.x(), event.y(), self.width(), self.height())
        if not x == 0:
            angle = math.atan2(y, x) / math.pi * 180
            # winkellaenge der anzeige immer positiv 0 - 360deg
            # min wert + umskalierter wert
            value = (float(math.fmod(angle - self.scale_angle_start_value + 720, 360)) /
                     (float(self.scale_angle_size) / float(self.maxValue - self.minValue))) + self.minValue
            temp = value
            fmod = float(
                math.fmod(angle - self.scale_angle_start_value + 720, 360))
            state = 0
            if (self.value - (self.maxValue - self.minValue) * self.valueNeedleSnapzone) <= \
                    value <= \
                    (self.value + (self.maxValue - self.minValue) * self.valueNeedleSnapzone):
                self.NeedleColor = self.NeedleColorDrag
                # todo: evtl ueberpruefen
                #
                state = 9
                # if value >= self.maxValue and self.last_value < (self.maxValue - self.minValue) / 2:
                if value >= self.maxValue and self.last_value < (self.maxValue - self.minValue) / 2:
                    state = 1
                    value = self.maxValue
                    self.last_value = self.minValue
                    self.valueChanged.emit(int(value))

                elif value >= self.maxValue >= self.last_value:
                    state = 2
                    value = self.maxValue
                    self.last_value = self.maxValue
                    self.valueChanged.emit(int(value))

                else:
                    state = 3
                    self.last_value = value
                    self.valueChanged.emit(int(value))

                self.updateValue(value)


#!####################################################################################################################################################### VELOCİTY END

###############################################################################################################################################! YAW START
class AnalogGauge_yaw(QWidget):
    valueChanged = pyqtSignal(int)
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(100, 100)
        
        self.altTimer = QTimer()
        self.altTimer.start(10) # Saniyede bir güncelle
        self.altTimer.timeout.connect(self.update_yaw)
    
    def update_yaw(self):
        while True:
            gaugeYaw = vehicle.attitude.yaw
            self.value= gaugeYaw
            break
        
        self.use_timer_event = False
        self.setNeedleColor(0, 0, 0, 255)
        self.NeedleColorReleased = self.NeedleColor
        self.setNeedleColorOnDrag(255, 0, 00, 255)
        self.setScaleValueColor(0, 0, 0, 255)
        self.setDisplayValueColor(0, 0, 0, 255)
        self.set_CenterPointColor(0, 0, 0, 255)
        self.value_needle_count = 1
        self.value_needle = QObject
        self.minValue = 0
        self.maxValue = 10
        self.value_offset = 0

        self.valueNeedleSnapzone = 0.05
        self.last_value = 0
        self.gauge_color_outer_radius_factor = 1
        self.gauge_color_inner_radius_factor = 0.9

        self.center_horizontal_value = 0
        self.center_vertical_value = 0

        self.scale_angle_start_value = 135
        self.scale_angle_size = 270

        self.angle_offset = 0

        self.setScalaCount(10)
        self.scala_subdiv_count = 5

        self.pen = QPen(QColor(0, 0, 0))

        QFontDatabase.addApplicationFont(os.path.join(os.path.dirname(
            __file__), 'fonts/Orbitron/Orbitron-VariableFont_wght.ttf'))

        self.scale_polygon_colors = []

        self.bigScaleMarker = Qt.black

        self.fineScaleColor = Qt.black

        self.setEnableScaleText(True)
        self.scale_fontname = "Orbitron"
        self.initial_scale_fontsize = 14
        self.scale_fontsize = self.initial_scale_fontsize
        self.enable_value_text = True
        self.value_fontname = "Orbitron"
        self.initial_value_fontsize = 40
        self.value_fontsize = self.initial_value_fontsize
        self.text_radius_factor = 0.5
        self.setEnableBarGraph(True)
        self.setEnableScalePolygon(True)
        self.enable_CenterPoint = True
        self.enable_fine_scaled_marker = True
        self.enable_big_scaled_marker = True
        self.needle_scale_factor = 0.8
        self.enable_Needle_Polygon = True

        self.setMouseTracking(False)
        self.units = "m/s"

        # QTimer sorgt für neu Darstellung alle X ms
        # evtl performance hier verbessern mit self.update() und self.use_timer_event = False
        # todo: self.update als default ohne ueberpruefung, ob self.use_timer_event gesetzt ist oder nicht
        # Timer startet alle 10ms das event paintEvent
        if self.use_timer_event:
            timer = QTimer(self)
            timer.timeout.connect(self.update)
            timer.start(10)
        else:
            self.update()

        self.setGaugeTheme(0)

        self.rescale_method()

    def setScaleFontFamily(self, font):
        self.scale_fontname = str(font)

    def setValueFontFamily(self, font):
        self.value_fontname = str(font)

    def setBigScaleColor(self, color):
        self.bigScaleMarker = QColor(color)

    def setFineScaleColor(self, color):
        self.fineScaleColor = QColor(color)

    def setGaugeTheme(self, Theme=1):
        if Theme == 0 or Theme == None:
            self.set_scale_polygon_colors([[.00, Qt.red],
                                           [.1, Qt.yellow],
                                           [.15, Qt.green],
                                           [1, Qt.transparent]])

            self.needle_center_bg = [
                                    [0, QColor(35, 40, 3, 255)],
                                    [0.16, QColor(30, 36, 45, 255)],
                                    [0.225, QColor(36, 42, 54, 255)],
                                    [0.423963, QColor(19, 23, 29, 255)],
                                    [0.580645, QColor(45, 53, 68, 255)],
                                    [0.792627, QColor(59, 70, 88, 255)],
                                    [0.935, QColor(30, 35, 45, 255)],
                                    [1, QColor(35, 40, 3, 255)]
            ]

            self.outer_circle_bg = [
                [0.0645161, QColor(30, 35, 45, 255)],
                [0.37788, QColor(57, 67, 86, 255)],
                [1, QColor(30, 36, 45, 255)]
            ]

        if Theme == 1:
            self.set_scale_polygon_colors([[.75, Qt.red],
                                           [.5, Qt.yellow],
                                           [.25, Qt.green]])

            self.needle_center_bg = [
                                    [0, QColor(35, 40, 3, 255)],
                                    [0.16, QColor(30, 36, 45, 255)],
                                    [0.225, QColor(36, 42, 54, 255)],
                                    [0.423963, QColor(19, 23, 29, 255)],
                                    [0.580645, QColor(45, 53, 68, 255)],
                                    [0.792627, QColor(59, 70, 88, 255)],
                                    [0.935, QColor(30, 35, 45, 255)],
                                    [1, QColor(35, 40, 3, 255)]
            ]

            self.outer_circle_bg = [
                [0.0645161, QColor(30, 35, 45, 255)],
                [0.37788, QColor(57, 67, 86, 255)],
                [1, QColor(30, 36, 45, 255)]
            ]

        if Theme == 2:
            self.set_scale_polygon_colors([[.25, Qt.red],
                                           [.5, Qt.yellow],
                                           [.75, Qt.green]])

            self.needle_center_bg = [
                                    [0, QColor(35, 40, 3, 255)],
                                    [0.16, QColor(30, 36, 45, 255)],
                                    [0.225, QColor(36, 42, 54, 255)],
                                    [0.423963, QColor(19, 23, 29, 255)],
                                    [0.580645, QColor(45, 53, 68, 255)],
                                    [0.792627, QColor(59, 70, 88, 255)],
                                    [0.935, QColor(30, 35, 45, 255)],
                                    [1, QColor(35, 40, 3, 255)]
            ]

            self.outer_circle_bg = [
                [0.0645161, QColor(30, 35, 45, 255)],
                [0.37788, QColor(57, 67, 86, 255)],
                [1, QColor(30, 36, 45, 255)]
            ]

        elif Theme == 3:
            self.set_scale_polygon_colors([[.00, Qt.white]])

            self.needle_center_bg = [
                                    [0, Qt.white],
            ]

            self.outer_circle_bg = [
                [0, Qt.white],
            ]

            self.bigScaleMarker = Qt.black
            self.fineScaleColor = Qt.black

        elif Theme == 4:
            self.set_scale_polygon_colors([[1, Qt.black]])

            self.needle_center_bg = [
                                    [0, Qt.black],
            ]

            self.outer_circle_bg = [
                [0, Qt.black],
            ]

            self.bigScaleMarker = Qt.white
            self.fineScaleColor = Qt.white

        elif Theme == 5:
            self.set_scale_polygon_colors([[1, QColor("#029CDE")]])

            self.needle_center_bg = [
                                    [0, QColor("#029CDE")],
            ]

            self.outer_circle_bg = [
                [0, QColor("#029CDE")],
            ]

        elif Theme == 6:
            self.set_scale_polygon_colors([[.75, QColor("#01ADEF")],
                                           [.5, QColor("#0086BF")],
                                           [.25, QColor("#005275")]])

            self.needle_center_bg = [
                                    [0, QColor(0, 46, 61, 255)],
                                    [0.322581, QColor(1, 173, 239, 255)],
                                    [0.571429, QColor(0, 73, 99, 255)],
                                    [1, QColor(0, 46, 61, 255)]
            ]

            self.outer_circle_bg = [
                [0.0645161, QColor(0, 85, 116, 255)],
                [0.37788, QColor(1, 173, 239, 255)],
                [1, QColor(0, 69, 94, 255)]
            ]

            self.bigScaleMarker = Qt.black
            self.fineScaleColor = Qt.black

        elif Theme == 7:
            self.set_scale_polygon_colors([[.25, QColor("#01ADEF")],
                                           [.5, QColor("#0086BF")],
                                           [.75, QColor("#005275")]])

            self.needle_center_bg = [
                                    [0, QColor(0, 46, 61, 255)],
                                    [0.322581, QColor(1, 173, 239, 255)],
                                    [0.571429, QColor(0, 73, 99, 255)],
                                    [1, QColor(0, 46, 61, 255)]
            ]

            self.outer_circle_bg = [
                [0.0645161, QColor(0, 85, 116, 255)],
                [0.37788, QColor(1, 173, 239, 255)],
                [1, QColor(0, 69, 94, 255)]
            ]

            self.bigScaleMarker = Qt.black
            self.fineScaleColor = Qt.black

        elif Theme == 8:
            self.setCustomGaugeTheme(
                color1="#ffaa00",
                color2="#7d5300",
                color3="#3e2900"
            )

            self.bigScaleMarker = Qt.black
            self.fineScaleColor = Qt.black

        elif Theme == 9:
            self.setCustomGaugeTheme(
                color1="#3e2900",
                color2="#7d5300",
                color3="#ffaa00"
            )

            self.bigScaleMarker = Qt.white
            self.fineScaleColor = Qt.white

        elif Theme == 10:
            self.setCustomGaugeTheme(
                color1="#ff007f",
                color2="#aa0055",
                color3="#830042"
            )

            self.bigScaleMarker = Qt.black
            self.fineScaleColor = Qt.black

        elif Theme == 11:
            self.setCustomGaugeTheme(
                color1="#830042",
                color2="#aa0055",
                color3="#ff007f"
            )

            self.bigScaleMarker = Qt.white
            self.fineScaleColor = Qt.white

        elif Theme == 12:
            self.setCustomGaugeTheme(
                color1="#ffe75d",
                color2="#896c1a",
                color3="#232803"
            )

            self.bigScaleMarker = Qt.black
            self.fineScaleColor = Qt.black

        elif Theme == 13:
            self.setCustomGaugeTheme(
                color1="#ffe75d",
                color2="#896c1a",
                color3="#232803"
            )

            self.bigScaleMarker = Qt.black
            self.fineScaleColor = Qt.black

        elif Theme == 14:
            self.setCustomGaugeTheme(
                color1="#232803",
                color2="#821600",
                color3="#ffe75d"
            )

            self.bigScaleMarker = Qt.white
            self.fineScaleColor = Qt.white

        elif Theme == 15:
            self.setCustomGaugeTheme(
                color1="#00FF11",
                color2="#00990A",
                color3="#002603"
            )

            self.bigScaleMarker = Qt.black
            self.fineScaleColor = Qt.black

        elif Theme == 16:
            self.setCustomGaugeTheme(
                color1="#002603",
                color2="#00990A",
                color3="#00FF11"
            )

            self.bigScaleMarker = Qt.white
            self.fineScaleColor = Qt.white

        elif Theme == 17:
            self.setCustomGaugeTheme(
                color1="#00FFCC",
                color2="#00876C",
                color3="#00211B"
            )

            self.bigScaleMarker = Qt.black
            self.fineScaleColor = Qt.black

        elif Theme == 18:
            self.setCustomGaugeTheme(
                color1="#00211B",
                color2="#00876C",
                color3="#00FFCC"
            )

            self.bigScaleMarker = Qt.white
            self.fineScaleColor = Qt.white

        elif Theme == 19:
            self.setCustomGaugeTheme(
                color1="#001EFF",
                color2="#001299",
                color3="#000426"
            )

            self.bigScaleMarker = Qt.black
            self.fineScaleColor = Qt.black

        elif Theme == 20:
            self.setCustomGaugeTheme(
                color1="#000426",
                color2="#001299",
                color3="#001EFF"
            )

            self.bigScaleMarker = Qt.white
            self.fineScaleColor = Qt.white

        elif Theme == 21:
            self.setCustomGaugeTheme(
                color1="#F200FF",
                color2="#85008C",
                color3="#240026"
            )

            self.bigScaleMarker = Qt.black
            self.fineScaleColor = Qt.black

        elif Theme == 22:
            self.setCustomGaugeTheme(
                color1="#240026",
                color2="#85008C",
                color3="#F200FF"
            )

            self.bigScaleMarker = Qt.white
            self.fineScaleColor = Qt.white

        elif Theme == 23:
            self.setCustomGaugeTheme(
                color1="#FF0022",
                color2="#080001",
                color3="#009991"
            )

            self.bigScaleMarker = Qt.white
            self.fineScaleColor = Qt.white

        elif Theme == 24:
            self.setCustomGaugeTheme(
                color1="#009991",
                color2="#080001",
                color3="#FF0022"
            )

            self.bigScaleMarker = Qt.white
            self.fineScaleColor = Qt.white

    def setCustomGaugeTheme(self, **colors):
        if "color1" in colors and len(str(colors['color1'])) > 0:
            if "color2" in colors and len(str(colors['color2'])) > 0:
                if "color3" in colors and len(str(colors['color3'])) > 0:

                    self.set_scale_polygon_colors([[.25, QColor(str(colors['color1']))],
                                                   [.5, QColor(
                                                       str(colors['color2']))],
                                                   [.75, QColor(str(colors['color3']))]])

                    self.needle_center_bg = [
                                            [0, QColor(str(colors['color3']))],
                                            [0.322581, QColor(
                                                str(colors['color1']))],
                                            [0.571429, QColor(
                                                str(colors['color2']))],
                                            [1, QColor(str(colors['color3']))]
                    ]

                    self.outer_circle_bg = [
                        [0.0645161, QColor(str(colors['color3']))],
                        [0.36, QColor(
                            str(colors['color1']))],
                        [1, QColor(str(colors['color2']))]
                    ]

                else:

                    self.set_scale_polygon_colors([[.5, QColor(str(colors['color1']))],
                                                   [1, QColor(str(colors['color2']))]])

                    self.needle_center_bg = [
                                            [0, QColor(str(colors['color2']))],
                                            [1, QColor(str(colors['color1']))]
                    ]

                    self.outer_circle_bg = [
                        [0, QColor(str(colors['color2']))],
                        [1, QColor(str(colors['color2']))]
                    ]

            else:

                self.set_scale_polygon_colors(
                    [[1, QColor(str(colors['color1']))]])

                self.needle_center_bg = [
                                        [1, QColor(str(colors['color1']))]
                ]

                self.outer_circle_bg = [
                    [1, QColor(str(colors['color1']))]
                ]

        else:

            self.setGaugeTheme(0)
            print("color1 is not defined")

    def setScalePolygonColor(self, **colors):
        if "color1" in colors and len(str(colors['color1'])) > 0:
            if "color2" in colors and len(str(colors['color2'])) > 0:
                if "color3" in colors and len(str(colors['color3'])) > 0:

                    self.set_scale_polygon_colors([[.25, QColor(str(colors['color1']))],
                                                   [.5, QColor(
                                                       str(colors['color2']))],
                                                   [.75, QColor(str(colors['color3']))]])

                else:

                    self.set_scale_polygon_colors([[.5, QColor(str(colors['color1']))],
                                                   [1, QColor(str(colors['color2']))]])

            else:

                self.set_scale_polygon_colors(
                    [[1, QColor(str(colors['color1']))]])

        else:
            print("color1 is not defined")

    def setNeedleCenterColor(self, **colors):
        if "color1" in colors and len(str(colors['color1'])) > 0:
            if "color2" in colors and len(str(colors['color2'])) > 0:
                if "color3" in colors and len(str(colors['color3'])) > 0:

                    self.needle_center_bg = [
                                            [0, QColor(str(colors['color3']))],
                                            [0.322581, QColor(
                                                str(colors['color1']))],
                                            [0.571429, QColor(
                                                str(colors['color2']))],
                                            [1, QColor(str(colors['color3']))]
                    ]

                else:

                    self.needle_center_bg = [
                                            [0, QColor(str(colors['color2']))],
                                            [1, QColor(str(colors['color1']))]
                    ]

            else:

                self.needle_center_bg = [
                                        [1, QColor(str(colors['color1']))]
                ]
        else:
            print("color1 is not defined")

    def setOuterCircleColor(self, **colors):
        if "color1" in colors and len(str(colors['color1'])) > 0:
            if "color2" in colors and len(str(colors['color2'])) > 0:
                if "color3" in colors and len(str(colors['color3'])) > 0:

                    self.outer_circle_bg = [
                        [0.0645161, QColor(str(colors['color3']))],
                        [0.37788, QColor(
                            str(colors['color1']))],
                        [1, QColor(str(colors['color2']))]
                    ]

                else:

                    self.outer_circle_bg = [
                        [0, QColor(str(colors['color2']))],
                        [1, QColor(str(colors['color2']))]
                    ]

            else:

                self.outer_circle_bg = [
                    [1, QColor(str(colors['color1']))]
                ]

        else:
            print("color1 is not defined")

    def rescale_method(self):
        if self.width() <= self.height():
            self.widget_diameter = self.width()
        else:
            self.widget_diameter = self.height()
        self.change_value_needle_style([QPolygon([
            QPoint(4, 30),
            QPoint(-4, 30),
            QPoint(-2, int(- self.widget_diameter / 2 * self.needle_scale_factor)),
            QPoint(0, int(- self.widget_diameter /
                   2 * self.needle_scale_factor - 6)),
            QPoint(2, int(- self.widget_diameter / 2 * self.needle_scale_factor))
        ])])

        self.scale_fontsize = int(
            self.initial_scale_fontsize * self.widget_diameter / 400)
        self.value_fontsize = int(
            self.initial_value_fontsize * self.widget_diameter / 400)

    def change_value_needle_style(self, design):
        # prepared for multiple needle instrument
        self.value_needle = []
        for i in design:
            self.value_needle.append(i)
        if not self.use_timer_event:
            self.update()

    def updateValue(self, value, mouse_controlled=False):
        # if not mouse_controlled:
        #     self.value = value
        #
        # if mouse_controlled:
        #     self.valueChanged.emit(int(value))

        if value <= self.minValue:
            self.value = self.minValue
        elif value >= self.maxValue:
            self.value = self.maxValue
        else:
            self.value = value
        # self.paintEvent("")
        self.valueChanged.emit(int(value))
        # print(self.value)

        # ohne timer: aktiviere self.update()
        if not self.use_timer_event:
            self.update()

    def updateAngleOffset(self, offset):
        self.angle_offset = offset
        if not self.use_timer_event:
            self.update()

    def center_horizontal(self, value):
        self.center_horizontal_value = value
        # print("horizontal: " + str(self.center_horizontal_value))

    def center_vertical(self, value):
        self.center_vertical_value = value
        # print("vertical: " + str(self.center_vertical_value))

    def setNeedleColor(self, R=50, G=50, B=50, Transparency=255):
        # Red: R = 0 - 255
        # Green: G = 0 - 255
        # Blue: B = 0 - 255
        # Transparency = 0 - 255
        self.NeedleColor = QColor(R, G, B, Transparency)
        self.NeedleColorReleased = self.NeedleColor

        if not self.use_timer_event:
            self.update()

    def setNeedleColorOnDrag(self, R=50, G=50, B=50, Transparency=255):
        # Red: R = 0 - 255
        # Green: G = 0 - 255
        # Blue: B = 0 - 255
        # Transparency = 0 - 255
        self.NeedleColorDrag = QColor(R, G, B, Transparency)

        if not self.use_timer_event:
            self.update()

    def setScaleValueColor(self, R=50, G=50, B=50, Transparency=255):
        # Red: R = 0 - 255
        # Green: G = 0 - 255
        # Blue: B = 0 - 255
        # Transparency = 0 - 255
        self.ScaleValueColor = QColor(R, G, B, Transparency)

        if not self.use_timer_event:
            self.update()

    def setDisplayValueColor(self, R=50, G=50, B=50, Transparency=255):
        # Red: R = 0 - 255
        # Green: G = 0 - 255
        # Blue: B = 0 - 255
        # Transparency = 0 - 255
        self.DisplayValueColor = QColor(R, G, B, Transparency)

        if not self.use_timer_event:
            self.update()

    def set_CenterPointColor(self, R=50, G=50, B=50, Transparency=255):
        self.CenterPointColor = QColor(R, G, B, Transparency)

        if not self.use_timer_event:
            self.update()

    def setEnableNeedlePolygon(self, enable=True):
        self.enable_Needle_Polygon = enable

        if not self.use_timer_event:
            self.update()

    def setEnableScaleText(self, enable=True):
        self.enable_scale_text = enable

        if not self.use_timer_event:
            self.update()

    def setEnableBarGraph(self, enable=True):
        self.enableBarGraph = enable

        if not self.use_timer_event:
            self.update()

    def setEnableValueText(self, enable=True):
        self.enable_value_text = enable

        if not self.use_timer_event:
            self.update()

    def setEnableCenterPoint(self, enable=True):
        self.enable_CenterPoint = enable

        if not self.use_timer_event:
            self.update()

    def setEnableScalePolygon(self, enable=True):
        self.enable_filled_Polygon = enable

        if not self.use_timer_event:
            self.update()

    def setEnableBigScaleGrid(self, enable=True):
        self.enable_big_scaled_marker = enable

        if not self.use_timer_event:
            self.update()

    def setEnableFineScaleGrid(self, enable=True):
        self.enable_fine_scaled_marker = enable

        if not self.use_timer_event:
            self.update()

    def setScalaCount(self, count):
        if count < 1:
            count = 1
        self.scalaCount = count

        if not self.use_timer_event:
            self.update()

    def setMinValue(self, min):
        if self.value < min:
            self.value = min
        if min >= self.maxValue:
            self.minValue = self.maxValue - 1
        else:
            self.minValue = min

        if not self.use_timer_event:
            self.update()

    def setMaxValue(self, max):
        if self.value > max:
            self.value = max
        if max <= self.minValue:
            self.maxValue = self.minValue + 1
        else:
            self.maxValue = max

        if not self.use_timer_event:
            self.update()

    def setScaleStartAngle(self, value):
        # Value range in DEG: 0 - 360
        self.scale_angle_start_value = value
        # print("startFill: " + str(self.scale_angle_start_value))

        if not self.use_timer_event:
            self.update()

    def setTotalScaleAngleSize(self, value):
        self.scale_angle_size = value
        # print("stopFill: " + str(self.scale_angle_size))

        if not self.use_timer_event:
            self.update()

    def setGaugeColorOuterRadiusFactor(self, value):
        self.gauge_color_outer_radius_factor = float(value) / 1000
        # print(self.gauge_color_outer_radius_factor)

        if not self.use_timer_event:
            self.update()

    def setGaugeColorInnerRadiusFactor(self, value):
        self.gauge_color_inner_radius_factor = float(value) / 1000
        # print(self.gauge_color_inner_radius_factor)

        if not self.use_timer_event:
            self.update()

    def set_scale_polygon_colors(self, color_array):
        # print(type(color_array))
        if 'list' in str(type(color_array)):
            self.scale_polygon_colors = color_array
        elif color_array == None:
            self.scale_polygon_colors = [[.0, Qt.transparent]]
        else:
            self.scale_polygon_colors = [[.0, Qt.transparent]]

        if not self.use_timer_event:
            self.update()

    ################################################################################################
    # GET MAXIMUM VALUE
    ################################################################################################
    def get_value_max(self):
        return self.maxValue

    def create_polygon_pie(self, outer_radius, inner_raduis, start, lenght, bar_graph=True):
        polygon_pie = QPolygonF()
        # start = self.scale_angle_start_value
        # start = 0
        # lenght = self.scale_angle_size
        # lenght = 180
        # inner_raduis = self.width()/4
        # print(start)
        n = 360     # angle steps size for full circle
        # changing n value will causes drawing issues
        w = 360 / n   # angle per step
        # create outer circle line from "start"-angle to "start + lenght"-angle
        x = 0
        y = 0

        # todo enable/disable bar graf here
        if not self.enableBarGraph and bar_graph:
            # float_value = ((lenght / (self.maxValue - self.minValue)) * (self.value - self.minValue))
            lenght = int(
                round((lenght / (self.maxValue - self.minValue)) * (self.value - self.minValue)))
            # print("f: %s, l: %s" %(float_value, lenght))
            pass

        # mymax = 0

        # add the points of polygon
        for i in range(lenght + 1):
            t = w * i + start - self.angle_offset
            x = outer_radius * math.cos(math.radians(t))
            y = outer_radius * math.sin(math.radians(t))
            polygon_pie.append(QPointF(x, y))
        # create inner circle line from "start + lenght"-angle to "start"-angle
        # add the points of polygon
        for i in range(lenght + 1):
            # print("2 " + str(i))
            t = w * (lenght - i) + start - self.angle_offset
            x = inner_raduis * math.cos(math.radians(t))
            y = inner_raduis * math.sin(math.radians(t))
            polygon_pie.append(QPointF(x, y))

        # close outer line
        polygon_pie.append(QPointF(x, y))
        return polygon_pie

    def draw_filled_polygon(self, outline_pen_with=0):
        if not self.scale_polygon_colors == None:
            painter_filled_polygon = QPainter(self)
            painter_filled_polygon.setRenderHint(QPainter.Antialiasing)
            # Koordinatenursprung in die Mitte der Flaeche legen
            painter_filled_polygon.translate(
                self.width() / 2, self.height() / 2)

            painter_filled_polygon.setPen(Qt.NoPen)

            self.pen.setWidth(outline_pen_with)
            if outline_pen_with > 0:
                painter_filled_polygon.setPen(self.pen)

            colored_scale_polygon = self.create_polygon_pie(
                ((self.widget_diameter / 2) - (self.pen.width() / 2)) *
                self.gauge_color_outer_radius_factor,
                (((self.widget_diameter / 2) - (self.pen.width() / 2))
                 * self.gauge_color_inner_radius_factor),
                self.scale_angle_start_value, self.scale_angle_size)

            gauge_rect = QRect(QPoint(0, 0), QSize(
                int(self.widget_diameter / 2 - 1), int(self.widget_diameter - 1)))
            grad = QConicalGradient(QPointF(0, 0), - self.scale_angle_size - self.scale_angle_start_value +
                                    self.angle_offset - 1)

            # todo definition scale color as array here
            for eachcolor in self.scale_polygon_colors:
                grad.setColorAt(eachcolor[0], eachcolor[1])
            # grad.setColorAt(.00, Qt.red)
            # grad.setColorAt(.1, Qt.yellow)
            # grad.setColorAt(.15, Qt.green)
            # grad.setColorAt(1, Qt.transparent)
            # self.brush = QBrush(QColor(255, 0, 255, 255))
            # grad.setStyle(Qt.Dense6Pattern)
            # painter_filled_polygon.setBrush(self.brush)
            painter_filled_polygon.setBrush(grad)

            painter_filled_polygon.drawPolygon(colored_scale_polygon)
            # return painter_filled_polygon

    def draw_icon_image(self):
        pass

    def draw_big_scaled_marker(self):
        my_painter = QPainter(self)
        my_painter.setRenderHint(QPainter.Antialiasing)
        # Koordinatenursprung in die Mitte der Flaeche legen
        my_painter.translate(self.width() / 2, self.height() / 2)

        # my_painter.setPen(Qt.NoPen)
        self.pen = QPen(self.bigScaleMarker)
        self.pen.setWidth(2)
        # # if outline_pen_with > 0:
        my_painter.setPen(self.pen)

        my_painter.rotate(self.scale_angle_start_value - self.angle_offset)
        steps_size = (float(self.scale_angle_size) / float(self.scalaCount))
        scale_line_outer_start = self.widget_diameter // 2
        scale_line_lenght = int((self.widget_diameter / 2) -
                                (self.widget_diameter / 20))
        # print(stepszize)
        for i in range(self.scalaCount + 1):
            my_painter.drawLine(scale_line_lenght, 0,
                                scale_line_outer_start, 0)
            my_painter.rotate(steps_size)

    def create_scale_marker_values_text(self):
        painter = QPainter(self)
        # painter.setRenderHint(QPainter.HighQualityAntialiasing)
        painter.setRenderHint(QPainter.Antialiasing)

        # Koordinatenursprung in die Mitte der Flaeche legen
        painter.translate(self.width() / 2, self.height() / 2)
        # painter.save()
        font = QFont(self.scale_fontname, self.scale_fontsize, QFont.Bold)
        fm = QFontMetrics(font)

        pen_shadow = QPen()

        pen_shadow.setBrush(self.ScaleValueColor)
        painter.setPen(pen_shadow)

        text_radius_factor = 0.8
        text_radius = self.widget_diameter / 2 * text_radius_factor

        scale_per_div = int((self.maxValue - self.minValue) / self.scalaCount)

        angle_distance = (float(self.scale_angle_size) /
                          float(self.scalaCount))
        for i in range(self.scalaCount + 1):
            # text = str(int((self.maxValue - self.minValue) / self.scalaCount * i))
            text = str(int(self.minValue + scale_per_div * i))
            w = fm.width(text) + 1
            h = fm.height()
            painter.setFont(QFont(self.scale_fontname,
                            self.scale_fontsize, QFont.Bold))
            angle = angle_distance * i + \
                float(self.scale_angle_start_value - self.angle_offset)
            x = text_radius * math.cos(math.radians(angle))
            y = text_radius * math.sin(math.radians(angle))
            # print(w, h, x, y, text)

            painter.drawText(int(x - w / 2), int(y - h / 2), int(w),
                             int(h), Qt.AlignCenter, text)
        # painter.restore()

    def create_fine_scaled_marker(self):
        #  Description_dict = 0
        my_painter = QPainter(self)

        my_painter.setRenderHint(QPainter.Antialiasing)
        # Koordinatenursprung in die Mitte der Flaeche legen
        my_painter.translate(self.width() / 2, self.height() / 2)

        my_painter.setPen(self.fineScaleColor)
        my_painter.rotate(self.scale_angle_start_value - self.angle_offset)
        steps_size = (float(self.scale_angle_size) /
                      float(self.scalaCount * self.scala_subdiv_count))
        scale_line_outer_start = self.widget_diameter // 2
        scale_line_lenght = int(
            (self.widget_diameter / 2) - (self.widget_diameter / 40))
        for i in range((self.scalaCount * self.scala_subdiv_count) + 1):
            my_painter.drawLine(scale_line_lenght, 0,
                                scale_line_outer_start, 0)
            my_painter.rotate(steps_size)

    def create_values_text(self):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.HighQualityAntialiasing)
        # painter.setRenderHint(QPainter.Antialiasing)

        painter.translate(self.width() / 2, self.height() / 2)
        font = QFont(self.value_fontname, self.value_fontsize, QFont.Bold)
        fm = QFontMetrics(font)

        pen_shadow = QPen()

        pen_shadow.setBrush(self.DisplayValueColor)
        painter.setPen(pen_shadow)

        text_radius = self.widget_diameter / 2 * self.text_radius_factor
        text = str(int(self.value))
        w = fm.width(text) + 1
        h = fm.height()
        painter.setFont(QFont(self.value_fontname,
                        self.value_fontsize, QFont.Bold))
        angle_end = float(self.scale_angle_start_value +
                          self.scale_angle_size - 360)
        angle = (angle_end - self.scale_angle_start_value) / \
            2 + self.scale_angle_start_value

        x = text_radius * math.cos(math.radians(angle))
        y = text_radius * math.sin(math.radians(angle))
        # print(w, h, x, y, text)
        painter.drawText(int(x - w / 2), int(y - h / 2), int(w),
                         int(h), Qt.AlignCenter, text)

    def create_units_text(self):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.HighQualityAntialiasing)
        # painter.setRenderHint(QPainter.Antialiasing)

        painter.translate(self.width() / 2, self.height() / 2)
        font = QFont(self.value_fontname, int(
            self.value_fontsize / 2.5), QFont.Bold)
        fm = QFontMetrics(font)

        pen_shadow = QPen()

        pen_shadow.setBrush(self.DisplayValueColor)
        painter.setPen(pen_shadow)

        text_radius = self.widget_diameter / 2 * self.text_radius_factor

        text = str(self.units)
        w = fm.width(text) + 1
        h = fm.height()
        painter.setFont(QFont(self.value_fontname, int(
            self.value_fontsize / 2.5), QFont.Bold))

        angle_end = float(self.scale_angle_start_value +
                          self.scale_angle_size + 180)
        angle = (angle_end - self.scale_angle_start_value) / \
            2 + self.scale_angle_start_value

        x = text_radius * math.cos(math.radians(angle))
        y = text_radius * math.sin(math.radians(angle))
        # print(w, h, x, y, text)
        painter.drawText(int(x - w / 2), int(y - h / 2), int(w),
                         int(h), Qt.AlignCenter, text)


    def draw_big_needle_center_point(self, diameter=30):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.translate(self.width() / 2, self.height() / 2)
        painter.setPen(Qt.NoPen)
        colored_scale_polygon = self.create_polygon_pie(
            ((self.widget_diameter / 8) - (self.pen.width() / 2)),
            0,
            self.scale_angle_start_value, 360, False)

        grad = QConicalGradient(QPointF(0, 0), 0)

        # todo definition scale color as array here
        for eachcolor in self.needle_center_bg:
            grad.setColorAt(eachcolor[0], eachcolor[1])
        painter.setBrush(grad)

        painter.drawPolygon(colored_scale_polygon)
    def draw_outer_circle(self, diameter=30):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        painter.translate(self.width() / 2, self.height() / 2)
        painter.setPen(Qt.NoPen)
        colored_scale_polygon = self.create_polygon_pie(
            ((self.widget_diameter / 2) - (self.pen.width())),
            (self.widget_diameter / 6),
            self.scale_angle_start_value / 10, 360, False)

        radialGradient = QRadialGradient(QPointF(0, 0), self.width())

        for eachcolor in self.outer_circle_bg:
            radialGradient.setColorAt(eachcolor[0], eachcolor[1])

        painter.setBrush(radialGradient)

        painter.drawPolygon(colored_scale_polygon)

    ################################################################################################
    # NEEDLE POINTER
    ################################################################################################

    def draw_needle(self):
        painter = QPainter(self)
        # painter.setRenderHint(QtGui.QPainter.HighQualityAntialiasing)
        painter.setRenderHint(QPainter.Antialiasing)
        # Koordinatenursprung in die Mitte der Flaeche legen
        painter.translate(self.width() / 2, self.height() / 2)
        painter.setPen(Qt.NoPen)
        painter.setBrush(self.NeedleColor)
        painter.rotate(((self.value - self.value_offset - self.minValue) * self.scale_angle_size /
                        (self.maxValue - self.minValue)) + 90 + self.scale_angle_start_value)

        painter.drawConvexPolygon(self.value_needle[0])

    ###############################################################################################
    # EVENTS
    ###############################################################################################

    ################################################################################################
    # ON WINDOW RESIZE
    ################################################################################################
    def resizeEvent(self, event):
        # self.resized.emit()
        # return super(self.parent, self).resizeEvent(event)
        # print("resized")
        # print(self.width())
        self.rescale_method()
        # self.emit(QtCore.SIGNAL("resize()"))
        # print("resizeEvent")

    ################################################################################################
    # ON PAINT EVENT
    ################################################################################################
    def paintEvent(self, event):
        # Main Drawing Event:
        # Will be executed on every change
        # vgl http://doc.qt.io/qt-4.8/qt-demos-affine-xform-cpp.html
        # print("event", event)

        self.draw_outer_circle()
        self.draw_icon_image()
        # colored pie area
        if self.enable_filled_Polygon:
            self.draw_filled_polygon()

        # draw scale marker lines
        if self.enable_fine_scaled_marker:
            self.create_fine_scaled_marker()
        if self.enable_big_scaled_marker:
            self.draw_big_scaled_marker()

        # draw scale marker value text
        if self.enable_scale_text:
            self.create_scale_marker_values_text()

        # Display Value
        if self.enable_value_text:
            self.create_values_text()
            self.create_units_text()

        # draw needle 1
        if self.enable_Needle_Polygon:
            self.draw_needle()

        # Draw Center Point
        if self.enable_CenterPoint:
            self.draw_big_needle_center_point(
                diameter=(self.widget_diameter / 6))

    ###############################################################################################
    # MOUSE EVENTS
    ###############################################################################################

    def setMouseTracking(self, flag):
        def recursive_set(parent):
            for child in parent.findChildren(QObject):
                try:
                    child.setMouseTracking(flag)
                except:
                    pass
                recursive_set(child)

        QWidget.setMouseTracking(self, flag)
        recursive_set(self)

    def mouseReleaseEvent(self, QMouseEvent):
        self.NeedleColor = self.NeedleColorReleased

        if not self.use_timer_event:
            self.update()
        pass

    ########################################################################
    # MOUSE LEAVE EVENT
    ########################################################################
    def leaveEvent(self, event):
        self.NeedleColor = self.NeedleColorReleased
        self.update()

    def mouseMoveEvent(self, event):
        x, y = event.x() - (self.width() / 2), event.y() - (self.height() / 2)
        # print(event.x(), event.y(), self.width(), self.height())
        if not x == 0:
            angle = math.atan2(y, x) / math.pi * 180
            # winkellaenge der anzeige immer positiv 0 - 360deg
            # min wert + umskalierter wert
            value = (float(math.fmod(angle - self.scale_angle_start_value + 720, 360)) /
                     (float(self.scale_angle_size) / float(self.maxValue - self.minValue))) + self.minValue
            temp = value
            fmod = float(
                math.fmod(angle - self.scale_angle_start_value + 720, 360))
            state = 0
            if (self.value - (self.maxValue - self.minValue) * self.valueNeedleSnapzone) <= \
                    value <= \
                    (self.value + (self.maxValue - self.minValue) * self.valueNeedleSnapzone):
                self.NeedleColor = self.NeedleColorDrag
                # todo: evtl ueberpruefen
                #
                state = 9
                # if value >= self.maxValue and self.last_value < (self.maxValue - self.minValue) / 2:
                if value >= self.maxValue and self.last_value < (self.maxValue - self.minValue) / 2:
                    state = 1
                    value = self.maxValue
                    self.last_value = self.minValue
                    self.valueChanged.emit(int(value))

                elif value >= self.maxValue >= self.last_value:
                    state = 2
                    value = self.maxValue
                    self.last_value = self.maxValue
                    self.valueChanged.emit(int(value))

                else:
                    state = 3
                    self.last_value = value
                    self.valueChanged.emit(int(value))

                self.updateValue(value)


#!####################################################################################################################################################### YAW END

###############################################################################################################################################! PİTCH START
class AnalogGauge_pitch(QWidget):
    valueChanged = pyqtSignal(int)
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(100, 100)
        
        self.altTimer = QTimer()
        self.altTimer.start(10) # Saniyede bir güncelle
        self.altTimer.timeout.connect(self.update_pitch)
    
    def update_pitch(self):
        while True:
            gaugePitch = vehicle.attitude.pitch
            self.value= gaugePitch
            break
        
        self.use_timer_event = False
        self.setNeedleColor(0, 0, 0, 255)
        self.NeedleColorReleased = self.NeedleColor
        self.setNeedleColorOnDrag(255, 0, 00, 255)
        self.setScaleValueColor(0, 0, 0, 255)
        self.setDisplayValueColor(0, 0, 0, 255)
        self.set_CenterPointColor(0, 0, 0, 255)
        self.value_needle_count = 1
        self.value_needle = QObject
        self.minValue = 0
        self.maxValue = 10
        
        self.value_offset = 0

        self.valueNeedleSnapzone = 0.05
        self.last_value = 0
        self.gauge_color_outer_radius_factor = 1
        self.gauge_color_inner_radius_factor = 0.9

        self.center_horizontal_value = 0
        self.center_vertical_value = 0

        self.scale_angle_start_value = 135
        self.scale_angle_size = 270

        self.angle_offset = 0

        self.setScalaCount(10)
        self.scala_subdiv_count = 5

        self.pen = QPen(QColor(0, 0, 0))

        QFontDatabase.addApplicationFont(os.path.join(os.path.dirname(
            __file__), 'fonts/Orbitron/Orbitron-VariableFont_wght.ttf'))

        self.scale_polygon_colors = []

        self.bigScaleMarker = Qt.black

        self.fineScaleColor = Qt.black

        self.setEnableScaleText(True)
        self.scale_fontname = "Orbitron"
        self.initial_scale_fontsize = 14
        self.scale_fontsize = self.initial_scale_fontsize
        self.enable_value_text = True
        self.value_fontname = "Orbitron"
        self.initial_value_fontsize = 40
        self.value_fontsize = self.initial_value_fontsize
        self.text_radius_factor = 0.5
        self.setEnableBarGraph(True)
        self.setEnableScalePolygon(True)
        self.enable_CenterPoint = True
        self.enable_fine_scaled_marker = True
        self.enable_big_scaled_marker = True
        self.needle_scale_factor = 0.8
        self.enable_Needle_Polygon = True

        self.setMouseTracking(False)
        self.units = "m/s"

        # QTimer sorgt für neu Darstellung alle X ms
        # evtl performance hier verbessern mit self.update() und self.use_timer_event = False
        # todo: self.update als default ohne ueberpruefung, ob self.use_timer_event gesetzt ist oder nicht
        # Timer startet alle 10ms das event paintEvent
        if self.use_timer_event:
            timer = QTimer(self)
            timer.timeout.connect(self.update)
            timer.start(10)
        else:
            self.update()

        self.setGaugeTheme(0)

        self.rescale_method()

    def setScaleFontFamily(self, font):
        self.scale_fontname = str(font)

    def setValueFontFamily(self, font):
        self.value_fontname = str(font)

    def setBigScaleColor(self, color):
        self.bigScaleMarker = QColor(color)

    def setFineScaleColor(self, color):
        self.fineScaleColor = QColor(color)

    def setGaugeTheme(self, Theme=1):
        if Theme == 0 or Theme == None:
            self.set_scale_polygon_colors([[.00, Qt.red],
                                           [.1, Qt.yellow],
                                           [.15, Qt.green],
                                           [1, Qt.transparent]])

            self.needle_center_bg = [
                                    [0, QColor(35, 40, 3, 255)],
                                    [0.16, QColor(30, 36, 45, 255)],
                                    [0.225, QColor(36, 42, 54, 255)],
                                    [0.423963, QColor(19, 23, 29, 255)],
                                    [0.580645, QColor(45, 53, 68, 255)],
                                    [0.792627, QColor(59, 70, 88, 255)],
                                    [0.935, QColor(30, 35, 45, 255)],
                                    [1, QColor(35, 40, 3, 255)]
            ]

            self.outer_circle_bg = [
                [0.0645161, QColor(30, 35, 45, 255)],
                [0.37788, QColor(57, 67, 86, 255)],
                [1, QColor(30, 36, 45, 255)]
            ]

        if Theme == 1:
            self.set_scale_polygon_colors([[.75, Qt.red],
                                           [.5, Qt.yellow],
                                           [.25, Qt.green]])

            self.needle_center_bg = [
                                    [0, QColor(35, 40, 3, 255)],
                                    [0.16, QColor(30, 36, 45, 255)],
                                    [0.225, QColor(36, 42, 54, 255)],
                                    [0.423963, QColor(19, 23, 29, 255)],
                                    [0.580645, QColor(45, 53, 68, 255)],
                                    [0.792627, QColor(59, 70, 88, 255)],
                                    [0.935, QColor(30, 35, 45, 255)],
                                    [1, QColor(35, 40, 3, 255)]
            ]

            self.outer_circle_bg = [
                [0.0645161, QColor(30, 35, 45, 255)],
                [0.37788, QColor(57, 67, 86, 255)],
                [1, QColor(30, 36, 45, 255)]
            ]

        if Theme == 2:
            self.set_scale_polygon_colors([[.25, Qt.red],
                                           [.5, Qt.yellow],
                                           [.75, Qt.green]])

            self.needle_center_bg = [
                                    [0, QColor(35, 40, 3, 255)],
                                    [0.16, QColor(30, 36, 45, 255)],
                                    [0.225, QColor(36, 42, 54, 255)],
                                    [0.423963, QColor(19, 23, 29, 255)],
                                    [0.580645, QColor(45, 53, 68, 255)],
                                    [0.792627, QColor(59, 70, 88, 255)],
                                    [0.935, QColor(30, 35, 45, 255)],
                                    [1, QColor(35, 40, 3, 255)]
            ]

            self.outer_circle_bg = [
                [0.0645161, QColor(30, 35, 45, 255)],
                [0.37788, QColor(57, 67, 86, 255)],
                [1, QColor(30, 36, 45, 255)]
            ]

        elif Theme == 3:
            self.set_scale_polygon_colors([[.00, Qt.white]])

            self.needle_center_bg = [
                                    [0, Qt.white],
            ]

            self.outer_circle_bg = [
                [0, Qt.white],
            ]

            self.bigScaleMarker = Qt.black
            self.fineScaleColor = Qt.black

        elif Theme == 4:
            self.set_scale_polygon_colors([[1, Qt.black]])

            self.needle_center_bg = [
                                    [0, Qt.black],
            ]

            self.outer_circle_bg = [
                [0, Qt.black],
            ]

            self.bigScaleMarker = Qt.white
            self.fineScaleColor = Qt.white

        elif Theme == 5:
            self.set_scale_polygon_colors([[1, QColor("#029CDE")]])

            self.needle_center_bg = [
                                    [0, QColor("#029CDE")],
            ]

            self.outer_circle_bg = [
                [0, QColor("#029CDE")],
            ]

        elif Theme == 6:
            self.set_scale_polygon_colors([[.75, QColor("#01ADEF")],
                                           [.5, QColor("#0086BF")],
                                           [.25, QColor("#005275")]])

            self.needle_center_bg = [
                                    [0, QColor(0, 46, 61, 255)],
                                    [0.322581, QColor(1, 173, 239, 255)],
                                    [0.571429, QColor(0, 73, 99, 255)],
                                    [1, QColor(0, 46, 61, 255)]
            ]

            self.outer_circle_bg = [
                [0.0645161, QColor(0, 85, 116, 255)],
                [0.37788, QColor(1, 173, 239, 255)],
                [1, QColor(0, 69, 94, 255)]
            ]

            self.bigScaleMarker = Qt.black
            self.fineScaleColor = Qt.black

        elif Theme == 7:
            self.set_scale_polygon_colors([[.25, QColor("#01ADEF")],
                                           [.5, QColor("#0086BF")],
                                           [.75, QColor("#005275")]])

            self.needle_center_bg = [
                                    [0, QColor(0, 46, 61, 255)],
                                    [0.322581, QColor(1, 173, 239, 255)],
                                    [0.571429, QColor(0, 73, 99, 255)],
                                    [1, QColor(0, 46, 61, 255)]
            ]

            self.outer_circle_bg = [
                [0.0645161, QColor(0, 85, 116, 255)],
                [0.37788, QColor(1, 173, 239, 255)],
                [1, QColor(0, 69, 94, 255)]
            ]

            self.bigScaleMarker = Qt.black
            self.fineScaleColor = Qt.black

        elif Theme == 8:
            self.setCustomGaugeTheme(
                color1="#ffaa00",
                color2="#7d5300",
                color3="#3e2900"
            )

            self.bigScaleMarker = Qt.black
            self.fineScaleColor = Qt.black

        elif Theme == 9:
            self.setCustomGaugeTheme(
                color1="#3e2900",
                color2="#7d5300",
                color3="#ffaa00"
            )

            self.bigScaleMarker = Qt.white
            self.fineScaleColor = Qt.white

        elif Theme == 10:
            self.setCustomGaugeTheme(
                color1="#ff007f",
                color2="#aa0055",
                color3="#830042"
            )

            self.bigScaleMarker = Qt.black
            self.fineScaleColor = Qt.black

        elif Theme == 11:
            self.setCustomGaugeTheme(
                color1="#830042",
                color2="#aa0055",
                color3="#ff007f"
            )

            self.bigScaleMarker = Qt.white
            self.fineScaleColor = Qt.white

        elif Theme == 12:
            self.setCustomGaugeTheme(
                color1="#ffe75d",
                color2="#896c1a",
                color3="#232803"
            )

            self.bigScaleMarker = Qt.black
            self.fineScaleColor = Qt.black

        elif Theme == 13:
            self.setCustomGaugeTheme(
                color1="#ffe75d",
                color2="#896c1a",
                color3="#232803"
            )

            self.bigScaleMarker = Qt.black
            self.fineScaleColor = Qt.black

        elif Theme == 14:
            self.setCustomGaugeTheme(
                color1="#232803",
                color2="#821600",
                color3="#ffe75d"
            )

            self.bigScaleMarker = Qt.white
            self.fineScaleColor = Qt.white

        elif Theme == 15:
            self.setCustomGaugeTheme(
                color1="#00FF11",
                color2="#00990A",
                color3="#002603"
            )

            self.bigScaleMarker = Qt.black
            self.fineScaleColor = Qt.black

        elif Theme == 16:
            self.setCustomGaugeTheme(
                color1="#002603",
                color2="#00990A",
                color3="#00FF11"
            )

            self.bigScaleMarker = Qt.white
            self.fineScaleColor = Qt.white

        elif Theme == 17:
            self.setCustomGaugeTheme(
                color1="#00FFCC",
                color2="#00876C",
                color3="#00211B"
            )

            self.bigScaleMarker = Qt.black
            self.fineScaleColor = Qt.black

        elif Theme == 18:
            self.setCustomGaugeTheme(
                color1="#00211B",
                color2="#00876C",
                color3="#00FFCC"
            )

            self.bigScaleMarker = Qt.white
            self.fineScaleColor = Qt.white

        elif Theme == 19:
            self.setCustomGaugeTheme(
                color1="#001EFF",
                color2="#001299",
                color3="#000426"
            )

            self.bigScaleMarker = Qt.black
            self.fineScaleColor = Qt.black

        elif Theme == 20:
            self.setCustomGaugeTheme(
                color1="#000426",
                color2="#001299",
                color3="#001EFF"
            )

            self.bigScaleMarker = Qt.white
            self.fineScaleColor = Qt.white

        elif Theme == 21:
            self.setCustomGaugeTheme(
                color1="#F200FF",
                color2="#85008C",
                color3="#240026"
            )

            self.bigScaleMarker = Qt.black
            self.fineScaleColor = Qt.black

        elif Theme == 22:
            self.setCustomGaugeTheme(
                color1="#240026",
                color2="#85008C",
                color3="#F200FF"
            )

            self.bigScaleMarker = Qt.white
            self.fineScaleColor = Qt.white

        elif Theme == 23:
            self.setCustomGaugeTheme(
                color1="#FF0022",
                color2="#080001",
                color3="#009991"
            )

            self.bigScaleMarker = Qt.white
            self.fineScaleColor = Qt.white

        elif Theme == 24:
            self.setCustomGaugeTheme(
                color1="#009991",
                color2="#080001",
                color3="#FF0022"
            )

            self.bigScaleMarker = Qt.white
            self.fineScaleColor = Qt.white

    def setCustomGaugeTheme(self, **colors):
        if "color1" in colors and len(str(colors['color1'])) > 0:
            if "color2" in colors and len(str(colors['color2'])) > 0:
                if "color3" in colors and len(str(colors['color3'])) > 0:

                    self.set_scale_polygon_colors([[.25, QColor(str(colors['color1']))],
                                                   [.5, QColor(
                                                       str(colors['color2']))],
                                                   [.75, QColor(str(colors['color3']))]])

                    self.needle_center_bg = [
                                            [0, QColor(str(colors['color3']))],
                                            [0.322581, QColor(
                                                str(colors['color1']))],
                                            [0.571429, QColor(
                                                str(colors['color2']))],
                                            [1, QColor(str(colors['color3']))]
                    ]

                    self.outer_circle_bg = [
                        [0.0645161, QColor(str(colors['color3']))],
                        [0.36, QColor(
                            str(colors['color1']))],
                        [1, QColor(str(colors['color2']))]
                    ]

                else:

                    self.set_scale_polygon_colors([[.5, QColor(str(colors['color1']))],
                                                   [1, QColor(str(colors['color2']))]])

                    self.needle_center_bg = [
                                            [0, QColor(str(colors['color2']))],
                                            [1, QColor(str(colors['color1']))]
                    ]

                    self.outer_circle_bg = [
                        [0, QColor(str(colors['color2']))],
                        [1, QColor(str(colors['color2']))]
                    ]

            else:

                self.set_scale_polygon_colors(
                    [[1, QColor(str(colors['color1']))]])

                self.needle_center_bg = [
                                        [1, QColor(str(colors['color1']))]
                ]

                self.outer_circle_bg = [
                    [1, QColor(str(colors['color1']))]
                ]

        else:

            self.setGaugeTheme(0)
            print("color1 is not defined")

    def setScalePolygonColor(self, **colors):
        if "color1" in colors and len(str(colors['color1'])) > 0:
            if "color2" in colors and len(str(colors['color2'])) > 0:
                if "color3" in colors and len(str(colors['color3'])) > 0:

                    self.set_scale_polygon_colors([[.25, QColor(str(colors['color1']))],
                                                   [.5, QColor(
                                                       str(colors['color2']))],
                                                   [.75, QColor(str(colors['color3']))]])

                else:

                    self.set_scale_polygon_colors([[.5, QColor(str(colors['color1']))],
                                                   [1, QColor(str(colors['color2']))]])

            else:

                self.set_scale_polygon_colors(
                    [[1, QColor(str(colors['color1']))]])

        else:
            print("color1 is not defined")

    def setNeedleCenterColor(self, **colors):
        if "color1" in colors and len(str(colors['color1'])) > 0:
            if "color2" in colors and len(str(colors['color2'])) > 0:
                if "color3" in colors and len(str(colors['color3'])) > 0:

                    self.needle_center_bg = [
                                            [0, QColor(str(colors['color3']))],
                                            [0.322581, QColor(
                                                str(colors['color1']))],
                                            [0.571429, QColor(
                                                str(colors['color2']))],
                                            [1, QColor(str(colors['color3']))]
                    ]

                else:

                    self.needle_center_bg = [
                                            [0, QColor(str(colors['color2']))],
                                            [1, QColor(str(colors['color1']))]
                    ]

            else:

                self.needle_center_bg = [
                                        [1, QColor(str(colors['color1']))]
                ]
        else:
            print("color1 is not defined")

    def setOuterCircleColor(self, **colors):
        if "color1" in colors and len(str(colors['color1'])) > 0:
            if "color2" in colors and len(str(colors['color2'])) > 0:
                if "color3" in colors and len(str(colors['color3'])) > 0:

                    self.outer_circle_bg = [
                        [0.0645161, QColor(str(colors['color3']))],
                        [0.37788, QColor(
                            str(colors['color1']))],
                        [1, QColor(str(colors['color2']))]
                    ]

                else:

                    self.outer_circle_bg = [
                        [0, QColor(str(colors['color2']))],
                        [1, QColor(str(colors['color2']))]
                    ]

            else:

                self.outer_circle_bg = [
                    [1, QColor(str(colors['color1']))]
                ]

        else:
            print("color1 is not defined")

    def rescale_method(self):
        if self.width() <= self.height():
            self.widget_diameter = self.width()
        else:
            self.widget_diameter = self.height()
        self.change_value_needle_style([QPolygon([
            QPoint(4, 30),
            QPoint(-4, 30),
            QPoint(-2, int(- self.widget_diameter / 2 * self.needle_scale_factor)),
            QPoint(0, int(- self.widget_diameter /
                   2 * self.needle_scale_factor - 6)),
            QPoint(2, int(- self.widget_diameter / 2 * self.needle_scale_factor))
        ])])

        self.scale_fontsize = int(
            self.initial_scale_fontsize * self.widget_diameter / 400)
        self.value_fontsize = int(
            self.initial_value_fontsize * self.widget_diameter / 400)

    def change_value_needle_style(self, design):
        # prepared for multiple needle instrument
        self.value_needle = []
        for i in design:
            self.value_needle.append(i)
        if not self.use_timer_event:
            self.update()

    def updateValue(self, value, mouse_controlled=False):
        # if not mouse_controlled:
        #     self.value = value
        #
        # if mouse_controlled:
        #     self.valueChanged.emit(int(value))

        if value <= self.minValue:
            self.value = self.minValue
        elif value >= self.maxValue:
            self.value = self.maxValue
        else:
            self.value = value
        # self.paintEvent("")
        self.valueChanged.emit(int(value))
        # print(self.value)

        # ohne timer: aktiviere self.update()
        if not self.use_timer_event:
            self.update()

    def updateAngleOffset(self, offset):
        self.angle_offset = offset
        if not self.use_timer_event:
            self.update()

    def center_horizontal(self, value):
        self.center_horizontal_value = value
        # print("horizontal: " + str(self.center_horizontal_value))

    def center_vertical(self, value):
        self.center_vertical_value = value
        # print("vertical: " + str(self.center_vertical_value))

    def setNeedleColor(self, R=50, G=50, B=50, Transparency=255):
        # Red: R = 0 - 255
        # Green: G = 0 - 255
        # Blue: B = 0 - 255
        # Transparency = 0 - 255
        self.NeedleColor = QColor(R, G, B, Transparency)
        self.NeedleColorReleased = self.NeedleColor

        if not self.use_timer_event:
            self.update()

    def setNeedleColorOnDrag(self, R=50, G=50, B=50, Transparency=255):
        # Red: R = 0 - 255
        # Green: G = 0 - 255
        # Blue: B = 0 - 255
        # Transparency = 0 - 255
        self.NeedleColorDrag = QColor(R, G, B, Transparency)

        if not self.use_timer_event:
            self.update()

    def setScaleValueColor(self, R=50, G=50, B=50, Transparency=255):
        # Red: R = 0 - 255
        # Green: G = 0 - 255
        # Blue: B = 0 - 255
        # Transparency = 0 - 255
        self.ScaleValueColor = QColor(R, G, B, Transparency)

        if not self.use_timer_event:
            self.update()

    def setDisplayValueColor(self, R=50, G=50, B=50, Transparency=255):
        # Red: R = 0 - 255
        # Green: G = 0 - 255
        # Blue: B = 0 - 255
        # Transparency = 0 - 255
        self.DisplayValueColor = QColor(R, G, B, Transparency)

        if not self.use_timer_event:
            self.update()

    def set_CenterPointColor(self, R=50, G=50, B=50, Transparency=255):
        self.CenterPointColor = QColor(R, G, B, Transparency)

        if not self.use_timer_event:
            self.update()

    def setEnableNeedlePolygon(self, enable=True):
        self.enable_Needle_Polygon = enable

        if not self.use_timer_event:
            self.update()

    def setEnableScaleText(self, enable=True):
        self.enable_scale_text = enable

        if not self.use_timer_event:
            self.update()

    def setEnableBarGraph(self, enable=True):
        self.enableBarGraph = enable

        if not self.use_timer_event:
            self.update()

    def setEnableValueText(self, enable=True):
        self.enable_value_text = enable

        if not self.use_timer_event:
            self.update()

    def setEnableCenterPoint(self, enable=True):
        self.enable_CenterPoint = enable

        if not self.use_timer_event:
            self.update()

    def setEnableScalePolygon(self, enable=True):
        self.enable_filled_Polygon = enable

        if not self.use_timer_event:
            self.update()

    def setEnableBigScaleGrid(self, enable=True):
        self.enable_big_scaled_marker = enable

        if not self.use_timer_event:
            self.update()

    def setEnableFineScaleGrid(self, enable=True):
        self.enable_fine_scaled_marker = enable

        if not self.use_timer_event:
            self.update()

    def setScalaCount(self, count):
        if count < 1:
            count = 1
        self.scalaCount = count

        if not self.use_timer_event:
            self.update()

    def setMinValue(self, min):
        if self.value < min:
            self.value = min
        if min >= self.maxValue:
            self.minValue = self.maxValue - 1
        else:
            self.minValue = min

        if not self.use_timer_event:
            self.update()

    def setMaxValue(self, max):
        if self.value > max:
            self.value = max
        if max <= self.minValue:
            self.maxValue = self.minValue + 1
        else:
            self.maxValue = max

        if not self.use_timer_event:
            self.update()

    def setScaleStartAngle(self, value):
        # Value range in DEG: 0 - 360
        self.scale_angle_start_value = value
        # print("startFill: " + str(self.scale_angle_start_value))

        if not self.use_timer_event:
            self.update()

    def setTotalScaleAngleSize(self, value):
        self.scale_angle_size = value
        # print("stopFill: " + str(self.scale_angle_size))

        if not self.use_timer_event:
            self.update()

    def setGaugeColorOuterRadiusFactor(self, value):
        self.gauge_color_outer_radius_factor = float(value) / 1000
        # print(self.gauge_color_outer_radius_factor)

        if not self.use_timer_event:
            self.update()

    def setGaugeColorInnerRadiusFactor(self, value):
        self.gauge_color_inner_radius_factor = float(value) / 1000
        # print(self.gauge_color_inner_radius_factor)

        if not self.use_timer_event:
            self.update()

    def set_scale_polygon_colors(self, color_array):
        # print(type(color_array))
        if 'list' in str(type(color_array)):
            self.scale_polygon_colors = color_array
        elif color_array == None:
            self.scale_polygon_colors = [[.0, Qt.transparent]]
        else:
            self.scale_polygon_colors = [[.0, Qt.transparent]]

        if not self.use_timer_event:
            self.update()

    ################################################################################################
    # GET MAXIMUM VALUE
    ################################################################################################
    def get_value_max(self):
        return self.maxValue

    def create_polygon_pie(self, outer_radius, inner_raduis, start, lenght, bar_graph=True):
        polygon_pie = QPolygonF()
        # start = self.scale_angle_start_value
        # start = 0
        # lenght = self.scale_angle_size
        # lenght = 180
        # inner_raduis = self.width()/4
        # print(start)
        n = 360     # angle steps size for full circle
        # changing n value will causes drawing issues
        w = 360 / n   # angle per step
        # create outer circle line from "start"-angle to "start + lenght"-angle
        x = 0
        y = 0

        # todo enable/disable bar graf here
        if not self.enableBarGraph and bar_graph:
            # float_value = ((lenght / (self.maxValue - self.minValue)) * (self.value - self.minValue))
            lenght = int(
                round((lenght / (self.maxValue - self.minValue)) * (self.value - self.minValue)))
            # print("f: %s, l: %s" %(float_value, lenght))
            pass

        # mymax = 0

        # add the points of polygon
        for i in range(lenght + 1):
            t = w * i + start - self.angle_offset
            x = outer_radius * math.cos(math.radians(t))
            y = outer_radius * math.sin(math.radians(t))
            polygon_pie.append(QPointF(x, y))
        # create inner circle line from "start + lenght"-angle to "start"-angle
        # add the points of polygon
        for i in range(lenght + 1):
            # print("2 " + str(i))
            t = w * (lenght - i) + start - self.angle_offset
            x = inner_raduis * math.cos(math.radians(t))
            y = inner_raduis * math.sin(math.radians(t))
            polygon_pie.append(QPointF(x, y))

        # close outer line
        polygon_pie.append(QPointF(x, y))
        return polygon_pie

    def draw_filled_polygon(self, outline_pen_with=0):
        if not self.scale_polygon_colors == None:
            painter_filled_polygon = QPainter(self)
            painter_filled_polygon.setRenderHint(QPainter.Antialiasing)
            # Koordinatenursprung in die Mitte der Flaeche legen
            painter_filled_polygon.translate(
                self.width() / 2, self.height() / 2)

            painter_filled_polygon.setPen(Qt.NoPen)

            self.pen.setWidth(outline_pen_with)
            if outline_pen_with > 0:
                painter_filled_polygon.setPen(self.pen)

            colored_scale_polygon = self.create_polygon_pie(
                ((self.widget_diameter / 2) - (self.pen.width() / 2)) *
                self.gauge_color_outer_radius_factor,
                (((self.widget_diameter / 2) - (self.pen.width() / 2))
                 * self.gauge_color_inner_radius_factor),
                self.scale_angle_start_value, self.scale_angle_size)

            gauge_rect = QRect(QPoint(0, 0), QSize(
                int(self.widget_diameter / 2 - 1), int(self.widget_diameter - 1)))
            grad = QConicalGradient(QPointF(0, 0), - self.scale_angle_size - self.scale_angle_start_value +
                                    self.angle_offset - 1)

            # todo definition scale color as array here
            for eachcolor in self.scale_polygon_colors:
                grad.setColorAt(eachcolor[0], eachcolor[1])
            # grad.setColorAt(.00, Qt.red)
            # grad.setColorAt(.1, Qt.yellow)
            # grad.setColorAt(.15, Qt.green)
            # grad.setColorAt(1, Qt.transparent)
            # self.brush = QBrush(QColor(255, 0, 255, 255))
            # grad.setStyle(Qt.Dense6Pattern)
            # painter_filled_polygon.setBrush(self.brush)
            painter_filled_polygon.setBrush(grad)

            painter_filled_polygon.drawPolygon(colored_scale_polygon)
            # return painter_filled_polygon

    def draw_icon_image(self):
        pass

    def draw_big_scaled_marker(self):
        my_painter = QPainter(self)
        my_painter.setRenderHint(QPainter.Antialiasing)
        # Koordinatenursprung in die Mitte der Flaeche legen
        my_painter.translate(self.width() / 2, self.height() / 2)

        # my_painter.setPen(Qt.NoPen)
        self.pen = QPen(self.bigScaleMarker)
        self.pen.setWidth(2)
        # # if outline_pen_with > 0:
        my_painter.setPen(self.pen)

        my_painter.rotate(self.scale_angle_start_value - self.angle_offset)
        steps_size = (float(self.scale_angle_size) / float(self.scalaCount))
        scale_line_outer_start = self.widget_diameter // 2
        scale_line_lenght = int((self.widget_diameter / 2) -
                                (self.widget_diameter / 20))
        # print(stepszize)
        for i in range(self.scalaCount + 1):
            my_painter.drawLine(scale_line_lenght, 0,
                                scale_line_outer_start, 0)
            my_painter.rotate(steps_size)

    def create_scale_marker_values_text(self):
        painter = QPainter(self)
        # painter.setRenderHint(QPainter.HighQualityAntialiasing)
        painter.setRenderHint(QPainter.Antialiasing)

        # Koordinatenursprung in die Mitte der Flaeche legen
        painter.translate(self.width() / 2, self.height() / 2)
        # painter.save()
        font = QFont(self.scale_fontname, self.scale_fontsize, QFont.Bold)
        fm = QFontMetrics(font)

        pen_shadow = QPen()

        pen_shadow.setBrush(self.ScaleValueColor)
        painter.setPen(pen_shadow)

        text_radius_factor = 0.8
        text_radius = self.widget_diameter / 2 * text_radius_factor

        scale_per_div = int((self.maxValue - self.minValue) / self.scalaCount)

        angle_distance = (float(self.scale_angle_size) /
                          float(self.scalaCount))
        for i in range(self.scalaCount + 1):
            # text = str(int((self.maxValue - self.minValue) / self.scalaCount * i))
            text = str(int(self.minValue + scale_per_div * i))
            w = fm.width(text) + 1
            h = fm.height()
            painter.setFont(QFont(self.scale_fontname,
                            self.scale_fontsize, QFont.Bold))
            angle = angle_distance * i + \
                float(self.scale_angle_start_value - self.angle_offset)
            x = text_radius * math.cos(math.radians(angle))
            y = text_radius * math.sin(math.radians(angle))
            # print(w, h, x, y, text)

            painter.drawText(int(x - w / 2), int(y - h / 2), int(w),
                             int(h), Qt.AlignCenter, text)
        # painter.restore()

    def create_fine_scaled_marker(self):
        #  Description_dict = 0
        my_painter = QPainter(self)

        my_painter.setRenderHint(QPainter.Antialiasing)
        # Koordinatenursprung in die Mitte der Flaeche legen
        my_painter.translate(self.width() / 2, self.height() / 2)

        my_painter.setPen(self.fineScaleColor)
        my_painter.rotate(self.scale_angle_start_value - self.angle_offset)
        steps_size = (float(self.scale_angle_size) /
                      float(self.scalaCount * self.scala_subdiv_count))
        scale_line_outer_start = self.widget_diameter // 2
        scale_line_lenght = int(
            (self.widget_diameter / 2) - (self.widget_diameter / 40))
        for i in range((self.scalaCount * self.scala_subdiv_count) + 1):
            my_painter.drawLine(scale_line_lenght, 0,
                                scale_line_outer_start, 0)
            my_painter.rotate(steps_size)

    def create_values_text(self):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.HighQualityAntialiasing)
        # painter.setRenderHint(QPainter.Antialiasing)

        painter.translate(self.width() / 2, self.height() / 2)
        font = QFont(self.value_fontname, self.value_fontsize, QFont.Bold)
        fm = QFontMetrics(font)

        pen_shadow = QPen()

        pen_shadow.setBrush(self.DisplayValueColor)
        painter.setPen(pen_shadow)

        text_radius = self.widget_diameter / 2 * self.text_radius_factor
        text = str(int(self.value))
        w = fm.width(text) + 1
        h = fm.height()
        painter.setFont(QFont(self.value_fontname,
                        self.value_fontsize, QFont.Bold))
        angle_end = float(self.scale_angle_start_value +
                          self.scale_angle_size - 360)
        angle = (angle_end - self.scale_angle_start_value) / \
            2 + self.scale_angle_start_value

        x = text_radius * math.cos(math.radians(angle))
        y = text_radius * math.sin(math.radians(angle))
        # print(w, h, x, y, text)
        painter.drawText(int(x - w / 2), int(y - h / 2), int(w),
                         int(h), Qt.AlignCenter, text)

    def create_units_text(self):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.HighQualityAntialiasing)
        # painter.setRenderHint(QPainter.Antialiasing)

        painter.translate(self.width() / 2, self.height() / 2)
        font = QFont(self.value_fontname, int(
            self.value_fontsize / 2.5), QFont.Bold)
        fm = QFontMetrics(font)

        pen_shadow = QPen()

        pen_shadow.setBrush(self.DisplayValueColor)
        painter.setPen(pen_shadow)

        text_radius = self.widget_diameter / 2 * self.text_radius_factor

        text = str(self.units)
        w = fm.width(text) + 1
        h = fm.height()
        painter.setFont(QFont(self.value_fontname, int(
            self.value_fontsize / 2.5), QFont.Bold))

        angle_end = float(self.scale_angle_start_value +
                          self.scale_angle_size + 180)
        angle = (angle_end - self.scale_angle_start_value) / \
            2 + self.scale_angle_start_value

        x = text_radius * math.cos(math.radians(angle))
        y = text_radius * math.sin(math.radians(angle))
        # print(w, h, x, y, text)
        painter.drawText(int(x - w / 2), int(y - h / 2), int(w),
                         int(h), Qt.AlignCenter, text)


    def draw_big_needle_center_point(self, diameter=30):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.translate(self.width() / 2, self.height() / 2)
        painter.setPen(Qt.NoPen)
        colored_scale_polygon = self.create_polygon_pie(
            ((self.widget_diameter / 8) - (self.pen.width() / 2)),
            0,
            self.scale_angle_start_value, 360, False)

        grad = QConicalGradient(QPointF(0, 0), 0)

        # todo definition scale color as array here
        for eachcolor in self.needle_center_bg:
            grad.setColorAt(eachcolor[0], eachcolor[1])
        painter.setBrush(grad)

        painter.drawPolygon(colored_scale_polygon)
    def draw_outer_circle(self, diameter=30):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        painter.translate(self.width() / 2, self.height() / 2)
        painter.setPen(Qt.NoPen)
        colored_scale_polygon = self.create_polygon_pie(
            ((self.widget_diameter / 2) - (self.pen.width())),
            (self.widget_diameter / 6),
            self.scale_angle_start_value / 10, 360, False)

        radialGradient = QRadialGradient(QPointF(0, 0), self.width())

        for eachcolor in self.outer_circle_bg:
            radialGradient.setColorAt(eachcolor[0], eachcolor[1])

        painter.setBrush(radialGradient)

        painter.drawPolygon(colored_scale_polygon)

    ################################################################################################
    # NEEDLE POINTER
    ################################################################################################

    def draw_needle(self):
        painter = QPainter(self)
        # painter.setRenderHint(QtGui.QPainter.HighQualityAntialiasing)
        painter.setRenderHint(QPainter.Antialiasing)
        # Koordinatenursprung in die Mitte der Flaeche legen
        painter.translate(self.width() / 2, self.height() / 2)
        painter.setPen(Qt.NoPen)
        painter.setBrush(self.NeedleColor)
        painter.rotate(((self.value - self.value_offset - self.minValue) * self.scale_angle_size /
                        (self.maxValue - self.minValue)) + 90 + self.scale_angle_start_value)

        painter.drawConvexPolygon(self.value_needle[0])

    ###############################################################################################
    # EVENTS
    ###############################################################################################

    ################################################################################################
    # ON WINDOW RESIZE
    ################################################################################################
    def resizeEvent(self, event):
        # self.resized.emit()
        # return super(self.parent, self).resizeEvent(event)
        # print("resized")
        # print(self.width())
        self.rescale_method()
        # self.emit(QtCore.SIGNAL("resize()"))
        # print("resizeEvent")

    ################################################################################################
    # ON PAINT EVENT
    ################################################################################################
    def paintEvent(self, event):
        # Main Drawing Event:
        # Will be executed on every change
        # vgl http://doc.qt.io/qt-4.8/qt-demos-affine-xform-cpp.html
        # print("event", event)

        self.draw_outer_circle()
        self.draw_icon_image()
        # colored pie area
        if self.enable_filled_Polygon:
            self.draw_filled_polygon()

        # draw scale marker lines
        if self.enable_fine_scaled_marker:
            self.create_fine_scaled_marker()
        if self.enable_big_scaled_marker:
            self.draw_big_scaled_marker()

        # draw scale marker value text
        if self.enable_scale_text:
            self.create_scale_marker_values_text()

        # Display Value
        if self.enable_value_text:
            self.create_values_text()
            self.create_units_text()

        # draw needle 1
        if self.enable_Needle_Polygon:
            self.draw_needle()

        # Draw Center Point
        if self.enable_CenterPoint:
            self.draw_big_needle_center_point(
                diameter=(self.widget_diameter / 6))

    ###############################################################################################
    # MOUSE EVENTS
    ###############################################################################################

    def setMouseTracking(self, flag):
        def recursive_set(parent):
            for child in parent.findChildren(QObject):
                try:
                    child.setMouseTracking(flag)
                except:
                    pass
                recursive_set(child)

        QWidget.setMouseTracking(self, flag)
        recursive_set(self)

    def mouseReleaseEvent(self, QMouseEvent):
        self.NeedleColor = self.NeedleColorReleased

        if not self.use_timer_event:
            self.update()
        pass

    ########################################################################
    # MOUSE LEAVE EVENT
    ########################################################################
    def leaveEvent(self, event):
        self.NeedleColor = self.NeedleColorReleased
        self.update()

    def mouseMoveEvent(self, event):
        x, y = event.x() - (self.width() / 2), event.y() - (self.height() / 2)
        # print(event.x(), event.y(), self.width(), self.height())
        if not x == 0:
            angle = math.atan2(y, x) / math.pi * 180
            # winkellaenge der anzeige immer positiv 0 - 360deg
            # min wert + umskalierter wert
            value = (float(math.fmod(angle - self.scale_angle_start_value + 720, 360)) /
                     (float(self.scale_angle_size) / float(self.maxValue - self.minValue))) + self.minValue
            temp = value
            fmod = float(
                math.fmod(angle - self.scale_angle_start_value + 720, 360))
            state = 0
            if (self.value - (self.maxValue - self.minValue) * self.valueNeedleSnapzone) <= \
                    value <= \
                    (self.value + (self.maxValue - self.minValue) * self.valueNeedleSnapzone):
                self.NeedleColor = self.NeedleColorDrag
                # todo: evtl ueberpruefen
                #
                state = 9
                # if value >= self.maxValue and self.last_value < (self.maxValue - self.minValue) / 2:
                if value >= self.maxValue and self.last_value < (self.maxValue - self.minValue) / 2:
                    state = 1
                    value = self.maxValue
                    self.last_value = self.minValue
                    self.valueChanged.emit(int(value))

                elif value >= self.maxValue >= self.last_value:
                    state = 2
                    value = self.maxValue
                    self.last_value = self.maxValue
                    self.valueChanged.emit(int(value))

                else:
                    state = 3
                    self.last_value = value
                    self.valueChanged.emit(int(value))

                self.updateValue(value)


#!####################################################################################################################################################### PİTCH END

#!####################################################################################################################################################### PİTCH END

#!####################################################################################################################################################### PİTCH END

#!####################################################################################################################################################### PİTCH END

#!####################################################################################################################################################### PİTCH END

#!####################################################################################################################################################### PİTCH END

#!####################################################################################################################################################### PİTCH END

#!####################################################################################################################################################### PİTCH END

#!####################################################################################################################################################### PİTCH END

#!####################################################################################################################################################### PİTCH END

#!####################################################################################################################################################### PİTCH END

#!####################################################################################################################################################### PİTCH END

#!####################################################################################################################################################### PİTCH END

#!####################################################################################################################################################### PİTCH END

#!####################################################################################################################################################### PİTCH END

#!####################################################################################################################################################### PİTCH END

#!####################################################################################################################################################### PİTCH END

#!####################################################################################################################################################### PİTCH END

#!####################################################################################################################################################### PİTCH END

#!####################################################################################################################################################### PİTCH END

#!####################################################################################################################################################### PİTCH END

#!####################################################################################################################################################### PİTCH END

#!####################################################################################################################################################### PİTCH END

#!####################################################################################################################################################### PİTCH END

#!####################################################################################################################################################### PİTCH END

#!####################################################################################################################################################### PİTCH END

#!####################################################################################################################################################### PİTCH END

#!####################################################################################################################################################### PİTCH END

#!####################################################################################################################################################### PİTCH END

#!####################################################################################################################################################### PİTCH END

#!####################################################################################################################################################### PİTCH END

#!####################################################################################################################################################### PİTCH END

#!####################################################################################################################################################### PİTCH END

#!####################################################################################################################################################### PİTCH END


class karayelPage(QMainWindow):

    
    def __init__(self) -> None:
        super().__init__()
        self.homeForm = Ui_KarayelWindow()#tasarım dosyası(karayel_ui) tanıtıldı
        self.homeForm.setupUi(self)

        while True:
            batarya=vehicle.battery.voltage
            self.homeForm.bataryaPB.setValue(round(batarya,1))
            break
######################## ALTTİTUDE GAUGE ########################
        altGauge = AnalogGauge_alt() # Gauge eklemek için bir widget class'ını ekle
        altGaugeLayout = QVBoxLayout()
        self.homeForm.ykseklikW.setLayout(altGaugeLayout)# Ana pencereye layout ekle
        altGaugeLayout.addWidget(altGauge)
        #################################################################
        
        ######################## GROUNDSPEED GAUGE ######################## 
        groundGauge = AnalogGauge_ground()
        groundGaugeLayout = QVBoxLayout()
        self.homeForm.groundSW.setLayout(groundGaugeLayout)# Ana pencereye layout ekle
        groundGaugeLayout.addWidget(groundGauge)
        #################################################################
        
        ######################## AİRSPEED GAUGE ######################## 
        airSpeedGauge = AnalogGauge_airSpeed()
        airSpeedGaugeLayout = QVBoxLayout()
        self.homeForm.airSpeedhizW.setLayout(airSpeedGaugeLayout)# Ana pencereye layout ekle
        airSpeedGaugeLayout.addWidget(airSpeedGauge)
        #################################################################
        
        ######################## ROLL GAUGE ######################## 
        rollGauge = AnalogGauge_roll()
        rollGaugeLayout = QVBoxLayout()
        self.homeForm.rollDegeriW.setLayout(rollGaugeLayout)# Ana pencereye layout ekle
        rollGaugeLayout.addWidget(rollGauge)
        #################################################################
        
        ######################## YAW GAUGE ######################## 
        yawGauge = AnalogGauge_yaw()
        yawGaugeLayout = QVBoxLayout()
        self.homeForm.yawDegeriW.setLayout(yawGaugeLayout)# Ana pencereye layout ekle
        yawGaugeLayout.addWidget(yawGauge)
        #################################################################
        
        ######################## PİTCH GAUGE ######################## 
        pitchGauge = AnalogGauge_pitch()
        pitchGaugeLayout = QVBoxLayout()
        self.homeForm.pitchdegeriW.setLayout(pitchGaugeLayout)# Ana pencereye layout ekle
        pitchGaugeLayout.addWidget(pitchGauge)
        #################################################################
        

##############################################################################################################################
##############################################################################################################################     
########-----YER KONTROL İSTASYONU-----#########-----YER KONTROL İSTASYONU-----########-----YER KONTROL İSTASYONU-----########
##############################################################################################################################
############################################################################################################################## 

        """layoutdataFlight = QVBoxLayout()
        self.setLayout(layoutdataFlight)"""
        
        # while True:
        #     mapObj = folium.Map(location=[home.lat,home.lon],
        #              zoom_start=16, tiles=None)
        #     folium.Marker(location=[home.lat,home.lon], tooltip='').add_to(mapObj)
        #     break

        # view widget'ını layout'a ekleyelim
        #layoutdataFlight.addWidget(view)
        ###############################################################

        layoutt = QVBoxLayout()
        layoutt.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layoutt)

        # Veritabanı bağlantısı
        conn = sql.connect(
                host = "localhost",
                user="root",
                password="root",
                database="karayel" )
        im = conn.cursor()
        
        mapObj = folium.Map(location=[40.77876116603416, 30.366209016770387],
                    zoom_start=16, tiles=None)
        
        # çizim yapmak için kullanıyoruz
        draw = Draw(
            export=True,
            filename="my_data.geojson",
            position="topleft",
            draw_options={"polyline": {"allowIntersection": True}}, #kesişim olmamasını istiyorsak false yaparız
            edit_options={"poly": {"allowIntersection": True}},
        )
        draw.add_to(mapObj)
        
        
        formatter = "function(num) {return L.Util.formatNum(num, ) + ' º ';};"

        MousePosition(
            position="topright",
            separator=" | ",
            empty_string="NaN",
            lng_first=True,
            num_digits=20,
            prefix="Coordinates:",
            lat_formatter=formatter,
            lng_formatter=formatter,
        ).add_to(mapObj)

        

      
        minimap = plugins.MiniMap()
        mapObj.add_child(minimap)
        

        # add tile layers
        folium.TileLayer('openstreetmap').add_to(mapObj)
        folium.TileLayer('stamenterrain', attr="stamenterrain").add_to(mapObj)
        folium.TileLayer('stamenwatercolor', attr="stamenwatercolor").add_to(mapObj)
        folium.TileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', name='CartoDB.DarkMatter', attr="CartoDB.DarkMatter").add_to(mapObj)

        
        # add layers control over the map
        folium.LayerControl().add_to(mapObj)

        data = io.BytesIO()
        mapObj.save(data, close_file=False)
        
        mp = MousePosition()
        mp.add_to(mapObj)
        # bu kısım sadece konum verilerini ekrana göstermek için kullanılıyor
        class WebEnginePage(QtWebEngineWidgets.QWebEnginePage):
            def javaScriptConsoleMessage(self, level, message, lineNumber, sourceID):
                    sil = "TRUNCATE TABLE koordinat"
                    im.execute(sil)
                    conn.commit()
                    coords_dict = json.loads(message)
                    print(*coords_dict['geometry']['coordinates'])
                    coords = coords_dict['geometry']['coordinates']
                    for pos in coords:
                        ekle = "INSERT INTO koordinat (KoordinatID,X,Y) VALUES (NULL,'{}','{}')" 
                        data1=(pos[0],pos[1])
                        ekle = ekle.format(*data1)
                        im.execute(ekle)
                        conn.commit()

                        

        view = QtWebEngineWidgets.QWebEngineView()
        page = WebEnginePage(view)
        map_dataFlight_html = mapObj._repr_html_()
        view.setHtml(map_dataFlight_html)
        #view.setGeometry(0, 0, 500, 370)
        #view.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        view.setPage(page)
        view.setHtml(data.getvalue().decode())
        mapObj.save('map.html')
        layoutt.addWidget(view)
        self.homeForm.mapW.setLayout(layoutt)

###################################################################################################################
        self.window_width, self.window_height = 800, 800
        self.setMinimumSize(self.window_width, self.window_height)

        layouttt = QVBoxLayout()
        layouttt.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layouttt)

        while True:
            mapObj = folium.Map(location=[vehicle.location.global_frame.lat,vehicle.location.global_frame.lon],
                     zoom_start=16, tiles=None)
            folium.Marker(location=[vehicle.location.global_frame.lat,vehicle.location.global_frame.lon], tooltip='New York City').add_to(mapObj)
            break


################-----silindi-----#################        
        # # Veritabanı bağlantısı
        # conn = mysql.connector.connect(
        #         host = "localhost",
        #         user="root",
        #         password="gulcann",
        #         database="karayel" )
        

        #mapObj = folium.Map(location=[40.77876116603416, 30.366209016770387],
        #        zoom_start=16, tiles=None)
            
         
        
        # çizim yapmak için kullanıyoruz
        # draw = Draw(
        #     export=True,
        #     filename="my_data.geojson",
        #     position="topleft",
        #     draw_options={"polyline": {"allowIntersection": True}}, #kesişim olmamasını istiyorsak false yaparız
        #     edit_options={"poly": {"allowIntersection": True}},
        # )
        # draw.add_to(mapObj)
        
        
        formatter = "function(num) {return L.Util.formatNum(num, ) + ' º ';};"

        MousePosition(
            position="topright",
            separator=" | ",
            empty_string="NaN",
            lng_first=True,
            num_digits=20,
            prefix="Coordinates:",
            lat_formatter=formatter,
            lng_formatter=formatter,
        ).add_to(mapObj)

        

      
        # minimap = plugins.MiniMap()
        # mapObj.add_child(minimap)
        
#################-----silindi-----#########################
        # # add tile layers
        folium.TileLayer('openstreetmap').add_to(mapObj)
        # folium.TileLayer('stamenterrain', attr="stamenterrain").add_to(mapObj)
        # folium.TileLayer('stamenwatercolor', attr="stamenwatercolor").add_to(mapObj)
        # folium.TileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', name='CartoDB.DarkMatter', attr="CartoDB.DarkMatter").add_to(mapObj)

        
        # # add layers control over the map
        # folium.LayerControl().add_to(mapObj)

        data = io.BytesIO()
        mapObj.save(data, close_file=False)
        
        mp = MousePosition()
        mp.add_to(mapObj)

        # bu kısım sadece konum verilerini ekrana göstermek için kullanılıyor
        class WebEnginePage(QtWebEngineWidgets.QWebEnginePage):
            def javaScriptConsoleMessage(self, level, message, lineNumber, sourceID):
                coords_dict = json.loads(message)
                coords = coords_dict['geometry']['coordinates'][0]
                print(coords)

        # view = QtWebEngineWidgets.QWebEngineView()
        # page = WebEnginePage(view)
        # view.setPage(page)
        # view.setHtml(data.getvalue().decode())
        # # view widget'ını layout'a ekleyelim
        # layouttt.addWidget(view)

        
        view = QtWebEngineWidgets.QWebEngineView()
        page = WebEnginePage(view)
        map_dataFlight_html = mapObj._repr_html_()
        view.setHtml(map_dataFlight_html)
        #view.setGeometry(0, 0, 500, 370)
        #view.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        #view.setPage(page)
        view.setHtml(data.getvalue().decode())
        mapObj.save('map.html')
        layouttt.addWidget(view)
        self.homeForm.droneharitaW.setLayout(layouttt)

###################################################################################################################
        # self.timerrr = QTimer()
        # self.timerrr.timeout.connect(self.guncelle)
        self.camera=None


        self.player = QMediaPlayer()#içine ses dosyalarını atadığımız QMediaPlayer veri tipinde bir nesne oluşturulması.
########-----default windows pencere kenarlıkları, close-max-min butonu ve genişletme özellğinin kaldırılması-----########       
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.homeForm.titleBarW.mouseMoveEvent = self.MoveWindow
        self.gripSize = 50
        self.grip = QtWidgets.QSizeGrip(self)
        self.grip.resize(self.gripSize, self.gripSize)
##################################-----pencere ilk açıldığındaki visible ayarları-----####################################        
        # self.homeForm.Acilis.setVisible(False)
        # self.homeForm.AnaSayfa.setVisible(False)
        # self.homeForm.YerKontrol.setVisible(False)
        # self.homeForm.Gorev.setVisible(False)
        # self.homeForm.Ayarlar.setVisible(False)
        self.homeForm.ucusVeriLbl.setMaximumWidth(3)
        self.homeForm.ucusVeriLbl.setMinimumWidth(3)
        self.homeForm.ucusVeriLbl.setStyleSheet('background-color: {}'.format(QColor(222, 222, 222).name()))
        self.homeForm.kaydetBtn.clicked.connect(self.kullanici_ayarlari)
##################################-----close-max-min fonkisyonlarının çağrılması-----#####################################        
        self.homeForm.logoutBtn.clicked.connect(self.cikis)
        self.homeForm.closeBtn.clicked.connect(self.cikis)
        self.homeForm.maximizeBtn.clicked.connect(self.maximize)
        self.homeForm.minimizeBtn.clicked.connect(self.minimize)
#######################################-----profil-side bar fonksiyonlarının çağrılması-----##############################
        self.homeForm.ProfileW.setMaximumWidth(0)#penceremiz ilk açıldığında profil barımızın gizli kalması için 
        self.homeForm.userBtn.clicked.connect(self.profilBarGoster)
        self.homeForm.menuBtn.clicked.connect(self.toggleSideBar)
##################################-----visible fonkisyonlarının çağrılması-----###########################################        
        self.homeForm.hakkimizdaBtn.clicked.connect(self.showHomePage)
        self.homeForm.ucusVeriBtn.clicked.connect(self.showUcusVeri)
        self.homeForm.yerKontrolBtn.clicked.connect(self.showYerKontrol)
        self.homeForm.gorevBtn.clicked.connect(self.showGorev)
        self.homeForm.ayarlarBtn.clicked.connect(self.showAyarlar)

##################################-----load data fonkisyonun çağrılması-----#########################################        
        self.homeForm.lightBtn.clicked.connect(self.loaddata)

##################################-----ucus verileri fonkisyonun çağrılması-----#########################################        
    #    self.homeForm.baglanBtn.clicked.connect(self.Baglan)
##################################-----goruntu isleme fonkisyonun çağrılması-----#########################################        
        self.homeForm.acBtn.clicked.connect(self.start_camera)
##################################-----otonom kod fonkisyonun çağrılması-----#############################################        
        # self.homeForm.gorevStartBtn.clicked.connect(self.otonomu_calistir)
        # self.homeForm.gorevStartBtn_2.clicked.connect(self.otonomu_calistir)
##############################-----dil değiştiren fonkisyonların çağrılması-----##########################################        
        self.homeForm.DilSecenekCB.currentIndexChanged.connect(self.dilDegistir)
##############################-----mail gönderen fonsiyonun çağrılması-----###############################################        
        self.homeForm.gonderBtn.clicked.connect(self.mailGonder)
##############################-----butona ses ekleyen fonkisyonların çağrılması-----######################################        
        self.homeForm.hakkimizdaBtn.clicked.connect(self.play_sound)
        self.homeForm.ucusVeriBtn.clicked.connect(self.play_sound)
        self.homeForm.yerKontrolBtn.clicked.connect(self.play_sound)
        self.homeForm.gorevBtn.clicked.connect(self.play_sound)
        self.homeForm.ayarlarBtn.clicked.connect(self.play_sound)
        self.homeForm.menuBtn.clicked.connect(self.play_soundd)
        self.homeForm.myprofileBtn.clicked.connect(self.play_Logout_Sound)
        self.homeForm.userBtn.clicked.connect(self.play_Logout_Sound)
        self.homeForm.SessizRB.clicked.connect(self.sesi_kapat)
        self.homeForm.GenelRB.clicked.connect(self.sesi_ac)
        self.homeForm.GenelRB.setChecked(True)
##############################-----label reengini değiştiren fonkisyonların çağrılması-----###############################        

        self.homeForm.hakkimizdaBtn.clicked.connect(self.ucusVerilbl)
        self.homeForm.ucusVeriBtn.clicked.connect(self.ucusVerilbl)
        self.homeForm.gorevBtn.clicked.connect(self.ucusVerilbl)
        self.homeForm.yerKontrolBtn.clicked.connect(self.ucusVerilbl)
        self.homeForm.ayarlarBtn.clicked.connect(self.ucusVerilbl)

        self.homeForm.hakkimizdaBtn.clicked.connect(self.yerKontrollbl)
        self.homeForm.ucusVeriBtn.clicked.connect(self.yerKontrollbl)
        self.homeForm.gorevBtn.clicked.connect(self.yerKontrollbl)
        self.homeForm.yerKontrolBtn.clicked.connect(self.yerKontrollbl)
        self.homeForm.ayarlarBtn.clicked.connect(self.yerKontrollbl)

        self.homeForm.hakkimizdaBtn.clicked.connect(self.Gorevlbl)
        self.homeForm.ucusVeriBtn.clicked.connect(self.Gorevlbl)
        self.homeForm.gorevBtn.clicked.connect(self.Gorevlbl)
        self.homeForm.yerKontrolBtn.clicked.connect(self.Gorevlbl)
        self.homeForm.ayarlarBtn.clicked.connect(self.Gorevlbl)

        self.homeForm.hakkimizdaBtn.clicked.connect(self.hakkimizdalbl)
        self.homeForm.ucusVeriBtn.clicked.connect(self.hakkimizdalbl)
        self.homeForm.gorevBtn.clicked.connect(self.hakkimizdalbl)
        self.homeForm.yerKontrolBtn.clicked.connect(self.hakkimizdalbl)
        self.homeForm.ayarlarBtn.clicked.connect(self.hakkimizdalbl)

        self.homeForm.hakkimizdaBtn.clicked.connect(self.ayarlarlbl)
        self.homeForm.ucusVeriBtn.clicked.connect(self.ayarlarlbl)
        self.homeForm.gorevBtn.clicked.connect(self.ayarlarlbl)
        self.homeForm.yerKontrolBtn.clicked.connect(self.ayarlarlbl)
        self.homeForm.ayarlarBtn.clicked.connect(self.ayarlarlbl)
#######-----batarya göstergesi-----#######-----batarya göstergesi-----#######-----batarya göstergesi-----#######
    #     # Hız göstergesi oluşturma ve ayarları
    #     self.progress_bar = QProgressBar(self)
    #     self.progress_bar.setMaximum(100)
    #     self.progress_bar.setValue(100)

    #     # Hız göstergesi güncelleme fonksiyonu
    #     self.update_progress_bar()

    # def update_progress_bar(self):
    #     """ Hız göstergesini güncelleme fonksiyonu """
    #     value = self.progress_bar.value()#value=vecihle.batteryLevel
    #     if value > 100:
    #         value = 0
    #     self.progress_bar.setValue(value)
    #     # 100ms sonra tekrar güncelleme
    #     QTimer.singleShot(100, self.update_progress_bar)
    #     pass
    #     layout = QVBoxLayout()
    #     layout.addWidget(self.progress_bar)
    #     layout.setContentsMargins(0, 0, 0, 0)
    #     self.homeForm.bataryaSeviyeW.setLayout(layout)

############-----matplotlib-----################-----matplotlib-----##############-----matplotlib-----###############
        # Create the matplotlib figure
        self.figure = Figure(figsize=(5, 4), dpi=100)
        self.figure.set_edgecolor("#323232")
        self.figure.set_facecolor("#505050")
        self.canvas = FigureCanvas(self.figure)

        # Add the matplotlib figure to the window
        
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        layout.setContentsMargins(0, 0, 0, 0)
        self.homeForm.suBilgiCenterW.setLayout(layout)

        # Create the line chart
        self.ax = self.figure.add_subplot(111)
        # self.ax.set_facecolor('#323232')
        self.xdata, self.ydata = [], []
        self.line, = self.ax.plot([], [], 'ro')

        # Start the animation timer
        self.timer = QTimer()
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.update_figure)

        
    def update_figure(self):
    # MySQL'den verileri seçme
        try:
            mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                password="root",
                database="karayel",
                auth_plugin='mysql_native_password' # Eski kimlik doğrulama mekanizmasını kullan
            )
            mycursor = mydb.cursor()
            mycursor.execute("SELECT SonucID, Sonuc FROM testsonuc")
            data = mycursor.fetchall()

            # Verileri ayrıştırma
            xdata = []
            ydata = []
            for row in data:
                xdata.append(row[0])
                ydata.append(row[1])

            # Update the line chart
            self.line.set_data(xdata, ydata)
            self.ax.relim()
            self.ax.autoscale_view()

            # Refresh the canvas to show the updated line chart
            self.canvas.draw()

        except mysql.connector.Error as error:
            print("MySQL Hatası: {}".format(error))


        # mydb = mysql.connector.connect(
        #     host="localhost",
        #     user="root",
        #     password="root",
        #     database="karayel",
        #     auth_plugin='mysql_native_password' # Eski kimlik doğrulama mekanizmasını kullan
        # )

        # with open("test.txt", "r") as file:
        #     veriler = file.readlines()

        # mycursor = mydb.cursor()

        # for veri in veriler:
        #     sql = "INSERT INTO testsonuc (Sonuc) VALUES (%s)"
        #     val = (veri.strip(), )
        #     mycursor.execute(sql, val)


        # mydb = mysql.connector.connect(
        #     host="localhost",
        #     user="root",
        #     password="root",
        #     database="karayel",
        #     auth_plugin='mysql_native_password' # Eski kimlik doğrulama mekanizmasını kullan
        # )


        # # MySQL'den verileri seçme
        # mycursor = mydb.cursor()
        # mycursor.execute("SELECT SonucID, Sonuc FROM testsonuc")
        # data = mycursor.fetchall()

        # # Verileri ayrıştırma
        # ID = []
        # Sonuc = []
        # for row in data:
        #     ID.append(row[0])
        #     Sonuc.append(row[1])

        # # Görselleştirme
        # self.plt = plt.scatter(ID,Sonuc, cmap='viridis')
        # layout = QVBoxLayout()
        # layout.addWidget(self.plt)
        # self.homeForm.suBilgiCenterW.setLayout(layout)
        

        # mydb.commit()
        # mydb.close()


    #     # Create the matplotlib figure
    #     self.figure = Figure(figsize=(5, 4), dpi=100)
    #     self.canvas = FigureCanvas(self.figure)

    #     # Add the matplotlib figure to the window
    #     layout = QVBoxLayout()
    #     layout.addWidget(self.canvas)
    #     self.homeForm.suBilgiCenterW.setLayout(layout)

    #     # # Create the bar chart
    #     # ax = self.figure.add_subplot(111)
    #     # data = [1, 2, 3, 4, 5]
    #     # ax.bar(range(len(data)), data)

    #     # # Refresh the canvas to show the bar chart
    #     # self.canvas.draw()

    #     # Create the line chart
    #     self.ax = self.figure.add_subplot(111)
    #     self.xdata, self.ydata = [], []
    #     self.line, = self.ax.plot([], [], 'ro')

    #     # Start the animation timer
    #     self.timer = QTimer()
    #     self.timer.setInterval(100)
    #     self.timer.timeout.connect(self.update_figure)
    #     self.timer.start()

    # def update_figure(self):
    #     # Generate new data

    #     ########-----gülcan/süleyman buraya veritabanından veri çekmesi lazım-----############### 
    #     x = np.random.rand()#way pointleri buraya koyarız
    #     y = np.random.rand()#ardunio değerlerini buraya koyarız

    #     # Update the line chart
    #     self.xdata.append(x)
    #     self.ydata.append(y)
    #     self.line.set_data(self.xdata, self.ydata)
    #     self.ax.relim()
    #     self.ax.autoscale_view()

    #     # Refresh the canvas to show the updated line chart
    #     self.canvas.draw()




        
########################################################################################################################################
########################################################################################################################################
##############################-----FONKSİYONLAR AŞAĞIDADIR-----############-----FONKSİYONLAR AŞAĞIDADIR-----############################
##############################-----FONKSİYONLAR AŞAĞIDADIR-----############-----FONKSİYONLAR AŞAĞIDADIR-----############################
##############################-----FONKSİYONLAR AŞAĞIDADIR-----############-----FONKSİYONLAR AŞAĞIDADIR-----############################
########################################################################################################################################
########################################################################################################################################

    ###########################################################################

    def loaddata(self):
        konum_cek = "SELECT * FROM koordinat"
        im.execute(konum_cek)
        data = im.fetchall()
        self.homeForm.konumVeriTW.setRowCount(len(data))
        self.homeForm.konumVeriTW.setColumnCount(2)
        self.homeForm.konumVeriTW.setHorizontalHeaderLabels(["ID","X","Y"])


        for i, row in enumerate(data):
            for j in range(len(row)):
                item = QTableWidgetItem(str(row[j]))
                self.homeForm.konumVeriTW.setItem(i, j, item)
        conn.commit()
        conn.close()

    

########################################-----pencere genişliği ayaralama fonksiyonu-----###############################
    def MoveWindow(self,event):
        if self.isMaximized() == False:
            self.move(self.pos() + event.globalPos() - self.clickPosition)
            self.clickPosition = event.globalPos()
            event.accept()
            pass
    def mousePressEvent(self,event):
        self.clickPosition = event.globalPos()
        pass

    def resizeEvent(self, event):
        rect = self.rect()
        self.grip.move(rect.right() - self.gripSize, rect.bottom() - self.gripSize)
    
#######################################-----close max min buton fonksiyonları-----########################################

    def minimize(self):
        self.setWindowState(QtCore.Qt.WindowMinimized)
    
    def maximize(self):
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()

    def cikis(self):
        self.close()

#################################-----side bar label renk değiştirme fonksiyonları-----###################################
    def hakkimizdalbl(self):
        if self.homeForm.Hakkimizda.isVisible()==True:
            self.homeForm.hakkimizdaLbl.setMaximumWidth(3)
            self.homeForm.hakkimizdaLbl.setMinimumWidth(3)
            self.homeForm.hakkimizdaLbl.setStyleSheet('background-color: {}'.format(QColor(222, 222, 222).name()))
            self.homeForm.ucusVeriLbl.setMinimumWidth(1)
            self.homeForm.ucusVeriLbl.setMaximumWidth(1)
            self.homeForm.ucusVeriLbl.setStyleSheet('background-color: {}'.format(QColor(38, 38, 38).name()))
        elif self.homeForm.Hakkimizda.isVisible()==False:
            self.homeForm.hakkimizdaLbl.setMinimumWidth(1)
            self.homeForm.hakkimizdaLbl.setMaximumWidth(1)
            self.homeForm.hakkimizdaLbl.setStyleSheet('background-color: {}'.format(QColor(38, 38, 38).name()))
    def ucusVerilbl(self):
        if self.homeForm.UcusVeri.isVisible()==True:
            self.homeForm.ucusVeriLbl.setMaximumWidth(3)
            self.homeForm.ucusVeriLbl.setMinimumWidth(3)
            self.homeForm.ucusVeriLbl.setStyleSheet('background-color: {}'.format(QColor(222, 222, 222).name()))
        else:
            self.homeForm.ucusVeriLbl.setMinimumWidth(1)
            self.homeForm.ucusVeriLbl.setMaximumWidth(1)
            self.homeForm.ucusVeriLbl.setStyleSheet('background-color: {}'.format(QColor(38, 38, 38).name()))

    def yerKontrollbl(self):
        if self.homeForm.YerKontrol.isVisible()==True:
            self.homeForm.yerKontrolLbl.setMaximumWidth(3)
            self.homeForm.yerKontrolLbl.setMinimumWidth(3)
            self.homeForm.yerKontrolLbl.setStyleSheet('background-color: {}'.format(QColor(222, 222, 222).name()))
            self.homeForm.ucusVeriLbl.setMinimumWidth(1)
            self.homeForm.ucusVeriLbl.setMaximumWidth(1)
            self.homeForm.ucusVeriLbl.setStyleSheet('background-color: {}'.format(QColor(38, 38, 38).name()))
            
        else:
            self.homeForm.yerKontrolLbl.setMinimumWidth(1)
            self.homeForm.yerKontrolLbl.setMaximumWidth(1)
            self.homeForm.yerKontrolLbl.setStyleSheet('background-color: {}'.format(QColor(38, 38, 38).name()))

    def Gorevlbl(self):
        if self.homeForm.Gorev.isVisible()==True: 
            self.homeForm.gorevLbl.setMinimumWidth(3)
            self.homeForm.gorevLbl.setStyleSheet('background-color: {}'.format(QColor(222, 222, 222).name()))
            self.homeForm.ucusVeriLbl.setMinimumWidth(1)
            self.homeForm.ucusVeriLbl.setMaximumWidth(1)
            self.homeForm.ucusVeriLbl.setStyleSheet('background-color: {}'.format(QColor(38, 38, 38).name()))

        else:
            self.homeForm.gorevLbl.setMinimumWidth(1)
            self.homeForm.gorevLbl.setMaximumWidth(1)
            self.homeForm.gorevLbl.setStyleSheet('background-color: {}'.format(QColor(38, 38, 38).name()))        


    def ayarlarlbl(self):
        if self.homeForm.Ayarlar.isVisible()==True: 
            self.homeForm.ayarLbl.setMaximumWidth(3)
            self.homeForm.ayarLbl.setMinimumWidth(3)
            self.homeForm.ayarLbl.setStyleSheet('background-color: {}'.format(QColor(222, 222, 222).name()))
            self.homeForm.ucusVeriLbl.setMinimumWidth(1)
            self.homeForm.ucusVeriLbl.setMaximumWidth(1)
            self.homeForm.ucusVeriLbl.setStyleSheet('background-color: {}'.format(QColor(38, 38, 38).name()))
        else:
            self.homeForm.ayarLbl.setMinimumWidth(1)
            self.homeForm.ayarLbl.setMaximumWidth(1) 
            self.homeForm.ayarLbl.setStyleSheet('background-color: {}'.format(QColor(38, 38, 38).name()))  


############################################------dil değiştirme fonksiyonları-----#######################################
    def dilDegistir(self):
        if self.homeForm.DilSecenekCB.currentText()=="Türkçe":
            self.turkish()
        elif self.homeForm.DilSecenekCB.currentText()=="English":
            self.english()
             
##############################################-----ses fonksiyonları-----#################################################    
    def sesi_kapat(self):
        self.player.setMuted(True)

    def sesi_ac(self):
        self.player.setMuted(False)
    

    def play_sound(self):
        # Ses dosyasını yükle
        url = QUrl.fromLocalFile("audio\mixkit-cool-interface-click-tone-2568.wav")
        content = QMediaContent(url)

        # QMediaPlayer nesnesi için medya içeriği ayarla
        self.player.setMedia(content)

        # Ses dosyasını çal
        self.player.play()
    def play_soundd(self):
        # Ses dosyasını yükle
        url = QUrl.fromLocalFile("audio\mixkit-plastic-bubble-click-1124.wav")
        content = QMediaContent(url)

        # QMediaPlayer nesnesi için medya içeriği ayarla
        self.player.setMedia(content)

        # Ses dosyasını çal
        self.player.play()


    def play_Logout_Sound(self):

        url = QUrl.fromLocalFile("audio\mixkit-modern-click-box-check-1120.wav")
        content = QMediaContent(url)

        self.player.setMedia(content)

        self.player.play()

    
    
#########################################-----side bar click fonksiyonu-----##############################################
    def toggleSideBar(self):
        
        if self.homeForm.SideBarW.maximumWidth()==60:
            self.homeForm.SideBarW.setMaximumWidth(145)
            self.homeForm.SideBarW.setMinimumWidth(145)
            self.homeForm.logoW.setMaximumSize(145,95)
            self.homeForm.SideBarW.setMaximumWidth(145)
        else:
            self.homeForm.SideBarW.setMaximumWidth(60)
            self.homeForm.logoW.setMaximumSize(60,50)
            self.homeForm.SideBarW.setMinimumWidth(60)
#########################################-----profil bar click fonksiyonu-----############################################

    def profilBarGoster(self):
        if self.homeForm.ProfileW.maximumWidth()==0:
            self.homeForm.ProfileW.setMaximumWidth(100)
        else:
            self.homeForm.ProfileW.setMaximumWidth(0)

            
##########################################-----buton click fonksiyonları-----#############################################
    def defaultPage(self):
        self.homeForm.sayfalarSW.setCurrentWidget(self.homeForm.UcusVeri)        
            
    def showHomePage(self):
        self.homeForm.sayfalarSW.setCurrentWidget(self.homeForm.Hakkimizda)
        
    def showUcusVeri(self):
         self.homeForm.sayfalarSW.setCurrentWidget(self.homeForm.UcusVeri)
        
    def showGorev(self):
        self.homeForm.sayfalarSW.setCurrentWidget(self.homeForm.Gorev)

    def showYerKontrol(self):
        self.homeForm.sayfalarSW.setCurrentWidget(self.homeForm.YerKontrol)
        
        
    def showAyarlar(self):
        self.homeForm.sayfalarSW.setCurrentWidget(self.homeForm.Ayarlar)

##########################################-----mail gonderme fonksiyonu-----##############################################
    def mailGonder(self):
        to_address = self.homeForm.AyarlarVeriIicinEMailLE.text()
        
        # SMTP sunucu bilgileri
        smtp_server = 'smtp.gmail.com'
        smtp_port = 587
        smtp_username = 'karayelhavacilik@gmail.com'
        smtp_password = 'bwextvnasedqjhjh'
        
        # E-posta mesajı
        msg = MIMEText('su verileri')
        msg['From'] = smtp_username
        msg['To'] = to_address
        msg['Subject'] = "ekte verilen png dosyası size drone'umuzun su verilerini grafiksel olarak gösterir."#----arduniodan gelen veri png dosyası buraya yönlenririlcek

        # SMTP sunucusuna bağlan ve e-posta gönder
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.ehlo()
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.sendmail(smtp_username, to_address, msg.as_string())



# server = smtplib.SMTP('smtp.gmail.com', 587)
# server.starttls()

# # Kimlik doğrulama
# server.login("gonderen@gmail.com", "sifre")

# # Mesaj oluşturma
# msg = "Bu bir test e-postasıdır."

# # E-posta gönderme
# server.sendmail("gonderen@gmail.com", "alicilar@gmail.com", msg)

# # SMTP sunucusundan çıkış yapma
# server.quit()
    def kullanici_ayarlari(self):
        if self.homeForm.kaydetBtn.clicked:
            kullanici_adi = self.homeForm.AyarlarkullaniciAdiLE.text()
            old_password = self.homeForm.AyarlarkullaniciSifreLE.text()
            new_password = self.homeForm.AyarlarkullaniciYeniLE.text()
            new_password_control = self.homeForm.AyarlarkullaniciYEniTekrarLE.text()
            update = "UPDATE kullanici SET Sifre = %s WHERE Ad= %s"
            username_control = "SELECT Ad FROM kullanici"
            password_control = "SELECT Sifre FROM kullanici WHERE Ad = %s"
            im.execute(username_control)
            usernames = im.fetchall()
            if kullanici_adi == "":
                QMessageBox.warning(self,"Hata","Kullanıcı Adı Boş Bırakılamaz!")
            else:
                if kullanici_adi in [username[0] for username in usernames]:
                    if old_password == "":
                        QMessageBox.warning(self,"Hata","Mevcut Şifre Boş Bırakılamaz!")
                    elif new_password == "":
                        QMessageBox.warning(self,"Hata","Yeni Şifre Boş Bırakılamaz!")
                    elif new_password_control =="":
                        QMessageBox.warning(self,"Hata","Yeni Şifre Tekrarı Boş Bırakılamaz!")
                    elif old_password == new_password:
                        QMessageBox.warning(self,"Hata","Yeni Şifreniz Eski Şifre İle Aynı Olamaz!")
                    else:
                        im.execute(password_control,kullanici_adi)
                        passwords = im.fetchall()
                        if old_password in [pw[0] for pw in passwords]:
                            if new_password == new_password_control:
                                im.execute(update,(new_password,kullanici_adi))
                                QMessageBox.information(self,"Başarılı","Şifreniz Başarıyla Değiştirildi!")
                            else:
                                QMessageBox.warning(self,"Hata","Girdiğiniz Şifreler Uyuşmuyor!")
                        else:
                            QMessageBox.warning(self,"Hata","Kullanıcı Adınız Ve Şifreniz Uyuşmuyor!")
                else:
                    QMessageBox.warning(self,"Hata","Böyle Bir Kullanıcı Bulunamadı!")
            conn.commit()

############################-----drone vehicle.mod değiştirme fonksiyonları-----################################

    # def guideMod(self):
    #     vehicle.mode = VehicleMode("GUIDED")
    # def manuelMod(self):#ikiye ayrılır poshold, stabilize
    #     vehicle.mode = VehicleMode("MANUAL") 
    # def rtlMod(self):
    #     vehicle.mode = VehicleMode("RTL")
        

    


##############################################################################################################################
##############################################################################################################################
#############-----LİGHT/DARK MOD-----###############-----LİGHT/DARK MOD-----##############-----LİGHT/DARK MOD-----############
##############################################################################################################################
##############################################################################################################################
    # def darkMod(self):  from PyQt5.QtGui import QPainter, QColor
    # def paintEvent(self, event):

    #     qp = QPainter()
    #     qp.begin(self)
    #     self.drawRectangles(qp)
    #     qp.end()


    # def drawRectangles(self, qp):

    #     col = QColor(0, 0, 0)
    #     col.setNamedColor('#d4d4d4')
    #     qp.setPen(col)

    #     qp.setBrush(QColor(255, 255, 255))
    #     qp.drawRect(10, 15, 90, 60)

    #     qp.setBrush(QColor(200, 0, 0))
    #     qp.drawRect(130, 15, 90, 60)

    #     qp.setBrush(QColor(0, 0, 255))
    #     qp.drawRect(250, 15, 90, 60)

    # def lightMod(self):

##############################################################################################################################
##############################################################################################################################
#############-----DİL DESTEĞİ-----####################-----DİL DESTEĞİ-----#####################-----DİL DESTEĞİ-----#########
##############################################################################################################################
##############################################################################################################################

    def english(self):
        self.homeForm.hakkimizdaBtn.setText("  Home")
        self.homeForm.ucusVeriBtn.setText("  Data Flight")
        self.homeForm.yerKontrolBtn.setText("  Plan")
        self.homeForm.gorevBtn.setText("  Mission")
        self.homeForm.ayarlarBtn.setText(" Settings")
        self.homeForm.myprofileBtn.setText("Profile")
        self.homeForm.logoutBtn.setText("Logout")
        self.homeForm.DilSEcLbl.setText("LANGUAGE")
        self.homeForm.KullaniciHesabLbl.setText("USER ACCOUNT")
        self.homeForm.SesAyarlariLbl.setText("SOUND SETTİNGS")
        self.homeForm.VeriYedLbl.setText("DATA BACKUP")
        self.homeForm.YardmDesLbl.setText("HELP & SUPPORT")
        self.homeForm.GenelRB.setText("General")
        self.homeForm.SessizRB.setText("Silent")
        self.homeForm.kaydetBtn.setText("       Save")
        self.homeForm.AyarlarkarayelUILbl.setText("KARAYEL AVIATION UI SETTINGS")
        self.homeForm.gonderBtn.setText("       Submit")
        self.homeForm.gonderBtn_2.setText("       Submit")
        #ucusverileri
        self.homeForm.baglanBtn.setText("Connect")
        self.homeForm.yawTextLbl.setText("YAW")
        self.homeForm.rollTextLbl.setText("ROLL")
        self.homeForm.pitchTextLbl.setText("PITCH")
        self.homeForm.bataryaTextLbl.setText("BATTERY")
        self.homeForm.yatayHTextLbl.setText("HORIZONTAL SPEED")
        self.homeForm.dikeyHTextLbl.setText("VERTICAL SPEED")
        self.homeForm.yukesklikTextLbl.setText("ALTITUDE")
        self.homeForm.armDurumuTextLbl.setText("ARM STATUS")
        self.homeForm.gorevStartBtn_2.setText("GO!")
        self.homeForm.guideBtn_2.setText("GUIDE")
        self.homeForm.manuelBtn_2.setText("MANUEL")
        self.homeForm.rtlBtn_2.setText("RTL")
        #gorev
        self.homeForm.acBtn.setText("Camera Open")
        self.homeForm.kapaBtn.setText("Camera Close")
        self.homeForm.suVeriLbl.setText("WATER DATA")
        #ayarlar
        self.homeForm.AyarlarkullaniciAdiLE.setPlaceholderText("user name")
        self.homeForm.AyarlarkullaniciSifreLE.setPlaceholderText("current password")
        self.homeForm.AyarlarkullaniciYeniLE.setPlaceholderText("new password")
        self.homeForm.AyarlarkullaniciYEniTekrarLE.setPlaceholderText("new password again")
        self.homeForm.AyarlarVeriIicinEMailLE.setPlaceholderText("enter your e-mail address")
        self.homeForm.AyarlarYardmdstkIcinLE.setPlaceholderText("enter text")
        self.homeForm.AyarlarYardicinEmaile.setPlaceholderText("enter your e-mail address")

    def turkish(self):
        self.homeForm.hakkimizdaBtn.setText("  Hakkımızda")
        self.homeForm.ucusVeriBtn.setText("  Uçuş Verileri")
        self.homeForm.yerKontrolBtn.setText("  Yer Kontrol")
        self.homeForm.gorevBtn.setText("  Görev")
        self.homeForm.ayarlarBtn.setText(" Ayarlar")
        self.homeForm.myprofileBtn.setText("Profil")
        self.homeForm.logoutBtn.setText("Çıkış")
        self.homeForm.DilSEcLbl.setText("DİL SEÇENEKLERİ")
        self.homeForm.KullaniciHesabLbl.setText("KULLANICI HESABI")
        self.homeForm.SesAyarlariLbl.setText("SES AYARLARI")
        self.homeForm.VeriYedLbl.setText("VERİ YEDEKLEME")
        self.homeForm.YardmDesLbl.setText("YARDIM VE DESTEK")
        self.homeForm.GenelRB.setText("Genel")
        self.homeForm.SessizRB.setText("Sessiz")
        self.homeForm.kaydetBtn.setText("       Kaydet")
        self.homeForm.AyarlarkarayelUILbl.setText("KARAYEL HAVACILIK UI AYARLARI")
        self.homeForm.gonderBtn.setText("       Gönder")
        self.homeForm.gonderBtn_2.setText("       Gönder")
        #ucusverileri
        self.homeForm.baglanBtn.setText("Bağlan")
        self.homeForm.yawdegeriTextLbl.setText("YAW DEĞERİ")
        self.homeForm.rollDegeriTextLbl.setText("ROLL DEĞERİ")
        self.homeForm.pitchDegeriTextLbl.setText("PITCH DEĞERİ")
        self.homeForm.bataryaTextLbl.setText("BATARYA")
        self.homeForm.yatayHTextLbl.setText("YATAY HIZ")
        self.homeForm.dikeyHTextLbl.setText("DİKEY HIZ")
        self.homeForm.yukesklikTextLbl.setText("YÜKSEKLİK")
        self.homeForm.armDurumuTextLbl.setText("ARM DURUMU")
        self.homeForm.gorevStartBtn_2.setText("GO!")
        self.homeForm.guideBtn_2.setText("GUIDE")
        self.homeForm.manuelBtn_2.setText("MANUEL")
        self.homeForm.rtlBtn_2.setText("RTL")
        #gorev
        self.homeForm.acBtn.setText("Kamera Aç")
        self.homeForm.kapaBtn.setText("Kamera Kapa")
        self.homeForm.suVeriLbl.setText("SU VERİLERİ")
        #ayarlar
        self.homeForm.AyarlarkullaniciAdiLE.setPlaceholderText("kullanıcı adı")
        self.homeForm.AyarlarkullaniciSifreLE.setPlaceholderText("mevcut şifre")
        self.homeForm.AyarlarkullaniciYeniLE.setPlaceholderText("yeni şifre")
        self.homeForm.AyarlarkullaniciYEniTekrarLE.setPlaceholderText("yeni şifre tekrar")
        self.homeForm.AyarlarVeriIicinEMailLE.setPlaceholderText("e posta adresinizi giriniz")
        self.homeForm.AyarlarYardmdstkIcinLE.setPlaceholderText("metin giriniz")
        self.homeForm.AyarlarYardicinEmaile.setPlaceholderText("e posta adresinizi giriniz")
        pass
##############################################################################################################################     
##############################################################################################################################     
###########################-----ARDUNİO KODU-----#########-----GÖRÜNTÜ İŞLEME-----#########-----GÖRÜNTÜ İŞLEME-----#########
##############################################################################################################################
##############################################################################################################################     

    # mydb = mysql.connector.connect(
    # host="localhost",
    # user="root",
    # password="root",
    # database="test"
    # )

    # layout = QVBoxLayout()
    # layout.addWidget(self.canvas)
    # self.homeForm.suBilgiCenterW.setLayout(layout)

    # with open("test.txt", "r") as file:
    #     veriler = file.readlines()

    # mycursor = mydb.cursor()

    # for veri in veriler:
    #     sql = "INSERT INTO testsonuc (Sonuc) VALUES (%s)"
    #     val = (veri.strip(), )
    #     mycursor.execute(sql, val)

    # mydb.commit()
    # mydb.close()

    # # MySQL veritabanı bağlantısı
    # mydb = mysql.connector.connect(
    #     host="localhost",
    #     user="root",
    #     password="root",
    #     database="test"
    # )

    # # MySQL'den verileri seçme
    # mycursor = mydb.cursor()
    # mycursor.execute("SELECT SonucID, Sonuc FROM testsonuc")
    # data = mycursor.fetchall()

    # # Verileri ayrıştırma
    # ID = []
    # Sonuc = []
    # for row in data:
    #     ID.append(row[0])
    #     Sonuc.append(row[1])

    # # Görselleştirme
    # plt.scatter(ID,Sonuc, cmap='viridis')
    # plt.colorbar()
    # plt.show()

    # # Veritabanı bağlantısını kapatma
    # mydb.close()

##############################################################################################################################     
##############################################################################################################################     
###########################-----GÖRÜNTÜ İŞLEME-----#########-----GÖRÜNTÜ İŞLEME-----#########-----GÖRÜNTÜ İŞLEME-----#########
##############################################################################################################################
##############################################################################################################################     

    def start_camera(self):
        # Kamera aygıtına erişim sağla
        self.camera = cv2.VideoCapture(0)
        

        # Kamera görüntüsünü ekrana göster
        while True:
            ret, pic = self.camera.read()
            if ret:
                # Buton durdurma fonksiyonu
                self.homeForm.kapaBtn.clicked.connect(self.stop_camera)
                    #hsv renk uzayına çevirme
                hsv = cv2.cvtColor(pic, cv2.COLOR_BGR2HSV)
                #mavi alt ve ust sınır belirleme
                lower_blue = np.array([75, 120, 120])
                upper_blue = np.array([130, 255, 255])
                #mavi renge gore maskeleme
                mask = cv2.inRange(hsv, lower_blue, upper_blue)
                #blurlama için gray'e cevirme
                gray = cv2.cvtColor(pic,cv2.COLOR_BGR2GRAY)
                #blurlama
                blur = cv2.bilateralFilter(gray, 10, 80,95)
                #canny detection
                canny = cv2.Canny(blur,80,150)
                #çember bulma
                circles = cv2.HoughCircles(canny,cv2.HOUGH_GRADIENT, 1, 20,param1=10,param2=30,minRadius = 10,maxRadius=220)
                #sınırları konturleme
                contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                for cnt in contours:
                 area = cv2.contourArea(cnt)
                 #alan sınırlaması
                 if area > 60:
                  (x, y), radius = cv2.minEnclosingCircle(cnt)
                  if circles is not None:
                   circles = np.uint16(np.around(circles))
                   for i in circles[0,:]: 
                    cv2.circle(pic, (int(x), int(y)), int(radius), (0, 0, 255), 4)
                #sonuclarıgoruntuleme
                self.display_cam(pic)
                # Arayüzü güncelle
                QApplication.processEvents()
                
            else:
                break

    def display_cam(self,img):
               # OpenCV görüntüsünü QImage'e dönüştür
                image = QImage(img, img.shape[1], img.shape[0], QImage.Format_RGB888).rgbSwapped()
                pixmap = QPixmap.fromImage(image)
               # Etiketleri güncelle
                self.homeForm.cameraLbl.setPixmap(pixmap)
                self.homeForm.cameraLbl.setAlignment(Qt.AlignCenter)
                
    def stop_camera(self):
        # Kamera aygıtını durdur
        self.camera.release()
        self.homeForm.cameraLbl.clear()
        cv2.destroyAllWindows()
        pass

##############################################################################################################################     
##############################################################################################################################     
###########################-----UÇUŞ VERİLERİ-----#########-----UÇUŞ VERİLERİ-----#########-----UÇUŞ VERİLERİ-----############
##############################################################################################################################
##############################################################################################################################     

        

    # def Baglan(self):
    #     self.timerrr.start(1000)
    # def guncelle(self):
        
    #     self.homeForm.baglanBtn.setText("     Bağlandı")
    
    #     while True:
                
    #         yaw=vehicle.attitude.yaw
    #         self.homeForm.yawDegeriLbl.setText(format(yaw))
    #         roll=vehicle.attitude.roll
    #         pitch=vehicle.attitude.pitch
    #         horizontal_velocity = vehicle.velocity[0:2]
    #         vertical_velocity = vehicle.velocity[2]
    #         altitude = vehicle.location.global_relative_frame.alt
    #         battery=vehicle.battery.level
    #         self.homeForm.yawDegeriLbl.setText("{:.2f}".format(yaw))
    #         self.homeForm.rollDegeriLbl.setText("{:.2f}".format(roll))
    #         self.homeForm.pitchDegeriLbl.setText("{:.2f}".format(pitch))
    #         self.homeForm.yatayHLbl.setText(format(horizontal_velocity))
    #         self.homeForm.dikeyHLbl.setText(format(vertical_velocity))
    #         self.homeForm.yukseklikLbl.setText(format(altitude))
    #         self.homeForm.bataryaLbl.setText(format(battery))
    #         break


##############################################################################################################################     
##############################################################################################################################     
###########################-----OTONOM KOD-----#########-----OTONOM KOD-----#########-----OTONOM KOD-----#####################
##############################################################################################################################
##############################################################################################################################     

    def otonomu_calistir(self):
        connection_string="127.0.0.1:14550"

        iha=connect(connection_string, wait_ready=False);iha.wait_ready(True,timeout=300)

        def takeoff(irtifa):
            while iha.is_armable is not True:
                print("İHA arm edilebilir durumda değil..")
                time.sleep(1)

            print("İHA arm edilebilir!")

            iha.mode = VehicleMode("GUIDED")

            iha.armed = True

            while iha.armed is not True:
                print("İHA arm ediliyor...")
                time.sleep(0.5)

            print("İHA başarıyla arm edildi.")

            iha.simple_takeoff(irtifa)
            
            while iha.location.global_relative_frame.alt < irtifa * 0.9:
                print("İha hedef irtifaya yükseliyor.")
                time.sleep(1)

        def gorev_ekle():
            global komut
            komut = iha.commands

            komut.clear()
            time.sleep(1)

            # TAKEOFF
            komut.add(Command(0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_TAKEOFF, 0, 0, 0, 0, 0, 0, 0, 0, 10))

            # WAYPOINT
            komut.add(Command(0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 0, 2, 0, 0, 0, -35.36295286, 149.16514170, 15))

            komut.add(Command(0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 0, 5, 0, 0, 0, -35.36295286, 149.16514170, 5))
            
            komut.add(Command(0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 0, 2, 0, 0, 0, -35.36361897, 149.16496432, 15))

            komut.add(Command(0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 0, 5, 0, 0, 0, -35.36361897, 149.16496432, 5))

            # RTL
            komut.add(Command(0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_RETURN_TO_LAUNCH, 0, 0, 0, 0, 0, 0, 0, 0, 0))
            
            # DOĞRULAMA
            komut.add(Command(0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_RETURN_TO_LAUNCH, 0, 0, 0, 0, 0, 0, 0, 0, 0))

            komut.upload()
            print("Komutlar yükleniyor...")


        takeoff(10)

        gorev_ekle()

        komut.next = 0

        iha.mode = VehicleMode("AUTO")

        while True:
            next_waypoint = komut.next

            if next_waypoint is 0:
                print("İHA hedef irtifaya yükseldi.")
                time.sleep(1)

            if next_waypoint is 1:
                print("1. konuma gidiliyor.")
                time.sleep(1)

            if next_waypoint is 2:
                print("Test yapmak üzere inişe geçiliyor.")
                time.sleep(1)

            if next_waypoint is 3:
                print("2. konuma gidiliyor.")
                time.sleep(1)

            if next_waypoint is 4:
                print("Test yapmak üzere inişe geçiliyor.")
                time.sleep(1)

            if next_waypoint is 5:
                print("Üsse dönülüyor.")
                time.sleep(1)

            if next_waypoint is 6:
                print("Görev başarıyla sonlanmıştır :)")
                break

        print("Döngüden çıkıldı.")
        pass
#################################################################################################
##############################################################################################################################     