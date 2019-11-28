from flask import render_template, request
import ldap, re, sys

from wsgi import app


BASEDN = "DC=ldap,DC=cup,DC=ctf"
LDAP_FILTER_FORMAT = """(&
    (objectClass=inetOrgPerson)
    (sn={0})
    (uid={1})
)"""

def parse_card(response):
    return {
        "sn": response["sn"][0].decode(),
        "mail": response["mail"][0].decode()
    }


@app.route('/', methods=["GET", "POST"])
def index() -> str:
    if request.method == "GET":
        return render_template("auth.html")

    card = None
    login = request.form.get("login")
    password = request.form.get("password")

    conn = ldap.initialize("ldap://openldap/")
    try:
        ldap_filter = LDAP_FILTER_FORMAT.format(login, password)
        attributes = ["sn", "mail"]
        result = conn.search_s(BASEDN, ldap.SCOPE_SUBTREE, ldap_filter, attributes)
        
        if len(result) > 0:
            card = parse_card(result[0][1])
    except Exception as e:
        print(f"Error: {e}")
      
    return render_template("index.html", card=card)
