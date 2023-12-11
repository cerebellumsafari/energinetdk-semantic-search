import re
from PyPDF2 import PdfReader
from typing import Iterator, Tuple


def extract_text_from_pdf(filepath: str) -> Iterator[Tuple[int, str]]:
    """
    Extract text from a PDF file.

    :param filepath: Path to PDF file
    :return: Iterator of (page_number, text)
    """
    reader = PdfReader(filepath)
    for i, page in enumerate(reader.pages):
        yield i+1, re.sub(r'\s+', ' ', page.extract_text())


def extract_title_from_pdf(filepath: str) -> str:
    """
    Extract title from a PDF file.

    :param filepath: Path to PDF file
    :return: Title
    """
    reader = PdfReader(filepath)
    return reader.metadata.title
