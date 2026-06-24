from __future__ import annotations

import base64
import re
import sys
import xml.etree.ElementTree as ET
from collections import Counter, defaultdict
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse

from PIL import Image

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[1]
SITE = "https://zqcg.cn"
FIXED_TITLE = "加速器(智连全球)官方网站"
FIXED_KEYWORDS = "加速器,游戏加速器,加速器官网,网络加速器,加速器下载"
FIXED_DESCRIPTION = "加速器提供多线路选择、智能节点匹配与稳定连接支持，适配手机和电脑端使用，并包含版本下载、安装步骤、配置方法及常见故障处理内容，查找更方便。"
COPYRIGHT = "© 2026 加速器(智连全球)官方网站. All Rights Reserved"
PLAIN_TARGET = base64.b64decode("aHR0cHM6Ly9rbjUuMzEzNDg2Lnh5ejozNTg4OC8=").decode("ascii")

REQUIRED_FILES = [
    "index.html","route-lab.html","how-it-works.html","device-matrix.html",
    "performance-console.html","work-scenes.html","download.html","journal.html",
    "journal-network-difference.html","journal-node-latency.html","journal-desktop-status.html",
    "journal-mobile-switch.html","journal-remote-work.html","journal-version-update.html",
            "faq.html","about.html","contact.html","privacy.html","party.html",
            "robots.txt","sitemap.xml","assets/css/site.css","assets/js/site.js",
    "assets/js/download.js","assets/images/logo.png","assets/images/favicon-source.png",
    "favicon.ico","assets/images/hero-network.webp","assets/images/route-atlas.webp",
    "assets/images/device-matrix.webp","assets/images/performance-console.webp",
    "assets/images/how-it-works.webp","assets/images/remote-office.webp",
    "assets/images/privacy-layer.webp","assets/images/light-update.webp",
    "assets/images/journal-network-difference.webp","assets/images/journal-node-latency.webp",
    "assets/images/journal-desktop-status.webp","assets/images/journal-mobile-switch.webp",
    "assets/images/journal-remote-work.webp","assets/images/journal-version-update.webp",
    "scripts/generate-assets.py","scripts/validate-site.py",
]

SITEMAP_URLS = [
    "https://zqcg.cn/",
    "https://zqcg.cn/route-lab.html",
    "https://zqcg.cn/how-it-works.html",
    "https://zqcg.cn/device-matrix.html",
    "https://zqcg.cn/performance-console.html",
    "https://zqcg.cn/work-scenes.html",
    "https://zqcg.cn/download.html",
    "https://zqcg.cn/journal.html",
    "https://zqcg.cn/journal-network-difference.html",
    "https://zqcg.cn/journal-node-latency.html",
    "https://zqcg.cn/journal-desktop-status.html",
    "https://zqcg.cn/journal-mobile-switch.html",
    "https://zqcg.cn/journal-remote-work.html",
    "https://zqcg.cn/journal-version-update.html",
    "https://zqcg.cn/faq.html",
    "https://zqcg.cn/about.html",
    "https://zqcg.cn/contact.html",
            "https://zqcg.cn/privacy.html",
]


class Collector(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.tags = []
        self.data = []
        self.skip_depth = 0

    def handle_starttag(self, tag, attrs):
        attrs_dict = {k: (v if v is not None else "") for k, v in attrs}
        self.tags.append((tag.lower(), attrs_dict))
        if tag.lower() in {"script", "style", "svg"}:
            self.skip_depth += 1

    def handle_endtag(self, tag):
        if tag.lower() in {"script", "style", "svg"} and self.skip_depth:
            self.skip_depth -= 1

    def handle_data(self, data):
        if not self.skip_depth:
            self.data.append(data)

    def first_meta(self, name=None, prop=None):
        for tag, attrs in self.tags:
            if tag == "meta":
                if name and attrs.get("name") == name:
                    return attrs.get("content", "")
                if prop and attrs.get("property") == prop:
                    return attrs.get("content", "")
        return ""

    def title(self):
        for index, (tag, attrs) in enumerate(self.tags):
            pass
        m = re.search(r"<title>(.*?)</title>", self.raw, flags=re.I | re.S)
        return re.sub(r"\s+", " ", m.group(1)).strip() if m else ""

    def links(self, rel_value):
        out = []
        for tag, attrs in self.tags:
            if tag == "link" and attrs.get("rel") == rel_value:
                out.append(attrs)
        return out

    def visible_text(self):
        return re.sub(r"\s+", " ", "".join(self.data)).strip()


results = []

def record(kind, message):
    results.append((kind, message))
    print(f"{kind}: {message}")

def parse_html(path: Path):
    text = path.read_text(encoding="utf-8")
    parser = Collector()
    parser.raw = text
    try:
        parser.feed(text)
        parser.close()
        record("PASS", f"{path.name} parsed")
    except Exception as exc:
        record("FAIL", f"{path.name} parse error: {exc}")
    return parser, text

def file_for_url(url):
    parsed = urlparse(url)
    if parsed.path in {"", "/"}:
        return "index.html"
    return parsed.path.lstrip("/")

def check_files():
    for rel in REQUIRED_FILES:
        if (ROOT / rel).is_file():
            record("PASS", f"required file exists: {rel}")
        else:
            record("FAIL", f"missing required file: {rel}")

def check_sitemap():
    text = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    if "index.html" in text:
        record("FAIL", "sitemap contains index.html")
    else:
        record("PASS", "sitemap excludes index.html")
    if "party.html" in text:
        record("FAIL", "sitemap contains party.html")
    else:
        record("PASS", "sitemap excludes party.html")
    root = ET.fromstring(text)
    ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    urls = [loc.text for loc in root.findall("sm:url/sm:loc", ns)]
    if urls == SITEMAP_URLS:
        record("PASS", "sitemap URL list matches requirement")
    else:
        record("FAIL", f"sitemap URL list mismatch: {urls}")
    banned = ["lastmod", "changefreq", "priority"]
    for item in banned:
        if f"<{item}>" in text:
            record("FAIL", f"sitemap contains {item}")
        else:
            record("PASS", f"sitemap omits {item}")

def check_robots():
    expected = "User-agent: *\nAllow: /\n\nSitemap: https://zqcg.cn/sitemap.xml\n"
    actual = (ROOT / "robots.txt").read_text(encoding="utf-8")
    if actual == expected:
        record("PASS", "robots.txt matches requirement")
    else:
        record("FAIL", "robots.txt differs from required content")

def check_html_pages():
    indexable = [file_for_url(url) for url in SITEMAP_URLS]
    html_files = sorted(ROOT.glob("*.html"))
    parsed = {}
    titles = []
    descriptions = []
    class_files = set()
    visible_paragraphs = defaultdict(list)
    all_html = ""
    for path in html_files:
        parser, text = parse_html(path)
        parsed[path.name] = (parser, text)
        all_html += text
        if "zqcg-govcn" in text:
            class_files.add(path.name)

                bad_home_link = "/" + "index.html"
                if bad_home_link in text:
                    record("FAIL", f"{path.name} contains forbidden homepage file link")
                else:
                    record("PASS", f"{path.name} has no homepage file link")

        if path.name in indexable:
            h1_count = sum(1 for tag, _ in parser.tags if tag == "h1")
            if h1_count == 1:
                record("PASS", f"{path.name} has one H1")
            else:
                record("FAIL", f"{path.name} has {h1_count} H1 elements")

            if COPYRIGHT in text:
                record("PASS", f"{path.name} contains fixed copyright")
            else:
                record("FAIL", f"{path.name} missing fixed copyright")

            expected = "https://zqcg.cn/" if path.name == "index.html" else f"https://zqcg.cn/{path.name}"
            canonicals = [attrs.get("href") for tag, attrs in parser.tags if tag == "link" and attrs.get("rel") == "canonical"]
            if canonicals == [expected]:
                record("PASS", f"{path.name} canonical is correct")
            else:
                record("FAIL", f"{path.name} canonical mismatch: {canonicals}")

            title = parser.title()
            desc = parser.first_meta(name="description")
            titles.append((path.name, title))
            descriptions.append((path.name, desc))
            if not title:
                record("FAIL", f"{path.name} missing title")
            if not desc:
                record("FAIL", f"{path.name} missing description")

        if path.name == "index.html":
            if parser.title() == FIXED_TITLE:
                record("PASS", "homepage title fixed exactly")
            else:
                record("FAIL", f"homepage title mismatch: {parser.title()}")
            if parser.first_meta(name="keywords") == FIXED_KEYWORDS:
                record("PASS", "homepage keywords fixed exactly")
            else:
                record("FAIL", "homepage keywords mismatch")
            if parser.first_meta(name="description") == FIXED_DESCRIPTION:
                record("PASS", "homepage description fixed exactly")
            else:
                record("FAIL", "homepage description mismatch")

        if path.name == "party.html":
            if 'name="robots" content="noindex,nofollow,noarchive,nosnippet"' in text and 'name="googlebot" content="noindex,nofollow,noarchive,nosnippet"' in text:
                record("PASS", "party.html contains noindex directives")
            else:
                record("FAIL", "party.html missing noindex directives")
            if 'rel="canonical"' in text:
                record("FAIL", "party.html should not contain canonical")
            else:
                record("PASS", "party.html has no canonical")

        for tag, attrs in parser.tags:
            if tag == "img":
                src = attrs.get("src", "")
                rel = src.lstrip("/")
                if rel.startswith("http"):
                    continue
                if not (ROOT / rel).is_file():
                    record("FAIL", f"{path.name} image missing: {src}")
                elif attrs.get("alt") and attrs.get("title"):
                    record("PASS", f"{path.name} image ok: {src}")
                else:
                    record("FAIL", f"{path.name} image lacks alt/title: {src}")
            if tag == "a" and attrs.get("data-download") == "true":
                required = {
                    "href": "/party.html",
                    "target": "_blank",
                    "rel": "sponsored nofollow noopener noreferrer",
                    "referrerpolicy": "no-referrer",
                }
                for key, value in required.items():
                    if attrs.get(key) != value:
                        record("FAIL", f"{path.name} download link {key} mismatch: {attrs.get(key)}")
                if all(attrs.get(k) == v for k, v in required.items()):
                    record("PASS", f"{path.name} download link attributes ok")

        text_visible = parser.visible_text()
        for para in re.split(r"[。！？]\s*", text_visible):
            norm = re.sub(r"\s+", "", para)
            if len(norm) > 90:
                visible_paragraphs[norm].append(path.name)

    duplicate_titles = [value for value, count in Counter(v for _, v in titles).items() if count > 1]
    duplicate_desc = [value for value, count in Counter(v for _, v in descriptions).items() if count > 1]
    if duplicate_titles:
        record("FAIL", f"duplicate titles found: {duplicate_titles}")
    else:
        record("PASS", "titles are unique")
    if duplicate_desc:
        record("FAIL", f"duplicate descriptions found: {duplicate_desc}")
    else:
        record("PASS", "descriptions are unique")

    if len(class_files) >= 8 and all_html.count("zqcg-govcn") >= 20:
        record("PASS", "zqcg-govcn class marker is distributed")
    else:
        record("FAIL", "zqcg-govcn class marker is not distributed enough")

            friend_link_phrase = "友情" + "链接"
            if friend_link_phrase in all_html:
                record("FAIL", "friend-link wording found")
            else:
        record("PASS", "no friend-link section wording found")

    suspicious = ["display:none", "visibility:hidden", "font-size:0"]
    css_html = all_html + (ROOT / "assets/css/site.css").read_text(encoding="utf-8")
    for item in suspicious:
        if item in css_html.replace(" ", ""):
            record("FAIL", f"suspicious hidden-text style found: {item}")
        else:
            record("PASS", f"no suspicious hidden-text style: {item}")

    duplicate_large = {k: v for k, v in visible_paragraphs.items() if len(set(v)) > 1}
    if duplicate_large:
        record("FAIL", f"duplicate large visible text found in {duplicate_large}")
    else:
        record("PASS", "no duplicate large visible paragraphs")

    hm_count = all_html.count("hm.baidu.com/hm.js?1e9df50324a9cb5b884fc995da1c0c3d")
    push_count = all_html.count("百度自动推送")
    if hm_count == 1:
        record("PASS", "Baidu analytics appears once")
    else:
        record("FAIL", f"Baidu analytics count is {hm_count}")
    if push_count == 1:
        record("PASS", "Baidu auto push appears once")
    else:
        record("FAIL", f"Baidu auto push count is {push_count}")

    return parsed

def check_images():
    for path in sorted((ROOT / "assets/images").glob("*.webp")):
        with path.open("rb") as fh:
            header = fh.read(12)
        if header[:4] == b"RIFF" and header[8:12] == b"WEBP":
            with Image.open(path) as img:
                if img.format == "WEBP" and img.size[0] > 0 and img.size[1] > 0:
                    record("PASS", f"WebP verified: {path.name} {img.size[0]}x{img.size[1]}")
                else:
                    record("FAIL", f"WebP invalid via Pillow: {path.name}")
        else:
            record("FAIL", f"WebP header invalid: {path.name}")
    with Image.open(ROOT / "assets/images/logo.png") as img:
        if img.format == "PNG" and img.size == (600, 160):
            record("PASS", "logo.png is valid PNG")
        else:
            record("FAIL", "logo.png invalid")
    with Image.open(ROOT / "favicon.ico") as img:
        if img.format == "ICO":
            record("PASS", "favicon.ico is valid")
        else:
            record("FAIL", "favicon.ico invalid")

def check_plain_target():
    offenders = []
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        if any(part in {"python-embed", "libwebp", ".git"} for part in path.parts):
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except Exception:
            continue
        if PLAIN_TARGET in text:
            offenders.append(str(path.relative_to(ROOT)))
    if offenders:
        record("FAIL", f"plain third-party URL found outside README: {offenders}")
    else:
        record("PASS", "plain third-party URL is not present in site code")

def keyword_report(parsed):
    print("\n核心词比例报告")
    targets = [
        "index.html","route-lab.html","how-it-works.html","device-matrix.html",
        "performance-console.html","work-scenes.html","download.html","journal.html",
        "faq.html","about.html","privacy.html",
    ] + [urlparse(url).path.lstrip("/") for url in SITEMAP_URLS if "journal-" in url]
    seen = set()
    for name in targets:
        if not name or name in seen or name not in parsed:
            continue
        seen.add(name)
        text = parsed[name][0].visible_text()
        chinese_chars = len(re.findall(r"[\u4e00-\u9fff]", text))
        count = text.count("加速器")
        ratio = (count * len("加速器") / chinese_chars * 100) if chinese_chars else 0
        level = "PASS" if 0 < ratio < 8 else "WARNING"
        print(f"{level}: {name} 加速器 {count} 次，约 {ratio:.2f}%")

def main():
    check_files()
    check_robots()
    check_sitemap()
    parsed = check_html_pages()
    check_images()
    check_plain_target()
    keyword_report(parsed)
    has_fail = any(kind == "FAIL" for kind, _ in results)
    print("\nSUMMARY:", "FAIL" if has_fail else "PASS")
    if has_fail:
        sys.exit(1)


if __name__ == "__main__":
    main()
