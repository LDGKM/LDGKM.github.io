/* deogratias-loutou.fr — "Une question ?" : a small retrieval assistant over the site's own pages.
   Keyword search (BM25) with a glossary, a coverage threshold to refuse, extractive answers with links.
   No generative model: every word shown comes from a page of the site. Method borrowed from Vigie. */
(function(){
  "use strict";

  /* ---------- engine (also used by _tools/ask/eval.js under Node) ---------- */
  var STOP = ("a au aux avec ce ces cet cette c ca d de des du elle elles en et est etre il ils je j l la le les leur leurs lui m ma mais me mes moi mon n ne ni nos notre nous on ou par pas pour qu que quel quelle quelles quels qui quoi s sa se ses si son sur t ta te tes toi ton tu un une vos votre vous y " +
    "ai as avez avons ont sont suis etait fait faire fais font peut peux veut est-ce comment pourquoi combien quand ou dont lequel laquelle cela ceci tout tous toute toutes tres plus moins bien aussi deja encore " +
    "deo gratias loutou dgl parle parler dis dire donne donner moi connait connaitre sait savoir avoir utilise utiliser " +
    "the of and to in on for is are was were be been with what which who whom how why when where does do did has have had his him he it its an this that these those can could would will about tell me your you any").split(" ");
  var STOPSET = {}; STOP.forEach(function(w){ STOPSET[w] = 1; });
  var GLOSS = {
    contrat:["alternance","stage"], recherch:["alternance","stage"], disponib:["mai","2027","alternance"], quand:["mai","2027"],
    langue:["anglais","francais"], formation:["master","licence","universit"], etudie:["master","licence","universit"], diplome:["master","licence"],
    contact:["mail","linkedin"], contacte:["mail","linkedin"], joindre:["mail","linkedin"], email:["mail"], adresse:["mail"], ecrire:["mail"],
    ia:["rag","vigie","llama"], intellig:["rag","vigie"], llm:["rag","vigie","llama","qwen"], chatbot:["vigie","assistan"], langage:["qwen","llama","vigie"],
    machine:["scikit","gradient","regressi"], learning:["scikit","gradient","regressi"], apprenti:["scikit","gradient"],
    certific:["certific"], equipe:["equipe","scrum"], mort:["tue","mortel"], deces:["tue","mortel"], inventer:["control","verifie","refuse","citation"],
    biblioth:["pandas","numpy","scikit"], experien:["stage","stagiair"], travaill:["stage","stagiair"], entrepri:["stage","petitavi"],
    competen:["python","sql","cpp"], skill:["python","sql","cpp"], job:["alternance","stage"], internsh:["alternance","internsh"], available:["may","2027"],
    reach:["mail","linkedin"], contract:["alternance","work-study"], speak:["english","french"], language:["english","french"]
  };
  function norm(s){ return s.normalize("NFD").replace(/[̀-ͯ]/g, "").toLowerCase().replace(/c\+\+/g, " cpp ").replace(/c#/g, " csharp "); }
  // light stemming: plural, then one common French ending, then at most 8 letters
  var SUF = ["issement", "ation", "ement", "ance", "ence", "ite", "ee", "er", "ent", "ez", "e"];
  function stem(w){
    if (w.length > 4 && /[sx]$/.test(w) && !/ss$/.test(w)) w = w.slice(0, -1);
    for (var i = 0; i < SUF.length; i++){ var s = SUF[i]; if (w.length - s.length >= 4 && w.slice(-s.length) === s){ w = w.slice(0, -s.length); break; } }
    return w.length > 8 ? w.slice(0, 8) : w;
  }
  var G = {}; Object.keys(GLOSS).forEach(function(k){ G[stem(k)] = GLOSS[k].map(stem); }); GLOSS = G;
  function tokens(s){ return norm(s).split(/[^a-z0-9]+/).filter(function(w){ return w && !STOPSET[w] && (w.length > 1 || /\d/.test(w)); }).map(stem); }

  function Index(docs){
    var N = docs.length, df = {}, avg = 0;
    this.docs = docs.map(function(d){
      var head = tokens(d.title + " " + d.section), body = tokens(d.text), tf = {};
      head.concat(head, body).forEach(function(t){ tf[t] = (tf[t] || 0) + 1; });
      var len = head.length * 2 + body.length; avg += len;
      Object.keys(tf).forEach(function(t){ df[t] = (df[t] || 0) + 1; });
      return {d:d, tf:tf, len:len};
    });
    this.avg = avg / Math.max(1, N); this.N = N;
    this.idf = function(t){ return Math.log(1 + (N - (df[t] || 0) + .5) / ((df[t] || 0) + .5)); };
  }
  Index.prototype.search = function(q, opt){
    opt = opt || {}; var T = opt.threshold == null ? Index.THRESHOLD : opt.threshold, self = this;
    var terms = tokens(q).filter(function(t, i, a){ return a.indexOf(t) === i; });
    if (!terms.length) return {refused:true, terms:terms, best:0, hits:[]};
    var syn = terms.map(function(t){ return GLOSS[t] || []; });
    var total = 0; terms.forEach(function(t){ total += self.idf(t); });
    var scored = this.docs.map(function(x){
      var s = 0, cov = 0;
      function bm(t, w){ var f = x.tf[t] || 0; if (!f) return 0; return w * self.idf(t) * f * 2.2 / (f + 1.2 * (.25 + .75 * x.len / self.avg)); }
      terms.forEach(function(t, i){
        var hit = bm(t, 1), sh = 0;
        syn[i].forEach(function(u){ sh = Math.max(sh, bm(u, .5)); });
        s += hit + sh;
        if (hit || sh) cov += self.idf(t);
      });
      return {x:x, score:s, cov:cov / total};
    }).filter(function(r){ return r.score > 0; });
    scored.sort(function(a, b){ return (b.score * (.4 + b.cov)) - (a.score * (.4 + a.cov)); });
    var best = scored.length ? Math.max.apply(null, scored.slice(0, 5).map(function(r){ return r.cov; })) : 0;
    var seen = {}, hits = [];
    for (var i = 0; i < scored.length && hits.length < 3; i++){
      var k = scored[i].x.d.key; if (seen[k]) continue; seen[k] = 1; hits.push(scored[i]);
    }
    var top = hits.length ? hits[0].score * (.4 + hits[0].cov) : 0;
    hits = hits.filter(function(r, i){ return i === 0 || r.score * (.4 + r.cov) >= top * .35; });
    var marks = terms.slice(); syn.forEach(function(a){ a.forEach(function(u){ if (marks.indexOf(u) < 0) marks.push(u); }); });
    return {refused: best < T, terms:terms, marks:marks, best:best, hits:hits};
  };
  Index.THRESHOLD = 0.5;
  Index.tokens = tokens;
  if (typeof module !== "undefined" && module.exports){ module.exports = Index; return; }

  /* ---------- interface ---------- */
  var fr = (document.documentElement.lang || "fr").indexOf("fr") === 0;
  var L = fr ? {
    title:"Une question sur mon parcours ?", intro:"Je cherche la réponse dans les pages de ce site et je vous montre le passage exact, avec son lien. Je n'invente rien : si le site ne dit rien, je le dis.",
    ph:"Ex. : quel contrat recherche-t-il ?", go:"Chercher", close:"Fermer",
    ex:["Quel contrat recherche-t-il ?", "Quelles compétences en données ?", "Comment Vigie évite-t-il d'inventer ?", "Résultats au bloc opératoire"],
    best:"Passage le plus proche", more:"Autres passages", open:"Lire sur la page →",
    no:"Je ne trouve pas cette information sur le site.", noHow:"Plutôt que de deviner, je préfère vous laisser me poser la question directement : ",
    method:"Recherche par mots-clés (BM25) et glossaire, dans {n} passages du site. Pas de modèle génératif : chaque mot affiché vient d'une page. Même principe de refus que dans ",
    evalT:"Évaluation", loading:"Chargement…", file:"/assets/ask-fr.json", vigie:"/etudes/vigie.html"
  } : {
    title:"A question about my background?", intro:"I look for the answer in this site's pages and show you the exact passage, with its link. Nothing is made up: if the site doesn't say, I say so.",
    ph:"E.g. what kind of position is he looking for?", go:"Search", close:"Close",
    ex:["What position is he looking for?", "Which data skills?", "What is Vigie?", "Surgery scheduling results"],
    best:"Closest passage", more:"Other passages", open:"Read on the page →",
    no:"I can't find that on the site.", noHow:"Rather than guess, I'd rather you ask me directly: ",
    method:"Keyword search (BM25) with a glossary over {n} passages of the site. No generative model: every word shown comes from a page. Same refusal principle as ",
    evalT:"Evaluation", loading:"Loading…", file:"/assets/ask-en.json", vigie:"/etudes/vigie.html"
  };
  var idx = null, meta = null, dlg = null;
  function esc(s){ return s.replace(/[&<>"]/g, function(c){ return {"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]; }); }
  function mark(text, terms){
    // highlight words whose stem is one of the query terms
    return esc(text).replace(/[A-Za-zÀ-ÿ0-9+#]+/g, function(w){ var t = Index.tokens(w)[0]; return t && terms.indexOf(t) >= 0 ? "<mark>" + w + "</mark>" : w; });
  }
  function bestSentence(text, terms){
    var parts = text.match(/[^.!?;]+[.!?;]?/g) || [text], best = parts[0], bs = -1;
    parts.forEach(function(p){ var tk = Index.tokens(p), s = 0; terms.forEach(function(t){ if (tk.indexOf(t) >= 0) s++; }); s += Math.min(p.length, 200) / 1000; if (s > bs){ bs = s; best = p; } });
    return best.trim();
  }
  function build(){
    dlg = document.createElement("dialog"); dlg.className = "ask"; dlg.setAttribute("aria-labelledby", "ask-t");
    dlg.innerHTML = '<div class="ask-in"><div class="ask-head"><h2 id="ask-t">' + L.title + '</h2><button type="button" class="ask-x" aria-label="' + L.close + '">×</button></div>' +
      '<p class="ask-intro">' + L.intro + '</p>' +
      '<form class="ask-f" role="search"><label class="sr" for="ask-q">' + L.title + '</label><input id="ask-q" type="search" autocomplete="off" placeholder="' + esc(L.ph) + '" maxlength="200"><button class="btn primary" type="submit">' + L.go + '</button></form>' +
      '<div class="chips ask-ex">' + L.ex.map(function(e){ return '<button type="button" class="chip">' + esc(e) + '</button>'; }).join("") + '</div>' +
      '<div class="ask-out" aria-live="polite"></div><p class="ask-meta"></p></div>';
    document.body.appendChild(dlg);
    var input = dlg.querySelector("#ask-q");
    dlg.querySelector(".ask-x").addEventListener("click", function(){ dlg.close(); });
    dlg.addEventListener("click", function(e){ if (e.target === dlg) dlg.close(); });
    dlg.querySelector("form").addEventListener("submit", function(e){ e.preventDefault(); ask(input.value); });
    dlg.querySelectorAll(".ask-ex .chip").forEach(function(b){ b.addEventListener("click", function(){ input.value = b.textContent; ask(b.textContent); }); });
    dlg.querySelector(".ask-out").addEventListener("click", function(e){ if (e.target.closest("a") && !/^mailto:/.test(e.target.closest("a").getAttribute("href"))) dlg.close(); });
  }
  function ask(q){
    q = (q || "").trim(); var out = dlg.querySelector(".ask-out"); if (!q) return;
    if (!idx){ out.textContent = L.loading; return; }
    var r = idx.search(q);
    try { if (window.goatcounter && goatcounter.count) goatcounter.count({path:"ask/" + (r.refused ? "refused" : "found"), event:true}); } catch(e){}
    if (r.refused){
      out.innerHTML = '<div class="ask-no"><p><b>' + L.no + '</b></p><p>' + L.noHow + '<a href="mailto:loutoudeogratias@gmail.com?subject=' + encodeURIComponent(q) + '">loutoudeogratias@gmail.com</a></p></div>';
      return;
    }
    out.innerHTML = r.hits.map(function(h, i){
      var d = h.x.d, sent = bestSentence(d.text, r.marks), rest = d.text.length > sent.length + 5;
      return '<article class="ask-hit' + (i ? "" : " top") + '">' + (i === 0 ? '<p class="ask-k">' + L.best + '</p>' : (i === 1 ? '<p class="ask-k">' + L.more + '</p>' : "")) +
        '<h3>' + esc(d.title) + (d.section ? ' <span>· ' + esc(d.section) + '</span>' : "") + '</h3>' +
        '<blockquote>' + mark(i === 0 ? sent : (d.text.length > 220 ? sent : d.text), r.marks) + '</blockquote>' +
        (i === 0 && rest ? '<details><summary>' + (fr ? "Tout le passage" : "Full passage") + '</summary><p>' + mark(d.text, r.terms) + '</p></details>' : "") +
        '<a href="' + esc(d.url) + '">' + L.open + '</a></article>';
    }).join("");
  }
  function load(){
    fetch(L.file).then(function(r){ return r.json(); }).then(function(j){
      idx = new Index(j.docs); if (j.threshold != null) Index.THRESHOLD = j.threshold; meta = j.eval;
      var m = L.method.replace("{n}", j.docs.length) + '<a href="' + L.vigie + '"' + (fr ? "" : ' hreflang="fr"') + '>Vigie</a>.';
      if (meta) m += " <b>" + L.evalT + "</b>" + (fr ? " : " : ": ") + meta.text;
      dlg.querySelector(".ask-meta").innerHTML = m;
      var q = dlg.querySelector("#ask-q").value; if (q) ask(q);
    });
  }
  window.siteAsk = function(){
    if (!dlg){ build(); load(); }
    if (!dlg.open) dlg.showModal();
    setTimeout(function(){ dlg.querySelector("#ask-q").focus(); }, 30);
  };
})();
