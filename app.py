from flask import Flask, send_file
from flask_cors import CORS
import io
import matplotlib.pyplot as plt
import mysql.connector
import pandas as pd
from sqlalchemy import create_engine

app = Flask(__name__)
CORS(app)  # permite acceso desde React

@app.route("/api/grafica-promedio")
def grafica_promedio():
    # Conexión a la base de datos
    conexion = mysql.connector.connect(
        host="localhost",
        port=3306,
        user="root",
        password="",
        database="moduloacademicopi_bd"
    )
    cursor = conexion.cursor()
    cursor.close()
    conexion.close()

    engine = create_engine("mysql+mysqlconnector://root:@localhost:3306/moduloacademicopi_bd")

    df_notas = pd.read_sql("SELECT * FROM notas;", engine)

    # --- Cálculos ---
    df_notas["fecha"] = pd.to_datetime(df_notas["fecha"])
    df_notas["mes"] = df_notas["fecha"].dt.to_period("M").astype(str)
    promedio_mensual = df_notas.groupby("mes")["valor"].mean().reset_index()

    # --- Gráfica ---
    plt.figure(figsize=(8, 4))
    plt.plot(promedio_mensual["mes"], promedio_mensual["valor"], marker='o', color='teal')
    plt.title("Promedio mensual de notas")
    plt.xlabel("Mes")
    plt.ylabel("Promedio de valor")
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()

    # --- Convertir la gráfica a imagen en memoria ---
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()
    return send_file(img, mimetype='image/png')

if __name__ == "__main__":
    app.run(port=5001, debug=True) 
    
