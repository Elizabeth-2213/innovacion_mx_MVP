from datetime import datetime


class Usuario:
    """
    Representa a un usuario de la plataforma Innovación MX.
    Corresponde a la entidad 'Usuario' del Diagrama de Clases.
    Capa/Componente: Modelos (Dominio)
    ODS 9 — Industria, Innovación e Infraestructura.

    Tipo_Usuario funciona como discriminador (igual que en el diagrama de
    clases original): "Ciudadano", "Empresa" o "Transportista".
    Una empresa puede comprar y vender materiales con el mismo perfil.
    """

    TIPOS_VALIDOS = ["Ciudadano", "Empresa", "Transportista"]

    def __init__(self, correo: str, contrasena: str, tipo_usuario: str, nombre: str):
        self.id = None # Asignado por el repositorio
        self.correo = correo
        self.contrasena = contrasena
        self.tipo_usuario = tipo_usuario
        self.nombre = nombre # Razón social o nombre completo
        self.fecha_registro = datetime.now()
        self.activo = True

        # Atributos específicos por especialización (sólo se llenan según el tipo)
        self.razon_social = None
        self.rfc = None
        self.certificacion_ambiental = None
        self.huella_carbono_evitada_total = 0.0 # Acumulado de la empresa
        self.licencia_sct = None # Sólo Transportista

    def es_valido(self) -> bool:
        return (
            bool(self.correo) and
            bool(self.contrasena) and
            self.tipo_usuario in self.TIPOS_VALIDOS and
            bool(self.nombre)
        )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "correo": self.correo,
            "tipo_usuario": self.tipo_usuario,
            "nombre": self.nombre,
            "fecha_registro": self.fecha_registro.strftime("%Y-%m-%d %H:%M"),
            "razon_social": self.razon_social,
            "rfc": self.rfc,
            "huella_carbono_evitada_total": self.huella_carbono_evitada_total,
            "licencia_sct": self.licencia_sct,
        }

    def __repr__(self) -> str:
        return f"Usuario(id={self.id}, correo='{self.correo}', tipo='{self.tipo_usuario}')"
