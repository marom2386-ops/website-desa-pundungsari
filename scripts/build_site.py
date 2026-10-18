#!/usr/bin/env python3
"""Build the public GitHub Pages website and the native WordPress block theme."""
from pathlib import Path
from html import escape
from urllib.parse import quote
from datetime import date
import json
import shutil
import zipfile
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
DATA = json.loads((ROOT / "content/site.json").read_text())
D = DATA["desa"]
BASE = "https://marom2386-ops.github.io/website-desa-pundungsari/"
REPO = "https://github.com/marom2386-ops/website-desa-pundungsari"
WP_BASE = "https://desa-pundungsari.great-site.net/"
WP_ADMIN = "https://desa-pundungsari.great-site.net/wp-admin/"
UPDATED = DATA["updated"]
PHONE = "62" + D["telepon"].lstrip("0")
WA = "https://wa.me/" + PHONE
MAP = "https://www.google.com/maps/search/?api=1&query=" + quote("Balai Desa Pundungsari, Tempursari, Lumajang")
E = lambda value: escape(str(value), quote=True)
MONTHS = ["", "Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"]

def tanggal(value):
    d = date.fromisoformat(value)
    return f"{d.day} {MONTHS[d.month]} {d.year}"

def wa(message="Halo Pemerintah Desa Pundungsari, saya ingin memperoleh informasi pelayanan."):
    return WA + "?text=" + quote(message)

def write(path, content):
    path = ROOT / path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8")

ICONS = {
    "arrow": '<path d="M5 12h14m-6-6 6 6-6 6"/>',
    "file": '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8Z"/><path d="M14 2v6h6M8 13h8M8 17h6"/>',
    "news": '<path d="M4 4h14v16H6a2 2 0 0 1-2-2V4ZM18 8h3v10a2 2 0 0 1-2 2H6M8 8h6M8 12h6M8 16h4"/>',
    "chart": '<path d="M4 3v18h17M8 16v-5M13 16V7M18 16v-8"/>',
    "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
    "pin": '<path d="M20 10c0 6-8 12-8 12S4 16 4 10a8 8 0 1 1 16 0Z"/><circle cx="12" cy="10" r="2.5"/>',
    "phone": '<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 2 .7 2.9a2 2 0 0 1-.4 2.1L8.1 10a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.9.6 2.9.7a2 2 0 0 1 1.6 1.9Z"/>',
}

def icon(name, cls=""):
    return f'<svg class="{E(cls)}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICONS[name]}</svg>'

NAV = [("beranda","index.html","Beranda"),("profil","profil.html","Profil Desa"),("pemerintahan","pemerintahan.html","Pemerintahan"),("layanan","layanan.html","Layanan"),("transparansi","transparansi.html","Transparansi"),("berita","berita.html","Berita"),("kontak","kontak.html","Kontak")]

def header(prefix, current):
    links = "".join(f'<a href="{prefix}{path}"' + (' aria-current="page"' if key == current else '') + f'>{label}</a>' for key,path,label in NAV)
    return f'''<a class="skip-link" href="#main-content">Langsung ke isi</a>
<header>
 <div class="utility"><div class="wrap"><span>Pemerintah Desa Pundungsari · Kabupaten Lumajang</span><span class="service-hours">{E(D["jamLayanan"])}</span></div></div>
 <div class="wrap masthead modern-masthead">
  <a class="brand" href="{prefix}index.html"><img src="{prefix}assets/img/lambang-lumajang.png" alt="Lambang Kabupaten Lumajang" width="45" height="60"><span><small>Pemerintah Desa</small><strong>Pundungsari</strong><span>Kecamatan Tempursari · Kabupaten Lumajang</span></span></a>
  <nav class="main-nav" aria-label="Menu utama"><div class="nav-inner">{links}</div></nav>
  <a class="button nav-cta" href="{E(wa())}" target="_blank" rel="noopener noreferrer">Hubungi desa ↗</a>
 </div>
</header>'''

def footer(prefix):
    return f'''<footer class="site-footer"><div class="wrap">
 <div class="footer-grid">
  <div><strong class="footer-brand">Desa Pundungsari</strong><p>Kecamatan Tempursari, Kabupaten Lumajang<br>Provinsi Jawa Timur</p><p>{E(D["alamat"])}<br>Jawa Timur {E(D["kodePos"])}</p></div>
  <div><h2>Informasi desa</h2><ul><li><a href="{prefix}profil.html">Profil Desa</a></li><li><a href="{prefix}pemerintahan.html">Pemerintahan</a></li><li><a href="{prefix}transparansi.html">Transparansi &amp; dokumen</a></li><li><a href="{prefix}berita.html">Berita Desa</a></li></ul></div>
  <div><h2>Pelayanan</h2><ul><li><a href="{prefix}layanan.html">Panduan layanan</a></li><li><a href="{E(wa())}" target="_blank" rel="noopener noreferrer">WhatsApp: {E(D["telepon"])}</a></li><li><a href="mailto:{E(D["email"])}">{E(D["email"])}</a></li><li><a href="{prefix}kontak.html">Alamat &amp; lokasi kantor</a></li></ul></div>
 </div>
 <div class="copyright"><span>© 2026 Pemerintah Desa Pundungsari</span><span><a href="{prefix}privasi.html">Privasi</a> · <a href="{prefix}admin.html">Pengelola</a></span></div>
</div></footer>'''

def band():
    return f'''<section class="contact-band"><div class="wrap"><div><h2>Perlu informasi lebih lanjut?</h2><p>Hubungi petugas atau datang ke kantor desa pada jam pelayanan.</p></div><a class="button gold" href="{E(wa())}" target="_blank" rel="noopener noreferrer">Hubungi pemerintah desa {icon("arrow")}</a></div></section>'''

def page(path, title, desc, body, current="", noindex=False, contact=True, article=None):
    prefix = "../" * path.count("/")
    canonical = BASE + path
    schema = {"@context":"https://schema.org","@type":"GovernmentOrganization","name":"Pemerintah Desa Pundungsari","url":BASE,"telephone":"+"+PHONE,"email":D["email"],"address":{"@type":"PostalAddress","streetAddress":"Jalan Raya Pundungsari Nomor 16","addressLocality":"Tempursari, Lumajang","addressRegion":"Jawa Timur","postalCode":D["kodePos"],"addressCountry":"ID"}}
    if article:
        schema = {"@context":"https://schema.org","@type":"NewsArticle","headline":article["judul"],"datePublished":article["tanggal"]+"T00:00:00+07:00","dateModified":UPDATED+"T00:00:00+07:00","mainEntityOfPage":canonical,"publisher":{"@type":"GovernmentOrganization","name":"Pemerintah Desa Pundungsari","url":BASE}}
    metadata = json.dumps(schema, ensure_ascii=False).replace("<", "\\u003c")
    html = f'''<!doctype html>
<html lang="id"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(title)} — Desa Pundungsari</title><meta name="description" content="{E(desc)}">
<link rel="canonical" href="{E(canonical)}"><meta name="theme-color" content="#143e32">
<meta property="og:type" content="{"article" if article else "website"}"><meta property="og:locale" content="id_ID"><meta property="og:site_name" content="Desa Pundungsari"><meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(desc)}"><meta property="og:url" content="{E(canonical)}"><meta property="og:image" content="{BASE}assets/img/lambang-lumajang.png">
<meta name="twitter:card" content="summary"><link rel="icon" href="{prefix}assets/img/lambang-lumajang.png" type="image/png">
{('<meta name="robots" content="noindex,follow">' if noindex else '')}
{(f'<base href="{BASE}">' if path == '404.html' else '')}
<link rel="stylesheet" href="{prefix}assets/css/public.css"><link rel="stylesheet" href="{prefix}assets/css/modern.css"><script defer src="{prefix}assets/js/public.js"></script>
<script type="application/ld+json">{metadata}</script></head><body>
{header(prefix,current)}<main id="main-content">{body}</main>{band() if contact else ''}{footer(prefix)}
</body></html>'''
    write(path, html)

def intro(title, text):
    return f'<div class="page-intro"><div class="wrap"><div class="breadcrumbs"><a href="index.html">Beranda</a><span aria-hidden="true">/</span><span>{E(title)}</span></div><h1>{E(title)}</h1><p>{E(text)}</p></div></div>'

def aside():
    return f'<aside><div class="aside-box"><h2>Informasi pelayanan</h2><p>{E(D["jamLayanan"])}</p><p>{E(D["alamat"])}</p><p>Telepon / WhatsApp<br><a href="tel:+{PHONE}">{E(D["telepon"])}</a></p><a class="button" href="{E(wa())}" target="_blank" rel="noopener noreferrer">Tanyakan kepada petugas</a></div></aside>'

def news_card(n, prefix=""):
    return f'''<article class="news-card" data-search-text="{E(n["judul"]+" "+n["ringkasan"]+" "+n["kategori"])}"><div><span class="tag">{E(n["kategori"])}</span><time datetime="{n["tanggal"]}">{tanggal(n["tanggal"])}</time></div><h3><a href="{prefix}berita/{n["slug"]}.html">{E(n["judul"])}</a></h3><p>{E(n["ringkasan"])}</p><a class="text-link" href="{prefix}berita/{n["slug"]}.html">Baca informasi<span class="sr-only">: {E(n["judul"])}</span> →</a></article>'''

def search_ui(target, label, placeholder):
    return f'<div class="search-box" data-search-ui hidden><label for="cari-{target}">{label}</label><input id="cari-{target}" type="search" placeholder="{E(placeholder)}" data-filter="{target}" data-empty="kosong-{target}" aria-describedby="jumlah-{target}"></div><p id="jumlah-{target}" class="result-count" role="status" aria-live="polite"></p>'

def empty(target):
    return f'<p class="empty-state" id="kosong-{target}" hidden>Informasi belum ditemukan. Coba kata lain atau <a href="kontak.html">hubungi petugas desa</a>.</p>'

def build_public():
    tiles="".join(f'<article class="service-tile tile-{i}">{icon(ic)}<h3>{title}</h3><p>{desc}</p><a href="{url}">{label} ↗</a></article>' for i,(ic,title,desc,label,url) in enumerate([
        ("file","Kependudukan","Panduan awal KTP-el, KK, kelahiran, dan administrasi penduduk.","Temukan panduan","layanan.html#ktp-el"),
        ("news","Surat & pengantar","Informasi surat keterangan, usaha, serta keperluan administrasi.","Lihat layanan","layanan.html"),
        ("chart","Informasi publik","Kenali informasi perencanaan, anggaran, dan dokumen desa.","Buka informasi","transparansi.html"),
        ("pin","Kontak & lokasi","Alamat kantor, jam pelayanan, dan saluran komunikasi desa.","Hubungi desa","kontak.html")]))
    body = f'''<section class="hero"><div class="wrap hero-grid"><div class="hero-copy"><span class="eyebrow hero-label">Ruang informasi warga</span><h1>Pundungsari.<br><em>Lebih dekat,<br>lebih terhubung.</em></h1><p class="lead">Temukan panduan layanan, kenali potensi desa, dan ikuti kabar Pundungsari. Semua berawal dari informasi yang mudah dijangkau.</p><div class="button-row"><a class="button" href="layanan.html">Jelajahi layanan ↗</a><a class="button outline" href="profil.html">Kenali desa kami →</a></div><p class="hero-location">TEMPURSARI · LUMAJANG · JAWA TIMUR</p></div><figure class="village-visual"><img class="hero-scene" src="assets/img/pundungsari-landscape.svg" width="720" height="760" alt="Ilustrasi suasana perdesaan, bukan foto lokasi Desa Pundungsari"><span class="visual-place">Pundungsari · Lumajang</span><span class="visual-badge">DESA KITA<br>CERITA KITA</span><div class="visual-hours">{icon("clock")}<div><strong>Jam pelayanan kantor desa</strong><span>Senin–Jumat · 08.00–14.00 WIB</span></div></div><figcaption>Ilustrasi suasana perdesaan</figcaption></figure></div></section>
<section class="section service-section"><div class="wrap"><div class="section-head"><div><span class="eyebrow">Dari kebutuhan sehari-hari</span><h2>Ada yang bisa kami bantu?</h2></div><a class="text-link" href="layanan.html">Semua layanan ↗</a></div><div class="service-tiles">{tiles}</div></div></section>
<section class="section about-section"><div class="wrap about-panel"><div><span class="eyebrow">Mengenal Pundungsari</span><h2>Berangkat dari desa,<br>tumbuh bersama.</h2></div><div><p>Di Kecamatan Tempursari, Kabupaten Lumajang, Pundungsari memiliki cerita tentang pertanian, usaha desa, dan kegiatan masyarakat. Kenali lebih dekat potensi serta arah pembangunan desa kita.</p><a class="button gold" href="profil.html">Jelajahi profil desa ↗</a><p class="about-links"><a href="pemerintahan.html">Pemerintahan desa →</a><a href="transparansi.html">Transparansi →</a></p></div></div></section>
<section class="section tint"><div class="wrap"><div class="section-head"><div><span class="eyebrow">Cerita dari desa kita</span><h2>Kabar Pundungsari</h2></div><a class="text-link" href="berita.html">Semua berita ↗</a></div><div class="news-grid">{''.join(news_card(n) for n in DATA["berita"][:3])}</div></div></section>'''
    page("index.html","Portal Informasi Pemerintah Desa","Informasi Desa Pundungsari, Kecamatan Tempursari, Kabupaten Lumajang: profil, layanan warga, berita, transparansi, dan kontak kantor desa.",body,"beranda")

    misi = "".join(f"<li>{E(m)}</li>" for m in DATA["profil"]["misi"])
    body = intro("Profil Desa","Mengenal Desa Pundungsari, Kecamatan Tempursari, Kabupaten Lumajang.") + f'''<section class="section"><div class="wrap content-grid"><div class="prose"><h2>Desa Pundungsari</h2><p>Desa Pundungsari berada di Kecamatan Tempursari, Kabupaten Lumajang, Provinsi Jawa Timur. Portal ini menyajikan informasi pemerintahan desa, panduan pelayanan, dan kegiatan masyarakat.</p><h2>Visi pembangunan desa</h2><p class="meta">Periode RPJMDes {E(DATA["profil"]["periode"])}</p><div class="note"><p>{E(DATA["profil"]["visi"])}</p></div><h3>Misi</h3><ol>{misi}</ol><h2>Potensi &amp; kegiatan masyarakat</h2><h3>Pertanian</h3><p>Pertanian menjadi salah satu kegiatan masyarakat, antara lain komoditas cabai, pisang, dan palawija.</p><h3>BUMDesa Sumber Rejeki</h3><p>Pengembangan usaha desa mencakup kegiatan BUMDesa Sumber Rejeki, termasuk pengelolaan Taman Pundungsari dan usaha perikanan.</p><h3>Perpustakaan Desa Kasih Ibu</h3><p>Perpustakaan desa menjadi bagian dari kegiatan literasi masyarakat Pundungsari.</p><h2>Identitas wilayah</h2><table><tbody><tr><th scope="row">Desa</th><td>Pundungsari</td></tr><tr><th scope="row">Kecamatan</th><td>Tempursari</td></tr><tr><th scope="row">Kabupaten</th><td>Lumajang</td></tr><tr><th scope="row">Provinsi</th><td>Jawa Timur</td></tr></tbody></table><p>Untuk memperoleh data statistik kependudukan dan wilayah terbaru, hubungi pelayanan informasi desa.</p></div>{aside()}</div></section>'''
    page("profil.html","Profil Desa","Profil, visi dan misi, potensi, serta identitas wilayah Desa Pundungsari.",body,"profil")

    cards = ""
    for i,p in enumerate(DATA["perangkat"]):
        initials = "".join(w[0] for w in p["nama"].split()[:2])
        cards += f'<article class="staff-card{" leader" if i == 0 else ""}"><span class="staff-initial" aria-hidden="true">{E(initials)}</span><small>{E(p["jabatan"])}</small><h2>{E(p["nama"])}</h2></article>'
    body = intro("Pemerintahan Desa","Mengenal perangkat yang tercantum dalam informasi Pemerintah Desa Pundungsari.") + f'<section class="section"><div class="wrap"><div class="staff-grid">{cards}</div><p class="legal-line" style="margin-top:24px">Informasi perangkat mengikuti pembaruan pemerintah desa. Untuk koordinasi pelayanan, gunakan kontak kantor desa.</p></div></section>'
    page("pemerintahan.html","Pemerintahan Desa","Informasi Pj. Kepala Desa dan perangkat Pemerintah Desa Pundungsari.",body,"pemerintahan")

    details = ""
    for s in DATA["layanan"]:
        awal = "".join(f"<li>{E(t)}</li>" for t in s["awal"])
        details += f'<details class="service-detail" id="{s["id"]}" data-search-text="{E(s["nama"]+" "+s["deskripsi"]+" "+s["kata_kunci"])}"><summary>{E(s["nama"])}</summary><div class="service-body"><p>{E(s["deskripsi"])}</p><h3>Bahan awal untuk konsultasi</h3><ul>{awal}</ul><p>Persyaratan akhir, biaya sesuai ketentuan, serta waktu penyelesaian dikonfirmasi kepada petugas berdasarkan jenis layanan dan kelengkapan berkas.</p><a class="button outline" href="{E(wa("Halo Pemerintah Desa Pundungsari, saya ingin menanyakan "+s["nama"]+"."))}" target="_blank" rel="noopener noreferrer">Tanyakan layanan ini {icon("arrow")}</a></div></details>'
    steps = '<ol class="steps"><li><strong>Pilih layanan</strong>Kenali keperluan dan baca panduan singkatnya.</li><li><strong>Siapkan berkas</strong>Bawa dokumen yang tersedia atau tanyakan petugas terlebih dahulu.</li><li><strong>Datang / hubungi</strong>Ajukan keperluan pada jam pelayanan kantor desa.</li><li><strong>Ikuti arahan</strong>Petugas memeriksa berkas dan menjelaskan tindak lanjut.</li></ol>'
    body = intro("Panduan Layanan","Temukan informasi awal pengurusan administrasi. Pilih jenis layanan untuk melihat penjelasannya.") + f'<section class="section"><div class="wrap content-grid"><div>{search_ui("layanan","Cari layanan","Contoh: KK, KTP, usaha, kelahiran")}<div id="layanan" class="service-list">{details}</div>{empty("layanan")}<div class="note"><p>Daftar di atas membantu persiapan awal. Pelayanan dan penerbitan dokumen mengikuti kewenangan masing-masing instansi.</p></div></div>{aside()}</div></section><section class="section tint"><div class="wrap"><span class="eyebrow">Langkah pelayanan</span><h2>Alur yang mudah diikuti</h2>{steps}</div></section>'
    page("layanan.html","Panduan Layanan Warga","Cari panduan 17 layanan administrasi Desa Pundungsari, bahan awal konsultasi, alur, jam, dan kontak pelayanan.",body,"layanan")

    docs = [("Anggaran desa","Tanyakan APBDes, perubahan APBDes, serta informasi anggaran berdasarkan tahun yang diperlukan."),("Realisasi & pelaksanaan","Tanyakan laporan realisasi anggaran dan informasi pelaksanaan kegiatan yang dapat diberikan kepada publik."),("Perencanaan pembangunan","Tanyakan dokumen perencanaan seperti RKPDesa dan informasi prioritas pembangunan desa."),("Peraturan desa","Tanyakan peraturan desa dan dokumen kebijakan sesuai judul, nomor, atau tahun yang diperlukan.")]
    cards = "".join(f'<article class="document-card"><h2>{title}</h2><p>{desc}</p><a class="text-link" href="{E(wa("Halo Pemerintah Desa Pundungsari, saya ingin memperoleh informasi mengenai "+title.lower()+"."))}" target="_blank" rel="noopener noreferrer">Minta informasi →</a></article>' for title,desc in docs)
    body = intro("Transparansi & Dokumen","Saluran untuk memperoleh informasi anggaran, pembangunan, dan peraturan Desa Pundungsari.") + f'<section class="section"><div class="wrap"><div class="note"><p>Dokumen unduhan belum tersedia pada halaman ini. Untuk memperoleh informasi yang diperlukan, sampaikan jenis dokumen dan tahunnya kepada petugas desa.</p></div><div class="document-grid">{cards}</div><div class="prose" style="margin-top:42px"><h2>Cara meminta informasi</h2><ol><li>Sebutkan informasi atau dokumen yang diperlukan beserta tahunnya.</li><li>Hubungi petugas melalui WhatsApp, email, atau datang ke kantor desa.</li><li>Petugas akan menjelaskan ketersediaan dan cara memperoleh informasi tersebut.</li></ol><p><a href="kontak.html">Lihat seluruh kontak pemerintah desa →</a></p></div></div></section>'
    page("transparansi.html","Transparansi dan Dokumen Desa","Informasi publik mengenai anggaran, realisasi, perencanaan pembangunan, dan peraturan Desa Pundungsari.",body,"transparansi")

    body = intro("Berita Desa","Informasi kegiatan pemerintahan dan masyarakat Desa Pundungsari.") + f'<section class="section"><div class="wrap">{search_ui("berita","Cari berita","Cari kegiatan atau kata kunci")}<div class="news-grid listing" id="berita">{''.join(news_card(n) for n in DATA["berita"])}</div>{empty("berita")}</div></section>'
    page("berita.html","Berita dan Kegiatan Desa","Kabar kegiatan pemerintahan dan masyarakat Desa Pundungsari, Tempursari, Lumajang.",body,"berita")
    for n in DATA["berita"]:
        share = "https://wa.me/?text=" + quote(n["judul"]+"\n"+BASE+"berita/"+n["slug"]+".html")
        body = f'<section class="section"><article class="wrap article-shell"><div class="breadcrumbs"><a href="../index.html">Beranda</a><span>/</span><a href="../berita.html">Berita Desa</a></div><span class="eyebrow">{E(n["kategori"])}</span><h1>{E(n["judul"])}</h1><div class="article-meta"><time class="meta" datetime="{n["tanggal"]}">{tanggal(n["tanggal"])}</time><span class="meta">Pemerintah Desa Pundungsari</span></div><div class="article-body"><p>{E(n["ringkasan"])}</p></div><div class="share-row"><p>Bagikan informasi:</p><a class="button outline" href="{E(share)}" target="_blank" rel="noopener noreferrer">WhatsApp</a></div><p style="margin-top:32px"><a class="text-link" href="../berita.html">← Kembali ke Berita Desa</a></p></article></section>'
        page("berita/"+n["slug"]+".html",n["judul"],n["ringkasan"],body,"berita",article=n)

    contactrows = [("Alamat kantor",E(D["alamat"])+", Jawa Timur "+E(D["kodePos"])),("Jam pelayanan",E(D["jamLayanan"])),("Telepon",f'<a href="tel:+{PHONE}">{E(D["telepon"])}</a>'),("Email",f'<a href="mailto:{E(D["email"])}">{E(D["email"])}</a>')]
    rows = "".join(f'<div class="contact-item"><small>{title}</small>{value}</div>' for title,value in contactrows)
    body = intro("Kontak & Lokasi","Hubungi pemerintah desa atau kunjungi kantor pada jam pelayanan.") + f'<section class="section"><div class="wrap contact-grid"><div><span class="eyebrow">Kantor desa</span><h2>Pemerintah Desa Pundungsari</h2>{rows}</div><div class="contact-panel"><h2>Sampaikan keperluan Anda.</h2><p>Untuk bertanya tentang pelayanan atau ketersediaan informasi desa, hubungi petugas melalui saluran berikut.</p><div class="button-row"><a class="button" href="{E(wa())}" target="_blank" rel="noopener noreferrer">Buka WhatsApp {icon("arrow")}</a><a class="button outline" href="{E(MAP)}" target="_blank" rel="noopener noreferrer">Petunjuk lokasi {icon("pin")}</a></div><p class="legal-line" style="margin-top:25px">Petunjuk lokasi dibuka di Google Maps. Pastikan titik tujuan sebelum berangkat.</p></div></div></section>'
    page("kontak.html","Kontak dan Lokasi Kantor","Alamat, jam pelayanan, telepon, WhatsApp, email, dan petunjuk lokasi Kantor Desa Pundungsari.",body,"kontak",contact=False)

    body = intro("Privasi Pengunjung","Informasi singkat mengenai penggunaan situs dan saluran komunikasi.") + '<section class="section"><div class="wrap article-shell prose"><h2>Informasi yang tersedia</h2><p>Website ini menyajikan informasi publik desa. Halaman publik tidak meminta akun, kata sandi, NIK, atau unggahan dokumen kependudukan.</p><h2>Saluran komunikasi</h2><p>Tautan WhatsApp, email, dan Google Maps membuka layanan pihak terkait. Informasi yang Anda kirim melalui layanan tersebut mengikuti pengaturan dan kebijakan layanan masing-masing.</p><h2>Pencarian di halaman</h2><p>Pencarian layanan dan berita memfilter isi yang sudah tampil pada perangkat Anda. Website ini tidak menyimpan kata pencarian melalui fitur tersebut.</p><h2>Hosting website</h2><p>Situs saat ini menggunakan GitHub Pages. Penyedia hosting dapat mencatat informasi teknis kunjungan sesuai kebijakannya.</p><h2>Perbaikan informasi</h2><p>Apabila menemukan informasi yang perlu diperbarui, silakan hubungi pemerintah desa melalui <a href="kontak.html">halaman kontak</a>.</p></div></section>'
    page("privasi.html","Privasi Pengunjung","Informasi privasi pengunjung website Desa Pundungsari dan penggunaan saluran komunikasi.",body,contact=False)

    body = intro("Pusat Pengelola","Akses pengelolaan WordPress dan sumber website di GitHub.") + f'''<section class="section"><div class="wrap"><div class="admin-grid">
<section class="admin-card"><span class="eyebrow">WordPress aktif</span><h2>Kelola berita & halaman</h2><p>Website WordPress sudah aktif pada hosting gratis InfinityFree. Masuk menggunakan akun yang dibuat saat pemasangan untuk memperbarui berita, layanan, dan informasi desa.</p><a class="button" href="{WP_ADMIN}" target="_blank" rel="noopener noreferrer">Masuk ke dasbor WordPress</a><p><a href="{WP_BASE}" target="_blank" rel="noopener noreferrer">Lihat website WordPress →</a></p><p><a href="panduan-wordpress.html">Panduan pengelolaan →</a></p></section>
<section class="admin-card"><span class="eyebrow">Sumber & situs GitHub</span><h2>Kelola sumber website</h2><p>Sumber tema, paket instalasi, dan situs GitHub Pages tetap disimpan di repositori. Untuk memperbarui situs GitHub, ubah konten lalu bangun ulang sesuai panduan proyek.</p><a class="button" href="{REPO}/edit/main/content/site.json" target="_blank" rel="noopener noreferrer">Buka konten di GitHub</a><p><a href="{REPO}/blob/main/README.md" target="_blank" rel="noopener noreferrer">Panduan proyek GitHub →</a></p><p><a href="downloads/pundungsari-wordpress.zip" download>Unduh cadangan tema WordPress</a></p></section>
</div><div class="note"><p>Perubahan melalui dasbor WordPress tersimpan pada hosting WordPress. Situs GitHub diperbarui melalui repositori; keduanya tidak tersinkron otomatis.</p></div></div></section>'''
    page("admin.html","Pusat Pengelola","Dasbor WordPress aktif dan pengelolaan sumber GitHub Desa Pundungsari.",body,noindex=True,contact=False)
    build_guide()
    body = intro("Halaman tidak ditemukan","Alamat yang Anda buka tidak tersedia atau sudah berubah.") + '<section class="section"><div class="wrap"><p>Silakan kembali ke halaman utama atau gunakan menu untuk menemukan informasi desa.</p><a class="button" href="index.html">Kembali ke beranda</a></div></section>'
    page("404.html","Halaman Tidak Ditemukan","Kembali ke portal informasi Desa Pundungsari.",body,noindex=True,contact=False)

def build_guide():
    body = intro("Panduan WordPress","Pengelolaan website Desa Pundungsari yang sudah aktif.") + f'''<section class="section"><div class="wrap article-shell prose">
<div class="note"><p><strong>Sudah aktif:</strong> <a href="{WP_BASE}">website WordPress Desa Pundungsari</a> berjalan di hosting gratis InfinityFree dengan HTTPS. Tema Pundungsari, delapan halaman, 17 panduan layanan, empat ringkasan berita, dan lambang desa sudah terpasang.</p></div>
<h2>Pengelolaan sehari-hari</h2><ol><li><a href="{WP_ADMIN}">Masuk ke dasbor WordPress</a> menggunakan akun pemasangan.</li><li>Berita baru: Pos → Tambah Pos. Isi judul, naskah, dan foto kegiatan yang benar; periksa pratinjau lalu terbitkan.</li><li>Perbarui profil, layanan, kontak, atau transparansi melalui Laman → Semua Laman.</li><li>Ubah tampilan melalui Tampilan → Editor. Identitas situs dan lambang tersedia di Identity.</li><li>Untuk cadangan isi, buka Peralatan → Ekspor → Semua konten. Simpan juga cadangan basis data dan berkas hosting secara berkala.</li></ol><p>Beranda statis, halaman berita, bahasa Indonesia, zona waktu Jakarta, dan permalink nama tulisan sudah diatur. Pemasangan serta impor di bawah hanya diperlukan ketika menyiapkan ulang situs; jangan mengimpor kembali ke situs aktif agar tidak ada konten ganda.</p>
<h2>1. Unduh paket yang diperlukan</h2><ul><li><a href="downloads/pundungsari-wordpress.zip" download>Tema Pundungsari untuk WordPress (.zip)</a></li><li><a href="downloads/konten-pundungsari.xml" download>Konten awal untuk diimpor (.xml)</a></li><li><a href="assets/img/lambang-lumajang.png" download>Lambang Kabupaten Lumajang (.png)</a></li></ul>
<h2>2. Hosting dan alamat</h2><p>WordPress berjalan pada paket gratis InfinityFree di <a href="{WP_BASE}">{WP_BASE}</a>. Sumber tema dan situs GitHub Pages tetap disimpan di repositori. Perubahan isi di WordPress tidak otomatis memperbarui situs GitHub.</p><p>Untuk pemasangan ulang, gunakan hosting yang mendukung PHP, MySQL atau MariaDB, dan HTTPS. Gunakan WordPress versi stabil yang masih didukung, sekurang-kurangnya 6.6 untuk tema ini. Akun hosting sebaiknya tetap dalam pengelolaan desa.</p>
<h2>3. Pasang dan aktifkan tema</h2><ol><li>Pasang WordPress melalui panel hosting.</li><li>Masuk ke dasbor WordPress pada alamat website tujuan, biasanya melalui /wp-admin.</li><li>Buka Tampilan → Tema → Tambah Tema → Unggah Tema.</li><li>Pilih berkas pundungsari-wordpress.zip, pasang, lalu aktifkan.</li></ol>
<h2>4. Impor konten awal</h2><ol><li>Buka Perkakas → Impor → WordPress. Pasang pengimpor resmi apabila diminta.</li><li>Pilih konten-pundungsari.xml, lalu petakan penulis ke akun pengelola desa.</li><li>Pilih unduh dan impor lampiran untuk mengambil lambang dari situs GitHub saat ini, atau unggah lambang secara manual ke Media.</li><li>Jalankan impor satu kali agar tidak menambahkan konten ganda.</li></ol>
<h2>5. Atur identitas dan navigasi</h2><ol><li>Di Pengaturan → Umum, isi judul situs Desa Pundungsari, bahasa Indonesia, dan zona waktu Jakarta.</li><li>Di Pengaturan → Membaca, pilih halaman statis: Beranda untuk halaman utama dan Berita Desa untuk halaman pos.</li><li>Di Pengaturan → Permalink, pilih Nama pos, lalu simpan.</li><li>Di Tampilan → Editor, buka bagian Header. Pilih blok Logo Situs dan gunakan lambang Lumajang yang telah diunggah.</li><li>Periksa menu navigasi. Tema memakai daftar halaman bawaan WordPress; sesuaikan urutannya dan hindari tautan Beranda ganda.</li><li>Periksa nomor telepon, email, jam pelayanan, nama perangkat, serta isi profil sebelum pengumuman resmi.</li></ol>
<h2>6. Kelola berita dan halaman</h2><p>Untuk berita: buka Pos → Tambah Baru, isi judul dan naskah, tambahkan foto kegiatan yang benar, periksa pratinjau, lalu terbitkan. Untuk profil, layanan, pemerintahan, dan kontak: gunakan menu Halaman.</p><p>Tampilan beranda dan kepala/kaki halaman dapat disesuaikan melalui Tampilan → Editor. Tema memakai blok bawaan WordPress; tidak membutuhkan pembuat halaman berbayar.</p><p>Buat akun tersendiri untuk setiap petugas melalui Pengguna. Gunakan peran Editor untuk petugas pengelola isi; akun Administrator digunakan untuk pengaturan situs. Penulis dapat digunakan untuk petugas yang hanya menulis berita.</p>
<h2>7. Lengkapi informasi publik</h2><p>Angka kependudukan dan APBDes belum dimasukkan ke paket publik karena data sumber belum cocok. Periksa catatan verifikasi dalam proyek. Setelah disahkan, masukkan angka beserta periode dan sumbernya, lalu unggah dokumen publik yang sudah diperiksa.</p><p>Empat berita awal mempertahankan ringkasan pada situs sebelumnya. Lengkapi naskah dan dokumentasi berdasarkan kegiatan nyata; paket ini tidak menambahkan kutipan, foto kegiatan, atau angka rekaan.</p>
<h2>8. Pemeliharaan dan pengumuman</h2><ol><li>Periksa perubahan melalui HP dan komputer, termasuk menu, gambar, tautan WhatsApp, dan berita.</li><li>Cadangkan isi, basis data, dan berkas sebelum perubahan besar. Perbarui WordPress, tema, serta plugin dari sumber resmi.</li><li>Lengkapi dokumen transparansi dengan berkas publik yang sudah diperiksa.</li><li>Gunakan alamat website yang sama secara konsisten saat menginformasikan kepada masyarakat.</li></ol>
<h2>Rujukan</h2><ul><li><a href="https://wordpress.org/about/requirements/" target="_blank" rel="noopener noreferrer">Persyaratan hosting WordPress</a></li><li><a href="https://developer.wordpress.org/advanced-administration/wordpress/import/" target="_blank" rel="noopener noreferrer">Panduan impor WordPress</a></li><li><a href="https://wordpress.org/documentation/article/roles-and-capabilities/" target="_blank" rel="noopener noreferrer">Peran akun WordPress</a></li></ul><p class="meta">Disiapkan {tanggal(UPDATED)}.</p></div></section>'''
    page("panduan-wordpress.html","Panduan Pemasangan WordPress","Unduh tema, konten awal, dan panduan pemasangan WordPress untuk Desa Pundungsari.",body,noindex=True,contact=False)

# WordPress block helpers. No custom PHP or third-party page builder is required.
def block(name, inner="", attrs=None, selfclose=False):
    attr = " " + json.dumps(attrs,ensure_ascii=False,separators=(",",":")) if attrs else ""
    return f"<!-- wp:{name}{attr} /-->" if selfclose else f"<!-- wp:{name}{attr} -->{inner}<!-- /wp:{name} -->"

def para(text, cls=""):
    return block("paragraph",f'<p{(" class="+chr(34)+cls+chr(34)) if cls else ""}>{text}</p>',{"className":cls} if cls else None)

def heading(text, level=2):
    return block("heading",f'<h{level} class="wp-block-heading">{text}</h{level}>',{"level":level} if level != 2 else None)

def group(inner, cls="", align=None, tag="div", layout="constrained"):
    attrs={"layout":{"type":layout}}
    if cls: attrs["className"]=cls
    if align: attrs["align"]=align
    if tag != "div": attrs["tagName"]=tag
    classes = "wp-block-group" + (" align"+align if align else "") + (" "+cls if cls else "")
    return block("group",f'<{tag} class="{classes}">{inner}</{tag}>',attrs)

def buttons(items):
    children = "".join(block("button",f'<div class="wp-block-button"><a class="wp-block-button__link wp-element-button" href="{E(url)}">{E(label)}</a></div>') for label,url in items)
    return block("buttons",f'<div class="wp-block-buttons">{children}</div>')

def wp_list(items, ordered=False):
    tag="ol" if ordered else "ul"
    return block("list",f'<{tag} class="wp-block-list">'+''.join(block("list-item",f"<li>{item}</li>") for item in items)+f"</{tag}>",{"ordered":True} if ordered else None)

def wp_columns(items, cls=""):
    cols="".join(block("column",'<div class="wp-block-column">'+item+"</div>") for item in items)
    return block("columns",'<div class="wp-block-columns'+(' '+cls if cls else '')+'">'+cols+"</div>",{"className":cls} if cls else None)

def wp_query(inherit=False):
    query={"perPage":9 if inherit else 3,"pages":0,"offset":0,"postType":"post","order":"desc","orderBy":"date","author":"","search":"","exclude":[],"sticky":"","inherit":inherit}
    entry=group(block("post-date",selfclose=True)+block("post-title",attrs={"isLink":True,"level":2},selfclose=True)+block("post-excerpt",attrs={"moreText":"Baca informasi →","excerptLength":35},selfclose=True),"ps-news-card")
    posts=block("post-template",entry,{"layout":{"type":"grid","columnCount":3}})
    pagination=block("query-pagination",block("query-pagination-previous",selfclose=True)+block("query-pagination-numbers",selfclose=True)+block("query-pagination-next",selfclose=True),{"layout":{"type":"flex","justifyContent":"space-between"}})
    noresults=block("query-no-results",para("Belum ada berita yang sesuai."))
    return block("query",'<div class="wp-block-query">'+posts+pagination+noresults+'</div>',{"queryId":1,"query":query})

def wp_header():
    brand=group(block("site-logo",attrs={"width":36},selfclose=True)+group(block("site-title",attrs={"level":0},selfclose=True)+para("Tempursari · Kabupaten Lumajang","ps-location")),"ps-brand",layout="flex")
    nav=block("navigation",block("page-list",selfclose=True),{"className":"ps-navigation","overlayMenu":"mobile","layout":{"type":"flex","justifyContent":"right"}})
    contact=group(buttons([("Hubungi desa ↗",wa())]),"ps-header-action")
    return group(group(para("Pemerintah Desa Pundungsari · Tempursari, Lumajang"),"ps-top",align="full")+group(brand+nav+contact,"ps-masthead",align="wide",layout="flex"),"ps-header",align="full")

def wp_footer():
    contact=heading("Desa Pundungsari")+para(E(D["alamat"])+", Jawa Timur "+E(D["kodePos"]))+para(E(D["jamLayanan"]))
    links=heading("Tetap terhubung",3)+para(f'<a href="{E(wa())}">WhatsApp: {E(D["telepon"])}</a>')+para(f'<a href="mailto:{E(D["email"])}">{E(D["email"])}</a>')+para(f'<a href="{E(MAP)}">Petunjuk lokasi kantor ↗</a>')
    explore=heading("Jelajahi desa",3)+para('<a href="/?pagename=profil">Profil & potensi desa</a>')+para('<a href="/?pagename=layanan">Panduan layanan</a>')+para('<a href="/?pagename=privasi">Privasi pengunjung</a>')
    return group(group(wp_columns([contact,explore,links])+para("© 2026 Pemerintah Desa Pundungsari · Informasi untuk kita bersama.","ps-footer-note"),align="wide"),"ps-footer",align="full")

def wp_front():
    hero_left=group(para("Ruang informasi warga","ps-eyebrow")+heading('Pundungsari.<br><span class="ps-accent">Lebih dekat,<br>lebih terhubung.</span>',1)+para("Temukan panduan layanan, kenali potensi desa, dan ikuti kabar Pundungsari. Semua berawal dari informasi yang mudah dijangkau.")+buttons([("Jelajahi layanan ↗","/?pagename=layanan"),("Kenali desa kami →","/?pagename=profil")])+para("TEMPURSARI · LUMAJANG · JAWA TIMUR","ps-hero-location"),"ps-hero-copy")
    office=group(para("<strong>Jam pelayanan kantor desa</strong>")+para("Senin–Jumat · 08.00–14.00 WIB","ps-hours"),"ps-office")
    visual=group(para("Pundungsari · Lumajang","ps-place")+para("DESA KITA<br>CERITA KITA","ps-visual-badge")+office+para("Ilustrasi suasana perdesaan","ps-illustration-credit"),"ps-visual")
    hero=group(group(wp_columns([hero_left,visual]),align="wide"),"ps-hero",align="full")
    cards=[]
    for title,desc,label,url,cls in [
        ("Kependudukan","Panduan awal KTP-el, KK, kelahiran, dan administrasi penduduk.","Temukan panduan ↗","/?pagename=layanan#ktp-el","ps-card-citizen"),
        ("Surat & pengantar","Informasi surat keterangan, usaha, serta keperluan administrasi.","Lihat layanan ↗","/?pagename=layanan","ps-card-letter"),
        ("Informasi publik","Kenali informasi perencanaan, anggaran, dan dokumen desa.","Buka informasi ↗","/?pagename=transparansi","ps-card-public"),
        ("Kontak & lokasi","Alamat kantor, jam pelayanan, dan saluran komunikasi desa.","Hubungi desa ↗","/?pagename=kontak","ps-card-contact")]:
        cards.append(group(heading(title,3)+para(desc)+buttons([(label,url)]),"ps-service-card "+cls))
    service_head=group(group(para("Dari kebutuhan sehari-hari","ps-eyebrow")+heading("Ada yang bisa kami bantu?"))+para('<a href="/?pagename=layanan">Semua layanan ↗</a>'),"ps-section-head",layout="flex")
    service_grid=wp_columns(cards,"ps-service-grid")
    services=group(group(service_head+service_grid,align="wide"),"ps-section ps-services-section",align="full")
    about_left=para("Mengenal Pundungsari","ps-eyebrow")+heading("Berangkat dari desa,<br>tumbuh bersama.")
    about_right=para("Di Kecamatan Tempursari, Kabupaten Lumajang, Pundungsari memiliki cerita tentang pertanian, usaha desa, dan kegiatan masyarakat. Kenali lebih dekat potensi serta arah pembangunan desa kita.")+buttons([("Jelajahi profil desa ↗","/?pagename=profil")])+para('<a href="/?pagename=pemerintahan">Pemerintahan desa →</a> &nbsp; <a href="/?pagename=transparansi">Transparansi →</a>',"ps-about-links")
    about=group(group(group(wp_columns([about_left,about_right]),"ps-about"),align="wide"),"ps-section ps-about-section",align="full")
    news_head=group(group(para("Cerita dari desa kita","ps-eyebrow")+heading("Kabar Pundungsari"))+para('<a href="/?pagename=berita">Semua berita ↗</a>'),"ps-section-head",layout="flex")
    news=group(group(news_head+wp_query(False),align="wide"),"ps-section ps-news-section",align="full")
    contact=group(group(heading("Mari tetap terhubung.")+para("Tanyakan keperluan Anda kepada petugas desa pada jam pelayanan."))+buttons([("Hubungi pemerintah desa ↗",wa())]),"ps-contact",align="wide",layout="flex")
    contact=group(contact,"ps-section ps-contact-section",align="full")
    return hero+services+about+news+contact

def wp_pages():
    profile=heading("Desa Pundungsari")+para("Desa Pundungsari berada di Kecamatan Tempursari, Kabupaten Lumajang, Provinsi Jawa Timur.")+heading("Visi pembangunan desa")+para("Periode RPJMDes "+E(DATA["profil"]["periode"]))+para(E(DATA["profil"]["visi"]))+heading("Misi",3)+wp_list([E(m) for m in DATA["profil"]["misi"]],True)+heading("Potensi & kegiatan masyarakat")+para("Pertanian menjadi salah satu kegiatan masyarakat, antara lain komoditas cabai, pisang, dan palawija. Pengembangan usaha desa mencakup kegiatan BUMDesa Sumber Rejeki, pengelolaan Taman Pundungsari, dan usaha perikanan. Perpustakaan Desa Kasih Ibu menjadi bagian dari kegiatan literasi masyarakat.")+para("Untuk data statistik kependudukan dan wilayah terbaru, hubungi pelayanan informasi desa.")
    govt=heading("Perangkat Pemerintah Desa")
    for p in DATA["perangkat"]:
        govt+=heading(E(p["nama"]),3)+para(E(p["jabatan"]))
    services=para("Pilih layanan untuk melihat penjelasan dan bahan awal konsultasi. Persyaratan akhir, biaya sesuai ketentuan, dan waktu penyelesaian dikonfirmasi kepada petugas.")
    for s in DATA["layanan"]:
        inner=f'<details class="wp-block-details" id="{s["id"]}"><summary>{E(s["nama"])}</summary>'+para(E(s["deskripsi"]))+heading("Bahan awal untuk konsultasi",3)+wp_list([E(t) for t in s["awal"]])+para("Pelayanan dan penerbitan dokumen mengikuti kewenangan masing-masing instansi.")+buttons([("Tanyakan layanan ini",wa("Halo Pemerintah Desa Pundungsari, saya ingin menanyakan "+s["nama"]+"."))])+"</details>"
        services+=block("details",inner,{"anchor":s["id"]})
    transparency=para("Dokumen unduhan belum tersedia pada halaman ini. Untuk memperoleh informasi yang diperlukan, sampaikan jenis dokumen dan tahunnya kepada petugas desa.")
    for title,text in [("Anggaran desa","APBDes dan perubahan APBDes berdasarkan tahun yang diperlukan."),("Realisasi dan pelaksanaan","Informasi realisasi anggaran dan pelaksanaan kegiatan yang dapat diberikan kepada publik."),("Perencanaan pembangunan","Dokumen perencanaan dan informasi prioritas pembangunan desa."),("Peraturan desa","Peraturan desa dan dokumen kebijakan sesuai judul, nomor, atau tahun yang diperlukan.")]:
        transparency+=heading(title)+para(text)
    transparency+=buttons([("Minta informasi publik",wa("Halo Pemerintah Desa Pundungsari, saya ingin memperoleh informasi dokumen publik desa."))])
    contact=heading("Kantor Desa Pundungsari")+para(E(D["alamat"])+", Jawa Timur "+E(D["kodePos"]))+para("<strong>Jam pelayanan</strong><br>"+E(D["jamLayanan"]))+para(f'<strong>Telepon</strong><br><a href="tel:+{PHONE}">{E(D["telepon"])}</a>')+para(f'<strong>Email</strong><br><a href="mailto:{E(D["email"])}">{E(D["email"])}</a>')+buttons([("Buka WhatsApp",wa()),("Petunjuk lokasi",MAP)])
    privacy=heading("Informasi pengunjung")+para("Halaman publik tidak meminta NIK, unggahan KK, atau data kependudukan pribadi. Tautan WhatsApp, email, dan Google Maps membuka layanan pihak terkait. Kebijakan privasi perlu diperbarui apabila pengelola menambahkan formulir, analitik, atau layanan lain.")
    return [("Beranda","beranda",para("Portal informasi Pemerintah Desa Pundungsari.")),("Profil Desa","profil",profile),("Pemerintahan","pemerintahan",govt),("Layanan","layanan",services),("Transparansi","transparansi",transparency),("Berita Desa","berita",para("Berita dan kegiatan Desa Pundungsari.")),("Kontak","kontak",contact),("Privasi","privasi",privacy)]

def build_theme():
    theme=ROOT/"wordpress/pundungsari"
    (theme/"templates").mkdir(parents=True,exist_ok=True)
    (theme/"parts").mkdir(exist_ok=True)
    (theme/"assets/images").mkdir(parents=True,exist_ok=True)
    shutil.copyfile(ROOT/"assets/img/lambang-lumajang.png",theme/"assets/images/lambang-lumajang.png")
    write("wordpress/pundungsari/style.css","""/*
Theme Name: Pundungsari
Theme URI: https://github.com/marom2386-ops/website-desa-pundungsari
Author: Pemerintah Desa Pundungsari
Description: Tema blok untuk informasi publik Desa Pundungsari. Dikelola melalui Editor Situs dan blok bawaan WordPress.
Version: 2.0.0
Requires at least: 6.6
Requires PHP: 7.4
License: GPL-2.0-or-later
License URI: https://www.gnu.org/licenses/gpl-2.0.html
Text Domain: pundungsari
Tags: block-patterns, full-site-editing, accessibility-ready
*/
/* Styles are delivered by the native theme.json global styles system. */
""".replace(", accessibility-ready",""))
    css=(ROOT/"wordpress/design.css").read_text()
    landscape="data:image/svg+xml,"+quote((ROOT/"assets/img/pundungsari-landscape.svg").read_text(),safe="")
    css=css.replace("__LANDSCAPE__",landscape)
    config={"$schema":"https://schemas.wp.org/wp/6.6/theme.json","version":3,"settings":{"appearanceTools":True,"useRootPaddingAwareAlignments":True,"layout":{"contentSize":"780px","wideSize":"1160px"},"color":{"defaultPalette":False,"palette":[{"slug":"green","name":"Hijau desa","color":"#143e32"},{"slug":"gold","name":"Emas","color":"#d9b46c"},{"slug":"cream","name":"Krem","color":"#f7f5ee"},{"slug":"ink","name":"Teks","color":"#1d302a"},{"slug":"muted","name":"Teks sekunder","color":"#52685f"},{"slug":"white","name":"Putih","color":"#ffffff"}]},"spacing":{"units":["px","rem","em","%","vw"]},"typography":{"fluid":True,"fontFamilies":[{"slug":"system","name":"Sistem","fontFamily":"system-ui, -apple-system, Segoe UI, sans-serif"},{"slug":"serif","name":"Serif","fontFamily":"Georgia, Times New Roman, serif"}],"fontSizes":[{"slug":"small","name":"Kecil","size":"0.875rem"},{"slug":"medium","name":"Normal","size":"1rem"},{"slug":"large","name":"Besar","size":"1.5rem"},{"slug":"x-large","name":"Judul","size":"2.5rem"}]}},"styles":{"color":{"background":"#ffffff","text":"#1d302a"},"spacing":{"blockGap":"24px","padding":{"top":"0","right":"0","bottom":"0","left":"0"}},"typography":{"fontFamily":"var:preset|font-family|system","fontSize":"1rem","lineHeight":"1.75"},"elements":{"heading":{"typography":{"fontFamily":"var:preset|font-family|serif","fontWeight":"500","lineHeight":"1.25"},"color":{"text":"#143e32"}},"link":{"color":{"text":"#143e32"}},"button":{"border":{"radius":"5px"},"color":{"background":"#143e32","text":"#ffffff"},"spacing":{"padding":{"top":"12px","right":"22px","bottom":"12px","left":"22px"}},"typography":{"fontSize":".9rem","fontWeight":"600"}}},"css":css},"templateParts":[{"name":"header","title":"Kepala halaman","area":"header"},{"name":"footer","title":"Kaki halaman","area":"footer"}]}
    config["settings"]["layout"]["wideSize"]="1240px"
    config["settings"]["color"]["palette"]=[
        {"slug":"green","name":"Hijau zamrud","color":"#103f35"},
        {"slug":"lime","name":"Limau lembut","color":"#d9eaa7"},
        {"slug":"cream","name":"Putih alami","color":"#fbfcf8"},
        {"slug":"ink","name":"Teks","color":"#173e31"},
        {"slug":"muted","name":"Teks sekunder","color":"#748073"},
        {"slug":"white","name":"Putih","color":"#ffffff"}]
    config["styles"]["color"]={"background":"#fbfcf8","text":"#173e31"}
    config["styles"]["elements"]["heading"]["typography"]={"fontFamily":"var:preset|font-family|system","fontWeight":"700","lineHeight":"1.25"}
    config["styles"]["elements"]["button"]["border"]["radius"]="12px"
    config["styles"]["elements"]["button"]["color"]["background"]="#103f35"
    write("wordpress/pundungsari/theme.json",json.dumps(config,ensure_ascii=False,indent=2))
    write("wordpress/pundungsari/parts/header.html",wp_header())
    write("wordpress/pundungsari/parts/footer.html",wp_footer())
    start=block("template-part",attrs={"slug":"header","tagName":"header"},selfclose=True)
    finish=block("template-part",attrs={"slug":"footer","tagName":"footer"},selfclose=True)
    write("wordpress/pundungsari/templates/front-page.html",start+group(wp_front(),tag="main",align="full")+finish)
    title=block("post-title",attrs={"level":1},selfclose=True)
    content=block("post-content",attrs={"layout":{"type":"constrained"}},selfclose=True)
    write("wordpress/pundungsari/templates/page.html",start+group(title+content,"ps-page",tag="main")+finish)
    single=title+block("post-date",selfclose=True)+content+block("post-terms",attrs={"term":"category"},selfclose=True)
    write("wordpress/pundungsari/templates/single.html",start+group(single,"ps-page",tag="main")+finish)
    for name,label in [("index","Berita Desa"),("home","Berita Desa"),("archive","Arsip Berita")]:
        head=block("query-title",attrs={"type":"archive","showPrefix":False},selfclose=True) if name=="archive" else heading(label,1)
        write(f"wordpress/pundungsari/templates/{name}.html",start+group(head+wp_query(True),"ps-page",align="wide",tag="main")+finish)
    search=block("query-title",attrs={"type":"search"},selfclose=True)+block("search",attrs={"label":"Cari informasi desa","showLabel":False,"placeholder":"Cari informasi desa","buttonText":"Cari"},selfclose=True)+wp_query(True)
    write("wordpress/pundungsari/templates/search.html",start+group(search,"ps-page",align="wide",tag="main")+finish)
    write("wordpress/pundungsari/templates/404.html",start+group(heading("Halaman tidak ditemukan",1)+para("Gunakan pencarian untuk menemukan informasi yang diperlukan.")+block("search",attrs={"label":"Cari informasi desa","buttonText":"Cari"},selfclose=True),"ps-page",tag="main")+finish)
    write("wordpress/pundungsari/README.txt","""PUNDUNGSARI — TEMA WORDPRESS
Versi 2.0.0 | GPL-2.0-or-later

Tema blok dengan halaman depan, daftar berita, artikel, halaman, arsip,
pencarian, dan halaman 404. Memakai blok bawaan WordPress; tidak memerlukan
PHP khusus, pembuat halaman berbayar, atau JavaScript dari layanan luar.
Gaya dikirimkan oleh sistem Global Styles melalui theme.json.

Pasang ZIP ini melalui Tampilan > Tema > Tambah > Unggah.
Impor konten-pundungsari.xml melalui Perkakas > Impor > WordPress.
Atur Beranda sebagai halaman utama dan Berita Desa sebagai halaman pos.
Pilih lambang dalam blok Logo Situs melalui Tampilan > Editor > Header.
Lambang juga disertakan di assets/images/lambang-lumajang.png.

Lambang berwarna bersumber dari situs resmi BKPSDM Kabupaten Lumajang.
https://bkpsdm.lumajangkab.go.id/assets/images/logo-bkpsdm.png
Ilustrasi perdesaan adalah gambar dekoratif, bukan foto lokasi desa.
Gunakan sesuai peruntukan Pemerintah Desa Pundungsari.
Paket tidak menyertakan foto rekaan, data pribadi penduduk, atau kata sandi.

Dokumentasi lengkap:
https://marom2386-ops.github.io/website-desa-pundungsari/panduan-wordpress.html

Paket ini belum berarti WordPress sudah terpasang di hosting.
""")
    (ROOT/"downloads").mkdir(exist_ok=True)
    with zipfile.ZipFile(ROOT/"downloads/pundungsari-wordpress.zip","w",zipfile.ZIP_DEFLATED) as z:
        for p in sorted(theme.rglob("*")):
            if p.is_file(): z.write(p, str(Path("pundungsari")/p.relative_to(theme)))
    build_wxr()

def build_wxr():
    ns={"content":"http://purl.org/rss/1.0/modules/content/","dc":"http://purl.org/dc/elements/1.1/","wp":"http://wordpress.org/export/1.2/","excerpt":"http://wordpress.org/export/1.2/excerpt/"}
    for prefix,url in ns.items(): ET.register_namespace(prefix,url)
    rss=ET.Element("rss",{"version":"2.0"})
    ch=ET.SubElement(rss,"channel")
    def put(parent,tag,text):
        if ":" in tag:
            pre,key=tag.split(":",1); tag="{"+ns[pre]+"}"+key
        el=ET.SubElement(parent,tag);el.text=str(text);return el
    put(ch,"title","Desa Pundungsari");put(ch,"link",BASE);put(ch,"description","Konten awal portal informasi Desa Pundungsari");put(ch,"language","id-ID")
    put(ch,"wp:wxr_version","1.2");put(ch,"wp:base_site_url",BASE);put(ch,"wp:base_blog_url",BASE)
    author=ET.SubElement(ch,"{"+ns["wp"]+"}author")
    for tag,val in [("author_id","1"),("author_login","pengelola-desa"),("author_email",D["email"]),("author_display_name","Pemerintah Desa Pundungsari"),("author_first_name",""),("author_last_name","")]:put(author,"wp:"+tag,val)
    cat=ET.SubElement(ch,"{"+ns["wp"]+"}category")
    for tag,val in [("term_id","1"),("category_nicename","berita-desa"),("category_parent",""),("cat_name","Berita Desa")]:put(cat,"wp:"+tag,val)
    items=[]
    for order,(title,slug,content) in enumerate(wp_pages()):
        items.append({"title":title,"slug":slug,"content":content,"type":"page","date":UPDATED,"order":order,"status":"publish"})
    for n in DATA["berita"]:
        items.append({"title":n["judul"],"slug":n["slug"],"content":para(E(n["ringkasan"])),"type":"post","date":n["tanggal"],"order":0,"status":"publish","excerpt":n["ringkasan"]})
    items.append({"title":"Lambang Kabupaten Lumajang","slug":"lambang-lumajang","content":"","type":"attachment","date":UPDATED,"order":0,"status":"inherit","attachment":BASE+"assets/img/lambang-lumajang.png"})
    for idx,n in enumerate(items,101):
        item=ET.SubElement(ch,"item")
        for tag,value in [("title",n["title"]),("link",BASE+n["slug"]+"/"),("dc:creator","pengelola-desa"),("content:encoded",n["content"]),("excerpt:encoded",n.get("excerpt","")),("wp:post_id",idx),("wp:post_date",n["date"]+" 08:00:00"),("wp:post_date_gmt",n["date"]+" 01:00:00"),("wp:post_modified",UPDATED+" 08:00:00"),("wp:post_modified_gmt",UPDATED+" 01:00:00"),("wp:comment_status","closed"),("wp:ping_status","closed"),("wp:post_name",n["slug"]),("wp:status",n["status"]),("wp:post_parent",0),("wp:menu_order",n["order"]),("wp:post_type",n["type"]),("wp:post_password",""),("wp:is_sticky",0)]:
            put(item,tag,value)
        guid=ET.SubElement(item,"guid",{"isPermaLink":"false"});guid.text=BASE+"?p="+str(idx)
        if n["type"]=="post":ET.SubElement(item,"category",{"domain":"category","nicename":"berita-desa"}).text="Berita Desa"
        if "attachment" in n:put(item,"wp:attachment_url",n["attachment"])
    ET.indent(rss,space="  ")
    ET.ElementTree(rss).write(ROOT/"downloads/konten-pundungsari.xml",encoding="utf-8",xml_declaration=True)

def build_meta():
    pages=["index.html","profil.html","pemerintahan.html","layanan.html","transparansi.html","berita.html","kontak.html","privasi.html"]+["berita/"+n["slug"]+".html" for n in DATA["berita"]]
    urlset=ET.Element("urlset",{"xmlns":"http://www.sitemaps.org/schemas/sitemap/0.9"})
    for path in pages:
        node=ET.SubElement(urlset,"url");ET.SubElement(node,"loc").text=BASE+path;ET.SubElement(node,"lastmod").text=UPDATED
    ET.indent(urlset,space="  ")
    ET.ElementTree(urlset).write(ROOT/"sitemap.xml",encoding="utf-8",xml_declaration=True)
    write("robots.txt","User-agent: *\nAllow: /\nDisallow: /website-desa-pundungsari/admin.html\nDisallow: /website-desa-pundungsari/panduan-wordpress.html\nSitemap: "+BASE+"sitemap.xml")
    write(".nojekyll","")
    write("README.md","""# Website Desa Pundungsari

Situs GitHub Pages dan WordPress dimulai dari sumber konten yang sama.
Pembaruan 18 Oktober 2026: halaman publik terpisah, layanan yang dapat dicari,
berita dengan tautan sendiri, identitas resmi, dan WordPress aktif di hosting gratis.

## Situs publik

https://marom2386-ops.github.io/website-desa-pundungsari/

WordPress: https://desa-pundungsari.great-site.net/
Dasbor: https://desa-pundungsari.great-site.net/wp-admin/

Hosting WordPress memakai paket gratis InfinityFree dengan HTTPS. Tema Pundungsari
2.0.0, delapan halaman, 17 panduan layanan, empat ringkasan berita, dan lambang
sudah dipasang. WordPress diperbarui ke 7.1.3 saat penyiapan.

Perubahan melalui dasbor WordPress tersimpan pada hosting WordPress. Perubahan
situs GitHub dilakukan melalui repositori; keduanya tidak tersinkron otomatis.

## Memperbarui konten pada GitHub

1. Ubah content/site.json menggunakan akun GitHub yang memiliki akses.
2. Jalankan python3 scripts/build_site.py untuk membangun halaman dan paket.
3. Jalankan python3 scripts/check_site.py dan node scripts/check_search.cjs.
4. Commit dan push hasilnya ke main.

GitHub Pages tetap menyajikan hasil HTML, CSS, dan JavaScript. Dasbor PIN demo
telah diganti dengan pusat pengelola yang menjelaskan jalur pengelolaan nyata.

## Paket WordPress

- downloads/pundungsari-wordpress.zip: unggah langsung sebagai tema WordPress.
- downloads/konten-pundungsari.xml: impor halaman, empat ringkasan berita, dan lambang.
- panduan-wordpress.html: panduan pemasangan dan pengelolaan.
- wordpress/pundungsari/: sumber tema blok.

WordPress memakai hosting yang mendukung PHP dan basis data. GitHub tetap
menyimpan sumber website, tema, dan paket pemasangan. Akun dan kata sandi
pemasangan tidak disimpan dalam repositori. Jangan mengimpor kembali XML ke
situs aktif karena konten awal sudah dimasukkan.

Tema memakai blok bawaan WordPress dan Global Styles, tanpa pembuat halaman
berbayar. Berita dikelola sebagai Pos dan informasi layanan sebagai Halaman.

## Sumber dan verifikasi

Konten awal mempertahankan ringkasan pada situs sebelumnya. Alamat kantor
dicocokkan dengan kop Surat Tugas PKAD Pundungsari Resmi 2026 milik pengguna.
Lambang berwarna diambil dari situs resmi BKPSDM Kabupaten Lumajang:
https://bkpsdm.lumajangkab.go.id/assets/images/logo-bkpsdm.png
Bentuk dan warnanya diperiksa terhadap halaman Lambang Daerah Pemkab:
https://lumajangkab.go.id/main/single
Tanda tangan/stempel dan dokumen sumber tidak dipublikasikan. Ilustrasi
perdesaan pada beranda adalah gambar dekoratif, bukan foto lokasi desa.

Angka kependudukan dan APBDes belum ditayangkan karena belum konsisten. Lihat
docs/CATATAN_VERIFIKASI.md. Jangan menebak data agar angka tampak cocok.
Data warga, KK, NIK, token, dan kata sandi tidak termasuk dalam paket.

## Validasi

Pemeriksaan tautan lokal, judul, metadata, struktur halaman, paket tema,
struktur blok WordPress, XML impor, angka publik, dan perilaku pencarian.
Halaman WordPress, rincian layanan, artikel, navigasi, gambar, serta tautan
kontak diperiksa melalui browser pada hosting aktif. Tata letak desktop
disesuaikan setelah pemeriksaan visual. Periksa kembali konten dan tampilan
melalui perangkat warga setelah setiap pembaruan besar.
""")
    write("docs/CATATAN_VERIFIKASI.md","""# Catatan verifikasi sebelum pengumuman resmi

## Data yang belum dipublikasikan

- Total penduduk lama: 4.179. Laki-laki 2.021 + perempuan 2.146 = 4.167.
  Selisih 12 jiwa. Cocokkan dengan rekap kependudukan resmi dan tanggal cut-off.
- Belanja lama: Rp1.115.723.251. Jumlah rincian Rp1.115.723.252.
  Selisih Rp1. Jangan menyamakan angka tanpa dokumen sumber.
- Judul lama menyebut rincian per bidang, sedangkan kategori adalah jenis
  belanja. Gunakan judul yang sesuai data sumber setelah diverifikasi.
- Pastikan versi Perubahan APBDes yang berlaku; materi lama menyebut Perdes
  Nomor 3 Tahun 2026. Jangan memublikasikan sebagai versi terbaru tanpa pemeriksaan.
- Luas dan batas wilayah belum ditayangkan karena dokumen sumber belum diperiksa.

## Konten yang dipertahankan

- Nama dan jabatan perangkat mengikuti sumber situs. Periksa dengan SK terbaru.
- Visi-misi ditandai periode RPJMDes 2020–2026 sesuai keterangan sumber.
- Empat berita mempertahankan ringkasan lama; tidak menambahkan detail rekaan.
- Jam dan nomor kontak mengikuti situs sebelumnya. Alamat sesuai kop surat desa.

## Setelah sumber tersedia

Masukkan data beserta periode dan sumbernya, periksa kecocokan jumlah,
unggah dokumen yang memang boleh dibuka publik, lalu perbarui halaman.
""")

if __name__=="__main__":
    for old in ["assets/js/admin.js","assets/js/app.js","assets/js/data.js","assets/css/admin.css","assets/css/style.css","assets/img/panorama.jpg"]:
        (ROOT/old).unlink(missing_ok=True)
    build_public()
    build_theme()
    build_meta()
    print(f"Built public pages, {len(DATA['layanan'])} services, {len(DATA['berita'])} articles, and WordPress theme.")
