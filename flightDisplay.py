import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel,QComboBox,QVBoxLayout
from PyQt5.QtCore import Qt, QTimer
from dronekit import connect, VehicleMode



class Example(QWidget):
    
    def __init__(self):
        super().__init__()
        self.initUI()
        
        
    def initUI(self):

        #tittle label
        self.tittleLabel=QLabel(self)
        self.tittleLabel.setText("KARAYEL HAVACILIK FLİGHT DİSPLAY")
        self.tittleLabel.move(5,15)
        self.tittleLabel.resize(360,40)
        self.tittleLabel.setStyleSheet("font: 87 12pt \"Arial\";\n"
"color:rgb(220,220,220)")
        
        #yaw textlabel
        self.yaw_label = QLabel(self)
        self.yaw_label.setText("YAW DEĞERİ:")
        self.yaw_label.move(30, 100)
        self.yaw_label.resize(130, 40)
        self.yaw_label.setStyleSheet("font: 87 12pt \"Arial\";\n"
"color:rgb(0,240 ,255)")
        self.yaw_label.setAlignment(Qt.AlignCenter)

        # Yaw değerini göstermek için bir QLabel oluşturun
        self.data_yaw_label = QLabel(self)
        self.data_yaw_label.setText("0")
        self.data_yaw_label.move(30, 150)
        self.data_yaw_label.resize(100, 30)
        self.data_yaw_label.setStyleSheet("font: 87 15pt \"Arial\";\n"
"color:rgb(0,240 ,255)")
        self.data_yaw_label.setAlignment(Qt.AlignCenter)

        #roll degerlabel
        self.data_roll_label= QLabel(self)
        self.data_roll_label.setText("0")
        self.data_roll_label.move(325,150)
        self.data_roll_label.resize(100, 30)
        self.data_roll_label.setStyleSheet("font: 87 16pt \"Arial\";\n"
"color:rgb(255, 0, 0)")
        self.data_roll_label.setAlignment(Qt.AlignCenter)


        #roll textlabel
        self.roll_label = QLabel(self)
        self.roll_label.setText("ROLL DEGERİ:")
        self.roll_label.move(325, 100)
        self.roll_label.resize(140, 40)
        self.roll_label.setStyleSheet("font: 87 12pt \"Arial\";\n"
"color: rgb(255, 0, 0);")
        
        
        #pitch degerlabel
        self.data_pitch_label= QLabel(self)
        self.data_pitch_label.setText("0")
        self.data_pitch_label.move(620,150)
        self.data_pitch_label.resize(100, 30)
        self.data_pitch_label.setStyleSheet("font: 87 16pt \"Arial\";\n"
"color:rgb(0, 255, 0)")
        self.data_pitch_label.setAlignment(Qt.AlignCenter)


        #pitch textlabel
        self.pitch_label = QLabel(self)
        self.pitch_label.setText("PİTCH DEGERİ:")
        self.pitch_label.move(620, 100)
        self.pitch_label.resize(145, 40)
        self.pitch_label.setStyleSheet("font: 87 12pt \"Arial\";\n"
"color: rgb(0, 255, 0);")
        
                
        #yükseklik degerlabel
        self.data_altitude_label= QLabel(self)
        self.data_altitude_label.setText("0")
        self.data_altitude_label.move(620,320)
        self.data_altitude_label.resize(100, 30)
        self.data_altitude_label.setStyleSheet("font: 87 16pt \"Arial\";\n"
"color:rgb(0, 255, 0)")
        self.data_altitude_label.setAlignment(Qt.AlignCenter)


        #yükseklik textlabel
        self.altitude_label = QLabel(self)
        self.altitude_label.setText("YÜKSEKLİK:")
        self.altitude_label.move(620, 270)
        self.altitude_label.resize(145, 40)
        self.altitude_label.setStyleSheet("font: 87 12pt \"Arial\";\n"
"color: rgb(0, 255, 0);")
        
        #D.Hız degerlabel
        self.data_verticalSpeed_label= QLabel(self)
        self.data_verticalSpeed_label.setText("0")
        self.data_verticalSpeed_label.move(325,320)
        self.data_verticalSpeed_label.resize(100, 30)
        self.data_verticalSpeed_label.setStyleSheet("font: 87 16pt \"Arial\";\n"
"color:rgb(255, 0, 0)")
        self.data_verticalSpeed_label.setAlignment(Qt.AlignCenter)


        #D.Hız textlabel
        self.verticalSpeed_label = QLabel(self)
        self.verticalSpeed_label.setText("DİKEY HIZ:")
        self.verticalSpeed_label.move(325, 270)
        self.verticalSpeed_label.resize(145, 40)
        self.verticalSpeed_label.setStyleSheet("font: 87 12pt \"Arial\";\n"
"color: rgb(255, 0, 0);")
        
        #Y.Hız degerlabel
        self.data_horizontalSpeed_label= QLabel(self)
        self.data_horizontalSpeed_label.setText("0")
        self.data_horizontalSpeed_label.move(30,320)
        self.data_horizontalSpeed_label.resize(100, 30)
        self.data_horizontalSpeed_label.setStyleSheet("font: 87 16pt \"Arial\";\n"
"color:rgb(0,240,255)")
        self.data_horizontalSpeed_label.setAlignment(Qt.AlignCenter)


        #Y.Hız textlabel
        self.horizontalSpeed_label = QLabel(self)
        self.horizontalSpeed_label.setText("YATAY HIZ:")
        self.horizontalSpeed_label.move(30, 270)
        self.horizontalSpeed_label.resize(145, 40)
        self.horizontalSpeed_label.setStyleSheet("font: 87 12pt \"Arial\";\n"
"color: rgb(0, 240, 255);")
         
        #batarya degerlabel
        self.data_battery_label = QLabel(self)
        self.data_battery_label.setText("0")
        self.data_battery_label.move(30,480)
        self.data_battery_label.resize(100, 30)
        self.data_battery_label.setStyleSheet("font: 87 15pt \"Arial\";\n"
"color:rgb(0,240,255)")
        self.data_battery_label.setAlignment(Qt.AlignCenter)


        #batarya textlabel
        self.battery_label = QLabel(self)
        self.battery_label.setText("BATARYA:")
        self.battery_label.move(30, 430)
        self.battery_label.resize(145, 40)
        self.battery_label.setStyleSheet("font: 87 12pt \"Arial\";\n"
"color: rgb(0, 240,255);")
        
        #Armdurumu degerlabel
        self.data_arm_label= QLabel(self)
        self.data_arm_label.setText("DİSARMED")
        self.data_arm_label.move(325,485)
        self.data_arm_label.resize(140, 40)
        self.data_arm_label.setStyleSheet("font: 87 16pt \"Arial\";\n"
"color:rgb(255,0,0)")
        self.data_arm_label.setAlignment(Qt.AlignCenter)


        #Armdurumu textlabel
        self.arm_label = QLabel(self)
        self.arm_label.setText("ARM DURUMU:")
        self.arm_label.move(325, 435)
        self.arm_label.resize(145, 40)
        self.arm_label.setStyleSheet("font: 87 12pt \"Arial\";\n"
"color: rgb(255, 0, 0);")

        # Btn olustur
        self.btn = QPushButton('CONNECT', self)
        self.btn.move(670,10)
        self.btn.setStyleSheet("QPushButton{\n"
"background-color: rgb(199, 23, 0);\n"
"font: 75 10pt \"Arial\";\n"
"color: rgb(255, 255, 255);\n"
"border-radius:20px;\n"
"}\n"
"QPushButton:pressed {                \n"
"background-color: rgba(255, 100, 80, 170);\n"
"}\n"
"")
        self.btn.resize(120, 40)
        self.btn.clicked.connect(self.Baglan)
        #combo olustur
        self.combo = QComboBox(self)
        self.combo.addItem('COM10')
        self.combo.addItem('COM8')
        self.combo.addItem('COM7')
        self.combo.addItem('COM3')
        self.combo.addItem('COM14')
        self.combo.move(390, 20)
        self.combo.resize(100, 30)
        self.combo.setStyleSheet("background-color: rgb(120, 120, 120);\n"
"font: 75 10pt \"Arial\";\n"
"border-radius:10px;")
        #combo1 olustur
        self.combo1 = QComboBox(self)
        self.combo1.addItem('9600')
        self.combo1.addItem('57600')
        self.combo1.move(520, 20)
        self.combo1.resize(100, 30)
        self.combo1.setStyleSheet("background-color: rgb(120, 120, 120);\n"
"font: 75 10pt \"Arial\";\n"
"border-radius:10px;")
        
        # Pencereyi ayarla
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("\n"
"background-color: rgb(0,0,0);\n"
"border-radius:20px;\n"
"")
        self.setWindowTitle('KARAYEL FLİGHT DİSPLAY')
        self.show()
        
        
    def Baglan(self):
        
        # Pixhawk ile bağlantıyı kur
         vehicle = connect('COM3', baud=9600, wait_ready=True)
         self.btn.setText("CONNECTED")
         self.btn.setStyleSheet("QPushButton{\n"
"background-color: rgb(0, 255, 0);\n"
"font: 75 10pt \"Arial\";\n"
"color: rgb(255, 255, 255);\n"
"border-radius:20px;\n"
"}\n"
"QPushButton:pressed {                \n"
"background-color: rgba(255, 100, 80, 170);\n"
"}\n"
"")     
        #  while True:
        #   #if self.vehicle.is_armable:
        #      #self.data_arm_label.setText("ARMED")
        #      yaw=vehicle.attitude.yaw
        #      roll=vehicle.attitude.roll
        #      pitch=vehicle.attitude.pitch
        #      horizontal_velocity = vehicle.velocity[0:2]
        #      vertical_velocity = vehicle.velocity[2]
        #      data = vehicle.readline().decode('utf-8').strip().split(',')
        #      # Veri formatı: [mesaj tipi, yükseklik]
        #      if data[0] == 'AHRS3' and len(data) > 10:
        #        height = float(data[10])
        #      battery_value=vehicle.battery.level

        #      self.data_yaw_label.setText(format(yaw))
        #      self.data_roll_label.setText(format(roll))
        #      self.data_pitch_label.setText(format(pitch))
        #      self.data_horizontalSpeed_label.setText(format(horizontal_velocity))
        #      self.data_verticalSpeed_label.setText(format(vertical_velocity))
        #      self.data_altitude_label.setText(format(height))    
        #      self.data_battery_label.setText(format(battery_value))  

         
        
        
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


