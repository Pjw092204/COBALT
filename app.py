"""
Vercel / WSGI entry point.
Vercel only auto-detects Flask when `app` lives in app.py, index.py, or server.py — not main.py.
This file re-exports the real application from main.
"""
from main import app

__all__ = ["app"]
