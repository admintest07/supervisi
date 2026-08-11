with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

old_func = """    window.getThemeForSatuan = (satName) => {
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
    };"""

new_func = """    window.getThemeForSatuan = (satName) => {
        const name = (satName || "").toLowerCase();
        if (name.includes('tk') || name.includes('taman kanak')) return { border: '#db2777', bg: 'linear-gradient(145deg, #ffffff 0%, #fdf2f8 100%)', iconBg: 'rgba(219,39,119,0.1)' };
        if (name.includes('sd') || name.includes('sekolah dasar')) return { border: '#ea580c', bg: 'linear-gradient(145deg, #ffffff 0%, #fff7ed 100%)', iconBg: 'rgba(234,88,12,0.1)' };
        if (name.includes('smp')) return { border: '#0284c7', bg: 'linear-gradient(145deg, #ffffff 0%, #f0f9ff 100%)', iconBg: 'rgba(2,132,199,0.1)' };
        if ((name.includes('sma') || name.includes('smk')) && !name.includes('boarding')) return { border: '#059669', bg: 'linear-gradient(145deg, #ffffff 0%, #ecfdf5 100%)', iconBg: 'rgba(5,150,105,0.1)' };
        if (name.includes('boarding') || name.includes('mbs')) return { border: '#8b5cf6', bg: 'linear-gradient(145deg, #ffffff 0%, #f5f3ff 100%)', iconBg: 'rgba(139,92,246,0.1)' };
        const fallbacks = [
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
    };"""

content = content.replace(old_func, new_func)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

