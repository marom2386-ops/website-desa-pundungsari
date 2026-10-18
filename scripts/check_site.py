#!/usr/bin/env python3
"""Check visitor-facing pages, links, import content, and the installable theme."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
import json,re,zipfile,xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parents[1]
DATA=json.loads((ROOT/"content/site.json").read_text())
errors=[]
checks=0
def check(ok, message):
    global checks
    checks+=1
    if not ok: errors.append(message)

class Page(HTMLParser):
    def __init__(self,text):
        super().__init__(convert_charrefs=True)
        self.ids=[];self.urls=[];self.h1=0;self.main=0;self.title=False;self.description=False;self.canonical=False;self.labels=set();self.inputs=[]
        self.feed(text)
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if "id" in a:self.ids.append(a["id"])
        for key in ["href","src"]:
            if a.get(key):self.urls.append((tag,key,a[key]))
        if tag=="h1":self.h1+=1
        if tag=="main":self.main+=1
        if tag=="title":self.title=True
        if tag=="meta" and a.get("name")=="description":self.description=bool(a.get("content"))
        if tag=="link" and a.get("rel")=="canonical":self.canonical=True
        if tag=="label":self.labels.add(a.get("for"))
        if tag=="input" and a.get("type")!="hidden":self.inputs.append(a.get("id"))

def check_blocks(path,text):
    stack=[]
    for match in re.finditer(r"<!--\s*(/?)wp:([\w/-]+)(.*?)-->",text,re.S):
        close,name,tail=match.groups()
        tail=tail.strip();selfclose=tail.endswith("/")
        if close:
            check(bool(stack) and stack[-1]==name,f"Unbalanced block close {name}: {path}")
            if stack:stack.pop()
        else:
            payload=tail[:-1].strip() if selfclose else tail
            if payload:
                try:json.loads(payload)
                except Exception as e:errors.append(f"Invalid block attributes: {path}: {e}")
            if not selfclose:stack.append(name)
    check(not stack,f"Unclosed blocks: {path}: {stack}")

def main():
    pages={p:Page(p.read_text()) for p in list(ROOT.glob("*.html"))+list((ROOT/"berita").glob("*.html"))}
    for p,page in pages.items():
        rel=p.relative_to(ROOT)
        text=p.read_text()
        check(page.h1==1,f"{rel}: expected one main heading")
        check(page.main==1,f"{rel}: expected one main landmark")
        check(page.title and page.description and page.canonical,f"{rel}: missing page metadata")
        check(len(page.ids)==len(set(page.ids)),f"{rel}: duplicate IDs")
        check("PIN_DEMO" not in text and "PIN <b>1234" not in text,f"{rel}: demo login is still public")
        check(not any(n in text for n in ["4.179","4.167","1.115.723.251","1.115.723.252"]),f"{rel}: inconsistent statistics escaped the publication filter")
        for field in page.inputs:check(field in page.labels,f"{rel}: input has no visible label")
        for tag,key,url in page.urls:
            parts=urlsplit(url)
            if parts.scheme or parts.netloc or url.startswith("data:"):continue
            target=(p.parent/unquote(parts.path)).resolve() if parts.path else p
            if parts.path.endswith("/"):target=target/"index.html"
            check(target.is_relative_to(ROOT),f"{rel}: link escaped site root: {url}")
            check(target.exists(),f"{rel}: broken local resource {url}")
            if parts.fragment and target.suffix==".html" and target in pages:
                check(unquote(parts.fragment) in pages[target].ids,f"{rel}: broken fragment {url}")
        for s in re.findall(r'<script type="application/ld\+json">(.*?)</script>',text,re.S):
            try:json.loads(s)
            except Exception as e:errors.append(f"{rel}: invalid structured data: {e}")
    check(len(DATA["layanan"])==17,"Expected 17 original service categories")
    check(len({s["id"] for s in DATA["layanan"]})==len(DATA["layanan"]),"Service IDs must be unique")
    check(not any((ROOT/p).exists() for p in ["assets/js/admin.js","assets/js/data.js","assets/css/admin.css"]),"Legacy demo assets remain in the deployment")
    for n in DATA["berita"]:
        p=ROOT/"berita"/(n["slug"]+".html")
        check(p.exists(),f"Missing shareable article {n['slug']}")
        check(n["judul"] in p.read_text(),f"Article title changed unexpectedly: {n['slug']}")
    sitemap=ET.parse(ROOT/"sitemap.xml")
    urls=sitemap.findall(".//{http://www.sitemaps.org/schemas/sitemap/0.9}loc")
    check(len(urls)==12,"Sitemap should contain eight public pages and four articles")
    for loc in urls:check((ROOT/loc.text.split("/website-desa-pundungsari/",1)[1]).exists(),"Sitemap points at a missing page")
    theme=ROOT/"wordpress/pundungsari"
    conf=json.loads((theme/"theme.json").read_text())
    check(conf["version"]==3 and "styles" in conf,"Theme configuration missing")
    check("styles" in conf and "css" in conf["styles"],"Theme CSS is not wired to native global styles")
    check("Theme Name: Pundungsari" in (theme/"style.css").read_text(),"WordPress theme header missing")
    check(not list(theme.rglob("*.php")),"Block theme should not require custom PHP")
    for p in list((theme/"templates").glob("*.html"))+list((theme/"parts").glob("*.html")):
        check_blocks(p.relative_to(ROOT),p.read_text())
    with zipfile.ZipFile(ROOT/"downloads/pundungsari-wordpress.zip") as z:
        check(z.testzip() is None,"WordPress ZIP is corrupt")
        names=z.namelist()
        for req in ["pundungsari/style.css","pundungsari/theme.json","pundungsari/templates/index.html","pundungsari/templates/front-page.html","pundungsari/parts/header.html","pundungsari/assets/images/lambang-lumajang.png"]:
            check(req in names,f"Theme archive missing {req}")
        check(all(n.startswith("pundungsari/") and ".." not in Path(n).parts for n in names),"Unsafe ZIP paths")
        for p in theme.rglob("*"):
            if p.is_file():check(z.read("pundungsari/"+str(p.relative_to(theme)))==p.read_bytes(),f"ZIP source mismatch {p}")
    ns={"wp":"http://wordpress.org/export/1.2/","content":"http://purl.org/rss/1.0/modules/content/"}
    wxr=ET.parse(ROOT/"downloads/konten-pundungsari.xml")
    items=wxr.findall("./channel/item")
    check(len(items)==13,"Import should contain eight pages, four articles, and a logo")
    check(len({i.findtext("wp:post_id",namespaces=ns) for i in items})==13,"Import post IDs are not unique")
    imported_pages=[i for i in items if i.findtext("wp:post_type",namespaces=ns)=="page"]
    check(len(imported_pages)==8,"WordPress pages are missing")
    for i in items:
        content=i.findtext("content:encoded",default="",namespaces=ns)
        if content:check_blocks(i.findtext("title"),content)
        check(i.findtext("wp:post_password",default="",namespaces=ns)=="","Unexpected password in imported content")
        check(not any(v in content for v in ["4.179","4.167","1.115.723.251"]),"Unverified data in WordPress content")
    # Native blocks, rather than an opaque HTML dump, keep the imported content editable.
    check(all("<!-- wp:html" not in i.findtext("content:encoded",default="",namespaces=ns) for i in imported_pages),"Imported pages must use editable WordPress blocks")
    if errors:
        print("\n".join(errors))
        raise SystemExit(f"FAILED: {len(errors)} errors in {checks} checks")
    print(f"PASS: {checks} checks across {len(pages)} public/utility pages, local links, structured data, WordPress templates, ZIP, and WXR.")

if __name__=="__main__":main()
