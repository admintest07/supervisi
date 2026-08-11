with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

target_loadLogTrail = '''    window.loadLogTrail = async function loadLogTrail() {        const tbody = document.getElementById('tbody-logtrail');        if (!tbody) return;        tbody.innerHTML = '<tr><td colspan="5" style="text-align:center; padding:1.5rem;"><i class="material-icons-round" style="animation: spin 1s linear infinite;">sync</i> Memuat riwayat log...</td></tr>';                try {            globalLogs = [];            if (IS_PREVIEW) {                globalLogs = window.mockLogs || [];            } else {                try {                    const snap = await getDocs(collection(db, "logs"));                    snap.forEach(doc => globalLogs.push({ id: doc.id, ...doc.data() }));                } catch(fsErr) {                    console.warn("Firestore log fetch permission/network error, fallback to local logs:", fsErr);                    globalLogs = window.mockLogs || [];                }            }            if (globalLogs.length === 0 && window.mockLogs && window.mockLogs.length > 0) {                globalLogs = [...window.mockLogs];            }            globalLogs.sort((a,b) => (b.timestamp || 0) - (a.timestamp || 0));            filterLogTrail();        } catch(e) {            console.error("Error load log trail:", e);            globalLogs = window.mockLogs || [];            filterLogTrail();        }    };'''

replacement_loadLogTrail = '''    window.loadLogTrail = async function loadLogTrail() {
        const tbody = document.getElementById('tbody-logtrail');
        if (!tbody) return;
        tbody.innerHTML = '<tr><td colspan="5" style="text-align:center; padding:1.5rem;"><i class="material-icons-round" style="animation: spin 1s linear infinite;">sync</i> Memuat riwayat log...</td></tr>';
        
        try {
            globalLogs = [];
            const savedLocal = localStorage.getItem('supervisi_mock_logs');
            let localLogs = [];
            if (savedLocal) {
                try { localLogs = JSON.parse(savedLocal); } catch(e){}
            }
            if (IS_PREVIEW) {
                globalLogs = (window.mockLogs && window.mockLogs.length > 0) ? window.mockLogs : localLogs;
            } else {
                try {
                    const snap = await getDocs(collection(db, "logs"));
                    snap.forEach(doc => globalLogs.push({ id: doc.id, ...doc.data() }));
                } catch(fsErr) {
                    console.warn("Firestore log fetch permission/network error, fallback to local logs:", fsErr);
                    globalLogs = (window.mockLogs && window.mockLogs.length > 0) ? window.mockLogs : localLogs;
                }
            }
            if (globalLogs.length === 0) {
                globalLogs = localLogs.length > 0 ? localLogs : (window.mockLogs || []);
            }
            globalLogs.sort((a,b) => (b.timestamp || 0) - (a.timestamp || 0));
            filterLogTrail();
        } catch(e) {
            console.error("Error load log trail:", e);
            globalLogs = window.mockLogs || [];
            filterLogTrail();
        }
    };'''

if target_loadLogTrail in content:
    content = content.replace(target_loadLogTrail, replacement_loadLogTrail)
    print("loadLogTrail updated successfully")
else:
    print("target_loadLogTrail not found directly")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)
