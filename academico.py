import mysql.connector
import pandas as pd 
from  sqlalchemy import create_engine
import matplotlib.pyplot as plt

conexion = mysql.connector.connect(
    host="localhost",
    port=3306,                      
    user="root",                    
    password="",                    
    database="moduloacademicopi_bd"
)
cursor = conexion.cursor()

cursor.execute("SELECT DATABASE();")
print("BD actual:", cursor.fetchone()[0])

cursor.execute("SHOW TABLES;")  

print("Tablas disponibles:")
for tabla in cursor.fetchall():  
    print("-", tabla[0])

cursor.close()
conexion.close()
print("Conexión cerrada.")

engine = create_engine("mysql+mysqlconnector://root:@localhost:3306/moduloacademicopi_bd")

df_estudiantes = pd.read_sql("SELECT * FROM estudiantes;", engine)
print("Tablas Estudiantes")
print(df_estudiantes.head())    
print(df_estudiantes.columns)


df_materias=pd.read_sql("SELECT * FROM materias;",engine)
print("Tabla  Materias")
print(df_materias.head())
print(df_materias.columns)

df_matriculas=pd.read_sql("SELECT * FROM matriculas;",engine)

print("Tablas Matriculas")
print(df_matriculas.head())
print(df_matriculas.columns)

df_grupos=pd.read_sql("SELECT * FROM grupos;",engine)

print("Tabla Grupos")
print(df_grupos.head())
print(df_grupos.columns)

df_notas=pd.read_sql("SELECT * FROM notas;",engine)

print("Tabla Notas")
print(df_notas.head())
print(df_notas.columns)

df_usuarios=pd.read_sql("SELECT * FROM usuarios;",engine)

print("Tabla Usuarios")
print(df_usuarios.head())
print(df_usuarios.columns)

#Calculos 

reprobados = df_notas[df_notas["valor"] < 3.0]

alertas = reprobados.merge(df_usuarios, left_on="id", right_on="id", how="left")

alertas = alertas.merge(df_materias, left_on="id", right_on="id", how="left", suffixes=('', '_materia'))

alertas["alerta"] = (
    "Alerta: " + alertas["nombre"] +
    " reprobó " + alertas["nombre_materia"] +
    " con nota " + alertas["valor"].astype(str) +
    ". Contactar a: " + alertas["correo"]
)

pd.set_option('display.max_colwidth', None)
print(alertas[["nombre", "nombre_materia", "valor", "correo", "alerta"]])

# Promedio mensual
df_notas["fecha"] = pd.to_datetime(df_notas["fecha"])  # Asegurarnos de que es tipo fecha
df_notas["mes"] = df_notas["fecha"].dt.to_period("M").astype(str)  # Formato YYYY-MM

promedio_mensual = df_notas.groupby("mes")["valor"].mean().reset_index()

print("Promedio de notas por mes:")
print(promedio_mensual)

# Gráfica
plt.figure(figsize=(8, 4))
plt.plot(promedio_mensual["mes"], promedio_mensual["valor"], marker='o', color='teal')
plt.title("Promedio mensual de notas")
plt.xlabel("Mes")
plt.ylabel("Promedio de valor")
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.show()