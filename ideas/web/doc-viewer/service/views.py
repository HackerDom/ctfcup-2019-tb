from typing import List
import uuid

from flask import redirect, render_template, request, url_for, make_response, session, render_template_string
from functools import wraps
from sqlalchemy import desc

from .models import Document
from .wsgi import app, Session, ADMIN_LOGIN, FLAG
from .utils.hasher import calculate_hash
from .utils.aes import AESCipher


def auth_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_hash = request.cookies.get("auth_hash")
        login = request.cookies.get("login")
        if not auth_hash or not login:
            return redirect(url_for("auth", next=request.url))

        calculated_hash = calculate_hash(login)
        if calculated_hash != auth_hash:
            return redirect(url_for("auth", next=request.url))

        return f(*args, **kwargs)

    return decorated_function


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        is_admin = request.cookies.get("login") == ADMIN_LOGIN
        if not is_admin:
            return render_template("not-admin.html")

        return f(*args, **kwargs)

    return decorated_function


@app.route('/login', methods=["GET", "POST"])
def auth():
    if request.method == "POST":
        login = request.form["login"]

        if ADMIN_LOGIN in login:
            return render_template("login.html", error="Do you realy think this is so easy???")
        resp = make_response(redirect(url_for("index")))
        resp.set_cookie("login", login)
        resp.set_cookie("auth_hash", calculate_hash(login))
        return resp

    error = request.args.get("error")
    return render_template("login.html", error=error)


@app.route('/')
@auth_required
@admin_required
def index() -> str:
    batch_size = 20
    page = int(request.args.get('page', '1'))
    documents = _get_documents(page, batch_size)
    page_info = _get_page_info(page, batch_size)
    return render_template("index.html", documents=documents, **page_info)


@app.route('/document/<document_id>')
@auth_required
@admin_required
def get_document(document_id: int) -> str:
    key = session.get('key', '')
    document = _get_decoded_document(document_id, key)
    return render_template("document.html", document=document)


@app.route('/document', methods=['GET', 'POST'])
@auth_required
@admin_required
def document():
    if request.method == 'GET':
        key = session.get('key', '')
        rendered_template = render_template('add-document.html', key=key)
        return render_template_string(rendered_template)

    title, content, key = request.form['title'], request.form['content'], request.form['key']
    s = Session()
    aes = AESCipher(key)
    s.add(Document(title, aes.encrypt(content)))
    s.commit()
    return redirect(url_for('index'))


@app.route('/key')
@auth_required
@admin_required
def generate_key():
    key = str(uuid.uuid4()).replace("-", "")
    session['key'] = key
    return render_template("key.html", key=key)


def _get_decoded_document(document_id: int, key: str) -> Document or None:
    doc = Session().query(Document)\
        .filter(Document.id == document_id)\
        .first()
    if not doc:
        return None

    print(doc.title, doc.content, key)

    try:
        aes = AESCipher(key)
        doc_content = aes.decrypt(doc.content)
        print(doc_content)
        if not doc_content:
            return None
        doc.content = doc_content
        return doc
    except Exception as e:
        print(e)


def _get_documents(page: int, batch_size: int) -> List[Document]:
    skip = (page - 1) * batch_size
    return Session().query(Document.id, Document.title, Document.created_at) \
        .order_by(desc(Document.created_at)) \
        .offset(skip)\
        .limit(batch_size)\
        .all()


def _get_page_info(page: int, batch_size: int):
    s = Session()
    docs_count = s.query(Document).count()

    a = docs_count / batch_size
    b = 0 if a % 1 == 0 else 1
    pages_count = int(a) + b
    print(pages_count)

    return {
        "current_page": page,
        "pages_count": pages_count,
        "next_page": page + 1 if page < pages_count else None,
        "previous_page": page - 1 if page > 1 else None
    }
