# Sistema de Gestión y Análisis de Mercados Locales

## Descripción del Proyecto

El presente proyecto consiste en una aplicación de escritorio desarrollada en Python orientada a la gestión y análisis de información comercial dentro de mercados locales. El sistema fue diseñado utilizando Programación Orientada a Objetos (POO) y cuenta con una interfaz gráfica moderna desarrollada con CustomTkinter, permitiendo una interacción intuitiva y organizada para distintos tipos de usuarios.

La aplicación tiene como objetivo principal facilitar el registro, control y administración de vendedores, productos, inventario y ventas, además de proporcionar herramientas de análisis estadístico que permitan identificar patrones de consumo, productos con mayor demanda y comportamiento comercial dentro del mercado.

Este proyecto surge como una propuesta tecnológica para mejorar la organización de mercados tradicionales mediante herramientas digitales accesibles, buscando optimizar procesos que comúnmente se realizan de manera manual.


# Objetivos del Sistema

- Automatizar el control de productos y ventas.
- Facilitar la administración de usuarios y roles.
- Mejorar la organización de información comercial.
- Generar estadísticas y reportes automáticos.
- Implementar análisis visual mediante gráficas.
- Aplicar conceptos avanzados de Programación Orientada a Objetos.


# Características Principales

## Gestión de Usuarios

El sistema permite registrar, editar y eliminar usuarios con distintos roles:
- Administrador
- Vendedor
- Comprador

Además, implementa autenticación segura mediante cifrado SHA-256 para el manejo de contraseñas.


## Gestión de Productos

La aplicación permite:
- Registrar nuevos productos.
- Actualizar información de inventario.
- Editar precios y categorías.
- Eliminar productos.
- Realizar búsquedas dinámicas.
- Detectar productos con bajo stock.


## Registro de Ventas

El sistema incluye un módulo de ventas capaz de:
- Registrar transacciones.
- Actualizar automáticamente el inventario.
- Calcular montos totales.
- Asociar ventas a usuarios específicos.
- Registrar fecha y hora de cada operación.


## Estadísticas y Análisis

El proyecto incorpora herramientas visuales de análisis utilizando Matplotlib:
- Productos más vendidos.
- Ingresos por producto.
- Análisis de ventas por día.
- Gráficas de barras.
- Gráficas de pastel.

Estas funcionalidades permiten interpretar visualmente el comportamiento comercial del mercado.


# Exportación de Reportes

La aplicación puede generar reportes automáticos en formato Excel que incluyen:
- Información de usuarios.
- Inventario de productos.
- Historial de ventas.
- Estadísticas comerciales.
- Gráficas integradas.

Los reportes son generados automáticamente utilizando OpenPyXL.


# Tecnologías Utilizadas

## Lenguaje de Programación

- Python

## Librerías Principales

- Pandas
- CustomTkinter
- Tkinter
- Matplotlib
- OpenPyXL
- PIL 

## Herramientas

- Visual Studio Code
- Archivos CSV como almacenamiento local


# Arquitectura del Proyecto

El proyecto está organizado utilizando separación entre frontend y backend:

- `frontend.py`
  - Contiene toda la interfaz gráfica.
  - Manejo de pantallas y componentes visuales.

- `backend.py`
  - Manejo de lógica de negocio.
  - Gestión de usuarios, productos y ventas.
  - Generación de estadísticas y reportes.

- `setup_data.py`
  - Generación de datos de prueba para el sistema.


# Ventajas del Proyecto

- Interfaz gráfica moderna y amigable.
- Sistema multiusuario basado en roles.
- Control dinámico de inventario.
- Estadísticas integradas en tiempo real.
- Exportación profesional de reportes.
- Funcionamiento completamente local sin internet.
- Arquitectura escalable y modular.
- Seguridad básica mediante cifrado de contraseñas.


# Público Objetivo

El sistema está dirigido principalmente a:
- Mercados locales.
- Comerciantes pequeños.
- Administradores de mercados.
- Negocios familiares.
- Instituciones educativas para fines académicos.


# Estado del Proyecto

Proyecto académico desarrollado para la materia de Programación Avanzada, enfocado en la aplicación práctica de Programación Orientada a Objetos, interfaces gráficas y análisis de datos.

.
