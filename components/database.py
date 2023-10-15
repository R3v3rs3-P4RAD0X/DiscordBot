# File: Database
# Description: Handles all database operations.
# Author: StrangeParadox
# Version: 0.0.1

# Imports
import sqlalchemy
from sqlalchemy.orm import sessionmaker, declarative_base

# Declarative Base
Base = declarative_base()

# Database Tables
class User(Base):
    __tablename__ = "users"

    # Columns
    id = sqlalchemy.Column(sqlalchemy.BigInteger, primary_key=True)

    # Relationships
    economy = sqlalchemy.orm.relationship("Economy", uselist=False, back_populates="user")

    # Methods
    def __repr__(self):
        return f"<User(id={self.id})>"


class Economy(Base):
    __tablename__ = "economy"

    # Columns
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.BigInteger, sqlalchemy.ForeignKey("users.id"))

    balance = sqlalchemy.Column(sqlalchemy.BigInteger, default=500)
    bank = sqlalchemy.Column(sqlalchemy.BigInteger, default=0)

    # Relationships
    user = sqlalchemy.orm.relationship("User", back_populates="economy")

    # Methods
    def __repr__(self):
        return f"<Economy(id={self.id}, user_id={self.user_id}, balance={self.balance}, bank={self.bank})>"

# Database Class
class Database:
    """
    Handles all database operations.

    Methods:
    get_user(user_id: int) -> User or False: Get a user from the database.
    create_user(user_id: int) -> User: Create a user in the database.
    delete_user(user_id: int) -> bool: Delete a user from the database.
    get_economy(user_id: int) -> Economy or False: Get an economy from the database.
    create_economy(user_id: int) -> Economy: Create an economy in the database.
    delete_economy(user_id: int) -> bool: Delete an economy from the database.
    handle_user(user_id: int) -> User: Handle a user.
    """

    def __init__(self, url: str = ""):
        """
        Initialize the class.
        Set the variables.
        """
        self.engine = sqlalchemy.create_engine(url or "sqlite:///database.db")
        self.base = Base

        self.base.metadata.create_all(self.engine)
        self.session = sessionmaker(bind=self.engine)()

    def get_user(self, user_id: int) -> User:
        """
        Get a user from the database.

        Args:
        user_id (int): The ID of the user to get.

        Returns:
        User or False: The user object if found, False otherwise.
        """
        return self.session.query(User).filter_by(id=user_id).first() or False
    
    def create_user(self, user_id: int) -> User:
        """
        Create a user in the database.

        Args:
        user_id (int): The ID of the user to create.

        Returns:
        User: The created user object.
        """
        user = User(id=user_id)

        self.session.add(user)
        self.session.commit()

        return user
    
    def delete_user(self, user_id: int) -> bool:
        """
        Delete a user from the database.

        Args:
        user_id (int): The ID of the user to delete.

        Returns:
        bool: True if the user was deleted, False otherwise.
        """
        user = self.get_user(user_id)

        if not user:
            return False
        
        self.session.delete(user)
        self.session.commit()

        return True
    
    def get_economy(self, user_id: int) -> Economy:
        """
        Get an economy from the database.

        Args:
        user_id (int): The ID of the user whose economy to get.

        Returns:
        Economy or False: The economy object if found, False otherwise.
        """
        return self.session.query(Economy).filter_by(user_id=user_id).first() or False
    
    def create_economy(self, user_id: int) -> Economy:
        """
        Create an economy in the database.

        Args:
        user_id (int): The ID of the user whose economy to create.

        Returns:
        Economy: The created economy object.
        """
        economy = Economy(user_id=user_id)

        self.session.add(economy)
        self.session.commit()

        return economy
    
    def delete_economy(self, user_id: int) -> bool:
        """
        Delete an economy from the database.

        Args:
        user_id (int): The ID of the user whose economy to delete.

        Returns:
        bool: True if the economy was deleted, False otherwise.
        """
        economy = self.get_economy(user_id)

        if not economy:
            return False
        
        self.session.delete(economy)
        self.session.commit()

        return True
    
    def update_economy(self, user_id: int, **kwargs) -> bool:
        """
        Update an economy in the database.

        Args:
        user_id (int): The ID of the user whose economy to update.
        **kwargs: The attributes to update.

        Returns:
        bool: True if the economy was updated, False otherwise.
        """
        economy = self.get_economy(user_id)

        if not economy:
            return False
        
        for key, value in kwargs.items():
            # Check if the attribute exists
            if not hasattr(economy, key):
                continue

            setattr(economy, key, value)
        
        self.session.commit()

        return True
    
    def handle_user(self, user_id: int) -> User:
        """
        Handle a user.

        Args:
        user_id (int): The ID of the user to handle.

        Returns:
        User: The user object.
        """
        user = self.get_user(user_id)

        if not user:
            user = self.create_user(user_id)
            self.create_economy(user_id)

        # Check if the user has an economy
        if not user.economy:
            self.create_economy(user_id)
        
        return user
