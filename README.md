# Website Desa Pundungsari

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
