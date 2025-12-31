import os
import requests
from datetime import datetime, timedelta
from typing import List, Dict
import logging
import json

logger = logging.getLogger(__name__)

class JobFetcher:
    """Fetch jobs from Adzuna. Requires ADZUNA_APP_ID and ADZUNA_APP_KEY environment variables.

    If credentials are missing, falls back to a small mocked set of jobs to allow local testing.

    Filtering and selection rules:
    - Only jobs posted within the last 5 days are kept
    - Title must contain one of the provided role keywords (case-insensitive)
    - Only the fields title, company, description, posted_date, apply_url are returned
    """

    ADZUNA_URL = "https://api.adzuna.com/v1/api/jobs/us/search/1"

    def __init__(self):
        self.app_id = os.getenv("ADZUNA_APP_ID")
        self.app_key = os.getenv("ADZUNA_APP_KEY")

    def _parse_posted_date(self, date_str: str):
        try:
            # Try ISO format first
            return datetime.fromisoformat(date_str.replace("Z", "+00:00"))
        except Exception:
            try:
                # Fallback: parse common formats
                return datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S")
            except Exception:
                return None

    def _filter_job(self, job: Dict, roles: List[str]) -> bool:
        # recency filter
        created = None
        if job.get("created"):
            created = self._parse_posted_date(job.get("created"))
        elif job.get("created_at"):
            created = self._parse_posted_date(job.get("created_at"))

        if created:
            if datetime.utcnow() - created > timedelta(days=5):
                return False
        # title filter
        title = (job.get("title") or "").lower()
        for r in roles:
            if r.lower() in title:
                return True
        return False

    def _normalize(self, job: Dict) -> Dict:
        created = job.get("created") or job.get("created_at")
        posted_date = None
        if created:
            parsed = self._parse_posted_date(created)
            posted_date = parsed.isoformat() if parsed else None

        return {
            "external_id": str(job.get("id") or job.get("redirect_url") or ""),
            "title": job.get("title"),
            "company": job.get("company" , {}).get("display_name") if isinstance(job.get("company"), dict) else job.get("company"),
            "description": job.get("description"),
            "posted_date": posted_date,
            "apply_url": job.get("redirect_url") or job.get("url") or job.get("apply_url")
        }

    def fetch_jobs(self, roles: List[str], companies: List[str]) -> List[Dict]:
        """Return a list of normalized jobs that match criteria.

        If Adzuna credentials are missing or an error occurs, return a small mocked dataset.
        """
        if not self.app_id or not self.app_key:
            logger.warning("ADZUNA credentials not set - using mocked jobs for local testing")
            # mocked sample jobs
            now = datetime.utcnow()
            mocked = [
                {
                    "id": "mock-1",
                    "title": "Backend Developer",
                    "company": "Amazon",
                    "description": "Work on backend systems with Python and Docker.",
                    "created": (now - timedelta(days=1)).isoformat(),
                    "redirect_url": "https://example.com/apply/1"
                },
                {
                    "id": "mock-2",
                    "title": "Frontend Engineer",
                    "company": "Google",
                    "description": "Frontend work with React and TypeScript.",
                    "created": (now - timedelta(days=3)).isoformat(),
                    "redirect_url": "https://example.com/apply/2"
                }
            ]
            filtered = [self._normalize(j) for j in mocked if self._filter_job(j, roles)]
            return filtered

        params = {
            "app_id": self.app_id,
            "app_key": self.app_key,
            "results_per_page": 50
        }

        # Build query - include roles; company handled client-side when needed
        what = " OR ".join(roles) if roles else ""
        params["what"] = what

        if companies:
            params["company"] = ",".join(companies)

        try:
            resp = requests.get(self.ADZUNA_URL, params=params, timeout=10)
            resp.raise_for_status()
            data = resp.json()
            results = data.get("results", [])
            # Filter and normalize
            jobs = []
            for r in results:
                if not self._filter_job(r, roles):
                    continue
                norm = self._normalize(r)
                # If companies are given, ensure company matches
                if companies:
                    comp = (norm.get("company") or "").lower()
                    if not any(c.lower() in comp for c in companies):
                        continue
                jobs.append(norm)
            return jobs
        except Exception as e:
            logger.exception("Failed to fetch from Adzuna, returning empty list: %s", e)
            return []
