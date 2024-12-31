# Web Scraper con BeautifulSoup

Un scraper web moderno y eficiente implementado en Python que utiliza BeautifulSoup4 para extraer y analizar contenido de páginas web. El proyecto está diseñado para extraer automáticamente títulos, encabezados, párrafos, tablas, imágenes y metadatos de cualquier página web proporcionada.

## 🚀 Características Principales

- Extracción automática de contenido web
- Procesamiento de tablas HTML a Excel
- Extracción de metadatos e imágenes
- Sistema de limpieza de texto
- Organización automática de resultados por timestamp
- Sistema completo de logging
- Manejo de errores robusto

## 📋 Requisitos Previos

## 📖 Instalación

1. Clona el repositorio:

2. Crea un entorno virtual:

3. Instala las dependencias:

## 🎯 Uso

### Uso Básico

### Estructura de Resultados

El scraper genera los siguientes archivos en `output/[timestamp]/`:

- `article_info.json`: Información general del artículo
- `clean_text.txt`: Texto extraído y limpio
- `tables.xlsx`: Tablas encontradas en formato Excel
- `metadata.json`: Metadatos del análisis

## 📁 Estructura del Proyecto

## 🔍 Funcionalidades Detalladas

### Extracción de Contenido
- Títulos y encabezados
- Párrafos y texto limpio
- Enlaces
- Tablas
- Imágenes y sus atributos
- Metadatos de la página

### Procesamiento
- Limpieza automática de texto
- Conversión de tablas a Excel
- Organización temporal de resultados

### Almacenamiento
- Resultados organizados por timestamp
- Múltiples formatos (JSON, Excel, TXT)
- Metadatos completos del análisis

## ⚙️ Dependencias Principales

- beautifulsoup4>=4.12.0
- requests>=2.31.0
- pandas>=2.0.0
- lxml>=4.9.0
- openpyxl>=3.1.0

## 📝 Logging

El sistema incluye logging completo que:
- Registra todas las operaciones en `scraping.log`
- Guarda errores y advertencias
- Proporciona trazabilidad completa

## 🔒 Manejo de Errores

El scraper incluye manejo robusto de errores para:
- Conexiones fallidas
- Páginas no encontradas
- Contenido malformado
- Errores de parseo
- Problemas de escritura de archivos

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para detalles

## ✨ Agradecimientos

- BeautifulSoup4 por su excelente biblioteca de scraping
- Pandas por el manejo de datos
- Requests por la gestión de peticiones HTTP
