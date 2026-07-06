-- Script de creación de BD TEMP 
CREATE TABLE IF NOT EXISTS historial_temperatura (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    valor_temperatura REAL NOT NULL,
    fecha_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);