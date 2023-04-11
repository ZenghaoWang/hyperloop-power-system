import sys, random
from time import sleep
import time
import serial
from typing import Optional
import can

from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QLabel, QWidget, QProgressBar, QFrame, QPushButton, QCheckBox
from interface import Ui_MainWindow
from PyQt5.QtCore import Qt, QTimer
from plot import *
import pyqtgraph as pg
import struct

STATUS_DEBUG_STYLESHEET = "background-color: rgb(255, 221, 98); color: #6284FF; border-radius: 20%;"
STATUS_ON_STYLESHEET ="color: #99615f; background-color:  rgb(121, 195, 119); border-radius: 20%;"
POWER_BUTTON_ON_STYLESHEET="border: 1px solid;border-radius:85%; color: #99615f; background-color: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1, stop: 0 #dadbde, stop:  1 rgb(80, 195, 26));"

# !!!!!!!!! CONFIG OPTIIONS !!!!!!!!!
# The serial port that the can interface is connected to. 
CAN_INTERFACE_COM_PORT = "COM22" # Placeholder, set this on the testing computer. 
# The serial port that the arduino due is connected to. 
ARDUINO_COM_PORT = "COM13" # placeholder, set this on the testing computer.
# Needs to be set the same as on the arduino, otherwise communication will be gibberish.
BAUD_RATE = 9600 

# thresholds for battery temps in celsius.
BATTERY_TEMP_WARNING_THRESHOLD = 50
BATTERY_TEMP_MAX_THRESHOLD = 60

# Converts a the bytearray data from a received CAN packet into a float representing a sensor value.
def bytes_to_float(b: bytearray) -> float:
  try:
    return struct.unpack('f', b)[0]
  except Exception as e:
    print(f"Error converting bytes {b} to float: {e}")
    return -1

def generate_timestamp() -> str:
  return time.strftime("%Y%m%d%H%M%S", time.localtime())

class MainWindow(QMainWindow, Ui_MainWindow):

  summaryvoltagelinegraph: VLinePlot
  summaryvoltagebargraph: VBarPlot
  summarytemplinegraph: TLinePlot
  summarytempbargraph: TBarPlot

  voltagegraph: VLinePlot
  tempgraph: TLinePlot
  currentgraph: CLinePlot



  def __init__(self) -> None:
    super(MainWindow, self).__init__()
    self.setupUi(self)
    
    # Set file handles to none
    self.voltage_file = None
    self.temp_file = None
    self.current_file = None

    # Make sure the summary tab is showing
    self.tabs.setCurrentIndex(0)

    # Checkbox toggles 288V/HV battery when clicked
    self.hvcheckbox.clicked.connect(self.toggle_288V)

    # Power Button toggles system on/off
    self.hvsystembutton.clicked.connect(self.toggle_system) 

    # Record Button toggles recording on/off
    self.temprecordbutton.clicked.connect(self.toggle_recording_temp)
    self.voltagerecordbutton.clicked.connect(self.toggle_recording_voltage)
    self.currentrecordbutton.clicked.connect(self.toggle_recording_current)

    self.showMaximized()
  
  def toggle_system(self) -> None: 
    print("hi")

  def toggle_288V(self):
    # show hv lines and bars on graphs
    if self.hvcheckbox.isChecked():
      self.summaryvoltagelinegraph.enable_288V()
      self.summaryvoltagebargraph.enable_288V()
      self.voltagegraph.enable_288V()

    # hide hv lines and bars
    else:
      self.summaryvoltagelinegraph.disable_288V()
      self.summaryvoltagebargraph.disable_288V()
      self.voltagegraph.disable_288V()

  def toggle_recording_voltage(self):
    button = self.voltagerecordbutton 
    # Start recording
    if button.isChecked():
      button.setText("Stop")
      # TODO: stylesheet
			# TODO: sqlite
      self.voltage_file = open(f"voltage_{generate_timestamp()}.txt", 'w')
    else:
      button.setText("Record")
      #_TODO: stylesheet
      if self.voltage_file:
        self.voltage_file.close()
        self.voltage_file = None
  
  def toggle_recording_temp(self):
    pass
  def toggle_recording_current(self):
    pass



if __name__ == "__main__":
  app = QApplication([])
  window = MainWindow()
  window.show()
  app.exec_()