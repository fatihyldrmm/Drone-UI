# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'login.ui'
#
# Created by: PyQt5 UI code generator 5.15.8
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(1450, 800)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QtCore.QSize(1450, 800))
        MainWindow.setMaximumSize(QtCore.QSize(1450, 800))
        MainWindow.setWindowOpacity(1.0)
        MainWindow.setStyleSheet("")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setStyleSheet("*{\n"
"    border-style:none;\n"
"    color: rgb(211, 211, 211);\n"
"}\n"
"#mainF{\n"
"    background-image: url(:/images/images/login1.jpg);\n"
"}\n"
"#profilLbl,#passLbl{\n"
"    background-color: rgba(244,0,0,255);\n"
"    border-radius:1px;\n"
"}\n"
"#profilLE,#passLE{\n"
"    background-color: Transparent;\n"
"}\n"
"#girisBtn{\n"
"    border-radius:8px;\n"
"    background-color: rgba(244,0,0,255);\n"
"    color: rgb(0, 0, 0);\n"
"}\n"
"#girisBtn:hover{\n"
"    color: rgb(0, 0, 0);\n"
"    background-color: rgb(180, 20, 20);\n"
"}\n"
"#closeBtn{\n"
"    color: rgb(214, 214, 214);\n"
"    background-color: rgb(150, 11, 11);\n"
"    border-bottom-left-radius:11px;\n"
"}\n"
"#closeBtn:hover{\n"
"    color: rgb(200, 200, 200);\n"
"    background-color: rgb(140, 20, 20);\n"
"}\n"
"\n"
"")
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.mainF = QtWidgets.QFrame(self.centralwidget)
        self.mainF.setStyleSheet("")
        self.mainF.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.mainF.setFrameShadow(QtWidgets.QFrame.Raised)
        self.mainF.setLineWidth(1)
        self.mainF.setObjectName("mainF")
        self.profilLE = QtWidgets.QLineEdit(self.mainF)
        self.profilLE.setGeometry(QtCore.QRect(140, 362, 411, 31))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.profilLE.setFont(font)
        self.profilLE.setWhatsThis("")
        self.profilLE.setStyleSheet("")
        self.profilLE.setInputMask("")
        self.profilLE.setObjectName("profilLE")
        self.passLE = QtWidgets.QLineEdit(self.mainF)
        self.passLE.setGeometry(QtCore.QRect(140, 443, 411, 31))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.passLE.setFont(font)
        self.passLE.setStyleSheet("")
        self.passLE.setEchoMode(QtWidgets.QLineEdit.Password)
        self.passLE.setObjectName("passLE")
        self.girisBtn = QtWidgets.QPushButton(self.mainF)
        self.girisBtn.setGeometry(QtCore.QRect(130, 520, 351, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.girisBtn.setFont(font)
        self.girisBtn.setObjectName("girisBtn")
        self.closeBtn = QtWidgets.QPushButton(self.mainF)
        self.closeBtn.setGeometry(QtCore.QRect(1410, 0, 41, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.closeBtn.setFont(font)
        self.closeBtn.setObjectName("closeBtn")
        self.userIconLbl = QtWidgets.QLabel(self.mainF)
        self.userIconLbl.setGeometry(QtCore.QRect(553, 363, 30, 30))
        self.userIconLbl.setText("")
        self.userIconLbl.setPixmap(QtGui.QPixmap(":/icons/pngIcons/icons8_account_30px.png"))
        self.userIconLbl.setScaledContents(True)
        self.userIconLbl.setObjectName("userIconLbl")
        self.passIconLbl = QtWidgets.QLabel(self.mainF)
        self.passIconLbl.setGeometry(QtCore.QRect(555, 447, 27, 27))
        self.passIconLbl.setText("")
        self.passIconLbl.setPixmap(QtGui.QPixmap(":/icons/pngIcons/icons8_lock_30px.png"))
        self.passIconLbl.setScaledContents(True)
        self.passIconLbl.setObjectName("passIconLbl")
        self.horizontalLayout.addWidget(self.mainF)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.profilLE.setPlaceholderText(_translate("MainWindow", "Kullanıcı adı"))
        self.passLE.setPlaceholderText(_translate("MainWindow", "Şifre"))
        self.girisBtn.setText(_translate("MainWindow", "GİRİŞ"))
        self.closeBtn.setText(_translate("MainWindow", "X"))
import resoruces_rc


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())