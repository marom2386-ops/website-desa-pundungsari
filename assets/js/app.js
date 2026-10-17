// Logika halaman publik Website Desa Pundungsari
const $ = s => document.querySelector(s);
const rupiah = n => "Rp" + n.toLocaleString("id-ID");
const escapeHtml = value => String(value ?? "").replace(/[&<>"\']/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","\'":"&#39;"}[c]));

/* navigasi SPA */
function nav(pg){
  document.querySelectorAll(".page").forEach(p => p.classList.remove("active"));
  const target = document.getElementById("pg-" + pg);
  if (!target) return;
  target.classList.add("active");
  document.querySelectorAll(".nav a").forEach(a => a.classList.toggle("active", a.dataset.nav === pg));
  document.getElementById("nav").classList.remove("open");
  document.getElementById("burger").setAttribute("aria-expanded","false");
  window.scrollTo({top: 0, behavior: "smooth"});
}
document.addEventListener("click", e => {
  const t = e.target.closest("[data-nav]");
  if (t){ e.preventDefault(); nav(t.dataset.nav); history.replaceState(null,"","#"+t.dataset.nav); if(t.dataset.nav === "berita") showNewsList(); }
});
document.getElementById("burger").addEventListener("click", () => {
  const open = document.getElementById("nav").classList.toggle("open");
  document.getElementById("burger").setAttribute("aria-expanded", String(open));
});

/* render dari DB */
(function render(){
  const d = DB.desa;
  // statistik
  const s = DB.statistik;
  const pendudukValid = Number.isInteger(s.penduduk) && (s.laki + s.perempuan === s.penduduk) && s.status !== "perlu_verifikasi";
  $("#statCards").innerHTML = [
    [pendudukValid ? s.penduduk.toLocaleString("id-ID") : "Verifikasi", "Jiwa Penduduk"],
    [s.kk.toLocaleString("id-ID"), "Kepala Keluarga"],
    [DB.layanan.length, "Jenis Layanan Surat"],
    [s.dusun + " Dusun", "Sukosari · Krajan · Sukorejo"],
  ].map(x => `<div class="stat"><strong>${x[0]}</strong><small>${x[1]}</small></div>`).join("");
  $("#statNote").hidden = pendudukValid;
  if (!pendudukValid) $("#statNote").textContent = "Jumlah penduduk belum dapat ditampilkan: angka total dan jumlah menurut jenis kelamin belum sesuai. Menunggu verifikasi data agregat resmi.";

  // layanan unggulan (6 pertama) — deskripsi khas per layanan
  const deskLayanan = {
    "Surat Keterangan": "Keterangan domisili, usaha, dan keperluan administrasi lainnya.",
    "Surat Keterangan Usaha (SKU)": "Untuk pengajuan modal usaha, kredit bank, dan perizinan.",
    "Surat Pengantar SKCK": "Pengantar SKCK untuk melamar pekerjaan dan keperluan resmi.",
    "Fasilitasi KTP-el": "Informasi dan fasilitasi administrasi KTP-el sesuai kewenangan desa.",
    "Fasilitasi Kartu Keluarga (KK)": "Fasilitasi permohonan KK; penerbitan dokumen dilakukan oleh instansi berwenang.",
    "Kematian": "Surat keterangan kematian untuk ahli waris dan administrasi kependudukan.",
  };
  $("#layananTop").innerHTML = DB.layanan.slice(0,6).map(l =>
    `<div class="card"><div class="c-body"><span class="badge">Layanan</span><h3>${l}</h3><p>${deskLayanan[l] || ("Urus di Balai Desa " + d.nama + " — cepat dan gratis.")}</p></div></div>`).join("");
  $("#layananChips").innerHTML = DB.layanan.map(l => `<span class="chip">📄 ${l}</span>`).join("");
  $("#jamLayanan").textContent = d.jamLayanan;

  // profil
  $("#sejarah").textContent = DB.profil.sejarah;
  $("#visi").textContent = DB.profil.visi;
  $("#misi").innerHTML = DB.profil.misi.map(m => `<li>${m}</li>`).join("");
  const b = DB.profil.batasWilayah;
  $("#tblWilayah").innerHTML = `
    <tr><th style="width:40%">Batas</th><th>Desa/Kecamatan</th></tr>
    <tr><td>Utara</td><td>${b.utara}</td></tr><tr><td>Timur</td><td>${b.timur}</td></tr>
    <tr><td>Selatan</td><td>${b.selatan}</td></tr><tr><td>Barat</td><td>${b.barat}</td></tr>
    <tr><td>Luas wilayah</td><td>${DB.profil.luas}</td></tr>`;

  // perangkat
  $("#perangkatCards").innerHTML = DB.perangkat.map(p => {
    const inisial = p.nama.split(" ").map(w => w[0]).slice(0,2).join("");
    return `<div class="card"><div class="c-body"><div class="avatar">${inisial}</div>
      <span class="badge">${p.jabatan}</span><h3>${p.nama}</h3></div></div>`;
  }).join("");

  // transparansi APBDes
  const a = DB.apbdes;
  $("#thnApbdes").textContent = a.tahun;
  $("#apbdesNote").textContent = a.catatan;
  const jumlahRincian = a.rincianBelanja.reduce((n, r) => n + r.nilai, 0);
  const anggaranValid = a.status !== "perlu_verifikasi" && jumlahRincian === a.belanja;
  $("#apPendapatan").textContent = anggaranValid ? rupiah(a.pendapatan) : "Dalam verifikasi";
  $("#apBelanja").textContent = anggaranValid ? rupiah(a.belanja) : "Dalam verifikasi";
  $("#apbdesAlert").hidden = anggaranValid;
  if (!anggaranValid) $("#apbdesAlert").textContent = "Angka dan klasifikasi belanja APBDes sedang dicocokkan dengan dokumen anggaran resmi terakhir. Data belum layak dipublikasikan sebagai angka final.";
  const maks = Math.max(...a.rincianBelanja.map(r => r.nilai));
  $("#apBars").innerHTML = !anggaranValid ? '<p class="muted">Rincian anggaran akan ditampilkan setelah diverifikasi.</p>' : a.rincianBelanja.map(r => `
    <div class="bar-row"><div class="lbl"><span>${r.bidang}</span><strong>${rupiah(r.nilai)}</strong></div>
    <div class="bar"><i style="width:${Math.round(r.nilai/maks*100)}%"></i></div></div>`).join("");

  // berita
  const card = n => `<div class="card"><div class="c-body"><span class="tgl">${n.tgl}</span>
    <h3>${n.judul}</h3><p>${n.ringkas}</p></div></div>`;
  $("#beritaTop").innerHTML = DB.berita.slice(0,3).map(card).join("");
  $("#beritaAll").innerHTML = DB.berita.map(card).join("");

  // kontak
  $("#tblKontak").innerHTML = `
    <tr><td style="width:35%"><strong>Alamat</strong></td><td>${d.alamat}</td></tr>
    <tr><td><strong>Kecamatan</strong></td><td>${d.kecamatan}</td></tr>
    <tr><td><strong>Kabupaten</strong></td><td>${d.kabupaten}, ${d.provinsi} ${d.kodePos}</td></tr>
    <tr><td><strong>Telepon</strong></td><td><a href="tel:${d.telepon.replace(/\D/g,"")}">${escapeHtml(d.telepon)}</a></td></tr>
    <tr><td><strong>Email</strong></td><td><a href="mailto:${encodeURIComponent(d.email)}">${escapeHtml(d.email)}</a></td></tr>
    <tr><td><strong>Jam layanan</strong></td><td>${d.jamLayanan}</td></tr>`;
})();


// Artikel berita, tautan langsung, dan berbagi: semua berjalan tanpa database pribadi.
const newsDetail = document.getElementById("artikelDetail");
const newsList = document.getElementById("beritaAll");
function showNewsList(){
  newsList.hidden = false;
  newsDetail.hidden = true;
  newsDetail.innerHTML = "";
}
function openArticle(index, preserveHash = false){
  const berita = DB.berita[index];
  if(!berita){showNewsList();return;}
  nav("berita");
  newsList.hidden = true;
  newsDetail.hidden = false;
  const url = location.origin + location.pathname + "#artikel-" + index;
  const wa = "https://wa.me/?text=" + encodeURIComponent(berita.judul + " — " + url);
  const fb = "https://www.facebook.com/sharer/sharer.php?u=" + encodeURIComponent(url);
  newsDetail.innerHTML = '<article class="article-card"><button type="button" id="backNews" class="btn outline">← Semua berita</button>'+
    '<p class="tgl">'+escapeHtml(berita.tgl)+'</p><h2>'+escapeHtml(berita.judul)+'</h2>'+
    '<p class="article-summary">'+escapeHtml(berita.ringkas)+'</p>'+
    '<p class="muted">Informasi di atas merupakan ringkasan kegiatan. Artikel lengkap dan dokumentasi resmi akan ditambahkan oleh pengelola setelah diverifikasi.</p>'+
    '<div class="article-actions"><a target="_blank" rel="noopener noreferrer" href="'+wa+'">Bagikan ke WhatsApp</a>'+
    '<a target="_blank" rel="noopener noreferrer" href="'+fb+'">Bagikan ke Facebook</a></div></article>';
  document.getElementById("backNews").addEventListener("click", ()=>{
    showNewsList();
    history.pushState(null, "", "#berita");
    nav("berita");
  });
  if(!preserveHash) history.pushState(null, "", "#artikel-" + index);
}
function addNewsButtons(){
  for(const [sel,items] of [["#beritaTop .card", DB.berita.slice(0,3)],["#beritaAll .card", DB.berita]]){
    document.querySelectorAll(sel).forEach((card,index)=>{
      const a = document.createElement("a");
      a.href = "#artikel-"+index;
      a.textContent = "Baca ringkasan lengkap →";
      a.className = "news-link";
      a.addEventListener("click", e=>{e.preventDefault();openArticle(index);});
      card.querySelector(".c-body").appendChild(a);
    });
  }
}
function handleInitialHash(){
  const hash = decodeURIComponent(location.hash.slice(1));
  const match = /^artikel-(\d+)$/.exec(hash);
  if(match){openArticle(Number(match[1]),true);return;}
  const pages = ["beranda","profil","pemerintahan","layanan","transparansi","berita","kontak"];
  if(pages.includes(hash)){nav(hash);if(hash==="berita")showNewsList();}
}
addNewsButtons();
window.addEventListener("popstate",handleInitialHash);
window.addEventListener("hashchange",handleInitialHash);
handleInitialHash();
