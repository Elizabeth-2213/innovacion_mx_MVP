class Material:
    """
    Representa el insumo objeto del intercambio entre empresas.
    Corresponde a la entidad 'Material' del Diagrama de Clases.
    Capa/Componente: Modelos (Dominio)
    """

    CATEGORIAS_VALIDAS = ["Metal", "Plástico", "Papel/Cartón", "Madera", "Químico", "Textil", "Otro"]

    def __init__(self, nombre: str, categoria: str, estado_fisico: str, toxicidad: str,
                 cantidad_disponible: float, unidad_medida: str, tipo_transporte_requerido: str,
                 id_usuario_propietario: int):
        self.id = None
        self.nombre = nombre
        self.categoria = categoria
        self.estado_fisico = estado_fisico
        self.toxicidad = toxicidad                       # Baja / Media / Alta
        self.cantidad_disponible = cantidad_disponible
        self.unidad_medida = unidad_medida
        self.tipo_transporte_requerido = tipo_transporte_requerido
        self.id_usuario_propietario = id_usuario_propietario  # Empresa que lo registró
        self.activo = True

    def es_valido(self) -> bool:
        return (
            bool(self.nombre) and
            bool(self.categoria) and
            self.cantidad_disponible > 0 and
            self.toxicidad.lower() != "alta"   # Regla de negocio: se filtran residuos de alta toxicidad
        )

    def reducir_cantidad(self, cantidad: float) -> bool:
        if cantidad <= 0 or cantidad > self.cantidad_disponible:
            return False
        self.cantidad_disponible -= cantidad
        return True

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "nombre": self.nombre,
            "categoria": self.categoria,
            "estado_fisico": self.estado_fisico,
            "toxicidad": self.toxicidad,
            "cantidad_disponible": self.cantidad_disponible,
            "unidad_medida": self.unidad_medida,
            "tipo_transporte_requerido": self.tipo_transporte_requerido,
            "id_usuario_propietario": self.id_usuario_propietario,
        }

    def __repr__(self) -> str:
        return f"Material(id={self.id}, nombre='{self.nombre}', disponible={self.cantidad_disponible})"
