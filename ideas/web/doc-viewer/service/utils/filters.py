from flask import Flask, render_template_string
from jinja2 import contextfilter


def add_filters(app: Flask):
    app.add_template_filter(_render_doc_content, name="render_content")


@contextfilter
def _render_doc_content(_, value):
    template = f"<section class='doc_content'>{value}</section>"
    return render_template_string(template)
