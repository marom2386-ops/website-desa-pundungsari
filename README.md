# Website Desa Pundungsari

Situs GitHub Pages dan WordPress dimulai dari sumber konten yang sama.
Pembaruan 18 Oktober 2026: halaman publik terpisah, layanan yang dapat dicari,
berita dengan tautan sendiri, identitas resmi, dan WordPress aktif di hosting gratis.

## Situs publik

https://marom2386-ops.github.io/website-desa-pundungsari/

WordPress: https://desa-pundungsari.great-site.net/
Dasbor: https://desa-pundungsari.great-site.net/wp-admin/

Hosting WordPress memakai paket gratis InfinityFree dengan HTTPS. Tema Pundungsari
2.0.1, delapan halaman, 17 panduan layanan, empat ringkasan berita, dan lambang
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
