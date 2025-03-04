from db.models import Paciente, Obrasocial, Pacientexobrasocial
from sqlalchemy.orm import Session

def get_all_pacientes(db: Session):
    try:
        pacientes = db.query(Paciente).join(Paciente.pacientexobrasocial).join(Obrasocial).all()
        return pacientes
    except Exception as e:
        print(f"Error al obtener pacientes: {e}")
        return []
