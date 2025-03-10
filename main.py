import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from database import Database


def print_menu():
    """Vypíše menu s možnostmi."""
    print("\n" + "=" * 40)
    print(" " * 10 + "HLAVNÍ MENU")
    print("=" * 40)
    print("1: Start scrapování")
    print("2: Vymazat databázi")
    print("3: Vyhledat slovo v databázi")
    print("4: Export do HTML")
    print("5: Konec")
    print("=" * 40)


def scrape_comments(profile_url, headless=False):
    # Nastavení WebDriveru
    options = webdriver.ChromeOptions()
    if headless:
        options.add_argument('--headless')  # Headless režim
    options.add_argument('--disable-gpu')  # Vypni GPU akceleraci
    options.add_argument('--disable-dev-shm-usage')  # Zabrání problémům s pamětí
    driver = webdriver.Chrome(options=options)

    # Přejdeme na profil
    print(f"\nNačítám URL: {profile_url}")
    driver.get(profile_url)
    time.sleep(2)  # Krátká pauza pro načtení stránky

    # Inicializace databáze
    db = Database()

    # Proměnné pro počítadlo
    total_comments = 0  # Celkový počet načtených komentářů
    saved_comments = 0  # Počet uložených komentářů

    # Smyčka pro scrollování a načítání komentářů
    while True:
        try:
            # Načtení komentářů
            comments = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'li .relative.hover\\:bg-gray-100.duration-150'))
            )

            # Pokud jsme načetli všechny komentáře, ukončíme smyčku
            if len(comments) == total_comments:
                print("\nVšechny komentáře byly načteny.")
                break

            # Aktualizace celkového počtu komentářů
            total_comments = len(comments)

            # Uložení komentářů do databáze
            db.conn.execute('BEGIN TRANSACTION')
            for comment in comments[saved_comments:]:  # Ukládáme pouze nové komentáře
                try:
                    # Získání autora
                    author = comment.find_element(By.CSS_SELECTOR,
                                                'a.atm-link.whitespace-nowrap.text-sm.font-bold.hover\\:underline').text
                except:
                    author = "Neznámý autor"

                # Získání datumu
                comment_date = comment.find_element(By.CSS_SELECTOR,
                                                  '.text-xs.block.mt-0\\.5.whitespace-nowrap.text-gray-500').text

                # Získání celého textu komentáře (všechny <p> elementy)
                paragraphs = comment.find_elements(By.CSS_SELECTOR, '.atm-paragraph')
                comment_text = "\n".join([p.text for p in paragraphs])  # Spojení textů všech <p>

                # Získání odkazu na článek (s ošetřením chyby)
                try:
                    article_url = comment.find_element(By.CSS_SELECTOR, '.mol-article-card').get_attribute('href')
                except:
                    article_url = ""  # Pokud odkaz na článek není nalezen

                # Uložení do databáze
                db.insert_comment(comment_date, comment_text, article_url, author)
                saved_comments += 1  # Inkrementace počtu uložených komentářů
                print(f"Uložen komentář {saved_comments}: {comment_text[:50]}... (Autor: {author})")

                # Krátká pauza
                time.sleep(0.3)

            # Potvrzení transakce
            db.commit()

            # Scrollování dolů
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1.2)  # Krátká pauza pro načtení dalších komentářů
        except Exception as e:
            print(f"\nChyba při scrapování: {e}")
            break

    # Uzavření databáze a prohlížeče
    db.close()
    driver.quit()

    # Výpis celkového počtu načtených a uložených komentářů
    print("\n" + "=" * 40)
    print("SCRAPOVÁNÍ DOKONČENO")
    print("=" * 40)
    print(f"Celkem načteno komentářů: {total_comments}")
    print(f"Celkem uloženo komentářů: {saved_comments}")
    print("=" * 40)


if __name__ == "__main__":
    # Inicializace proměnných
    headless = False
    test_url = "https://www.seznam.cz/profil/zdenek-hubner-ba99199f6196f9da54d8c3ce44cb9d7ec0a7774ea42f5e116fec"
    custom_url = ""
    use_test_url = True
    search_results = None  # Uloží výsledky vyhledávání

    # Hlavní smyčka programu
    while True:
        print_menu()
        choice = input("Vyber možnost (1-5): ").strip()

        if choice == "1":
            # Start scrapování
            print("\n" + "=" * 40)
            print("NASTAVENÍ SCRAPOVÁNÍ")
            print("=" * 40)

            # Volba headless módu
            headless_choice = input("Chceš spustit v headless režimu? (ano/ne): ").strip().lower()
            headless = headless_choice == 'ano'

            # Volba URL
            url_choice = input("Chceš použít testovací link? (ano/ne): ").strip().lower()
            if url_choice == 'ano':
                url_to_scrape = test_url
                print(f"Používám testovací link: {test_url}")
            else:
                custom_url = input("Zadej vlastní URL: ").strip()
                url_to_scrape = custom_url
                print(f"Používám zadané URL: {custom_url}")

            # Spuštění scrapování
            print("\nSpouštím scrapování...")
            scrape_comments(url_to_scrape, headless)

        elif choice == "2":
            # Vymazání databáze
            print("\n" + "=" * 40)
            print("VYMAZÁNÍ DATABÁZE")
            print("=" * 40)
            db = Database()
            db.clear_database()
            db.close()
            print("Databáze byla úspěšně vymazána.")

        elif choice == "3":
            # Vyhledat slovo v databázi
            print("\n" + "=" * 40)
            print("VYHLEDÁVÁNÍ KOMENTÁŘŮ")
            print("=" * 40)
            keyword = input("Zadej slovo pro vyhledání: ").strip()
            db = Database()
            search_results = db.search_comments(keyword)  # Uloží výsledky
            db.close()

            if search_results:
                print("\nVýsledky vyhledávání:")
                for id_, date, text, url, author in search_results:
                    print(f"ID: {id_}, Datum: {date}, Autor: {author}, Komentář: {text}, Odkaz: {url}")
            else:
                print("Nebyly nalezeny žádné komentáře obsahující zadané slovo.")

        elif choice == "4":
            # Export do HTML (pouze pokud byly nalezeny výsledky)
            if search_results:
                print("\n" + "=" * 40)
                print("EXPORT DO HTML")
                print("=" * 40)
                db = Database()
                db.export_to_html(search_results)
                db.close()
            else:
                print("\nNejprve musíš provést vyhledání a najít nějaké výsledky.")

        elif choice == "5":
            # Konec programu
            print("\n" + "=" * 40)
            print("UKONČENÍ PROGRAMU")
            print("=" * 40)
            print("Děkuji za použití programu. Ukončuji...")
            break

        else:
            print("\nNeplatná volba. Zadej číslo od 1 do 5.")