import sqlite3


def migrate_database():
    # Připojení k databázi
    conn = sqlite3.connect('comments.db')
    cursor = conn.cursor()

    # Přidání sloupce `author`
    try:
        cursor.execute('ALTER TABLE comments ADD COLUMN author TEXT NOT NULL DEFAULT ""')
        print("Sloupec `author` byl úspěšně přidán.")
    except sqlite3.OperationalError as e:
        print(f"Chyba při migraci: {e}")

    # Uložení změn a uzavření spojení
    conn.commit()
    conn.close()


if __name__ == "__main__":
    migrate_database()