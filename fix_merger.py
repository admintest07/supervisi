import re
with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Insert the filter indicator below the date range filter card and above the table
indicator_html = """                <div class="card" style="padding: 0;">
                    <div id="satuan-filter-indicator" style="display: none; padding: 1rem 1.25rem; background: #eef2ff; border-bottom: 1px solid #c7d2fe; color: #3730a3; font-weight: 700; font-size: 0.95rem; align-items: center; gap: 8px;">
                        <i class="material-icons-round" style="font-size: 1.2rem;">filter_alt</i> Menampilkan data untuk Satuan: <span id="satuan-filter-name" style="color: #1e1b4b; background: #c7d2fe; padding: 2px 8px; border-radius: 4px; margin-left: 4px;"></span>
                    </div>
                    <div class="table-container">"""

content = content.replace("""                <div class="card" style="padding: 0;">
                    <div class="table-container">""", indicator_html)

# 2. Update renderRekapTable
old_render = """        // Ambil hanya data untuk halaman ini
        const pagedData = filteredSupervisiData.slice(startIndex, endIndex);
        const hariArr = ['Minggu', 'Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu'];
        pagedData.forEach((s) => {
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
            
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td style="white-space: nowrap;">${formattedDate}</td>
                <td><div class="font-semibold text-main" style="font-size: 0.95rem;">${s.satuanPendidikan}</div></td>
                <td>
                    <div style="display: flex; align-items: center; gap: 8px;">
                        <div class="badge-spv">${s.namaSupervisor.charAt(0).toUpperCase()}</div>
                        <span style="font-size: 0.85rem; font-weight: 600; color: #334155;">${s.namaSupervisor}</span>
                    </div>
                </td>
                <td><div class="badge-waktu"><i class="material-icons-round" style="font-size: 1rem;">schedule</i> ${s.waktu} WIB</div></td>
                <td><div class="badge-temuan">${s.detailPertemuan.length} Temuan</div></td>
                <td>
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
        });"""

new_render = """        const filterSatuan = document.getElementById('filter-rekap-satuan') ? document.getElementById('filter-rekap-satuan').value : 'Semua';
        const isSatuanFiltered = filterSatuan !== 'Semua';
        
        const indContainer = document.getElementById('satuan-filter-indicator');
        const indName = document.getElementById('satuan-filter-name');
        if (indContainer && indName) {
            if (isSatuanFiltered) {
                indContainer.style.display = 'flex';
                indName.innerText = filterSatuan;
            } else {
                indContainer.style.display = 'none';
            }
        }

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
        });"""

content = content.replace(old_render, new_render)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

