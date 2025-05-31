
# sistema_multiagente_mejorado.py

from modules.base import AgenteBase, SimuladorAgentes
from crawler import obtener_eventos
from embedding import EventEmbedder
from grafo_conocimiento import obtener_coordenadas_ciudad
from geopy.distance import geodesic

# Agente que busca eventos nuevos
class AgenteExplorador(AgenteBase):
    def actuar(self):
        eventos_nuevos = obtener_eventos()
        self.comunicar({"tipo": "evento", "eventos": eventos_nuevos})

# Agente que filtra por ubicación
class AgenteGeografico(AgenteBase):
    def __init__(self, nombre, ubicacion_usuario):
        super().__init__(nombre)
        self.ubicacion_usuario = ubicacion_usuario

    def actuar(self):
        coord_usuario = obtener_coordenadas_ciudad(self.ubicacion_usuario)
        for _, mensaje in self.escuchar():
            if mensaje["tipo"] == "evento":
                eventos_filtrados = []
                for evento in mensaje["eventos"]:
                    try:
                        coord_evento = obtener_coordenadas_ciudad(evento["ubicacion"])
                        if geodesic(coord_usuario, coord_evento).km < 100:
                            eventos_filtrados.append(evento)
                    except:
                        continue
                self.comunicar({"tipo": "evento_filtrado", "eventos": eventos_filtrados})

# Agente que recomienda eventos usando embeddings
class AgenteRecomendador(AgenteBase):
    def __init__(self, nombre, perfil_usuario):
        super().__init__(nombre)
        self.embedder = EventEmbedder.load("embedding_data")
        self.perfil = perfil_usuario

    def actuar(self):
        for _, mensaje in self.escuchar():
            if mensaje["tipo"] == "evento_filtrado":
                eventos = mensaje["eventos"]
                textos = [e["descripcion"] for e in eventos]
                indices, _ = self.embedder.buscar_similares(textos, self.perfil, top_k=5)
                recomendaciones = [eventos[i] for i in indices]
                self.comunicar({"tipo": "recomendacion", "recom": recomendaciones})

# Agente que representa al usuario final
class AgenteUsuarioVirtual(AgenteBase):
    def actuar(self):
        for _, mensaje in self.escuchar():
            if mensaje["tipo"] == "recomendacion":
                print("\n🎯 Eventos Recomendados:")
                for ev in mensaje["recom"]:
                    print(f" - {ev['nombre']} ({ev['ubicacion']})")
                print()

# Simulación de todos los agentes
def main():
    sim = SimuladorAgentes()
    sim.registrar(AgenteExplorador("explorador"))
    sim.registrar(AgenteGeografico("geografico", ubicacion_usuario="Madrid"))
    sim.registrar(AgenteRecomendador("recomendador", perfil_usuario="música rock en vivo"))
    sim.registrar(AgenteUsuarioVirtual("usuario"))
    sim.ejecutar()

if __name__ == "__main__":
    main()
