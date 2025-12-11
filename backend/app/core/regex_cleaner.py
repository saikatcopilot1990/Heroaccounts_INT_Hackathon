"""
Regex-driven text cleaner tailored for OCR output.
"""

import re
from typing import Callable, Dict, List, Optional, Any


class RegexCleaner:
    """
    Comprehensive Regex OCR data cleaning class with configurable cleaning steps.
    """

    def __init__(self) -> None:
        # 1. Remove non-printable / non-ASCII noise
        self.REGEX_NON_ASCII = re.compile(r"[^\x20-\x7E\n]")
        self.REGEX_CONTROL = re.compile(r"[\x00-\x09\x0B\x0C\x0E-\x1F\x7F]")

        # 2. Remove weird OCR symbols (keep legit chars)
        self.REGEX_WEIRD_SYMBOLS = re.compile(r"[^\w\s.,:/\-()#+&%]")

        # 3. Normalize unicode dashes + quotes
        self.REGEX_DASHES = re.compile(r"[–—−]")
        self.REGEX_QUOTES = re.compile(r"[“”«»‘’]")

        # 4. Fix spacing before punctuation
        self.REGEX_FIX_SPACE_BEFORE_PUNCT = re.compile(r"\s+([.,!?;:])")

        # 5. Reduce multiple spaces
        self.REGEX_MULTI_SPACES = re.compile(r"\s{2,}")
        self.REGEX_OCR_MERGED_LETTERS = re.compile(r"(?<!\w)([A-Za-z])\s+(?=[A-Za-z](?!\w))")

        # 6. Fix OCR merged letter spacing
        self.REGEX_MERGED_OCR_SPACING = re.compile(r"(?<=\w)\s(?=\w)")

        # 7. Remove line breaks inside sentences
        self.REGEX_BAD_LINEBREAKS = re.compile(r"(?<!\n)\n(?!\n)(?=[a-zA-Z0-9])")

        # 8. Bullet points cleanup
        self.REGEX_BULLETS = re.compile(r"[•·●◆◇▪▫]")

        # 9. Deduplicate punctuation (OCR glitch)
        self.REGEX_MULTI_PUNCT = re.compile(r"([.,;:!?])\1+")

        # 10. Remove page numbers
        self.REGEX_PAGE_NUMBERS = re.compile(r"page[\s:.-]*\d+", re.IGNORECASE)

        # 11. Fix duplicate characters beyond 3 (OCR)
        self.REGEX_DUPLICATE_CHARS = re.compile(r"(.)\1{2,}")

        # 12. Fix email OCR issues
        self.REGEX_EMAIL_AT = re.compile(r"\s*@\s*")
        self.REGEX_EMAIL_MULTI_SPACES = re.compile(r"(@\S+)\s+(\S+)")

        # 13. Fix spaced-out month names
        self.REGEX_MONTH_SPACED = re.compile(
            r"\b(N o v e m b e r|D e c e m b e r|J a n u a r y|F e b r u a r y|"
            r"M a r c h|A p r i l|M a y|J u n e|J u l y|A u g u s t|"
            r"S e p t e m b e r|O c t o b e r)\b",
            re.IGNORECASE,
        )

        # 14. Fix broken “@” OCR artifacts
        self.REGEX_AT_FIX = re.compile(r"\s*@\s*")

        # 15. Split glued words (camel case OCR bug)
        self.REGEX_STUCK_CAMEL = re.compile(r"(?<=[a-z])(?=[A-Z])")

        # 16. Fix glued numbers/letters
        self.REGEX_NUMBER_WORD = re.compile(r"(\d)([A-Za-z])")
        self.REGEX_WORD_NUMBER = re.compile(r"([A-Za-z])(\d)")

    def clean_text(self, text: str) -> str:
        """Run canonical cleaning pipeline on OCR text."""
        text = self.REGEX_CONTROL.sub(" ", text)
        text = self.REGEX_NON_ASCII.sub(" ", text)

        text = self.REGEX_DASHES.sub("-", text)
        text = self.REGEX_QUOTES.sub('"', text)
        text = self.REGEX_BULLETS.sub("-", text)

        text = self.REGEX_EMAIL_AT.sub("@", text)
        text = self.REGEX_EMAIL_MULTI_SPACES.sub(r"\1\2", text)
        text = re.sub(r"\s*\.\s*", ".", text)

        text = self.REGEX_MULTI_SPACES.sub(" ", text)
        text = self.REGEX_OCR_MERGED_LETTERS.sub(r"\1", text)

        text = self.REGEX_FIX_SPACE_BEFORE_PUNCT.sub(r"\1", text)
        text = self.REGEX_MULTI_PUNCT.sub(r"\1", text)

        text = self.REGEX_STUCK_CAMEL.sub(" ", text)
        text = self.REGEX_MONTH_SPACED.sub(lambda m: m.group(0).replace(" ", ""), text)

        text = self.REGEX_MULTI_SPACES.sub(" ", text)
        return text.strip()


