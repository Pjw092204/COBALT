"""
Browserless.io Scraper - Uses cloud browser API to render JavaScript pages.
Works on Vercel/serverless without needing local Playwright.
"""

import os
import re
import requests
from bs4 import BeautifulSoup

# Browserless.io API - free tier: 1000 requests/month
BROWSERLESS_API_KEY = os.environ.get("BROWSERLESS_API_KEY", "")
BROWSERLESS_URL = "https://chrome.browserless.io/content"


def scrape_with_browserless(dsn: str) -> dict:
    """
    Scrape DNR BRRTS page using Browserless.io cloud browser.
    Returns site_info, risk_flags, documents.
    """
    url = f"https://apps.dnr.wi.gov/rrbotw/botw-activity-detail?dsn={dsn}"
    
    site_info = {"dsn": dsn}
    risk_flags = {"status_label": "UNKNOWN"}
    documents = []
    
    if not BROWSERLESS_API_KEY:
        return {
            "site_info": site_info,
            "risk_flags": risk_flags,
            "documents": documents,
            "error": "BROWSERLESS_API_KEY not set. Add it to environment variables.",
            "summary": "Browserless API key required for full scraping."
        }
    
    try:
        # Call Browserless.io to render the page
        payload = {
            "url": url,
            "waitFor": 5000,  # Wait 5 seconds for JS to load
            "gotoOptions": {
                "waitUntil": "networkidle2"
            }
        }
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Basic {BROWSERLESS_API_KEY}"
        }
        
        # Alternative: use token in URL
        api_url = f"{BROWSERLESS_URL}?token={BROWSERLESS_API_KEY}"
        
        response = requests.post(
            api_url,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=60
        )
        
        if response.status_code != 200:
            return {
                "site_info": site_info,
                "risk_flags": risk_flags,
                "documents": documents,
                "error": f"Browserless API error: {response.status_code}",
                "summary": f"Failed to render page: {response.text[:200]}"
            }
        
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        page_text = soup.get_text()
        
        # Extract activity number and name from header
        header_match = re.search(
            r'(\d{2}-\d{2}-\d+)\s+([A-Z][A-Z0-9\s\'\-\.]+?)(?:\s*Activity Type|\s*$)',
            page_text
        )
        if header_match:
            site_info["activity_number"] = header_match.group(1)
            site_info["location_name"] = header_match.group(2).strip()
        
        # Find all input values (the DNR page uses readonly inputs)
        inputs = soup.find_all('input', {'class': 'form-control'})
        values = [inp.get('value', '').strip() for inp in inputs]
        
        # Map values by position (same as playwright_scraper.py)
        field_map = {
            0: "activity_type",
            1: "status", 
            2: "jurisdiction",
            3: "dnr_region",
            4: "county",
            5: "location_name",
            6: "address",
            7: "municipality",
            8: "plss_description",
            9: "latitude",
            10: "longitude",
            11: "acres",
            12: "facility_id",
            13: "pecfa_number",
            14: "epa_id",
            15: "start_date",
            16: "end_date",
        }
        
        for idx, key in field_map.items():
            if idx < len(values) and values[idx]:
                # Don't overwrite location_name if we got it from header
                if key == "location_name" and "location_name" in site_info:
                    continue
                site_info[key] = values[idx]
        
        # Set risk flags
        status = site_info.get("status", "").upper()
        risk_flags["status_label"] = status if status else "UNKNOWN"
        
        # Check for risk indicators
        activity_type = site_info.get("activity_type", "").upper()
        if activity_type == "LUST" or "petroleum" in page_text.lower():
            risk_flags["petroleum"] = True
        if "pfas" in page_text.lower():
            risk_flags["pfas"] = True
        if any(m in page_text.lower() for m in ['arsenic', 'lead', 'mercury', 'chromium']):
            risk_flags["heavy_metals"] = True
        
        # Extract document links
        for link in soup.find_all('a', href=re.compile(r'download-document|docSeqNo')):
            href = link.get('href', '')
            if href:
                if not href.startswith('http'):
                    href = f"https://apps.dnr.wi.gov{href}"
                
                seq_match = re.search(r'docSeqNo=(\d+)', href)
                seq_no = seq_match.group(1) if seq_match else str(len(documents))
                
                documents.append({
                    "id": len(documents),
                    "download_url": href,
                    "category": "Site File",
                    "name": f"Site File Documentation (ID: {seq_no})",
                    "comment": "DNR site documentation",
                })
        
        # Generate summary
        location = site_info.get("location_name", "Unknown")
        status = site_info.get("status", "Unknown")
        summary = f"Site: {location} - Status: {status}"
        
        return {
            "site_info": site_info,
            "risk_flags": risk_flags,
            "documents": documents,
            "summary": summary,
            "error": None
        }
        
    except requests.Timeout:
        return {
            "site_info": site_info,
            "risk_flags": risk_flags,
            "documents": documents,
            "error": "Request timed out",
            "summary": "Page load timed out"
        }
    except Exception as e:
        return {
            "site_info": site_info,
            "risk_flags": risk_flags,
            "documents": documents,
            "error": str(e),
            "summary": f"Error: {str(e)}"
        }


if __name__ == "__main__":
    # Test
    import sys
    import json
    dsn = sys.argv[1] if len(sys.argv) > 1 else "271147"
    result = scrape_with_browserless(dsn)
    print(json.dumps(result, indent=2))
