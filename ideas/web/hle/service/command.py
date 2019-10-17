from typing import Dict


class Command:
    def __init__(self, method: str, arguments: Dict[str, str], auth_hash: str):
        self.method = method
        self.arguments = arguments
        self.auth_hash = auth_hash
        
    def __str__(self):
        return "[{0}] {1} {2}".format(self.method, self.arguments, self.auth_hash)
