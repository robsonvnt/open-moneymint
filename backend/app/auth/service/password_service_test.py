from auth.service.services import PasswordService


def test_protect_password_creates_hash():
    password = "my_secure_password"
    password_hash = PasswordService.protect_password(password)

    assert password_hash is not None
    assert password_hash != password
    assert len(password_hash) == 60


def test_verify_password_with_correct_password():
    password = "my_secure_password"
    password_hash = PasswordService.protect_password(password)

    assert PasswordService.verify_password(password, password_hash) is True


def test_verify_password_with_incorrect_password():
    password = "my_secure_password"
    wrong_password = "my_wrong_password"
    password_hash = PasswordService.protect_password(password)

    assert PasswordService.verify_password(wrong_password, password_hash) is False
