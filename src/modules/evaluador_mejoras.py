
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
import numpy as np

def evaluar_recomendaciones(eventos, eventos_originales, feedback_dict, modelo=None):
    """
    Evalúa la calidad de las recomendaciones antes y después de aplicar filtros.
    """
    if modelo is None:
        modelo = SentenceTransformer("paraphrase-MiniLM-L6-v2")

    def calcular_similitud(e1, e2):
        emb1 = modelo.encode(e1['descripcion'], convert_to_tensor=True)
        emb2 = modelo.encode(e2['descripcion'], convert_to_tensor=True)
        return float(cosine_similarity([emb1], [emb2])[0][0])

    mejoras = []
    for i, evento in enumerate(eventos):
        id_evt = evento['id']
        if feedback_dict.get(id_evt) == 'like':
            similares = [
                calcular_similitud(evento, e_orig)
                for e_orig in eventos_originales if e_orig['id'] != id_evt
            ]
            mejora = max(similares, default=0)
            mejoras.append(mejora)

    if mejoras:
        score_promedio = round(np.mean(mejoras), 3)
    else:
        score_promedio = 0.0

    return {
        "eventos_totales": len(eventos),
        "feedback_positivos": sum(1 for v in feedback_dict.values() if v == "like"),
        "score_promedio_similitud": score_promedio
    }
