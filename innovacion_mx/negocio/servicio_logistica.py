# SERVICIO DE LOGÍSTICA 
# Archivo: negocio/servicio_logistica.py
# Capa: Negocio — Reglas de negocio del módulo "Cálculo Logístico"
# Implementa la Máquina de Estado del Residuo Industrial para el actor
# Personal de Transporte: tomar ruta, escanear recolección y escanear entrega.


class ServicioLogistica:
    """
    Capa/Componente: Negocio
    """

    def __init__(self, repositorio):
        self.repositorio = repositorio

    def listar_paquetes_disponibles(self) -> dict:
        """Paquetes 'Asignado para Recolección' que ningún transportista ha tomado aún."""
        disponibles = [t for t in self.repositorio._traslados.values()
                       if t.id_transportista is None and t.estado == "Asignado para Recolección"]
        return {"exito": True, "mensaje": f"{len(disponibles)} paquete(s) sin asignar.",
                "datos": [t.to_dict() for t in disponibles]}

    def tomar_ruta(self, id_traslado: int, id_transportista: int) -> dict:
        traslado = self.repositorio.buscar_traslado_por_id(id_traslado)
        if traslado is None:
            return {"exito": False, "mensaje": "No existe un traslado con ese ID.", "datos": None}
        if traslado.id_transportista is not None:
            return {"exito": False, "mensaje": "Esta ruta ya fue tomada por otro transportista.", "datos": None}
        traslado.id_transportista = id_transportista
        return {"exito": True, "mensaje": f"Ruta {id_traslado} asignada. Código a recolectar: {traslado.codigo_paquete}.",
                "datos": traslado.to_dict()}

    def listar_mis_rutas(self, id_transportista: int) -> dict:
        rutas = self.repositorio.listar_traslados_por_transportista(id_transportista)
        return {"exito": True, "mensaje": f"{len(rutas)} ruta(s) asignada(s).",
                "datos": [t.to_dict() for t in rutas]}

    def escanear_recoleccion(self, codigo_paquete: str, id_transportista: int) -> dict:
        traslado = self.repositorio.buscar_traslado_por_codigo(codigo_paquete)
        if traslado is None:
            return {"exito": False, "mensaje": "Código de paquete no encontrado.", "datos": None}
        if traslado.id_transportista != id_transportista:
            return {"exito": False, "mensaje": "Este paquete no está asignado a tu ruta.", "datos": None}
        if not traslado.escanear_recoleccion():
            return {"exito": False, "mensaje": f"No se puede recolectar. Estado actual: {traslado.estado}.", "datos": None}
        return {"exito": True, "mensaje": f"Paquete {codigo_paquete} recolectado. Estado: En Transporte.",
                "datos": traslado.to_dict()}

    def escanear_entrega(self, codigo_paquete: str, id_transportista: int) -> dict:
        traslado = self.repositorio.buscar_traslado_por_codigo(codigo_paquete)
        if traslado is None:
            return {"exito": False, "mensaje": "Código de paquete no encontrado.", "datos": None}
        if traslado.id_transportista != id_transportista:
            return {"exito": False, "mensaje": "Este paquete no está asignado a tu ruta.", "datos": None}
        if not traslado.escanear_entrega():
            return {"exito": False, "mensaje": f"No se puede entregar. Estado actual: {traslado.estado}.", "datos": None}
        return {"exito": True, "mensaje": f"Paquete {codigo_paquete} entregado en destino.",
                "datos": traslado.to_dict()}

    def reportar_incidencia(self, codigo_paquete: str, id_transportista: int) -> dict:
        traslado = self.repositorio.buscar_traslado_por_codigo(codigo_paquete)
        if traslado is None or traslado.id_transportista != id_transportista:
            return {"exito": False, "mensaje": "Paquete no encontrado o no asignado a ti.", "datos": None}
        if not traslado.reportar_incidencia():
            return {"exito": False, "mensaje": f"No se puede reportar incidencia. Estado actual: {traslado.estado}.", "datos": None}
        return {"exito": True, "mensaje": "Incidencia registrada en la ruta.", "datos": traslado.to_dict()}

    def confirmar_reutilizacion(self, id_traslado: int, id_usuario_receptor: int) -> dict:
        """La empresa receptora confirma el procesamiento/reutilización del residuo."""
        traslado = self.repositorio.buscar_traslado_por_id(id_traslado)
        if traslado is None:
            return {"exito": False, "mensaje": "No existe un traslado con ese ID.", "datos": None}
        transaccion = self.repositorio.buscar_transaccion_por_id(traslado.id_transaccion)
        if transaccion is None or transaccion.id_usuario_receptor != id_usuario_receptor:
            return {"exito": False, "mensaje": "No tienes permiso sobre esta transacción.", "datos": None}
        if not traslado.confirmar_reutilizacion():
            return {"exito": False, "mensaje": f"No se puede confirmar. Estado actual: {traslado.estado}.", "datos": None}
        return {"exito": True, "mensaje": "Residuo confirmado como reutilizado. Ciclo de vida finalizado.",
                "datos": traslado.to_dict()}
