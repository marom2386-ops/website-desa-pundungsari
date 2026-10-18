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
 <div class="wrap masthead">
  <a class="brand" href="{prefix}index.html"><img src="{prefix}assets/img/lambang-lumajang.png" alt="Lambang Kabupaten Lumajang" width="45" height="60"><span><small>Pemerintah Desa</small><strong>Pundungsari</strong><span>Kecamatan Tempursari · Kabupaten Lumajang</span></span></a>
  <div class="header-contact">{icon("phone")}<div><span>Informasi pelayanan</span><a href="{E(wa())}" target="_blank" rel="noopener noreferrer">{E(D["telepon"])}</a></div></div>
 </div>
 <nav class="main-nav" aria-label="Menu utama"><div class="wrap nav-inner">{links}</div></nav>
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
<link rel="stylesheet" href="{prefix}assets/css/public.css"><script defer src="{prefix}assets/js/public.js"></script>
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
    quick = "".join(f'<a class="quick-item" href="{path}">{icon(ic)}<div><h2>{title}</h2><p>{desc}</p></div>{icon("arrow","arrow")}</a>' for path,ic,title,desc in [("layanan.html","file","Panduan layanan","Temukan jenis layanan dan bahan yang dapat disiapkan."),("transparansi.html","chart","Transparansi desa","Informasi anggaran, peraturan, dan dokumen desa."),("kontak.html","pin","Kontak & lokasi","Jam pelayanan, alamat kantor, dan saluran komunikasi.")])
    services = "".join(f'<a href="layanan.html#{s["id"]}">{E(s["nama"])}{icon("arrow")}</a>' for s in DATA["layanan"][:6])
    body = f'''<section class="hero"><div class="wrap hero-grid"><div><span class="eyebrow">Tempursari · Lumajang · Jawa Timur</span><h1>Desa Pundungsari.<br><em>Informasi untuk kita bersama.</em></h1><p class="lead">Kenali desa, ikuti kabar kegiatan, dan temukan panduan pelayanan dalam satu tempat.</p><div class="button-row"><a class="button gold" href="layanan.html">Temukan layanan {icon("arrow")}</a><a class="button outline" href="profil.html">Kenali desa kami</a></div></div><aside class="office-card" aria-label="Informasi kantor desa"><span class="eyebrow">Pelayanan masyarakat</span><h2>Kantor Desa<br>Pundungsari</h2><div class="office-row">{icon("clock")}<div><strong>Jam pelayanan</strong><p>{E(D["jamLayanan"])}</p></div></div><div class="office-row">{icon("pin")}<div><strong>Alamat kantor</strong><p>{E(D["alamat"])}<br>Jawa Timur {E(D["kodePos"])}</p></div></div><p class="office-note"><a href="kontak.html">Lihat kontak dan petunjuk lokasi →</a></p></aside></div></section>
<div class="quick-wrap"><div class="wrap quick-grid">{quick}</div></div>
<section class="section"><div class="wrap intro-grid"><div><span class="eyebrow">Pelayanan warga</span><h2>Mulai dari informasi yang Anda perlukan.</h2><p>Pelajari layanan sebelum datang ke kantor desa. Petugas akan membantu menjelaskan dokumen dan proses sesuai keperluan Anda.</p><a class="text-link" href="layanan.html">Lihat seluruh panduan layanan →</a></div><div class="info-list">{services}</div></div></section>
<section class="section tint"><div class="wrap"><div class="section-head"><div><span class="eyebrow">Kabar Pundungsari</span><h2>Berita &amp; kegiatan desa</h2></div><a class="text-link" href="berita.html">Semua berita →</a></div><div class="news-grid">{''.join(news_card(n) for n in DATA["berita"][:3])}</div></div></section>
<section class="section"><div class="wrap intro-grid"><div><span class="eyebrow">Pemerintahan terbuka</span><h2>Informasi publik yang mudah dijangkau.</h2></div><div><p>Ketahui informasi anggaran, perencanaan, dan peraturan desa. Dokumen yang belum tersedia di halaman publik dapat ditanyakan melalui pelayanan informasi desa.</p><a class="button outline" href="transparansi.html">Informasi &amp; dokumen desa {icon("arrow")}</a></div></div></section>'''
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

    body = intro("Pusat Pengelola","Pengelolaan situs yang berjalan dan persiapan penggunaan WordPress.") + f'<section class="section"><div class="wrap"><div class="admin-grid"><section class="admin-card"><span class="eyebrow">Situs saat ini</span><h2>Kelola melalui GitHub</h2><p>Isi website publik disimpan pada berkas konten situs. Perubahan dilakukan dengan akun GitHub yang memiliki akses, kemudian halaman dibangun ulang sesuai panduan proyek.</p><a class="button" href="{REPO}/edit/main/content/site.json" target="_blank" rel="noopener noreferrer">Buka berkas konten di GitHub</a><p><a href="{REPO}/blob/main/README.md" target="_blank" rel="noopener noreferrer">Baca panduan pengelolaan GitHub →</a></p></section><section class="admin-card"><span class="eyebrow">Paket siap dipasang</span><h2>Gunakan WordPress</h2><p>Tema dan konten awal sudah disiapkan. Setelah tersedia hosting WordPress, petugas dapat mengelola berita dan halaman dari dasbor WordPress.</p><a class="button" href="downloads/pundungsari-wordpress.zip" download>Unduh tema WordPress</a><p><a href="panduan-wordpress.html">Panduan pemasangan dan pengelolaan →</a></p></section></div><div class="note"><p>WordPress belum terpasang pada alamat GitHub ini. Akses pengelola WordPress tersedia setelah pemasangan di hosting yang mendukungnya.</p></div></div></section>'
    page("admin.html","Pusat Pengelola","Pengelolaan website GitHub dan paket persiapan WordPress Desa Pundungsari.",body,noindex=True,contact=False)
    build_guide()
    body = intro("Halaman tidak ditemukan","Alamat yang Anda buka tidak tersedia atau sudah berubah.") + '<section class="section"><div class="wrap"><p>Silakan kembali ke halaman utama atau gunakan menu untuk menemukan informasi desa.</p><a class="button" href="index.html">Kembali ke beranda</a></div></section>'
    page("404.html","Halaman Tidak Ditemukan","Kembali ke portal informasi Desa Pundungsari.",body,noindex=True,contact=False)

def build_guide():
    body = intro("Panduan WordPress","Paket tema dan konten awal Desa Pundungsari, siap dipasang ketika hosting WordPress tersedia.") + f'''<section class="section"><div class="wrap article-shell prose">
<div class="note"><p><strong>Status saat ini:</strong> situs publik berjalan di GitHub Pages. Tema ini adalah paket WordPress yang sebenarnya, tetapi WordPress belum terpasang secara daring karena hostingnya belum tersedia.</p></div>
<h2>1. Unduh paket yang diperlukan</h2><ul><li><a href="downloads/pundungsari-wordpress.zip" download>Tema Pundungsari untuk WordPress (.zip)</a></li><li><a href="downloads/konten-pundungsari.xml" download>Konten awal untuk diimpor (.xml)</a></li><li><a href="assets/img/lambang-lumajang.png" download>Lambang Kabupaten Lumajang (.png)</a></li></ul>
<h2>2. Siapkan hosting</h2><p>Gunakan hosting yang mendukung WordPress dengan PHP, MySQL atau MariaDB, serta HTTPS. Gunakan WordPress versi stabil yang masih didukung, sekurang-kurangnya versi 6.6 untuk tema ini. Akun hosting dan domain sebaiknya berada dalam pengelolaan desa.</p><p>Hosting adalah tempat WordPress dijalankan. Domain adalah alamat website. Pembelian, pemilihan penyedia, dan pemasangan ke akun hosting belum termasuk dalam pekerjaan ini karena akun hosting belum tersedia.</p>
<h2>3. Pasang dan aktifkan tema</h2><ol><li>Pasang WordPress melalui panel hosting.</li><li>Masuk ke dasbor WordPress pada alamat website tujuan, biasanya melalui /wp-admin.</li><li>Buka Tampilan → Tema → Tambah Tema → Unggah Tema.</li><li>Pilih berkas pundungsari-wordpress.zip, pasang, lalu aktifkan.</li></ol>
<h2>4. Impor konten awal</h2><ol><li>Buka Perkakas → Impor → WordPress. Pasang pengimpor resmi apabila diminta.</li><li>Pilih konten-pundungsari.xml, lalu petakan penulis ke akun pengelola desa.</li><li>Pilih unduh dan impor lampiran untuk mengambil lambang dari situs GitHub saat ini, atau unggah lambang secara manual ke Media.</li><li>Jalankan impor satu kali agar tidak menambahkan konten ganda.</li></ol>
<h2>5. Atur identitas dan navigasi</h2><ol><li>Di Pengaturan → Umum, isi judul situs Desa Pundungsari, bahasa Indonesia, dan zona waktu Jakarta.</li><li>Di Pengaturan → Membaca, pilih halaman statis: Beranda untuk halaman utama dan Berita Desa untuk halaman pos.</li><li>Di Pengaturan → Permalink, pilih Nama pos, lalu simpan.</li><li>Di Tampilan → Editor, buka bagian Header. Pilih blok Logo Situs dan gunakan lambang Lumajang yang telah diunggah.</li><li>Periksa menu navigasi. Tema memakai daftar halaman bawaan WordPress; sesuaikan urutannya dan hindari tautan Beranda ganda.</li><li>Periksa nomor telepon, email, jam pelayanan, nama perangkat, serta isi profil sebelum pengumuman resmi.</li></ol>
<h2>6. Kelola berita dan halaman</h2><p>Untuk berita: buka Pos → Tambah Baru, isi judul dan naskah, tambahkan foto kegiatan yang benar, periksa pratinjau, lalu terbitkan. Untuk profil, layanan, pemerintahan, dan kontak: gunakan menu Halaman.</p><p>Tampilan beranda dan kepala/kaki halaman dapat disesuaikan melalui Tampilan → Editor. Tema memakai blok bawaan WordPress; tidak membutuhkan pembuat halaman berbayar.</p><p>Buat akun tersendiri untuk setiap petugas melalui Pengguna. Gunakan peran Editor untuk petugas pengelola isi; akun Administrator digunakan untuk pengaturan situs. Penulis dapat digunakan untuk petugas yang hanya menulis berita.</p>
<h2>7. Lengkapi informasi publik</h2><p>Angka kependudukan dan APBDes belum dimasukkan ke paket publik karena data sumber belum cocok. Periksa catatan verifikasi dalam proyek. Setelah disahkan, masukkan angka beserta periode dan sumbernya, lalu unggah dokumen publik yang sudah diperiksa.</p><p>Empat berita awal mempertahankan ringkasan pada situs sebelumnya. Lengkapi naskah dan dokumentasi berdasarkan kegiatan nyata; paket ini tidak menambahkan kutipan, foto kegiatan, atau angka rekaan.</p>
<h2>8. Pindahkan alamat setelah siap</h2><ol><li>Uji website tujuan melalui HP dan komputer, termasuk menu, pencarian, gambar, tautan WhatsApp, dan akun petugas.</li><li>Siapkan pencadangan dan pembaruan rutin WordPress, tema, serta plugin yang dipakai.</li><li>Setelah alamat WordPress final aktif, arahkan pengunjung dari situs GitHub ke alamat baru.</li><li>Umumkan satu alamat resmi yang akan digunakan masyarakat.</li></ol>
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

def wp_columns(items):
    cols="".join(block("column",'<div class="wp-block-column">'+item+"</div>") for item in items)
    return block("columns",'<div class="wp-block-columns">'+cols+"</div>")

def wp_query(inherit=False):
    query={"perPage":9 if inherit else 3,"pages":0,"offset":0,"postType":"post","order":"desc","orderBy":"date","author":"","search":"","exclude":[],"sticky":"","inherit":inherit}
    entry=group(block("post-date",selfclose=True)+block("post-title",attrs={"isLink":True,"level":2},selfclose=True)+block("post-excerpt",attrs={"moreText":"Baca informasi →","excerptLength":35},selfclose=True),"ps-news-card")
    posts=block("post-template",entry,{"layout":{"type":"grid","columnCount":3}})
    pagination=block("query-pagination",block("query-pagination-previous",selfclose=True)+block("query-pagination-numbers",selfclose=True)+block("query-pagination-next",selfclose=True),{"layout":{"type":"flex","justifyContent":"space-between"}})
    noresults=block("query-no-results",para("Belum ada berita yang sesuai."))
    return block("query",'<div class="wp-block-query">'+posts+pagination+noresults+'</div>',{"queryId":1,"query":query})

def wp_header():
    brand=group(block("site-logo",attrs={"width":42},selfclose=True)+group(block("site-title",attrs={"level":0},selfclose=True)+para("Kecamatan Tempursari · Kabupaten Lumajang","ps-location")),"ps-brand",layout="flex")
    nav=block("navigation",block("page-list",selfclose=True),{"overlayMenu":"mobile","layout":{"type":"flex","justifyContent":"left"}})
    return group(group(para("Pemerintah Desa Pundungsari · Kabupaten Lumajang"),"ps-top",align="full")+group(brand,"ps-masthead",align="wide")+group(nav,"ps-navigation",align="wide"),"ps-header",align="full")

def wp_footer():
    contact=heading("Desa Pundungsari")+para(E(D["alamat"])+", Jawa Timur "+E(D["kodePos"]))+para(E(D["jamLayanan"]))
    links=heading("Informasi pelayanan",3)+para(f'<a href="{E(wa())}">WhatsApp: {E(D["telepon"])}</a>')+para(f'<a href="mailto:{E(D["email"])}">{E(D["email"])}</a>')+para(f'<a href="{E(MAP)}">Petunjuk lokasi kantor →</a>')
    return group(group(wp_columns([contact,links])+para("Pemerintah Desa Pundungsari · Kecamatan Tempursari · Kabupaten Lumajang","ps-footer-note"),align="wide"),"ps-footer",align="full")

def wp_front():
    hero_left=para("Tempursari · Lumajang · Jawa Timur","ps-eyebrow")+heading("Desa Pundungsari.<br>Informasi untuk kita bersama.",1)+para("Kenali desa, ikuti kabar kegiatan, dan temukan panduan pelayanan dalam satu tempat.")+buttons([("Temukan layanan","?pagename=layanan"),("Kenali desa kami","?pagename=profil")])
    hero_right=group(heading("Kantor Desa Pundungsari",2)+para("<strong>Jam pelayanan</strong><br>"+E(D["jamLayanan"]))+para("<strong>Alamat kantor</strong><br>"+E(D["alamat"]))+para(f'<a href="{E(wa())}">Hubungi petugas desa →</a>'),"ps-office")
    hero=group(group(wp_columns([hero_left,hero_right]),align="wide"),"ps-hero",align="full")
    quick=wp_columns([heading("Panduan layanan",3)+para("Temukan jenis layanan dan bahan yang dapat disiapkan.")+buttons([("Lihat layanan","?pagename=layanan")]),heading("Transparansi desa",3)+para("Informasi anggaran, perencanaan, dan dokumen publik desa.")+buttons([("Informasi publik","?pagename=transparansi")]),heading("Kontak & lokasi",3)+para("Jam pelayanan, alamat kantor, dan saluran komunikasi.")+buttons([("Hubungi desa","?pagename=kontak")])])
    quick=group(group(quick,align="wide"),"ps-quick",align="full")
    news=group(para("Kabar Pundungsari","ps-eyebrow")+heading("Berita & kegiatan desa")+wp_query(False),align="wide")
    info=group(heading("Perlu informasi lebih lanjut?")+para("Hubungi petugas atau datang ke kantor desa pada jam pelayanan.")+buttons([("Hubungi pemerintah desa",wa())]),"ps-contact",align="wide")
    return hero+quick+group(news+info,"ps-main")

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
Version: 1.0.0
Requires at least: 6.6
Requires PHP: 7.4
License: GPL-2.0-or-later
License URI: https://www.gnu.org/licenses/gpl-2.0.html
Text Domain: pundungsari
Tags: block-patterns, full-site-editing, accessibility-ready
*/
/* Styles are delivered by the native theme.json global styles system. */
""".replace(", accessibility-ready",""))
    css="""
html{scroll-behavior:smooth}body{line-height:1.75}a{text-underline-offset:4px}a:focus-visible,button:focus-visible,summary:focus-visible{outline:3px solid #a46a15;outline-offset:4px}h1,h2,h3{text-wrap:balance}.wp-site-blocks{padding:0}.ps-header,.ps-footer,.ps-top,.ps-hero,.ps-quick{margin-block-start:0!important}.ps-top{background:#143e32;color:#fff;padding:8px 24px;font-size:.75rem}.ps-top p{max-width:1160px;margin:0 auto}.ps-masthead{padding:25px 24px}.ps-brand{gap:15px}.ps-brand .wp-block-site-title{font-family:Georgia,serif;font-size:1.8rem;line-height:1.25;font-weight:500}.ps-brand .wp-block-site-title a{text-decoration:none}.ps-location{font-size:.75rem;color:#52685f;margin:4px 0 0}.ps-navigation{border-block:1px solid #dce4de;padding:15px 24px;font-size:.86rem}.ps-navigation a{text-decoration:none}.ps-navigation a:hover{text-decoration:underline}.ps-hero{background:#143e32;color:#fff;padding:70px 24px}.ps-hero h1{font-size:clamp(2.3rem,4.7vw,4rem);letter-spacing:-.04em;line-height:1.15}.ps-hero .wp-block-columns{gap:65px;align-items:center}.ps-hero p{color:#dbe7df}.ps-hero .ps-eyebrow{color:#ecd6ab}.ps-eyebrow{text-transform:uppercase;letter-spacing:.14em;font-size:.72rem;font-weight:700;color:#52685f}.ps-hero a{color:#fff}.ps-hero .wp-block-button__link{background:#d9b46c;color:#18382d}.ps-office{background:#ffffff0b;border-top:3px solid #d9b46c;padding:28px}.ps-office h2{font-size:1.65rem}.ps-office p{font-size:.9rem}.ps-quick{background:#f7f5ee;padding:32px 24px;border-bottom:1px solid #dce4de}.ps-quick h3{font-family:inherit;font-size:1.05rem}.ps-quick p{font-size:.88rem;color:#52685f}.ps-quick .wp-block-button__link{background:transparent;color:#143e32;border:1px solid #b7c9bc;padding:10px 16px;font-size:.8rem}.ps-main{padding:64px 24px}.ps-news-card{border-top:2px solid #143e32;padding-top:22px}.ps-news-card .wp-block-post-title{font-family:inherit;font-size:1.15rem;line-height:1.45;font-weight:650}.ps-news-card .wp-block-post-title a{text-decoration:none}.ps-news-card .wp-block-post-date{font-size:.76rem;color:#52685f}.ps-news-card .wp-block-post-excerpt{font-size:.9rem;color:#52685f}.ps-news-card .wp-block-post-excerpt__more-text{font-size:.85rem}.wp-block-post-template{gap:30px}.ps-contact{margin-top:60px!important;padding:35px;background:#f7f5ee}.ps-footer{background:#eef2ec;border-top:1px solid #dce4de;padding:42px 24px}.ps-footer h2{font-size:1.6rem}.ps-footer h3{font-family:inherit;font-size:1rem}.ps-footer p{font-size:.86rem;color:#52685f}.ps-footer-note{border-top:1px solid #d5ddd4;padding-top:18px;font-size:.75rem!important}.ps-page{padding:48px 24px 64px}.ps-page .wp-block-post-title{font-size:clamp(2.2rem,4vw,3.4rem);letter-spacing:-.03em}.wp-block-details{border-bottom:1px solid #dce4de;padding:20px 0}.wp-block-details summary{font-weight:650;cursor:pointer}.wp-block-details>p,.wp-block-details>ul{font-size:.92rem}.wp-block-query-pagination{margin-top:35px}.wp-block-search__inside-wrapper{gap:8px}.wp-block-search__input{border:1px solid #a9bbb0;padding:12px}.wp-block-search__button{border:0;background:#143e32;color:white;padding:12px 18px;border-radius:5px}.wp-block-post-content>h2{margin-top:38px}.wp-block-post-content p{overflow-wrap:anywhere}
@media(max-width:760px){.ps-masthead{padding:20px 18px}.ps-navigation{padding:13px 18px}.ps-hero{padding:45px 18px}.ps-hero .wp-block-columns{gap:30px}.ps-quick,.ps-main,.ps-page{padding-inline:18px}.ps-main{padding-block:45px}.ps-contact{padding:26px;margin-top:40px!important}.ps-footer{padding-inline:18px}.wp-block-post-template{grid-template-columns:1fr!important}.ps-brand .wp-block-site-title{font-size:1.5rem}}
@media(prefers-reduced-motion:reduce){html{scroll-behavior:auto}}
""".strip()
    config={"$schema":"https://schemas.wp.org/wp/6.6/theme.json","version":3,"settings":{"appearanceTools":True,"useRootPaddingAwareAlignments":True,"layout":{"contentSize":"780px","wideSize":"1160px"},"color":{"defaultPalette":False,"palette":[{"slug":"green","name":"Hijau desa","color":"#143e32"},{"slug":"gold","name":"Emas","color":"#d9b46c"},{"slug":"cream","name":"Krem","color":"#f7f5ee"},{"slug":"ink","name":"Teks","color":"#1d302a"},{"slug":"muted","name":"Teks sekunder","color":"#52685f"},{"slug":"white","name":"Putih","color":"#ffffff"}]},"spacing":{"units":["px","rem","em","%","vw"]},"typography":{"fluid":True,"fontFamilies":[{"slug":"system","name":"Sistem","fontFamily":"system-ui, -apple-system, Segoe UI, sans-serif"},{"slug":"serif","name":"Serif","fontFamily":"Georgia, Times New Roman, serif"}],"fontSizes":[{"slug":"small","name":"Kecil","size":"0.875rem"},{"slug":"medium","name":"Normal","size":"1rem"},{"slug":"large","name":"Besar","size":"1.5rem"},{"slug":"x-large","name":"Judul","size":"2.5rem"}]}},"styles":{"color":{"background":"#ffffff","text":"#1d302a"},"spacing":{"blockGap":"24px","padding":{"top":"0","right":"0","bottom":"0","left":"0"}},"typography":{"fontFamily":"var:preset|font-family|system","fontSize":"1rem","lineHeight":"1.75"},"elements":{"heading":{"typography":{"fontFamily":"var:preset|font-family|serif","fontWeight":"500","lineHeight":"1.25"},"color":{"text":"#143e32"}},"link":{"color":{"text":"#143e32"}},"button":{"border":{"radius":"5px"},"color":{"background":"#143e32","text":"#ffffff"},"spacing":{"padding":{"top":"12px","right":"22px","bottom":"12px","left":"22px"}},"typography":{"fontSize":".9rem","fontWeight":"600"}}},"css":css},"templateParts":[{"name":"header","title":"Kepala halaman","area":"header"},{"name":"footer","title":"Kaki halaman","area":"footer"}]}
    # White heading color inside the dark homepage hero.
    config["styles"]["css"]+="\n.ps-hero h1,.ps-hero h2{color:#fff}"
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
Versi 1.0.0 | GPL-2.0-or-later

Tema blok dengan halaman depan, daftar berita, artikel, halaman, arsip,
pencarian, dan halaman 404. Memakai blok bawaan WordPress; tidak memerlukan
PHP khusus, pembuat halaman berbayar, atau JavaScript dari layanan luar.
Gaya dikirimkan oleh sistem Global Styles melalui theme.json.

Pasang ZIP ini melalui Tampilan > Tema > Tambah > Unggah.
Impor konten-pundungsari.xml melalui Perkakas > Impor > WordPress.
Atur Beranda sebagai halaman utama dan Berita Desa sebagai halaman pos.
Pilih lambang dalam blok Logo Situs melalui Tampilan > Editor > Header.
Lambang juga disertakan di assets/images/lambang-lumajang.png.

Lambang bersumber dari kop surat desa yang disediakan pengguna.
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

Situs publik GitHub Pages dan paket tema WordPress menggunakan konten yang sama.
Pembaruan 18 Oktober 2026: halaman publik terpisah, layanan yang dapat dicari,
berita dengan tautan sendiri, identitas resmi, dan paket WordPress.

## Situs publik

https://marom2386-ops.github.io/website-desa-pundungsari/

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

WordPress memerlukan hosting yang mendukung PHP dan basis data. Paket ini tidak
memasang WordPress pada GitHub Pages. Tidak ada akun hosting baru, pembelian,
atau domain baru yang dibuat oleh perubahan ini.

Tema memakai blok bawaan WordPress dan Global Styles, tanpa pembuat halaman
berbayar. Berita dikelola sebagai Pos dan informasi layanan sebagai Halaman.

## Sumber dan verifikasi

Konten awal mempertahankan ringkasan pada situs sebelumnya. Alamat serta lambang
dicocokkan dengan kop Surat Tugas PKAD Pundungsari Resmi 2026 milik pengguna.
Lambang saja yang disertakan; tanda tangan/stempel dan dokumen sumber tidak
dipublikasikan. Gambar lanskap rekaan pada versi lama tidak digunakan.

Angka kependudukan dan APBDes belum ditayangkan karena belum konsisten. Lihat
docs/CATATAN_VERIFIKASI.md. Jangan menebak data agar angka tampak cocok.
Data warga, KK, NIK, token, dan kata sandi tidak termasuk dalam paket.

## Validasi

Pemeriksaan tautan lokal, judul, metadata, struktur halaman, paket tema,
struktur blok WordPress, XML impor, angka publik, dan perilaku pencarian.
Render WordPress pada hosting serta pemeriksaan visual browser tetap perlu
dilakukan setelah hosting tersedia.
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
