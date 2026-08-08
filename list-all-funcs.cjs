const fs = require('fs');
const html = fs.readFileSync('index.html', 'utf8');

const funcRegex = /function\s+([a-zA-Z0-9_$]+)\s*\(/g;
let match;
while ((match = funcRegex.exec(html)) !== null) {
  const name = match[1];
  const isWindow = new RegExp(`window\\.${name}\\s*=`).test(html);
  console.log(`Function: ${name} -> Window Attached? ${isWindow}`);
}
