"""Password hashing and opaque login-session token helpers.

Chú ý về bcrypt: thuật toán chỉ nhận tối đa 72 byte. Mật khẩu tiếng Việt có dấu
tốn 2-3 byte mỗi ký tự, nên phải cắt trước khi băm, nếu không sẽ ném ValueError.
(Không dùng passlib vì passlib 1.7.4 xung đột với bcrypt >= 4.1.)
"""
import hashlib
import secrets

import bcrypt

BCRYPT_MAX_BYTES = 72


def _to_bytes(password: str) -> bytes:
    return password.encode("utf-8")[:BCRYPT_MAX_BYTES]


def hash_password(password: str) -> str:
    return bcrypt.hashpw(_to_bytes(password), bcrypt.gensalt()).decode()


def verify_password(password: str, hashed: str) -> bool:
    try:
        return bcrypt.checkpw(_to_bytes(password), hashed.encode())
    except ValueError:
        return False


def create_session_token() -> str:
    return secrets.token_urlsafe(32)


def hash_session_token(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()
