import pandas as pd 
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import oracledb

USER = "system"
PASSWORD = "system"
DSN = "localhost:1521/XE"

# 1. Configuración de Chrome
chrome_options = Options()
# chrome_options.add_argument("--headless") # Descomenta esto para que no se abra la ventana

driver = webdriver.Chrome(options=chrome_options)

termino = "smartphones" # Puedes cambiarlo por lo que quieras buscar

def scrapear_lider(termino_busqueda):
    # Ir a la página principal primero para establecer la sesión
    driver.get("https://www.lider.cl/supermercado/")
    productos_lista = []
    
    try:
        wait = WebDriverWait(driver, 10)
        
        # 1. Buscar la barra de búsqueda por su ID o Clase
        # En Lider suele ser un input con un placeholder tipo "¿Qué buscas hoy?"
        search_input = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div/div[1]/span/header/form/div/input")))
        
        # 2. Escribir el término y presionar Enter
        search_input.clear()
        search_input.send_keys(termino_busqueda)
        search_input.submit() # Esto simula el "Enter"
        
        print(f"Buscando: {termino_busqueda}...")

        # 3. Esperar a que carguen los resultados
        wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div/div[1]/div/div/div[1]/main/div/div[2]/div/div/div[1]/div/section/div/div[2]")))

        print("Resultados cargados, extrayendo datos...")

        # 4. Un pequeño scroll para asegurar carga de lazy-loading
        driver.execute_script("window.scrollBy(0, 800);")
        time.sleep(3)
         
        print("Extrayendo productos...")

        # 5. Capturar los productos
        productos = driver.find_elements(By.CSS_SELECTOR, "div.flex.flex-wrap.w-100.flex-grow-0.flex-shrink-0.ph2.pr0-xl.pl4-xl.mt0-xl>div")

        print(f"Productos encontrados: {len(productos)}")

        for p in productos:
            try:
                nombre = p.find_element(By.CSS_SELECTOR, "div.flex.flex-wrap.w-100.flex-grow-0.flex-shrink-0.ph2.pr0-xl.pl4-xl.mt0-xl>div>div>div>div>div>div>span>span").text
                marca = p.find_element(By.CSS_SELECTOR, "div.flex.flex-wrap.w-100.flex-grow-0.flex-shrink-0.ph2.pr0-xl.pl4-xl.mt0-xl>div>div>div>div>div>div> div.mb1.mt2.b.f6.black.mr1.lh-copy").text
                precio = p.find_element(By.CSS_SELECTOR, "div.flex.flex-wrap.w-100.flex-grow-0.flex-shrink-0.ph2.pr0-xl.pl4-xl.mt0-xl>div>div>div>div>div>div>div>div>div.mr1.mr2-xl.b.black.lh-copy.f5.f4-l").text
                
                if nombre and precio and marca:
                    productos_lista.append({
                        "Nombre": nombre,
                        "Precio": precio.replace('$', '').replace('.', '').strip(),
                        "Marca": marca,
                    })
            except:
                continue 

    except Exception as e:
        print(f"Error durante la búsqueda: {e}")
    
    return productos_lista

# --- EJECUCIÓN ---

datos = scrapear_lider(termino)

df = pd.DataFrame(datos)
df['Precio'] = pd.to_numeric(df['Precio'], errors='coerce').fillna(0).astype(int)

try:
    # 3. Conectar a Oracle
    connection = oracledb.connect(user=USER, password=PASSWORD, dsn=DSN)
    cursor = connection.cursor()

    # 4. Preparar los datos para la inserción masiva
    # Convertimos el DataFrame en una lista de tuplas
    registros = list(df.itertuples(index=False, name=None))

    # 5. Ejecutar la inserción
    sql = "INSERT INTO Smartphone_Lider (NOMBRE, PRECIO, MARCA) VALUES (:1, :2, :3)"
    
    cursor.executemany(sql, registros)
    
    # 6. Confirmar cambios
    connection.commit()
    print(f"✅ ¡Éxito! Se han subido {len(registros)} registros a la tabla Smartphone_Lider.")

except Exception as e:
    print(f"❌ Error al subir a Oracle: {e}")

finally:
    if 'cursor' in locals():
        cursor.close()
    if 'connection' in locals():
        connection.close()

# 2. Guardar con Pandas
#if datos:
#    df = pd.DataFrame(datos)
#    print(df.head())
#    df.to_csv("precios_lider.csv", index=False, encoding='utf-8-sig')
#   print("\n¡Archivo guardado exitosamente!")
#else:
#    print("No se encontraron productos.")

driver.quit()