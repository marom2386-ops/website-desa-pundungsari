# Portal Pemerintah Desa Pundungsari

Website publik statis di GitHub Pages yang dikelola melalui repositori GitHub. Data sensitif warga **tidak boleh** disimpan di sini.

## Status perbaikan Oktober 2026

- PIN demo `1234` dan dashboard yang seolah-olah menyimpan ke server telah **dinonaktifkan**.
- Ketidaksesuaian angka penduduk (4.179 versus 2.021 + 2.146 = 4.167) ditandai **dalam verifikasi** tanpa menebak angka pengganti.
- Ketidaksesuaian penjumlahan belanja APBDes (selisih Rp1) serta status perubahan anggaran terakhir ditandai **dalam verifikasi**.
- Berita dapat dibuka sebagai halaman ringkasan dengan tautan langsung `#artikel-N` dan dibagikan. Artikel lengkap/foto belum tersedia, dan tidak dikarang.
- Kontak email dan telepon dapat diklik; alur layanan disesuaikan agar tidak menjanjikan fitur daring yang belum tersedia.
- Ada navigasi berbasis hash, elemen aksesibilitas dasar, dan tampilan artikel untuk telepon seluler.

## Mengelola konten (sementara)

1. Login ke GitHub sebagai kolaborator dengan hak akses pada repositori.
2. Buka `assets/js/data.js`, edit data **publik dan terverifikasi** menggunakan editor GitHub.
3. Simpan perubahan melalui commit / pull request dan tinjau sebelum merge.
4. Setelah masuk branch `main`, GitHub Pages akan menerbitkan konten tersebut.

**Penting:** Jangan memasukkan NIK, nomor KK, tanggal lahir, nomor ponsel warga, alamat individual, dokumen pelayanan, kunci API, atau kata sandi ke repositori publik.

## Data yang harus dikonfirmasi

- Rekap penduduk agregat dari sumber resmi, berikut tanggal pemutakhirannya.
- Dokumen Perdes APBDes / P-APBDes **terakhir** dan angka pendapatan, belanja, pembiayaan, serta klasifikasi sesuai format dokumen.
- Logo pemerintah daerah, foto kantor / kegiatan asli, foto perangkat desa yang disetujui untuk publikasi.
- Jam layanan, nomor telepon/email desa, batas wilayah, dan luas wilayah.
- Artikel berita lengkap beserta foto, tanggal dan penanggung jawab publikasi.

## Agar dapat mengelola tanpa mengedit kode GitHub

Dibutuhkan CMS/backend terautentikasi (misalnya Apps Script + Google Sheet **khusus konten publik**, dengan akses dibatasi kepada akun petugas) atau layanan CMS terkelola. GitHub Pages sendiri hanya menyediakan hosting statis, bukan penyimpanan konten berfitur login dan hak akses.

Rancangan CMS minimal:
- Akun petugas dan hak akses editor/pemeriksa/penerbit.
- Draf berita dengan judul, tanggal, isi lengkap, foto berizin, dan status publikasi.
- Validasi input di server, log perubahan, dan fitur pemulihan.
- API publik read-only khusus data yang layak ditampilkan.
- Tidak terhubung secara langsung ke tabel sensitif kependudukan/aplikasi pelayanan warga.

Jangan memindahkan credential atau data pribadi ke client-side JavaScript. Konfigurasi dan pengujian backend harus dilakukan sebelum admin produksi dibuka.

## Rencana penerbitan

1. Periksa perubahan di pull request lalu merge ke main.
2. Buka website di ponsel dan desktop; pastikan seluruh menu berfungsi.
3. Periksa laporan console browser, tautan berita dan kontak, serta Google Maps.
4. Masukkan angka resmi yang sudah diperiksa; ganti placeholder media dengan aset resmi.
5. Baru aktifkan domain resmi desa dan CMS terautentikasi setelah tersedia.

## Struktur

- `index.html`: halaman informasi publik.
- `assets/js/data.js`: dataset informasi **publik**.
- `assets/js/app.js`: render halaman dan detail ringkasan berita.
- `assets/css/style.css`: desain dan responsif.
- `admin.html`: pemberitahuan admin nonaktif sampai tersedia backend aman.

Perubahan kode tidak otomatis memperbarui database kependudukan, Google Drive, KIM.ID, atau aplikasi operator. Integrasi harus dirancang terpisah dan diujikan.
