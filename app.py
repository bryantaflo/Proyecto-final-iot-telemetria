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
    <!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Telemetría de Temperatura</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 40px 20px;
            display: flex;
            justify-content: center;
            align-items: center;
        }

        .container {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 40px;
            max-width: 1200px;
            width: 100%;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            animation: slideIn 0.8s ease-out;
        }

        @keyframes slideIn {
            from {
                opacity: 0;
                transform: translateY(-30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        .header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 30px;
            flex-wrap: wrap;
            gap: 20px;
        }

        h1 {
            color: #2d3748;
            font-size: 2rem;
            font-weight: 700;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }

        .stats {
            display: flex;
            gap: 20px;
            flex-wrap: wrap;
        }

        .stat-item {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 10px 20px;
            border-radius: 12px;
            font-size: 0.9rem;
            font-weight: 600;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
            transition: all 0.3s ease;
        }

        .stat-item:hover {
            transform: translateY(-3px) scale(1.05);
            box-shadow: 0 6px 25px rgba(102, 126, 234, 0.6);
        }

        .stat-item span {
            font-size: 1.2rem;
            margin-right: 5px;
        }

        .table-wrapper {
            overflow-x: auto;
            border-radius: 12px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
        }

        table {
            width: 100%;
            border-collapse: separate;
            border-spacing: 0;
            background: white;
            border-radius: 12px;
            overflow: hidden;
        }

        thead {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }

        th {
            color: white;
            font-weight: 600;
            padding: 18px 20px;
            text-transform: uppercase;
            font-size: 0.85rem;
            letter-spacing: 0.5px;
            position: relative;
            transition: all 0.3s ease;
        }

        th:hover {
            background: rgba(255, 255, 255, 0.1);
            transform: scale(1.02);
        }

        td {
            padding: 16px 20px;
            color: #2d3748;
            font-size: 0.95rem;
            border-bottom: 1px solid #edf2f7;
            transition: all 0.3s ease;
        }

        tr {
            transition: all 0.3s ease;
        }

        tbody tr {
            animation: fadeInRow 0.5s ease-out forwards;
            opacity: 0;
        }

        tbody tr:nth-child(1) { animation-delay: 0.1s; }
        tbody tr:nth-child(2) { animation-delay: 0.2s; }
        tbody tr:nth-child(3) { animation-delay: 0.3s; }
        tbody tr:nth-child(4) { animation-delay: 0.4s; }
        tbody tr:nth-child(5) { animation-delay: 0.5s; }
        tbody tr:nth-child(6) { animation-delay: 0.6s; }
        tbody tr:nth-child(7) { animation-delay: 0.7s; }
        tbody tr:nth-child(8) { animation-delay: 0.8s; }
        tbody tr:nth-child(9) { animation-delay: 0.9s; }
        tbody tr:nth-child(10) { animation-delay: 1.0s; }

        @keyframes fadeInRow {
            from {
                opacity: 0;
                transform: translateX(-20px);
            }
            to {
                opacity: 1;
                transform: translateX(0);
            }
        }

        tbody tr:hover {
            background: linear-gradient(135deg, #f6f8ff 0%, #f0f2ff 100%);
            transform: scale(1.01);
            box-shadow: 0 4px 20px rgba(102, 126, 234, 0.15);
            cursor: pointer;
        }

        tbody tr:last-child td {
            border-bottom: none;
        }

        td:first-child {
            font-weight: 600;
            color: #667eea;
        }

        td:nth-child(2) {
            font-weight: 600;
        }

        td:nth-child(2)::after {
            content: " ";
            font-size: 1rem;
        }

        td:last-child {
            color: #718096;
            font-size: 0.9rem;
        }

        .badge {
            display: inline-block;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.75rem;
            font-weight: 600;
            background: #e2e8f0;
            color: #4a5568;
            transition: all 0.3s ease;
        }

        .badge:hover {
            transform: scale(1.1) rotate(-5deg);
            background: #667eea;
            color: white;
        }

        /* Responsive */
        @media (max-width: 768px) {
            .container {
                padding: 20px;
            }
            
            h1 {
                font-size: 1.5rem;
            }
            
            .header {
                flex-direction: column;
                align-items: flex-start;
            }
            
            .stats {
                width: 100%;
            }
            
            .stat-item {
                flex: 1;
                text-align: center;
                font-size: 0.8rem;
                padding: 8px 15px;
            }
            
            th, td {
                padding: 12px 15px;
                font-size: 0.85rem;
            }
        }

        @media (max-width: 480px) {
            body {
                padding: 10px;
            }
            
            .container {
                padding: 15px;
            }
            
            th, td {
                padding: 10px 12px;
                font-size: 0.75rem;
            }
            
            .stat-item {
                font-size: 0.7rem;
                padding: 6px 12px;
            }
        }

        /* Scrollbar personalizado */
        ::-webkit-scrollbar {
            width: 8px;
            height: 8px;
        }

        ::-webkit-scrollbar-track {
            background: #f1f1f1;
            border-radius: 10px;
        }

        ::-webkit-scrollbar-thumb {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 10px;
        }

        ::-webkit-scrollbar-thumb:hover {
            background: linear-gradient(135deg, #5a67d8 0%, #6b46a1 100%);
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1> Historial de Telemetría </h1>
            <div class="stats">
                <div class="stat-item">
                    <span> </span> Raspberry Pi 3
                </div>
                <div class="stat-item">
                    <span> </span> Última: 23.5 °C
                </div>
                <div class="stat-item">
                    <span> </span> {{ registros|length }} registros
                </div>
            </div>
        </div>

        <div class="table-wrapper">
            <table>
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Temperatura (°C)</th>
                        <th>Fecha y Hora</th>
                    </tr>
                </thead>
                <tbody>
                    {% for reg in registros %}
                    <tr>
                        <td>#{{ reg['id'] }}</td>
                        <td>{{ reg['valor_temperatura'] }}</td>
                        <td>{{ reg['fecha_hora'] }}</td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    </div>
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