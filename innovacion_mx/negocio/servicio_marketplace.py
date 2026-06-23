#SERVICIO DE MARKETPLACE DE RESIDUOS
# Archivo: negocio/servicio_marketplace.py
# Capa: Negocio — Reglas de negocio de los módulos "Gestión Residuo" y
# "Publicaciones y Noticias Feed" (parte de materiales)

import random
import string
from typing import Optional

from modelos.material import Material
from modelos.publicacion import Publicacion
from modelos.transaccion import Transaccion
from modelos.traslado import Traslado


class ServicioMarketplace:
    """
    Implementa el ciclo: una empresa registra y publica un material residual
    -> otra empresa lo compra -> se genera una Transacción y, en automático,
    un Traslado (en espera de que un transportista tome la ruta).
    Capa/Componente: Negocio
    """

    TOXICIDAD_PROHIBIDA = "alta"   # Regla de negocio: evita residuos tóxicos ilegales

    def __init__(self, repositorio):
        self.repositorio = repositorio

    # CASO DE USO 1: Empresa registra y publica un material residual

    def publicar_material(self, datos: dict, id_usuario_empresa: int) -> dict:
        campos_requeridos = ["nombre", "categoria", "estado_fisico", "toxicidad",
                              "cantidad_disponible", "unidad_medida", "tipo_transporte_requerido", "precio"]
        for campo in campos_requeridos:
            if datos.get(campo) in (None, ""):
                return {"exito": False, "mensaje": f'El campo "{campo}" es obligatorio.', "datos": None}

        if str(datos["toxicidad"]).lower() == self.TOXICIDAD_PROHIBIDA:
            return {
                "exito": False,
                "mensaje": "No se permite publicar residuos de toxicidad ALTA (Taxonomía y Filtrado de Materiales).",
                "datos": None,
            }

        try:
            cantidad = float(datos["cantidad_disponible"])
            precio = float(datos["precio"])
        except (ValueError, TypeError):
            return {"exito": False, "mensaje": "Cantidad y precio deben ser números válidos.", "datos": None}

        material = Material(
            nombre=datos["nombre"],
            categoria=datos["categoria"],
            estado_fisico=datos["estado_fisico"],
            toxicidad=datos["toxicidad"],
            cantidad_disponible=cantidad,
            unidad_medida=datos["unidad_medida"],
            tipo_transporte_requerido=datos["tipo_transporte_requerido"],
            id_usuario_propietario=id_usuario_empresa,
        )

        if not material.es_valido():
            return {"exito": False, "mensaje": "Los datos del material no son válidos.", "datos": None}

        id_material = self.repositorio.guardar_material(material)

        publicacion = Publicacion(precio=precio, id_material=id_material, id_usuario=id_usuario_empresa)
        id_publicacion = self.repositorio.guardar_publicacion(publicacion)

        return {
            "exito": True,
            "mensaje": f"Material '{material.nombre}' registrado y publicado (Publicación ID {id_publicacion}).",
            "datos": {"material": material.to_dict(), "publicacion": publicacion.to_dict()},
        }

    #CASO DE USO 2: Listar publicaciones disponibles en el marketplace

    def listar_marketplace(self, excluir_id_usuario: Optional[int] = None) -> dict:
        publicaciones = self.repositorio.listar_publicaciones_disponibles()
        resultado = []
        for pub in publicaciones:
            if excluir_id_usuario is not None and pub.id_usuario == excluir_id_usuario:
                continue
            material = self.repositorio.buscar_material_por_id(pub.id_material)
            vendedor = self.repositorio.buscar_usuario_por_id(pub.id_usuario)
            if material is None or vendedor is None:
                continue
            resultado.append({
                "publicacion": pub.to_dict(),
                "material": material.to_dict(),
                "vendedor": vendedor.nombre,
            })
        return {"exito": True, "mensaje": f"{len(resultado)} publicación(es) disponible(s).", "datos": resultado}

    #CASO DE USO 3: Empresa compra un material -> Transacción + Traslado 

    def comprar_material(self, id_publicacion: int, cantidad: float, id_usuario_comprador: int,
                          punto_destino: str) -> dict:
        publicacion = self.repositorio.buscar_publicacion_por_id(id_publicacion)
        if publicacion is None or publicacion.estatus != "Disponible":
            return {"exito": False, "mensaje": "La publicación no existe o ya no está disponible.", "datos": None}

        if publicacion.id_usuario == id_usuario_comprador:
            return {"exito": False, "mensaje": "No puedes comprar tu propio material.", "datos": None}

        material = self.repositorio.buscar_material_por_id(publicacion.id_material)
        if material is None:
            return {"exito": False, "mensaje": "El material asociado ya no existe.", "datos": None}

        try:
            cantidad = float(cantidad)
        except (ValueError, TypeError):
            return {"exito": False, "mensaje": "La cantidad debe ser un número válido.", "datos": None}

        if not material.reducir_cantidad(cantidad):
            return {"exito": False, "mensaje": f"Cantidad inválida. Disponible: {material.cantidad_disponible}.", "datos": None}

        # 1. Registrar transacción
        transaccion = Transaccion(
            id_material=material.id,
            cantidad_material=cantidad,
            id_usuario_proveedor=publicacion.id_usuario,
            id_usuario_receptor=id_usuario_comprador,
        )
        id_transaccion = self.repositorio.guardar_transaccion(transaccion)

        if material.cantidad_disponible == 0:
            publicacion.marcar_vendida()

        # 2. Activar traslado automáticamente (1:1 con la transacción)
        codigo_paquete = self._generar_codigo_paquete()
        huella_estimada = round(cantidad * 0.42, 2)   # kg CO2 evitados (estimación simple)
        distancia_estimada = round(random.uniform(15, 180), 1)

        traslado = Traslado(
            id_transaccion=id_transaccion,
            codigo_paquete=codigo_paquete,
            punto_destino=punto_destino,
            id_transportista=0,   # Aún no asignado: se usa 0 como indicador de no asignado
            distancia_km=distancia_estimada,
            huella_carbono_evitada=huella_estimada,
        )
        id_traslado = self.repositorio.guardar_traslado(traslado)
        transaccion.id_traslado = id_traslado

        # Acumular huella de carbono evitada de la empresa receptora
        receptor = self.repositorio.buscar_usuario_por_id(id_usuario_comprador)
        if receptor:
            receptor.huella_carbono_evitada_total += huella_estimada

        return {
            "exito": True,
            "mensaje": (f"Compra registrada. Transacción ID {id_transaccion}. "
                        f"Código de paquete para el transportista: {codigo_paquete}."),
            "datos": {
                "transaccion": transaccion.to_dict(),
                "traslado": traslado.to_dict(),
            },
        }

    def listar_mis_materiales(self, id_usuario: int) -> dict:
        materiales = self.repositorio.listar_materiales_por_propietario(id_usuario)
        return {"exito": True, "mensaje": f"{len(materiales)} material(es) registrado(s).",
                "datos": [m.to_dict() for m in materiales]}

    def listar_mis_transacciones(self, id_usuario: int) -> dict:
        transacciones = self.repositorio.listar_transacciones_por_usuario(id_usuario)
        resultado = []
        for t in transacciones:
            traslado = self.repositorio.buscar_traslado_por_id(t.id_traslado) if t.id_traslado else None
            resultado.append({"transaccion": t.to_dict(), "traslado": traslado.to_dict() if traslado else None})
        return {"exito": True, "mensaje": f"{len(resultado)} transacción(es) encontrada(s).", "datos": resultado}

    @staticmethod
    def _generar_codigo_paquete() -> str:
        sufijo = "".join(random.choices(string.ascii_uppercase + string.digits, k=6))
        return f"IMX-{sufijo}"
