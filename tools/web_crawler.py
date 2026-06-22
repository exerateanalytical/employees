"""
Web crawler for ATLAS — competitor monitoring, tender scraping, market research.
Uses httpx + BeautifulSoup for lightweight crawling, Playwright for JS-heavy sites.
"""

from __future__ import annotations

import asyncio
import os
import time
from urllib.parse import urljoin, urlparse

import httpx
from bs4 import BeautifulSoup
from tenacity import retry, stop_after_attempt, wait_exponential


class WebCrawler:
    HEADERS = {
        "User-Agent": (
            "Mozilla/5.0 (compatible; OpesHealthBot/1.0; "
            "+https://opeshealthsystems.com/bot)"
        ),
        "Accept-Language": "en-US,en;q=0.9,fr;q=0.8",
    }
    DELAY = float(os.getenv("CRAWL_DELAY_SECONDS", "2"))

    def __init__(self) -> None:
        self.client = httpx.Client(
            headers=self.HEADERS,
            follow_redirects=True,
            timeout=30,
        )

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(min=2, max=10))
    def fetch(self, url: str) -> str:
        time.sleep(self.DELAY)
        response = self.client.get(url)
        response.raise_for_status()
        return response.text

    def extract_text(self, html: str) -> str:
        soup = BeautifulSoup(html, "lxml")
        for tag in soup(["script", "style", "nav", "footer", "header"]):
            tag.decompose()
        return soup.get_text(separator="\n", strip=True)

    def extract_links(self, html: str, base_url: str) -> list[str]:
        soup = BeautifulSoup(html, "lxml")
        links = []
        for a in soup.find_all("a", href=True):
            href = urljoin(base_url, a["href"])
            if urlparse(href).scheme in ("http", "https"):
                links.append(href)
        return list(set(links))

    def crawl_competitor(self, base_url: str, max_pages: int = 10) -> dict[str, str]:
        """Crawl a competitor site and return {url: text_content}."""
        visited: set[str] = set()
        to_visit = [base_url]
        results: dict[str, str] = {}
        domain = urlparse(base_url).netloc

        while to_visit and len(visited) < max_pages:
            url = to_visit.pop(0)
            if url in visited:
                continue
            try:
                html = self.fetch(url)
                text = self.extract_text(html)
                results[url] = text
                visited.add(url)
                new_links = [
                    link for link in self.extract_links(html, url)
                    if urlparse(link).netloc == domain and link not in visited
                ]
                to_visit.extend(new_links[:5])
            except Exception as e:
                results[url] = f"ERROR: {e}"
                visited.add(url)

        return results

    def scrape_page(self, url: str) -> str:
        """Fetch a single page and return clean text."""
        html = self.fetch(url)
        return self.extract_text(html)

    def check_for_changes(self, url: str, previous_hash: str) -> tuple[bool, str]:
        """Return (changed, new_hash) for monitoring page changes."""
        import hashlib
        content = self.scrape_page(url)
        new_hash = hashlib.md5(content.encode()).hexdigest()
        return new_hash != previous_hash, new_hash

    def search_tenders(self, sources: list[str], keywords: list[str]) -> list[dict]:
        """Search tender portals for matching opportunities."""
        results = []
        for source_url in sources:
            try:
                html = self.fetch(source_url)
                text = self.extract_text(html)
                for keyword in keywords:
                    if keyword.lower() in text.lower():
                        results.append({
                            "source": source_url,
                            "keyword_matched": keyword,
                            "snippet": self._extract_snippet(text, keyword, 300),
                        })
            except Exception as e:
                results.append({"source": source_url, "error": str(e)})
        return results

    def _extract_snippet(self, text: str, keyword: str, window: int = 300) -> str:
        idx = text.lower().find(keyword.lower())
        if idx == -1:
            return text[:window]
        start = max(0, idx - window // 2)
        end = min(len(text), idx + window // 2)
        return text[start:end].strip()

    def close(self) -> None:
        self.client.close()

    def __enter__(self) -> "WebCrawler":
        return self

    def __exit__(self, *_) -> None:
        self.close()
