# Návod k použití Scrapovacího projektu

## 1. Instalace potřebných závislostí

Pro spuštění projektu je potřeba nainstalovat Python balíčky. Použijte následující příkaz:

```bash
pip install -r requirements.txt
```

Pokud soubor `requirements.txt` neexistuje, můžete ho vygenerovat pomocí:

```bash
pip freeze > requirements.txt
```

---

## 2. Spuštění projektu

Projekt můžete spustit pomocí následujícího příkazu:

```bash
python main.py
```

Po spuštění se zobrazí menu s možnostmi:

1. **Start scrapování** – Spustí scrapování komentářů.
2. **Vymazat databázi** – Vymaže všechna data z databáze.
3. **Vyhledat slovo v databázi** – Vyhledá komentáře obsahující zadané slovo.
4. **Export do HTML** – Exportuje výsledky do HTML souboru.
5. **Konec** – Ukončí program.

---

## 3. Spuštění projektu v PyCharmu

1. **Otevření projektu**
   - Spusťte **PyCharm** a otevřete složku s projektem.

2. **Vytvoření virtuálního prostředí** (doporučeno)
   - Otevřete **Terminal** v PyCharmu a spusťte:
     
     ```bash
     python -m venv venv
     ```
   - Aktivujte virtuální prostředí:
     - **Windows:**
       ```bash
       venv\Scripts\activate
       ```
     - **Mac/Linux:**
       ```bash
       source venv/bin/activate
       ```
   - Nainstalujte závislosti:
     ```bash
     pip install -r requirements.txt
     ```

3. **Nastavení běhové konfigurace**
   - Klikněte na **Run → Edit Configurations...**
   - Klikněte na **+** a vyberte **Python**.
   - V poli **Script path** vyberte `main.py`.
   - Uložte nastavení a spusťte projekt tlačítkem **Run**.

---

## 4. Požadavky na systém

- Python **3.7** nebo novější.
- Knihovna `selenium` pro scrapování.
- WebDriver pro Chrome (musí být nainstalován a přístupný v PATH).

---

## 5. Kontakt

Pokud máte jakékoli dotazy nebo potřebujete pomoc, neváhejte mě kontaktovat na [vas@email.cz](mailto:vas@email.cz).

