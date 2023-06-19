import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import QtCore
from login_ui import Ui_MainWindow
from karayel import karayelPage
from PyQt5.uic import loadUi
import pymysql as sql


class loginPage(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.loginForm = Ui_MainWindow() 
        self.loginForm.setupUi(self)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.loginForm.profilLE.setFocus(False)
        self.loginForm.mainF.setFocus(True)
        self.loginForm.closeBtn.clicked.connect(self.cikis)
        self.homeAc = karayelPage()
        self.loginForm.girisBtn.clicked.connect(self.girisYapBtn)
        self.loginForm.passLE.returnPressed.connect(self.girisYapBtn)
        self.loginForm.profilLE.returnPressed.connect(self.girisYapBtn)
        
        self.loginForm.mainF.mouseMoveEvent = self.MoveWindow


    def girisYapBtn(self):  
        conn = sql.connect(
        host = "localhost",
        user="root",
        password="root",
        database="karayel"  
        )
        im = conn.cursor()
        user = self.loginForm.profilLE.text()
        password = self.loginForm.passLE.text()
        veriCek  = "SELECT * FROM kullanici WHERE Ad = '" + user +"' AND Sifre ='"+password+"'"
        im.execute(veriCek)
        users=im.fetchone()
        username_control = "SELECT ad FROM kullanici"
        if user == "":
            QMessageBox.warning(self,"Hata","Kullanıcı Adı Boş Bırakılamaz!")
        elif password == "":
            QMessageBox.warning(self,"Hata","Şifre Boş Bırakılamaz!")
        elif users:
            print("GİRİS BASARİLİ")
            self.close()
            self.homeAc.show()
        else:
            im.execute(username_control)
            usernames = im.fetchall()
            if user in [username[0] for username in usernames]:
                QMessageBox.warning(self,"Hata","Şifreniz Yanlış!")
            else:
                QMessageBox.warning(self,"Hata","Böyle Bir Kullanıcı Bulunamadı!")
        conn.close()

  
    def cikis(self):
        self.close()

        
    def MoveWindow(self,event):
        if self.isMaximized() == False:
            self.move(self.pos() + event.globalPos() - self.clickPosition)
            self.clickPosition = event.globalPos()
            event.accept()
            pass
    def mousePressEvent(self,event):
        self.clickPosition = event.globalPos()
        pass

if __name__ == '_main_':
    app = QApplication(sys.argv)
    app.setStyleSheet('''
        QWidget {
            font-size: 35px;
        }
    ''')
    loginPage = loginPage()
    loginPage.show()
    sys.exit(app.exec_())