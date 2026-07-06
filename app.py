from flask import Flask, request, jsonify, render_template_string
import sqlite3

app = Flask(__name__)
DB_NAME = "database.db"

def init_db():
    """Inicializa la base de datos usando el esquema definido."""
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS historial_temperatura (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                valor_temperatura REAL NOT NULL,
                fecha_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        conn.commit()

# Inicializar BD
init_db()

@app.route('/', methods=['GET'])
def index():
    """Ruta principal: Consulta el historial y lo muestra en una vista HTML básica."""
    with sqlite3.connect(DB_NAME) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM historial_temperatura ORDER BY fecha_hora DESC")
        registros = cursor.fetchall()
    
    # HTML embebido básico para previsualización 
    html_template = """
    <!... html ...>
    <html>
    <head>
        <title>Telemetría de Temperatura</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background-color: #f4f6f9; }
            table { width: 100%; border-collapse: collapse; margin-top: 20px; background: white; }
            th, td { padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }
            th { background-color: #0052cc; color: white; }
        </style>
    </head>
    <body>
        <h1>Historial de Telemetría (Raspberry Pi 3)</h1>
        <table>
            <tr>
                <th>ID</th>
                <th>Temperatura (°C)</th>
                <th>Fecha y Hora</th>
            </tr>
            {% for reg in registros %}
            <tr>
                <td>{{ reg['id'] }}</td>
                <td>{{ reg['valor_temperatura'] }} °C</td>
                <td>{{ reg['fecha_hora'] }}</td>
            </tr>
            {% endfor %}
        </table>
    </body>
    </html>
    """
    return render_template_string(html_template, registros=registros)

@app.route('/api/temperatura', methods=['POST'])
def registrar_temperatura():
    """Endpoint REST para recibir los datos JSON enviados por la Raspberry Pi."""
    data = request.get_json()
    
    if not data or 'temperatura' not in data:
        return jsonify({"error": "Bad Request", "message": "Falta el parámetro 'temperatura'"}), 400
    
    val_temp = data['temperatura']
    
    try:
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO historial_temperatura (valor_temperatura) VALUES (?)",
                (val_temp,)
            )
            conn.commit()
        return jsonify({"status": "Created", "message": "Métrica persistida con éxito"}), 201
    except Exception as e:
        return jsonify({"error": "Internal Server Error", "message": str(e)}), 500

if __name__ == '__main__':
    
    app.run(host='0.0.0.0', port=5000, debug=True)