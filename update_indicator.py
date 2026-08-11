import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update HTML structure for indicator banner
# Replace old indicator if present or insert between filter card and table card
old_indicator_pattern = r'<div class="card" style="padding: 0;">\s*<div id="satuan-filter-indicator".*?</div>\s*<div class="table-container">'

new_indicator_html = """<div id="satuan-filter-indicator" class="card" style="display: none; padding: 0.85rem 1.25rem; background: #eef2ff; border: 1px solid #c7d2fe; border-radius: 12px; margin-bottom: 1rem; color: #3730a3; font-weight: 600; font-size: 0.95rem; align-items: center; justify-content: space-between;">
                    <div style="display: flex; align-items: center; gap: 8px;">
                        <i class="material-icons-round" style="font-size: 1.25rem; color: #4f46e5;">filter_alt</i>
                        <span>Menampilkan Data Supervisi Satuan: <strong id="satuan-filter-name" style="color: #1e1b4b; background: #c7d2fe; padding: 3px 10px; border-radius: 6px; font-weight: 700; margin-left: 4px;"></strong></span>
                    </div>
                    <button class="btn btn-outline" style="padding: 0.25rem 0.6rem; font-size: 0.8rem; background: #ffffff; border-color: #a5b4fc; color: #3730a3; font-weight: 600;" onclick="resetSatuanFilter()"><i class="material-icons-round" style="font-size: 1rem;">close</i> Tampilkan Semua Satuan</button>
                </div>
                <div class="card" style="padding: 0;">
                    <div class="table-container">"""

if "satuan-filter-indicator" in content:
    content = re.sub(old_indicator_pattern, new_indicator_html, content, flags=re.DOTALL)
else:
    content = content.replace("""                <div class="card" style="padding: 0;">
                    <div class="table-container">""", new_indicator_html)

# 2. Add helper functions for indicator
helper_js = """
    window.updateSatuanFilterIndicator = function() {
        const indContainer = document.getElementById('satuan-filter-indicator');
        const indName = document.getElementById('satuan-filter-name');
        if (!indContainer || !indName) return;

        const selSatuan = document.getElementById('filter-rekap-satuan');
        const filterSatuan = selSatuan ? selSatuan.value : 'Semua';

        let activeSatuan = '';
        if (filterSatuan && filterSatuan !== 'Semua') {
            activeSatuan = filterSatuan;
        } else if (currentUser && currentUser.role !== 'admin' && currentUser.role !== 'supervisor_lpis' && currentUser.satuanPendidikan) {
            activeSatuan = currentUser.satuanPendidikan;
        }

        if (activeSatuan) {
            indContainer.style.display = 'flex';
            indName.innerText = activeSatuan;
        } else {
            indContainer.style.display = 'none';
        }
    };

    window.resetSatuanFilter = function() {
        const selSatuan = document.getElementById('filter-rekap-satuan');
        if (selSatuan) selSatuan.value = 'Semua';
        window.applyFilterRekap();
    };
"""

# Insert helper_js right before window.applyFilterRekap
content = content.replace("window.applyFilterRekap = () => {", helper_js + "\n    window.applyFilterRekap = () => {")

# 3. Update applyFilterRekap to call updateSatuanFilterIndicator
content = content.replace("renderRekapTable();\n    };", "updateSatuanFilterIndicator();\n        renderRekapTable();\n    };")
content = content.replace("renderRekapTable();    };", "updateSatuanFilterIndicator(); renderRekapTable(); };")

# 4. Replace renderRekapTable implementation with proper indicator call at start and rowspan table merging
old_render_fn_start = "window.renderRekapTable = function renderRekapTable() {"

new_render_fn = """window.renderRekapTable = function renderRekapTable() {
        if (window.updateSatuanFilterIndicator) window.updateSatuanFilterIndicator();
        const tbody = document.getElementById('tbody-rekap');
        tbody.innerHTML = '';

        const filterSatuan = document.getElementById('filter-rekap-satuan') ? document.getElementById('filter-rekap-satuan').value : 'Semua';
        const isSatuanFiltered = filterSatuan !== 'Semua' || (currentUser && currentUser.role !== 'admin' && currentUser.role !== 'supervisor_lpis');

        const totalItems = filteredSupervisiData.length;
        const totalPages = Math.ceil(totalItems / itemsPerPage) || 1;

        // Perbarui Info Paginasi
        const btnPrev = document.getElementById('btn-prev-page');
        const btnNext = document.getElementById('btn-next-page');
        const infoText = document.getElementById('pagination-info');

        if(totalItems === 0) {
            if(infoText) infoText.innerText = `Menampilkan 0 - 0 dari 0 data`;
            btnPrev.disabled = true; btnPrev.style.opacity = '0.5';
            btnNext.disabled = true; btnNext.style.opacity = '0.5';
            tbody.innerHTML = `<tr><td colspan="6"><div class="empty-state"><i class="material-icons-round">folder_open</i><p>Tidak ada data laporan ditemukan pada filter ini.</p></div></td></tr>`; 
            return;
        }

        // Hitung batasan potong data (slice)
        if (currentPage > totalPages) currentPage = totalPages;
        const startIndex = (currentPage - 1) * itemsPerPage;
        const endIndex = Math.min(startIndex + itemsPerPage, totalItems);

        // Update teks dan status tombol
        if(infoText) infoText.innerText = `Menampilkan ${startIndex + 1} - ${endIndex} dari ${totalItems} data`;
        btnPrev.disabled = currentPage === 1; btnPrev.style.opacity = currentPage === 1 ? '0.5' : '1';
        btnNext.disabled = currentPage === totalPages; btnNext.style.opacity = currentPage === totalPages ? '0.5' : '1';

        // Ambil hanya data untuk halaman ini
        const pagedData = filteredSupervisiData.slice(startIndex, endIndex);
        const hariArr = ['Minggu', 'Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu'];

        let dateSpans = [];
        if (isSatuanFiltered) {
            let i = 0;
            while (i < pagedData.length) {
                let count = 1;
                while (i + count < pagedData.length && pagedData[i].tanggal === pagedData[i + count].tanggal) {
                    count++;
                }
                dateSpans.push(count);
                for (let j = 1; j < count; j++) dateSpans.push(0);
                i += count;
            }
        }

        pagedData.forEach((s, idx) => {
            const originalIdx = globalSupervisiData.findIndex(g => g.id === s.id);
            
            // Konversi Tanggal ke Format: Hari, DD/MM/YY
            let formattedDate = s.tanggal;
            try {
                const d = new Date(s.tanggal);
                if(!isNaN(d)) {
                    const namaHari = hariArr[d.getDay()];
                    const tgl = d.getDate().toString().padStart(2, '0');
                    const bln = (d.getMonth() + 1).toString().padStart(2, '0');
                    const thn = d.getFullYear().toString().slice(-2);
                    // Disusun 2 baris (Hari dicetak tebal, tanggal warna abu-abu di bawahnya)
                    formattedDate = `<div style="font-weight: 800; color: var(--text-main); font-size: 0.9rem;">${namaHari}</div><div style="font-size: 0.75rem; font-weight: 600; color: #64748b; margin-top: 2px;">${tgl}/${bln}/${thn}</div>`;
                }
            } catch(e) {}
            
            let dateTd = '';
            let satuanTd = '';
            
            if (isSatuanFiltered) {
                if (dateSpans[idx] > 0) {
                    dateTd = `<td rowspan="${dateSpans[idx]}" style="white-space: nowrap; vertical-align: top; border-bottom: 1px solid var(--border-color); background: #ffffff;">${formattedDate}</td>`;
                    satuanTd = `<td rowspan="${dateSpans[idx]}" style="vertical-align: top; border-bottom: 1px solid var(--border-color); background: #ffffff;"><div class="font-semibold text-main" style="font-size: 0.95rem;">${s.satuanPendidikan}</div></td>`;
                }
            } else {
                dateTd = `<td style="white-space: nowrap; vertical-align: top;">${formattedDate}</td>`;
                satuanTd = `<td style="vertical-align: top;"><div class="font-semibold text-main" style="font-size: 0.95rem;">${s.satuanPendidikan}</div></td>`;
            }

            const tr = document.createElement('tr');
            tr.innerHTML = `
                ${dateTd}
                ${satuanTd}
                <td style="vertical-align: top;">
                    <div style="display: flex; align-items: center; gap: 8px;">
                        <div class="badge-spv">${s.namaSupervisor.charAt(0).toUpperCase()}</div>
                        <span style="font-size: 0.85rem; font-weight: 600; color: #334155;">${s.namaSupervisor}</span>
                    </div>
                </td>
                <td style="vertical-align: top;"><div class="badge-waktu"><i class="material-icons-round" style="font-size: 1rem;">schedule</i> ${s.waktu} WIB</div></td>
                <td style="vertical-align: top;"><div class="badge-temuan">${s.detailPertemuan.length} Temuan</div></td>
                <td style="vertical-align: top;">
                    <div class="action-group">
                        <button class="btn-action view" title="Lihat Detail" onclick="lihatDetail(${originalIdx})">
                            <i class="material-icons-round" style="font-size:1.2rem;">visibility</i>
                        </button>
                        <button class="btn-action edit" title="Edit Data" onclick="editSupervisi(${originalIdx})">
                            <i class="material-icons-round" style="font-size:1.2rem;">edit</i>
                        </button>
                        <button class="btn-action delete" title="Hapus Data" onclick="hapusSupervisi('${s.id}')">
                            <i class="material-icons-round" style="font-size:1.2rem;">delete</i>
                        </button>
                    </div>
                </td>
            `;
            tbody.appendChild(tr);
        });
    }"""

# Find full renderRekapTable function and replace
render_pattern = r'window\.renderRekapTable = function renderRekapTable\(\) \{.*?\n    \}'
content = re.sub(render_pattern, new_render_fn, content, flags=re.DOTALL)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated index.html successfully.")
