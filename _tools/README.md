# Outils de génération

- `story/build_story.py` : génère le récit 3D (`/index.html` en français, `/en/index.html` en anglais) à partir de `story_template.html`. Usage : `python3 _tools/story/build_story.py .`
- `make_etudes.py` : génère les pages `etudes/*.html`.
- `data/bloc_day.json` : journée de bloc opératoire tirée de la simulation du dépôt surgery-duration-uncertainty (jour 146, le plus représentatif des moyennes).
- `site_chrome.py` : en-tête, pied de page et liens communs des pages classiques, études et 404 (entre les marqueurs `<!--site:...-->`). Usage : `python3 _tools/site_chrome.py .`
- `/assets/site.css` et `/assets/site.js` : système de design commun (couleurs, thème clair/sombre, menu, boutons, filtres) ; `/assets/charts.js` : graphiques interactifs des études, données dans `/data/etudes/`.
