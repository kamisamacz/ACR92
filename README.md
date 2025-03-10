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

### Jak funguje menu

- Po zadání čísla odpovídající možnosti v menu a stisknutí **Enter** program provede zvolenou akci.
- **Start scrapování** zahájí proces stahování dat z předem definovaného zdroje.
- **Vymazání databáze** nenávratně odstraní všechna uložená data.
- **Vyhledání slova v databázi** umožňuje uživateli zadat klíčové slovo a získat odpovídající výsledky.
- **Export do HTML** uloží výstup do souboru ve formátu HTML pro snadné prohlížení.
- **Konec** ukončí program a zavře všechny procesy.

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
- Chrome

---
## 5. Postup řešení

Jelikož jediný programovací jazyk, který momentálně ovládám, je Python, byla jeho volba jasná.
Bohužel, po přibližně třech měsících kurzu mé znalosti stále nejsou dostatečné, a proto jsem se
velmi často radil s AI. Z dřívějších rozhovorů s bratrem, který mi kdysi popisoval svou práci
junior testera webových aplikací, jsem měl základní představu, jak postupovat.
Hned mi bylo jasné, že pro tuto úlohu bude dostačující kombinace Python, Selenium a ChromeDriver.
Sice toto řešení pravděpodobně není nejrychlejší, protože simuluje chování uživatele na webové stránce,
ale pro mé potřeby bylo dostačující.

Jak program funguje

Po proklikaní jednoduchého menu se spustí proces zachytávání komentářů. Tento proces může běžet
na pozadí nebo ve viditelném okně, kde lze sledovat, jak Python pomocí Selenia ovládá webový prohlížeč.
Pomocí zobrazení zdrojového kódu jsem dohledal selektory, které jsou jedinečné pro:

komentář,autora,odkaz na článek, kde byl komentář zveřejněn.

Tyto zachycené údaje se následně ukládají do databáze, kde lze vyhledávat fráze a exportovat
komentáře do HTML souboru.

Snažil jsem se kód optimalizovat pro rychlejší scrapování, ale ukázalo se, že bez hlubších znalostí
optimalizace začne zachytávání komentářů padat. Aplikace si pak myslí, že získala všechny komentáře,
ve skutečnosti ale může obsahovat například jen 15 % skutečného obsahu.

V budoucnu bych rád přišel na způsob, jak tento proces urychlit a zpřesnit.



---

## 6. Kontakt

Pokud máte jakékoli dotazy nebo potřebujete pomoc, neváhejte mě kontaktovat na [kamisamacz@gmail.com](kamisamacz@gmail.com).

