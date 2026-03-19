"""
Playwright scrape entry point — single place all browser automation goes through.

Use this from Flask routes (or any worker) so Playwright stays behind one boundary.
Runs subprocess → playwright_scraper.py (see document_scraper.py).

**Deployment**: Requires Chromium (Dockerfile on Railway, or local `playwright install`).
Not available on typical Vercel serverless; those requests fall back to HTTP-only scraping.
"""

from __future__ import annotations

from typing import Any, Dict


def normalize_dsn(raw: str) -> str:
    """Extract 6-digit DSN from user input."""
    digits_only = "".join(c for c in raw if c.isdigit())
    if len(digits_only) >= 6:
        return digits_only[-6:]
    return digits_only


def run_playwright_scrape(dsn: str) -> Dict[str, Any]:
    """
    Full BRRTS site + documents scrape via Playwright (subprocess).

    Returns the same shape as document_scraper.extract_site_and_documents:
    site_info, risk_flags, documents, summary, error (optional), note (optional).
    """
    from document_scraper import extract_site_and_documents

    return extract_site_and_documents(dsn)
