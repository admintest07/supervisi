const fs = require('fs');
const html = fs.readFileSync('index.html', 'utf8');

// Parse all inline event attribute values
const inlineRegex = /on([a-z]+)\s*=\s*["']([^"']+)["']/gi;
let match;
const inlineEvents = [];
while ((match = inlineRegex.exec(html)) !== null) {
  inlineEvents.push({ event: match[1], code: match[2] });
}

// Find all function calls in code snippets
const fnNames = new Set();
inlineEvents.forEach(ie => {
  // matches word followed by (
  const matches = ie.code.matchAll(/([a-zA-Z0-9_$]+)\s*\(/g);
  for (const m of matches) {
    const fn = m[1];
    if (!['if', 'for', 'while', 'switch', 'catch', 'alert', 'confirm', 'prompt', 'parseInt', 'parseFloat', 'String', 'Number', 'Boolean', 'Date', 'Math', 'JSON', 'encodeURIComponent', 'preventDefault', 'stopPropagation'].includes(fn)) {
      fnNames.add(fn);
    }
  }
});

console.log("Functions called in inline events:", Array.from(fnNames));

// Check each function in script
const moduleScript = html.match(/<script type="module">([\s\S]*?)<\/script>/)[1];

Array.from(fnNames).forEach(fn => {
  // Is it window.fn = ... or function fn() ...?
  const windowAssigned = new RegExp(`window\\.${fn}\\s*=`).test(moduleScript);
  const funcDeclared = new RegExp(`function\\s+${fn}\\b`).test(moduleScript);
  const constLetVarDeclared = new RegExp(`(const|let|var)\\s+${fn}\\s*=`).test(moduleScript);

  if (!windowAssigned) {
    if (funcDeclared || constLetVarDeclared) {
      console.log(`⚠️ ${fn}: declared in module scope but NOT attached to window!`);
    } else {
      console.log(`❌ ${fn}: NOT FOUND in script!`);
    }
  } else {
    console.log(`✅ ${fn}: attached to window`);
  }
});

