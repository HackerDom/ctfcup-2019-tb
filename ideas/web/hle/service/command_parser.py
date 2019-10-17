from command import Command
from typing import List, Dict


def parse(command: str) -> Command:
    parts = command.split(' ')

    if len(parts) == 0:
        raise ValueError("Bad command query")

    method = _parse_method(parts)
    if not method:
        raise ValueError("Bad command query")

    auth = _parse_auth_hash(parts)
    args = _parse_args(parts)
    return Command(method.lower(), args, auth)

def _parse_auth_hash(arguments: List[str]) -> str or None:
    return __parse_with_prefix(arguments, "u_")

def _parse_method(arguments: List[str]) -> str or None:
    return __parse_with_prefix(arguments, "m_")

def _parse_args(arguments: List[str]) -> Dict[str, str] or None:
    arguments_str = __parse_with_prefix(arguments, "a_")
    if arguments_str is None:
        return None

    arguments_pairs = [x for x in arguments_str.split("&") if x != ""]
    res = {}
    for pair in arguments_pairs:
        key, value = pair.split("=", 1)
        res[key] = value

    return res

def __parse_with_prefix(arguments: List[str], prefix: str) -> str or None:
    parts = [x for x in arguments if x.startswith(prefix)]
    if len(parts) == 0:
        return None

    return parts[0][len(prefix):]
