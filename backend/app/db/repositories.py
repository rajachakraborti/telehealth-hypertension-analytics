from sqlalchemy.orm import Session
from app.models.dataset import Dataset
from app.models.user import User

class DatasetRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_dataset(self, dataset: Dataset):
        self.db.add(dataset)
        self.db.commit()
        self.db.refresh(dataset)
        return dataset

    def get_dataset(self, dataset_id: int):
        return self.db.query(Dataset).filter(Dataset.id == dataset_id).first()

    def get_all_datasets(self):
        return self.db.query(Dataset).all()

    def update_dataset(self, dataset_id: int, updated_data: dict):
        dataset = self.get_dataset(dataset_id)
        for key, value in updated_data.items():
            setattr(dataset, key, value)
        self.db.commit()
        return dataset

    def delete_dataset(self, dataset_id: int):
        dataset = self.get_dataset(dataset_id)
        if dataset:
            self.db.delete(dataset)
            self.db.commit()
            return True
        return False

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_user(self, user: User):
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def get_user(self, user_id: int):
        return self.db.query(User).filter(User.id == user_id).first()

    def get_all_users(self):
        return self.db.query(User).all()

    def update_user(self, user_id: int, updated_data: dict):
        user = self.get_user(user_id)
        for key, value in updated_data.items():
            setattr(user, key, value)
        self.db.commit()
        return user

    def delete_user(self, user_id: int):
        user = self.get_user(user_id)
        if user:
            self.db.delete(user)
            self.db.commit()
            return True
        return False