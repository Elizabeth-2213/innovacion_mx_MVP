from datetime import datetime


class Traslado:
    """
    Representa el ciclo de vida logístico del residuo industrial (Traslado),
    implementando la Máquina de Estado documentada en el Segundo Parcial.
    Capa/Componente: Modelos (Dominio)

    Estados soportados (versión operativa para el transportista):
      1. Asignado para Recolección
      2. En Transporte           (se activa al ESCANEAR el código en el origen)
      3. Entregado                (se activa al ESCANEAR el código en el destino)
      4. Residuo Reutilizado      (confirmación final de cierre del ciclo)
      5. Incidencia Detectada / Proceso Cancelado (rutas alternas de error)
    """

    ESTADOS_VALIDOS = [
        "Asignado para Recolección",
        "En Transporte",
        "Incidencia Detectada",
        "Entregado",
        "Residuo Reutilizado",
        "Proceso Cancelado",
    ]

    def __init__(self, id_transaccion: int, codigo_paquete: str, punto_destino: str,
                 id_transportista: int, distancia_km: float, huella_carbono_evitada: float):
        self.id = None
        self.id_transaccion = id_transaccion
        self.codigo_paquete = codigo_paquete # Código que el transportista escanea
        self.distancia_recorrida = distancia_km
        self.huella_carbono_evitada = huella_carbono_evitada
        self.punto_destino = punto_destino
        self.id_transportista = id_transportista
        self.estado = "Asignado para Recolección"
        self.hora_salida = None
        self.hora_llegada = None

    # Transiciones de la máquina de estado

    def escanear_recoleccion(self) -> bool:
        """Evento: el transportista escanea el paquete en el punto de origen."""
        if self.estado != "Asignado para Recolección":
            return False
        self.estado = "En Transporte"
        self.hora_salida = datetime.now()
        return True

    def escanear_entrega(self) -> bool:
        """Evento: el transportista escanea el paquete en el punto de destino."""
        if self.estado != "En Transporte":
            return False
        self.estado = "Entregado"
        self.hora_llegada = datetime.now()
        return True

    def confirmar_reutilizacion(self) -> bool:
        """Evento: la empresa receptora confirma el procesamiento del residuo."""
        if self.estado != "Entregado":
            return False
        self.estado = "Residuo Reutilizado"
        return True

    def reportar_incidencia(self) -> bool:
        if self.estado != "En Transporte":
            return False
        self.estado = "Incidencia Detectada"
        return True

    def resolver_incidencia(self) -> bool:
        if self.estado != "Incidencia Detectada":
            return False
        self.estado = "En Transporte"
        return True

    def cancelar(self) -> bool:
        if self.estado in ("Residuo Reutilizado", "Proceso Cancelado"):
            return False
        self.estado = "Proceso Cancelado"
        return True

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "id_transaccion": self.id_transaccion,
            "codigo_paquete": self.codigo_paquete,
            "distancia_recorrida": self.distancia_recorrida,
            "huella_carbono_evitada": self.huella_carbono_evitada,
            "punto_destino": self.punto_destino,
            "id_transportista": self.id_transportista,
            "estado": self.estado,
            "hora_salida": self.hora_salida.strftime("%Y-%m-%d %H:%M") if self.hora_salida else None,
            "hora_llegada": self.hora_llegada.strftime("%Y-%m-%d %H:%M") if self.hora_llegada else None,
        }

    def __repr__(self) -> str:
        return f"Traslado(id={self.id}, codigo='{self.codigo_paquete}', estado='{self.estado}')"
