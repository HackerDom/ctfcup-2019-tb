from wsgi import db, Base


class Document(Base):
    __tablename__ = 'documents'

    id = db.Column('id', db.Integer, primary_key=True)
    title = db.Column('title', db.String, nullable=False)
    content = db.Column('content', db.Text, nullable=False)
    created_at = db.Column('created_at', db.DateTime, nullable=False, default=db.func.now())

    def __init__(self, title: str, content: str):
        self.title = title
        self.content = content
