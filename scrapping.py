import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC

def configurar_driver():
    chrome_options = Options()
    # chrome_options.add_argument("--headless")
    return webdriver.Chrome(options=chrome_options)

def realizar_scraping(driver, termino_busqueda):
    driver.get("https://www.lider.cl/supermercado/")
    productos_lista = []
    
    try:
        wait = WebDriverWait(driver, 10)
        logging.info(f"Iniciando busqueda de: {termino_busqueda}")
        
        search_input = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div/div[1]/span/header/form/div/input")))
        search_input.clear()
        search_input.send_keys(termino_busqueda)
        search_input.submit()
        
        wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div/div[1]/div/div/div[1]/main/div/div[2]/div/div/div[1]/div/section/div/div[2]")))
        driver.execute_script("window.scrollBy(0, 800);")
        time.sleep(3)

        productos = driver.find_elements(By.CSS_SELECTOR, "div.flex.flex-wrap.w-100.flex-grow-0.flex-shrink-0.ph2.pr0-xl.pl4-xl.mt0-xl>div")
        
        for p in productos:
            try:
                nombre = p.find_element(By.CSS_SELECTOR, "div.flex.flex-wrap.w-100.flex-grow-0.flex-shrink-0.ph2.pr0-xl.pl4-xl.mt0-xl>div>div>div>div>div>div>span").text
                marca = p.find_element(By.CSS_SELECTOR, "div.mb1.mt2.b.f6.black.mr1.lh-copy").text
                precio = p.find_element(By.CSS_SELECTOR, "div.mr1.mr2-xl.b.black.lh-copy.f5.f4-l").text
                
                if nombre and precio and marca:
                    productos_lista.append({
                        "Nombre": nombre,
                        "Precio": precio.replace('$', '').replace('.', '').strip(),
                        "Marca": marca,
                    })
            except:
                continue 
                
    except Exception as e:
        logging.error(f"Error en scraper.py: {e}")
        
    return productos_lista
# 2. Guardar con Pandas
#if datos:
#    df = pd.DataFrame(datos)
#    print(df.head())
#    df.to_csv("precios_lider.csv", index=False, encoding='utf-8-sig')
#   print("\n¡Archivo guardado exitosamente!")
#else:
#    print("No se encontraron productos.")