from selenium.webdriver.common.by import By
import time

def accept_cookies(driver):
    """
    Odklikne cookie souhlas, pokud se objeví.
    """
    try:
        # Najde tlačítko pro přijetí cookies
        cookie_button = driver.find_element(By.CSS_SELECTOR, 'button#CybotCookiebotDialogBodyButtonAccept')
        cookie_button.click()
        print("Cookies accepted.")
    except Exception as e:
        print("Cookie consent not found or already accepted.")

def close_login_popup(driver):
    """
    Zavře přihlašovací pop-up, pokud se objeví.
    """
    try:
        # Najde tlačítko pro zavření pop-up okna
        close_button = driver.find_element(By.CSS_SELECTOR, 'button.modal-close')  # Uprav selektor podle potřeby
        close_button.click()
        print("Login pop-up closed.")
    except Exception as e:
        print("Login pop-up not found or already closed.")

def login_to_seznam(driver, email, password):
    """
    Přihlásí uživatele do Seznam.cz.
    """
    try:
        # Klikne na tlačítko "Přihlásit se"
        login_button = driver.find_element(By.CSS_SELECTOR, 'a[href="https://login.szn.cz/"]')
        login_button.click()
        time.sleep(3)  # Počkáme na načtení přihlašovací stránky

        # Vyplní e-mail
        email_input = driver.find_element(By.CSS_SELECTOR, 'input[name="email"]')
        email_input.send_keys(email)
        time.sleep(1)

        # Vyplní heslo
        password_input = driver.find_element(By.CSS_SELECTOR, 'input[name="password"]')
        password_input.send_keys(password)
        time.sleep(1)

        # Klikne na tlačítko "Přihlásit se"
        submit_button = driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
        submit_button.click()
        time.sleep(5)  # Počkáme na dokončení přihlášení

        print("Login successful.")
    except Exception as e:
        print(f"Login failed: {e}")