// Logika halaman publik Website Desa Pundungsari
const $ = s => document.querySelector(s);
const rupiah = n => "Rp" + n.toLocaleString("id-ID");

/* navigasi SPA */
function nav(pg){
  document.querySelectorAll(".page").forEach(p => p.classList.remove("active"));
  document.getElementById("pg-" + pg).classList.add("active");
  document.querySelectorAll(".nav a").forEach(a => a.classList.toggle("active", a.dataset.nav === pg));
  document.getElementById("nav").classList.remove("open");
  window.scrollTo({top: 0, behavior: "smooth"});
}
document.addEventListener("click", e => {
  const t = e.target.closest("[data-nav]");
  if (t){ e.preventDefault(); nav(t.dataset.nav); }
});
document.getElementById("burger").addEventListener("click", () =>
  document.getElementById("nav").classList.toggle("open"));

/* render dari DB */
(function render(){
  const d = DB.desa;
  // statistik
  const s = DB.statistik;
  $("#statCards").innerHTML = [
    [s.penduduk.toLocaleString("id-ID"), "Jiwa Penduduk"],
    [s.kk.toLocaleString("id-ID"), "Kepala Keluarga"],
    [DB.layanan.length, "Jenis Layanan Surat"],
    [s.dusun + " Dusun", "Sukosari · Krajan · Sukorejo"],
  ].map(x => `<div class="stat"><strong>${x[0]}</strong><small>${x[1]}</small></div>`).join("");

  // layanan unggulan (6 pertama) — deskripsi khas per layanan
  const deskLayanan = {
    "Surat Keterangan": "Keterangan domisili, usaha, dan keperluan administrasi lainnya.",
    "Surat Keterangan Usaha (SKU)": "Untuk pengajuan modal usaha, kredit bank, dan perizinan.",
    "SKCK": "Surat pengantar SKCK untuk melamar pekerjaan dan keperluan resmi.",
    "KTP-el": "Pengantar perekaman dan penerbitan KTP elektronik.",
    "Kartu Keluarga (KK)": "Penerbitan KK baru, pembaruan data, dan pecah KK.",
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
  $("#apPendapatan").textContent = rupiah(a.pendapatan);
  $("#apBelanja").textContent = rupiah(a.belanja);
  const maks = Math.max(...a.rincianBelanja.map(r => r.nilai));
  $("#apBars").innerHTML = a.rincianBelanja.map(r => `
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
    <tr><td><strong>Telepon</strong></td><td>${d.telepon}</td></tr>
    <tr><td><strong>Email</strong></td><td>${d.email}</td></tr>
    <tr><td><strong>Jam layanan</strong></td><td>${d.jamLayanan}</td></tr>`;
})();
