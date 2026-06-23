# SERVICIO DE AUTENTICACIÓN 
# Capa: Negocio — Reglas de negocio del módulo "Perfiles y Auth"

from modelos.usuario import Usuario
from modelos.usuario_factory import UsuarioFactory


class ServicioAutenticacion:
    """
    Implementa el registro y el inicio de sesión de los 3 tipos de usuario:
    Ciudadano, Empresa (compra y/o vende) y Transportista.
    Capa/Componente: Negocio
    """

    def __init__(self, repositorio):
        self.repositorio = repositorio

    def registrar_usuario(self, datos: dict) -> dict:
        campos_requeridos = ["correo", "contrasena", "tipo_usuario", "nombre"]
        for campo in campos_requeridos:
            if not datos.get(campo):
                return {"exito": False, "mensaje": f'El campo "{campo}" es obligatorio.', "datos": None}

        if datos["tipo_usuario"] not in Usuario.TIPOS_VALIDOS:
            return {
                "exito": False,
                "mensaje": f"Tipo de usuario no válido. Opciones: {', '.join(Usuario.TIPOS_VALIDOS)}.",
                "datos": None,
            }

        if self.repositorio.buscar_usuario_por_correo(datos["correo"]) is not None:
            return {"exito": False, "mensaje": "Ya existe una cuenta registrada con ese correo.", "datos": None}

        # Patrón Factory Method: la creación del Usuario (incluyendo sus
        # atributos de especialización por tipo) queda encapsulada en la
        # Factory; el Servicio ya no conoce esos detalles de construcción.
        try:
            usuario = UsuarioFactory.crear_usuario(datos["tipo_usuario"], datos)
        except ValueError as error:
            return {"exito": False, "mensaje": str(error), "datos": None}

        if not usuario.es_valido():
            return {"exito": False, "mensaje": "Los datos del usuario no son válidos.", "datos": None}

        id_asignado = self.repositorio.guardar_usuario(usuario)
        return {
            "exito": True,
            "mensaje": f"Cuenta creada exitosamente con ID {id_asignado}. Ya puedes iniciar sesión.",
            "datos": usuario.to_dict(),
        }

    def iniciar_sesion(self, correo: str, contrasena: str) -> dict:
        usuario = self.repositorio.buscar_usuario_por_correo(correo)
        if usuario is None:
            return {"exito": False, "mensaje": "No existe ninguna cuenta con ese correo.", "datos": None}
        if usuario.contrasena != contrasena:
            return {"exito": False, "mensaje": "Contraseña incorrecta.", "datos": None}
        return {
            "exito": True,
            "mensaje": f"Bienvenido/a, {usuario.nombre} ({usuario.tipo_usuario}).",
            "datos": usuario,
        }
