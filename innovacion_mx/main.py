# PROYECTO: Innovación MX — Gestión e Intercambio de Residuos Industriales
# ODS: 9 — Industria, Innovación e Infraestructura
# Materia: Modelado de Sistemas — Semestre Feb-Jun 2026
# Arquitectura: Layered (Por Capas) — Modelos / Datos / Negocio / Presentación
# Patrones de diseño aplicados: Repository Pattern + Singleton
# Versión: MVP 1.0 — Funcionalidades básicas implementadas para demostración.
# Descripción general:
# Innovación MX es una plataforma que conecta empresas generadoras de residuos industriales
# con empresas recicladoras, transportistas y ciudadanos interesados en el impacto ambiental.
# Permite publicar materiales residuales disponibles para venta, gestionar transacciones e intercambios, y compartir noticias sobre logros ambientales.
# El sistema se compone de las siguientes capas:
# - Modelos: Define las entidades del dominio (Material, Publicación, Noticia, Usuario, Transacción, Traslado).
# - Datos: Implementa un repositorio de datos en memoria para almacenar y gestionar las entidades.
# - Negocio: Contiene la lógica de negocio para autenticación, gestión de marketplace, noticias y logística.
# - Presentación: Proporciona una interfaz de línea de comandos (CLI) para interactuar con el sistema.
# 
# ESCENARIO DE DEMOSTRACIÓN DEL MVP
# 1. Una Empresa publica un material residual disponible para venta.
# 2. Otra Empresa lo compra → se genera una Transacción y un Traslado.
# 3. Un Transportista toma la ruta y escanea recolección y entrega.
# 4. La Empresa receptora confirma la reutilización del residuo.
# 5. Una Empresa publica una noticia sobre su huella de carbono ahorrada.
# 6. Un Ciudadano consulta y filtra el tablero de noticias por año/mes.
#
# Cuentas precargadas para probar rápido (todas con contraseña "1234"):
#   - empresa1@innovacionmx.com   (Empresa — Recicladora del Bajío)
#   - empresa2@innovacionmx.com   (Empresa — Acero Industrial León)
#   - transportista1@innovacionmx.com (Transportista — Juan Pérez)
#   - ciudadano1@innovacionmx.com (Ciudadano — Ana Torres)

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from datos.repositorio_datos import RepositorioDatos
from negocio.servicio_autenticacion import ServicioAutenticacion
from negocio.servicio_marketplace import ServicioMarketplace
from negocio.servicio_noticias import ServicioNoticias
from negocio.servicio_logistica import ServicioLogistica
from presentacion.interfaz_cli import InterfazCLI


def cargar_datos_demo(auth: ServicioAutenticacion, marketplace: ServicioMarketplace,
                       noticias: ServicioNoticias, logistica: ServicioLogistica):
    print("\n  Cargando datos de demostración...")

    auth.registrar_usuario({
        "correo": "empresa1@innovacionmx.com", "contrasena": "1234",
        "tipo_usuario": "Empresa", "nombre": "Recicladora del Bajío",
        "rfc": "RDB900101AB1", "certificacion_ambiental": "ISO 14001",
    })
    auth.registrar_usuario({
        "correo": "empresa2@innovacionmx.com", "contrasena": "1234",
        "tipo_usuario": "Empresa", "nombre": "Acero Industrial León",
        "rfc": "AIL850202CD2", "certificacion_ambiental": "ISO 14001",
    })
    auth.registrar_usuario({
        "correo": "transportista1@innovacionmx.com", "contrasena": "1234",
        "tipo_usuario": "Transportista", "nombre": "Juan Pérez",
        "licencia_sct": "SCT-LEO-2026-0091",
    })
    auth.registrar_usuario({
        "correo": "ciudadano1@innovacionmx.com", "contrasena": "1234",
        "tipo_usuario": "Ciudadano", "nombre": "Ana Torres",
    })

    # Recicladora del Bajío (id 1) publica un material
    marketplace.publicar_material({
        "nombre": "Acero reciclado", "categoria": "Metal", "estado_fisico": "Sólido",
        "toxicidad": "Baja", "cantidad_disponible": 2000, "unidad_medida": "kg",
        "tipo_transporte_requerido": "Camión industrial", "precio": 5.0,
    }, id_usuario_empresa=1)

    # Acero Industrial León (id 2) compra parte del material -> genera Transacción + Traslado
    resultado_compra = marketplace.comprar_material(
        id_publicacion=1, cantidad=500, id_usuario_comprador=2,
        punto_destino="Parque Industrial León, Gto."
    )

    # El transportista (id 3) toma la ruta generada y la avanza
    id_traslado = resultado_compra["datos"]["traslado"]["id"]
    codigo = resultado_compra["datos"]["traslado"]["codigo_paquete"]
    logistica.tomar_ruta(id_traslado, id_transportista=3)
    logistica.escanear_recoleccion(codigo, id_transportista=3)

    # Recicladora del Bajío publica una noticia sobre su impacto
    noticias.publicar_noticia({
        "titulo": "Recicladora del Bajío reduce 210 kg de CO2 este mes",
        "contenido": "Gracias al intercambio de acero reciclado con empresas del "
                     "Parque Industrial León, evitamos la extracción de materia prima virgen.",
        "categoria": "Local", "huella_carbono_ahorrada": 210,
    }, id_usuario_empresa=1)

    print("  ✅ Sistema listo para la demostración.\n")


if __name__ == "__main__":
    # 1. Instanciar capas de más bajo a más alto nivel (inyección de dependencias)
    repositorio = RepositorioDatos.obtener_instancia() # Capa de Datos — Singleton
    servicio_auth = ServicioAutenticacion(repositorio) # Capa de Negocio
    servicio_marketplace = ServicioMarketplace(repositorio) # Capa de Negocio
    servicio_noticias = ServicioNoticias(repositorio) # Capa de Negocio
    servicio_logistica = ServicioLogistica(repositorio) # Capa de Negocio

    interfaz = InterfazCLI(servicio_auth, servicio_marketplace,
                            servicio_noticias, servicio_logistica) # Capa de Presentación

    # 2. Pre-cargar datos de demostración
    cargar_datos_demo(servicio_auth, servicio_marketplace, servicio_noticias, servicio_logistica)

    # 3. Iniciar la aplicación
    interfaz.iniciar()
