# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\testing interface.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.




from PyQt5 import QtCore, QtGui, QtWidgets
import random
import pyqtgraph as pg



class Ui_MainWindow(object):
    timer: QtCore.QTimer
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(1640, 847)
        MainWindow.setUnifiedTitleAndToolBarOnMac(False)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setStyleSheet("background-color: #282C34;")
        self.centralwidget.setObjectName("centralwidget")

        self.hvbatterytempframe = QtWidgets.QFrame(self.centralwidget)
        self.hvbatterytempframe.setGeometry(QtCore.QRect(30, 420, 541, 341))
        self.hvbatterytempframe.setFrameShape(QtWidgets.QFrame.Box)
        self.hvbatterytempframe.setFrameShadow(QtWidgets.QFrame.Raised)
        self.hvbatterytempframe.setObjectName("hvbatterytempframe")
        self.hvbatterytemplabel = QtWidgets.QLabel(self.hvbatterytempframe)
        self.hvbatterytemplabel.setGeometry(QtCore.QRect(80, 0, 341, 31))
        self.hvbatterytemplabel.setStyleSheet(" font-weight: bold;\n"
"color: #60AEEE;")
        self.hvbatterytemplabel.setAlignment(QtCore.Qt.AlignCenter)
        self.hvbatterytemplabel.setObjectName("hvbatterytemplabel")
        self.layoutWidget = QtWidgets.QWidget(self.hvbatterytempframe)
        self.layoutWidget.setGeometry(QtCore.QRect(-10, 30, 555, 311))
        self.layoutWidget.setObjectName("layoutWidget")
        self.hvbatterytempgrid = QtWidgets.QGridLayout(self.layoutWidget)
        self.hvbatterytempgrid.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.hvbatterytempgrid.setContentsMargins(0, 0, 0, 0)
        self.hvbatterytempgrid.setObjectName("hvbatterytempgrid")
        self.hvbattery6tempframe = QtWidgets.QFrame(self.layoutWidget)
        self.hvbattery6tempframe.setStyleSheet("")
        self.hvbattery6tempframe.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.hvbattery6tempframe.setFrameShadow(QtWidgets.QFrame.Raised)
        self.hvbattery6tempframe.setObjectName("hvbattery6tempframe")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout(self.hvbattery6tempframe)
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.hvbattery6templabel = QtWidgets.QLabel(self.hvbattery6tempframe)
        self.hvbattery6templabel.setStyleSheet(" font-weight: bold;\n"
"color: #60AEEE;")
        self.hvbattery6templabel.setAlignment(QtCore.Qt.AlignCenter)
        self.hvbattery6templabel.setObjectName("hvbattery6templabel")
        self.verticalLayout_10.addWidget(self.hvbattery6templabel)
        self.hvbattery6tempcircle = QtWidgets.QFrame(self.hvbattery6tempframe)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.hvbattery6tempcircle.sizePolicy().hasHeightForWidth())
        self.hvbattery6tempcircle.setSizePolicy(sizePolicy)
        self.hvbattery6tempcircle.setMinimumSize(QtCore.QSize(71, 71))
        self.hvbattery6tempcircle.setStyleSheet("border-radius: 20px;\n"
"background-color: rgb(0, 255, 0);")
        self.hvbattery6tempcircle.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.hvbattery6tempcircle.setFrameShadow(QtWidgets.QFrame.Raised)
        self.hvbattery6tempcircle.setObjectName("hvbattery6tempcircle")
        self.hvbattery6temp = QtWidgets.QLabel(self.hvbattery6tempcircle)
        self.hvbattery6temp.setGeometry(QtCore.QRect(0, 10, 81, 51))
        self.hvbattery6temp.setAlignment(QtCore.Qt.AlignCenter)
        self.hvbattery6temp.setObjectName("hvbattery6temp")
        self.verticalLayout_10.addWidget(self.hvbattery6tempcircle)
        self.hvbatterytempgrid.addWidget(self.hvbattery6tempframe, 1, 0, 1, 1)
        self.hvbattery10tempframe = QtWidgets.QFrame(self.layoutWidget)
        self.hvbattery10tempframe.setStyleSheet("")
        self.hvbattery10tempframe.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.hvbattery10tempframe.setFrameShadow(QtWidgets.QFrame.Raised)
        self.hvbattery10tempframe.setObjectName("hvbattery10tempframe")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.hvbattery10tempframe)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.hvbattery10templabel = QtWidgets.QLabel(self.hvbattery10tempframe)
        self.hvbattery10templabel.setStyleSheet(" font-weight: bold;\n"
"color: #60AEEE;")
        self.hvbattery10templabel.setAlignment(QtCore.Qt.AlignCenter)
        self.hvbattery10templabel.setObjectName("hvbattery10templabel")
        self.verticalLayout_8.addWidget(self.hvbattery10templabel)
        self.hvbattery10tempcircle = QtWidgets.QFrame(self.hvbattery10tempframe)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.hvbattery10tempcircle.sizePolicy().hasHeightForWidth())
        self.hvbattery10tempcircle.setSizePolicy(sizePolicy)
        self.hvbattery10tempcircle.setMinimumSize(QtCore.QSize(71, 71))
        self.hvbattery10tempcircle.setStyleSheet("border-radius: 20px;\n"
"background-color: rgb(0, 255, 0);")
        self.hvbattery10tempcircle.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.hvbattery10tempcircle.setFrameShadow(QtWidgets.QFrame.Raised)
        self.hvbattery10tempcircle.setObjectName("hvbattery10tempcircle")
        self.hvbattery10temp = QtWidgets.QLabel(self.hvbattery10tempcircle)
        self.hvbattery10temp.setGeometry(QtCore.QRect(0, 10, 81, 51))
        self.hvbattery10temp.setAlignment(QtCore.Qt.AlignCenter)
        self.hvbattery10temp.setObjectName("hvbattery10temp")
        self.verticalLayout_8.addWidget(self.hvbattery10tempcircle)
        self.hvbatterytempgrid.addWidget(self.hvbattery10tempframe, 1, 4, 1, 1)
        self.hvbattery8tempframe = QtWidgets.QFrame(self.layoutWidget)
        self.hvbattery8tempframe.setStyleSheet("")
        self.hvbattery8tempframe.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.hvbattery8tempframe.setFrameShadow(QtWidgets.QFrame.Raised)
        self.hvbattery8tempframe.setObjectName("hvbattery8tempframe")
        self.verticalLayout_9 = QtWidgets.QVBoxLayout(self.hvbattery8tempframe)
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.hvbattery8templabel = QtWidgets.QLabel(self.hvbattery8tempframe)
        self.hvbattery8templabel.setStyleSheet(" font-weight: bold;\n"
"color: #60AEEE;")
        self.hvbattery8templabel.setAlignment(QtCore.Qt.AlignCenter)
        self.hvbattery8templabel.setObjectName("hvbattery8templabel")
        self.verticalLayout_9.addWidget(self.hvbattery8templabel)
        self.hvbattery8tempcircle = QtWidgets.QFrame(self.hvbattery8tempframe)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.hvbattery8tempcircle.sizePolicy().hasHeightForWidth())
        self.hvbattery8tempcircle.setSizePolicy(sizePolicy)
        self.hvbattery8tempcircle.setMinimumSize(QtCore.QSize(71, 71))
        self.hvbattery8tempcircle.setStyleSheet("border-radius: 20px;\n"
"background-color: rgb(0, 255, 0);")
        self.hvbattery8tempcircle.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.hvbattery8tempcircle.setFrameShadow(QtWidgets.QFrame.Raised)
        self.hvbattery8tempcircle.setObjectName("hvbattery8tempcircle")
        self.hvbattery8temp = QtWidgets.QLabel(self.hvbattery8tempcircle)
        self.hvbattery8temp.setGeometry(QtCore.QRect(0, 10, 81, 51))
        self.hvbattery8temp.setAlignment(QtCore.Qt.AlignCenter)
        self.hvbattery8temp.setObjectName("hvbattery8temp")
        self.verticalLayout_9.addWidget(self.hvbattery8tempcircle)
        self.hvbatterytempgrid.addWidget(self.hvbattery8tempframe, 1, 2, 1, 1)
        self.hvbattery3tempframe = QtWidgets.QFrame(self.layoutWidget)
        self.hvbattery3tempframe.setStyleSheet("")
        self.hvbattery3tempframe.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.hvbattery3tempframe.setFrameShadow(QtWidgets.QFrame.Raised)
        self.hvbattery3tempframe.setObjectName("hvbattery3tempframe")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.hvbattery3tempframe)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.hvbattery3templabel = QtWidgets.QLabel(self.hvbattery3tempframe)
        self.hvbattery3templabel.setStyleSheet(" font-weight: bold;\n"
"color: #60AEEE;")
        self.hvbattery3templabel.setAlignment(QtCore.Qt.AlignCenter)
        self.hvbattery3templabel.setObjectName("hvbattery3templabel")
        self.verticalLayout_5.addWidget(self.hvbattery3templabel)
        self.hvbattery3tempcircle = QtWidgets.QFrame(self.hvbattery3tempframe)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.hvbattery3tempcircle.sizePolicy().hasHeightForWidth())
        self.hvbattery3tempcircle.setSizePolicy(sizePolicy)
        self.hvbattery3tempcircle.setMinimumSize(QtCore.QSize(71, 71))
        self.hvbattery3tempcircle.setStyleSheet("border-radius: 20px;\n"
"background-color: rgb(0, 255, 0);")
        self.hvbattery3tempcircle.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.hvbattery3tempcircle.setFrameShadow(QtWidgets.QFrame.Raised)
        self.hvbattery3tempcircle.setObjectName("hvbattery3tempcircle")
        self.hvbattery3temp = QtWidgets.QLabel(self.hvbattery3tempcircle)
        self.hvbattery3temp.setGeometry(QtCore.QRect(0, 10, 81, 51))
        self.hvbattery3temp.setAlignment(QtCore.Qt.AlignCenter)
        self.hvbattery3temp.setObjectName("hvbattery3temp")
        self.verticalLayout_5.addWidget(self.hvbattery3tempcircle)
        self.hvbatterytempgrid.addWidget(self.hvbattery3tempframe, 0, 2, 1, 1)
        self.hvbattery4tempframe = QtWidgets.QFrame(self.layoutWidget)
        self.hvbattery4tempframe.setStyleSheet("")
        self.hvbattery4tempframe.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.hvbattery4tempframe.setFrameShadow(QtWidgets.QFrame.Raised)
        self.hvbattery4tempframe.setObjectName("hvbattery4tempframe")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.hvbattery4tempframe)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.hvbattery4templabel = QtWidgets.QLabel(self.hvbattery4tempframe)
        self.hvbattery4templabel.setStyleSheet(" font-weight: bold;\n"
"color: #60AEEE;")
        self.hvbattery4templabel.setAlignment(QtCore.Qt.AlignCenter)
        self.hvbattery4templabel.setObjectName("hvbattery4templabel")
        self.verticalLayout_6.addWidget(self.hvbattery4templabel)
        self.hvbattery4tempcircle = QtWidgets.QFrame(self.hvbattery4tempframe)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.hvbattery4tempcircle.sizePolicy().hasHeightForWidth())
        self.hvbattery4tempcircle.setSizePolicy(sizePolicy)
        self.hvbattery4tempcircle.setMinimumSize(QtCore.QSize(71, 71))
        self.hvbattery4tempcircle.setStyleSheet("border-radius: 20px;\n"
"background-color: rgb(0, 255, 0);")
        self.hvbattery4tempcircle.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.hvbattery4tempcircle.setFrameShadow(QtWidgets.QFrame.Raised)
        self.hvbattery4tempcircle.setObjectName("hvbattery4tempcircle")
        self.hvbattery4temp = QtWidgets.QLabel(self.hvbattery4tempcircle)
        self.hvbattery4temp.setGeometry(QtCore.QRect(0, 10, 81, 51))
        self.hvbattery4temp.setAlignment(QtCore.Qt.AlignCenter)
        self.hvbattery4temp.setObjectName("hvbattery4temp")
        self.verticalLayout_6.addWidget(self.hvbattery4tempcircle)
        self.hvbatterytempgrid.addWidget(self.hvbattery4tempframe, 0, 3, 1, 1)
        self.hvbattery5tempframe = QtWidgets.QFrame(self.layoutWidget)
        self.hvbattery5tempframe.setStyleSheet("")
        self.hvbattery5tempframe.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.hvbattery5tempframe.setFrameShadow(QtWidgets.QFrame.Raised)
        self.hvbattery5tempframe.setObjectName("hvbattery5tempframe")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.hvbattery5tempframe)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.hvbattery5templabel = QtWidgets.QLabel(self.hvbattery5tempframe)
        self.hvbattery5templabel.setStyleSheet(" font-weight: bold;\n"
"color: #60AEEE;")
        self.hvbattery5templabel.setAlignment(QtCore.Qt.AlignCenter)
        self.hvbattery5templabel.setObjectName("hvbattery5templabel")
        self.verticalLayout_7.addWidget(self.hvbattery5templabel)
        self.hvbattery5tempcircle = QtWidgets.QFrame(self.hvbattery5tempframe)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.hvbattery5tempcircle.sizePolicy().hasHeightForWidth())
        self.hvbattery5tempcircle.setSizePolicy(sizePolicy)
        self.hvbattery5tempcircle.setMinimumSize(QtCore.QSize(71, 71))
        self.hvbattery5tempcircle.setStyleSheet("border-radius: 20px;\n"
"background-color: rgb(0, 255, 0);")
        self.hvbattery5tempcircle.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.hvbattery5tempcircle.setFrameShadow(QtWidgets.QFrame.Raised)
        self.hvbattery5tempcircle.setObjectName("hvbattery5tempcircle")
        self.hvbattery5temp = QtWidgets.QLabel(self.hvbattery5tempcircle)
        self.hvbattery5temp.setGeometry(QtCore.QRect(0, 10, 81, 51))
        self.hvbattery5temp.setAlignment(QtCore.Qt.AlignCenter)
        self.hvbattery5temp.setObjectName("hvbattery5temp")
        self.verticalLayout_7.addWidget(self.hvbattery5tempcircle)
        self.hvbatterytempgrid.addWidget(self.hvbattery5tempframe, 0, 4, 1, 1)
        self.hvbattery2tempframe = QtWidgets.QFrame(self.layoutWidget)
        self.hvbattery2tempframe.setStyleSheet("")
        self.hvbattery2tempframe.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.hvbattery2tempframe.setFrameShadow(QtWidgets.QFrame.Raised)
        self.hvbattery2tempframe.setObjectName("hvbattery2tempframe")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.hvbattery2tempframe)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.hvbattery2templabel = QtWidgets.QLabel(self.hvbattery2tempframe)
        self.hvbattery2templabel.setStyleSheet(" font-weight: bold;\n"
"color: #60AEEE;")
        self.hvbattery2templabel.setAlignment(QtCore.Qt.AlignCenter)
        self.hvbattery2templabel.setObjectName("hvbattery2templabel")
        self.verticalLayout_4.addWidget(self.hvbattery2templabel)
        self.hvbattery2tempcircle = QtWidgets.QFrame(self.hvbattery2tempframe)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.hvbattery2tempcircle.sizePolicy().hasHeightForWidth())
        self.hvbattery2tempcircle.setSizePolicy(sizePolicy)
        self.hvbattery2tempcircle.setMinimumSize(QtCore.QSize(71, 71))
        self.hvbattery2tempcircle.setStyleSheet("border-radius: 20px;\n"
"background-color: rgb(0, 255, 0);")
        self.hvbattery2tempcircle.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.hvbattery2tempcircle.setFrameShadow(QtWidgets.QFrame.Raised)
        self.hvbattery2tempcircle.setObjectName("hvbattery2tempcircle")
        self.hvbattery2temp = QtWidgets.QLabel(self.hvbattery2tempcircle)
        self.hvbattery2temp.setGeometry(QtCore.QRect(0, 10, 81, 51))
        self.hvbattery2temp.setAlignment(QtCore.Qt.AlignCenter)
        self.hvbattery2temp.setObjectName("hvbattery2templ")
        self.verticalLayout_4.addWidget(self.hvbattery2tempcircle)
        self.hvbatterytempgrid.addWidget(self.hvbattery2tempframe, 0, 1, 1, 1)
        self.hvbattery1tempframe = QtWidgets.QFrame(self.layoutWidget)
        self.hvbattery1tempframe.setStyleSheet("")
        self.hvbattery1tempframe.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.hvbattery1tempframe.setFrameShadow(QtWidgets.QFrame.Raised)
        self.hvbattery1tempframe.setObjectName("hvbattery1tempframe")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.hvbattery1tempframe)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.hvbattery1templabel = QtWidgets.QLabel(self.hvbattery1tempframe)
        self.hvbattery1templabel.setStyleSheet(" font-weight: bold;\n"
"color: #60AEEE;")
        self.hvbattery1templabel.setAlignment(QtCore.Qt.AlignCenter)
        self.hvbattery1templabel.setObjectName("hvbattery1templabel")
        self.verticalLayout_3.addWidget(self.hvbattery1templabel)
        self.hvbattery1tempcircle = QtWidgets.QFrame(self.hvbattery1tempframe)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.hvbattery1tempcircle.sizePolicy().hasHeightForWidth())
        self.hvbattery1tempcircle.setSizePolicy(sizePolicy)
        self.hvbattery1tempcircle.setMinimumSize(QtCore.QSize(71, 71))
        self.hvbattery1tempcircle.setStyleSheet("border-radius: 20px;\n"
"background-color: rgb(0, 255, 0);")
        self.hvbattery1tempcircle.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.hvbattery1tempcircle.setFrameShadow(QtWidgets.QFrame.Raised)
        self.hvbattery1tempcircle.setObjectName("hvbattery1tempcircle")
        self.hvbattery1temp = QtWidgets.QLabel(self.hvbattery1tempcircle)
        self.hvbattery1temp.setGeometry(QtCore.QRect(0, 10, 81, 51))
        self.hvbattery1temp.setAlignment(QtCore.Qt.AlignCenter)
        self.hvbattery1temp.setObjectName("hvbattery1temp")
        self.verticalLayout_3.addWidget(self.hvbattery1tempcircle)
        self.hvbatterytempgrid.addWidget(self.hvbattery1tempframe, 0, 0, 1, 1)
        self.hvbattery7tempframe = QtWidgets.QFrame(self.layoutWidget)
        self.hvbattery7tempframe.setStyleSheet("")
        self.hvbattery7tempframe.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.hvbattery7tempframe.setFrameShadow(QtWidgets.QFrame.Raised)
        self.hvbattery7tempframe.setObjectName("hvbattery7tempframe")
        self.verticalLayout_11 = QtWidgets.QVBoxLayout(self.hvbattery7tempframe)
        self.verticalLayout_11.setObjectName("verticalLayout_11")
        self.hvbattery7templabel = QtWidgets.QLabel(self.hvbattery7tempframe)
        self.hvbattery7templabel.setStyleSheet(" font-weight: bold;\n"
"color: #60AEEE;")
        self.hvbattery7templabel.setAlignment(QtCore.Qt.AlignCenter)
        self.hvbattery7templabel.setObjectName("hvbattery7templabel")
        self.verticalLayout_11.addWidget(self.hvbattery7templabel)
        self.hvbattery7tempcircle = QtWidgets.QFrame(self.hvbattery7tempframe)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.hvbattery7tempcircle.sizePolicy().hasHeightForWidth())
        self.hvbattery7tempcircle.setSizePolicy(sizePolicy)
        self.hvbattery7tempcircle.setMinimumSize(QtCore.QSize(71, 71))
        self.hvbattery7tempcircle.setStyleSheet("border-radius: 20px;\n"
"background-color: rgb(0, 255, 0);")
        self.hvbattery7tempcircle.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.hvbattery7tempcircle.setFrameShadow(QtWidgets.QFrame.Raised)
        self.hvbattery7tempcircle.setObjectName("hvbattery7tempcircle")
        self.hvbattery7temp = QtWidgets.QLabel(self.hvbattery7tempcircle)
        self.hvbattery7temp.setGeometry(QtCore.QRect(0, 10, 81, 51))
        self.hvbattery7temp.setAlignment(QtCore.Qt.AlignCenter)
        self.hvbattery7temp.setObjectName("hvbattery7temp")
        self.verticalLayout_11.addWidget(self.hvbattery7tempcircle)
        self.hvbatterytempgrid.addWidget(self.hvbattery7tempframe, 1, 1, 1, 1)
        self.hvbattery9tempframe = QtWidgets.QFrame(self.layoutWidget)
        self.hvbattery9tempframe.setStyleSheet("")
        self.hvbattery9tempframe.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.hvbattery9tempframe.setFrameShadow(QtWidgets.QFrame.Raised)
        self.hvbattery9tempframe.setObjectName("hvbattery9tempframe")
        self.verticalLayout_12 = QtWidgets.QVBoxLayout(self.hvbattery9tempframe)
        self.verticalLayout_12.setObjectName("verticalLayout_12")
        self.hvbattery9templabel = QtWidgets.QLabel(self.hvbattery9tempframe)
        self.hvbattery9templabel.setStyleSheet(" font-weight: bold;\n"
"color: #60AEEE;")
        self.hvbattery9templabel.setAlignment(QtCore.Qt.AlignCenter)
        self.hvbattery9templabel.setObjectName("hvbattery9templabel")
        self.verticalLayout_12.addWidget(self.hvbattery9templabel)
        self.hvbattery9tempcircle = QtWidgets.QFrame(self.hvbattery9tempframe)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.hvbattery9tempcircle.sizePolicy().hasHeightForWidth())
        self.hvbattery9tempcircle.setSizePolicy(sizePolicy)
        self.hvbattery9tempcircle.setMinimumSize(QtCore.QSize(71, 71))
        self.hvbattery9tempcircle.setStyleSheet("border-radius: 20px;\n"
"background-color: rgb(0, 255, 0);")
        self.hvbattery9tempcircle.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.hvbattery9tempcircle.setFrameShadow(QtWidgets.QFrame.Raised)
        self.hvbattery9tempcircle.setObjectName("hvbattery9tempcircle")
        self.hvbattery9temp = QtWidgets.QLabel(self.hvbattery9tempcircle)
        self.hvbattery9temp.setGeometry(QtCore.QRect(0, 10, 81, 51))
        self.hvbattery9temp.setAlignment(QtCore.Qt.AlignCenter)
        self.hvbattery9temp.setObjectName("hvbattery9temp")
        self.verticalLayout_12.addWidget(self.hvbattery9tempcircle)
        self.hvbatterytempgrid.addWidget(self.hvbattery9tempframe, 1, 3, 1, 1)

        self.layoutWidget2 = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget2.setGeometry(QtCore.QRect(690, 60, 761, 731))
        self.layoutWidget2.setObjectName("layoutWidget2")
        self.linegraphgrid = QtWidgets.QGridLayout(self.layoutWidget2)
        self.linegraphgrid.setContentsMargins(0, 0, 0, 0)
        self.linegraphgrid.setObjectName("linegraphgrid")

        self.lvframe = QtWidgets.QFrame(self.layoutWidget2)
        self.lvframe.setFrameShape(QtWidgets.QFrame.Box)
        self.lvframe.setFrameShadow(QtWidgets.QFrame.Raised)
        self.lvframe.setObjectName("lvframe")
        self.grid_lvframe = QtWidgets.QVBoxLayout(self.lvframe)
        self.grid_lvframe.setObjectName("grid_lvframe")
        self.lvlabel = QtWidgets.QLabel(self.lvframe)
        self.lvlabel.setGeometry(QtCore.QRect(0, 0, 381, 41))
        self.lvlabel.setStyleSheet("font: 14pt \".AppleSystemUIFont\";\n"
" font-weight: bold;\n"
"color: #60AEEE;")
        self.lvlabel.setAlignment(QtCore.Qt.AlignCenter)
        self.lvlabel.setObjectName("lvlabel")
        self.lvgraph = pg.PlotWidget()
        self.lvgraph.setYRange(0, 100)
        self.lvgraph_x = [x for x in range(1, 10)]
        self.lvgraph_y = [random.randint(0, 100) for i in range(1, 10)]
        self.lvgraph_dataline = self.lvgraph.plot(self.lvgraph_x, self.lvgraph_y)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(False)
        self.lvgraph.setSizePolicy(sizePolicy)
        self.grid_lvframe.addWidget(self.lvlabel)
        self.grid_lvframe.addWidget(self.lvgraph)
        self.linegraphgrid.addWidget(self.lvframe, 0, 0, 1, 1)

        self.hvframe = QtWidgets.QFrame(self.layoutWidget2)
        self.hvframe.setFrameShape(QtWidgets.QFrame.Box)
        self.hvframe.setFrameShadow(QtWidgets.QFrame.Raised)
        self.hvframe.setObjectName("hvframe")
        self.grid_hvframe = QtWidgets.QVBoxLayout(self.hvframe)
        self.grid_hvframe.setObjectName("grid_hvframe")
        self.hvlabel = QtWidgets.QLabel(self.hvframe)
        self.hvlabel.setGeometry(QtCore.QRect(0, 10, 381, 20))
        self.hvlabel.setStyleSheet("font: 14pt \".AppleSystemUIFont\";\n"
" font-weight: bold;\n"
"color: #60AEEE;")
        self.hvlabel.setAlignment(QtCore.Qt.AlignCenter)
        self.hvlabel.setObjectName("hvlabel")
        self.hvgraph = pg.PlotWidget()
        self.hvgraph.setYRange(0, 100)
        self.hvgraph_x = [x for x in range(1, 10)]
        self.hvgraph_y = [random.randint(0, 100) for i in range(1, 10)]
        self.hvgraph_dataline = self.hvgraph.plot(self.hvgraph_x, self.hvgraph_y)
        self.hvgraph.setSizePolicy(sizePolicy)
        self.grid_hvframe.addWidget(self.hvlabel)
        self.grid_hvframe.addWidget(self.hvgraph)
        self.linegraphgrid.addWidget(self.hvframe, 0, 1, 1, 1)

        self.lvcurrentframe = QtWidgets.QFrame(self.layoutWidget2)
        self.lvcurrentframe.setFrameShape(QtWidgets.QFrame.Box)
        self.lvcurrentframe.setFrameShadow(QtWidgets.QFrame.Raised)
        self.lvcurrentframe.setObjectName("lvcurrentframe")
        self.grid_lvcurrentframe = QtWidgets.QVBoxLayout(self.lvcurrentframe)
        self.grid_lvcurrentframe.setObjectName("grid_lvcurrentframe")
        self.lvcurrentlabel = QtWidgets.QLabel(self.lvcurrentframe)
        self.lvcurrentlabel.setGeometry(QtCore.QRect(0, 10, 381, 20))
        self.lvcurrentlabel.setStyleSheet("font: 14pt \".AppleSystemUIFont\";\n"
" font-weight: bold;\n"
"color: #60AEEE;")
        self.lvcurrentlabel.setAlignment(QtCore.Qt.AlignCenter)
        self.lvcurrentlabel.setObjectName("lvcurrentlabel")
        self.lvcurrentgraph = pg.PlotWidget()
        self.lvcurrentgraph.setYRange(0, 100)
        self.lvcurrent_x = [x for x in range(1, 10)]
        self.lvcurrent_y = [random.randint(0, 100) for i in range(1, 10)]
        self.lvcurrent_dataline = self.lvcurrentgraph.plot(self.lvcurrent_x, self.lvcurrent_y)
        self.lvgraph.setSizePolicy(sizePolicy)
        self.grid_lvcurrentframe.addWidget(self.lvcurrentlabel)
        self.grid_lvcurrentframe.addWidget(self.lvcurrentgraph)
        self.linegraphgrid.addWidget(self.lvcurrentframe, 1, 0, 1, 1)

        self.hvcurrentframe = QtWidgets.QFrame(self.layoutWidget2)
        self.hvcurrentframe.setFrameShape(QtWidgets.QFrame.Box)
        self.hvcurrentframe.setFrameShadow(QtWidgets.QFrame.Raised)
        self.hvcurrentframe.setObjectName("hvcurrentframe")
        self.grid_hvcurrentframe = QtWidgets.QVBoxLayout(self.hvcurrentframe)
        self.grid_hvcurrentframe.setObjectName("grid_hvcurrentframe")
        self.hvcurrentlabel = QtWidgets.QLabel(self.hvcurrentframe)
        self.hvcurrentlabel.setGeometry(QtCore.QRect(0, 10, 381, 20))
        self.hvcurrentlabel.setStyleSheet("color: #60AEEE;\n"
"font: 14pt \".AppleSystemUIFont\";\n"
" font-weight: bold;")
        self.hvcurrentlabel.setAlignment(QtCore.Qt.AlignCenter)
        self.hvcurrentlabel.setObjectName("hvcurrentlabel")
        self.hvcurrentgraph = pg.PlotWidget()
        self.hvcurrentgraph.setYRange(0, 100)
        self.hvcurrent_x = [x for x in range(1, 10)]
        self.hvcurrent_y = [random.randint(0, 100) for i in range(1, 10)]
        self.hvcurrent_dataline = self.hvcurrentgraph.plot(self.hvcurrent_x, self.hvcurrent_y)
        self.hvcurrentgraph.setSizePolicy(sizePolicy)
        self.grid_hvcurrentframe.addWidget(self.hvcurrentlabel)
        self.grid_hvcurrentframe.addWidget(self.hvcurrentgraph)
        self.linegraphgrid.addWidget(self.hvcurrentframe, 1, 1, 1, 1)

        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(60, 220, 511, 141))
        self.widget.setObjectName("widget")
        self.powerlvlayout = QtWidgets.QHBoxLayout(self.widget)
        self.powerlvlayout.setContentsMargins(0, 0, 0, 0)
        self.powerlvlayout.setObjectName("powerlvlayout")
        self.powerstatusframe = QtWidgets.QFrame(self.widget)
        self.powerstatusframe.setFrameShape(QtWidgets.QFrame.Box)
        self.powerstatusframe.setFrameShadow(QtWidgets.QFrame.Raised)
        self.powerstatusframe.setObjectName("powerstatusframe")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.powerstatusframe)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.powerstatuslabel = QtWidgets.QLabel(self.powerstatusframe)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.powerstatuslabel.sizePolicy().hasHeightForWidth())
        self.powerstatuslabel.setSizePolicy(sizePolicy)
        self.powerstatuslabel.setStyleSheet(" font-weight: bold;\n"
"color: #33D918;\n"
"\n"
"")
        self.powerstatuslabel.setAlignment(QtCore.Qt.AlignCenter)
        self.powerstatuslabel.setObjectName("powerstatuslabel")
        self.verticalLayout_2.addWidget(self.powerstatuslabel)
        self.powerbutton = QtWidgets.QPushButton(self.powerstatusframe)
        self.powerbutton.setMinimumSize(QtCore.QSize(181, 71))
        self.powerbutton.setStyleSheet("background-color: rgb(0, 255, 0);\n")
        self.powerbutton.setObjectName("powerbutton")
        self.verticalLayout_2.addWidget(self.powerbutton)
        self.powerlvlayout.addWidget(self.powerstatusframe)
        self.lvbatterycontainer = QtWidgets.QFrame(self.widget)
        self.lvbatterycontainer.setFrameShape(QtWidgets.QFrame.Box)
        self.lvbatterycontainer.setFrameShadow(QtWidgets.QFrame.Raised)
        self.lvbatterycontainer.setObjectName("lvbatterycontainer")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.lvbatterycontainer)
        self.verticalLayout.setObjectName("verticalLayout")
        self.lvbatterylabel = QtWidgets.QLabel(self.lvbatterycontainer)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lvbatterylabel.sizePolicy().hasHeightForWidth())
        self.lvbatterylabel.setSizePolicy(sizePolicy)
        self.lvbatterylabel.setStyleSheet(" font-weight: bold;\n"
"color: #60AEEE;")
        self.lvbatterylabel.setAlignment(QtCore.Qt.AlignCenter)
        self.lvbatterylabel.setObjectName("lvbatterylabel")
        self.verticalLayout.addWidget(self.lvbatterylabel)
        self.lvbatterylayout = QtWidgets.QHBoxLayout()
        self.lvbatterylayout.setObjectName("lvbatterylayout")
        self.lvbatteryframe = QtWidgets.QFrame(self.lvbatterycontainer)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lvbatteryframe.sizePolicy().hasHeightForWidth())
        self.lvbatteryframe.setSizePolicy(sizePolicy)
        self.lvbatteryframe.setMinimumSize(QtCore.QSize(91, 91))
        self.lvbatteryframe.setStyleSheet("border-radius: 20px;\n"
"background-color: rgb(0, 255, 0);")
        self.lvbatteryframe.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.lvbatteryframe.setFrameShadow(QtWidgets.QFrame.Raised)
        self.lvbatteryframe.setObjectName("lvbatteryframe")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.lvbatteryframe)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.lvbatterytemp = QtWidgets.QLabel(self.lvbatteryframe)
        self.lvbatterytemp.setStyleSheet("font: 18pt \".AppleSystemUIFont\";")
        self.lvbatterytemp.setScaledContents(False)
        self.lvbatterytemp.setAlignment(QtCore.Qt.AlignCenter)
        self.lvbatterytemp.setObjectName("lvbatterytemp")
        self.gridLayout_4.addWidget(self.lvbatterytemp, 0, 0, 1, 1)
        self.lvbatterylayout.addWidget(self.lvbatteryframe)
        self.verticalLayout.addLayout(self.lvbatterylayout)
        self.powerlvlayout.addWidget(self.lvbatterycontainer)
        self.convertertempframe = QtWidgets.QFrame(self.widget)
        self.convertertempframe.setStyleSheet("")
        self.convertertempframe.setFrameShape(QtWidgets.QFrame.Box)
        self.convertertempframe.setFrameShadow(QtWidgets.QFrame.Raised)
        self.convertertempframe.setObjectName("convertertempframe")
        self.verticalLayout_13 = QtWidgets.QVBoxLayout(self.convertertempframe)
        self.verticalLayout_13.setObjectName("verticalLayout_13")
        self.convertertemplabel = QtWidgets.QLabel(self.convertertempframe)
        self.convertertemplabel.setStyleSheet(" font-weight: bold;\n"
"color: #60AEEE;")
        self.convertertemplabel.setAlignment(QtCore.Qt.AlignCenter)
        self.convertertemplabel.setObjectName("convertertemplabel")
        self.verticalLayout_13.addWidget(self.convertertemplabel)
        self.convertertempcircle = QtWidgets.QFrame(self.convertertempframe)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.convertertempcircle.sizePolicy().hasHeightForWidth())
        self.convertertempcircle.setSizePolicy(sizePolicy)
        self.convertertempcircle.setMinimumSize(QtCore.QSize(71, 71))
        self.convertertempcircle.setStyleSheet("border-radius: 20px;\n"
"background-color: rgb(0, 255, 0);")
        self.convertertempcircle.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.convertertempcircle.setFrameShadow(QtWidgets.QFrame.Raised)
        self.convertertempcircle.setObjectName("convertertempcircle")
        self.gridLayout = QtWidgets.QGridLayout(self.convertertempcircle)
        self.gridLayout.setObjectName("gridLayout")
        self.convertertemp = QtWidgets.QLabel(self.convertertempcircle)
        self.convertertemp.setAlignment(QtCore.Qt.AlignCenter)
        self.convertertemp.setObjectName("convertertemp")
        self.gridLayout.addWidget(self.convertertemp, 0, 0, 1, 1)
        self.verticalLayout_13.addWidget(self.convertertempcircle)
        self.powerlvlayout.addWidget(self.convertertempframe)


        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Hyperloop Testing Interface"))
        self.hvbatterytemplabel.setText(_translate("MainWindow", "HV Battery Temperatures"))
        self.hvbattery6templabel.setText(_translate("MainWindow", "Battery 6"))
        self.hvbattery6temp.setText(_translate("MainWindow", "40°c"))
        self.hvbattery10templabel.setText(_translate("MainWindow", "Battery 10"))
        self.hvbattery10temp.setText(_translate("MainWindow", "40°c"))
        self.hvbattery8templabel.setText(_translate("MainWindow", "Battery 8"))
        self.hvbattery8temp.setText(_translate("MainWindow", "40°c"))
        self.hvbattery3templabel.setText(_translate("MainWindow", "Battery 3"))
        self.hvbattery3temp.setText(_translate("MainWindow", "40°c"))
        self.hvbattery4templabel.setText(_translate("MainWindow", "Battery 4"))
        self.hvbattery4temp.setText(_translate("MainWindow", "40°c"))
        self.hvbattery5templabel.setText(_translate("MainWindow", "Battery 5"))
        self.hvbattery5temp.setText(_translate("MainWindow", "40°c"))
        self.hvbattery2templabel.setText(_translate("MainWindow", "Battery 2"))
        self.hvbattery2temp.setText(_translate("MainWindow", "40°c"))
        self.hvbattery1templabel.setText(_translate("MainWindow", "Battery 1"))
        self.hvbattery1temp.setText(_translate("MainWindow", "40°c"))
        self.hvbattery7templabel.setText(_translate("MainWindow", "Battery 7"))
        self.hvbattery7temp.setText(_translate("MainWindow", "40°c"))
        self.hvbattery9templabel.setText(_translate("MainWindow", "Battery 9"))
        self.hvbattery9temp.setText(_translate("MainWindow", "40°c"))
        self.lvlabel.setText(_translate("MainWindow", "Low Voltage"))
        self.hvlabel.setText(_translate("MainWindow", "High Voltage"))
        self.lvcurrentlabel.setText(_translate("MainWindow", "LV Current"))
        self.hvcurrentlabel.setText(_translate("MainWindow", "HV Current"))
        self.powerstatuslabel.setText(_translate("MainWindow", "Status: ON"))
        self.powerbutton.setText(_translate("MainWindow", "Power Off"))
        self.lvbatterylabel.setText(_translate("MainWindow", "LV Battery"))
        self.lvbatterytemp.setText(_translate("MainWindow", "40°c"))
        self.convertertemplabel.setText(_translate("MainWindow", "Converter Temp"))
        self.convertertemp.setText(_translate("MainWindow", "40°c"))