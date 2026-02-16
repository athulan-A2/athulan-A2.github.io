import json
import re
import sys
import urllib.parse
import urllib.request
from pathlib import Path

import xbmc
import xbmcaddon
import xbmcgui
import xbmcplugin


ADDON = xbmcaddon.Addon()
ADDON_ID = ADDON.getAddonInfo("id")
ADDON_NAME = ADDON.getAddonInfo("name")
ADDON_PATH = Path(ADDON.getAddonInfo("path"))

HANDLE = int(sys.argv[1])
BASE_URL = sys.argv[0]

# Browser-like headers so sites return the same HTML as in a browser (with video embed)
BROWSER_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}


def log(msg):
    """Helper to log messages to Kodi log."""
    # Kodi 19+/Omega use xbmc.LOGINFO constant; keep a safe fallback
    level = getattr(xbmc, "LOGINFO", None)
    if level is None:
        try:
            level = xbmc.LOG_INFO  # older naming, just in case
        except AttributeError:
            level = 0
    xbmc.log(f"[{ADDON_NAME}] {msg}", level)


def get_query():
    """Parse query string parameters from sys.argv[2]."""
    if len(sys.argv) < 3 or not sys.argv[2]:
        return {}
    query_str = sys.argv[2][1:]  # strip leading '?'
    return {k: v[0] for k, v in urllib.parse.parse_qs(query_str).items()}


def build_url(**kwargs):
    """Build a plugin URL with query parameters."""
    return f"{BASE_URL}?{urllib.parse.urlencode(kwargs)}"


def load_dataset():
    """
    Load the crawled dataset JSON.

    Priority:
      1) resources/data inside the installed addon
      2) User's Downloads folder (handy while testing on desktop)
    """
    filename = "dataset_website-content-crawler_2026-01-27_09-48-41-319.json"

    candidates = [
        ADDON_PATH / "resources" / "data" / filename,
        Path.home() / "Downloads" / filename,
    ]

    for data_path in candidates:
        if data_path.is_file():
            log(f"Loading dataset JSON from: {data_path}")
            try:
                with data_path.open("r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as exc:  # noqa: BLE001
                xbmcgui.Dialog().notification(
                    ADDON_NAME,
                    "Failed to load dataset JSON – see log",
                    xbmcgui.NOTIFICATION_ERROR,
                    5000,
                )
                log(f"Error loading dataset JSON from {data_path}: {exc}")
                return None

    # If we get here, nothing was found
    xbmcgui.Dialog().notification(
        ADDON_NAME,
        "Dataset JSON not found (addon/resources or Downloads)",
        xbmcgui.NOTIFICATION_ERROR,
        5000,
    )
    log(
        "Dataset JSON not found. Tried: "
        + ", ".join(str(p) for p in candidates),
    )
    return None


def parse_episodes_by_show(dataset):
    """
    Extract latest episodes from the first object in the dataset.

    The first entry's 'markdown' field contains a bullet list of episodes like:

      *   [Title![Alt](thumb_url)](episode_page_url)

    and sometimes:

      *   [Title](episode_page_url)
    """
    if not dataset:
        return []

    shows: dict[str, list[dict]] = {}

    for entry in dataset:
        url = entry.get("url") or ""
        meta = entry.get("metadata") or {}
        title = meta.get("title") or ""
        thumb = None
        show_name = None
        air_date = None

        # Try to get show info from jsonLd Article
        jsonld_list = meta.get("jsonLd") or []
        for jl in jsonld_list:
            if not isinstance(jl, dict):
                continue
            # Either an Article itself or contains articleSection
            if jl.get("@type") == "Article" or "articleSection" in jl:
                show_name = jl.get("articleSection") or show_name
                # Headline is nicer episode title if present
                title = jl.get("headline") or title
                # image may be dict with url
                image = jl.get("image")
                if isinstance(image, dict):
                    thumb = image.get("url") or thumb
                break

        # Fallback thumb from openGraph og:image
        if not thumb:
            for og in meta.get("openGraph") or []:
                if isinstance(og, dict) and og.get("property") == "og:image":
                    thumb = og.get("content")
                    break

        if not show_name:
            # Try to derive from title by stripping date + channel
            # e.g. "Siragadikka Aasai 27-01-2026 Sun TV Serial - TamilDhool"
            m = re.match(r"(.+?)\s+\d{2}-\d{2}-\d{4}", title)
            if m:
                show_name = m.group(1).strip()

        if not show_name or not url:
            continue

        # Extract air date if present in title
        m_date = re.search(r"(\d{2}-\d{2}-\d{4})", title)
        if m_date:
            air_date = m_date.group(1)

        episode = {
            "title": title.strip() or show_name,
            "page_url": url.strip(),
            "thumb": thumb,
            "show": show_name,
            "date": air_date,
        }

        shows.setdefault(show_name, []).append(episode)

    # Sort episodes for each show by date (newest first) when we have dates
    for show, eps in shows.items():
        shows[show] = sorted(
            eps,
            key=lambda e: e.get("date") or "",
            reverse=True,
        )

    log(f"Parsed episodes for {len(shows)} shows from dataset")
    return shows


def list_latest_episodes():
    """Root view: list all shows as folders."""
    dataset = load_dataset()
    shows = parse_episodes_by_show(dataset) if dataset else {}

    if not shows:
        # Fallback: show a help item so the directory is never empty.
        help_li = xbmcgui.ListItem(
            label="Kolukattai TV – no episodes yet",
            label2="Make sure the dataset JSON is placed in resources/data inside the addon.",
        )
        help_li.setInfo(
            "video",
            {
                "title": "Kolukattai TV – setup help",
                "plot": (
                    "The Kolukattai TV addon is installed, but it could not read any "
                    "episodes from the dataset.\n\n"
                    "Check that the JSON file is located at:\n"
                    "resources/data/dataset_website-content-crawler_2026-01-27_09-48-41-319.json"
                ),
            },
        )
        xbmcplugin.addDirectoryItem(
            handle=HANDLE,
            url="",
            listitem=help_li,
            isFolder=False,
        )
        xbmcplugin.endOfDirectory(HANDLE, succeeded=True)
        return

    # Show list of shows
    for show_name in sorted(shows.keys()):
        episodes = shows[show_name]
        # Use thumb from latest episode if available
        thumb = episodes[0].get("thumb")

        li = xbmcgui.ListItem(label=show_name)
        li.setInfo("video", {"title": show_name})
        if thumb:
            li.setArt({"thumb": thumb, "icon": thumb, "poster": thumb})

        url = build_url(action="list_show", show=show_name)

        xbmcplugin.addDirectoryItem(
            handle=HANDLE,
            url=url,
            listitem=li,
            isFolder=True,
        )

    xbmcplugin.endOfDirectory(HANDLE)


def list_show_episodes(show_name):
    """List all episodes for a given show."""
    dataset = load_dataset()
    shows = parse_episodes_by_show(dataset) if dataset else {}
    episodes = shows.get(show_name, [])

    if not episodes:
        xbmcgui.Dialog().notification(
            ADDON_NAME,
            f"No episodes found for {show_name}",
            xbmcgui.NOTIFICATION_INFO,
            4000,
        )
        xbmcplugin.endOfDirectory(HANDLE, succeeded=False)
        return

    for ep in episodes:
        title = ep["title"]
        li = xbmcgui.ListItem(label=title)
        li.setInfo("video", {"title": title})

        thumb = ep.get("thumb")
        if thumb:
            li.setArt({"thumb": thumb, "icon": thumb, "poster": thumb})

        url = build_url(action="play", page_url=ep["page_url"], title=title)

        xbmcplugin.addDirectoryItem(
            handle=HANDLE,
            url=url,
            listitem=li,
            isFolder=False,
        )

    xbmcplugin.endOfDirectory(HANDLE)


# Extensions Kodi can play (streaming / direct media)
STREAM_EXTENSIONS = (".m3u8", ".mp4", ".mpd", ".ts")


def _is_playable_media_url(url):
    """Return True if URL looks like a direct playable stream (m3u8, mp4, mpd, ts)."""
    if not url or " " in url:
        return False
    url_lower = url.split("?")[0].lower()
    return any(url_lower.endswith(ext) for ext in STREAM_EXTENSIONS)


def _extract_media_urls(html):
    """
    Extract direct media URLs from HTML/JS: .m3u8, .mp4, .mpd, .ts.
    Returns the first URL that looks like a playable stream.
    """
    # Direct URLs in quotes (with optional query string)
    for ext in STREAM_EXTENSIONS:
        pattern = (
            r"(https?://[^\"'<>\\s]+"
            + re.escape(ext)
            + r"[^\"'<>\\s]*)"
        )
        match = re.search(pattern, html, re.IGNORECASE)
        if match:
            url = match.group(1).strip()
            if _is_playable_media_url(url):
                return url

    # HTML5 <video> or <source src="...">
    source_match = re.search(
        r'<source[^>]+src\s*=\s*["\'](https?://[^"\']+)["\']',
        html,
        re.IGNORECASE,
    )
    if source_match:
        url = source_match.group(1).strip()
        if _is_playable_media_url(url):
            return url

    # Common JS/player variable patterns (file, source, src, url)
    js_patterns = [
        r'["\']?(?:file|source|src|url)["\']?\s*:\s*["\'](https?://[^"\']+)["\']',
        r'data-(?:src|file)\s*=\s*["\'](https?://[^"\']+)["\']',
        r"(?:file|source|src|url)\s*=\s*[\"'](https?://[^\"']+)[\"']",
        r'"(?:file|source|src|url)"\s*:\s*"(https?://[^"]+)"',
        r"'(?:file|source|src|url)'\s*:\s*'(https?://[^']+)'",
        r'content["\']?\s*:\s*["\'](https?://[^"\']+\.(?:m3u8|mp4|mpd|ts)[^"\']*)["\']',
    ]
    for pattern in js_patterns:
        match = re.search(pattern, html, re.IGNORECASE)
        if match:
            url = match.group(1).strip()
            if _is_playable_media_url(url):
                return url

    return None


def _dailymotion_video_id(url):
    """Extract Dailymotion video ID from embed or video URL. Returns None if not Dailymotion."""
    if "dailymotion.com" not in url.lower():
        return None
    # e.g. https://www.dailymotion.com/embed/video/x12345 or .../video/k5abc
    match = re.search(r"dailymotion\.com/(?:embed/)?video/([a-zA-Z0-9]+)", url, re.IGNORECASE)
    if match:
        return match.group(1)
    return None


def _find_url_in_json(obj):
    """Recursively find first value that looks like an http stream URL in dict/list."""
    if isinstance(obj, dict):
        if obj.get("url") and isinstance(obj["url"], str) and obj["url"].startswith("http"):
            return obj["url"]
        for v in obj.values():
            u = _find_url_in_json(v)
            if u:
                return u
    elif isinstance(obj, list) and obj:
        u = _find_url_in_json(obj[0])
        if u:
            return u
    return None


def _resolve_dailymotion_stream(video_id):
    """
    Resolve Dailymotion video ID to a playable stream URL using their public metadata API.
    Returns m3u8 (or similar) URL or None.
    """
    api_url = f"https://www.dailymotion.com/player/metadata/video/{video_id}"
    try:
        headers = {
            **BROWSER_HEADERS,
            "Referer": "https://www.dailymotion.com/",
            "Origin": "https://www.dailymotion.com",
        }
        req = urllib.request.Request(api_url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8", errors="ignore"))
        qualities = data.get("qualities") or {}
        # qualities.auto is list of {url, ...}; take first/best
        auto = qualities.get("auto")
        if isinstance(auto, list) and auto:
            first = auto[0]
            if isinstance(first, dict) and first.get("url"):
                return first["url"]
            if isinstance(first, str) and first.startswith("http"):
                return first
            for item in auto:
                if isinstance(item, dict) and item.get("url"):
                    return item["url"]
        # Fallback: quality keys like "720", "480", etc.
        for key in ("720", "1080", "480", "380", "240"):
            lst = qualities.get(key)
            if isinstance(lst, list) and lst:
                first = lst[0]
                if isinstance(first, dict) and first.get("url"):
                    return first["url"]
        # Last resort: any "url" in the whole response
        return _find_url_in_json(data)
    except Exception as exc:  # noqa: BLE001
        log(f"Dailymotion metadata API failed for {video_id}: {exc}")
        return None


def _get_all_iframe_urls(html, page_url):
    """Collect all iframe src (and data-src) URLs from the page."""
    urls = []
    seen = set()
    for pattern in [
        r'<iframe[^>]+src\s*=\s*["\']([^"\']+)["\']',
        r'<iframe[^>]+data-src\s*=\s*["\']([^"\']+)["\']',
    ]:
        for match in re.finditer(pattern, html, re.IGNORECASE):
            raw = match.group(1).strip()
            if not raw or raw.startswith("javascript:") or raw.startswith("data:"):
                continue
            if raw.startswith("//"):
                raw = "https:" + raw
            elif raw.startswith("/") and page_url:
                raw = urllib.parse.urljoin(page_url, raw)
            if raw not in seen and raw.startswith("http"):
                seen.add(raw)
                urls.append(raw)
    return urls


def extract_stream_url_from_page(html, page_url=None, iframe_depth=3):
    """
    Extract a playable stream URL (m3u8, mp4, mpd, ts) from page HTML.
    If the page only has an iframe, fetch the iframe(s) and extract from there.
    Follows up to iframe_depth levels (default 3) and tries all iframes until one yields a stream.
    """
    # 1) First look for direct media URLs in this page
    direct = _extract_media_urls(html)
    if direct:
        return direct

    # 2) Look for Dailymotion video IDs in the page (URL, data-video, script, etc.)
    dm_ids = set()
    has_dm = "dailymotion" in html.lower()
    for m in re.finditer(
        r"dailymotion\.com/(?:embed/)?video/([a-zA-Z0-9]+)", html, re.IGNORECASE
    ):
        dm_ids.add(m.group(1))
    if has_dm:
        for pattern in [
            r'data-video(?:-id)?\s*=\s*["\']([a-zA-Z0-9]+)["\']',
            r'["\']video(?:Id)?["\']\s*:\s*["\']([a-zA-Z0-9]+)["\']',
        ]:
            for m in re.finditer(pattern, html, re.IGNORECASE):
                vid = m.group(1)
                if len(vid) >= 4:
                    dm_ids.add(vid)
    for dm_id in dm_ids:
        log(f"Trying Dailymotion video: {dm_id}")
        stream_url = _resolve_dailymotion_stream(dm_id)
        if stream_url and stream_url.startswith("http"):
            return stream_url

    # 3) Try every iframe on the page until one gives us a stream
    if iframe_depth > 0:
        iframe_urls = _get_all_iframe_urls(html, page_url)
        for iframe_src in iframe_urls:
            # Dailymotion embed: resolve via their metadata API instead of parsing HTML
            dm_id = _dailymotion_video_id(iframe_src)
            if dm_id:
                log(f"Resolving Dailymotion video: {dm_id}")
                stream_url = _resolve_dailymotion_stream(dm_id)
                if stream_url and _is_playable_media_url(stream_url):
                    return stream_url
                # Metadata might return a redirect URL; try using it anyway
                if stream_url and stream_url.startswith("http"):
                    return stream_url
                continue
            # Other iframes: fetch and recurse
            log(f"Following iframe ({iframe_depth} left): {iframe_src}")
            try:
                req = urllib.request.Request(
                    iframe_src,
                    headers={
                        **BROWSER_HEADERS,
                        "Referer": page_url or "",
                    },
                )
                with urllib.request.urlopen(req, timeout=15) as resp:
                    iframe_html = resp.read().decode("utf-8", errors="ignore")
                result = extract_stream_url_from_page(
                    iframe_html, page_url=iframe_src, iframe_depth=iframe_depth - 1
                )
                if result:
                    return result
            except Exception as exc:  # noqa: BLE001
                log(f"Failed to fetch iframe {iframe_src}: {exc}")
                continue

    return None


def play_episode(page_url, title):
    """Fetch the episode page and try to play the embedded stream."""
    log(f"Attempting to play episode from page: {page_url}")

    try:
        req = urllib.request.Request(page_url, headers=BROWSER_HEADERS)
        with urllib.request.urlopen(req, timeout=15) as resp:
            html_bytes = resp.read()
        html = html_bytes.decode("utf-8", errors="ignore")
    except Exception as exc:  # noqa: BLE001
        xbmcgui.Dialog().notification(
            ADDON_NAME,
            "Failed to load episode page",
            xbmcgui.NOTIFICATION_ERROR,
            5000,
        )
        log(f"Error fetching page {page_url}: {exc}")
        xbmcplugin.setResolvedUrl(HANDLE, False, xbmcgui.ListItem())
        return

    stream_url = extract_stream_url_from_page(html, page_url=page_url)
    if not stream_url:
        log("No stream URL found in episode page HTML")
        # Single clear message instead of two different popups
        xbmcgui.Dialog().notification(
            ADDON_NAME,
            "Could not play this video. Source may be unavailable.",
            xbmcgui.NOTIFICATION_ERROR,
            5000,
        )
        xbmcplugin.setResolvedUrl(HANDLE, False, xbmcgui.ListItem())
        return

    log(f"Resolved stream URL: {stream_url}")

    list_item = xbmcgui.ListItem(path=stream_url)
    list_item.setInfo("video", {"title": title})
    # Prevent Kodi from probing the URL (avoids playback errors on HLS/DASH)
    if hasattr(list_item, "setContentLookup"):
        list_item.setContentLookup(False)

    # Tell Kodi how to play the stream (HLS/DASH need inputstream.adaptive)
    url_lower = stream_url.split("?")[0].lower()
    if url_lower.endswith(".m3u8"):
        list_item.setProperty("inputstream", "inputstream.adaptive")
        list_item.setProperty("inputstream.adaptive.manifest_type", "hls")
        if hasattr(list_item, "setMimeType"):
            list_item.setMimeType("application/vnd.apple.mpegurl")
    elif url_lower.endswith(".mpd"):
        list_item.setProperty("inputstream", "inputstream.adaptive")
        list_item.setProperty("inputstream.adaptive.manifest_type", "mpd")
        if hasattr(list_item, "setMimeType"):
            list_item.setMimeType("application/dash+xml")
    elif url_lower.endswith(".ts"):
        if hasattr(list_item, "setMimeType"):
            list_item.setMimeType("video/mp2t")
    elif url_lower.endswith(".mp4"):
        if hasattr(list_item, "setMimeType"):
            list_item.setMimeType("video/mp4")

    xbmcplugin.setResolvedUrl(HANDLE, True, list_item)


def router():
    """Main router for plugin entry."""
    params = get_query()
    action = params.get("action")

    if not action:
        # Default view: list shows
        list_latest_episodes()
    elif action == "list_show":
        show_name = params.get("show")
        if show_name:
            list_show_episodes(show_name)
        else:
            xbmcgui.Dialog().notification(
                ADDON_NAME,
                "Missing show name",
                xbmcgui.NOTIFICATION_ERROR,
                4000,
            )
            xbmcplugin.endOfDirectory(HANDLE, succeeded=False)
    elif action == "play":
        page_url = params.get("page_url")
        title = params.get("title", "Kolukattai TV")
        if page_url:
            play_episode(page_url, title)
        else:
            xbmcgui.Dialog().notification(
                ADDON_NAME,
                "Missing page URL",
                xbmcgui.NOTIFICATION_ERROR,
                4000,
            )
            xbmcplugin.setResolvedUrl(HANDLE, False, xbmcgui.ListItem())
    else:
        log(f"Unknown action: {action}")
        xbmcplugin.endOfDirectory(HANDLE, succeeded=False)


if __name__ == "__main__":
    try:
        router()
    except Exception as exc:  # noqa: BLE001
        # Make sure unexpected errors never crash the plugin
        log(f"Unexpected error in Kolukattai TV: {exc}")
        xbmcgui.Dialog().notification(
            ADDON_NAME,
            "Kolukattai TV had an unexpected error. See log for details.",
            xbmcgui.NOTIFICATION_ERROR,
            5000,
        )
        try:
            xbmcplugin.endOfDirectory(HANDLE, succeeded=False)
        except Exception:
            # If HANDLE is invalid, just swallow – nothing else we can do
            pass

