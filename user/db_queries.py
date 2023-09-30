from sqlalchemy.orm import Session
from . import models, schemas


def get_users(db: Session, skip: int = 0, limit: int = 100):
    """
    Get a list of users from the database.

    Args:
        db (Session): The database session.
        skip (int, optional): Number of records to skip (default is 0).
        limit (int, optional): Maximum number of records to return (default is 100).

    Returns:
        list: A list of users.
    """
    return db.query(models.User).offset(skip).limit(limit).all()


def get_user_by_id(db: Session, user_id: int):
    """
    Get a user from the database by ID.

    Args:
        db (Session): The database session.
        user_id (int): The user's ID.

    Returns:
        models.User: The user object.
    """
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_username(db: Session, username: str):
    """
    Get a user from the database by username.

    Args:
        db (Session): The database session.
        username (str): The username to search for.

    Returns:
        models.User: The user object.
    """
    return db.query(models.User).filter(models.User.username == username).first()


def get_user_by_email(db: Session, user_email: str):
    """
    Get a user from the database by email address.

    Args:
        db (Session): The database session.
        user_email (str): The user's email address to search for.

    Returns:
        models.User: The user object.
    """
    return db.query(models.User).filter(models.User.email == user_email).first()


def create_user(db: Session, user: schemas.UserCreate):
    """
    Create a new user and add it to the database.

    Args:
        db (Session): The database session.
        user (schemas.UserCreate): The user data to create.

    Returns:
        models.User: The created user object.
    """
    fake_hashed_password = user.password
    db_user = models.User(username=user.username, email=user.email, password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user: schemas.UserDelete):
    """
    Delete a user from the database.

    Args:
        db (Session): The database session.
        user (schemas.UserDelete): The user data to delete.

    Returns:
        models.User: The deleted user object.
    """
    db_user = get_user_by_username(db, username=user.username)
    db.delete(db_user)
    db.commit()
    return db_user


def update_user(db: Session, user: schemas.UserCreate, user_id: int):
    """
    Update a user's information in the database.

    Args:
        db (Session): The database session.
        user (schemas.UserCreate): The updated user data.
        user_id (int): The user's ID to update.

    Returns:
        models.User: The updated user object.
    """
    db_user = get_user_by_id(db, user_id=user_id)
    db_user.username = user.username
    db_user.email = user.email
    db_user.password = user.password
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
