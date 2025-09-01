from src.contexts.users.domain.user import User


def test_user_creation_and_password_hashing():
    """
    Test that the static method `hash_password` generates a valid hash.
    """
    plain_password = "my_secret_password_123"

    # Call the static method directly from the class
    hashed_password = User.hash_password(plain_password)

    # Assert: Check that the hash is not the original password
    assert hashed_password is not None
    assert hashed_password != plain_password

    # Assert: Check that the hash is a string
    assert isinstance(hashed_password, str)

    # Assert: Bcrypt hashes start with a specific prefix ($2b$)
    assert hashed_password.startswith("$2b$")


def test_password_verification():
    """
    Test that the `verify_password` method works for correct and incorrect passwords.
    """
    plain_password = "a_very_secure_password"
    wrong_password = "not_the_password"

    # Create a User instance, hashing the password in the process
    user = User(
        name="Test User",
        email="verify@example.com",
        hashed_password=User.hash_password(plain_password),
    )

    # Assert: Correct password returns True
    assert user.verify_password(plain_password) is True

    # Assert: Incorrect password returns False
    assert user.verify_password(wrong_password) is False

    # Assert: Empty or null password returns False
    assert user.verify_password("") is False


def test_verify_password_with_different_hashes():
    """
    Test that two hashes generated from the same password are different,
    but both validate correctly. This is a key property of bcrypt due to the random 'salt'.
    """
    plain_password = "same_password_different_hash"

    hash1 = User.hash_password(plain_password)
    hash2 = User.hash_password(plain_password)

    # Assert: The two hashes should be different
    assert hash1 != hash2

    # Create a user with the first hash
    user1 = User(name="User 1", email="u1@test.com", hashed_password=hash1)

    # Assert: Original password validates against hash1
    assert user1.verify_password(plain_password) is True

    # Create another user with the second hash
    user2 = User(name="User 2", email="u2@test.com", hashed_password=hash2)

    # Assert: Same original password validates against hash2
    assert user2.verify_password(plain_password) is True
