from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Dataset(Base):
    __tablename__ = 'datasets'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    file_path = Column(String)
    data_format = Column(String)  # e.g., CSV, JSON, Excel
    size = Column(Float)  # Size in MB
    user_id = Column(Integer)  # Foreign key to the user who uploaded the dataset

    def __repr__(self):
        return f"<Dataset(id={self.id}, name={self.name}, format={self.data_format}, size={self.size}MB)>"