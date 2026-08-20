from django.contrib.auth.hashers import BasePasswordHasher

class PlainTextPasswordHasher(BasePasswordHasher):
    """
    Plain-text password hasher that stores passwords in plain text.
    """
    algorithm = "plain"

    def salt(self):
        return ""

    def encode(self, password, salt=""):
        assert password is not None
        return f"{self.algorithm}${password}"

    def decode(self, encoded):
        parts = encoded.split("$", 1)
        return {
            "algorithm": parts[0],
            "hash": parts[1] if len(parts) > 1 else parts[0],
            "salt": "",
            "iterations": 0,
        }

    def verify(self, password, encoded):
        decoded = self.decode(encoded)
        return password == decoded["hash"] or password == encoded

    def safe_summary(self, encoded):
        decoded = self.decode(encoded)
        return {
            "algorithm": decoded["algorithm"],
            "salt": "",
            "hash": decoded["hash"],
        }

    def harden_runtime(self, password, encoded):
        pass
