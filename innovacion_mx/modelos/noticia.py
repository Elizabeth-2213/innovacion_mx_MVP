from datetime import datetime


class Noticia:
    """
    Contenido informativo publicado por una empresa sobre sus avances en
    reducción de huella de carbono / aprovechamiento de residuos (ODS 9).
    Corresponde a la entidad 'Noticias' del Diagrama de Clases.
    Capa/Componente: Modelos (Dominio)
    """

    CATEGORIAS_VALIDAS = ["Global", "Local"]

    def __init__(self, titulo: str, contenido: str, categoria: str,
                 id_usuario: int, huella_carbono_ahorrada: float = 0.0):
        self.id = None
        self.titulo = titulo
        self.contenido = contenido
        self.fuente = "Innovación MX"
        self.fecha_publicacion = datetime.now()
        self.categoria = categoria
        self.id_usuario = id_usuario          # Empresa que publica
        self.huella_carbono_ahorrada = huella_carbono_ahorrada

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "titulo": self.titulo,
            "contenido": self.contenido,
            "fuente": self.fuente,
            "fecha_publicacion": self.fecha_publicacion.strftime("%Y-%m-%d %H:%M"),
            "anio": self.fecha_publicacion.year,
            "mes": self.fecha_publicacion.month,
            "categoria": self.categoria,
            "id_usuario": self.id_usuario,
            "huella_carbono_ahorrada": self.huella_carbono_ahorrada,
        }

    def __repr__(self) -> str:
        return f"Noticia(id={self.id}, titulo='{self.titulo}')"
