"""
Flask blueprint: HTTP boundary for Playwright-backed scraping.

Treat this as the "serverless-style" surface for browser automation — one module,
predictable JSON in/out, easy to put behind a separate service or route prefix later.
"""

from __future__ import annotations

from flask import Blueprint, request, jsonify

from pdf_extractor import get_extraction_capabilities
from playwright_wrapper import normalize_dsn, run_playwright_scrape

playwright_bp = Blueprint(
    "playwright",
    __name__,
    url_prefix="/api/playwright",
)


@playwright_bp.route("/scrape", methods=["POST"])
def scrape():
    """
    POST JSON: { "dsn": "588459" } or { "brrts": "588459" }

    Returns full scrape payload: site_info, risk_flags, documents, summary,
    documents_available (count), extraction_available, error (if any).
    """
    data = request.get_json() or {}
    raw = (data.get("dsn") or data.get("brrts") or "").strip()

    if not raw:
        return jsonify({"error": "Missing dsn or brrts."}), 400

    dsn = normalize_dsn(raw)
    if not dsn:
        return jsonify({"error": "Could not derive a DSN from input."}), 400

    try:
        result = run_playwright_scrape(dsn)
    except Exception as e:
        return jsonify({"error": f"Playwright scrape failed: {str(e)}", "dsn": dsn}), 500

    if result.get("error"):
        return (
            jsonify(
                {
                    "error": result["error"],
                    "dsn": dsn,
                    "site_info": result.get("site_info", {"dsn": dsn}),
                    "risk_flags": result.get("risk_flags", {"status_label": "UNKNOWN"}),
                    "documents": [],
                    "summary": result.get("summary", ""),
                }
            ),
            500,
        )

    documents = result.get("documents", [])
    out = {
        "dsn": dsn,
        "site_info": result.get("site_info", {"dsn": dsn}),
        "risk_flags": result.get("risk_flags", {"status_label": "UNKNOWN"}),
        "summary": result.get("summary", ""),
        "documents": documents,
        "documents_available": len(documents),
        "extraction_available": get_extraction_capabilities()["can_extract"],
    }
    if result.get("note"):
        out["note"] = result["note"]
    return jsonify(out)


@playwright_bp.route("/health", methods=["GET"])
def playwright_layer_health():
    """Sub-route health for load balancers / canaries."""
    return jsonify({"service": "playwright-api", "status": "ok"}), 200
