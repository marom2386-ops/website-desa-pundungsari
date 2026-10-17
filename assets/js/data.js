/* ============================================================
   DATA RESMI Website Desa Pundungsari
   ------------------------------------------------------------
   Sumber:
   - Visi & misi  : RPJMDes Pundungsari 2020-2026 (dokumen resmi desa)
   - APBDes       : Perdes No. 3 Tahun 2026 tentang Perubahan APBDes 2026
   - Kependudukan : Master Data Penduduk Pundungsari (per Okt 2026)
   - Perangkat    : hasil audit aplikasi operator (Okt 2026)
   - Alamat       : Berita Acara Kesepakatan Kades & BPD No.
                    100.3.7/3/427.81.06/2026
   ============================================================ */
const DB = {
  desa: {
    nama: "Pundungsari",
    kecamatan: "Tempursari",
    kabupaten: "Lumajang",
    provinsi: "Jawa Timur",
    kodePos: "67375",
    alamat: "Jl. Raya Pundungsari No. 16, Kec. Tempursari, Kab. Lumajang",
    telepon: "085236529079",
    email: "desapundungsari87@gmail.com",
    jamLayanan: "Senin–Jumat, 08.00–14.00 WIB",
  },

  profil: {
    sejarah: "Desa Pundungsari adalah salah satu desa di Kecamatan Tempursari, Kabupaten Lumajang, yang terletak di lereng tenggara Gunung Semeru. Masyarakatnya mayoritas bermata pencaharian sebagai petani dengan komoditas cabai, pisang, dan palawija.",
    visi: "Terwujudnya Masyarakat Pundungsari yang Berdaya Saing, Mandiri, Sejahtera, Berbudaya, Demokratis dan Bermartabat",
    misi: [
      "Meningkatkan SDM aparatur desa dan mewujudkan tata kelola pemerintahan yang lebih baik.",
      "Memberdayakan kelembagaan masyarakat dan Linmas desa.",
      "Meningkatkan sarana dan prasarana umum, pertanian, dan transportasi.",
      "Membina kerukunan umat beragama serta meningkatkan perekonomian masyarakat melalui pembinaan usaha kecil.",
      "Memberdayakan gotong royong dan karang taruna, serta melestarikan budaya dan kesenian daerah.",
      "Membentuk dan mengembangkan BUMDes serta mengoptimalkan sektor pertanian.",
    ],
    batasWilayah: { utara: "Desa Kaliuling", selatan: "Desa Tempursari", barat: "Desa Purorejo", timur: "Hutan Negara" },
    luas: "412 ha",
  },

  // Perangkat desa — dari hasil audit aplikasi operator (Okt 2026)
  perangkat: [
    { nama: "Mulyadi", jabatan: "Pj. Kepala Desa", foto: null },
    { nama: "Abdul Rohman", jabatan: "Sekretaris Desa", foto: null },
    { nama: "Singgih Firma A W", jabatan: "Kaur Perencanaan", foto: null },
    { nama: "Lia Khoiriyah", jabatan: "Kaur Keuangan", foto: null },
    { nama: "Ma'rifatul Khoiriyah", jabatan: "Kasi Pelayanan", foto: null },
    { nama: "Maskut Haryono", jabatan: "Kasi Kesra", foto: null },
    { nama: "Fendika Setiawan", jabatan: "Kasi Pemerintahan", foto: null },
  ],

  // 17 jenis layanan surat (dari aplikasi operator)
  layanan: [
    "Surat Keterangan", "Surat Keterangan Usaha (SKU)", "Surat Pengantar SKCK",
    "Fasilitasi KTP-el", "Fasilitasi Kartu Keluarga (KK)", "Kematian", "Kelahiran",
    "Pindah Penduduk", "Penduduk Datang", "Numpang Nikah (NCTR)",
    "Bepergian / Luar Negeri", "Pernyataan", "Kuasa",
    "Ahli Waris", "Izin Keramaian", "Legalisir Dokumen", "Nikah N1–N6",
  ],

  // Perubahan APBDes 2026 — Perdes No. 3 Tahun 2026 (angka resmi)
  apbdes: {
    tahun: 2026,
    catatan: "Data APBDes 2026 memerlukan verifikasi dengan dokumen perubahan anggaran terakhir sebelum dipublikasikan.",
    status: "perlu_verifikasi",
    pendapatan: 1040634980,
    belanja: 1115723251,
    rincianBelanja: [
      { bidang: "Belanja Pegawai", nilai: 374888800 },
      { bidang: "Belanja Barang dan Jasa", nilai: 513691400 },
      { bidang: "Belanja Modal", nilai: 200543052 },
      { bidang: "Belanja Tidak Terduga", nilai: 26600000 },
    ],
  },

  // Data kependudukan resmi (master data, Okt 2026)
  statistik: {
    penduduk: 4179, kk: 1460, laki: 2021, perempuan: 2146,
    status: "perlu_verifikasi", // 4.179 tidak sama dengan 2.021 + 2.146; jangan menebak angka baru
    dusun: 3,
  },

  // Berita asli desa
  berita: [
    { tgl: "15 Okt 2026", judul: "KIM Desa Pundungsari Ikuti Pembinaan Komunitas Informasi Masyarakat se-Kabupaten Lumajang", ringkas: "Abdul Rohman hadir sebagai anggota KIM Desa Pundungsari pada pembinaan yang dibuka Kepala Dinas Kominfo Kabupaten Lumajang di Sukodono." },
    { tgl: "07 Okt 2026", judul: "Monev RKPDesa 2027 dan P-APBDes 2026 oleh Kecamatan Tempursari", ringkas: "Kecamatan Tempursari melaksanakan monitoring dan evaluasi RKPDesa Tahun 2027 dan Perubahan APBDes 2026 di pendopo kecamatan." },
    { tgl: "21 Sep 2026", judul: "Musdes Pembahasan dan Kesepakatan RKPDesa 2027", ringkas: "Musyawarah desa membahas dan menyepakati RKPDesa Tahun 2027 bersama BPD dan unsur masyarakat." },
    { tgl: "18 Sep 2026", judul: "Musrenbangdes Penyusunan RKPDesa 2027", ringkas: "Musyawarah perencanaan pembangunan desa menjaring usulan prioritas untuk tahun anggaran 2027." },
  ],

  galeri: [], // unggah foto asli dan berizin publikasi sebelum dipakai
};
