import argparse
from enum import Enum
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
from PyQt5.QtCore import Qt, QTimer, QThread, pyqtSignal, QObject
from plot import *
import pyqtgraph as pg
import struct

# names for all the sql tables
# SQL Schema:
# Table [NAME] (Timestamp INTEGER, elapsed REAL, [NAME] REAL)
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

# CAN IDs for all the sensors
HVB1_T_ID = 0x000
HVB2_T_ID = 0x001
HVB3_T_ID = 0x002
HVB4_T_ID = 0x003
HVB5_T_ID = 0x004
HVB6_T_ID = 0x005
HVB7_T_ID = 0x006
HVB8_T_ID = 0x007
HVB9_T_ID = 0x008
HVB10_T_ID = 0x009
LVB_T_ID = 0x100
LV_PCB_T_ID = 0x104

HVB_V_ID = 0x014
LVB_V_ID = 0x101
RAIL_V_ID = 0x103
U1_V_ID = 0x105
U2_V_ID = 0x106
U4_V_ID = 0x107
U3_V_ID = 0x108

HV_C_ID = 0x015
LV_C_ID = 0x102


STATUS_DEBUG_STYLESHEET = "background-color: rgb(255, 221, 98); color: #6284FF;"
STATUS_ON_STYLESHEET ="color: #99615f; background-color:  rgb(121, 195, 119);"
STATUS_OFF_STYLESHEET ="color: white; background-color:  #c3777a;"
POWER_BUTTON_ON_STYLESHEET="color: #99615f; background-color: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1, stop: 0 #dadbde, stop:  1 rgb(80, 195, 26));"
POWER_BUTTON_OFF_STYLESHEET="color: white; background-color: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1, stop: 0 #dadbde, stop:  1 #de1641);"
POWER_BUTTON_DISABLED_STYLESHEET= "color: white; background-color: rgb(170, 170, 127);"

CURR_PATH = Path(__file__).parent.absolute()
RECORDINGS_PATH = CURR_PATH / "recordings"
ASSETS_PATH = CURR_PATH / 'assets'

# Converts a the bytearray data from a received CAN packet into a float representing a sensor value.
def bytes_to_float(b: bytearray) -> float:
  try:
    return struct.unpack('f', b)[0]
  except Exception as e:
    print(f"Error converting bytes {b} to float: {e}")
    return -1

def generate_db_timestamp() -> str:
  return time.strftime("%Y%m%d%H%M%S", time.localtime())

class Status(Enum):
  OFF = 0
  ON = 1
  DEBUG = 2


class CANWorker(QObject):
  data_received = pyqtSignal(object)
  def receive_data(self):
    if CAN_PORT:
      msg = listener.get_message(0.1)
      self.data_received.emit(msg)
    
    
class MainWindow(QMainWindow, Ui_MainWindow):
  # The interval in msecs between each update 
  REFRESH_INTERVAL = 1000 // 100 # 1000 ms/s / 100 s = 10 ms
  def __init__(self) -> None:
    super(MainWindow, self).__init__()
    self.setupUi(self)

    self.summarytemplinegraph: TLinePlot
    self.summarytempbargraph: TBarPlot
    self.summaryvoltagebargraph: VBarPlot
    self.summaryvoltagelinegraph: VLinePlot

    self.voltagegraph: VLinePlot
    self.tempgraph: TLinePlot
    self.currentgraph: CLinePlot

    self.statuslabel: QLabel
    self.hvsystembutton: QPushButton

    self.start_time: float = time.time()

    if not RECORDINGS_PATH.exists():
      RECORDINGS_PATH.mkdir()
    


    self.set_status(Status.OFF)

		# Used to calculate elapsed time for line chart x values

  # Connection to current sqlite database file. A new file is created when recording is started.
    self.db_conn: Optional[sqlite3.Connection] = None

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

    self.temprecordbutton: QPushButton
    # self.temprecordbutton.setIcon(QIcon(ASSETS_PATH / 'pause.svg'))

    # Record Button toggles recording on/off
    self.temprecordbutton.clicked.connect(self.toggle_recording)
    self.voltagerecordbutton.clicked.connect(self.toggle_recording)
    self.currentrecordbutton.clicked.connect(self.toggle_recording)

    self.showMaximized()

  # Overrides a QT method which runs when the application window is closed.  # Runs cleanup and closes any connections that need to be closed.
  def closeEvent(self, event) -> None:
    print("Closing application")
    if self.arduino_conn.is_open:
      self.arduino_conn.close()
    super().closeEvent(event)
  

  def init_can(self):
    if not CAN_PORT:
      print("No CAN port specified on command line, not initializing CAN interface.")
      return

    try:
      print(f"Initializing CAN interface on port {CAN_PORT}")
      self.bus = can.ThreadSafeBus(interface='slcan', channel=CAN_PORT, bitrate=1000000)

      self.listener = can.BufferedReader()
      self.notifier = can.Notifier(self.bus, listeners=[self.listener], timeout=0.01)
      print(f"CAN interface initialized")
    except Exception as e:
      print(f"Error initializing CAN interface: {e}")


  def init_timer(self):
    self.can_thread: QThread = QThread()
    self.can_worker = CANWorker()
    self.timer = QTimer()
    self.timer.setInterval(self.REFRESH_INTERVAL)
    self.timer.moveToThread(self.can_thread)
    self.can_worker.moveToThread(self.can_thread)
    self.can_worker.data_received.connect(self.update_data)
    self.can_thread.start()


    # self.timer.timeout.connect(self.timer_loop)
    # self.timer.start()
  
  def get_elapsed_seconds(self, time: float) -> float:
    return time - self.start_time

  # Setup a serial connection to the arduino due.
  def init_arduino_serial_conn(self) -> None:
    if not ARDUINO_PORT:
      print("No arduino port specified on command line, not initializing arduino serial connection.")
      return

    try:
      print(f"Initializing arduino serial connection on port {ARDUINO_PORT}")
      self.arduino_conn = serial.Serial()
      self.arduino_conn.baudrate = self.baud_rate
      self.arduino_conn.port = ARDUINO_PORT
      self.arduino_conn.timeout = 1
      
      # Close the port just in case it wasn't closed properly.
      if (self.arduino_conn.is_open):
        self.arduino_conn.close()
      self.arduino_conn.open()	

      
      # Arduino sends out stuff when it starts up
      # We don't want to read that, so we sleep 
      # hacky 
      time.sleep(0.2)

      print(f"Arduino serial connection initialized:", end=" ")
      print(self.arduino_conn)
    except Exception as e:
      print(f"Error initializing arduino serial connection: {e}")

  # Write to the arduino via serial.
  # Used to turn on/off the software switch and bucks.
  # Do not call this method directly, call the toggle_* methods instead.
  def write_to_arduino(self, data: str) -> None:
    if not ARDUINO_PORT:
      print("No arduino port specified on command line, not writing to arduino.")
      return

    print(f"Sending {data} to arduino")
    self.arduino_conn.write(data.encode())
    res = self.arduino_conn.read(1)

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
  
  def update_data(self, msg: can.Message) -> None:
    print(f"CAN message received: {msg}")
    if not msg:
      return
    
    timestamp = time.time()
    elapsed = self.get_elapsed_seconds(timestamp)
    sensor_data: float = bytes_to_float(msg.data)
    if msg.arbitration_id == HVB1_T_ID:
      if sensor_data >= 60:
        self.system_off()
      self.summarytemplinegraph.advance_dataline(self.summarytemplinegraph.hvb1_x, self.summarytemplinegraph.hvb1_y, self.summarytemplinegraph.hvb1_line, elapsed, sensor_data)
      self.tempgraph.advance_dataline(self.tempgraph.hvb1_x, self.tempgraph.hvb1_y, self.tempgraph.hvb1_line, elapsed, sensor_data)
      self.summarytempbargraph.set_bar_data(self.summarytempbargraph.hvbattery1_i, sensor_data)
      self.insert_data_sql(TABLE_T_HV1, timestamp, elapsed, sensor_data)
    elif msg.arbitration_id == HVB2_T_ID:
      if sensor_data >= 60:
        self.system_off()
      self.summarytemplinegraph.advance_dataline(self.summarytemplinegraph.hvb2_x, self.summarytemplinegraph.hvb2_y, self.summarytemplinegraph.hvb2_line, elapsed, sensor_data)
      self.tempgraph.advance_dataline(self.tempgraph.hvb2_x, self.tempgraph.hvb2_y, self.tempgraph.hvb2_line, elapsed, sensor_data)
      self.summarytempbargraph.set_bar_data(self.summarytempbargraph.hvbattery2_i, sensor_data)
      self.insert_data_sql(TABLE_T_HV2, timestamp, elapsed, sensor_data)
    elif msg.arbitration_id == HVB3_T_ID:
      if sensor_data >= 60:
        self.system_off()
      self.summarytemplinegraph.advance_dataline(self.summarytemplinegraph.hvb3_x, self.summarytemplinegraph.hvb3_y, self.summarytemplinegraph.hvb3_line, elapsed, sensor_data)
      self.tempgraph.advance_dataline(self.tempgraph.hvb3_x, self.tempgraph.hvb3_y, self.tempgraph.hvb3_line, elapsed, sensor_data)
      self.summarytempbargraph.set_bar_data(self.summarytempbargraph.hvbattery3_i, sensor_data)
      self.insert_data_sql(TABLE_T_HV3, timestamp, elapsed, sensor_data)
    elif msg.arbitration_id == HVB4_T_ID:
      if sensor_data >= 60:
        self.system_off()
      self.summarytemplinegraph.advance_dataline(self.summarytemplinegraph.hvb4_x, self.summarytemplinegraph.hvb4_y, self.summarytemplinegraph.hvb4_line, elapsed, sensor_data)
      self.tempgraph.advance_dataline(self.tempgraph.hvb4_x, self.tempgraph.hvb4_y, self.tempgraph.hvb4_line, elapsed, sensor_data)
      self.summarytempbargraph.set_bar_data(self.summarytempbargraph.hvbattery4_i, sensor_data) 
      self.insert_data_sql(TABLE_T_HV4, timestamp, elapsed, sensor_data)
    elif msg.arbitration_id == HVB5_T_ID:
      if sensor_data >= 60:
        self.system_off()
      self.summarytemplinegraph.advance_dataline(self.summarytemplinegraph.hvb5_x, self.summarytemplinegraph.hvb5_y, self.summarytemplinegraph.hvb5_line, elapsed, sensor_data)
      self.tempgraph.advance_dataline(self.tempgraph.hvb5_x, self.tempgraph.hvb5_y, self.tempgraph.hvb5_line, elapsed, sensor_data)
      self.summarytempbargraph.set_bar_data(self.summarytempbargraph.hvbattery5_i, sensor_data)
      self.insert_data_sql(TABLE_T_HV5, timestamp, elapsed, sensor_data)
    elif msg.arbitration_id == HVB6_T_ID:
      if sensor_data >= 60:
        self.system_off()
      self.summarytemplinegraph.advance_dataline(self.summarytemplinegraph.hvb6_x, self.summarytemplinegraph.hvb6_y, self.summarytemplinegraph.hvb6_line, elapsed, sensor_data)
      self.tempgraph.advance_dataline(self.tempgraph.hvb6_x, self.tempgraph.hvb6_y, self.tempgraph.hvb6_line, elapsed, sensor_data)
      self.summarytempbargraph.set_bar_data(self.summarytempbargraph.hvbattery6_i, sensor_data)
      self.insert_data_sql(TABLE_T_HV6, timestamp, elapsed, sensor_data)
    elif msg.arbitration_id == HVB7_T_ID:
      if sensor_data >= 60:
        self.system_off()
      self.summarytemplinegraph.advance_dataline(self.summarytemplinegraph.hvb7_x, self.summarytemplinegraph.hvb7_y, self.summarytemplinegraph.hvb7_line, elapsed, sensor_data)
      self.tempgraph.advance_dataline(self.tempgraph.hvb7_x, self.tempgraph.hvb7_y, self.tempgraph.hvb7_line, elapsed, sensor_data)
      self.summarytempbargraph.set_bar_data(self.summarytempbargraph.hvbattery7_i, sensor_data)
      self.insert_data_sql(TABLE_T_HV7, timestamp, elapsed, sensor_data)
    elif msg.arbitration_id == HVB8_T_ID:
      if sensor_data >= 60:
        self.system_off()
      self.summarytemplinegraph.advance_dataline(self.summarytemplinegraph.hvb8_x, self.summarytemplinegraph.hvb8_y, self.summarytemplinegraph.hvb8_line, elapsed, sensor_data)
      self.tempgraph.advance_dataline(self.tempgraph.hvb8_x, self.tempgraph.hvb8_y, self.tempgraph.hvb8_line, elapsed, sensor_data)
      self.summarytempbargraph.set_bar_data(self.summarytempbargraph.hvbattery8_i, sensor_data)
      self.insert_data_sql(TABLE_T_HV8, timestamp, elapsed, sensor_data)
    elif msg.arbitration_id == HVB9_T_ID:
      if sensor_data >= 60:
        self.system_off()
      self.summarytemplinegraph.advance_dataline(self.summarytemplinegraph.hvb9_x, self.summarytemplinegraph.hvb9_y, self.summarytemplinegraph.hvb9_line, elapsed, sensor_data)
      self.tempgraph.advance_dataline(self.tempgraph.hvb9_x, self.tempgraph.hvb9_y, self.tempgraph.hvb9_line, elapsed, sensor_data)
      self.summarytempbargraph.set_bar_data(self.summarytempbargraph.hvbattery9_i, sensor_data)
      self.insert_data_sql(TABLE_T_HV9, timestamp, elapsed, sensor_data)
    elif msg.arbitration_id == HVB10_T_ID:
      if sensor_data >= 60:
        self.system_off()
      self.summarytemplinegraph.advance_dataline(self.summarytemplinegraph.hvb10_x, self.summarytemplinegraph.hvb10_y, self.summarytemplinegraph.hvb10_line, elapsed, sensor_data)
      self.tempgraph.advance_dataline(self.tempgraph.hvb10_x, self.tempgraph.hvb10_y, self.tempgraph.hvb10_line, elapsed, sensor_data)
      self.summarytempbargraph.set_bar_data(self.summarytempbargraph.hvbattery10_i, sensor_data)
      self.insert_data_sql(TABLE_T_HV10, timestamp, elapsed, sensor_data)
    elif msg.arbitration_id == LVB_T_ID:
      if sensor_data >= 60:
        self.system_off()
      self.summarytemplinegraph.advance_dataline(self.summarytemplinegraph.lvb_x, self.summarytemplinegraph.lvb_y, self.summarytemplinegraph.lvb_line, elapsed, sensor_data)
      self.tempgraph.advance_dataline(self.tempgraph.lvb_x, self.tempgraph.lvb_y, self.tempgraph.lvb_line, elapsed, sensor_data)
      self.summarytempbargraph.set_bar_data(self.summarytempbargraph.lvbattery_i, sensor_data)
      self.insert_data_sql(TABLE_T_LV, timestamp, elapsed, sensor_data)
    elif msg.arbitration_id == LV_PCB_T_ID:
      if sensor_data >= 60:
        self.system_off()
      self.summarytemplinegraph.advance_dataline(self.summarytemplinegraph.pcb_x, self.summarytemplinegraph.pcb_y, self.summarytemplinegraph.pcb_line, elapsed, sensor_data)
      self.tempgraph.advance_dataline(self.tempgraph.pcb_x, self.tempgraph.pcb_y, self.tempgraph.pcb_line, elapsed, sensor_data)
      self.summarytempbargraph.set_bar_data(self.summarytempbargraph.pcb_i, sensor_data)
      self.insert_data_sql(TABLE_T_PCB, timestamp, elapsed, sensor_data)
    elif msg.arbitration_id == HVB_V_ID:
      self.summaryvoltagelinegraph.advance_dataline(self.summaryvoltagelinegraph.hvb_x, self.summaryvoltagelinegraph.hvb_y, self.summaryvoltagelinegraph.hvb_line, elapsed, sensor_data)
      self.voltagegraph.advance_dataline(self.voltagegraph.hvb_x, self.voltagegraph.hvb_y, self.voltagegraph.hvb_line, elapsed, sensor_data)
      self.summaryvoltagebargraph.set_bar_data(self.summaryvoltagebargraph.hvbattery_i, sensor_data)
      self.insert_data_sql(TABLE_V_HVBATTERY, timestamp, elapsed, sensor_data)
    elif msg.arbitration_id == LVB_V_ID:
      self.summaryvoltagelinegraph.advance_dataline(self.summaryvoltagelinegraph.lvb_x, self.summaryvoltagelinegraph.lvb_y, self.summaryvoltagelinegraph.lvb_line, elapsed, sensor_data)
      self.voltagegraph.advance_dataline(self.voltagegraph.lvb_x, self.voltagegraph.lvb_y, self.voltagegraph.lvb_line, elapsed, sensor_data)
      self.summaryvoltagebargraph.set_bar_data(self.summaryvoltagebargraph.lvbattery_i, sensor_data)
      self.insert_data_sql(TABLE_V_LVBATTERY, timestamp, elapsed, sensor_data)
    elif msg.arbitration_id == RAIL_V_ID:
      match self.status:
        case Status.OFF:
          if sensor_data > 5:
            self.set_status(Status.DEBUG)
        case Status.DEBUG:
          if sensor_data <= 5:
            self.set_status(Status.OFF)
        case Status.ON:
          if sensor_data <= 30 and sensor_data > 0:
            self.set_status(Status.DEBUG)
      self.summaryvoltagelinegraph.advance_dataline(self.summaryvoltagelinegraph.rail_x, self.summaryvoltagelinegraph.rail_y, self.summaryvoltagelinegraph.rail_line, elapsed, sensor_data)
      self.voltagegraph.advance_dataline(self.voltagegraph.rail_x, self.voltagegraph.rail_y, self.voltagegraph.rail_line, elapsed, sensor_data)
      self.summaryvoltagebargraph.set_bar_data(self.summaryvoltagebargraph.rail_i, sensor_data)
      self.insert_data_sql(TABLE_V_RAIL, timestamp, elapsed, sensor_data)
    elif msg.arbitration_id == U1_V_ID:
      self.summaryvoltagelinegraph.advance_dataline(self.summaryvoltagelinegraph.u1_x, self.summaryvoltagelinegraph.u1_y, self.summaryvoltagelinegraph.u1_line, elapsed, sensor_data)
      self.voltagegraph.advance_dataline(self.voltagegraph.u1_x, self.voltagegraph.u1_y, self.voltagegraph.u1_line, elapsed, sensor_data)
      self.summaryvoltagebargraph.set_bar_data(self.summaryvoltagebargraph.u1_i, sensor_data)
      self.insert_data_sql(TABLE_V_U1, timestamp, elapsed, sensor_data)
    elif msg.arbitration_id == U2_V_ID:
      self.summaryvoltagelinegraph.advance_dataline(self.summaryvoltagelinegraph.u2_x, self.summaryvoltagelinegraph.u2_y, self.summaryvoltagelinegraph.u2_line, elapsed, sensor_data)
      self.voltagegraph.advance_dataline(self.voltagegraph.u2_x, self.voltagegraph.u2_y, self.voltagegraph.u2_line, elapsed, sensor_data)
      self.summaryvoltagebargraph.set_bar_data(self.summaryvoltagebargraph.u2_i, sensor_data)
      self.insert_data_sql(TABLE_V_U2, timestamp, elapsed, sensor_data)
    elif msg.arbitration_id == U3_V_ID:
      self.summaryvoltagelinegraph.advance_dataline(self.summaryvoltagelinegraph.u3_x, self.summaryvoltagelinegraph.u3_y, self.summaryvoltagelinegraph.u3_line, elapsed, sensor_data)
      self.voltagegraph.advance_dataline(self.voltagegraph.u3_x, self.voltagegraph.u3_y, self.voltagegraph.u3_line, elapsed, sensor_data)
      self.summaryvoltagebargraph.set_bar_data(self.summaryvoltagebargraph.u3_i, sensor_data)
      self.insert_data_sql(TABLE_V_U3, timestamp, elapsed, sensor_data)
    elif msg.arbitration_id == U4_V_ID:
      self.summaryvoltagelinegraph.advance_dataline(self.summaryvoltagelinegraph.u4_x, self.summaryvoltagelinegraph.u4_y, self.summaryvoltagelinegraph.u4_line, elapsed, sensor_data)
      self.voltagegraph.advance_dataline(self.voltagegraph.u4_x, self.voltagegraph.u4_y, self.voltagegraph.u4_line, elapsed, sensor_data)
      self.summaryvoltagebargraph.set_bar_data(self.summaryvoltagebargraph.u4_i, sensor_data)
      self.insert_data_sql(TABLE_V_U4, timestamp, elapsed, sensor_data)
    elif msg.arbitration_id == HV_C_ID:
      self.currentgraph.advance_dataline(self.currentgraph.hvcurrent_x, self.currentgraph.hvcurrent_y, self.currentgraph.hvcurrent_line, elapsed, sensor_data)
      self.insert_data_sql(TABLE_C_HV, timestamp, elapsed, sensor_data)
    elif msg.arbitration_id == LV_C_ID:
      self.currentgraph.advance_dataline(self.currentgraph.lvcurrent_x, self.currentgraph.lvcurrent_y, self.currentgraph.lvcurrent_line, elapsed, sensor_data)
      self.insert_data_sql(TABLE_C_LV, timestamp, elapsed, sensor_data)
    else:
      print(f"Unknown CAN ID: {msg.arbitration_id}")




  def toggle_system(self) -> None: 
    if self.hvsystembutton.isChecked():
      self.system_on()
    else:
      self.system_off()

  def system_on(self) -> None:
      print("Turning on HV system")
      self.set_status(Status.ON)
      self.toggle_software_switch(enable=True) 
  def system_off(self) -> None:
      print("Shutting off HV system")
      self.set_status(Status.DEBUG)
      self.toggle_software_switch(enable=False)

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
  
  def set_status(self, status: Status):
    self.status = status
    match status:
      case status.ON:
        self.statuslabel.setStyleSheet(STATUS_ON_STYLESHEET)
        self.statuslabel.setText("Status: ON")
        self.hvsystembutton.setEnabled(True)
        self.hvsystembutton.setStyleSheet(POWER_BUTTON_ON_STYLESHEET)
        self.hvsystembutton.setText("Engaged")
        self.summaryvoltagebargraph.rail_expected_v = 48
      case status.DEBUG:
        self.statuslabel.setStyleSheet(STATUS_DEBUG_STYLESHEET)
        self.statuslabel.setText("Status: DEBUG")
        self.hvsystembutton.setEnabled(True)
        self.hvsystembutton.setStyleSheet(POWER_BUTTON_OFF_STYLESHEET)
        self.hvsystembutton.setText("Disengaged")
        self.summaryvoltagebargraph.rail_expected_v = 36
      case status.OFF:
        self.statuslabel.setStyleSheet(STATUS_OFF_STYLESHEET)
        self.statuslabel.setText("Status: OFF")
        self.hvsystembutton.setEnabled(False)
        self.hvsystembutton.setStyleSheet(POWER_BUTTON_DISABLED_STYLESHEET)
        self.hvsystembutton.setText("Disengaged")
        self.summaryvoltagebargraph.rail_expected_v = 0




  def toggle_recording(self):
    # Create a new sqlite db file and connect to it.
    if not self.db_conn:
      self.db_conn = sqlite3.connect(RECORDINGS_PATH / f"{generate_db_timestamp()}.db")
      # Create tables for current, voltage, temp
      for table in TABLES:
        self.create_table_sql(table)
        
    # Close the connection to the current db file.
    else:
      self.db_conn.close()
      self.db_conn = None

    buttons = [self.voltagerecordbutton, self.temprecordbutton, self.currentrecordbutton]
    for button in buttons:
      # Start recording
      if self.db_conn:
        button.setText("Recording")
        button.setStyleSheet(POWER_BUTTON_ON_STYLESHEET)
      else:
        button.setText("Not\nRecording")
        button.setStyleSheet(POWER_BUTTON_OFF_STYLESHEET)

  def create_table_sql(self, name: str) -> None:
    if self.db_conn:
      cur = self.db_conn.cursor()
      cur.execute(f"CREATE TABLE {name} (timestamp REAL, elapsed REAL, {name} REAL)")
  
  def insert_data_sql(self, table: str, timestamp: float, elapsed: float, data: float) -> None:
    if self.db_conn:
      cur = self.db_conn.cursor()
      cur.execute(f"INSERT INTO {table} VALUES ({timestamp}, {elapsed}, {data})")
      self.db_conn.commit()
        
  



if __name__ == "__main__":
  parser = argparse.ArgumentParser(description="Testing Interface for the UTHT Power Distribution System.")
  parser.add_argument('-c', '--can-port', help='The serial port that the can interface is connected to.', type=str, default=None)
  parser.add_argument('-a', '--arduino-port', help='The serial port that the arduino due is connected to.', type=str, default=None)
  parser.add_argument('-b', '--baud-rate', help='The baud rate for the serial connection to the arduino.', type=int, default=9600)
  args = parser.parse_args()
  CAN_PORT: Optional[str] = args.can_port
  ARDUINO_PORT: Optional[str] = args.arduino_port
  BAUD_RATE: int = args.baud_rate

  if not CAN_PORT:
    print("No CAN port specified on command line, not initializing CAN interface.")
  else:
    try:
      print(f"Initializing CAN interface on port {CAN_PORT}")
      bus = can.ThreadSafeBus(interface='slcan', channel=CAN_PORT, bitrate=1000000)

      listener = can.BufferedReader()
      notifier = can.Notifier(bus, listeners=[listener], timeout=0.01)
      print(f"CAN interface initialized")
    except Exception as e:
      print(f"Error initializing CAN interface: {e}")

  app = QApplication([])
  window = MainWindow()
  window.show()
  app.exec_()