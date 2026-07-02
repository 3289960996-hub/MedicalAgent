from sqlalchemy import Boolean, Column, Float, Integer, String, Text
from sqlalchemy.orm import declarative_base


Base = declarative_base()


class Department(Base):
    __tablename__ = "departments"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), unique=True, nullable=False, index=True)
    description = Column(Text, default="")
    is_active = Column(Boolean, default=True, nullable=False)


class DepartmentLocation(Base):
    __tablename__ = "department_locations"

    id = Column(Integer, primary_key=True, autoincrement=True)
    department = Column(String(100), unique=True, nullable=False, index=True)
    floor = Column(String(50), default="")
    area = Column(String(100), default="")
    room = Column(String(100), default="")
    description = Column(Text, default="")


class Doctor(Base):
    __tablename__ = "doctors"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    title = Column(String(100), default="")
    department = Column(String(100), nullable=False, index=True)
    specialty = Column(Text, default="")
    available = Column(Boolean, default=True, nullable=False)
    time = Column(String(200), default="")
    fee = Column(String(50), default="")
    slots = Column(Integer, default=0)


class SymptomDepartmentRule(Base):
    __tablename__ = "symptom_department_rules"

    id = Column(Integer, primary_key=True, autoincrement=True)
    department = Column(String(100), nullable=False, index=True)
    keywords = Column(Text, nullable=False)
    reason = Column(Text, default="")
    matched_type = Column(String(50), default="rule")
    confidence = Column(String(50), default="medium")
    priority = Column(Integer, default=100, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)


class DiseaseKnowledge(Base):
    __tablename__ = "disease_knowledge"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), unique=True, nullable=False, index=True)
    department = Column(String(100), default="")
    summary = Column(Text, default="")
    red_flags = Column(Text, default="")
    source = Column(String(200), default="mock")


class InspectionSuggestion(Base):
    __tablename__ = "inspection_suggestions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    department = Column(String(100), nullable=False, index=True)
    suggestion = Column(Text, default="")
    risk_level = Column(String(50), default="low")
    confidence = Column(Float, default=0.5)
