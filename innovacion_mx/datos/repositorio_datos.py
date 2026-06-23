# REPOSITORIO EN MEMORIA (patrón Repository + Singleton)
# Archivo: datos/repositorio_datos.py
# Capa: Datos — Acceso y persistencia en memoria
# Patrones aplicados: Repository Pattern + Singleton
#
# Mantiene un "Mapeador de Entidades de Datos" único para Usuario, Material,
# Publicacion, Transaccion, Traslado y Noticia (igual rol que el componente
# "Mapeador de entidades de datos" del diagrama de arquitectura por capas).


class RepositorioDatos:
    """
    Almacena y recupera todas las entidades del sistema en memoria.
    Una única instancia compartida durante todo el ciclo de vida del sistema.
    Capa/Componente: Datos (Persistencia · Conector de base de datos centralizada)
    """
    
     # Variable de clase que almacenará la única instancia creada.
    # Inicialmente tiene valor None porque todavía no existe ningún objeto.
    # Esta variable pertenece a la clase completa y no a un objeto específico.
    _instancia = None

    # CAMBIO 1: atributo estático de clase (la única instancia)
    
    # Constructor de la clase def __init__(self)
    # Se encarga de inicializar los diccionarios donde se almacenarán
    # temporalmente las entidades del sistema.
    def __init__(self): 
        self._usuarios = {} # Diccionario para almacenar usuarios con estructura: {id_usuario : objeto_usuario}
        self._materiales = {} # Diccionario para almacenar materiales: {id_material : objeto_material}
        self._publicaciones = {} # Diccionario para almacenar publicaciones: {id_publicacion : objeto_publicacion}
        self._transacciones = {} # Diccionario para almacenar transacciones: {id_transaccion : objeto_transaccion}
        self._traslados = {} #Diccionario para almacenar traslados: {id_traslado : objeto_traslado}
        self._noticias = {} # Diccionario para almacenar noticias: {id_noticia : objeto_noticia}

        # Contadores utilizados para simular identificadores autoincrementables
        # como lo haría una base de datos.
        self._contador_usuario = 1 # Simulador de auto-incremento
        self._contador_material = 1
        self._contador_publicacion = 1
        self._contador_transaccion = 1
        self._contador_traslado = 1
        self._contador_noticia = 1

    # CAMBIO 2: método estático de acceso (punto de entrada global)
    # Método de acceso global del patrón Singleton.
    # @classmethod permite trabajar directamente con la clase,
    # sin necesidad de crear un objeto previamente.
    # Este método controla que solamente exista una instancia del repositorio.
    @classmethod
    def obtener_instancia(cls):
        if cls._instancia is None: # Verifica si todavía no existe una instancia creada.
            # Si no existe, crea la única instancia permitida.
            # Después de este punto todos los módulos usarán este mismo objeto.
            cls._instancia = RepositorioDatos()
        # Retorna siempre la misma instancia compartida.
        # Así todos los componentes acceden al mismo almacenamiento de datos.
        return cls._instancia

    # Usuario
    def guardar_usuario(self, usuario) -> int:
        usuario.id = self._contador_usuario
        self._usuarios[usuario.id] = usuario
        self._contador_usuario += 1
        return usuario.id

    def buscar_usuario_por_id(self, id_usuario: int):
        return self._usuarios.get(id_usuario)

    def buscar_usuario_por_correo(self, correo: str):
        for u in self._usuarios.values():
            if u.correo.lower() == correo.lower() and u.activo:
                return u
        return None

    def listar_usuarios_por_tipo(self, tipo: str) -> list:
        return [u for u in self._usuarios.values() if u.activo and u.tipo_usuario == tipo]

    # Material 
    def guardar_material(self, material) -> int:
        material.id = self._contador_material
        self._materiales[material.id] = material
        self._contador_material += 1
        return material.id

    def buscar_material_por_id(self, id_material: int):
        return self._materiales.get(id_material)

    def listar_materiales(self) -> list:
        return [m for m in self._materiales.values() if m.activo]

    def listar_materiales_por_propietario(self, id_usuario: int) -> list:
        return [m for m in self._materiales.values() if m.activo and m.id_usuario_propietario == id_usuario]

    # Publicación 
    def guardar_publicacion(self, publicacion) -> int:
        publicacion.id = self._contador_publicacion
        self._publicaciones[publicacion.id] = publicacion
        self._contador_publicacion += 1
        return publicacion.id

    def listar_publicaciones_disponibles(self) -> list:
        return [p for p in self._publicaciones.values() if p.estatus == "Disponible"]

    def buscar_publicacion_por_id(self, id_publicacion: int):
        return self._publicaciones.get(id_publicacion)

    def listar_publicaciones_por_usuario(self, id_usuario: int) -> list:
        return [p for p in self._publicaciones.values() if p.id_usuario == id_usuario]

    # Transacción 
    def guardar_transaccion(self, transaccion) -> int:
        transaccion.id = self._contador_transaccion
        self._transacciones[transaccion.id] = transaccion
        self._contador_transaccion += 1
        return transaccion.id

    def buscar_transaccion_por_id(self, id_transaccion: int):
        return self._transacciones.get(id_transaccion)

    def listar_transacciones_por_usuario(self, id_usuario: int) -> list:
        return [t for t in self._transacciones.values()
                if t.id_usuario_proveedor == id_usuario or t.id_usuario_receptor == id_usuario]

    # Traslado 
    def guardar_traslado(self, traslado) -> int:
        traslado.id = self._contador_traslado
        self._traslados[traslado.id] = traslado
        self._contador_traslado += 1
        return traslado.id

    def buscar_traslado_por_id(self, id_traslado: int):
        return self._traslados.get(id_traslado)

    def buscar_traslado_por_codigo(self, codigo_paquete: str):
        for t in self._traslados.values():
            if t.codigo_paquete == codigo_paquete:
                return t
        return None

    def listar_traslados_por_transportista(self, id_transportista: int) -> list:
        return [t for t in self._traslados.values() if t.id_transportista == id_transportista]

    # Noticia 
    def guardar_noticia(self, noticia) -> int:
        noticia.id = self._contador_noticia
        self._noticias[noticia.id] = noticia
        self._contador_noticia += 1
        return noticia.id

    def listar_noticias(self) -> list:
        return list(self._noticias.values())
