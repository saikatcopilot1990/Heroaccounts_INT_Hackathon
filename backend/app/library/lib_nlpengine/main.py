"""
Lightweight NLP engine that structures OCR text into business-ready metadata.
"""

from __future__ import annotations

import re
from datetime import datetime
from typing import Dict, List, Optional

import spacy
from rapidfuzz import fuzz, process

from ...config import get_settings

settings = get_settings()


class Call_NplEngine:
    """
    Wrapper around spaCy to extract receipt metadata + keyword hits.
    """

    def __init__(self, model_name: str | None = None) -> None:
        model = model_name or settings.spacy_model
        self._nlp = spacy.load(model)

    def process(self, text: str, keywords: Optional[List[str]] = None) -> Dict[str, object]:
        doc = self._nlp(text.lower())

        parsed: Dict[str, object] = {
            "amount": self._extract_amount(text, doc),
            "date": self._extract_date(text),
            "vendor": self._extract_vendor(doc, text),
            "gst": self._extract_gst(text),
            "category": self._infer_category(text),
            "purpose": self._extract_purpose(text),
            "raw_lines": [ln.strip() for ln in text.splitlines() if ln.strip()],
        }

        if keywords:
            parsed["keyword_hits"] = self._match_keywords(text, keywords)

        return parsed

    def _extract_amount(self, text: str, doc) -> Optional[float]:
        amount_regex = r"(?i)\b(total|amount|payable|balance|grand total)\s*[:\-]?\s*₹?\s*([0-9,]+\.\d{1,2}|[0-9,]+)"
        match = re.search(amount_regex, text)
        if match:
            try:
                return float(match.group(2).replace(",", ""))
            except ValueError:
                return None

        numeric_tokens = []
        for token in doc:
            stripped = token.text.replace(",", "").replace("₹", "").strip()
            if stripped.replace(".", "").isdigit():
                try:
                    numeric_tokens.append(float(stripped))
                except ValueError:
                    continue
        return max(numeric_tokens) if numeric_tokens else None

    def _extract_date(self, text: str) -> Optional[str]:
        date_patterns = [
            r"\b(\d{1,2}[\/\-\.\s]\d{1,2}[\/\-\.\s]\d{2,4})\b",
            r"\b(\d{2,4}[\/\-\.\s]\d{1,2}[\/\-\.\s]\d{1,2})\b",
            r"\b(\d{1,2}\s+(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\s+\d{4})\b",
        ]

        for pattern in date_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1)
        return None

    def _extract_vendor(self, doc, text: str) -> Optional[str]:
        orgs = [ent.text.title() for ent in doc.ents if ent.label_ in ("ORG", "GPE")]
        if orgs:
            return orgs[0]

        first_line = next((ln.strip() for ln in text.splitlines() if ln.strip()), "")
        return first_line[:120] or None

    def _extract_gst(self, text: str) -> Optional[str]:
        match = re.search(r"[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}Z[0-9A-Z]{1}", text.upper())
        return match.group(0) if match else None

    def _infer_category(self, text: str) -> str:
        categories = {
            "travel": ["flight", "hotel", "cab", "uber"],
            "meals": ["restaurant", "dining", "food", "meal"],
            "office_supplies": ["stationery", "printer", "paper"],
            "policy": ["policy", "licence", "license"],
            "invoice": ["invoice", "billing"],
        }
        lowered = text.lower()
        for cat, tokens in categories.items():
            if any(token in lowered for token in tokens):
                return cat
        return "uncategorized"

    def _extract_purpose(self, text: str) -> Optional[str]:
        match = re.search(r"purpose[:\-]\s*(.+)", text, re.IGNORECASE)
        return match.group(1).strip() if match else None

    def _match_keywords(self, text: str, keywords: List[str]) -> List[Dict[str, object]]:
        hits = []
        for keyword in keywords:
            score = fuzz.partial_ratio(keyword.lower(), text.lower())
            if score >= 70:
                hits.append({"keyword": keyword, "score": score})
        return hits

