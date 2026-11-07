// Measures the site assistant on the question sets. Usage: node _tools/ask/eval.js [--tune] [--details]
// --tune picks the refusal threshold on the "reglage" set only, then reports both sets and saves
// the threshold and the control-set score into assets/ask-fr.json.
const fs = require("fs"), path = require("path");
const ROOT = path.resolve(__dirname, "../..");
const Index = require(path.join(ROOT, "assets/ask.js"));
const Q = JSON.parse(fs.readFileSync(path.join(__dirname, "questions.json"), "utf8"));
const file = path.join(ROOT, "assets/ask-fr.json"), data = JSON.parse(fs.readFileSync(file, "utf8"));
const idx = new Index(data.docs);
const args = process.argv.slice(2);

function run(set, hors, T, show){
  let found = 0, top1 = 0, missed = [], ref = 0, wrong = [];
  for (const it of set){
    const r = idx.search(it.q, {threshold:T});
    const keys = r.hits.map(h => h.x.d.key);
    const ok = !r.refused && keys.some(k => it.expect.includes(k));
    if (ok) found++; if (!r.refused && it.expect.includes(keys[0])) top1++;
    if (!ok) missed.push(`${it.q}  [cov ${r.best.toFixed(2)}${r.refused ? ", refusée" : ""}] -> ${keys.join(", ")}`);
  }
  for (const q of hors){ const r = idx.search(q, {threshold:T}); if (r.refused) ref++; else wrong.push(`${q}  [cov ${r.best.toFixed(2)}] -> ${r.hits[0].x.d.key}`); }
  if (show){ missed.forEach(m => console.log("  manquée :", m)); wrong.forEach(m => console.log("  pas refusée :", m)); }
  return {found, top1, n:set.length, ref, nh:hors.length};
}
let T = data.threshold != null ? data.threshold : Index.THRESHOLD;
if (args.includes("--tune")){
  let best = null;
  for (let t = 0.2; t <= 0.9001; t += 0.05){
    const r = run(Q.reglage, Q.reglage_hors, t, false), s = r.found / r.n + r.ref / r.nh;
    console.log(`seuil ${t.toFixed(2)} : ${r.found}/${r.n} trouvées, ${r.ref}/${r.nh} refusées`);
    if (!best || s > best.s + 1e-9) best = {t, s};
  }
  T = +best.t.toFixed(2); console.log("seuil retenu :", T);
}
const show = args.includes("--details");
console.log("\nRéglage"); const a = run(Q.reglage, Q.reglage_hors, T, show);
console.log(`  ${a.found}/${a.n} bonne page parmi les 3 premières (${a.top1} en 1re), ${a.ref}/${a.nh} hors sujet refusées`);
console.log("Contrôle (jamais utilisé pour régler)"); const c = run(Q.controle, Q.controle_hors, T, show);
console.log(`  ${c.found}/${c.n} bonne page parmi les 3 premières (${c.top1} en 1re), ${c.ref}/${c.nh} hors sujet refusées`);
if (args.includes("--tune")){
  data.threshold = T;
  data.eval = {threshold:T, control:c, tuning:a,
    text:`sur ${c.n + c.nh} questions de contrôle écrites avant tout réglage, la bonne page arrive parmi les 3 premiers résultats pour ${c.found} questions sur ${c.n}, et ${c.ref} questions hors sujet sur ${c.nh} sont refusées.`};
  fs.writeFileSync(file, JSON.stringify(data));
  const enFile = path.join(ROOT, "assets/ask-en.json"), en = JSON.parse(fs.readFileSync(enFile, "utf8"));
  en.threshold = T; en.eval = {text:`measured on the French version: on ${c.n + c.nh} hold-out questions written before any tuning, the right page is in the top 3 results for ${c.found} of ${c.n}, and ${c.ref} of ${c.nh} off-topic questions are refused.`};
  fs.writeFileSync(enFile, JSON.stringify(en));
}
