from geopy.distance import geodesic
from datetime import datetime

def heuristica_total(evento, query_embedding, usuario_ciudad, modelo_ciudades, fecha_actual, alpha=0.5, beta=0.25, gamma=0.25):
    sim = evento['similitud']
    ciudad_evento = evento['ciudad']
    try:
        coords_evento = modelo_ciudades[ciudad_evento]
        coords_usuario = modelo_ciudades[usuario_ciudad]
        distancia_km = geodesic(coords_evento, coords_usuario).km
        dist_norm = max(0, 1 - distancia_km / 1000)
    except:
        dist_norm = 0
    try:
        fecha_evento = datetime.strptime(evento['fecha'], '%Y-%m-%d')
        dias = (fecha_evento - fecha_actual).days
        tiempo_norm = max(0, 1 - dias / 365)
    except:
        tiempo_norm = 0
    return alpha * sim + beta * dist_norm + gamma * tiempo_norm

def ajustar_por_feedback(recomendados, feedback):
    for evento in recomendados:
        e_id = evento['id']
        if e_id in feedback:
            if feedback[e_id] == 'like':
                evento['similitud'] += 0.1
            elif feedback[e_id] == 'dislike':
                evento['similitud'] -= 0.2
    return sorted(recomendados, key=lambda x: -x['similitud'])

def filtrar_por_afinidad(eventos, preferencias_usuario):
    """
    Filtra eventos que coincidan con los intereses del usuario.
    """
    tipos_preferidos = preferencias_usuario.get('tipos', [])
    artistas_preferidos = preferencias_usuario.get('artistas', [])

    def relevante(e):
        return (e.get('tipo') in tipos_preferidos or 
                any(artista in artistas_preferidos for artista in e.get('artistas', [])))

    return list(filter(relevante, eventos))

def ordenar_por_cercania(eventos, ubicacion_usuario):
    """
    Ordena eventos según proximidad geográfica al usuario.
    """
    def distancia(e):
        try:
            return geodesic(ubicacion_usuario, e['coordenadas']).kilometers
        except:
            return float('inf')

    return sorted(eventos, key=distancia)

def ordenar_por_fecha(eventos):
    """
    Ordena eventos por fecha próxima.
    """
    def fecha_valida(e):
        try:
            return datetime.strptime(e['fecha'], "%Y-%m-%d")
        except:
            return datetime.max

    return sorted(eventos, key=fecha_valida)