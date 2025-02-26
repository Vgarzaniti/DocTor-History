from sqlalchemy import Column, Integer, String, Boolean, Text, ForeignKey, Date
from sqlalchemy.orm import relationship, DeclarativeBase

class Base(DeclarativeBase):
    pass

class ObraSocial(Base):
    __tablename__ = 'obraSocial'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)

    pacientes = relationship('Paciente', back_populates='obraSocial')
    pacientesXObraSocial = relationship('PacienteXObraSocial', back_populates='obraSocial')

class Dbt(Base):
    __tablename__ = 'dbt'
    id = Column(Integer, primary_key=True)
    tipo = Column(Integer, nullable=False)

    antecedentes = relationship('Antecedentes', back_populates='dbt')

class Cardiologico(Base):
    __tablename__ = 'cardiologico'
    id = Column(Integer, primary_key=True)
    arritmia = Column(Boolean, nullable=False)
    iam = Column(Boolean, nullable=False)
    marcapaso = Column(Boolean, nullable=False)
    stent = Column(Boolean, nullable=False)
    otro = Column(Text, nullable=True)  # Puede ser None si no tiene otro problema

    antecedentes = relationship('Antecedentes', back_populates='cardiologico')

class Antecedentes(Base):
    __tablename__ = 'antecedentes'
    id = Column(Integer, primary_key=True)
    hta = Column(Boolean, nullable=False)
    idDbt = Column(Integer, ForeignKey('dbt.id'), nullable=True)
    dislipemia = Column(Boolean, nullable=False)
    hipotiroidismo = Column(Boolean, nullable=False)
    oncologico = Column(Text, nullable=True)
    cirugia = Column(Text, nullable=True)
    otros = Column(Text, nullable=True)
    idCardiologico = Column(Integer, ForeignKey('cardiologico.id'), nullable=True)

    dbt = relationship('Dbt', back_populates='antecedentes')
    cardiologico = relationship('Cardiologico', back_populates='antecedentes')
    paciente = relationship('Paciente', back_populates='antecedentes', uselist=False)

class Paciente(Base):
    __tablename__ = 'paciente'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    apellido = Column(String(100), nullable=False)
    edad = Column(Integer, nullable=False)
    idObraSocial = Column(Integer, ForeignKey('obraSocial.id'), nullable=False)
    idAntecedentes = Column(Integer, ForeignKey('antecedentes.id'), nullable=False)

    obraSocial = relationship('ObraSocial', back_populates='pacientes')
    antecedentes = relationship('Antecedentes', back_populates='paciente', uselist=False)
    consultas = relationship('Consulta', back_populates='paciente')
    pacientesXObraSocial = relationship('PacienteXObraSocial', back_populates='paciente')

class Consulta(Base):
    __tablename__ = 'consulta'
    id = Column(Integer, primary_key=True)
    fecha = Column(Date, nullable=False)
    descripcion = Column(Text, nullable=False)
    idPaciente = Column(Integer, ForeignKey('paciente.id'), nullable=False)

    paciente = relationship('Paciente', back_populates='consultas')
    extras = relationship('ConsultaXExtra', back_populates='consulta')

class Extra(Base):
    __tablename__ = 'extra'
    id = Column(Integer, primary_key=True)
    nombreFarmaco = Column(Text, nullable=False)
    laboratorio = Column(Text, nullable=False)
    estudios = Column(Text, nullable=True)  # Puede no tener estudios asociados

    consultas = relationship('ConsultaXExtra', back_populates='extra')

class ConsultaXExtra(Base):
    __tablename__ = 'consultaXextra'
    id = Column(Integer, primary_key=True)
    idconsulta = Column(Integer, ForeignKey('consulta.id'), nullable=False)
    idextra = Column(Integer, ForeignKey('extra.id'), nullable=False)

    consulta = relationship('Consulta', back_populates='extras')
    extra = relationship('Extra', back_populates='consultas')

class PacienteXObraSocial(Base):
    __tablename__ = 'pacienteXobraSocial'
    id = Column(Integer, primary_key=True)
    numeroObraSocial = Column(String(50), nullable=False)  # Puede ser alfanumérico
    idpaciente = Column(Integer, ForeignKey('paciente.id'), nullable=False)
    idobraSocial = Column(Integer, ForeignKey('obraSocial.id'), nullable=False)

    paciente = relationship('Paciente', back_populates='pacientesXObraSocial')
    obraSocial = relationship('ObraSocial', back_populates='pacientesXObraSocial')
