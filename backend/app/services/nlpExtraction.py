import re
from rapidfuzz import fuzz


class NplEngine:

    def __init__(self, keywords):
        self.keywords = [k.lower() for k in keywords]

    # Fuzzy match key
    def match_key(self, word):
        word = word.lower()
        best = None
        best_score = 0

        for key in self.keywords:
            score = fuzz.partial_ratio(word, key)
            if score > best_score:
                best_score = score
                best = key

        return best if best_score >= 80 else None

    def extract(self, text):
        lines = [ln.strip() for ln in text.split("\n") if ln.strip()]
        output = {k: [] for k in self.keywords}

        # ------------------------------
        # 1. Extract line-based fields
        # ------------------------------
        for line in lines:
            parts = re.split(r"[:\-]", line, maxsplit=1)
            if len(parts) == 2:
                key_candidate = parts[0].strip()
                val = parts[1].strip()

                matched = self.match_key(key_candidate)
                if matched:
                    output[matched].append({
                        "value": val,
                        "confidence": 1.0
                    })

        # ------------------------------
        # 2. Extract GST values (numbers like 325)
        # ------------------------------
        gst_match = re.search(r"\b([0-9]{1,5})\b\s*(GST|CGST|SGST|IGST)?", text, re.I)
        if gst_match and "gst" in output:
            gst_value = gst_match.group(1)
            output["gst"].append({
                "value": gst_value,
                "confidence": 1.0
            })

        # ------------------------------
        # 3. Extract amount (largest number)
        # ------------------------------
        amounts = re.findall(r"[0-9][0-9,]{1,10}", text)
        if amounts and "amount" in output:
            cleaned = [int(a.replace(",", "")) for a in amounts]
            biggest = max(cleaned)
            output["amount"].append({
                "value": str(biggest),
                "confidence": 1.0
            })

        # ------------------------------
        # 4. Extract category
        # ------------------------------
        categories = {
            "travel": ["flight", "cab", "ticket", "airport", "travel"],
            "hotel": ["hotel", "stay", "room"],
            "food": ["meal", "restaurant", "food", "lunch", "dinner"]
        }

        for key, words in categories.items():
            for w in words:
                if w in text.lower():
                    if "category" in output:
                        output["category"].append({
                            "value": key.capitalize(),
                            "confidence": 1.0
                        })
                    break

        # ------------------------------
        # 5. Convert to your structured output
        # ------------------------------
        final_list = []
        for key in self.keywords:
            if output[key]:
                final_list.append({
                    "label": key,
                    "values": output[key]
                })

        return final_list
