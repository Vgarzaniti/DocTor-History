from db.connection import engine

try:
    with engine.connect() as connection:
        print("✅ Conexión a la base de datos exitosa")
except Exception as e:
    print("❌ Error al conectar a la base de datos:", e)
