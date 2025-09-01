from src.contexts.users.domain.user import User
from src.contexts.users.infrastructure.user import User as UserOrmModel


def user_domain_to_orm(domain_user: User) -> UserOrmModel:
    """Transforms a domain User entity to an ORM User model."""
    return UserOrmModel(
        id=domain_user.id,
        name=domain_user.name,
        email=domain_user.email,
        hashed_password=domain_user.hashed_password,
    )


def user_orm_to_domain(orm_user: UserOrmModel) -> User:
    """Transforms an ORM User model to a domain User entity."""
    return User(
        id=orm_user.id,
        name=orm_user.name,
        email=orm_user.email,
        hashed_password=orm_user.hashed_password,
    )
