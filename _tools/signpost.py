"""Signposted home pages (index.html fr, classic.html en): a guide of big tiles under the intro, then
numbered sections with big titles and icons: projects, experience, education, skills, about, contact.
The detailed project list and the 3D district follow as "to go further". Run once; idempotent on markers."""
import pathlib, re

ROOT = pathlib.Path(__file__).resolve().parents[1]

ICON = {
 "doc": '<path d="M14 3H6a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V9z"/><path d="M14 3v6h6M8 13h8M8 17h6"/>',
 "chart": '<path d="M4 20V11M10 20V4M16 20v-8M21 20H3"/>',
 "case": '<rect x="3" y="7" width="18" height="13" rx="2"/><path d="M9 7V5a2 2 0 0 1 2-2h2a2 2 0 0 1 2 2v2M3 13h18"/>',
 "cap": '<path d="M2 9l10-5 10 5-10 5z"/><path d="M6 11v5c3 2 9 2 12 0v-5M22 9v6"/>',
 "mail": '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/>',
 "chat": '<path d="M21 12a8 8 0 0 1-11.6 7.1L4 20l1-4.6A8 8 0 1 1 21 12z"/>',
 "code": '<path d="M8 6l-6 6 6 6M16 6l6 6-6 6"/>',
 "user": '<circle cx="12" cy="8" r="4"/><path d="M4 21a8 8 0 0 1 16 0"/>',
 "cube": '<path d="M12 2l9 5v10l-9 5-9-5V7z"/><path d="M12 22V12M21 7l-9 5-9-5"/>',
 "pin": '<path d="M12 22s7-7 7-12a7 7 0 0 0-14 0c0 5 7 12 7 12z"/><circle cx="12" cy="10" r="2.5"/>',
}
def ico(k, cls="ico"):
    return f'<svg class="{cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICON[k]}</svg>'

def bighead(n, icon, hid, title, sub):
    num = f'<span class="num" aria-hidden="true">{n}</span>' if n else ""
    return f'<header class="bighead">{num}{ico(icon)}<div><h2 id="{hid}">{title}</h2><p>{sub}</p></div></header>'

T = {
"fr": dict(
  file="index.html", guide_aria="Sur cette page", cv_pdf="/cv/Deo_Gratias_Loutou_CV_FR.pdf",
  guide=[("doc", "Mon CV", "1 page, à lire ou télécharger", "#cv", "data-cv"),
         ("chart", "Mes projets", "4 projets data, avec leurs résultats", "#projets", ""),
         ("case", "Mon expérience", "2 stages en entreprise", "#experience", ""),
         ("cap", "Ma formation", "Master informatique à Mulhouse", "#formation", ""),
         ("mail", "Me contacter", "E-mail, LinkedIn, GitHub", "#contact", ""),
         ("chat", "Une question ?", "Un assistant répond à partir du site", "#", "data-ask")],
  h_proj=("Mes projets data", "Quatre projets, chacun avec son résultat. Cliquez sur une image pour lire le résumé."),
  h_exp=("Mon expérience", "Deux stages en entreprise."),
  exp=[("Stagiaire développeur web et analyste", "PetitAvis", "Feucherolles (Yvelines)", "juin – août 2026",
        ["ConfoPE, une plateforme de conformité pour les crèches et structures d'accueil de la petite enfance, déjà en production.",
         "Création du premier tableau de bord comparant les établissements.",
         "Restructuration d'une base de données de plus de 50 tables (48 migrations), sans perte de données."]),
       ("Stagiaire technicien informatique et réseaux", "JASPE Technologies", "Bénin", "2024 – 2025",
        ["Mise en place de la supervision du réseau et des serveurs (Nagios, Icinga) sous Linux.",
         "Configuration de routeurs MikroTik."])],
  h_edu=("Ma formation", "Un master d'informatique en cours, après une licence."),
  edu=[("Master Informatique (M1)", "Université de Haute-Alsace, Mulhouse", "depuis 2026", "Parcours Informatique et Mobilité"),
       ("Licence Informatique (L3)", "Université de Haute-Alsace, Mulhouse", "2025 – 2026", ""),
       ("Études en sécurité informatique (L1 – L3)", "IFRI, Université d'Abomey-Calavi, Bénin", "2022 – 2025", ""),
       ("Baccalauréat scientifique, mention Très bien", "Collège Sainte-Thérèse, Bénin", "2022", "")],
  h_sk=("Mes compétences", "Les outils que j'utilise, regroupés par domaine."),
  sk=[("chart", "Données", ["Python", "pandas", "NumPy", "scikit-learn", "statsmodels", "Matplotlib", "SQL", "DuckDB", "MySQL", "PostgreSQL", "statistiques", "visualisation"]),
      ("chat", "IA", ["RAG", "recherche hybride", "reclassement", "llama.cpp", "évaluation de modèles"]),
      ("code", "Développement", ["C++", "C#", "TypeScript", "Java", "Qt", "Unity", "three.js", "Git", "tests automatisés"]),
      ("cap", "Certificats", ["DataCamp Python Data Fundamentals (28 h)", "GitHub Foundations (9 h)", "MikroTik MTCNA"]),
      ("user", "Langues", ["Français (langue maternelle)", "Anglais (B2)"])],
  h_about=("Qui je suis", "En quelques lignes."),
  h_contact=("Me contacter", "Je réponds vite. Le plus simple : un e-mail."),
  c_mail="M'écrire un e-mail", c_copy="Copier l'adresse", c_cv="Mon CV (PDF)", c_li="LinkedIn", c_gh="GitHub (mon code)",
  h_more=("Pour aller plus loin", "Le détail de chaque projet, et tous mes autres projets."),
  h_bonus="Bonus : ",
),
"en": dict(
  file="classic.html", guide_aria="On this page", cv_pdf="/cv/Deo_Gratias_Loutou_CV.pdf",
  guide=[("doc", "My CV", "1 page, to read or download", "#cv", "data-cv"),
         ("chart", "My projects", "4 data projects, with their results", "#projets", ""),
         ("case", "My experience", "2 company internships", "#experience", ""),
         ("cap", "My education", "Master's in computer science, Mulhouse", "#formation", ""),
         ("mail", "Contact me", "Email, LinkedIn, GitHub", "#contact", ""),
         ("chat", "A question?", "An assistant answers from this site", "#", "data-ask")],
  h_proj=("My data projects", "Four projects, each with its result. Click an image to read the summary."),
  h_exp=("My experience", "Two company internships."),
  exp=[("Web developer and analyst intern", "PetitAvis", "Feucherolles, France", "Jun – Aug 2026",
        ["ConfoPE, a compliance platform for childcare facilities, already in production.",
         "Built the first dashboard comparing facilities.",
         "Restructured a database of more than 50 tables (48 migrations) without losing data."]),
       ("IT and network technician intern", "JASPE Technologies", "Benin", "2024 – 2025",
        ["Set up network and server monitoring (Nagios, Icinga) on Linux.",
         "Configured MikroTik routers."])],
  h_edu=("My education", "A master's in computer science in progress, after a bachelor's."),
  edu=[("Master's in Computer Science (M1)", "Université de Haute-Alsace, Mulhouse", "2026 – present", "Computing & Mobility track"),
       ("Bachelor's in Computer Science (L3)", "Université de Haute-Alsace, Mulhouse", "2025 – 2026", ""),
       ("Information security studies (L1 – L3)", "IFRI, University of Abomey-Calavi, Benin", "2022 – 2025", ""),
       ("Scientific baccalaureate, highest honours", "Collège Sainte-Thérèse, Benin", "2022", "")],
  h_sk=("My skills", "The tools I use, grouped by area."),
  sk=[("chart", "Data", ["Python", "pandas", "NumPy", "scikit-learn", "statsmodels", "Matplotlib", "SQL", "DuckDB", "MySQL", "PostgreSQL", "statistics", "visualisation"]),
      ("chat", "AI", ["RAG", "hybrid search", "reranking", "llama.cpp", "model evaluation"]),
      ("code", "Engineering", ["C++", "C#", "TypeScript", "Java", "Qt", "Unity", "three.js", "Git", "automated tests"]),
      ("cap", "Certificates", ["DataCamp Python Data Fundamentals (28 h)", "GitHub Foundations (9 h)", "MikroTik MTCNA"]),
      ("user", "Languages", ["French (native)", "English (B2)"])],
  h_about=("Who I am", "In a few lines."),
  h_contact=("Contact me", "I reply quickly. The simplest is an email."),
  c_mail="Send me an email", c_copy="Copy the address", c_cv="My CV (PDF)", c_li="LinkedIn", c_gh="GitHub (my code)",
  h_more=("To go further", "The details of each project, and all my other projects."),
  h_bonus="Bonus: ",
)}

CSS = """
/* signposting: guide tiles and numbered sections */
.guide{list-style:none;margin:30px 0 0;padding:0;display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:12px}
.guide a,.guide button{display:flex;flex-direction:column;gap:6px;height:100%;width:100%;text-align:left;padding:16px 16px 14px;border:1.5px solid var(--ink);border-radius:4px;background:var(--sheet);color:var(--ink);text-decoration:none;font:inherit;cursor:pointer;transition:transform .15s,box-shadow .15s,border-color .15s}
.guide a:hover,.guide button:hover{transform:translateY(-3px);box-shadow:0 10px 22px rgba(0,0,0,.12);border-color:var(--accent)}
.guide .ico{width:38px;height:38px;color:var(--accent-ink)}
.guide b{font-family:var(--font-display);font-weight:800;font-size:1.45rem;line-height:1;text-transform:uppercase}
.guide span{font-size:.88rem;color:var(--muted)}
.bighead{display:grid;grid-template-columns:auto auto minmax(0,1fr);gap:14px 18px;align-items:center;margin:72px 0 24px;padding-bottom:14px;border-bottom:3px solid var(--ink)}
.bighead .num{width:56px;height:56px;border-radius:50%;background:var(--accent);color:var(--on-accent);display:grid;place-items:center;font:800 1.9rem/1 var(--font-display)}
.bighead .ico{width:46px;height:46px;color:var(--ink)}
.bighead h2{font-family:var(--font-display);font-weight:800;font-size:clamp(2.1rem,1.5rem + 2.6vw,3.4rem);line-height:1;text-transform:uppercase;margin:0}
.bighead p{margin:6px 0 0;color:var(--muted);font-size:1.05rem}
.intro .bighead{margin-top:56px}
@media (max-width:600px){.bighead{grid-template-columns:auto minmax(0,1fr)}.bighead .ico{display:none}.bighead .num{width:44px;height:44px;font-size:1.5rem}}
.xp{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:16px}
.xp li{border:1.5px solid var(--ink);border-radius:4px;background:var(--sheet);padding:20px 22px;margin:0}
.xp .when{font-family:var(--font-mono);font-size:.8rem;color:var(--accent-ink);margin:0 0 6px}
.xp h3{font-family:var(--font-display);font-weight:800;font-size:1.6rem;line-height:1.05;text-transform:uppercase;margin:0 0 4px}
.xp .org{display:flex;align-items:center;gap:8px;font-weight:600;margin:0 0 10px}
.xp .org .ico{width:20px;height:20px;color:var(--muted)}
.xp ul{margin:0;padding-left:1.1em}
.xp ul li{border:0;background:none;padding:0;margin:0 0 6px}
.edu{list-style:none;margin:0;padding:0;display:grid;gap:10px}
.edu li{display:grid;grid-template-columns:auto minmax(0,1fr) auto;gap:6px 16px;align-items:center;border:1px solid var(--line);border-left:5px solid var(--accent);border-radius:4px;background:var(--sheet);padding:14px 18px;margin:0}
.edu .ico{width:30px;height:30px;color:var(--accent-ink)}
.edu b{font-size:1.1rem}
.edu small{display:block;color:var(--muted);font-size:.9rem}
.edu .when{font-family:var(--font-mono);font-size:.82rem;color:var(--muted);white-space:nowrap}
@media (max-width:600px){.edu li{grid-template-columns:auto minmax(0,1fr)}.edu .when{grid-column:2}}
.skills{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:14px}
.skills > div{border:1px solid var(--line);border-radius:4px;background:var(--sheet);padding:16px 18px}
.skills h3{display:flex;align-items:center;gap:10px;font-family:var(--font-display);font-weight:800;font-size:1.35rem;text-transform:uppercase;margin:0 0 10px}
.skills h3 .ico{width:26px;height:26px;color:var(--accent-ink)}
.skills ul{list-style:none;margin:0;padding:0;display:flex;flex-wrap:wrap;gap:6px}
.skills ul li{margin:0;padding:4px 10px;border:1px solid var(--line);border-radius:999px;background:var(--paper);font-size:.88rem}
.who p{max-width:70ch;font-size:1.05rem}
.contact-big{display:flex;flex-wrap:wrap;gap:12px;align-items:center}
.contact-big .btn{min-height:56px;font-size:.92rem;padding:12px 20px;gap:10px}
.contact-big .btn .ico{width:22px;height:22px}
.contact-mail{font:600 1.25rem var(--font-mono);margin:18px 0 0;word-break:break-all}
.more-head{margin-top:72px}
"""

def tiles(t):
    out = []
    for icon, title, desc, href, attr in t["guide"]:
        inner = f'{ico(icon)}<b>{title}</b><span>{desc}</span>'
        if attr == "data-ask":
            out.append(f'<li><button type="button" data-ask>{inner}</button></li>')
        else:
            a = f' {attr}' if attr else ""
            out.append(f'<li><a href="{href}"{a}>{inner}</a></li>')
    return f'<ul class="guide" aria-label="{t["guide_aria"]}">\n      ' + "\n      ".join(out) + "\n    </ul>"

def section(id_, head, body):
    return f'<section class="section" id="{id_}">\n  <div class="wrap">\n    {head}\n    {body}\n  </div>\n</section>\n'

def build(lang):
    t = T[lang]; p = ROOT / t["file"]; s = p.read_text(encoding="utf-8")
    if "<!--signpost-->" in s:
        print("already done:", p); return
    # 1. guide tiles + numbered head for the featured projects (inside the intro)
    s = re.sub(r'\s*<h2 class="sr">[^<]*</h2>\n    <ol class="featured">',
               "\n    <!--signpost-->" + tiles(t) + "\n    <div id=\"projets\">" + bighead(1, "chart", "proj-title", *t["h_proj"]) + "</div>\n    <ol class=\"featured\">", s, count=1)
    # 2. pull out the about block (texts reused) and the 3D district, then rebuild the order
    about = re.search(r'<section class="section" id="about".*?</section>\n', s, re.S)
    paras = re.findall(r'<p>(.*?)</p>', re.search(r'<div class="about">\s*<div>(.*?)</div>', about.group(0), re.S).group(1), re.S)
    s = s[:about.start()] + s[about.end():]
    nb = re.search(r'<section class="section" id="notebook".*?</section>\n', s, re.S)
    city = re.search(r'<section class="hero" id="city-section".*?</section>\n', s, re.S)
    nb_html, city_html = nb.group(0), city.group(0)
    s = s[:nb.start()] + "<!--signpost:body-->" + s[nb.end():]
    s = s.replace(city_html, "")
    # experience
    exp = "".join(f'<li><p class="when">{w}</p><h3>{r}</h3><p class="org">{ico("case")}{o} · {c}</p><ul>' + "".join(f"<li>{b}</li>" for b in bs) + "</ul></li>" for r, o, c, w, bs in t["exp"])
    edu = "".join(f'<li>{ico("cap")}<div><b>{d}</b><small>{o}{(" · " + x) if x else ""}</small></div><span class="when">{w}</span></li>' for d, o, w, x in t["edu"])
    sk = "".join(f'<div><h3>{ico(i)}{h}</h3><ul>' + "".join(f"<li>{x}</li>" for x in xs) + "</ul></div>" for i, h, xs in t["sk"])
    who = "".join(f"<p>{x.strip()}</p>" for x in paras)
    mail = "loutoudeogratias@gmail.com"
    contact = (f'<div class="contact-big"><a class="btn primary" href="mailto:{mail}">{ico("mail")}{t["c_mail"]}</a>'
               f'<a class="btn" href="#cv" data-cv>{ico("doc")}{t["c_cv"]}</a>'
               f'<a class="btn" href="https://www.linkedin.com/in/deo-gratias-loutou-545263278" target="_blank" rel="noopener">{ico("user")}{t["c_li"]} ↗</a>'
               f'<a class="btn" href="https://github.com/LDGKM" target="_blank" rel="noopener">{ico("code")}{t["c_gh"]} ↗</a></div>'
               f'<p class="contact-mail copyline"><code id="mail">{mail}</code> <button type="button" class="btn" id="copyMail">{t["c_copy"]}</button><span class="hint" id="copyMsg" aria-live="polite"></span></p>')
    body = (section("experience", bighead(2, "case", "exp-title", *t["h_exp"]), f'<ul class="xp">{exp}</ul>')
          + section("formation", bighead(3, "cap", "edu-title", *t["h_edu"]), f'<ul class="edu">{edu}</ul>')
          + section("competences", bighead(4, "code", "sk-title", *t["h_sk"]), f'<div class="skills">{sk}</div>')
          + section("about", bighead(5, "user", "about-title", *t["h_about"]), f'<div class="who">{who}</div>')
          + section("contact", bighead(6, "mail", "contact-title", *t["h_contact"]), contact))
    # "to go further": detailed list (head replaced) + the 3D district as a bonus
    nb_html = re.sub(r'<div class="section-head">\s*<h2 id="nb-title">[^<]*</h2>\s*<p>(.*?)</p>\s*</div>',
                     lambda m: '<div class="more-head">' + bighead(None, "doc", "nb-title", t["h_more"][0], t["h_more"][1] + " " + m.group(1)) + "</div>", nb_html, count=1, flags=re.S)
    city_html = city_html.replace('<h2 id="hero-title">', '<h2 id="hero-title">' + t["h_bonus"], 1)
    s = s.replace("<!--signpost:body-->", body + nb_html + city_html, 1)
    s = s.replace("</style>", CSS + "</style>", 1)
    p.write_text(s, encoding="utf-8"); print("signposted:", p)

for lang in T: build(lang)
