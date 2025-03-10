from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

# Automatická instalace driveru
driver = webdriver.Chrome()

# Otevře webovou stránku
driver.get("https://www.google.com")

# Počkej pár sekund, ať vidíš, že se okno otevře (volitelné)
import time
time.sleep(5)

# Zavře prohlížeč
driver.quit()
