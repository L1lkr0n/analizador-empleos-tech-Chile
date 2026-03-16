import pandas as pd
import logging
from scrapping import configurar_driver, realizar_scraping
from database import insertar_productos
from correo import enviar_correo

# Configuración de Logging centralizada
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("analisis_precios.log", encoding='utf-8'),
        logging.StreamHandler()
    ]
)

def ejecutar_pipeline():
    driver = configurar_driver()
    termino = "smartphones"
    
    try:
        # 1. Scrapeo
        datos = realizar_scraping(driver, termino)
        
        if not datos:
            logging.warning("No se encontraron datos.")
            return

        # 2. Procesamiento
        df = pd.DataFrame(datos)
        df['Precio'] = pd.to_numeric(df['Precio'], errors='coerce').fillna(0).astype(int)
        
        # 3. Carga a Oracle
        insertar_productos(df)

        # Si todo sale bien, enviamos el aviso
        enviar_correo(
            "✅ Scraping Lider: Éxito",
            f"Hola Alejandro, el proceso ha finalizado correctamente. Se subieron {len(df)} productos a Oracle."
        )
        
    except Exception as e:
        logging.error(f"Fallo crítico en el pipeline principal: {e}")
        # Si falla, también te avisa del error
        enviar_correo(
           "❌ Scraping Lider: FALLO",
           f"El proceso falló. Error: {str(e)}"
        )
    finally:
        driver.quit()
        logging.info("Proceso finalizado.")

if __name__ == "__main__":
    ejecutar_pipeline()