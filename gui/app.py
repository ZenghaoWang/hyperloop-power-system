import sys, random

from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QLabel, QWidget
from interface import Ui_MainWindow
from PyQt5.QtCore import Qt, QTimer



class MainWindow(QMainWindow):
	# The interval in msecs between each update 
	REFRESH_INTERVAL = 1000 // 100 # 1000 ms/s / 100 s = 10 ms
	def __init__(self):
		super(MainWindow, self).__init__()
		self.ui = Ui_MainWindow()
		self.ui.setupUi(self)

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

