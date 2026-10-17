// Logika Dasbor Admin — versi demo (localStorage). Ganti PIN & sumber data saat deploy.
const PIN_DEMO = "1234"; // GANTI dengan PIN asli / sistem login Apps Script
const $ = s => document.querySelector(s);
const LS_BERITA = "pundungsari_berita";

/* ---------- login ---------- */
$("#btnLogin").addEventListener("click", login);
$("#pinInput").addEventListener("keydown", e => { if (e.key === "Enter") login(); });
function login(){
  if ($("#pinInput").value === PIN_DEMO){
    $("#loginWrap").classList.add("hidden");
    $("#app").classList.remove("hidden");
    renderAll();
  } else {
    $("#loginErr").textContent = "PIN salah. Coba lagi.";
  }
}
$("#btnLogout").addEventListener("click", () => location.reload());

/* ---------- navigasi ---------- */
document.addEventListener("click", e => {
  const t = e.target.closest("[data-adm]");
  if (!t) return;
  e.preventDefault();
  document.querySelectorAll(".apage").forEach(p => p.classList.remove("active"));
  document.getElementById("ad-" + t.dataset.adm).classList.add("active");
  document.querySelectorAll(".side nav a").forEach(a => a.classList.toggle("active", a === t));
  $("#admTitle").textContent = t.textContent.trim().replace(/^[^\s]+\s/, "");
});

/* ---------- data berita (localStorage) ---------- */
function getBerita(){
  try {
    const s = JSON.parse(localStorage.getItem(LS_BERITA));
    if (Array.isArray(s) && s.length) return s;
  } catch(e){}
  return DB.berita.map(b => ({...b}));
}
function setBerita(arr){ localStorage.setItem(LS_BERITA, JSON.stringify(arr)); }

/* ---------- render ---------- */
function renderAll(){
  // KPI
  $("#kPenduduk").textContent = DB.statistik.penduduk.toLocaleString("id-ID");
  const ber = getBerita();
  $("#kBerita").textContent = ber.length;

  // chart surat per bulan (contoh)
  const bulan = ["Mei","Jun","Jul","Agu","Sep","Okt"];
  const nilai = [28, 35, 31, 39, 44, 42];
  const maks = Math.max(...nilai);
  $("#chartSurat").innerHTML = bulan.map((b,i) =>
    `<div class="col"><i style="height:${Math.round(nilai[i]/maks*140)}px" title="${nilai[i]}"></i><span>${b}</span></div>`).join("");

  // aktivitas
  $("#tblAktivitas").innerHTML = `
    <tr><th>Waktu</th><th>Aktivitas</th></tr>
    <tr><td>08 Okt 2026</td><td>Audit aplikasi operator V20 selesai</td></tr>
    <tr><td>07 Okt 2026</td><td>Monev RKPDesa 2027 &amp; P-APBDes 2026 oleh kecamatan</td></tr>
    <tr><td>06 Okt 2026</td><td>Berkas Perubahan Kedua APBDes 2026 difinalkan (F4)</td></tr>`;

  renderBerita(ber);

  // layanan
  $("#nLayanan").textContent = DB.layanan.length;
  $("#admLayanan").innerHTML = DB.layanan.map(l => `<span class="chip">${l}</span>`).join("");
  const rekap = [["Surat Keterangan",12],["SKU",5],["Kematian",3],["Kelahiran",4],["KK",6],["Lainnya",12]];
  $("#tblRekap").innerHTML = `<tr><th>Jenis</th><th>Jumlah</th></tr>` +
    rekap.map(r => `<tr><td>${r[0]}</td><td>${r[1]}</td></tr>`).join("");
}

function renderBerita(ber){
  $("#tblBerita").innerHTML = `<tr><th>Tanggal</th><th>Judul</th><th>Aksi</th></tr>` +
    ber.map((b,i) => `<tr><td>${b.tgl}</td><td>${b.judul}</td>
      <td class="aksi"><button data-del="${i}" title="Hapus">🗑️</button></td></tr>`).join("");
  document.querySelectorAll("[data-del]").forEach(btn =>
    btn.addEventListener("click", () => {
      if (!confirm("Hapus berita ini?")) return;
      const arr = getBerita(); arr.splice(+btn.dataset.del, 1);
      setBerita(arr); renderBerita(arr);
      $("#kBerita").textContent = arr.length;
    }));
}

$("#btnTambahBerita").addEventListener("click", () => {
  const j = $("#bJudul").value.trim(), r = $("#bRingkas").value.trim();
  if (!j || !r){ alert("Isi judul dan ringkasan dulu."); return; }
  const t = $("#bTgl").value;
  const tgl = t ? new Date(t + "T00:00").toLocaleDateString("id-ID", {day:"2-digit",month:"short",year:"numeric"}) : "—";
  const arr = getBerita(); arr.unshift({tgl, judul: j, ringkas: r});
  setBerita(arr); renderBerita(arr);
  $("#kBerita").textContent = arr.length;
  $("#bJudul").value = $("#bRingkas").value = ""; $("#bTgl").value = "";
  alert("Berita ditambahkan (tersimpan di browser demo).");
});

$("#btnSimpanSet").addEventListener("click", () => {
  $("#setOk").textContent = "✓ Pengaturan disimpan (demo — hubungkan ke Sheets saat deploy).";
  setTimeout(() => $("#setOk").textContent = "", 3500);
});
