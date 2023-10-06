from random_number_generator import Generator as RandomGenerator
import hmac
import hashlib

class Generator:
    def __init__(self, random_generator: RandomGenerator):
        self._random_generator = random_generator

    def generate_secret(self) -> str:
        return hmac.new(
                bytes(self._random_generator.generate()), 
                bytes(self._random_generator.generate()),
                hashlib.sha256,
                ).hexdigest()

    def generate_sha256(self, message: str, secret: str) -> str:
        return hmac.new(
                    bytes(secret, 'utf-8'), 
                    bytes(message, 'utf-8'), 
                    hashlib.sha256
                ).hexdigest()
