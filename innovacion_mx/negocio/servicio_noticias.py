# SERVICIO DE NOTICIAS 
# Archivo: negocio/servicio_noticias.py
# Capa: Negocio — Reglas de negocio del módulo "Publicaciones y Noticias Feed"

from modelos.noticia import Noticia
from typing import Optional


class ServicioNoticias:
    """
    Capa/Componente: Negocio
    """

    def __init__(self, repositorio):
        self.repositorio = repositorio

    # Empresa publica una noticia sobre sus logros (huella de carbono, etc.)

    def publicar_noticia(self, datos: dict, id_usuario_empresa: int) -> dict:
        for campo in ["titulo", "contenido", "categoria"]:
            if not datos.get(campo):
                return {"exito": False, "mensaje": f'El campo "{campo}" es obligatorio.', "datos": None}

        if datos["categoria"] not in Noticia.CATEGORIAS_VALIDAS:
            return {"exito": False,
                    "mensaje": f"Categoría no válida. Opciones: {', '.join(Noticia.CATEGORIAS_VALIDAS)}.",
                    "datos": None}

        huella = float(datos.get("huella_carbono_ahorrada", 0) or 0)

        noticia = Noticia(
            titulo=datos["titulo"],
            contenido=datos["contenido"],
            categoria=datos["categoria"],
            id_usuario=id_usuario_empresa,
            huella_carbono_ahorrada=huella,
        )
        id_noticia = self.repositorio.guardar_noticia(noticia)
        return {"exito": True, "mensaje": f"Noticia publicada con ID {id_noticia}.", "datos": noticia.to_dict()}

    # Ciudadano consulta el feed completo ordenado por fecha (más reciente primero)

    def consultar_feed(self) -> dict:
        noticias = self.repositorio.listar_noticias()
        noticias_ordenadas = sorted(noticias, key=lambda n: n.fecha_publicacion, reverse=True)
        resultado = []
        for n in noticias_ordenadas:
            empresa = self.repositorio.buscar_usuario_por_id(n.id_usuario)
            dato = n.to_dict()
            dato["empresa"] = empresa.nombre if empresa else "Empresa desconocida"
            resultado.append(dato)
        return {"exito": True, "mensaje": f"{len(resultado)} noticia(s) publicada(s).", "datos": resultado}

    # Ciudadano filtra el feed por año y/o mes (ambos opcionales)

    def filtrar_feed(self, anio: Optional[int] = None, mes: Optional[int] = None) -> dict:
        feed = self.consultar_feed()["datos"]
        filtrado = feed
        if anio is not None:
            filtrado = [n for n in filtrado if n["anio"] == anio]
        if mes is not None:
            filtrado = [n for n in filtrado if n["mes"] == mes]
        return {"exito": True, "mensaje": f"{len(filtrado)} noticia(s) coinciden con el filtro.", "datos": filtrado}
