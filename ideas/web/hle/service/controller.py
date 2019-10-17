from command import Command
from hasher import calculate_hash
import os

SCRIPT_PATH = os.path.dirname(os.path.realpath(__file__))
with open(os.path.join(SCRIPT_PATH, "flag.txt")) as f:
    FLAG = f.read()

with open(os.path.join(SCRIPT_PATH, "secret.txt")) as f:
    SECRET = f.read()

ADMIN_LOGIN = "admin"


def must_be_authorized(function):
    def check_auth(self, command: Command):
        if not command.arguments or "login" not in command.arguments or command.auth_hash is None:
            raise ValueError("Must be authorized")
        actual_hash = calculate_hash(SECRET + command.arguments["login"])

        if actual_hash != command.auth_hash:
            raise ValueError("Failed to recognise user")

        return function(self, command)

    return check_auth


def must_be_admin(function):
    def check_admin(self, command: Command):
        if not command.arguments or ADMIN_LOGIN.lower() not in command.arguments["login"].lower():
            raise ValueError("Must be admin")
        return function(self, command)

    return check_admin


class MethodController:
    def __init__(self):
        self.methods = {
            "reg": self._register,
            "flag": self._get_flag
        }
        self.registered_users = set()

    def execute(self, command: Command):
        if command.method not in self.methods:
            raise ValueError("Method not implemented")

        return self.methods[command.method](command)

    def _register(self, command: Command) -> str:
        args = command.arguments
        if not args or "login" not in args:
            raise ValueError("Must select login to auth in arguments")

        if args["login"] in self.registered_users:
            raise ValueError("User already registered")

        if ADMIN_LOGIN.lower() in args["login"].lower():
            raise ValueError("Do you really think this is so easy???")

        self.registered_users.add(args["login"])
        return calculate_hash(SECRET + args["login"])

    @must_be_authorized
    @must_be_admin
    def _get_flag(self, _: Command) -> str:
        return FLAG
