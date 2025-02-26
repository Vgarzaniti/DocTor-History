from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import DATABASE_URL

# Crear el motor de conexión
engine = create_engine(DATABASE_URL, echo=True)

# Crear una sesión para interactuar con la BD
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

# Función para obtener la sesión
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
