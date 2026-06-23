# FACTORY DE USUARIOS (patrón Factory Method / Simple Factory)
# Archivo: modelos/usuario_factory.py
# Capa: Modelos (Dominio) — Creación de objetos
# Patrón aplicado: Factory Method
#
# El sistema crea 3 tipos de usuario (Ciudadano, Empresa, Transportista) que
# comparten la misma clase/interfaz base (Usuario) pero requieren atributos
# de especialización distintos al momento de construirse. La Factory
# centraliza y desacopla esa lógica de creación: el cliente (la capa de
# Negocio) solo solicita un usuario de cierto tipo sin conocer los detalles
# de qué atributos extra debe llenar cada especialización.

from modelos.usuario import Usuario

# Aplicacion de Factory Method
class UsuarioFactory:
    """
    Fábrica responsable de construir instancias de Usuario ya configuradas
    según su tipo (Ciudadano / Empresa / Transportista).
    Capa/Componente: Modelos (Dominio)
    """

    @staticmethod
    def crear_usuario(tipo_usuario: str, datos: dict) -> Usuario: #Contiene un metodo publico que delga en metodos privados
        """
        Crea y devuelve una instancia de Usuario completamente configurada
        según su tipo. Lanza ValueError si el tipo no es soportado.
        """
        if tipo_usuario == "Ciudadano":
            return UsuarioFactory._crear_ciudadano(datos) #(privado)
        elif tipo_usuario == "Empresa":
            return UsuarioFactory._crear_empresa(datos) #(privado)
        elif tipo_usuario == "Transportista":
            return UsuarioFactory._crear_transportista(datos) #(privado)
        else:
            raise ValueError(
                f"Tipo de usuario no soportado: '{tipo_usuario}'. "
                f"Opciones válidas: {', '.join(Usuario.TIPOS_VALIDOS)}."
            ) #  cada uno configurando los atributos de especialización correspondientes (RFC/certificación para Empresa, licencia SCT para Transportista).

    # Métodos de construcción especializados (privados a la Factory)

    @staticmethod
    def _crear_ciudadano(datos: dict) -> Usuario:
        usuario = Usuario(
            correo=datos["correo"],
            contrasena=datos["contrasena"],
            tipo_usuario="Ciudadano",
            nombre=datos["nombre"],
        )
        # El Ciudadano no requiere atributos de especialización adicionales.
        return usuario

    @staticmethod
    def _crear_empresa(datos: dict) -> Usuario:
        usuario = Usuario(
            correo=datos["correo"],
            contrasena=datos["contrasena"],
            tipo_usuario="Empresa",
            nombre=datos["nombre"],
        )
        usuario.razon_social = datos.get("razon_social", datos["nombre"])
        usuario.rfc = datos.get("rfc", "PENDIENTE")
        usuario.certificacion_ambiental = datos.get("certificacion_ambiental", "En trámite")
        return usuario

    @staticmethod
    def _crear_transportista(datos: dict) -> Usuario:
        usuario = Usuario(
            correo=datos["correo"],
            contrasena=datos["contrasena"],
            tipo_usuario="Transportista",
            nombre=datos["nombre"],
        )
        usuario.licencia_sct = datos.get("licencia_sct", "PENDIENTE")
        return usuario
