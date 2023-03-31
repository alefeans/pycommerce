from bcrypt import hashpw, checkpw, gensalt


class Hasher:
    @staticmethod
    def hash(value: str) -> str:
        return hashpw(value.encode("utf-8"), gensalt()).decode("utf-8")

    @staticmethod
    def check(value: str, hashed: str) -> bool:
        return checkpw(value.encode("utf-8"), hashed.encode("utf-8"))
