import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

try:


    # Cargar los datos
    historial_compras = pd.read_csv('data/historial_compras.csv')
    productos = pd.read_csv('data/productos.csv')

    # Crear una matriz de usuario-producto
    matriz_utilidad = pd.pivot_table(historial_compras, index='cliente_id', columns='producto_id', aggfunc=len, fill_value=0)

    # Convertir la matriz de utilidad en una matriz de usuarios x productos
    matriz_utilidad_np = matriz_utilidad.values

    # Calcular la similitud entre productos
    similitudes = cosine_similarity(matriz_utilidad_np.T)

    # Crear un DataFrame de similitudes
    df_similitudes = pd.DataFrame(similitudes, index=matriz_utilidad.columns, columns=matriz_utilidad.columns)

except:
    pass

def recomendar_productos(cliente_id, top_n=5):
    try:
        productos_comprados = matriz_utilidad.loc[cliente_id]
        productos_no_comprados = productos_comprados[productos_comprados == 0].index

        puntuaciones = np.zeros(len(productos_no_comprados))
        
        for i, producto_id in enumerate(productos_no_comprados):
            similaridades = df_similitudes[producto_id]
            puntuacion = (productos_comprados[productos_comprados > 0] @ similaridades[productos_comprados > 0])
            puntuaciones[i] = puntuacion

        recomendaciones = pd.Series(puntuaciones, index=productos_no_comprados)
        recomendaciones = recomendaciones.sort_values(ascending=False)
        return recomendaciones.head(top_n)


    except Exception as ex:
        print("\nsin recomendaciones (っ˘̩╭╮˘̩)っ")
        return None


# Ejemplo de uso
#cliente_id = 1
#print("Recomendaciones para el cliente ID", cliente_id)
#print(recomendar_productos(cliente_id))


