# Web Scraping para Monitoreo de Precios - Líder

## Descripción
Este proyecto automatiza la extracción de datos de productos desde el sitio web de Líder.cl. El objetivo es recopilar información de precios y stock de forma diaria para alimentar una base de datos de análisis.

## Tecnologías Utilizadas
* **Python**: Lenguaje principal.
* **Selenium**: Para la navegación y extracción de datos.
* **Oracle DB (21c)**: Almacenamiento persistente de los datos.
* **Windows Task Scheduler**: Orquestación y automatización diaria de la ejecución.
* **Email.MIME/smtplib/os/dotenv**: Creacion y envio de correo como notificacion de termino de ejecucion.

## Características
* **Extracción Automatizada**: Navega por las categorías configuradas.
* **Limpieza de Datos**: Procesa strings y formatos de precio antes de la inserción.
* **Carga Eficiente**: Manejo de conexiones y commits en Oracle para asegurar la integridad de los datos.
