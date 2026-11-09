"""French pages for the three studies: etudes/*.html (+ etudes/etudes.css)."""
import html, pathlib
ROOT = pathlib.Path("/home/claude/ldgkm.github.io"); OUT = ROOT / "etudes"; OUT.mkdir(exist_ok=True)
B = "https://deogratias-loutou.fr/"
GC = '<script data-goatcounter="https://ldgkm.goatcounter.com/count" async src="https://gc.zgo.at/count.js"></script>'

CSS = r""":root{
  --paper:#EDF0EC;--sheet:#F7F8F5;--ink:#16202A;--muted:#58636C;--line:#C6CDC8;--accent:#D69E14;--accent-ink:#8A5F00;
  --font-display:"Big Shoulders Display","Arial Narrow",Impact,sans-serif;
  --font-body:"Public Sans",system-ui,-apple-system,"Segoe UI",sans-serif;
  --font-mono:"JetBrains Mono",ui-monospace,"SFMono-Regular",Consolas,monospace;
  --step--1:clamp(.8rem,.78rem + .1vw,.86rem);--step-0:clamp(.95rem,.92rem + .15vw,1.03rem);
  --step-1:clamp(1.15rem,1.08rem + .35vw,1.35rem);--step-2:clamp(1.5rem,1.3rem + .9vw,2.1rem);
  --step-3:clamp(2.2rem,1.7rem + 2.4vw,3.6rem);color-scheme:light}
@media (prefers-color-scheme:dark){:root{--paper:#0F151B;--sheet:#151D25;--ink:#E4E9E5;--muted:#93A0A8;--line:#26323C;--accent:#E3AE2A;--accent-ink:#E9B83C;color-scheme:dark}}
*{box-sizing:border-box}
body{background:var(--paper);color:var(--ink);font-family:var(--font-body);font-size:var(--step-0);line-height:1.65;margin:0}
a{color:var(--accent-ink);text-underline-offset:.18em}
:focus-visible{outline:2px solid var(--accent);outline-offset:3px;border-radius:2px}
h1,h2,h3{font-family:var(--font-display);font-weight:800;line-height:1.05;margin:0;text-wrap:balance}
.wrap{max-width:860px;margin-inline:auto;padding-inline:16px}
.top{position:sticky;top:0;z-index:5;background:color-mix(in srgb,var(--paper) 90%,transparent);backdrop-filter:blur(8px);border-bottom:1px solid var(--line)}
.top .wrap{max-width:1180px;display:flex;flex-wrap:wrap;gap:8px 20px;align-items:center;padding-block:10px}
.brand{font-family:var(--font-display);font-weight:800;font-size:1.35rem;text-transform:uppercase;color:var(--ink);text-decoration:none}
.top nav{margin-left:auto;display:flex;flex-wrap:wrap;gap:14px}
.top nav a{color:var(--ink);text-decoration:none;font-size:var(--step--1);font-weight:600;letter-spacing:.06em;text-transform:uppercase;padding-block:4px}
.top nav a:hover{color:var(--accent-ink)}
main{padding-block:40px 24px}
.kicker{font-family:var(--font-mono);font-size:var(--step--1);color:var(--muted);margin:0 0 12px}
h1{font-size:var(--step-3);text-transform:uppercase}
.lede{font-size:var(--step-1);margin:16px 0 0}
.stats{list-style:none;padding:0;margin:28px 0 8px;display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:12px}
.stats li{background:var(--sheet);border:1px solid var(--line);border-radius:2px;padding:14px 16px}
.stats b{display:block;font-family:var(--font-display);font-size:var(--step-2);line-height:1.1}
.stats span{color:var(--muted);font-size:var(--step--1)}
.links{display:flex;flex-wrap:wrap;gap:10px;margin:22px 0 0}
.btn{display:inline-flex;align-items:center;min-height:44px;padding:10px 16px;border:1.5px solid var(--ink);border-radius:2px;font-weight:600;font-size:var(--step--1);letter-spacing:.06em;text-transform:uppercase;text-decoration:none;color:var(--ink)}
.btn.primary{background:var(--ink);color:var(--paper)}
.btn:hover{border-color:var(--accent)}
section{margin-top:44px}
h2{font-size:var(--step-2);text-transform:uppercase;border-bottom:2px solid var(--ink);padding-bottom:8px;margin-bottom:14px}
h3{font-size:var(--step-1);text-transform:uppercase;margin:26px 0 6px}
p{margin:0 0 12px}
ul{margin:0 0 12px;padding-left:1.2em}
li{margin-bottom:6px}
figure{margin:20px 0}
figure img{display:block;width:100%;height:auto;background:#fff;border:1px solid var(--line);border-radius:2px}
figcaption{font-size:var(--step--1);color:var(--muted);margin-top:6px}
.note{font-size:var(--step--1);color:var(--muted)}
code{font-family:var(--font-mono);font-size:.9em;background:var(--sheet);border:1px solid var(--line);padding:1px 6px;border-radius:2px}
.pager{display:flex;flex-wrap:wrap;justify-content:space-between;gap:12px;margin-top:48px;padding-top:16px;border-top:1px solid var(--line)}
.pager a{font-weight:600;padding-block:8px}
footer{border-top:1px solid var(--line);color:var(--muted);font-size:var(--step--1)}
footer .wrap{padding-block:18px 26px}
"""

def page(slug, title, short, kicker, lede, stats, repo, body, prev, nxt, desc, og):
    nbslug = {"bloc-operatoire":"plannings-bloc-operatoire"}.get(slug, slug)
    st = "\n".join(f"    <li><b>{v}</b><span>{l}</span></li>" for v, l in stats)
    pv = f'<a href="{prev[0]}">← {prev[1]}</a>' if prev else "<span></span>"
    nx = f'<a href="{nxt[0]}">{nxt[1]} →</a>' if nxt else "<span></span>"
    return f"""<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{short} · Deo Gratias Loutou</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="{B}etudes/{slug}.html">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:url" content="{B}etudes/{slug}.html">
<meta property="og:type" content="article">
<meta property="og:locale" content="fr_FR">
<meta property="og:image" content="{B}img/etudes/{og}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="../favicon.svg" type="image/svg+xml">
<link rel="icon" href="../favicon.ico" sizes="any">
<link rel="apple-touch-icon" href="../apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Big+Shoulders+Display:wght@600;800&family=Public+Sans:ital,wght@0,400;0,600;1,400&family=JetBrains+Mono:wght@400;600&display=swap">
<link rel="stylesheet" href="etudes.css">
</head>
<body>
<header class="top">
  <div class="wrap">
    <a class="brand" href="../">Deo Gratias Loutou</a>
    <nav aria-label="Menu principal">
      <a href="../#notebook">Projets</a>
      <a href="./">Études</a>
      <a href="../#contact">Contact</a>
      <a href="../cv/Deo_Gratias_Loutou_CV_FR.pdf">CV (PDF)</a>
      <a href="../index.html">Version 3D</a>
    </nav>
  </div>
</header>
<main class="wrap">
  <p class="kicker">{kicker}</p>
  <h1>{title}</h1>
  <p class="lede">{lede}</p>
  <ul class="stats" aria-label="Chiffres clés">
{st}
  </ul>
  <div class="links">
    <a class="btn primary" href="https://github.com/LDGKM/{repo}">Code ↗</a>
    <a class="btn" href="https://deogratias-loutou.fr/notebooks/{nbslug}.html">Notebook ↗</a>
    <a class="btn" href="https://deogratias-loutou.fr/rapports/{nbslug}.pdf">Rapport complet (PDF, en anglais) ↗</a>
  </div>
{body}
  <nav class="pager" aria-label="Autres études">{pv}{nx}</nav>
</main>
<footer><div class="wrap">© 2026 Deo Gratias Loutou · <a href="../">deogratias-loutou.fr</a> · Les graphiques sont ceux du rapport, avec leurs légendes en anglais.</div></footer>
{GC}
</body>
</html>
"""

def fig(src, alt, cap):
    return f'<figure><img src="../img/etudes/{src}" alt="{html.escape(alt)}" loading="lazy"><figcaption>{cap}</figcaption></figure>'

BLOC = f"""
  <section>
    <h2>La question</h2>
    <p>Les plannings de bloc opératoire reposent sur des durées prévues. Pourtant, l'incertitude autour de ces prévisions est le plus souvent ignorée, ou remplacée par une marge identique pour toutes les opérations. L'étude pose deux questions :</p>
    <ul>
      <li>Peut-on apprendre cette incertitude à partir des informations connues avant l'opération, et un intervalle annoncé « à 80 % » contient-il vraiment 80 % des cas, globalement et dans chaque contexte chirurgical ?</li>
      <li>Utiliser cette incertitude apprise dans un modèle de planification donne-t-il de meilleurs plannings que les pratiques habituelles (moyennes historiques, marges fixes) ?</li>
    </ul>
  </section>
  <section>
    <h2>Les données</h2>
    <p><a href="https://vitaldb.net">VitalDB</a> (Lee et al., <i>Scientific Data</i>, 2022, licence CC BY 4.0) : 6 388 opérations non cardiaques réalisées à l'hôpital universitaire national de Séoul. La variable à prédire est le temps passé en salle, de l'entrée à la sortie du patient : c'est ce qu'un planning doit réserver. Après retrait de trois cas de plus de 16 heures, il reste 6 385 opérations pour 6 089 patients (médiane 165 min, moyenne 189 min).</p>
    <p>Seules les informations disponibles au moment de planifier sont utilisées : âge, classe ASA, examens préopératoires, service, intervention prévue, voie d'abord, etc. Les mesures prises pendant l'opération sont exclues pour ne pas « tricher ». Les données sont découpées par patient : 60 % pour l'apprentissage, 20 % pour la calibration, 20 % pour le test.</p>
  </section>
  <section>
    <h2>La méthode</h2>
    <h3>Prédire une durée</h3>
    <p>Trois prédictions de la durée médiane sont comparées : la médiane globale, l'historique de la même intervention (la pratique courante), et un modèle de gradient boosting (scikit-learn).</p>
    <h3>Construire des intervalles à 80 %</h3>
    <p>Cinq méthodes : les percentiles historiques de l'intervention, la régression quantile, la prédiction conforme, la <b>régression quantile conforme</b> (CQR, Romano et al., 2019) et une CQR calibrée séparément dans chaque service. Elles sont comparées par leur couverture, leur largeur et le score d'intervalle (Gneiting et Raftery, 2007), qui récompense les intervalles étroits et pénalise les cas qui en sortent. Toute l'évaluation est répétée sur 10 découpages aléatoires.</p>
    <h3>Planifier sous incertitude</h3>
    <p>200 journées simulées : 4 salles de 8 heures et une liste d'attente de 24 opérations programmées tirées du jeu de test. Un modèle exact en nombres entiers (<i>set packing</i>, résolu avec le solveur HiGHS) choisit quelles opérations mettre dans quelle salle. Chaque règle de planification produit son planning : médianes historiques, médiane prédite, marges fixes de 5 à 30 %, quantiles appris de 60 à 90 %, et modèle robuste « à budget » (Bertsimas et Sim, 2004). Chaque planning est ensuite <b>rejoué avec les vraies durées</b> pour mesurer les dépassements et l'occupation des salles.</p>
  </section>
  <section>
    <h2>Les résultats</h2>
    <h3>1. La prédiction seule ne suffit pas</h3>
    <p>Le gradient boosting réduit l'erreur moyenne de 50,7 à 45,6 minutes par rapport à l'historique de l'intervention (sur 10 découpages). Mais environ la moitié des opérations restent à plus de 30 minutes de leur prédiction : il faut un intervalle, pas seulement un chiffre.</p>
    <h3>2. Les intervalles habituels sont trop optimistes</h3>
    <p>Les percentiles historiques ne couvrent que 76,5 % des nouveaux cas, et la régression quantile brute 67,7 %, au lieu des 80 % annoncés. La CQR atteint 80,1 %, avec le meilleur score d'intervalle : elle bat l'historique sur 10 découpages sur 10.</p>
    {fig("bloc_01_intervals_examples.webp", "Quarante opérations du jeu de test avec leur prédiction, leur intervalle CQR et leur durée réelle", "Quarante opérations du jeu de test : prédiction médiane, intervalle CQR à 80 % et durée réelle.")}
    <h3>3. La couverture n'est pas la même partout</h3>
    <p>Derrière la moyenne, certains contextes sont mal couverts : 66 % en chirurgie robotique (68 cas), 60 % en urologie (30 cas). Calibrer par service fait passer le service le moins bien couvert de 74 % à 76 % en moyenne, mais ne corrige pas l'urologie, qui n'a qu'une vingtaine de cas de calibration.</p>
    {fig("bloc_02_coverage.webp", "Couverture des intervalles par service, voie d'abord et longueur prédite", "Couverture des intervalles à 80 % selon le service, la voie d'abord et la longueur prédite.")}
    <h3>4. De meilleurs plannings</h3>
    <p>Planifier sur les médianes historiques donne <b>113 minutes de dépassement par salle et par jour</b>, et 80 % des salles finissent en retard : les durées sont asymétriques, chaque opération dépasse sa médiane de 10,4 minutes en moyenne, et ces retards s'additionnent dans une salle.</p>
    <p>Planifier chaque opération à son <b>80<sup>e</sup> percentile appris</b> ramène les dépassements à <b>19 minutes</b>, avec 88,7 % d'occupation des salles : 2,1 points de plus qu'une marge uniforme de 15 % pour le même niveau de dépassement. La marge est mise là où est l'incertitude, au lieu de protéger autant les opérations courtes et prévisibles que les longues et incertaines.</p>
    {fig("bloc_03_schedule_frontier.webp", "Occupation des salles en fonction des dépassements pour chaque règle de planification", "Occupation des salles et dépassements pour chaque règle de planification, 200 journées simulées. En haut à gauche, c'est mieux.")}
    <h3>5. Un résultat négatif</h3>
    <p>Le modèle robuste à budget, construit sur les écarts appris, s'est montré trop prudent : à dépassement égal, il perd environ 10 points d'occupation face aux quantiles appris. Il protège chaque salle contre ses pires écarts survenant tous en même temps, ce qui arrive rarement.</p>
  </section>
  <section>
    <h2>Les limites</h2>
    <ul>
      <li>Un seul hôpital, coréen, et sans dates : les résultats peuvent ne pas se transposer, et le découpage aléatoire ignore les évolutions dans le temps.</li>
      <li>Pas de données de salle de réveil, pourtant déterminante en pratique.</li>
      <li>Plannings simplifiés : salles identiques, pas de contraintes de chirurgien ou d'équipement, pas d'urgences.</li>
      <li>Les garanties de la prédiction conforme sont valables en moyenne, pas dans chaque petit groupe.</li>
    </ul>
    <p class="note">Tout se relance avec <code>python run_all.py</code> (environ 10 minutes) et redonne les mêmes chiffres.</p>
  </section>
"""

ROUTE = f"""
  <section>
    <h2>La question</h2>
    <p>Quand, où et à qui arrivent les morts sur la route ? Comment le Haut-Rhin se situe-t-il par rapport au reste de la France ? Et quelles circonstances transforment un accident corporel en accident mortel ?</p>
  </section>
  <section>
    <h2>Les données</h2>
    <p>Le fichier national des accidents corporels (BAAC), publié par l'Observatoire national interministériel de la sécurité routière (ONISR) sur data.gouv.fr : un enregistrement par accident avec au moins un blessé constaté par la police ou la gendarmerie, en quatre tables par an (accidents, lieux, véhicules, usagers). L'étude couvre 2019 à 2024 en France métropolitaine (96 départements), avec les populations de l'Insee au 1<sup>er</sup> janvier 2023.</p>
  </section>
  <section>
    <h2>La méthode</h2>
    <p><b>Nettoyage en SQL (DuckDB).</b> Les 24 fichiers CSV changent de format d'une année à l'autre : identifiant renommé en 2022, valeurs manquantes codées « -1 », « (1) » ou « N/A », virgules décimales, départements écrits « 1 » au lieu de « 01 ». Une seule macro SQL convertit chaque champ codé en entier ou en valeur manquante. Les quelque 40 catégories de véhicules sont regroupées en 11 modes de déplacement, plus les piétons.</p>
    <p><b>Validation.</b> Mes nombres de tués correspondent exactement aux chiffres officiels de l'ONISR pour 2019 à 2023 (3 244 ; 2 541 ; 2 944 ; 3 267 ; 3 167) : le nettoyage ne perd aucun accident.</p>
    <p><b>Modèle.</b> Une régression logistique (statsmodels) sur 301 290 accidents, avec un effet par année, testée sur 25 % des données mises de côté.</p>
  </section>
  <section>
    <h2>Les résultats</h2>
    <h3>Un plateau depuis 2019</h3>
    <p>Environ 3 000 morts par an, sans amélioration depuis 2019. Après les confinements de 2020, les accidents enregistrés se sont stabilisés environ 9 % sous leur niveau de 2019, tandis que les décès y sont revenus (3 193 en 2024).</p>
    {fig("route_01_trend.webp", "Évolution des accidents et des tués de 2019 à 2024", "Accidents corporels et tués par an, France métropolitaine et Haut-Rhin.")}
    <h3>Quand : la nuit tue davantage</h3>
    <p>Le créneau le plus chargé est le vendredi entre 17 h et 18 h. Mais entre 3 h et 6 h du matin, 11 % des accidents sont mortels, deux fois plus qu'en journée. La nuit représente 26 % des accidents et 35 % des tués.</p>
    {fig("route_02_when.webp", "Accidents par heure et par jour, et part d'accidents mortels selon l'heure", "Accidents selon l'heure et le jour, et part d'accidents mortels selon l'heure.")}
    <h3>Qui et où</h3>
    <ul>
      <li>78 % des tués sont des hommes ; le taux de mortalité culmine entre 20 et 24 ans, puis remonte après 80 ans.</li>
      <li>Les morts en trottinette électrique sont passés de 11 à 47 par an, les blessés de 677 à 2 746.</li>
      <li>Hors agglomération : 36 % des accidents, mais <b>68 % des tués</b>.</li>
    </ul>
    <h3>Le Haut-Rhin, et un piège dans les données</h3>
    <p>Avec 36 tués par million d'habitants et par an contre 46 au niveau national, le Haut-Rhin est le 11<sup>e</sup> département le plus sûr sur 96.</p>
    {fig("route_06_haut_rhin_map.webp", "Carte des accidents corporels du Haut-Rhin, les accidents mortels en rouge", "Tous les accidents corporels du Haut-Rhin, 2019-2024 ; en rouge, les accidents mortels.")}
    <p>Mais Mulhouse enregistre moins d'accidents que Colmar, ville plus petite (17 par an contre 28), et quinze fois moins que Strasbourg (266), alors qu'elle compte autant de tués que Colmar (13 de 2019 à 2024). Les accidents légers y sont très probablement sous-enregistrés dans le fichier national. Conséquence : pour ce secteur, <b>seuls les indicateurs fondés sur les décès sont fiables</b>.</p>
    <p>Le même décalage se voit à l'échelle du département : le Haut-Rhin enregistre 469 accidents par million d'habitants et par an, contre 785 au niveau national.</p>
    {fig("route_07_recording_completeness.webp", "Accidents enregistrés et tués par million d'habitants, pour chaque département", "Accidents enregistrés (en abscisse, échelle logarithmique) et tués (en ordonnée) par million d'habitants et par an, pour chaque département.")}
    <h3>Ce qui rend un accident mortel</h3>
    <p>À autres facteurs égaux, la présence d'un piéton ou d'un poids lourd multiplie environ par 3 la probabilité (en cote) qu'un accident soit mortel ; un obstacle fixe ou un choc frontal par 2,6 ; une route à 80-90 km/h par 2,1 par rapport à 50 km/h ; la nuit sans éclairage par 1,75. Deux résultats semblent contre-intuitifs et rappellent qu'il s'agit d'associations, pas de causes : le mauvais temps (0,84 : on ralentit, et la pluie ajoute beaucoup d'accidents légers) et la trottinette (0,75 : surtout des chutes urbaines à basse vitesse). Le modèle classe correctement les accidents (AUC 0,76 sur des données non vues) mais n'explique qu'une partie du résultat : la vitesse au choc, l'alcool et le port de la ceinture ne sont pas dans les données ouvertes.</p>
    {fig("route_08_odds_ratios.webp", "Rapports de cotes de la régression logistique", "Ce qui augmente ou diminue le risque qu'un accident corporel soit mortel (rapports de cotes).")}
  </section>
  <section>
    <h2>Les limites</h2>
    <ul>
      <li>Données de police uniquement : les accidents sans intervention manquent, et pas de la même façon partout (voir Mulhouse).</li>
      <li>Pas de données d'exposition (kilomètres parcourus par mode) : la hausse des morts en trottinette reflète peut-être en partie la hausse des trajets.</li>
      <li>Petits nombres dans le Haut-Rhin : les chiffres annuels fluctuent au hasard.</li>
    </ul>
    <p class="note">Tout se relance avec <code>python run_all.py</code> (environ 2 minutes).</p>
  </section>
"""

MED = f"""
  <section>
    <h2>La question</h2>
    <p>À quelle vitesse augmentent les dépenses de médicaments remboursés, et pourquoi ? Quels médicaments et quels domaines expliquent la hausse ? Comment ont évolué quelques usages suivis en santé publique ? Et comment comparer les régions une fois l'âge pris en compte ?</p>
  </section>
  <section>
    <h2>Les données</h2>
    <p>Open Medic, publié par l'Assurance maladie à partir du Système national des données de santé (SNDS) : chaque boîte de médicament délivrée en pharmacie de ville et remboursée, de 2019 à 2025, avec le nombre de patients, par âge, sexe et région. Les médicaments hospitaliers ne sont pas inclus, et les montants excluent les honoraires des pharmaciens.</p>
  </section>
  <section>
    <h2>La méthode</h2>
    <p><b>Chargement.</b> Les nombres sont au format français (1.171,74) et les fichiers ne partagent pas le même encodage (Windows-1252 ou UTF-8) : tout est réécrit en UTF-8, puis chargé et converti en SQL dans DuckDB.</p>
    <p><b>Validation.</b> Les totaux calculés à partir des trois niveaux de détail (molécule, classe, groupe) sont identiques chaque année, à l'euro près.</p>
    <p><b>Suivre une molécule dans le temps.</b> Une molécule ne garde pas toujours le même code : l'OMS a déplacé les analogues du GLP-1 en 2020 et réorganisé les anticancéreux en 2021, et certains libellés sont mal orthographiés certaines années. J'ai relié les codes et libellés qui désignent la même molécule avec un algorithme <i>union-find</i> : cela concerne 19 % de la dépense.</p>
    <p><b>Comparer les régions à âge égal.</b> Standardisation directe : la dépense par habitant de chaque région, dans chaque classe d'âge, est pondérée par la structure d'âge nationale.</p>
  </section>
  <section>
    <h2>Les résultats</h2>
    <h3>La dépense monte, pas le volume</h3>
    <p>L'Assurance maladie a remboursé 27,4 milliards d'euros de médicaments délivrés en pharmacie en 2025, contre 19,1 milliards en 2019 : <b>+43 % en six ans</b>. Le nombre de boîtes, lui, n'a pas bougé (+1 %). Le prix moyen d'une boîte est passé de 9,77 € à 13,51 € : la hausse vient de ce qui est délivré (des traitements nouveaux et chers), pas de la quantité.</p>
    {fig("med_01_spending_vs_volume.webp", "Dépense et nombre de boîtes de 2019 à 2025, et prix moyen d'une boîte", "Dépense remboursée et nombre de boîtes (indice 2019), et prix moyen d'une boîte.")}
    <h3>Où sont allés les 8,3 milliards de plus</h3>
    <p>Les médicaments du cancer et de l'immunologie expliquent 3,2 milliards de la hausse (38 %). Une seule molécule, le tafamidis (maladie cardiaque rare), est passée de 45 millions à 1,07 milliard d'euros pour environ 16 000 patients. La dépense se concentre : 55 molécules sur environ 1 100 font la moitié du total, contre 70 en 2019.</p>
    {fig("med_02_growth_by_group.webp", "Contribution de chaque groupe thérapeutique à la hausse de la dépense", "Contribution de chaque groupe thérapeutique à la hausse de la dépense entre 2019 et 2025.")}
    <h3>Trois évolutions d'usage</h3>
    <ul>
      <li><b>Analogues du GLP-1</b> (diabète) : de 415 000 patients en 2020 à 932 000 en 2025.</li>
      <li><b>Antibiotiques</b> : effondrement pendant la pandémie (-17 % de patients en 2020), retour au niveau de 2019 en 2024.</li>
      <li><b>TDAH</b> : les adultes traités par méthylphénidate sont passés de 17 000 à 114 000 (×6,8).</li>
    </ul>
    {fig("med_04_three_stories.webp", "Patients sous analogues du GLP-1, sous antibiotiques et traités pour un TDAH", "Analogues du GLP-1 (patients), antibiotiques (indice 2019 = 100) et méthylphénidate (patients, par âge), de 2019 à 2025.")}
    <h3>Les régions à âge égal</h3>
    <p>Les plus de 60 ans coûtent 852 € par habitant, contre 262 € pour les 20-59 ans et 110 € pour les moins de 20 ans. Les régions âgées paraissent donc chères. Après standardisation sur l'âge, l'Île-de-France, la région la plus jeune, passe de la 11<sup>e</sup> à la 3<sup>e</sup> place sur 12 ; la Nouvelle-Aquitaine recule de la 2<sup>e</sup> à la 7<sup>e</sup> ; le Grand Est est 4<sup>e</sup>.</p>
    {fig("med_05_regions.webp", "Dépense par habitant des régions, brute et standardisée sur l'âge", "Dépense par habitant de chaque région, brute et à âge égal.")}
  </section>
  <section>
    <h2>Les limites</h2>
    <ul>
      <li>Pharmacies de ville uniquement : beaucoup de traitements coûteux du cancer sont délivrés à l'hôpital et n'apparaissent pas ici.</li>
      <li>Prix catalogue, avant les remises confidentielles négociées avec l'État : la dépense nette est plus faible.</li>
      <li>Trois classes d'âge seulement : la standardisation reste grossière.</li>
    </ul>
    <p class="note">Tout se relance avec <code>python run_all.py</code>.</p>
  </section>
"""

P = [
 ("bloc-operatoire", "Des données aux plannings de bloc robustes", "Plannings de bloc opératoire",
  "Étude de recherche · octobre 2026 · Python, scikit-learn, HiGHS",
  "À quel point la durée d'une opération est-elle incertaine, et qu'est-ce que le fait d'apprendre cette incertitude change dans un planning de bloc opératoire ?",
  [("6 385","opérations en données ouvertes (VitalDB)"),("80,1 %","de couverture pour un intervalle visé à 80 %, contre 76,5 % avec l'historique"),("113 → 19 min","de dépassement par salle et par jour"),("88,7 %","d'occupation des salles")],
  "surgery-duration-uncertainty", BLOC,
  "Apprendre l'incertitude des durées opératoires (prédiction conforme) et l'utiliser dans un modèle de planification en nombres entiers : dépassements réduits de 113 à 19 minutes par salle et par jour.",
  "bloc_03_schedule_frontier.webp"),
 ("accidents-route", "Accidents de la route en France et dans le Haut-Rhin, 2019-2024", "Accidents de la route",
  "Analyse de données · octobre 2026 · SQL (DuckDB), Python, statsmodels",
  "Quand, où et à qui arrivent les morts sur la route, et qu'est-ce qui rend un accident corporel mortel ?",
  [("309 756","accidents corporels en métropole"),("18 356","tués de 2019 à 2024"),("68 %","des tués hors agglomération, pour 36 % des accidents"),("AUC 0,76","pour le modèle de gravité")],
  "road-accidents-france", ROUTE,
  "Analyse de 309 756 accidents corporels et 18 356 tués en France de 2019 à 2024 : SQL, validation sur les chiffres officiels, régression logistique, biais d'enregistrement à Mulhouse.",
  "route_06_haut_rhin_map.webp"),
 ("medicaments", "Ce que rembourse la France : les médicaments, 2019-2025", "Médicaments remboursés",
  "Analyse de données · octobre 2026 · SQL (DuckDB), Python, pandas",
  "Les dépenses de médicaments en pharmacie augmentent : de combien, pourquoi, et comment comparer les régions équitablement ?",
  [("27,4 Md€","remboursés en 2025, contre 19,1 Md€ en 2019"),("+43 %","de dépense pour +1 % de boîtes"),("9,77 → 13,51 €","prix moyen d'une boîte"),("19 %","de la dépense reliée malgré les changements de codes")],
  "medicine-spending-france", MED,
  "160 milliards d'euros de médicaments remboursés de 2019 à 2025 : la dépense augmente de 43 % à volume constant. Molécules suivies malgré les changements de codes, régions comparées à âge égal.",
  "med_01_spending_vs_volume.webp"),
]
(OUT / "etudes.css").write_text(CSS)
for i, (slug, title, short, kicker, lede, stats, repo, body, desc, og) in enumerate(P):
    prev = (f"{P[i-1][0]}.html", P[i-1][2]) if i > 0 else None
    nxt = (f"{P[i+1][0]}.html", P[i+1][2]) if i < len(P) - 1 else None
    (OUT / f"{slug}.html").write_text(page(slug, title, short, kicker, lede, stats, repo, body, prev, nxt, desc, og), encoding="utf-8")
    print("wrote", slug)
