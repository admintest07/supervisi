import re
with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('console.warn("Mencatat log ke Firestore dilewati/gagal:", e);', 'console.warn("Mencatat log ke Firestore dilewati/gagal:", e.message || "error");')
content = content.replace('console.warn("Anon auth failed", err);', 'console.warn("Anon auth failed", err.message || "error");')
content = content.replace('console.error("Firebase Init Error:", error);', 'console.error("Firebase Init Error:", error.message || "error");')
content = content.replace('console.error("Login user error:", e);', 'console.error("Login user error:", e.message || "error");')
content = content.replace('console.error("Admin login error:", e);', 'console.error("Admin login error:", e.message || "error");')
content = content.replace('console.warn("Firestore log fetch permission/network error, fallback to local logs:", fsErr);', 'console.warn("Firestore log fetch error:", fsErr.message || "error");')
content = content.replace('console.error("Error load log trail:", e);', 'console.error("Error load log trail:", e.message || "error");')
content = content.replace('console.error("Gagal reset log:", e);', 'console.error("Gagal reset log:", e.message || "error");')
content = content.replace("console.log('SW registration failed:', error);", "console.log('SW registration failed:', error.message || 'error');")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)
