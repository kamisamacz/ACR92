import sqlite3
import webbrowser
import os


class Database:
    def __init__(self):
        self.db_file = 'comments.db'
        self.conn = sqlite3.connect(self.db_file)

        # Optimalizace pro HDD
        self.conn.execute('PRAGMA journal_mode = WAL')  # Použij WAL režim
        self.conn.execute('PRAGMA synchronous = NORMAL')  # Vypni plnou synchronizaci
        self.conn.execute('PRAGMA cache_size = -10000')  # Zvětš cache na 10 MB

        self.create_table()

    def create_table(self):
        """Vytvoří tabulku `comments`, pokud neexistuje."""
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS comments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                comment_date TEXT NOT NULL,
                comment_text TEXT NOT NULL,
                article_url TEXT NOT NULL,
                author TEXT NOT NULL
            )
        ''')
        self.conn.commit()

    def insert_comment(self, comment_date, comment_text, article_url, author):
        """Vloží komentář do databáze."""
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO comments (comment_date, comment_text, article_url, author)
            VALUES (?, ?, ?, ?)
        ''', (comment_date, comment_text, article_url, author))

    def clear_database(self):
        """Vymaže všechna data z tabulky `comments` a resetuje ID."""
        cursor = self.conn.cursor()
        cursor.execute('DELETE FROM comments')  # Vymaže všechny záznamy
        cursor.execute('DELETE FROM sqlite_sequence WHERE name="comments"')  # Resetuje ID
        self.conn.commit()
        print("Databáze byla vymazána a ID resetováno.")

    def search_comments(self, keyword):
        """Vyhledá komentáře obsahující zadané slovo."""
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT id, comment_date, comment_text, article_url, author
            FROM comments
            WHERE comment_text LIKE ?
        ''', (f'%{keyword}%',))
        return cursor.fetchall()

    def export_to_html(self, comments, filename='export.html'):
        """Exportuje výsledky do HTML souboru a otevře ho v prohlížeči."""
        # Přepsání souboru, pokud existuje
        if os.path.exists(filename):
            print(f"Soubor {filename} bude přepsán.")

        html_content = """
        <!DOCTYPE html>
        <html lang="cs">
        <head>
            <meta charset="UTF-8">
            <title>Export komentářů</title>
            <style>
                table {
                    width: 100%;
                    border-collapse: collapse;
                }
                table, th, td {
                    border: 1px solid black;
                }
                th, td {
                    padding: 8px;
                    text-align: left;
                }
                th {
                    background-color: #f2f2f2;
                }
            </style>
        </head>
        <body>
            <h1>Export komentářů</h1>
            <table>
                <tr>
                    <th>ID</th>
                    <th>Datum zveřejnění</th>
                    <th>Autor</th>
                    <th>Komentář</th>
                    <th>Odkaz na článek</th>
                </tr>
        """

        for comment in comments:
            id_, date, text, url, author = comment  # Rozbalení všech hodnot
            # Nahrazení nových řádků za <br> pro HTML
            text = text.replace('\n', '<br>')
            html_content += f"""
                <tr>
                    <td>{id_}</td>
                    <td>{date}</td>
                    <td>{author}</td>
                    <td>{text}</td>
                    <td><a href="{url}" target="_blank">{url}</a></td>
                </tr>
            """

        html_content += """
            </table>
        </body>
        </html>
        """

        # Uložení do souboru
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(html_content)
        print(f"Data byla exportována do souboru {filename}.")

        # Otevření souboru v prohlížeči
        webbrowser.open(f'file://{os.path.abspath(filename)}')

    def commit(self):
        """Potvrdí všechny změny v databázi."""
        self.conn.commit()

    def close(self):
        """Uzavře spojení s databází."""
        self.conn.close()