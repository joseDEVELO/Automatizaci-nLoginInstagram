from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions  import  TimeoutException
from credenciales import *
import time
import pickle
import os 

def iniciar_chrome():

    ruta = ChromeDriverManager(path="./chromedriver").install()

    options = Options()
    user_agent = "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Mobile Safari/537.36"

    options.add_argument(user_agent)
    options.add_argument("--start-maximized")
    options.add_argument("--disable-web-security")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-notifications")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--no-sandbox")
    options.add_argument("--log-level=3")
    options.add_argument("--allow-runing-insecure-content")
    options.add_argument("--no-default-browser-check")
    options.add_argument("--no-first-run")
    options.add_argument("--no-proxy-server")
    options.add_argument("--disable-blink-features=AutomationControlled") 

    # Parametro a omitir en el inicio de Chrome
    exp_opt = [
        'enable-automation'
        'ignore-certificate-errors'
        'enable-logging'
     ]
    options.add_experimental_option("excludeSwitches", exp_opt)

    # Parametros de preferencias
    # preferencias = {
    #     'profile.default_content_setting_values.notifications' : 2,
    #     'intl.accept_languages' : ["es-ES", "es"],
    #     'credentials_enable_service': False
    # }

    # options.add_experimental_option("preferencias", preferencias)

    s = Service(ruta)
    driver = webdriver.Chrome(service=s, options=options)
    
    return driver

def login():
    if os.path.isfile("instagram.cookies"):
    # cargamos  robots.txt del dominion de instagram.com
        cookies = pickle.load(open("instagram.cookies", "rb"))
        driver.get("https://www.instagram.com/robots.txt")
    #recorremos el objeto cookies y las añadimos al driver
        for cookie in cookies:
            driver.add_cookie(cookie)
    # Comprobamos si el lokin por cookies funciona
        driver.get("https://www.instagram.com/")
    try:
        article = wait.until(ec.element_to_be_clickable((By.CSS_SELECTOR, "article[role='presentation']")))
        print ("todo OK desde las cookies")
        return "OK"
    except TimeoutException:
        print( 'ERROR: elemento no se encuentra')
        return "ERROR"

    driver.get("https://www.instagram.com/")
    try:
        el = wait.until(ec.visibility_of_element_located((By.NAME, "username")))
    except TimeoutException:
        print( 'ERROR: elemento "username" no disponible')
        return "ERROR"
    el.send_keys(USER_IG)
    ps = wait.until(ec.visibility_of_element_located((By.NAME, "password")))
    ps.send_keys(PASS_IG)
    # btn = driver.find_elements(By.CSS_SELECTOR, "button[type='submit']")
    # btn = wait.until(ec.visibility_of_element_located((By.CSS_SELECTOR, "button[type='submit']")))
    
    btn = wait.until(ec.element_to_be_clickable((By.XPATH, "//div[contains(text(),'Entrar')]")))
    btn.click()
    # Cerrar modal de ¿Guardar tu información de inicio de sesión?

    guardarSesion = wait.until(ec.element_to_be_clickable((By.XPATH, "//button[(text()='Guardar información')]")))
    guardarSesion.click()

    try:
        article = wait.until(ec.element_to_be_clickable((By.CSS_SELECTOR, "article[role='presentation']")))
        print ("OK")
    except TimeoutException:
        print( 'ERROR: elemento no se encuentra')
        return "ERROR"
    # guardamos las cookies con picke
    cookies = driver.get_cookies()
    pickle.dump(cookies, open("instagram.cookies", "wb"))
    print(" cookies guardadas ")
    return "ok"

if __name__ == '__main__':
    driver = iniciar_chrome()
    wait = WebDriverWait(driver, 10)
    login = login()
    if login == "ERROR":
       input("Pulsa ENTER para salir")
       driver.quit()
    input("Pulsa ENTER para salir")
    driver.quit()
    