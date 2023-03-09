import sys, random
import can
from frame import Frame

from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QLabel, QWidget, QProgressBar
from interface import Ui_MainWindow
from PyQt5.QtCore import Qt, QTimer
from pyqtgraph import PlotWidget, plot



class MainWindow(QMainWindow):
	# The interval in msecs between each update 
	REFRESH_INTERVAL = 1000 // 100 # 1000 ms/s / 100 s = 10 ms
	def __init__(self):
		super(MainWindow, self).__init__()
		self.ui = Ui_MainWindow()
		self.ui.setupUi(self)

		# Start updating data at regular intervals
		self.init_timer()

		# Power button toggles system
		self.ui.powerbutton.clicked.connect(self.toggle_system)

		for widget in self.ui.centralwidget.findChildren(QProgressBar):
			widget.setTextVisible(True)
		
		self.listen()
		

	def listen(self):
		self.bus = can.interface.Bus(interface='slcan', channel='COM0', bitrate=500000)

		self.listener = can.BufferedReader()
		can.Notifier(self.bus, [self.listener])


	def init_timer(self):
		self.ui.timer = QTimer()
		self.ui.timer.setInterval(self.REFRESH_INTERVAL)
		self.ui.timer.timeout.connect(self.update_data)
		self.ui.timer.start()

		"""Called for every timer interval.
		"""
		
	def update_data(self):
		msg = self.listener.get_message()
		if (msg): 
			frame = Frame.from_bytearray(msg.data)
			# TODO: Update rest of GUI values
			self.advance_dataline(self.ui.lvgraph_x, self.ui.lvgraph_y, self.ui.lvgraph_dataline, frame.lv_voltage)
			self.advance_dataline(self.ui.hvgraph_x, self.ui.hvgraph_y, self.ui.hvgraph_dataline, frame.hv_voltage)
			self.advance_dataline(self.ui.lvcurrent_x, self.ui.lvcurrent_y, self.ui.lvcurrent_dataline, frame.lv_batt_current)
			self.advance_dataline(self.ui.hvcurrent_x, self.ui.hvcurrent_y, self.ui.hvcurrent_dataline, frame.hv_current)
	
		"""Given a list of x values, a list of y values, a pyqtgraph dataline object, and a new y value, 
		update the dataline with the new y value and shift the x values over by one.
		"""
	def advance_dataline(self, xs: list, ys: list, dataline, new_y) -> None:
		xs.pop(0)
		xs.append(xs[-1] + 1)

		ys.pop(0)
		ys.append(new_y)

		dataline.setData(xs, ys)

	def toggle_system(self):
		# Turn system off
		if self.ui.powerstatuslabel.text() == "Status: ON":
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
			self.ui.powerbutton.setText("Power Off")
			self.ui.powerbutton.setStyleSheet("border-radius: 20px; background-color: rgb(224, 108, 117);")

			self.ui.powerstatuslabel.setStyleSheet(" font-weight: bold; color: #33D918;")
			self.ui.powerstatuslabel.setText("Status: ON")

			self.ui.timer.start()

			for widget in self.ui.centralwidget.findChildren(QProgressBar):
				widget.setTextVisible(True)



		



# class Label(QLabel):
# 	def __init__(self, *args, **kwargs):
# 		super().__init__(*args, **kwargs)

# 		self.setAlignment(Qt.AlignCenter)

# class MainWindow(QMainWindow):
# 	def __init__(self):
# 		super().__init__()

# 		self.setWindowTitle("Hyperloop Power System Testing Interface")
# 		main_layout = QVBoxLayout()
# 		main_layout.addWidget(Label("Hi"))

# 		main_widget = QWidget()
# 		main_widget.setLayout(main_layout)

# 		self.setCentralWidget(main_widget)

if __name__ == "__main__":
	app = QApplication(sys.argv)
	window = MainWindow()
	window.show()
	app.exec_()

