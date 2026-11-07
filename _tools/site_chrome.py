"""Shared header, footer and head links for the non-3D pages.

    python3 _tools/site_chrome.py .

Re-runnable: the generated blocks sit between <!--site:...--> markers.
"""
import pathlib, re, sys

SITE = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else ".")

L = {
 "fr": dict(skip="Aller au contenu", menu="Menu", nav_aria="Menu principal", story="Récit 3D", projects="Projets",
            studies="Études", about="À propos", contact="Contact", cv_pdf="/cv/Deo_Gratias_Loutou_CV_FR.pdf",
            home="/classic-fr.html", other_label="English", other_lang="en",
            seek="Alternance data ou R&amp;D 2027-2028, ou stage dès mai 2027 · Mulhouse",
            privacy="Sans cookies ; mesure d'audience anonyme (GoatCounter).", links_aria="Me joindre", ask="Une question ?", ask_aria="Poser une question sur mon parcours"),
 "en": dict(skip="Skip to content", menu="Menu", nav_aria="Main menu", story="3D story", projects="Projects",
            studies=None, about="About", contact="Contact", cv_pdf="/cv/Deo_Gratias_Loutou_CV.pdf",
            home="/classic.html", other_label="Français", other_lang="fr",
            seek="Data or R&amp;D work-study 2027-2028, or an internship from May 2027 · Mulhouse, France",
            privacy="No cookies; anonymous visit counts (GoatCounter).", links_aria="Get in touch", ask="Ask", ask_aria="Ask a question about my background"),
}

PAGES = {
 "classic-fr.html": dict(lang="fr", current="projects", other="/classic.html", cv_dialog=True,
                         note="Données cartographiques © IGN, Licence Ouverte 2.0 · 3D avec three.js."),
 "classic.html":    dict(lang="en", current="projects", other="/classic-fr.html", cv_dialog=True,
                         note="Map data © IGN, Licence Ouverte 2.0 · 3D with three.js."),
 "etudes/index.html":             dict(lang="fr", current="studies", other="/classic.html", note=""),
 "etudes/bloc-operatoire.html":   dict(lang="fr", current="studies", other="/classic.html", crumb="Plannings de bloc opératoire",
                                       note="Données : VitalDB (CC BY 4.0). Les graphiques fixes sont ceux du rapport, avec leurs légendes en anglais."),
 "etudes/accidents-route.html":   dict(lang="fr", current="studies", other="/classic.html", crumb="Accidents de la route",
                                       note="Données : ONISR, fichier BAAC (Licence Ouverte 2.0). Les graphiques fixes sont ceux du rapport, avec leurs légendes en anglais."),
 "etudes/medicaments.html":       dict(lang="fr", current="studies", other="/classic.html", crumb="Médicaments remboursés",
                                       note="Données : Assurance maladie, Open Medic. Les graphiques fixes sont ceux du rapport, avec leurs légendes en anglais."),
 "etudes/vigie.html":            dict(lang="fr", current="studies", other="/classic.html", crumb="Vigie",
                                       note="Résultats tirés du dépôt LDGKM/Vigie et de la relecture manuelle des réponses."),
 "404.html":                      dict(lang="fr", current=None, other="/classic.html", note=""),
}

THEME_EARLY = '<script>try{var t=localStorage.getItem("site-theme");if(t)document.documentElement.dataset.theme=t}catch(e){}</script>'

def header(p):
    t = L[p["lang"]]
    items = [("story", "/" if p["lang"] == "fr" else "/en/", t["story"]),
             ("projects", t["home"] + "#notebook", t["projects"])]
    if t["studies"]: items.append(("studies", "/etudes/", t["studies"]))
    items += [("about", t["home"] + "#about", t["about"]), ("contact", t["home"] + "#contact", t["contact"])]
    links = "\n".join(f'      <a href="{u}"{" aria-current=\"page\"" if k == p.get("current") else ""}>{lbl}</a>' for k, u, lbl in items)
    cv = (f'      <a class="site-cv" href="{t["cv_pdf"]}" data-cv>CV</a>' if p.get("cv_dialog")
          else f'      <a class="site-cv" href="{t["cv_pdf"]}">CV</a>')
    return f"""<!--site:header-->
<a class="skip" href="#main">{t["skip"]}</a>
<header class="site-top">
  <div class="site-wrap">
    <a class="site-brand" href="{t["home"]}">Deo Gratias Loutou</a>
    <button class="site-menu" type="button" aria-expanded="false" aria-controls="site-nav">{t["menu"]} ☰</button>
    <nav class="site-nav" id="site-nav" aria-label="{t["nav_aria"]}">
{links}
      <button class="site-ask" type="button" data-ask aria-label="{t["ask_aria"]}" aria-haspopup="dialog"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M21 12a8 8 0 0 1-11.6 7.1L4 20l1-4.6A8 8 0 1 1 21 12z"/></svg>{t["ask"]}</button>
{cv}
      <a href="{p["other"]}" lang="{t["other_lang"]}" hreflang="{t["other_lang"]}" data-setlang="{t["other_lang"]}">{t["other_label"]}</a>
      <button class="site-theme" type="button" aria-pressed="false"></button>
    </nav>
  </div>
</header>
<!--/site:header-->"""

def footer(p):
    t = L[p["lang"]]
    note = (p["note"] + " " if p.get("note") else "") + t["privacy"]
    return f"""<!--site:footer-->
<footer class="site-foot">
  <div class="site-wrap">
    <div><strong>Deo Gratias Loutou</strong><br>{t["seek"]}</div>
    <nav aria-label="{t["links_aria"]}">
      <a href="mailto:loutoudeogratias@gmail.com">loutoudeogratias@gmail.com</a>
      <a href="https://www.linkedin.com/in/deo-gratias-loutou-545263278">LinkedIn</a>
      <a href="https://github.com/LDGKM">GitHub</a>
      <a href="{t["cv_pdf"]}">CV (PDF)</a>
    </nav>
    <p class="note">© 2026 Deo Gratias Loutou · {note}</p>
  </div>
</footer>
<!--/site:footer-->"""

def apply(path, p):
    s = path.read_text(encoding="utf-8")
    # head: early theme + shared stylesheet (once)
    if "/assets/site.css" not in s:
        s = s.replace('<meta name="viewport"', THEME_EARLY + '\n<meta name="viewport"', 1)
        s = re.sub(r'(<style>|<link rel="stylesheet" href="etudes.css">)', '<link rel="stylesheet" href="/assets/site.css">\n\\1', s, count=1)
    # header
    if "<!--site:header-->" in s:
        s = re.sub(r"<!--site:header-->.*?<!--/site:header-->", lambda m: header(p), s, flags=re.S)
    else:
        s, n = re.subn(r'<header class="top">.*?</header>', lambda m: header(p), s, count=1, flags=re.S)
        assert n == 1, path
    # footer
    if "<!--site:footer-->" in s:
        s = re.sub(r"<!--site:footer-->.*?<!--/site:footer-->", lambda m: footer(p), s, flags=re.S)
    else:
        s, n = re.subn(r"<footer\b.*?</footer>", lambda m: footer(p), s, count=1, flags=re.S)
        assert n == 1, path
    # main landmark + breadcrumbs
    s = re.sub(r"<main(?![^>]*\bid=)([^>]*)>", r'<main id="main"\1>', s, count=1)
    if p.get("crumb") and 'class="crumbs"' not in s:
        s = s.replace('<main id="main" class="wrap">', f'<main id="main" class="wrap">\n  <nav class="crumbs" aria-label="Fil d\'Ariane"><a href="/classic-fr.html">Accueil</a> › <a href="/etudes/">Études</a> › <span aria-current="page">{p["crumb"]}</span></nav>', 1)
    if "/assets/site.js" not in s:
        s = s.replace("</body>", '<script src="/assets/site.js" defer></script>\n</body>', 1)
    path.write_text(s, encoding="utf-8")
    print("chrome:", path)

for rel, p in PAGES.items():
    apply(SITE / rel, p)
