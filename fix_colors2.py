import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Inject window.getThemeForSatuan at the top level
theme_def = '''    window.getThemeForSatuan = (satName) => {
        const fallbacks = [
            { border: '#db2777', bg: 'linear-gradient(145deg, #ffffff 0%, #fdf2f8 100%)', iconBg: 'rgba(219,39,119,0.1)' },   // Pink
            { border: '#ea580c', bg: 'linear-gradient(145deg, #ffffff 0%, #fff7ed 100%)', iconBg: 'rgba(234,88,12,0.1)' },   // Orange
            { border: '#0284c7', bg: 'linear-gradient(145deg, #ffffff 0%, #f0f9ff 100%)', iconBg: 'rgba(2,132,199,0.1)' },   // Light Blue
            { border: '#059669', bg: 'linear-gradient(145deg, #ffffff 0%, #ecfdf5 100%)', iconBg: 'rgba(5,150,105,0.1)' },   // Emerald
            { border: '#8b5cf6', bg: 'linear-gradient(145deg, #ffffff 0%, #f5f3ff 100%)', iconBg: 'rgba(139,92,246,0.1)' },  // Violet
            { border: '#dc2626', bg: 'linear-gradient(145deg, #ffffff 0%, #fef2f2 100%)', iconBg: 'rgba(220,38,38,0.1)' },   // Red
            { border: '#0d9488', bg: 'linear-gradient(145deg, #ffffff 0%, #f0fdfa 100%)', iconBg: 'rgba(13,148,136,0.1)' },   // Teal
            { border: '#d97706', bg: 'linear-gradient(145deg, #ffffff 0%, #fffbeb 100%)', iconBg: 'rgba(217,119,6,0.1)' },   // Amber
            { border: '#4f46e5', bg: 'linear-gradient(145deg, #ffffff 0%, #eef2ff 100%)', iconBg: 'rgba(79,70,229,0.1)' },   // Indigo
            { border: '#65a30d', bg: 'linear-gradient(145deg, #ffffff 0%, #f7fee7 100%)', iconBg: 'rgba(101,163,13,0.1)' },  // Lime
            { border: '#0891b2', bg: 'linear-gradient(145deg, #ffffff 0%, #ecfeff 100%)', iconBg: 'rgba(8,145,178,0.1)' },   // Cyan
            { border: '#c026d3', bg: 'linear-gradient(145deg, #ffffff 0%, #fdf4ff 100%)', iconBg: 'rgba(192,38,211,0.1)' },  // Fuchsia
            { border: '#be123c', bg: 'linear-gradient(145deg, #ffffff 0%, #fff1f2 100%)', iconBg: 'rgba(190,18,60,0.1)' },   // Rose
            { border: '#a21caf', bg: 'linear-gradient(145deg, #ffffff 0%, #fdf4ff 100%)', iconBg: 'rgba(162,28,175,0.1)' },  // Fuchsia Dark
            { border: '#1d4ed8', bg: 'linear-gradient(145deg, #ffffff 0%, #eff6ff 100%)', iconBg: 'rgba(29,78,216,0.1)' },   // Blue Dark
        ];
        let hash = 0;
        for (let i = 0; i < satName.length; i++) hash = satName.charCodeAt(i) + ((hash << 5) - hash);
        return fallbacks[Math.abs(hash) % fallbacks.length];
    };

    window.isBulanInitialized = false;'''

content = content.replace("    window.isBulanInitialized = false;", theme_def)

# 2. Update updateDashboardChart colors
chart1_old = '''            const colors = [
                'rgba(79, 70, 229, 0.8)',
                'rgba(5, 150, 105, 0.8)',
                'rgba(234, 88, 12, 0.8)',
                'rgba(219, 39, 119, 0.8)',
                'rgba(2, 132, 199, 0.8)'
            ];
            const datasets = targetSatuan.map((sat, index) => {
                const dataValues = labels.map(m => {
                    return globalSupervisiData.filter(s => {
                        let matchSat = window.isSameSatuan(s.satuanPendidikan, sat);
                        let matchBulan = s.bulan === m;
                        return matchSat && matchBulan && s.createdByRole !== 'supervisor_lpis';
                    }).reduce((acc, s) => acc + (s.detailPertemuan?.length || 0), 0);
                });
                return {
                    label: sat,
                    data: dataValues,
                    backgroundColor: colors[index % colors.length],
                    borderColor: colors[index % colors.length].replace('0.8', '1'),
                    borderWidth: 1,
                    borderRadius: 4
                };
            });'''

chart1_new = '''            const datasets = targetSatuan.map((sat, index) => {
                const satTheme = window.getThemeForSatuan(sat);
                const dataValues = labels.map(m => {
                    return globalSupervisiData.filter(s => {
                        let matchSat = window.isSameSatuan(s.satuanPendidikan, sat);
                        let matchBulan = s.bulan === m;
                        return matchSat && matchBulan && s.createdByRole !== 'supervisor_lpis';
                    }).reduce((acc, s) => acc + (s.detailPertemuan?.length || 0), 0);
                });
                return {
                    label: sat,
                    data: dataValues,
                    backgroundColor: satTheme.border,
                    borderColor: satTheme.border,
                    borderWidth: 1,
                    borderRadius: 4
                };
            });'''

content = content.replace(chart1_old, chart1_new)

# 3. Update updateDailyChart colors
chart2_old = '''            const colors = [
                'rgba(79, 70, 229, 0.8)',
                'rgba(5, 150, 105, 0.8)',
                'rgba(234, 88, 12, 0.8)',
                'rgba(219, 39, 119, 0.8)',
                'rgba(2, 132, 199, 0.8)'
            ];
            const datasets = targetSatuan.map((sat, index) => {
                const dataValues = labels.map(dateStr => {
                    return globalSupervisiData.filter(s => {
                        let matchSat = window.isSameSatuan(s.satuanPendidikan, sat);
                        let matchDate = s.tanggal === dateStr;
                        return matchSat && matchDate && s.createdByRole !== 'supervisor_lpis';
                    }).reduce((acc, s) => acc + (s.detailPertemuan?.length || 0), 0);
                });
                return {
                    label: sat,
                    data: dataValues,
                    backgroundColor: colors[index % colors.length],
                    borderColor: colors[index % colors.length].replace('0.8', '1'),
                    borderWidth: 2,
                    tension: 0.3,
                    fill: false,
                    pointBackgroundColor: colors[index % colors.length]
                };
            });'''

chart2_new = '''            const datasets = targetSatuan.map((sat, index) => {
                const satTheme = window.getThemeForSatuan(sat);
                const dataValues = labels.map(dateStr => {
                    return globalSupervisiData.filter(s => {
                        let matchSat = window.isSameSatuan(s.satuanPendidikan, sat);
                        let matchDate = s.tanggal === dateStr;
                        return matchSat && matchDate && s.createdByRole !== 'supervisor_lpis';
                    }).reduce((acc, s) => acc + (s.detailPertemuan?.length || 0), 0);
                });
                return {
                    label: sat,
                    data: dataValues,
                    backgroundColor: satTheme.border,
                    borderColor: satTheme.border,
                    borderWidth: 2,
                    tension: 0.3,
                    fill: false,
                    pointBackgroundColor: satTheme.border
                };
            });'''

content = content.replace(chart2_old, chart2_new)

# 4. Remove the inline getThemeForSatuan in updateStats
grid_old = '''                const getThemeForSatuan = (satName) => {
                    const name = satName.toLowerCase();
                    if (name.includes('tk') || name.includes('taman kanak')) return { border: '#db2777', bg: 'linear-gradient(145deg, #ffffff 0%, #fdf2f8 100%)', iconBg: 'rgba(219,39,119,0.1)' };
                    if (name.includes('sd') || name.includes('sekolah dasar')) return { border: '#ea580c', bg: 'linear-gradient(145deg, #ffffff 0%, #fff7ed 100%)', iconBg: 'rgba(234,88,12,0.1)' };
                    if (name.includes('smp')) return { border: '#0284c7', bg: 'linear-gradient(145deg, #ffffff 0%, #f0f9ff 100%)', iconBg: 'rgba(2,132,199,0.1)' };
                    if ((name.includes('sma') || name.includes('smk')) && !name.includes('boarding')) return { border: '#059669', bg: 'linear-gradient(145deg, #ffffff 0%, #ecfdf5 100%)', iconBg: 'rgba(5,150,105,0.1)' };
                    if (name.includes('boarding') || name.includes('mbs')) return { border: '#8b5cf6', bg: 'linear-gradient(145deg, #ffffff 0%, #f5f3ff 100%)', iconBg: 'rgba(139,92,246,0.1)' };
                    const fallbacks = [
                        { border: '#4f46e5', bg: 'linear-gradient(145deg, #ffffff 0%, #eef2ff 100%)', iconBg: 'rgba(79,70,229,0.1)' },
                        { border: '#0d9488', bg: 'linear-gradient(145deg, #ffffff 0%, #f0fdfa 100%)', iconBg: 'rgba(13,148,136,0.1)' },
                        { border: '#d97706', bg: 'linear-gradient(145deg, #ffffff 0%, #fffbeb 100%)', iconBg: 'rgba(217,119,6,0.1)' },
                    ];
                    let hash = 0;
                    for (let i = 0; i < satName.length; i++) hash = satName.charCodeAt(i) + ((hash << 5) - hash);
                    return fallbacks[Math.abs(hash) % fallbacks.length];
                };

                listSatuan.forEach((sat) => {
                    const theme = getThemeForSatuan(sat);'''

grid_new = '''                listSatuan.forEach((sat) => {
                    const theme = window.getThemeForSatuan(sat);'''

content = content.replace(grid_old, grid_new)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Colors fixed everywhere!")
