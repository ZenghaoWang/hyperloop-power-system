import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QLabel, QWidget
from PyQt5.QtCore import Qt

class Label(QLabel):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		self.setAlignment(Qt.AlignCenter)

class MainWindow(QMainWindow):
	def __init__(self):
		super().__init__()

		self.setWindowTitle("Hyperloop Power System Testing Interface")
		main_layout = QVBoxLayout()
		main_layout.addWidget(Label("Hi"))

		main_widget = QWidget()
		main_widget.setLayout(main_layout)

		self.setCentralWidget(main_widget)

if __name__ == "__main__":
	app = QApplication(sys.argv)
	window = MainWindow()

	window.show()
	app.exec_()
