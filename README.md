# Innovación MX — Gestión e Intercambio de Residuos Industriales

> **ODS 9 — Industria, Innovación e Infraestructura**  
> Materia: Modelado de Sistemas — Semestre Feb-Jun 2026  
> Versión: MVP 1.0

## Descripción

**Innovación MX** es una plataforma que conecta empresas generadoras de residuos industriales con empresas recicladoras, transportistas y ciudadanos interesados en el impacto ambiental.

Permite:
- Publicar materiales residuales disponibles para venta
- Gestionar transacciones e intercambios entre empresas
- Hacer seguimiento logístico de traslados
- Compartir noticias sobre logros ambientales

## Arquitectura

El proyecto sigue una **Arquitectura por Capas (Layered)** con los siguientes componentes:

```
innovacion_mx/
├── main.py                        # Punto de entrada
├── modelos/                       # Capa de Dominio (entidades)
│   ├── usuario.py
│   ├── usuario_factory.py
│   ├── material.py
│   ├── publicacion.py
│   ├── transaccion.py
│   ├── traslado.py
│   └── noticia.py
├── datos/                         # Capa de Datos (Repository Pattern + Singleton)
│   └── repositorio_datos.py
├── negocio/                       # Capa de Negocio (lógica de servicios)
│   ├── servicio_autenticacion.py
│   ├── servicio_marketplace.py
│   ├── servicio_logistica.py
│   └── servicio_noticias.py
└── presentacion/                  # Capa de Presentación (CLI)
    └── interfaz_cli.py
```

**Patrones de diseño aplicados:** Repository Pattern + Singleton

## Requisitos

- Python 3.10 o superior
- No se requieren dependencias externas (solo librería estándar)

## Instalación y ejecución

```bash
# Clonar el repositorio
git clone https://github.com/TU_USUARIO/innovacion_mx_MVP.git
cd innovacion_mx_MVP

# Ejecutar el sistema
python innovacion_mx/main.py
```

## Cuentas de demostración

Todas las cuentas usan la contraseña **`1234`**:

| Correo | Tipo | Nombre |
|--------|------|--------|
| empresa1@innovacionmx.com | Empresa | Recicladora del Bajío |
| empresa2@innovacionmx.com | Empresa | Acero Industrial León |
| transportista1@innovacionmx.com | Transportista | Juan Pérez |
| ciudadano1@innovacionmx.com | Ciudadano | Ana Torres |

## Escenario de demostración MVP

1. Una **Empresa** publica un material residual disponible para venta.
2. Otra **Empresa** lo compra → se genera una Transacción y un Traslado.
3. Un **Transportista** toma la ruta y escanea recolección y entrega.
4. La empresa receptora confirma la reutilización del residuo.
5. Una **Empresa** publica una noticia sobre su huella de carbono ahorrada.
6. Un **Ciudadano** consulta y filtra el tablero de noticias por año/mes.

## Equipo

Proyecto desarrollado para la materia de **Modelado de Sistemas** — Semestre Feb-Jun 2026.
