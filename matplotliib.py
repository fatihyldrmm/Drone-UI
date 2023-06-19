import matplotlib.pyplot as plt
import numpy as np

# X ve Y verilerini oluşturalım
x = np.array([1, 2, 3, 4, 5])
y = np.array([10, 8, 6, 4, 2])

# Çizgi grafiği oluşturalım
plt.plot(x, y)

# Grafiğin başlığını ve etiketlerini ayarlayalım
plt.title("Örnek Çizgi Grafiği")
plt.xlabel("X Değerleri")
plt.ylabel("Y Değerleri")

# Grafiği ekrana çıkaralım
plt.show()
