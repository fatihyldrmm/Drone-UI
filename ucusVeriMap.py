from encodings import search_function
import mysql.connector
import folium # pip install folium
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout
from PyQt5 import QtWebEngineWidgets
from folium.plugins import Draw ,MousePosition
import folium, io, sys, json
from folium import plugins
from dronekit import Command, connect, VehicleMode, LocationGlobalRelative
# connection_string="COM4"
# baud_rate=9600
# # Pixhawk ile bağlantıyı kur
# vehicle = connect(connection_string, baud=9600, wait_ready=True)

class UcusVeriMap(QWidget):
    def __init__(self):
        super().__init__()
        

        self.window_width, self.window_height = 800, 800
        self.setMinimumSize(self.window_width, self.window_height)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        # while True:
        #     mapObj = folium.Map(location=[vehicle.location.global_frame.lat,vehicle.location.global_frame.lon],
        #              zoom_start=16, tiles=None)
        #     folium.Marker(location=[vehicle.location.global_frame.lat,vehicle.location.global_frame.lon], tooltip='New York City').add_to(mapObj)
        #     break

################-----silindi-----#################        
        # # Veritabanı bağlantısı
        # conn = mysql.connector.connect(
        #         host = "localhost",
        #         user="root",
        #         password="gulcann",
        #         database="karayel" )
        
        mapObj = folium.Map(location=[40.77876116603416, 30.366209016770387],
                      zoom_start=16, tiles=None)
        
        # çizim yapmak için kullanıyoruz
        # draw = Draw(
        #     export=True,
        #     filename="my_data.geojson",
        #     position="topleft",
        #     draw_options={"polyline": {"allowIntersection": True}}, #kesişim olmamasını istiyorsak false yaparız
        #     edit_options={"poly": {"allowIntersection": True}},
        # )
        # draw.add_to(mapObj)
        
        
        formatter = "function(num) {return L.Util.formatNum(num, ) + ' º ';};"

        MousePosition(
            position="topright",
            separator=" | ",
            empty_string="NaN",
            lng_first=True,
            num_digits=20,
            prefix="Coordinates:",
            lat_formatter=formatter,
            lng_formatter=formatter,
        ).add_to(mapObj)

        

      
        # minimap = plugins.MiniMap()
        # mapObj.add_child(minimap)
        
#################-----silindi-----#########################
        # # add tile layers
        folium.TileLayer('openstreetmap').add_to(mapObj)
        # folium.TileLayer('stamenterrain', attr="stamenterrain").add_to(mapObj)
        # folium.TileLayer('stamenwatercolor', attr="stamenwatercolor").add_to(mapObj)
        # folium.TileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', name='CartoDB.DarkMatter', attr="CartoDB.DarkMatter").add_to(mapObj)

        
        # # add layers control over the map
        # folium.LayerControl().add_to(mapObj)

        data = io.BytesIO()
        mapObj.save(data, close_file=False)
        
        mp = MousePosition()
        mp.add_to(mapObj)

        # bu kısım sadece konum verilerini ekrana göstermek için kullanılıyor
        class WebEnginePage(QtWebEngineWidgets.QWebEnginePage):
            def javaScriptConsoleMessage(self, level, message, lineNumber, sourceID):
                coords_dict = json.loads(message)
                coords = coords_dict['geometry']['coordinates'][0]
                print(coords)

        view = QtWebEngineWidgets.QWebEngineView()
        page = WebEnginePage(view)
        view.setPage(page)
        view.setHtml(data.getvalue().decode())
        # view widget'ını layout'a ekleyelim
        layout.addWidget(view)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet('''
        QWidget {
            font-size: 35px;
        }
    ''')
    map = UcusVeriMap()
    map.show()
    sys.exit(app.exec_())