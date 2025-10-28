Documentación del Proyecto en Python
Proyecto: Análisis Académico con MySQL y Python
1. Descripción General
Este proyecto tiene como objetivo conectar un programa en Python con una base de datos MySQL llamada 'moduloacademicopi_bd', para extraer información de diferentes tablas académicas (como estudiantes, materias, notas, usuarios, etc.), realizar cálculos estadísticos (como el promedio mensual de notas) y visualizar los resultados mediante una gráfica generada con la librería Matplotlib.
2. Librerías Utilizadas
• mysql.connector: Permite la conexión directa entre Python y MySQL.
• pandas: Facilita la manipulación y análisis de datos mediante estructuras tipo DataFrame.
• sqlalchemy: Crea un motor de conexión más flexible para leer datos de MySQL con pandas.
• matplotlib.pyplot: Se utiliza para generar gráficos y visualizar datos.
3. Conexión con la Base de Datos
La primera parte del código establece la conexión con la base de datos MySQL utilizando la librería mysql.connector. Aquí se definen los parámetros de conexión como el host, puerto, usuario, contraseña y nombre de la base de datos.

conexion = mysql.connector.connect(
    host="localhost",
    port=3306,
    user="root",
    password="",
    database="moduloacademicopi_bd”)

4. Conexión Alternativa con SQLAlchemy
Después se crea una conexión usando SQLAlchemy, que permite trabajar más fácilmente con pandas mediante un motor de conexión.
engine = create_engine("mysql+mysqlconnector://root:@localhost:3306/moduloacademicopi_bd")
5. Cálculos y Análisis de Datos
Se realizan operaciones con pandas para identificar estudiantes reprobados y calcular el promedio mensual de notas.
Primero se filtran las notas menores a 3.0, luego se unen las tablas de usuarios y materias para obtener información adicional. Después se crean alertas personalizadas para cada estudiante reprobado.
Para calcular el promedio mensual, se convierte la columna de fecha en tipo datetime, se extrae el mes y se agrupan los valores para calcular el promedio mensual de las notas.
6. Visualización de Datos (Gráfica)
Finalmente, se genera una gráfica de línea con Matplotlib que muestra la evolución del promedio mensual de notas. Esta gráfica permite analizar las tendencias del rendimiento académico.
7. Conclusiones
• Se logró conectar Python con MySQL utilizando mysql.connector y SQLAlchemy.
• Se extrajeron y analizaron los datos de las tablas del sistema académico.
• Se identificaron los estudiantes reprobados con alertas personalizadas.
• Se calcularon los promedios mensuales de notas y se visualizaron con un gráfico claro.
• El uso de pandas y matplotlib permitió un análisis rápido y visualmente comprensible.

Documentación Técnica –Generación de gráfica de promedios mensual con Python y Front-end
Descripción general
Este modulo implementa un servidor backend en Python usando Flask, el cual se conecta a una base de datos MySQL, procesa los datos de las notas académicas, calcula el promedio mensual de las calificaciones con Pandas, genera una gráfica estadística con Matplotlib y la envía como imagen  en formato png al frontend (React) mediante una ruta API (/api/grafica-promedio).
Está diseñado para integrarse con un frontend desarrollado en React, permitiendo que este último consuma la ruta /api/grafica-promedio y visualice la gráfica directamente.
1 .Librerias Utilizadas :
Flask:  Framework web liviano para crear APIs y servidores HTTP en Python.
Flask-CORS:Permite que el frontend (React) acceda al backend evitando bloqueos de CORS.
Matplotlib:Biblioteca para la creación de graficos y visualizaciones.
MySQL Connector:Controlador que permite la conexion directa con bases de datos MY SQL.
Pandas : Biblioteca que permite manipular y analizar los datos.
IO (BytesIO):Permite manejar archivos en memoria sin necesidad de guardarlos físicamente.
SQLAlchemy:Herramienta ORM y conector flexible para acceder a bases de datos.
ORM ¿Que es ?
Una herramienta ORM (Object Relacional Mapper ) es una biblioteca que permite a los desarrolladores interactuar con bases de datos relacionales utilizando objetos de Python en lugar de escribir SQL directamente.
2 . Importaciones :
from flask import Flask, send_file
from flask_cors import CORS
import io
import matplotlib.pyplot as plt
import mysql.connector
import pandas as pd
from sqlalchemy import create_engine

Estas importaciones cargan las librerías necesarias para:
Crear el servidor Flask.
Habilitar peticiones desde el frontend (CORS).
Conectarse a MySQL.
Procesar datos y generar gráficos.

3 .Inicialización de la Aplicación
app = Flask(__name__)
CORS(app)
Flask(__name__): crea la aplicación principal.
CORS(app): permite que React (u otro frontend) haga peticiones sin ser bloqueado por políticas de seguridad del navegador.
Ruta Principal del API
@app.route("/api/grafica-promedio")def grafica_promedio():
Define una ruta HTTP GET que devolverá la gráfica en formato de imagen PNG cuando sea llamada desde el frontend.

4 .Conexión a la Base de Datos
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
Este bloque verifica la conexión con la base de datos moduloacademicopi_bd.
Luego, la conexión se cierra, ya que el acceso real a los datos se realiza mediante SQLAlchemy.
5 . Conexión con SQLAlchemy y Carga de Datos
engine = create_engine("mysql+mysqlconnector://root:@localhost:3306/moduloacademicopi_bd")
df_notas = pd.read_sql("SELECT * FROM notas;", engine)
create_engine() crea una conexión tipo “motor” a la base de datos.
pd.read_sql() ejecuta la consulta SQL y carga el resultado como un DataFrame de Pandas.
Resultado:
Una tabla en memoria llamada df_notas, con columnas como id, valor, fecha, etc.

6 .Procesamiento de Datos
df_notas["fecha"] = pd.to_datetime(df_notas["fecha"])
df_notas["mes"] = df_notas["fecha"].dt.to_period("M").astype(str)
promedio_mensual = df_notas.groupby("mes")["valor"].mean().reset_index()
1 .Convierte la columna fecha al tipo de dato fecha.
2 .Crea una nueva columna mes (formato “AÑO-MES”).
3 .Agrupa los registros por mes y calcula el promedio de la columna valor.
El resultado es un nuevo DataFrame:
                       MES	                VALOR
2025-09	     3.4 promedio mensual 
2025-10	     3.8 promedio mensual

7 .Generación de la Gráfica
plt.figure(figsize=(8, 4))
plt.plot(promedio_mensual["mes"], promedio_mensual["valor"], marker='o', color='teal')
plt.title("Promedio mensual de notas")
plt.xlabel("Mes")
plt.ylabel("Promedio de valor")
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
Crea una gráfica de líneas mostrando cómo varía el promedio mensual de las notas.
Se configuran títulos, ejes, rotación y estilo visual.

8 .Conversión de la Gráfica a Imagen
img = io.BytesIO()
plt.savefig(img, format='png')
img.seek(0)
plt.close()return send_file(img, mimetype='image/png')
 return send_file(img, mimetype='image/png')
Guarda la gráfica en memoria en formato PNG.
send_file() envía la imagen como respuesta HTTP.
Esto permite al front-end mostrar la imagen directamente, por ejemplo con:
<img src="http://localhost:5001/api/grafica-promedio" alt="Gráfica de Promedios" />

9 .Ejecución del Servidor
if __name__ == "__main__":
    app.run(port=5001, debug=True)
Inicia el servidor en el puerto 5001.
El modo debug=True reinicia automáticamente el servidor si se detectan cambios en el código.
Visualización de Gráfica :
Conclusión:
En conclusión, este desarrollo demuestra la efectividad de combinar Flask, MySQL, Pandas y Matplotlib para crear un backend sólido, capaz de analizar datos académicos y generar visualizaciones dinámicas que se integran fácilmente con un frontend en React.
La solución propuesta no solo cumple con los objetivos de conexión y visualización, sino que también presenta una estructura escalable, reutilizable y apta para futuras implementaciones. Este tipo de integración permite fortalecer la comunicación entre los distintos componentes del sistema, optimizando el flujo de información y la presentación de resultados de manera clara e interactiva.