import networkx as nx
import pickle

def cargar_grafo(path='grafo_eventos.graphml'):
    return nx.read_graphml(path)

def guardar_grafo(grafo, path='grafo_eventos_actualizado.graphml'):
    nx.write_graphml(grafo, path)

def enriquecer_grafo_con_relaciones(grafo, metadata):
    for id_a, data_a in metadata.items():
        for id_b, data_b in metadata.items():
            if id_a == id_b:
                continue
            if data_a['artista'] == data_b['artista'] or data_a['genero'] == data_b['genero']:
                grafo.add_edge(id_a, id_b, tipo='relacion_temporal', peso=1.0)
            elif data_a['ciudad'] == data_b['ciudad']:
                grafo.add_edge(id_a, id_b, tipo='proximidad_geografica', peso=0.5)
    return grafo

def calcular_pagerank_personalizado(grafo):
    return nx.pagerank(grafo, weight='peso')