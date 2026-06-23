from datetime import datetime


class Publicacion:
    """
    Representa la oferta de un material disponible en la PWA.
    Corresponde a la entidad 'Publicación' del Diagrama de Clases.
    Capa/Componente: Modelos (Dominio)
    """

    ESTATUS_VALIDOS = ["Disponible", "Vendido", "Cancelada"]

    def __init__(self, precio: float, id_material: int, id_usuario: int):
        self.id = None
        self.fecha = datetime.now()
        self.precio = precio
        self.estatus = "Disponible"
        self.id_material = id_material
        self.id_usuario = id_usuario   # Empresa que publica (vendedora)

    def marcar_vendida(self):
        self.estatus = "Vendido"

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "fecha": self.fecha.strftime("%Y-%m-%d %H:%M"),
            "precio": self.precio,
            "estatus": self.estatus,
            "id_material": self.id_material,
            "id_usuario": self.id_usuario,
        }

    def __repr__(self) -> str:
        return f"Publicacion(id={self.id}, material={self.id_material}, estatus='{self.estatus}')"
