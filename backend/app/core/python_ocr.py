"""
Thin OCR wrapper responsible for converting PDF bytes into normalized text.
"""

from __future__ import annotations

from dataclasses import dataclass
from io import BytesIO
from typing import Dict, List

from pdfminer.high_level import extract_text

from .regex_cleaner import RegexCleaner

__version__ = "1.0.0"
__author__ = "Risker AI Team"


@dataclass
class OCRResult:
    """Structured response emitted by pythonOCR."""

    raw_text: str
    clean_text: str
    pages: List[str]
    metadata: Dict[str, str]


class pythonOCR:
    """
    Advanced OCR processor for multiple file formats (PDF-focused here).
    """

    def __init__(self, cleaner: RegexCleaner | None = None) -> None:
        self.cleaner = cleaner or RegexCleaner()

    def process_file(self, file_bytes: bytes, language: str = "eng") -> OCRResult:
        if not file_bytes:
            raise ValueError("Empty PDF payload supplied to OCR.")

        raw_text = extract_text(BytesIO(file_bytes))
        clean_text = self.cleaner.clean_text(raw_text)
        pages = [page.strip() for page in raw_text.split("\f") if page.strip()]

        metadata = {
            "language": language,
            "char_count": str(len(raw_text)),
            "page_count": str(len(pages)),
        }

        return OCRResult(raw_text=raw_text, clean_text=clean_text, pages=pages, metadata=metadata)


class Call_pythonOCR:
    """
    Public callable used by upstream services for OCR work.
    """

    def __init__(self, cleaner: RegexCleaner | None = None) -> None:
        self.cleaner = cleaner or RegexCleaner()

    def process(self, file_bytes: bytes, language: str = "eng") -> OCRResult:
        ocr = pythonOCR(cleaner=self.cleaner)
        return ocr.process_file(file_bytes, language=language)

