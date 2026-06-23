from datetime import datetime


class Transaccion:
    """
    Registro legal y comercial del intercambio de material entre dos empresas.
    Corresponde a la entidad 'Transacción' del Diagrama de Clases.
    Capa/Componente: Modelos (Dominio)
    """

    def __init__(self, id_material: int, cantidad_material: float,
                 id_usuario_proveedor: int, id_usuario_receptor: int):
        self.id = None
        self.id_material = id_material
        self.fecha = datetime.now()
        self.cantidad_material = cantidad_material
        self.id_usuario_proveedor = id_usuario_proveedor
        self.id_usuario_receptor = id_usuario_receptor
        self.id_traslado = None   # Se activa 1:1 al generar el traslado

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "id_material": self.id_material,
            "fecha": self.fecha.strftime("%Y-%m-%d %H:%M"),
            "cantidad_material": self.cantidad_material,
            "id_usuario_proveedor": self.id_usuario_proveedor,
            "id_usuario_receptor": self.id_usuario_receptor,
            "id_traslado": self.id_traslado,
        }

    def __repr__(self) -> str:
        return f"Transaccion(id={self.id}, material={self.id_material})"
