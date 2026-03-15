import re
from typing import List, Dict
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup


# -----------------------------
# Compliance Keyword Intelligence
# -----------------------------
PRIMARY_KEYWORDS = [
    "regulation", "regulations", "rules", "statutes", "code",
    "insurance code", "administrative code", "bulletins",
    "circular letters", "rate and form filings", "filings",
    "p&c", "property & casualty", "auto insurance requirements",
    "minimum limits", "mandatory coverage",
]

AUTO_KEYWORDS = [
    "auto", "motor vehicle", "personal automobile",
    "private passenger auto", "private passenger",
    "pip", "um", "uim",
    "liability minimums", "liability", "coverage",
    "deductible", "cancellation", "nonrenewal",
]

SECTION_KEYWORDS = PRIMARY_KEYWORDS + AUTO_KEYWORDS

MANDATORY_VERBS = [
    "must", "shall", "required", "may not", "cannot",
    "prohibited", "is required to", "is mandated to",
    "shall not", "must not",
]

AUTO_TRIGGERS = [
    "auto", "motor vehicle", "personal automobile",
    "private passenger", "pip", "um", "uim",
    "liability", "minimum limits", "coverage",
    "deductible", "cancellation", "nonrenewal",
]


# -----------------------------
# Utility: Fetch HTML
# -----------------------------
def _fetch_html(url: str) -> str | None:
    try:
        resp = requests.get(
            url,
            timeout=15,
            headers={"User-Agent": "OptimaAI-RegIntel/1.0"},
        )
        if resp.status_code == 200 and "text/html" in resp.headers.get("Content-Type", ""):
            return resp.text
    except Exception:
        return None
    return None


# -----------------------------
# Rule Sentence Detector
# -----------------------------
def _is_rule_sentence(sentence: str) -> bool:
    s = sentence.lower().strip()

    if len(s.split()) < 8:
        return False

    if not any(v in s for v in MANDATORY_VERBS):
        return False

    if not any(t in s for t in AUTO_TRIGGERS):
        return False

    return True


class SmartRuleExtractor:
    """
    HTML-only state DOI rule extractor.
    No downloads. No PDFs. No files.
    """

    def __init__(self, max_depth: int = 2, max_links: int = 80):
        self.max_depth = max_depth
        self.max_links = max_links

    # -----------------------------
    # Discover compliance-relevant links
    # -----------------------------
    def discover_links(self, base_url: str) -> List[str]:
        html = _fetch_html(base_url)
        if not html:
            return []

        soup = BeautifulSoup(html, "html.parser")
        links = []

        for tag in soup.find_all("a", href=True):
            text = tag.get_text(strip=True).lower()
            href = urljoin(base_url, tag["href"])

            # Only follow links inside the same domain
            if urlparse(href).netloc != urlparse(base_url).netloc:
                continue

            # Only keep compliance-relevant links
            if any(k in text for k in SECTION_KEYWORDS):
                links.append(href)

        # Deduplicate + cap
        return list(dict.fromkeys(links))[: self.max_links]

    # -----------------------------
    # Extract rule-like sentences from a page
    # -----------------------------
    def extract_rules_from_page(self, url: str) -> List[str]:
        html = _fetch_html(url)
        if not html:
            return []

        soup = BeautifulSoup(html, "html.parser")
        text = soup.get_text(" ", strip=True)

        raw_sentences = re.split(r"[.?!]", text)
        rules = []

        for s in raw_sentences:
            s_clean = s.strip()
            if not s_clean:
                continue
            if _is_rule_sentence(s_clean):
                rules.append(s_clean)

        return rules

    # -----------------------------
    # Build JSON rulebook
    # -----------------------------
    def build_rulebook(self, base_url: str, state_code: str) -> Dict:
        discovered = self.discover_links(base_url)

        all_rules = []
        rule_id = 1

        for link in discovered:
            page_rules = self.extract_rules_from_page(link)

            for r in page_rules:
                all_rules.append(
                    {
                        "id": f"{state_code}-{rule_id:03}",
                        "topic": None,  # optional: can add topic classifier later
                        "text": r,
                        "source": link,
                    }
                )
                rule_id += 1

        return {
            "state": state_code,
            "base_url": base_url,
            "rules": all_rules,
        }


if __name__ == "__main__":
    # Manual test example
    extractor = SmartRuleExtractor()
    result = extractor.build_rulebook(
        base_url="https://insurance.delaware.gov",
        state_code="DE",
    )
    import json
    print(json.dumps(result, indent=2))
