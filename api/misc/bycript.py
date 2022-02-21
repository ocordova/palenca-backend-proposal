import bcrypt


def check_password(*, plain_password: str, hashed_password: str) -> bool:
    """Function to check whether a plaintext plain_password matches one that has been hashed previously
    :param str plain_password: The plain password
    :param str hashed_password: The hashed password
    :rtype: bool
    :return: If the plain_password matches the hashed_password
    """
    return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())


def hash_password(*, plain_password: str) -> str:
    """
    :param str plain_password: The password to hash
    :return: The hashed password
    """

    return bcrypt.hashpw(plain_password.encode(), bcrypt.gensalt()).decode()
