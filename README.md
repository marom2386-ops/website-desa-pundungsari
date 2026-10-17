# Website Desa Pundungsari

Website profil desa + dasbor admin, dibuat dari awal. Siap dipasang ke
Google Apps Script (pola yang sama dengan aplikasi operator V20:
satu aplikasi, satu database Spreadsheet).

## Struktur file

```
website-desa/
├── index.html              → halaman publik (Beranda, Profil, Pemerintahan,
│                             Layanan, Transparansi, Berita, Kontak)
├── admin.html              → dasbor admin (login PIN demo: 1234)
├── assets/
│   ├── css/style.css       → tema halaman publik
│   ├── css/admin.css       → tema dasbor
│   ├── js/data.js          → LAPISAN DATA (sementara, contoh)
│   ├── js/app.js           → logika halaman publik
│   ├── js/admin.js         → logika dasbor
│   └── img/hero.jpg        → foto hero (Semeru)
└── README.md
```

## Cara deploy ke Google Apps Script

**Opsi A — Web App Apps Script (disarankan, gratis, satu database):**

1. Buat project Apps Script baru.
2. Upload semua file:
   - `index.html` → ganti nama jadi `Index`
   - `admin.html` → `Admin`
   - File CSS/JS/img → upload sebagai file HTML terpisah lalu
     panggil dengan `<?!= include('style'); ?>`, atau gabungkan
     inline untuk awal (cara cepat).
3. `Code.gs` minimal:

```gs
function doGet(e) {
  const page = (e.parameter.page || 'index').toLowerCase();
  if (page === 'admin') return HtmlService.createHtmlOutputFromFile('Admin')
      .setTitle('Dasbor Admin — Desa Pundungsari');
  return HtmlService.createHtmlOutputFromFile('Index')
      .setTitle('Desa Pundungsari');
}
```

4. Deploy → New version → akses URL `/exec` untuk publik,
   `/exec?page=admin` untuk dasbor.

**Opsi B — Hosting statis** (Netlify/Vercel/GitHub Pages): upload
apa adanya, langsung jalan. Dasbor tetap demo (localStorage).

## Menghubungkan ke Spreadsheet (mengganti data.js)

Ganti pemanggilan `DB` di `app.js`/`admin.js` dengan
`google.script.run`:

```gs
// Code.gs
function getDataWebsite() {
  const ss = SpreadsheetApp.openById('ID_SPREADSHEET');
  return {
    berita: sheetToObjects(ss.getSheetByName('BERITA')),
    perangkat: sheetToObjects(ss.getSheetByName('PERANGKAT')),
    // ...
  };
}
```

Sheet yang disarankan: `BERITA`, `PERANGKAT`, `LAYANAN`,
`APBDES`, `STATISTIK`, `GALERI`, `PENGATURAN`.

## Yang masih perlu diisi data resmi

Semua yang bertanda **CONTOH** di `data.js`:
- Nomor telepon & email desa, sejarah, visi-misi, batas wilayah, luas
- Angka APBDes (rincian per bidang)
- Data kependudukan (penduduk, KK, dusun/RT/RW)
- Foto perangkat desa (`foto:` diisi path file)
- Embed Google Maps balai desa di halaman Kontak
- PIN admin asli (ganti `PIN_DEMO` di `admin.js`, atau pakai
  sistem login yang sama dengan aplikasi operator V20)

## Pratinjau lokal

```bash
cd ~/workspace/website-desa && python3 -m http.server 8080
# buka http://localhost:8080  dan  http://localhost:8080/admin.html
```
