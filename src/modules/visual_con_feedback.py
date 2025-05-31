import streamlit as st
from registro_feedback import registrar_feedback, cargar_logs_feedback
from datetime import datetime
from embedding import EventEmbedder
from grafo_conocimiento import cargar_grafo, enriquecer_grafo_con_relaciones, calcular_pagerank_personalizado
from optimizador import heuristica_total, ajustar_por_feedback
import pickle

@st.cache_data
def cargar_modelos():
    embedder = EventEmbedder.load("embedding_data")
    with open("eventos_metadata.pkl", "rb") as f:
        metadata = pickle.load(f)
    grafo = cargar_grafo()
    grafo = enriquecer_grafo_con_relaciones(grafo, metadata)
    return embedder, grafo, metadata

st.title("🎫 Recomendador de Eventos Avanzado")

embedder, grafo, metadata = cargar_modelos()

query = st.text_input("¿Qué tipo de evento te interesa?")
ciudad_usuario = st.text_input("¿En qué ciudad estás?", value="Madrid")
fecha_actual = datetime.today()

if query and ciudad_usuario:
    query_embedding = embedder.embed_query(query)
    eventos = embedder.buscar_eventos_similares(query_embedding, k=10)
    for e in eventos:
        e['similitud'] = e['score']
        score_total = heuristica_total(e, query_embedding, ciudad_usuario, embedder.modelo_ciudades, fecha_actual)
        e['score_total'] = round(score_total, 3)
    eventos_ordenados = sorted(eventos, key=lambda x: -x['score_total'])
    st.subheader("🎯 Eventos recomendados:")
    for e in eventos_ordenados:
        st.markdown(f"**{e['titulo']}** ({e['ciudad']}, {e['fecha']}) - Score: {e['score_total']}")