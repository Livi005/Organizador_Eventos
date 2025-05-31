import random
import pandas as pd
from datetime import datetime
import pickle
import os

from embedding import EventEmbedder
from grafo_conocimiento import cargar_grafo, enriquecer_grafo_con_relaciones
from optimizador import heuristica_total

def simular_eventos(output_path="resultados_simulaciones.csv", num_simulaciones=100):
    base_path = os.getcwd()
    embedder = EventEmbedder.load(os.path.join(base_path, "embedding_data"))

    with open(os.path.join(base_path, "eventos_metadata.pkl"), "rb") as f:
        metadata = pickle.load(f)

    grafo = cargar_grafo()
    grafo = enriquecer_grafo_con_relaciones(grafo, metadata)

    consultas = ["concierto", "teatro", "festival", "exposición", "deporte"]
    ciudades = ["Madrid", "Barcelona", "Valencia", "Sevilla", "Bilbao"]
    fecha_actual = datetime.today()

    resultados = []

    for i in range(num_simulaciones):
        consulta = random.choice(consultas)
        ciudad = random.choice(ciudades)
        query_embedding = embedder.embed_query(consulta)
        eventos = embedder.buscar_eventos_similares(query_embedding, k=10)

        for e in eventos:
            e['similitud'] = e['score']
            score_total = heuristica_total(e, query_embedding, ciudad, embedder.modelo_ciudades, fecha_actual)
            resultados.append({
                'simulacion': i + 1,
                'consulta': consulta,
                'ciudad': ciudad,
                'evento': e['titulo'],
                'ciudad_evento': e['ciudad'],
                'fecha_evento': e['fecha'],
                'score_total': round(score_total, 3),
                'similitud': round(e['similitud'], 3)
            })

    df_resultados = pd.DataFrame(resultados)
    df_resultados.to_csv(output_path, index=False)
    print(f"✅ Simulaciones completadas. Resultados guardados en: {output_path}")

if __name__ == "__main__":
    simular_eventos()
