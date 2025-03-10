import sqlite3
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

# 📌 Přihlašovací údaje (doporučuji uložit je bezpečněji, např. do `.env`)
SEZNAM_EMAIL = "tvuj@email.cz"
SEZNAM_HESLO = "tvojeheslo"

# 📌 Název databázového souboru
DB_FILE = "gptcrap.db"


def setup_database():
    """Vytvoří databázovou tabulku, pokud neexistuje."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS comments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            comment_time TEXT,
            comment_text TEXT,
            article_url TEXT
        )
    ''')
    conn.commit()
    conn.close()


def save_comment(comment_time, comment_text, article_url):
    """Uloží komentář do databáze."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO comments (comment_time, comment_text, article_url) VALUES (?, ?, ?)",
                   (comment_time, comment_text, article_url))
    conn.commit()
    conn.close()


def login_to_seznam(driver):
    """Přihlásí se do Seznam.cz účtu."""
    driver.get("https://login.szn.cz/")
    time.sleep(3)

    # 📌 Přijmout cookies (pokud se zobrazí)
    try:
        cookies_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Přijmout vše')]")
        cookies_button.click()
        print("✅ Cookies přijaty")
        time.sleep(2)
    except:
        print("⏩ Žádné cookies tlačítko nenalezeno")

    # 📌 Najít pole pro e-mail a heslo
    email_input = driver.find_element(By.NAME, "login-username")
    email_input.send_keys(SEZNAM_EMAIL)
    email_input.send_keys(Keys.RETURN)
    time.sleep(2)

    password_input = driver.find_element(By.NAME, "login-password")
    password_input.send_keys(SEZNAM_HESLO)
    password_input.send_keys(Keys.RETURN)
    time.sleep(5)

    print("✅ Přihlášení dokončeno")


def scrape_comments():
    """Přihlásí se, přejde na profil a scrapuje komentáře."""

    # 📌 Spustí Chrome s automatickým WebDriverem
    options = Options()
    options.add_argument("--start-maximized")  # Otevře prohlížeč na celou obrazovku
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    # 📌 Přihlášení do Seznam.cz
    login_to_seznam(driver)

    # 📌 Otevře profil uživatele Miroslava Svobody
    url = "https://www.seznam.cz/profil/miroslav-svoboda-a9b6227c76f3cfca54d8c3ce44cb9d7ec0a87e4ca92950106fe2"
    driver.get(url)

    time.sleep(5)  # Počkej na načtení stránky

    # 📌 Najde všechny komentáře na stránce
    comments = driver.find_elements(By.CLASS_NAME, "comment-container")

    for comment in comments:
        try:
            # 📌 Získání času komentáře
            comment_time = comment.find_element(By.CLASS_NAME, "comment-time").text

            # 📌 Získání obsahu komentáře
            comment_text = comment.find_element(By.CLASS_NAME, "comment-text").text

            # 📌 URL článku, ke kterému byl komentář napsán
            article_url_element = comment.find_element(By.CSS_SELECTOR, ".related-article")
            article_url = article_url_element.get_attribute("href")

            # 📌 Uložení do databáze
            save_comment(comment_time, comment_text, article_url)

            print(f"✅ Uloženo: {comment_time} | {comment_text} | {article_url}")
        except Exception as e:
            print(f"⚠️ Chyba při zpracování komentáře: {e}")

    print("✅ Scrapování dokončeno")
    input("Stiskni ENTER pro ukončení...")  # Nezavře okno hned
    driver.quit()


if __name__ == "__main__":
    setup_database()  # Inicializuje databázi
    scrape_comments()  # Spustí scraper
