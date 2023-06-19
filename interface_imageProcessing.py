import sys
import cv2
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton
import numpy as np

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("\n"
"background-color: rgb(0,0,0);\n"
"border-radius:20px;\n"
"")
        self.setGeometry(100, 100, 640, 480)
        self.setFixedSize(600, 460)

        # Etiketler oluştur
        self.label = QLabel(self)
        self.label.setGeometry(30, 10, 510, 397.5)
        self.label.setScaledContents(True)
        self.label.setStyleSheet("\n"
"background-color: rgb(0, 0,75);\n"
"border-radius:20px;\n"
"")
               

        # Buton oluştur
        self.button = QPushButton('Kamera Aç', self)
        self.button.setStyleSheet("QPushButton{\n"
"background-color: rgb(199, 23, 0);\n"
"font: 75 10pt \"Arial\";\n"
"color: rgb(255, 255, 255);\n"
"border-radius:20px;\n"
"}\n"
"QPushButton:pressed {                \n"
"background-color: rgba(255, 100, 80, 170);\n"
"}\n"
"")
                               
        self.button.setGeometry(450, 416, 120, 40)
        self.button.clicked.connect(self.start_camera)
        
        self.camera = None
        
        self.button = QPushButton('Kamera kapat', self)
        self.button.setStyleSheet("QPushButton{\n"
"background-color: rgb(199, 23, 0);\n"
"font: 75 10pt \"Arial\";\n"
"color: rgb(255, 255, 255);\n"
"border-radius:20px;\n"
"}\n"
"QPushButton:pressed {                \n"
"background-color: rgba(255, 100, 80, 170);\n"
"}\n"
"")
        self.button.setGeometry(10, 416, 120, 40)
        self.button.clicked.connect(self.stop_camera)
        
        self.camera = None
    def start_camera(self):
        # Kamera aygıtına erişim sağla
        self.camera = cv2.VideoCapture(0)
        

        # Kamera görüntüsünü ekrana göster
        while True:
            ret, pic = self.camera.read()
            if ret:
                # Buton durdurma fonksiyonu
                self.button.clicked.connect(self.stop_camera)
                    #hsv renk uzayına çevirme
                hsv = cv2.cvtColor(pic, cv2.COLOR_BGR2HSV)
                #mavi alt ve ust sınır belirleme
                lower_blue = np.array([75, 120, 120])
                upper_blue = np.array([130, 255, 255])
                #mavi renge gore maskeleme
                mask = cv2.inRange(hsv, lower_blue, upper_blue)
                #blurlama için gray'e cevirme
                gray = cv2.cvtColor(pic,cv2.COLOR_BGR2GRAY)
                #blurlama
                blur = cv2.bilateralFilter(gray, 10, 80,95)
                #canny detection
                canny = cv2.Canny(blur,80,150)
                #çember bulma
                circles = cv2.HoughCircles(canny,cv2.HOUGH_GRADIENT, 1, 20,param1=10,param2=30,minRadius = 10,maxRadius=220)
                #sınırları konturleme
                contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                for cnt in contours:
                 area = cv2.contourArea(cnt)
                 #alan sınırlaması
                 if area > 60:
                  (x, y), radius = cv2.minEnclosingCircle(cnt)
                  if circles is not None:
                   circles = np.uint16(np.around(circles))
                   for i in circles[0,:]: 
                    cv2.circle(pic, (int(x), int(y)), int(radius), (0, 0, 255), 4)
                #sonuclarıgoruntuleme
                self.display_cam(pic)
                # Arayüzü güncelle
                QApplication.processEvents()
                
            else:
                break

    def display_cam(self,img):
               # OpenCV görüntüsünü QImage'e dönüştür
                image = QImage(img, img.shape[1], img.shape[0], QImage.Format_RGB888).rgbSwapped()
                pixmap = QPixmap.fromImage(image)
               # Etiketleri güncelle
                self.label.setPixmap(pixmap)
                self.label.setAlignment(Qt.AlignCenter)
                
    def stop_camera(self):
        # Kamera aygıtını durdur
        self.camera.release()
        self.label.clear()
        cv2.destroyAllWindows()
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


