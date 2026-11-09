"""Build the scroll-driven 3D story: /recit/index.html (fr) and /en/index.html (en).

    python3 build_story.py /home/claude/ldgkm.github.io
"""
import json, pathlib, sys

SITE = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else ".")
TPL = (pathlib.Path(__file__).parent / "story_template.html").read_text(encoding="utf-8")

T = {
"fr": dict(
  langredirect='',
  lang="fr", locale="fr_FR", url="https://deogratias-loutou.fr/recit/", other_url="/en/", other_label="English", other_lang="en",
  title="Deo Gratias Loutou · alternance data &amp; R&amp;D 2027 · Mulhouse en données",
  desc="Deo Gratias Loutou, étudiant en M1 informatique à Mulhouse, cherche une alternance data ou R&amp;D pour 2027-2028. Son portfolio, raconté en 3D avec de vraies données publiques.",
  og="og-classic-fr.jpg", classic="/", cv="/cv/Deo_Gratias_Loutou_CV_FR.pdf",
  skip="Aller au récit", nav_projects="Projets", nav_studies="Études", nav_studies_url="/etudes/", nav_contact="Contact", nav_text="Version texte",
  ch=["Qui je suis","La ville","Les accidents","Les décès","Le piège","Le bloc","L'incertitude","Contact"],
  watch_k="Vous regardez", watch=["Le centre de Mulhouse en 3D, reconstruit à partir de données publiques.", "Le centre de Mulhouse : chaque bâtiment, coloré selon son année de construction.", "Le Haut-Rhin vu du ciel : chaque point bleu est un accident de la route avec blessé (2019-2024).", "Les mêmes accidents : en rouge, ceux où quelqu'un est mort.", "Deux cercles de 3 km, autour de Mulhouse et de Colmar, pour comparer leurs accidents.", "Une journée dans 4 salles d'opération : contour = prévu, bloc plein = réel, rouge = retard.", "La même journée, planifiée avec l'incertitude apprise : le rouge a presque disparu.", "Fin du récit."],
  ch_aria="Chapitres", menu_aria="Menu principal",
  load="Chargement de la carte…", nogl="La 3D n'est pas disponible sur cet appareil : le récit reste lisible.", nodata="Les données n'ont pas pu se charger : le récit reste lisible.",
  standing="bâtiments debout", acc_inj="accident corporel", acc_fat="accident mortel", acc_unit="accidents",
  eras=["avant 1790","1790–1870","1871–1918","1919–1975","après 1975"], era_unknown="date inconnue",
  lab_mul="Mulhouse", lab_col="Colmar", lab_mul_trap="Mulhouse · <b>115</b> accidents · 14 mortels", lab_col_trap="Colmar · <b>157</b> accidents · 12 mortels",
  room="Salle", eight="8 h : fin de journée",
  bloc_plan="planning", bloc_real="durée réelle", bloc_over="dépassement",
  bloc_statA="Planning sur l'historique · ce jour-là : <b>111 min</b> de dépassement par salle, 3 salles sur 4 en retard",
  bloc_statB="Planning sur l'incertitude apprise · ce jour-là : <b>18 min</b> de dépassement par salle, 1 salle sur 4 en retard",
  numfmt="fr-FR",
  s0_kick="Mulhouse en données · un portfolio en 2 minutes",
  s0_who="Étudiant en M1 informatique à l'Université de Haute-Alsace, à Mulhouse.",
  s0_seek="Je cherche une alternance en data ou en R&amp;D pour 2027-2028, ou un stage à partir de mai 2027 qui pourrait y mener.",
  s0_intro="Faites défiler : la carte 3D affiche, écran par écran, une de mes analyses sur de vraies données de Mulhouse et du Haut-Rhin. Ce qu'elles montrent :",
  s0_skills=["construire un modèle à partir de données ouvertes ;","nettoyer, vérifier et comparer équitablement ;","repérer un biais avant de conclure ;","quantifier l'incertitude pour mieux décider."],
  scroll="Faites défiler ↓", shows="Ce que ça montre",
  proj1_n="Projet 1 / 2", proj1="Accidents de la route", proj2_n="Projet 2 / 2", proj2="Plannings du bloc opératoire",
  s1_kick="1 · La ville", s1_h="1 678 bâtiments et 533 arbres, reconstruits",
  s1_p="Le centre de Mulhouse, chaque bâtiment à son année de construction, d'après la base nationale de l'IGN. Les arbres n'y figurent pas : je les ai détectés moi-même sur des photos aériennes.",
  s1_s="Construire un modèle exploitable en croisant plusieurs sources publiques.",
  s2_kick="2 · Les accidents", s2_h="2 164 accidents, à leur vraie place",
  s2_p="Voici le Haut-Rhin. Chaque point est un accident avec au moins un blessé, enregistré par la police ou la gendarmerie de 2019 à 2024.",
  s2_s="Nettoyer et vérifier : 24 fichiers nationaux au format changeant, nettoyés en SQL ; mes nombres de tués pour la France sont identiques aux chiffres officiels.",
  s2_src="Source : fichier BAAC de l'ONISR, data.gouv.fr.",
  s3_kick="3 · Les décès", s3_h="156 accidents mortels",
  s3_p1="En rouge, les accidents où au moins une personne est morte dans les 30 jours.",
  s3_p2="Le Haut-Rhin compte <span class=\"big\">36</span> tués par million d'habitants et par an, contre <span class=\"big\">46</span> en France métropolitaine : 11<sup>e</sup> département le plus sûr sur 96.",
  s3_s="Comparer équitablement : des taux par habitant, pas des totaux bruts.",
  s4_kick="4 · Le piège", s4_h="Trop peu d'accidents à Mulhouse",
  s4_p1="À moins de 3 km du centre : <b>115</b> accidents autour de Mulhouse, <b>157</b> autour de Colmar, pourtant moins peuplée. Mais Mulhouse compte plus d'accidents mortels (14 contre 12).",
  s4_p2="Les accidents légers y sont très probablement sous-enregistrés : ici, seuls les décès sont un indicateur fiable.",
  s4_s="Repérer un biais : vérifier que les données mesurent bien ce qu'on croit avant de conclure.",
  s4_btn="Lire l'étude complète", s4_url="/etudes/accidents-route.html",
  s5_kick="5 · Le bloc opératoire", s5_h="Planifier sur l'historique : 3 salles sur 4 en retard",
  s5_p1="Une journée simulée à partir de vraies opérations (base ouverte VitalDB) : 4 salles de 8 heures. Les blocs transparents sont le planning, fait avec la durée habituelle de chaque intervention ; les blocs pleins, ce qui s'est vraiment passé. En rouge, le dépassement.",
  s5_p2="Ce jour-là : 111 minutes de dépassement en moyenne par salle. Sur 200 journées simulées : 113.",
  s6_kick="6 · L'incertitude", s6_h="Avec l'incertitude apprise : 18 minutes",
  s6_p1="Le même jour, chaque opération est planifiée avec la durée qu'elle a 80 % de chances de ne pas dépasser, apprise par un modèle (régression quantile conforme), puis placée par un solveur d'optimisation.",
  s6_p2="Ce jour-là : 18 minutes de dépassement par salle, en programmant 10 opérations au lieu de 12. Sur 200 journées : 19 minutes, avec 88,7 % d'occupation des salles.",
  s6_s="Quantifier l'incertitude et s'en servir pour optimiser une décision : c'est mon projet de recherche.",
  s6_btn="Lire l'étude", s6_url="/etudes/bloc-operatoire.html",
  s7_kick="Contact", s7_h="Me contacter",
  s7_seek="Alternance data ou R&amp;D pour 2027-2028, ou stage à partir de mai 2027.",
  s7_p="Code public et rapport pour chaque étude, dont une troisième sur <a href=\"/etudes/medicaments.html\">les médicaments remboursés en France</a>.",
  s7_cv="Mon CV (PDF)", s7_all="Tous les projets", s7_all_url="/#projets",
),
"en": dict(
  langredirect="",
  lang="en", locale="en_GB", url="https://deogratias-loutou.fr/en/", other_url="/recit/", other_label="Français", other_lang="fr",
  title="Deo Gratias Loutou · data &amp; R&amp;D work-study 2027 · Mulhouse in data",
  desc="Deo Gratias Loutou, a computer science master's student in Mulhouse, is looking for a data or R&amp;D work-study position for 2027-2028. His portfolio, told in 3D with real public data.",
  og="og-classic.jpg", classic="/classic.html", cv="/cv/Deo_Gratias_Loutou_CV.pdf",
  skip="Skip to the story", nav_projects="Projects", nav_studies="Reports", nav_studies_url="/classic.html#projets", nav_contact="Contact", nav_text="Text version",
  ch=["Who I am","The city","Accidents","Deaths","The trap","Surgery","Uncertainty","Contact"],
  watch_k="You are looking at", watch=["Central Mulhouse in 3D, rebuilt from public data.", "Central Mulhouse: every building, coloured by its construction year.", "The Haut-Rhin from above: each blue dot is a road accident with someone injured (2019-2024).", "The same accidents: in red, those in which someone died.", "Two 3 km circles, around Mulhouse and Colmar, to compare their accidents.", "One day in 4 operating rooms: outline = planned, solid block = actual, red = overtime.", "The same day, planned with learned uncertainty: the red has almost gone.", "End of the story."],
  ch_aria="Chapters", menu_aria="Main menu",
  load="Loading the map…", nogl="3D isn't available on this device: the story is still readable.", nodata="The data couldn't load: the story is still readable.",
  standing="buildings standing", acc_inj="injury accident", acc_fat="fatal accident", acc_unit="accidents",
  eras=["before 1790","1790–1870","1871–1918","1919–1975","after 1975"], era_unknown="date unknown",
  lab_mul="Mulhouse", lab_col="Colmar", lab_mul_trap="Mulhouse · <b>115</b> accidents · 14 fatal", lab_col_trap="Colmar · <b>157</b> accidents · 12 fatal",
  room="Room", eight="8 h: end of the day",
  bloc_plan="planned", bloc_real="actual duration", bloc_over="overtime",
  bloc_statA="Planned on history · that day: <b>111 min</b> of overtime per room, 3 rooms out of 4 late",
  bloc_statB="Planned on learned uncertainty · that day: <b>18 min</b> of overtime per room, 1 room out of 4 late",
  numfmt="en-GB",
  s0_kick="Mulhouse in data · a two-minute portfolio",
  s0_who="Computer science master's student (M1) at Université de Haute-Alsace, Mulhouse, France.",
  s0_seek="I'm looking for a work-study position (alternance) in data or R&amp;D for 2027-2028, or an internship from May 2027 that could lead to it.",
  s0_intro="Scroll down: the 3D map shows one of my analyses per screen, on real data from Mulhouse and the Haut-Rhin. What they show:",
  s0_skills=["build a model from open data;","clean, check and compare fairly;","spot a bias before concluding;","quantify uncertainty to make better decisions."],
  scroll="Scroll down ↓", shows="What this shows",
  proj1_n="Project 1 / 2", proj1="Road accidents", proj2_n="Project 2 / 2", proj2="Operating-room schedules",
  s1_kick="1 · The city", s1_h="1,678 buildings and 533 trees, rebuilt",
  s1_p="Central Mulhouse, each building in its construction year, from France's national map database (IGN). Trees aren't in it: I detected them myself in aerial photos.",
  s1_s="Building a usable model by combining several public sources.",
  s2_kick="2 · Accidents", s2_h="2,164 accidents, where they happened",
  s2_p="This is the Haut-Rhin department. Each dot is an accident with at least one person injured, recorded by the police from 2019 to 2024.",
  s2_s="Cleaning and checking: 24 national files whose format changes every year, cleaned in SQL; my death counts for France match the official figures exactly.",
  s2_src="Source: ONISR national accident file (BAAC), data.gouv.fr.",
  s3_kick="3 · Deaths", s3_h="156 fatal accidents",
  s3_p1="In red, accidents in which at least one person died within 30 days.",
  s3_p2="Haut-Rhin has <span class=\"big\">36</span> road deaths per million inhabitants a year, against <span class=\"big\">46</span> in mainland France: the 11th safest of 96 departments.",
  s3_s="Comparing fairly: rates per inhabitant, not raw totals.",
  s4_kick="4 · The trap", s4_h="Too few accidents in Mulhouse",
  s4_p1="Within 3 km of the centre: <b>115</b> accidents around Mulhouse, <b>157</b> around Colmar, a smaller town. Yet Mulhouse has more fatal accidents (14 against 12).",
  s4_p2="Minor accidents are very likely under-recorded there: in this area, only deaths are a reliable indicator.",
  s4_s="Spotting a bias: checking that the data measure what we think before drawing a conclusion.",
  s4_btn="Read the report (PDF)", s4_url="/rapports/accidents-route.pdf",
  s5_kick="5 · Operating rooms", s5_h="Planning on history: 3 rooms out of 4 run late",
  s5_p1="One simulated day built from real operations (open VitalDB dataset): 4 rooms of 8 hours. Transparent blocks are the plan, made with each procedure's usual duration; solid blocks are what really happened. In red, overtime.",
  s5_p2="That day: 111 minutes of overtime per room on average. Over 200 simulated days: 113.",
  s6_kick="6 · Uncertainty", s6_h="With learned uncertainty: 18 minutes",
  s6_p1="The same day, each operation is planned with the duration it has an 80% chance of not exceeding, learned by a model (conformalized quantile regression), then placed by an optimisation solver.",
  s6_p2="That day: 18 minutes of overtime per room, scheduling 10 operations instead of 12. Over 200 days: 19 minutes, with 88.7% of room time used.",
  s6_s="Quantifying uncertainty and using it to optimise a decision: this is my research project.",
  s6_btn="Read the paper (PDF)", s6_url="/rapports/plannings-bloc-operatoire.pdf",
  s7_kick="Contact", s7_h="Get in touch",
  s7_seek="Data or R&amp;D work-study position for 2027-2028, or an internship from May 2027.",
  s7_p="Public code and a written report for each study, including a third one on <a href=\"/rapports/medicaments.pdf\">medicines reimbursed in France</a>.",
  s7_cv="My CV (PDF)", s7_all="All projects", s7_all_url="/classic.html#projets",
),
}

def render(t):
    s = TPL
    t = dict(t)
    t["skills_li"] = "\n".join(f"        <li>{x}</li>" for x in t.pop("s0_skills"))
    t["chapters_li"] = "\n".join(f'    <li><a href="#c{i}">{c}</a></li>' for i, c in enumerate(t["ch"]))
    t["watch_js"] = json.dumps(t.pop("watch"), ensure_ascii=False)
    t["ch_js"] = "[" + ",".join('"' + c.replace('"', '\\"') + '"' for c in t.pop("ch")) + "]"
    eras = t.pop("eras")
    for i, e in enumerate(eras): t[f"era{i}"] = e
    if t["lang"] == "fr":   # French typography: no line break before ":" "?" "!"
        for k in list(t):
            if k.startswith(("s0_", "s1_", "s2_", "s3_", "s4_", "s5_", "s6_", "s7_", "bloc_stat")) and isinstance(t[k], str):
                t[k] = t[k].replace(" :", "&nbsp;:").replace(" ?", "&nbsp;?").replace(" !", "&nbsp;!")
    for k, v in t.items():
        s = s.replace("{{" + k + "}}", v)
    assert "{{" not in s, s[s.index("{{"):s.index("{{") + 40]
    return s

(SITE / "recit" / "index.html").write_text(render(T["fr"]), encoding="utf-8")
(SITE / "en").mkdir(exist_ok=True)
(SITE / "en" / "index.html").write_text(render(T["en"]), encoding="utf-8")
print("built fr + en")
