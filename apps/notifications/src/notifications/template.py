import json

import pdfkit
from jinja2 import Environment

from src.utils.jinja2_utils import format_decimal, format_decimal_precision, format_date


class PdfFile(object):
    def __init__(self, filename: str, data: bytes):
        self.filename = filename
        self.data = data

    def __repr__(self):
        return self.filename + ": " + str(len(self.data))

    def __str__(self):
        return self.filename + ": " + str(len(self.data))


def create_pdf_string(html, default_options=True):
    if default_options:
        return pdfkit.from_string(
            html,
            False,
            options={
                'page-size': 'A4',
                'margin-top': '0.25in',
                'margin-right': '0.25in',
                'margin-bottom': '0.25in',
                'margin-left': '0.25in',
                'encoding': "UTF-8",
            }
        )
    else:
        return pdfkit.from_string(html, False)


def get_pdf_attachment(html_template, pdf_data, pdf_name) -> PdfFile:
    pdf_document_html = build_template(html_template, pdf_data)
    return PdfFile(pdf_name, create_pdf_string(pdf_document_html))


def build_template(template, values_dict=None):
    if not template:
        return None

    environment = Environment()
    environment.filters['format_decimal'] = format_decimal
    environment.filters['format_decimal_precision'] = format_decimal_precision
    environment.filters['format_date'] = format_date
    return environment.from_string(template).render(values_dict or {})
