from pathlib import Path
import sys, random
import sqlite3
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

# names for all the sql tables
# SQL Schema:
# Table [NAME] (Timestamp INTEGER, [NAME] REAL)
TABLE_V_U1 = "v_u1"
TABLE_V_U2 = "v_u2"
TABLE_V_U3 = "v_u3"
TABLE_V_U4 = "v_u4"
TABLE_V_RAIL = "v_rail"
TABLE_V_HVBATTERY = "v_hvbattery"
TABLE_V_LVBATTERY = "v_lvbattery"
TABLE_T_HV1 = "t_hv1"
TABLE_T_HV2 = "t_hv2"
TABLE_T_HV3 = "t_hv3"
TABLE_T_HV4 = "t_hv4"
TABLE_T_HV5 = "t_hv5"
TABLE_T_HV6 = "t_hv6"
TABLE_T_HV7 = "t_hv7"
TABLE_T_HV8 = "t_hv8"
TABLE_T_HV9 = "t_hv9"
TABLE_T_HV10 = "t_hv10"
TABLE_T_LV = "t_lv"
TABLE_T_PCB = "t_pcb"
TABLE_C_HV = "c_hv"
TABLE_C_LV = "c_lv"
TABLES = [TABLE_V_U1, TABLE_V_U2, TABLE_V_U3, TABLE_V_U4, TABLE_V_RAIL, TABLE_V_HVBATTERY, TABLE_V_LVBATTERY, TABLE_T_HV1, TABLE_T_HV2, TABLE_T_HV3, TABLE_T_HV4, TABLE_T_HV5, TABLE_T_HV6, TABLE_T_HV7, TABLE_T_HV8, TABLE_T_HV9, TABLE_T_HV10, TABLE_T_LV, TABLE_T_PCB, TABLE_C_HV, TABLE_C_LV]

STATUS_DEBUG_STYLESHEET = "background-color: rgb(255, 221, 98); color: #6284FF;"
STATUS_ON_STYLESHEET ="color: #99615f; background-color:  rgb(121, 195, 119);"
STATUS_OFF_STYLESHEET ="color: white; background-color:  #c3777a;"
POWER_BUTTON_ON_STYLESHEET="color: #99615f; background-color: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1, stop: 0 #dadbde, stop:  1 rgb(80, 195, 26));"
POWER_BUTTON_OFF_STYLESHEET="color: white; background-color: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1, stop: 0 #dadbde, stop:  1 #de1641);"

CURR_PATH = Path(__file__).parent.absolute()
RECORDINGS_PATH = CURR_PATH / "recordings"



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

# Expected voltages should be within 5%
U1_EXPECTED_V = 24
U2_EXPECTED_V = 12
U3_EXPECTED_V = 5
U4_EXPECTED_V = 12
RAIL_EXPECTED_V = 36
HV_EXPECTED_V = 288
# Expected LV voltage should be between 12 and 29
LV_EXPECTED_V_LOW = 12
LV_EXPECTED_V_HIGH = 29

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
  # The interval in msecs between each update 
  REFRESH_INTERVAL = 1000 // 100 # 1000 ms/s / 100 s = 10 ms
  def __init__(self) -> None:
    super(MainWindow, self).__init__()
    self.setupUi(self)

  # Connection to current sqlite database file. A new file is created when recording is started.
    self.db_conn: Optional[sqlite3.Connection] = None
    self.is_recording = False

    # Setup a serial connection to the arduino due to send signals.
    self.init_arduino_serial_conn()		
    # Start listening for CAN messages
    self.init_can()
    # Start updating data at regular intervals
    self.init_timer()
    
    # Make sure the summary tab is showing
    self.tabs.setCurrentIndex(0)

    # Checkbox toggles 288V/HV battery when clicked
    self.hvcheckbox.clicked.connect(self.toggle_288V)

    # Power Button toggles system on/off
    self.hvsystembutton.clicked.connect(self.toggle_system) 

    # Record Button toggles recording on/off
    self.temprecordbutton.clicked.connect(self.toggle_recording)
    self.voltagerecordbutton.clicked.connect(self.toggle_recording)
    self.currentrecordbutton.clicked.connect(self.toggle_recording)

    self.showMaximized()

  # Overrides a QT method which runs when the application window is closed.  # Runs cleanup and closes any connections that need to be closed.
  def closeEvent(self, event) -> None:
    print("Closing application")
    self.arduino_serial.close()
    super().closeEvent(event)

  def init_can(self):
    try:
      print(f"Initializing CAN interface on port {CAN_INTERFACE_COM_PORT}")
      self.bus = can.ThreadSafeBus(interface='slcan', channel=CAN_INTERFACE_COM_PORT, bitrate=1000000)

      self.listener = can.BufferedReader()
      self.notifier = can.Notifier(self.bus, listeners=[self.listener], timeout=0.01)
      print(f"CAN interface initialized")
    except Exception as e:
      print(f"Error initializing CAN interface: {e}")


  def init_timer(self):
    self.timer = QTimer()
    self.timer.setInterval(self.REFRESH_INTERVAL)
    self.timer.timeout.connect(self.timer_loop)
    self.timer.start()

  # Setup a serial connection to the arduino due.
  def init_arduino_serial_conn(self) -> None:
    try:
      print(f"Initializing arduino serial connection on port {ARDUINO_COM_PORT}")
      self.arduino_serial = serial.Serial()
      self.arduino_serial.baudrate = BAUD_RATE
      self.arduino_serial.port = ARDUINO_COM_PORT
      self.arduino_serial.timeout = 1
      
      # Close the port just in case it wasn't closed properly.
      if (self.arduino_serial.is_open):
        self.arduino_serial.close()
      self.arduino_serial.open()	

      
      # We don't want to read that, so we sleep 
      # hacky 
      time.sleep(0.2)

      print(f"Arduino serial connection initialized:", end=" ")
      print(self.arduino_serial)
    except Exception as e:
      print(f"Error initializing arduino serial connection: {e}")

  # Write to the arduino via serial.
  # Used to turn on/off the software switch and bucks.
  # Do not call this method directly, call the toggle_* methods instead.
  def write_to_arduino(self, data: str) -> None:
    print(f"Sending {data} to arduino")
    self.arduino_serial.write(data.encode())
    res = self.arduino_serial.read(1)

    try:
      if res.decode('ASCII') == 'A':
        print(f"Arduino successfully received data: {data}")
      elif res.decode('ASCII') == 'N':
        # This should never happen because the arduino will only return 'N' if it received something it did not recognize.
        print(f"Arduino received {data} but did not act on it.")
    except:
      print(f"Error decoding response {res}")

    # TODO: implement timeout logic
  
  # enable flag controls whether the system is toggled on or off.
  def toggle_software_switch(self, enable: bool) -> None:
    if enable:
      self.write_to_arduino("S")
    else:
      self.write_to_arduino("s")
  
  def toggle_buckA(self, enable: bool) -> None:
    if enable:
      self.write_to_arduino("A")
    else:
      self.write_to_arduino("a")
  
  def toggle_buckB(self, enable: bool) -> None:
    if enable:
      self.write_to_arduino("B")
    else:
      self.write_to_arduino("b")
  def toggle_buckC(self, enable: bool) -> None:
    if enable:
      self.write_to_arduino("C")
    else:
      self.write_to_arduino("c")
  def toggle_buckD(self, enable: bool) -> None:
    if enable:
      self.write_to_arduino("D")
    else: 
      self.write_to_arduino("d")
  
  def timer_loop(self):
    # TODO
    self.summaryvoltagebargraph.set_bar_data(0, random.randint(1, 10))
    pass

  def toggle_system(self) -> None: 
    # TODO
    if self.hvsystembutton.isChecked():
      print("Turning system on")
      self.toggle_software_switch(enable=True)
      self.hvsystembutton.setText("Engaged")
      self.hvsystembutton.setStyleSheet(POWER_BUTTON_ON_STYLESHEET)

      self.timer.start()
    else:
      print("Turning system off")
      self.toggle_software_switch(enable=False)
      self.hvsystembutton.setText("Disengaged")
      self.hvsystembutton.setStyleSheet(POWER_BUTTON_OFF_STYLESHEET)

      self.timer.stop()

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

  def toggle_recording(self):
    # Create a new sqlite db file and connect to it.
    if not self.is_recording:
      self.db_conn = sqlite3.connect(RECORDINGS_PATH / f"{generate_timestamp()}.db")
      self.is_recording = True
      # Create tables for current, voltage, temp
      cur = self.db_conn.cursor()
      for table in TABLES:
        cur.execute(f"CREATE TABLE {table} (timestamp INTEGER, {table} REAL)")
    # Close the connection to the current db file.
    else:
      if self.db_conn:
        self.db_conn.close()
        self.db_conn = None
      self.is_recording = False

    buttons = [self.voltagerecordbutton, self.temprecordbutton, self.currentrecordbutton]
    for button in buttons:
      # Start recording
      if button.isChecked():
        button.setText("Stop")
        button.setStyleSheet(STATUS_ON_STYLESHEET)
      else:
        button.setText("Record")
        button.setStyleSheet(STATUS_OFF_STYLESHEET)
        
  



if __name__ == "__main__":
  app = QApplication([])
  window = MainWindow()
  window.show()
  app.exec_()