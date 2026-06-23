# INTERFAZ DE LÍNEA DE COMANDOS (CLI)
# Archivo: presentacion/interfaz_cli.py
# Capa: Presentación — Interacción con el usuario
# Sólo muestra datos y solicita entradas. Las decisiones van en los Servicios.
#
# Flujo de autenticación -> 3 interfaces diferenciadas:
# 1. Ciudadano -> Tablero de noticias (consultar / filtrar por año-mes)
# 2. Empresa -> Publicar materiales, comprar en el marketplace,
# publicar noticias de sus logros (compra y venta comparten la misma interfaz)
# 3. Transportista-> Tomar rutas, escanear recolección y entrega 

from modelos.usuario import Usuario
from modelos.noticia import Noticia


class InterfazCLI:

    SEP = "=" * 64
    LINEA = "-" * 64

    def __init__(self, servicio_auth, servicio_marketplace, servicio_noticias, servicio_logistica):
        self.servicio_auth = servicio_auth
        self.servicio_marketplace = servicio_marketplace
        self.servicio_noticias = servicio_noticias
        self.servicio_logistica = servicio_logistica
        self.usuario_actual = None

    # PANTALLA DE AUTENTICACIÓN 

    def iniciar(self):
        while True:
            print(f"\n{self.SEP}")
            print("  INNOVACIÓN MX — Gestión e Intercambio de Residuos Industriales")
            print("  ODS 9 · Industria, Innovación e Infraestructura")
            print(self.SEP)
            print("  1. Iniciar sesión")
            print("  2. Registrarme")
            print("  0. Salir")
            print(self.LINEA)
            opcion = input("  Selecciona una opción: ").strip()

            if opcion == "1":
                self._flujo_login()
            elif opcion == "2":
                self._flujo_registro()
            elif opcion == "0":
                print("\n  Cerrando sistema. Hasta luego.\n")
                break
            else:
                print("  ⚠  Opción no válida.")

            if self.usuario_actual is not None:
                self._enrutar_a_interfaz()
                self.usuario_actual = None   # logout al volver

    def _flujo_registro(self):
        print(f"\n{self.LINEA}")
        print("  CREAR CUENTA")
        print(self.LINEA)
        print("  ¿Qué tipo de cuenta deseas crear?")
        print("  1. Ciudadano               (consultar noticias del ODS 9)")
        print("  2. Empresa                 (publicar y/o comprar residuos)")
        print("  3. Transportista            (personal de paquetería / rutas)")
        sub = input("  Opción: ").strip()

        mapa_tipo = {"1": "Ciudadano", "2": "Empresa", "3": "Transportista"}
        tipo = mapa_tipo.get(sub)
        if tipo is None:
            print("  ❌ Opción no válida.")
            return

        correo = input("  Correo: ").strip()
        contrasena = input("  Contraseña: ").strip()
        nombre = input("  Nombre completo / Razón social: ").strip()

        datos = {"correo": correo, "contrasena": contrasena, "tipo_usuario": tipo, "nombre": nombre}

        if tipo == "Empresa":
            datos["rfc"] = input("  RFC: ").strip()
            datos["certificacion_ambiental"] = input("  Certificación ambiental (o 'En trámite'): ").strip()
        elif tipo == "Transportista":
            datos["licencia_sct"] = input("  Licencia SCT: ").strip()

        resultado = self.servicio_auth.registrar_usuario(datos)
        icono = "✅" if resultado["exito"] else "❌"
        print(f"\n  {icono} {resultado['mensaje']}")

    def _flujo_login(self):
        print(f"\n{self.LINEA}")
        print("  INICIAR SESIÓN")
        correo = input("  Correo: ").strip()
        contrasena = input("  Contraseña: ").strip()

        resultado = self.servicio_auth.iniciar_sesion(correo, contrasena)
        if not resultado["exito"]:
            print(f"\n  ❌ {resultado['mensaje']}")
            return
        print(f"\n  ✅ {resultado['mensaje']}")
        self.usuario_actual = resultado["datos"]

    def _enrutar_a_interfaz(self):
        if self.usuario_actual is None:
            return
        if self.usuario_actual.tipo_usuario == "Ciudadano":
            self._interfaz_ciudadano()
        elif self.usuario_actual.tipo_usuario == "Empresa":
            self._interfaz_empresa()
        elif self.usuario_actual.tipo_usuario == "Transportista":
            self._interfaz_transportista()

    # INTERFAZ 1: CIUDADANO — Tablero de noticias

    def _interfaz_ciudadano(self):
        if self.usuario_actual is None:
            return
        while True:
            print(f"\n{self.SEP}")
            print(f"  TABLERO DE NOTICIAS ODS 9 — {self.usuario_actual.nombre}")
            print(self.SEP)
            print("  1. Ver todas las noticias")
            print("  2. Filtrar noticias por año")
            print("  3. Filtrar noticias por mes")
            print("  4. Filtrar noticias por año y mes")
            print("  0. Cerrar sesión")
            opcion = input("  Selecciona una opción: ").strip()

            if opcion == "1":
                self._mostrar_noticias(self.servicio_noticias.consultar_feed())
            elif opcion == "2":
                anio = self._pedir_entero("  Año (ej. 2026): ")
                if anio is not None:
                    self._mostrar_noticias(self.servicio_noticias.filtrar_feed(anio=anio))
            elif opcion == "3":
                mes = self._pedir_entero("  Mes (1-12): ")
                if mes is not None:
                    self._mostrar_noticias(self.servicio_noticias.filtrar_feed(mes=mes))
            elif opcion == "4":
                anio = self._pedir_entero("  Año (ej. 2026): ")
                mes = self._pedir_entero("  Mes (1-12): ")
                if anio is not None and mes is not None:
                    self._mostrar_noticias(self.servicio_noticias.filtrar_feed(anio=anio, mes=mes))
            elif opcion == "0":
                print("\n  Sesión cerrada.")
                break
            else:
                print("  ⚠  Opción no válida.")

    def _mostrar_noticias(self, resultado):
        print(f"\n  {resultado['mensaje']}")
        for n in resultado["datos"]:
            print(f"""
  ┌─ Noticia ID {n['id']} {'─' * 30}
  │  Título   : {n['titulo']}
  │  Empresa  : {n['empresa']}
  │  Categoría: {n['categoria']}
  │  Fecha    : {n['fecha_publicacion']}
  │  Huella de carbono ahorrada: {n['huella_carbono_ahorrada']} kg CO2
  │  Contenido: {n['contenido']}
  └{'─' * 47}""")

    # INTERFAZ 2: EMPRESA (compra y/o vende, misma interfaz)

    def _interfaz_empresa(self):
        if self.usuario_actual is None:
            print("  ⚠  No hay usuario autenticado. Regresa al inicio.")
            return
        while True:
            print(f"\n{self.SEP}")
            print(f"  PANEL EMPRESARIAL — {self.usuario_actual.nombre}")
            print(f"  Huella de carbono evitada acumulada: {self.usuario_actual.huella_carbono_evitada_total} kg CO2")
            print(self.SEP)
            print("  1. Publicar material residual para venta")
            print("  2. Ver mis materiales publicados")
            print("  3. Ver marketplace (materiales de otras empresas)")
            print("  4. Comprar material del marketplace")
            print("  5. Ver mis transacciones (compras y ventas)")
            print("  6. Publicar noticia sobre mis logros ODS 9")
            print("  7. Confirmar reutilización de un residuo recibido")
            print("  0. Cerrar sesión")
            opcion = input("  Selecciona una opción: ").strip()

            if opcion == "1":
                self._flujo_publicar_material()
            elif opcion == "2":
                self._flujo_mis_materiales()
            elif opcion == "3":
                self._flujo_ver_marketplace()
            elif opcion == "4":
                self._flujo_comprar_material()
            elif opcion == "5":
                self._flujo_mis_transacciones()
            elif opcion == "6":
                self._flujo_publicar_noticia()
            elif opcion == "7":
                self._flujo_confirmar_reutilizacion()
            elif opcion == "0":
                print("\n  Sesión cerrada.")
                break
            else:
                print("  ⚠  Opción no válida.")

    def _flujo_publicar_material(self):
        if not self.usuario_actual:
            print("  ⚠  Error: No hay usuario autenticado.")
            return
        print(f"\n{self.LINEA}")
        print("  PUBLICAR MATERIAL RESIDUAL")
        datos = {
            "nombre": input("  Nombre del material: ").strip(),
            "categoria": input("  Categoría (Metal/Plástico/Papel-Cartón/Madera/Químico/Textil/Otro): ").strip(),
            "estado_fisico": input("  Estado físico (Sólido/Líquido/Gaseoso): ").strip(),
            "toxicidad": input("  Toxicidad (Baja/Media/Alta): ").strip(),
            "cantidad_disponible": input("  Cantidad disponible: ").strip(),
            "unidad_medida": input("  Unidad de medida (kg/ton/litros/piezas): ").strip(),
            "tipo_transporte_requerido": input("  Tipo de transporte requerido: ").strip(),
            "precio": input("  Precio: ").strip(),
        }
        resultado = self.servicio_marketplace.publicar_material(datos, self.usuario_actual.id)
        self._mostrar_resultado(resultado)

    def _flujo_mis_materiales(self):
        if not self.usuario_actual:
            print("  ⚠  Error: No hay usuario autenticado.")
            return
        resultado = self.servicio_marketplace.listar_mis_materiales(self.usuario_actual.id)
        print(f"\n  {resultado['mensaje']}")
        for m in resultado["datos"]:
            print(f"  • [{m['id']}] {m['nombre']} — {m['cantidad_disponible']} {m['unidad_medida']} "
                  f"(Toxicidad: {m['toxicidad']})")

    def _flujo_ver_marketplace(self):
        if not self.usuario_actual:
            print("  ⚠  Error: No hay usuario autenticado.")
            return
        resultado = self.servicio_marketplace.listar_marketplace(excluir_id_usuario=self.usuario_actual.id)
        print(f"\n  {resultado['mensaje']}")
        for item in resultado["datos"]:
            pub, mat = item["publicacion"], item["material"]
            print(f"""
  ┌─ Publicación ID {pub['id']} {'─' * 25}
  │  Material  : {mat['nombre']} ({mat['categoria']})
  │  Vendedor  : {item['vendedor']}
  │  Cantidad  : {mat['cantidad_disponible']} {mat['unidad_medida']}
  │  Precio    : ${pub['precio']:,.2f}
  │  Transporte requerido: {mat['tipo_transporte_requerido']}
  └{'─' * 40}""")

    def _flujo_comprar_material(self):
        if not self.usuario_actual:
            print("  ⚠  Error: No hay usuario autenticado.")
            return
        print(f"\n{self.LINEA}")
        print("  COMPRAR MATERIAL")
        id_publicacion = self._pedir_entero("  ID de la publicación a comprar: ")
        if id_publicacion is None:
            return
        cantidad = input("  Cantidad a comprar: ").strip()
        destino = input("  Punto de destino (dirección de tu empresa): ").strip()

        resultado = self.servicio_marketplace.comprar_material(
            id_publicacion, cantidad, self.usuario_actual.id, destino
        )
        self._mostrar_resultado(resultado)

    def _flujo_mis_transacciones(self):
        if not self.usuario_actual:
            print("  ⚠  Error: No hay usuario autenticado.")
            return

        resultado = self.servicio_marketplace.listar_mis_transacciones(self.usuario_actual.id)
        print(f"\n  {resultado['mensaje']}")
        for item in resultado["datos"]:
            t = item["transaccion"]
            tr = item["traslado"]
            estado = tr["estado"] if tr else "Sin traslado"
            codigo = tr["codigo_paquete"] if tr else "-"
            print(f"  • Transacción [{t['id']}] material={t['id_material']} cantidad={t['cantidad_material']} "
                  f"| Traslado: {estado} (código {codigo})")

    def _flujo_publicar_noticia(self):
        if not self.usuario_actual:
            print("  ⚠  Error: No hay usuario autenticado.")
            return
        
        print(f"\n{self.LINEA}")
        print("  PUBLICAR NOTICIA SOBRE LOGROS ODS 9")
        datos = {
            "titulo": input("  Título: ").strip(),
            "contenido": input("  Contenido (qué se logró, cuánto se redujo, etc.): ").strip(),
            "categoria": input(f"  Categoría ({'/'.join(Noticia.CATEGORIAS_VALIDAS)}): ").strip(),
            "huella_carbono_ahorrada": input("  Huella de carbono ahorrada (kg CO2, opcional): ").strip() or 0,
        }
        resultado = self.servicio_noticias.publicar_noticia(datos, self.usuario_actual.id)
        self._mostrar_resultado(resultado)

    def _flujo_confirmar_reutilizacion(self):
        if not self.usuario_actual:
            print("  ⚠  Error: No hay usuario autenticado.")
            return

        print(f"\n{self.LINEA}")
        print("  CONFIRMAR REUTILIZACIÓN DE RESIDUO RECIBIDO")
        id_traslado = self._pedir_entero("  ID del traslado (lo ves en 'Mis transacciones'): ")
        if id_traslado is None:
            return
        resultado = self.servicio_logistica.confirmar_reutilizacion(id_traslado, self.usuario_actual.id)
        self._mostrar_resultado(resultado)

    # INTERFAZ 3: TRANSPORTISTA — Rutas y escaneo de paquetes 

    def _interfaz_transportista(self):
        if not self.usuario_actual:
            print("  ⚠  Error: No hay usuario autenticado.")
            return
        while True:
            print(f"\n{self.SEP}")
            print(f"  PANEL DE TRANSPORTISTA — {self.usuario_actual.nombre}")
            print(self.SEP)
            print("  1. Ver paquetes disponibles para tomar ruta")
            print("  2. Tomar una ruta")
            print("  3. Ver mis rutas asignadas")
            print("  4. Escanear paquete RECOLECTADO (origen)")
            print("  5. Escanear paquete ENTREGADO (destino)")
            print("  6. Reportar incidencia en ruta")
            print("  0. Cerrar sesión")
            opcion = input("  Selecciona una opción: ").strip()

            if opcion == "1":
                resultado = self.servicio_logistica.listar_paquetes_disponibles()
                self._mostrar_traslados(resultado)
            elif opcion == "2":
                id_traslado = self._pedir_entero("  ID del traslado a tomar: ")
                if id_traslado is not None:
                    resultado = self.servicio_logistica.tomar_ruta(id_traslado, self.usuario_actual.id)
                    self._mostrar_resultado(resultado)
            elif opcion == "3":
                resultado = self.servicio_logistica.listar_mis_rutas(self.usuario_actual.id)
                self._mostrar_traslados(resultado)
            elif opcion == "4":
                codigo = input("  Escanea (escribe) el código del paquete: ").strip()
                resultado = self.servicio_logistica.escanear_recoleccion(codigo, self.usuario_actual.id)
                self._mostrar_resultado(resultado)
            elif opcion == "5":
                codigo = input("  Escanea (escribe) el código del paquete: ").strip()
                resultado = self.servicio_logistica.escanear_entrega(codigo, self.usuario_actual.id)
                self._mostrar_resultado(resultado)
            elif opcion == "6":
                codigo = input("  Código del paquete con incidencia: ").strip()
                resultado = self.servicio_logistica.reportar_incidencia(codigo, self.usuario_actual.id)
                self._mostrar_resultado(resultado)
            elif opcion == "0":
                print("\n  Sesión cerrada.")
                break
            else:
                print("  ⚠  Opción no válida.")

    def _mostrar_traslados(self, resultado):
        print(f"\n  {resultado['mensaje']}")
        for t in resultado["datos"]:
            print(f"""
  ┌─ Traslado ID {t['id']} {'─' * 30}
  │  Código paquete : {t['codigo_paquete']}
  │  Destino         : {t['punto_destino']}
  │  Estado          : {t['estado']}
  │  Distancia       : {t['distancia_recorrida']} km
  │  Huella evitada  : {t['huella_carbono_evitada']} kg CO2
  └{'─' * 42}""")

    # Helpers comunes para mostrar resultados y pedir enteros

    def _mostrar_resultado(self, resultado: dict):
        icono = "✅" if resultado["exito"] else "❌"
        print(f"\n  {icono} {resultado['mensaje']}")

    def _pedir_entero(self, etiqueta: str):
        valor = input(etiqueta).strip()
        try:
            return int(valor)
        except ValueError:
            print("  ❌ Debes ingresar un número entero válido.")
            return None
