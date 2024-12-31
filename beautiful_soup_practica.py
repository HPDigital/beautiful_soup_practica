# 1. Importaciones y configuración inicial
from bs4 import BeautifulSoup
import requests
import pandas as pd
import re
import logging
import json
from pathlib import Path
from datetime import datetime

# 2. Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scraping.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class WebScraper:
    def __init__(self):
        """Inicializa el scraper con configuraciones básicas"""
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        self.output_dir = Path('output')
        self.output_dir.mkdir(exist_ok=True)

    def get_page_content(self, url):
        """Obtiene el contenido de una URL de forma segura"""
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            logger.error(f"Error obteniendo la página {url}: {e}")
            return None

    def extract_article_info(self, soup):
        """Extrae información relevante del artículo"""
        info = {
            'title': soup.find('title').text if soup.find('title') else None,
            'headings': [h.text.strip() for h in soup.find_all(['h1', 'h2', 'h3'])],
            'paragraphs': [p.text.strip() for p in soup.find_all('p')],
            'links': [a['href'] for a in soup.find_all('a', href=True)],
            'metadata': {
                meta.get('name', meta.get('property', 'unknown')): meta.get('content')
                for meta in soup.find_all('meta')
                if meta.get('content')
            }
        }
        return info

    def extract_table_data(self, soup):
        """Extrae datos de tablas y los convierte a DataFrame"""
        tables = []
        for i, table in enumerate(soup.find_all('table')):
            try:
                df = pd.read_html(str(table))[0]
                df = df.apply(lambda x: x.astype(str).str.strip())
                tables.append({
                    'table_id': i + 1,
                    'data': df
                })
            except Exception as e:
                logger.error(f"Error procesando tabla {i + 1}: {e}")
        return tables

    def clean_text(self, text):
        """Limpia el texto removiendo espacios extra y caracteres especiales"""
        if text:
            # Eliminar espacios múltiples
            text = re.sub(r'\s+', ' ', text)
            # Eliminar caracteres especiales manteniendo puntuación básica
            text = re.sub(r'[^\w\s.,!?-]', '', text)
            return text.strip()
        return ''

    def process_content(self, soup):
        """Procesa y estructura el contenido de la página"""
        content = {
            'text': self.clean_text(soup.get_text()),
            'article_info': self.extract_article_info(soup),
            'tables': self.extract_table_data(soup),
            'images': [
                {
                    'src': img.get('src'),
                    'alt': img.get('alt'),
                    'title': img.get('title')
                }
                for img in soup.find_all('img')
                if img.get('src')
            ]
        }
        return content

    def save_results(self, results, url):
        """Guarda los resultados en diferentes formatos"""
        try:
            # Crear directorio con timestamp
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_path = self.output_dir / timestamp
            output_path.mkdir(exist_ok=True)

            # Guardar información general en JSON
            with open(output_path / 'article_info.json', 'w', encoding='utf-8') as f:
                json.dump(results['article_info'], f, ensure_ascii=False, indent=2)

            # Guardar texto limpio
            with open(output_path / 'clean_text.txt', 'w', encoding='utf-8') as f:
                f.write(results['text'])

            # Guardar tablas en Excel
            if results['tables']:
                with pd.ExcelWriter(output_path / 'tables.xlsx') as writer:
                    for table in results['tables']:
                        table['data'].to_excel(
                            writer, 
                            sheet_name=f'Table_{table["table_id"]}',
                            index=False
                        )

            # Guardar metadata del análisis
            metadata = {
                'url': url,
                'timestamp': timestamp,
                'tables_found': len(results['tables']),
                'images_found': len(results['images']),
                'paragraphs_found': len(results['article_info']['paragraphs'])
            }
            with open(output_path / 'metadata.json', 'w', encoding='utf-8') as f:
                json.dump(metadata, f, ensure_ascii=False, indent=2)

            logger.info(f"Resultados guardados en {output_path}")
            return output_path
        except Exception as e:
            logger.error(f"Error guardando resultados: {e}")
            return None

    def analyze_webpage(self, url):
        """Función principal que coordina el análisis de la página web"""
        logger.info(f"Iniciando análisis de {url}")
        
        # Obtener contenido
        content = self.get_page_content(url)
        if not content:
            return None
        
        # Crear objeto BeautifulSoup
        soup = BeautifulSoup(content, 'html.parser')
        
        # Procesar contenido
        results = self.process_content(soup)
        
        # Guardar resultados
        output_path = self.save_results(results, url)
        
        if output_path:
            logger.info(f"Análisis completado. Resultados en {output_path}")
        else:
            logger.error("Error al guardar los resultados")
        
        return results

def main():
    """Función principal de ejemplo"""
    # Crear instancia del scraper
    scraper = WebScraper()
    
    # URL de ejemplo
    url = "https://es.wikipedia.org/wiki/Bolivia"
    
    # Realizar análisis
    results = scraper.analyze_webpage(url)
    
    if results:
        print("\nResumen del análisis:")
        print(f"Título: {results['article_info']['title']}")
        print(f"Encabezados encontrados: {len(results['article_info']['headings'])}")
        print(f"Tablas encontradas: {len(results['tables'])}")
        print(f"Imágenes encontradas: {len(results['images'])}")
        print(f"Párrafos encontrados: {len(results['article_info']['paragraphs'])}")

if __name__ == "__main__":
    main() 