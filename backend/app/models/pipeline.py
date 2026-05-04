from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base

class Pipeline(Base):
    __tablename__ = 'pipelines'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    steps = relationship("PipelineStep", back_populates="pipeline")

class PipelineStep(Base):
    __tablename__ = 'pipeline_steps'

    id = Column(Integer, primary_key=True, index=True)
    pipeline_id = Column(Integer, ForeignKey('pipelines.id'))
    step_name = Column(String, index=True)
    step_order = Column(Integer)
    parameters = Column(String)  # JSON string to store parameters

    pipeline = relationship("Pipeline", back_populates="steps")