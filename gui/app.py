import sys, random

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



	def init_timer(self):
		self.ui.timer = QTimer()
		self.ui.timer.setInterval(self.REFRESH_INTERVAL)
		self.ui.timer.timeout.connect(self.update_data)
		self.ui.timer.start()

		"""Called for every timer interval.
		"""
	def update_data(self):
		self.advance_dataline(self.ui.lvgraph_x, self.ui.lvgraph_y, self.ui.lvgraph_dataline, random.randint(30, 40))
		self.advance_dataline(self.ui.hvgraph_x, self.ui.hvgraph_y, self.ui.hvgraph_dataline, random.randint(30, 40))
		self.advance_dataline(self.ui.lvcurrent_x, self.ui.lvcurrent_y, self.ui.lvcurrent_dataline, random.randint(30, 40))
		self.advance_dataline(self.ui.hvcurrent_x, self.ui.hvcurrent_y, self.ui.hvcurrent_dataline, random.randint(30, 40))
	
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

if __name__ == "__main__":
	app = QApplication(sys.argv)
	window = MainWindow()
	window.show()
	app.exec_()

