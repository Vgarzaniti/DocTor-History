from typing import List

from sqlalchemy import Boolean, Date, ForeignKeyConstraint, Integer, PrimaryKeyConstraint, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
import datetime

class Base(DeclarativeBase):
    pass


class Cardiologico(Base):
    __tablename__ = 'cardiologico'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='cardiologico_pkey'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    arritmia: Mapped[bool] = mapped_column(Boolean)
    iam: Mapped[bool] = mapped_column(Boolean)
    marcapaso: Mapped[bool] = mapped_column(Boolean)
    stent: Mapped[bool] = mapped_column(Boolean)
    otro: Mapped[str] = mapped_column(Text)

    antecedentes: Mapped[List['Antecedentes']] = relationship('Antecedentes', back_populates='cardiologico')


class Dbt(Base):
    __tablename__ = 'dbt'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='dbt_pkey'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    tipo: Mapped[int] = mapped_column(Integer)

    antecedentes: Mapped[List['Antecedentes']] = relationship('Antecedentes', back_populates='dbt')


class Extra(Base):
    __tablename__ = 'extra'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='extra_pkey'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombrefarmaco: Mapped[str] = mapped_column(Text)
    laboratorio: Mapped[str] = mapped_column(Text)
    estudios: Mapped[str] = mapped_column(Text)

    consultaxextra: Mapped[List['Consultaxextra']] = relationship('Consultaxextra', back_populates='extra')


class Obrasocial(Base):
    __tablename__ = 'obrasocial'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='obrasocial_pkey'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100))

    pacientexobrasocial: Mapped[List['Pacientexobrasocial']] = relationship('Pacientexobrasocial', back_populates='obrasocial')


class Antecedentes(Base):
    __tablename__ = 'antecedentes'
    __table_args__ = (
        ForeignKeyConstraint(['idcardiologico'], ['cardiologico.id'], ondelete='SET NULL', name='fk_antecedentes_cardiologico'),
        ForeignKeyConstraint(['iddbt'], ['dbt.id'], ondelete='SET NULL', name='fk_antecedentes_dbt'),
        PrimaryKeyConstraint('id', name='antecedentes_pkey')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    hta: Mapped[bool] = mapped_column(Boolean)
    iddbt: Mapped[int] = mapped_column(Integer)
    dislipemia: Mapped[bool] = mapped_column(Boolean)
    hipotiroidismo: Mapped[bool] = mapped_column(Boolean)
    oncologico: Mapped[str] = mapped_column(Text)
    cirugia: Mapped[str] = mapped_column(Text)
    otros: Mapped[str] = mapped_column(Text)
    idcardiologico: Mapped[int] = mapped_column(Integer)

    cardiologico: Mapped['Cardiologico'] = relationship('Cardiologico', back_populates='antecedentes')
    dbt: Mapped['Dbt'] = relationship('Dbt', back_populates='antecedentes')
    paciente: Mapped[List['Paciente']] = relationship('Paciente', back_populates='antecedentes')


class Paciente(Base):
    __tablename__ = 'paciente'
    __table_args__ = (
        ForeignKeyConstraint(['idantecedentes'], ['antecedentes.id'], ondelete='SET NULL', name='fk_paciente_antecedentes'),
        PrimaryKeyConstraint('id', name='paciente_pkey')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100))
    apellido: Mapped[str] = mapped_column(String(100))
    edad: Mapped[int] = mapped_column(Integer)
    idantecedentes: Mapped[int] = mapped_column(Integer)

    antecedentes: Mapped['Antecedentes'] = relationship('Antecedentes', back_populates='paciente')
    consulta: Mapped[List['Consulta']] = relationship('Consulta', back_populates='paciente')
    pacientexobrasocial: Mapped[List['Pacientexobrasocial']] = relationship('Pacientexobrasocial', back_populates='paciente')


class Consulta(Base):
    __tablename__ = 'consulta'
    __table_args__ = (
        ForeignKeyConstraint(['idpaciente'], ['paciente.id'], ondelete='SET NULL', name='fk_consulta_paciente'),
        PrimaryKeyConstraint('id', name='consulta_pkey')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    fecha: Mapped[datetime.date] = mapped_column(Date)
    descripcion: Mapped[str] = mapped_column(Text)
    idpaciente: Mapped[int] = mapped_column(Integer)

    paciente: Mapped['Paciente'] = relationship('Paciente', back_populates='consulta')
    consultaxextra: Mapped[List['Consultaxextra']] = relationship('Consultaxextra', back_populates='consulta')


class Pacientexobrasocial(Base):
    __tablename__ = 'pacientexobrasocial'
    __table_args__ = (
        ForeignKeyConstraint(['idobrasocial'], ['obrasocial.id'], name='pacientexobrasocial_idobrasocial_fkey'),
        ForeignKeyConstraint(['idpaciente'], ['paciente.id'], name='pacientexobrasocial_idpaciente_fkey'),
        PrimaryKeyConstraint('id', name='pacientexobrasocial_pkey')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    numeroobrasocial: Mapped[int] = mapped_column(Integer)
    idpaciente: Mapped[int] = mapped_column(Integer)
    idobrasocial: Mapped[int] = mapped_column(Integer)

    obrasocial: Mapped['Obrasocial'] = relationship('Obrasocial', back_populates='pacientexobrasocial')
    paciente: Mapped['Paciente'] = relationship('Paciente', back_populates='pacientexobrasocial')


class Consultaxextra(Base):
    __tablename__ = 'consultaxextra'
    __table_args__ = (
        ForeignKeyConstraint(['idconsulta'], ['consulta.id'], name='consultaxextra_idconsulta_fkey'),
        ForeignKeyConstraint(['idextra'], ['extra.id'], name='consultaxextra_idextra_fkey'),
        PrimaryKeyConstraint('id', name='consultaxextra_pkey')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    idconsulta: Mapped[int] = mapped_column(Integer)
    idextra: Mapped[int] = mapped_column(Integer)

    consulta: Mapped['Consulta'] = relationship('Consulta', back_populates='consultaxextra')
    extra: Mapped['Extra'] = relationship('Extra', back_populates='consultaxextra')
