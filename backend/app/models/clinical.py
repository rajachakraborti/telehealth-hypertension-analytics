from sqlalchemy import Column, Integer, String, Date, ForeignKey, Float, Boolean, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.types import TypeDecorator, String as SQLString
from sqlalchemy.sql import func
from app.db.database import Base
import os

# The encryption key should be loaded securely from environment variables in production
# This satisfies HIPAA § 164.312(c/e) (Data Encryption at Rest)
PGP_KEY = os.getenv("PGP_SYMMETRIC_KEY", "telehealth_secure_key_2026")

class PGPString(TypeDecorator):
    """
    Custom SQLAlchemy Type that seamlessly encrypts/decrypts strings at the PostgreSQL 
    database level using the pgcrypto extension. 
    This guarantees that PHI (Protected Health Information) is never stored in plain-text.
    """
    impl = SQLString
    cache_ok = True

    def bind_expression(self, bindvalue):
        # Wraps the insert/update value in pgp_sym_encrypt
        return func.pgp_sym_encrypt(bindvalue, PGP_KEY)

    def column_expression(self, col):
        # Wraps the select query in pgp_sym_decrypt
        return func.pgp_sym_decrypt(col, PGP_KEY).cast(SQLString)

class Patient(Base):
    __tablename__ = 'patients'

    id = Column(Integer, primary_key=True, index=True)
    
    # Encrypted PHI Fields
    first_name = Column(PGPString, nullable=False)
    last_name = Column(PGPString, nullable=False)
    ssn_last_four = Column(PGPString, nullable=False)
    contact_email = Column(PGPString, nullable=False, unique=True)
    
    # Non-PHI Clinical/Demographic Fields (Plain-text for indexing/filtering)
    date_of_birth = Column(Date, nullable=False)
    assigned_clinician_id = Column(Integer, ForeignKey('users.id'), index=True)
    
    # Relationships
    telemetry_records = relationship("TelemetryRecord", back_populates="patient", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Patient(id={self.id}, clinician_id={self.assigned_clinician_id})>"

class TelemetryRecord(Base):
    """
    Stores high-frequency Ambulatory Blood Pressure Monitoring (ABPM) time-series data.
    """
    __tablename__ = 'telemetry_records'

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey('patients.id'), index=True, nullable=False)
    
    # The exact moment the reading was taken
    recorded_at = Column(DateTime, index=True, nullable=False)
    
    # Core physiological metrics
    systolic = Column(Float, nullable=False)
    diastolic = Column(Float, nullable=False)
    heart_rate = Column(Integer, nullable=True)
    
    # Derived clinical metrics (enforced bounds: MAP 70-110, PP 30-80)
    map = Column(Float, nullable=False)             # Mean Arterial Pressure
    pulse_pressure = Column(Float, nullable=False)  # Pulse Pressure
    
    # Anomaly / XAI Flags
    is_anomaly = Column(Boolean, default=False)
    
    # Relationships
    patient = relationship("Patient", back_populates="telemetry_records")

    def __repr__(self):
        return f"<Telemetry(patient={self.patient_id}, sbp={self.systolic}, dbp={self.diastolic})>"
