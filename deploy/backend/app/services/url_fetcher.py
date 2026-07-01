"""URL fetching and liveness checking for job postings."""
import re
from pathlib import Path
from typing import Optional
from urllib.parse import urlparse

import httpx

# Common job posting path patterns that indicate a real JD page
_JOB_PATH_PATTERNS = [
    r"/job[s]?/",
    r"/career[s]?/",
    r"/position[s]?/",
    r"/role[s]?/",
    r"/opening[s]?/",
    r"/opportunity/",
    r"/join/",
    r"/work-with-us/",
    r"/about/careers/",
    r"/company/careers/",
]

# Patterns that indicate a dead/closed posting
_DEAD_PATTERNS = [
    r"no longer accepting applications",
    r"position has been filled",
    r"this job is closed",
    r"this posting has expired",
    r"this position is no longer",
    r"we.?re sorry.{0,30}not found",
    r"404",
    r"page not found",
]


class FetchResult:
    def __init__(self, url: str, text: str = "", title: str = "",
                 is_live: bool = True, status_code: int = 0, error: str = ""):
        self.url = url
        self.text = text
        self.title = title
        self.is_live = is_live
        self.status_code = status_code
        self.error = error

    def to_dict(self) -> dict:
        return {
            "url": self.url,
            "text": self.text,
            "title": self.title,
            "is_live": self.is_live,
            "status_code": self.status_code,
            "error": self.error,
        }


async def fetch_job_posting(url: str, timeout: float = 15.0) -> FetchResult:
    """Fetch a job posting URL and extract the job description text.

    Strategy:
    1. HTTP GET with browser-like headers
    2. Check status code and content for liveness signals
    3. Extract readable text (strip nav, footer, scripts)
    4. Return structured result with liveness verdict
    """
    result = FetchResult(url=url)

    # Validate URL
    parsed = urlparse(url)
    if not parsed.scheme or not parsed.netloc:
        result.is_live = False
        result.error = "Invalid URL"
        return result

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
        ),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9,da;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
    }

    try:
        async with httpx.AsyncClient(timeout=timeout, follow_redirects=True, headers=headers) as client:
            resp = await client.get(url)
            result.status_code = resp.status_code
            final_url = str(resp.url)

            if resp.status_code >= 400:
                result.is_live = False
                result.error = f"HTTP {resp.status_code}"
                return result

            html = resp.text
            if not html or len(html) < 200:
                result.is_live = False
                result.error = "Empty or too-short response"
                return result

            # Extract title
            title_match = re.search(r"<title[^>]*>([^<]+)</title>", html, re.I)
            if title_match:
                result.title = title_match.group(1).strip()

            # Extract readable text
            result.text = _extract_text(html)

            # Check for dead-posting signals
            text_lower = result.text.lower()
            for pattern in _DEAD_PATTERNS:
                if re.search(pattern, text_lower):
                    result.is_live = False
                    result.error = f"Dead posting signal: '{pattern}'"
                    break

            # Check if redirected to generic careers page (not a specific JD)
            if result.is_live and final_url != url:
                path = urlparse(final_url).path.lower()
                if path in ("/", "/careers", "/jobs", "/careers/", "/jobs/"):
                    result.is_live = False
                    result.error = f"Redirected to generic careers page: {final_url}"

            # Minimum content check — real JDs have substance
            if result.is_live and len(result.text.strip()) < 100:
                result.is_live = False
                result.error = "Insufficient content (less than 100 chars extracted)"

    except httpx.TimeoutException:
        result.is_live = False
        result.error = "Request timed out"
    except httpx.ConnectError:
        result.is_live = False
        result.error = "Could not connect to server"
    except Exception as e:
        result.is_live = False
        result.error = f"Fetch error: {type(e).__name__}"

    return result


def _extract_text(html: str) -> str:
    """Extract readable text from HTML, stripping scripts, styles, nav, footer."""
    # Remove script and style tags with content
    text = re.sub(r"<script[^>]*>.*?</script>", "", html, flags=re.I | re.S)
    text = re.sub(r"<style[^>]*>.*?</style>", "", text, flags=re.I | re.S)

    # Remove common non-content elements
    for tag in ["nav", "footer", "header", "aside", "noscript"]:
        text = re.sub(rf"<{tag}[^>]*>.*?</{tag}>", "", text, flags=re.I | re.S)

    # Extract text from common content containers first
    content_blocks = []
    container_patterns = [
        r'<main[^>]*>(.*?)</main>',
        r'<article[^>]*>(.*?)</article>',
        r'<div[^>]*class="[^"]*job[^"]*"[^>]*>(.*?)</div>',
        r'<div[^>]*class="[^"]*posting[^"]*"[^>]*>(.*?)</div>',
        r'<div[^>]*class="[^"]*description[^"]*"[^>]*>(.*?)</div>',
        r'<div[^>]*id="[^"]*job[^"]*"[^>]*>(.*?)</div>',
        r'<div[^>]*id="[^"]*posting[^"]*"[^>]*>(.*?)</div>',
        r'<section[^>]*class="[^"]*job[^"]*"[^>]*>(.*?)</section>',
        r'<div[^>]*role="main"[^>]*>(.*?)</div>',
    ]
    for pattern in container_patterns:
        matches = re.findall(pattern, text, flags=re.I | re.S)
        for m in matches:
            clean = _strip_tags(m)
            if len(clean) > 100:
                content_blocks.append(clean)

    if content_blocks:
        # Use the largest content block (likely the JD)
        text = max(content_blocks, key=len)
    else:
        text = _strip_tags(text)

    # Clean up whitespace
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r" {2,}", " ", text)
    return text.strip()


def _strip_tags(html: str) -> str:
    """Remove HTML tags and decode entities."""
    # Replace <br>, <p> with newlines
    text = re.sub(r"<br\s*/?>", "\n", html, flags=re.I)
    text = re.sub(r"</p\s*>", "\n\n", text, flags=re.I)
    text = re.sub(r"</(div|li|h[1-6]|tr)>", "\n", text, flags=re.I)
    # Remove all remaining tags
    text = re.sub(r"<[^>]+>", "", text)
    # Decode common entities
    text = text.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")
    text = text.replace("&quot;", '"').replace("&#39;", "'").replace("&nbsp;", " ")
    text = re.sub(r"&#\d+;", "", text)
    return text
