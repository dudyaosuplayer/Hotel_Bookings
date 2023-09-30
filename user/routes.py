from fastapi import APIRouter, HTTPException, Query, Path
from typing import Annotated
from . import db_queries, schemas
from database import db_dependencies
from auth_dep import auth_dependencies

router = APIRouter(
    prefix='/users',
    tags=['User']
)


@router.get('/', response_model=list[schemas.User])
async def get_all_users(
        db: db_dependencies, skip: Annotated[int | None, Query(title="Number of values to skip",
                                                               description="Number of values to skip (from the beginning)")] = 0,
        limit: Annotated[int | None, Query(title="Limit number of entries",
                                           description="Limit number of entries (100 is optimal)")] = 100
):
    """
    Get a list of all users.

    Parameters:
    - **db**: Dependency to obtain a database session.
    - **skip** (optional): Number of records to skip (default is 0).
    - **limit** (optional): Maximum number of records to return (default is 100).

    Returns a list of users.
    """
    users = db_queries.get_users(db, skip=skip, limit=limit)
    return users


@router.post('/', response_model=schemas.User)
async def create_user(user: schemas.UserCreate, db: db_dependencies):
    """
    Create a new user.

    Parameters:
    - **user** (schemas.UserCreate): User data to create.
    - **db** (db_dependencies): Dependency to obtain a database session.

    Returns:
        schemas.User: The created user object.

    Possible Errors:
        HTTP 400: Email already registered.
        HTTP 400: Username already registered.
    """
    db_user_email = db_queries.get_user_by_email(db, user_email=user.email)
    db_user_username = db_queries.get_user_by_username(db, username=user.username)
    if db_user_email:
        raise HTTPException(status_code=400, detail="Email already registered")
    if db_user_username:
        raise HTTPException(status_code=400, detail="Username already registered")
    return db_queries.create_user(db=db, user=user)


@router.delete('/', response_model=schemas.User)
async def delete_user(credentials: auth_dependencies, user: schemas.UserDelete, db: db_dependencies):
    """
    Delete a user.

    Parameters:
    - **credentials** (auth_dependencies): User credentials for authentication.
    - **user** (schemas.UserDelete): User data to delete.
    - **db** (db_dependencies): Dependency to obtain a database session.

    Returns:
        schemas.User: The deleted user object.

    Possible Errors:
        HTTP 400: User does not exist.
    """
    db_user = db_queries.get_user_by_username(db, username=user.username)
    if not db_user:
        raise HTTPException(status_code=400, detail="User does not exist")
    return db_queries.delete_user(db=db, user=user)


@router.put('/{user_id}', response_model=schemas.User)
async def update_user(
        credentials: auth_dependencies, user_id: Annotated[
            int, Path(..., title="User ID", description="The ID of user to retrieve", ge=0)],
        user: schemas.UserCreate, db: db_dependencies
):
    """
    Update a user's information.

    Parameters:
    - **credentials** (auth_dependencies): User credentials for authentication.
    - **user_id** (int): ID of the user to update.
    - **user** (schemas.UserCreate): Updated user data.
    - **db** (db_dependencies): Dependency to obtain a database session.

    Returns:
        schemas.User: The updated user object.

    Possible Errors:
        HTTP 400: User does not exist.
    """
    db_user = db_queries.get_user_by_id(db, user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=400, detail="User does not exist")
    return db_queries.update_user(db=db, user=user, user_id=user_id)
