"""Build the passage index for the site assistant (assets/ask-fr.json, assets/ask-en.json).

Each page is rendered in Chromium (the project list is built by JavaScript), then cut into
passages by section: one passage per paragraph group, never across two headings.
Run from the repo root after changing a page:  python3 _tools/ask/build_index.py
"""
import json, pathlib, subprocess, sys, time, urllib.parse
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parents[2]
PORT = 8791

EXTRACT = r"""
(page) => {
  const T = s => (s || "").replace(/\s+/g, " ").replace(/\s+([,.)])/g, "$1").trim();
  const out = [];
  const add = (key, title, section, text, anchorText) => { text = T(text); if (text.length > 25) out.push({key, title: T(title), section: T(section), text, anchor: T(anchorText || text)}); };
  if (page.startsWith("classic") || page === "index.html") {
    const intro = document.querySelector("#top .lede"); if (intro) add(page + "#top", document.querySelector("#intro-title").textContent, "Présentation", intro.textContent);
    document.querySelectorAll("#about .who p").forEach(p => add(page + "#about", document.getElementById("about-title").textContent, "", p.textContent));
    document.querySelectorAll("#experience .xp > li").forEach(li => add(page + "#experience", document.getElementById("exp-title").textContent, li.querySelector("h3").textContent, li.querySelector("h3").textContent + ", " + li.querySelector(".org").textContent + " (" + li.querySelector(".when").textContent + ") : " + [...li.querySelectorAll("ul li")].map(x => x.textContent).join(" "), li.querySelector("h3").textContent));
    document.querySelectorAll("#formation .edu > li").forEach(li => add(page + "#formation", document.getElementById("edu-title").textContent, "", li.textContent, li.querySelector("b").textContent));
    document.querySelectorAll("#competences .skills > div").forEach(d => add(page + "#competences", document.getElementById("sk-title").textContent, d.querySelector("h3").textContent, d.querySelector("h3").textContent + " : " + [...d.querySelectorAll("li")].map(x => x.textContent).join(", "), d.querySelector("li").textContent));
    const c = document.getElementById("contact"); add(page + "#contact", document.getElementById("contact-title").textContent, "", c.querySelector(".bighead p").textContent + " E-mail : loutoudeogratias@gmail.com · LinkedIn · GitHub · CV", c.querySelector(".bighead p").textContent);
    document.querySelectorAll("li.entry").forEach(li => {
      const id = li.id, h = li.querySelector("h3").textContent, tags = [...li.querySelectorAll(".tags span")].map(s => s.textContent).join(", ");
      add(page + "#" + id, h, li.querySelector(".date").textContent, li.querySelector(".one").textContent + " (" + tags + ")", li.querySelector(".one").textContent);
      li.querySelectorAll(".notes > div").forEach(d => add(page + "#" + id, h, d.querySelector("h4").textContent, d.querySelector("p").textContent));
    });
  } else {
    const main = document.querySelector("main"), h1 = main.querySelector("h1").textContent;
    const lede = main.querySelector(".lede"); if (lede) add(page, h1, "En bref", lede.textContent);
    const stats = [...main.querySelectorAll(".stats li")].map(li => li.textContent.replace(/\s+/g, " ").trim()).join(" ; ");
    if (stats) add(page, h1, "Chiffres clés", stats, main.querySelector(".stats li span").textContent);
    main.querySelectorAll("section").forEach(sec => {
      const h2 = sec.querySelector("h2"); if (!h2) return;
      let sub = "", buf = [];
      const flush = () => { if (buf.length) { add(page, h1, h2.textContent + (sub ? " › " + sub : ""), buf.join(" "), buf[0]); buf = []; } };
      [...sec.children].forEach(c => {
        if (c.tagName === "H2" || c.matches("figure, .chart, noscript, .flow + .note")) return;
        if (c.tagName === "H3") { flush(); sub = c.textContent; return; }
        if (c.matches("ol.flow")) { c.querySelectorAll("li").forEach(li => { flush(); add(page, h1, h2.textContent + " › " + li.querySelector("b").textContent, li.querySelector("p").textContent); }); return; }
        if (c.matches("table")) { c.querySelectorAll("tbody tr").forEach(tr => add(page, h1, h2.textContent + " › " + tr.cells[0].textContent, [...tr.cells].map(td => td.textContent).join(" : "), tr.cells[2].textContent)); return; }
        if (c.matches(".split")) { c.querySelectorAll("div").forEach(d => buf.push(d.textContent)); return; }
        const t = T(c.textContent); if (t) buf.push(t);
        if (buf.join(" ").length > 700) flush();
      });
      flush();
    });
  }
  return out;
}
"""

def link(key, anchor):
    # links to the passage itself with a text fragment; the anchor id (if any) is the fallback
    words = anchor.split()[:7]
    frag = urllib.parse.quote(" ".join(words), safe="")
    base = "/" + (key[len("index.html"):] if key.startswith("index.html") else key)
    return base + (":~:text=" if "#" in base else "#:~:text=") + frag

def build(pages, out_name):
    docs = []
    with sync_playwright() as pw:
        b = pw.chromium.launch(); p = b.new_page()
        for page in pages:
            p.goto(f"http://localhost:{PORT}/{page}" + ("?lang=fr" if page == "index.html" else "")); p.wait_for_timeout(600)
            for d in p.evaluate(EXTRACT, page):
                d["url"] = link(d["key"], d.pop("anchor")); docs.append(d)
        b.close()
    path = ROOT / "assets" / out_name
    old = json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}
    data = {"docs": docs}
    if isinstance(old, dict):  # keep the threshold and score written by eval.js
        data.update({k: v for k, v in old.items() if k != "docs"})
    path.write_text(json.dumps(data, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    print(out_name, len(docs), "passages,", path.stat().st_size // 1024, "Ko")

if __name__ == "__main__":
    srv = subprocess.Popen([sys.executable, "-m", "http.server", str(PORT)], cwd=ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(1)
    try:
        build(["index.html", "etudes/vigie.html", "etudes/bloc-operatoire.html", "etudes/accidents-route.html", "etudes/medicaments.html"], "ask-fr.json")
        build(["classic.html"], "ask-en.json")
    finally:
        srv.terminate()
