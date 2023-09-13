Para la ejecuccion de este prorgama, debe tener instalado la ultima version de Python y tener instalado el paquete Numpy para hacer funcionar el programa

Para ejecutar necesita abrir una terminal donde se localizan los archivos y utilizar lo siguiente:
python agnreinas semilla.py [semilla] [tamaño_tablero] [tamaño_población] [probabilidad_cruza] [probabilidad_mutación] [número_iteraciones]
Donde:
- [semilla]: Valor de semilla para la aleatoriedad
- [tamaño_tablero]: Tamaño del tablero
- [tamaño_población]: Tamaño de la poblacion de cromosomas (posiciones de reinas en un tablero del tamaño introducido en [tamaño_tablero])
- [probabilidad_cruza]: Probabilidad de cruza entre dos cromosomas, debe ser un numero decimal entre 0 y 1
- [probabilidad_mutación]: Probabilidad de mutacion de un hijo, debe ser un numero decimal entre 0 y 1
- [número_iteraciones]: Limite de Generaciones

Para verificar su funcionamiento, pruebe estos casos de uso en donde dan una solución factible:
Solucion de 15 reinas (Tablero 15x15): python agnreinas.py 4 15 50 0.9 0.08 100
Solucion de 20 reinas (Tablero 20x20): python agnreinas.py 4 20 60 0.9 0.05 250
Solucion de 30 reinas (Tablero 30x30):  python agnreinas.py 54 30 80 0.9 0.05 300
Solucion de 50 reinas (Tablero 50x50): python agnreinas.py 42413 50 120 0.95 0.08 600