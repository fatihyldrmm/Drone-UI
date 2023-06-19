from encodings import search_function
import pymysql as sql
import folium # pip install folium
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout
from PyQt5 import QtWebEngineWidgets
from folium.plugins import Draw ,MousePosition
import folium, io, sys, json
from folium import plugins

class Map(QWidget):
    def __init__(self):
        super().__init__()
        

        self.window_width, self.window_height = 500, 500
        self.setMinimumSize(self.window_width, self.window_height)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)
        
        
        # Veritabanı bağlantısı
        conn = sql.connect(
                host = "localhost",
                user="root",
                password="root",
                database="karayel" )
        im = conn.cursor()
        
        mapObj = folium.Map(location=[40.77876116603416, 30.366209016770387],
                     zoom_start=16, tiles=None)
        
        # çizim yapmak için kullanıyoruz
        draw = Draw(
            export=True,
            filename="my_data.geojson",
            position="topleft",
            draw_options={"polyline": {"allowIntersection": True}}, #kesişim olmamasını istiyorsak false yaparız
            edit_options={"poly": {"allowIntersection": True}},
        )
        draw.add_to(mapObj)
        
        
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

        

      
        minimap = plugins.MiniMap()
        mapObj.add_child(minimap)
        

        # add tile layers
        folium.TileLayer('openstreetmap').add_to(mapObj)
        folium.TileLayer('stamenterrain', attr="stamenterrain").add_to(mapObj)
        folium.TileLayer('stamenwatercolor', attr="stamenwatercolor").add_to(mapObj)
        folium.TileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', name='CartoDB.DarkMatter', attr="CartoDB.DarkMatter").add_to(mapObj)

        
        # add layers control over the map
        folium.LayerControl().add_to(mapObj)

        data = io.BytesIO()
        mapObj.save(data, close_file=False)
        
        mp = MousePosition()
        mp.add_to(mapObj)

        # bu kısım sadece konum verilerini ekrana göstermek için kullanılıyor
        class WebEnginePage(QtWebEngineWidgets.QWebEnginePage):
            def javaScriptConsoleMessage(self, level, message, lineNumber, sourceID):
                    sil = "TRUNCATE TABLE koordinat"
                    im.execute(sil)
                    conn.commit()
                    coords_dict = json.loads(message)
                    print(*coords_dict['geometry']['coordinates'])
                    coords = coords_dict['geometry']['coordinates']
                    for pos in coords:
                        ekle = "INSERT INTO koordinat (KoordinatID,X,Y) VALUES (NULL,'{}','{}')" 
                        data1=(pos[0],pos[1])
                        ekle = ekle.format(*data1)
                        im.execute(ekle)
                        conn.commit()

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
    map = Map()
    map.show()
    sys.exit(app.exec_())