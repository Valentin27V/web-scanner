from flask import Flask, request
import mysql.connector

app = Flask(__name__)

# CONFIGURARE BAZA DE DATE
# (Aceleași setări ca la Java/DBngin)
db_config = {
    'user': 'root',
    'password': '',        # DBngin de obicei nu are parolă pe root
    'host': '127.0.0.1',
    'database': 'disertatie_db',
    'port': 3306
}

@app.route('/api/login-vulnerabil', methods=['GET'])
def login():
    # 1. Luăm datele din URL (echivalentul @RequestParam din Java)
    user_input = request.args.get('user')
    pass_input = request.args.get('pass')

    try:
        # 2. Ne conectăm la baza de date
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)

        # 3. VULNERABILITATEA MAJORA (SQL Injection)
        # Folosim "f-string" pentru a lipi textul direct in comanda.
        # NU facem nicio verificare!
        sql_query = f"SELECT * FROM users WHERE username = '{user_input}' AND password = '{pass_input}'"
        
        print(f"Execut comanda SQL: {sql_query}") # Vedem in consola ce se intampla

        # 4. Executăm comanda
        cursor.execute(sql_query)
        account = cursor.fetchone()

        # Închidem conexiunea
        cursor.close()
        conn.close()

        # 5. Verificăm dacă am găsit utilizatorul
        if account:
            return f"LOGIN REUSIT! Ai intrat ca: {account['username']}"
        else:
            return "Login esuat!"

    except Exception as e:
        return f"Eroare server: {e}"

if __name__ == '__main__':
    # Pornim serverul pe portul 5000
    app.run(debug=True, port=5000)