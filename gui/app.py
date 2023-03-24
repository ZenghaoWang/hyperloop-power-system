import sys, random
from time import sleep
import time
import serial
from typing import Optional
import can

from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QLabel, QWidget, QProgressBar
from interface import Ui_MainWindow
from PyQt5.QtCore import Qt, QTimer
from pyqtgraph import PlotWidget, plot
import struct

# !!!!!!!!!
CANABLE_COM_PORT = "COM10" # Placeholder, set this on the testing computer. 
ARDUINO_COM_PORT = "COM3" # placeholder, set this on the testing computer.
# Needs to be set the same as on the arduino, otherwise communication will be gibberish.
BAUD_RATE = 9600 



class MainWindow(QMainWindow):
  # The interval in msecs between each update 
  REFRESH_INTERVAL = 1000 // 100 # 1000 ms/s / 100 s = 10 ms
  def __init__(self):
    super(MainWindow, self).__init__()
    self.ui = Ui_MainWindow()
    self.ui.setupUi(self)


		# Setup a serial connection to the arduino due to send signals.
    self.init_arduino_serial_conn()		
		# Start listening for CAN messages
    self.init_can()
    # Start updating data at regular intervals
    self.init_timer()

    # Power button toggles system when clicked.
    # self.ui.powerbutton.clicked.connect(self.toggle_system)

    for widget in self.ui.centralwidget.findChildren(QProgressBar):
      widget.setTextVisible(True)

  # Overrides a QT method which runs when the application window is closed.
  # Runs cleanup and closes any connections that need to be closed.
  def closeEvent(self, event) -> None:
    # self.arduino_serial.close()
    # self.bus.shutdown()
    super().closeEvent(event)

  def init_can(self):
    pass
    # self.bus = can.interface.Bus(interface='slcan', channel=CANABLE_COM_PORT, bitrate=500000)

    # self.listener = can.BufferedReader()
    # can.Notifier(self.bus, [self.listener])


  def init_timer(self):
    self.ui.timer = QTimer()
    self.ui.timer.setInterval(self.REFRESH_INTERVAL)
    self.ui.timer.timeout.connect(self.update_data)
    self.ui.timer.start()
  
  
  # Setup a serial connection to the arduino due.
  def init_arduino_serial_conn(self) -> None:
    pass
    # try:
    #   print(f"Initializing arduino serial connection")
    #   self.arduino_serial = serial.Serial()
    #   self.arduino_serial.baudrate = BAUD_RATE
    #   self.arduino_serial.port = ARDUINO_COM_PORT
    #   self.arduino_serial.timeout = 1
      
    #   # Close the port just in case it wasn't closed properly.
    #   if (self.arduino_serial.is_open):
    #     self.arduino_serial.close()
    #   self.arduino_serial.open()	

      
    #   # We don't want to read that, so we sleep for a second.
    #   # hacky 
    #   time.sleep(1)

    #   print(f"Arduino serial connection initialized:", end=" ")
    #   print(self.arduino_serial)
    # except Exception as e:
    #   print(f"Error initializing arduino serial connection: {e}")



  # Write to the arduino via serial.
  # Used to turn on/off the software switch and bucks.
  # Do not call this method directly, call the toggle_* methods instead.
  def write_to_arduino(self, data: str) -> None:
    pass
    # print(f"Sending {data} to arduino")
    # self.arduino_serial.write(data.encode())
    # res = self.arduino_serial.read(1)

    # try:
    #   if res.decode('ASCII') == 'A':
    #     print(f"Arduino successfully received data: {data}")
    #   elif res.decode('ASCII') == 'N':
    #     # This should never happen because the arduino will only return 'N' if it received something it did not recognize.
    #     print(f"Arduino received {data} but did not act on it.")
    # except:
    #   print(f"Error decoding response {res}")

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



    """Called for every timer interval.
    Reads sensor data from CAN interface and updates the GUI.
    """
  def update_data(self):
    # msg: Optional[can.Message] = self.listener.get_message()
    # if (msg): 
    #   match msg.arbitration_id:
    #     # TODO: match on msg id and update gui
    #     # HV battery modules 1-10 temp
    #     case 0x000:
    #       self.ui.hvbattery1temp.setText(str(float(msg.data)) + '°c')
    #     case 0x001:
    #       self.ui.hvbattery2temp.setText(str(float(msg.data)) + '°c')
    #     case 0x002:
    #       self.ui.hvbattery3temp.setText(str(float(msg.data)) + '°c')
    #     case 0x003:
    #       self.ui.hvbattery4temp.setText(str(float(msg.data)) + '°c')
    #     case 0x004:
    #       self.ui.hvbattery5temp.setText(str(float(msg.data)) + '°c')
    #     case 0x005:
    #       self.ui.hvbattery6temp.setText(str(float(msg.data)) + '°c')
    #     case 0x006:
    #       self.ui.hvbattery7temp.setText(str(float(msg.data)) + '°c')
    #     case 0x007:
    #       self.ui.hvbattery8temp.setText(str(float(msg.data)) + '°c')
    #     case 0x008:
    #       self.ui.hvbattery9temp.setText(str(float(msg.data)) + '°c')
    #     case 0x009:
    #       self.ui.hvbattery10temp.setText(str(float(msg.data)) + '°c')
    #     # high voltage
    #     case 0x014:
    #       self.advance_dataline(self.ui.hvgraph_x, self.ui.hvgraph_y, self.ui.hvgraph_dataline, int(msg.data))
    #     # HV current
    #     case 0x015:
    #       self.advance_dataline(self.ui.hvcurrent_x, self.ui.hvcurrent_y, self.ui.hvcurrent_dataline, frame.hv_current)
    #     # LV battery temp
    #     case 0x100:	
    #       self.ui.lvbatterytemp.settext(str(float(msg.data)) + '°c')
    #     # LV battery current
    #     case 0x102:
    #       self.advance_dataline(self.ui.lvcurrent_x, self.ui.lvcurrent_y, self.ui.lvcurrent_dataline, int(msg.data))
    #     # LV voltage
    #     case 0x103:
    #       self.advance_dataline(self.ui.lvgraph_x, self.ui.lvgraph_y, self.ui.lvgraph_dataline, int(msg.data))
    #     # LV PCB temp
    #     case 0x104:
    #       self.ui.convertertemp.setText(str(float(msg.data)) + '°c')

  
    """Given a list of x values, a list of y values, a pyqtgraph dataline object, and a new y value, 
    update the dataline with the new y value and shift the x values over by one.
    """
  def advance_dataline(self, xs: list, ys: list, dataline, new_y) -> None:
    xs.pop(0)
    xs.append(xs[-1] + 1)

    ys.pop(0)
    ys.append(new_y)

    dataline.setData(xs, ys)

	# Triggered upon clicking the power button.
  def toggle_system(self):
    # Turn system off
    if self.ui.powerstatuslabel.text() == "Status: ON":
      self.toggle_software_switch(enable=False)
      self.ui.powerbutton.setText("Power On")
      self.ui.powerbutton.setStyleSheet("border-radius: 20px; background-color: rgb(170, 170, 127);")

      self.ui.powerstatuslabel.setStyleSheet(" font-weight: bold; color: rgb(170, 170, 127);")
      self.ui.powerstatuslabel.setText("Status: OFF")


      # Stop updating data
      self.ui.timer.stop()

      for widget in self.ui.centralwidget.findChildren(QLabel):
        if widget.text()[-1] == "c" or widget.text()[-1] == "%":
          widget.setText("N/A")
      for widget in self.ui.centralwidget.findChildren(QProgressBar):
        widget.setTextVisible(False)
        widget.setValue(0)
    # Turn system on
    else:
      self.toggle_software_switch(enable=True)
      self.ui.powerbutton.setText("Power Off")
      self.ui.powerbutton.setStyleSheet("border-radius: 20px; background-color: rgb(224, 108, 117);")

      self.ui.powerstatuslabel.setStyleSheet(" font-weight: bold; color: #33D918;")
      self.ui.powerstatuslabel.setText("Status: ON")

      self.ui.timer.start()

      for widget in self.ui.centralwidget.findChildren(QProgressBar):
        widget.setTextVisible(True)

if __name__ == "__main__":
  app = QApplication([])
  window = MainWindow()
  window.show()
  app.exec_()

