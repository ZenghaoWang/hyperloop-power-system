import sys, random
from time import sleep
import time
import serial
from typing import Optional
import can

from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QLabel, QWidget, QProgressBar, QFrame
from interface import Ui_MainWindow
from PyQt5.QtCore import Qt, QTimer
import pyqtgraph as pg
import struct

class MainWindow(QMainWindow, Ui_MainWindow):
  def __init__(self) -> None:
    super(MainWindow, self).__init__()
    self.setupUi(self)
    # Make the sure summary tab is showing
    self.tabs.setCurrentIndex(0)
    self.init_graphs()
  
  def init_graphs(self) -> None:
    self.summaryvoltagelinegraph.setLabel("bottom", "Time", units="s")
    self.summaryvoltagelinegraph.setLabel("left", "Voltage", units="V")
    self.summaryvoltagelinegraph.setTitle("Voltage sensors over time")
    self.summaryvoltagelinegraph.setYRange(10, 300, padding=0)
    self.summaryvoltagelinegraph.showGrid(x=True, y=True)
    self.summaryvoltagelinegraph.setBackground(None)
    self.summaryvoltagelinegraph.addLegend(colCount=2)
    self.summaryvoltagelinegraph.plot([x for x in range(1, 10)], [random.randint(20, 28) for _ in range(1, 10)], name="U1", pen=pg.mkPen(color=(255, 0, 0)))
    self.summaryvoltagelinegraph.plot([x for x in range(1, 10)], [random.randint(8, 16) for _ in range(1, 10)], name="U2", pen=pg.mkPen(color=(255, 50, 0)))
    self.summaryvoltagelinegraph.plot([x for x in range(1, 10)], [random.randint(1, 9) for _ in range(1, 10)], name="U3", pen=pg.mkPen(color=(255, 100, 0)))
    self.summaryvoltagelinegraph.plot([x for x in range(1, 10)], [random.randint(8, 16) for _ in range(1, 10)], name="U4", pen=pg.mkPen(color=(255, 150, 0)))
    self.summaryvoltagelinegraph.plot([x for x in range(1, 10)], [random.randint(32, 40) for _ in range(1, 10)], name="Power Rail", pen=pg.mkPen(color=(0, 150, 0)))
    self.summaryvoltagelinegraph.plot([x for x in range(1, 10)], [random.randint(284, 292) for _ in range(1, 10)], name="HV Battery", pen=pg.mkPen(color=(0, 255, 100)))
    self.summaryvoltagelinegraph.plot([x for x in range(1, 10)], [random.randint(17, 29) for _ in range(1, 10)], name="LV Battery", pen=pg.mkPen(color=(100, 255, 0)))


    self.summarytemplinegraph.setLabel("bottom", "Time", units="s")
    self.summarytemplinegraph.setLabel("left", "Temperature", units="°C")
    self.summarytemplinegraph.setTitle("Temperature sensors over time")
    self.summarytemplinegraph.setYRange(20, 70, padding=0)
    self.summarytemplinegraph.showGrid(x=True, y=True)
    self.summarytemplinegraph.setBackground(None)
    self.summarytemplinegraph.addLegend(colCount=3)
    self.summarytemplinegraph.plot([x for x in range(1, 10)], [random.randint(20, 40) for _ in range(1, 10)], name="HV Battery 1", pen=pg.mkPen(color=(255, 0, 0)))
    self.summarytemplinegraph.plot([x for x in range(1, 10)], [random.randint(20, 40) for _ in range(1, 10)], name="HV Battery 2", pen=pg.mkPen(color=(255, 20, 0)))
    self.summarytemplinegraph.plot([x for x in range(1, 10)], [random.randint(20, 40) for _ in range(1, 10)], name="HV Battery 3", pen=pg.mkPen(color=(255, 40, 0)))
    self.summarytemplinegraph.plot([x for x in range(1, 10)], [random.randint(20, 40) for _ in range(1, 10)], name="HV Battery 4", pen=pg.mkPen(color=(255, 60, 0)))
    self.summarytemplinegraph.plot([x for x in range(1, 10)], [random.randint(20, 40) for _ in range(1, 10)], name="HV Battery 5", pen=pg.mkPen(color=(255, 80, 0)))
    self.summarytemplinegraph.plot([x for x in range(1, 10)], [random.randint(20, 40) for _ in range(1, 10)], name="HV Battery 6", pen=pg.mkPen(color=(255, 100, 0)))
    self.summarytemplinegraph.plot([x for x in range(1, 10)], [random.randint(20, 40) for _ in range(1, 10)], name="HV Battery 7", pen=pg.mkPen(color=(255, 120, 0)))
    self.summarytemplinegraph.plot([x for x in range(1, 10)], [random.randint(20, 40) for _ in range(1, 10)], name="HV Battery 8", pen=pg.mkPen(color=(255, 140, 0)))
    self.summarytemplinegraph.plot([x for x in range(1, 10)], [random.randint(20, 40) for _ in range(1, 10)], name="HV Battery 9", pen=pg.mkPen(color=(255, 160, 0)))
    self.summarytemplinegraph.plot([x for x in range(1, 10)], [random.randint(20, 40) for _ in range(1, 10)], name="HV Battery 10", pen=pg.mkPen(color=(255, 180, 0)))
    self.summarytemplinegraph.plot([x for x in range(1, 10)], [random.randint(20, 40) for _ in range(1, 10)], name="LV Battery", pen=pg.mkPen(color=(0, 255, 0)))
    self.summarytemplinegraph.plot([x for x in range(1, 10)], [random.randint(20, 40) for _ in range(1, 10)], name="PCB", pen=pg.mkPen(color=(255, 255, 0)))


    self.summaryvoltagebargraph.setLabel("bottom", "Voltage Sensors")
    self.summaryvoltagebargraph.setLabel("left", "Voltage", units="V")
    self.summaryvoltagebargraph.setTitle("Voltage sensors")
    self.summaryvoltagebargraph.setYRange(0, 300, padding=0)
    self.summaryvoltagebargraph.showGrid(x=True, y=True)
    self.summaryvoltagebargraph.setBackground(None)
    voltages = [24, 12, 5, 12, 36, 288, 25]
    self.summaryvoltagebargraph.addItem(pg.BarGraphItem(x=[x for x in range(1, 8)], height=voltages, width=0.5, brush="g"))
    self.summaryvoltagebargraph.getAxis('bottom').setTicks([ [(1, "U1"), (2, "U2"), (3, "U3"), (4, "U4"), (5, "RAIL"), (6, "HVB"), (7, "LVB")] ])
    for i in range(1, 8):
      label = pg.TextItem(text=str(voltages[i - 1])+"V", anchor=(0.5,1), color=(0, 0, 0), border='w', fill=(255, 255, 255, 100))
      self.summaryvoltagebargraph.addItem(label)
      label.setPos(i, 0)


    self.summarytempbargraph.setLabel("bottom", "Temperature Sensors")
    self.summarytempbargraph.setLabel("left", "Temperature", units="°C")
    self.summarytempbargraph.setTitle("Temperature Sensors")
    self.summarytempbargraph.setYRange(20, 70, padding=0)
    self.summarytempbargraph.showGrid(x=True, y=True)
    self.summarytempbargraph.setBackground(None)
    temps = [random.randint(30, 50) for _ in range(1, 13)]
    self.summarytempbargraph.addItem(pg.BarGraphItem(x=[x for x in range(1, 13)], height=temps, width=0.5, brush="g"))
    self.summarytempbargraph.getAxis('bottom').setTicks([ [(1, "HV1"), (2, "HV2"), (3, "HV3"), (4, "HV4"), (5, "HV5"), (6, "HV6"), (7, "HV7"), (8, "HV8"), (9, "HV9"), (10, "HV10"), (11, "LVB"), (12, "PCB")] ])
    for i in range(1, 13):
      a = pg.TextItem(text=str(temps[i - 1])+"°C", anchor=(0.5,1), color=(0, 0, 0), border='w', fill=(255, 255, 255, 100))
      self.summarytempbargraph.addItem(a)
      a.setPos(i, 0)



if __name__ == "__main__":
  app = QApplication([])
  window = MainWindow()
  window.show()
  app.exec_()