/* Interactive charts for the study pages. Plain SVG, no library; colours come from the site's CSS tokens.
   Each chart: <figure class="chart" data-chart="name"> … </figure> */
(function(){
  "use strict";
  var NS = "http://www.w3.org/2000/svg";
  var reduced = matchMedia("(prefers-reduced-motion: reduce)").matches;
  function css(n){ return getComputedStyle(document.documentElement).getPropertyValue(n).trim(); }
  function el(tag, attrs, parent){ var e = document.createElementNS(NS, tag); for (var k in attrs) e.setAttribute(k, attrs[k]); if (parent) parent.appendChild(e); return e; }
  function h(tag, attrs, html){ var e = document.createElement(tag); for (var k in attrs) e.setAttribute(k, attrs[k]); if (html != null) e.innerHTML = html; return e; }
  function scale(d0, d1, r0, r1){ return function(v){ return r0 + (v - d0) / (d1 - d0) * (r1 - r0); }; }
  function fmt(v, d){ return v.toLocaleString("fr-FR", {minimumFractionDigits:d || 0, maximumFractionDigits:d || 0}); }
  function chips(container, items, onPick, label){
    var box = h("div", {class:"chips", role:"group", "aria-label":label});
    items.forEach(function(it, i){
      var b = h("button", {type:"button", class:"chip", "aria-pressed": String(i === 0)}, it.label);
      b.addEventListener("click", function(){ box.querySelectorAll(".chip").forEach(function(c){ c.setAttribute("aria-pressed", String(c === b)); }); onPick(it, i); });
      box.appendChild(b);
    });
    container.appendChild(box); return box;
  }
  function onTheme(fn){ new MutationObserver(fn).observe(document.documentElement, {attributes:true, attributeFilter:["data-theme"]});
    matchMedia("(prefers-color-scheme: dark)").addEventListener("change", fn); }
  function axisX(svg, x, ticks, y0, fmtT){ var g = el("g", {class:"axis"}, svg);
    ticks.forEach(function(t){ el("line", {x1:x(t), x2:x(t), y1:y0, y2:y0 + 4}, g); var tx = el("text", {x:x(t), y:y0 + 16, "text-anchor":"middle"}, g); tx.textContent = fmtT ? fmtT(t) : t; }); return g; }
  function axisY(svg, y, ticks, x0, x1, fmtT){ var g = el("g", {class:"axis"}, svg);
    ticks.forEach(function(t){ el("line", {x1:x0, x2:x1, y1:y(t), y2:y(t), "stroke-dasharray":"2 4"}, g); var tx = el("text", {x:x0 - 6, y:y(t) + 4, "text-anchor":"end"}, g); tx.textContent = fmtT ? fmtT(t) : t; }); return g; }
  function ord(n){ return n === 1 ? "1re" : n + "e"; }
  function width(fig){ return Math.round(Math.max(320, Math.min(720, fig.clientWidth - 34))); }
  function load(url){ return fetch(url).then(function(r){ return r.json(); }); }

  /* 1. Operating rooms: pick a planning rule, see overtime vs utilisation ----------------------- */
  function blocRules(fig){
    load("/data/etudes/bloc_rules.json").then(function(rows){
      var FAM = [
        {key:"quantile", label:"Quantile appris", color:"--d-blue", p:"τ", fmtP:function(v){ return fmt(v * 100) + "e percentile"; }},
        {key:"fixed buffer", label:"Marge fixe", color:"--accent", fmtP:function(v){ return "+" + fmt(v * 100) + " %"; }},
        {key:"robust (learned set)", label:"Robuste à budget", color:"--d-red", fmtP:function(v){ return "Γ = " + fmt(v, v % 1 ? 1 : 0); }},
        {key:"ML median", label:"Médiane prédite", color:"--ink", fmtP:function(){ return "médiane du modèle"; }},
        {key:"historical", label:"Médianes historiques", color:"--d-grey", fmtP:function(){ return "médiane de l'intervention"; }} ];
      FAM.forEach(function(f){ f.rows = rows.filter(function(r){ return r.policy === f.key; }).sort(function(a, b){ return a.param - b.param; }); });
      var state = {fam:FAM[0], i:2};
      var ctr = h("div", {class:"controls"}); fig.insertBefore(ctr, fig.querySelector(".tip"));
      chips(ctr, FAM, function(f){ state.fam = f; state.i = Math.min(state.i, f.rows.length - 1); if (f.key === "quantile") state.i = 2; setSlider(); draw(); }, "Règle de planification");
      var sl = h("input", {type:"range", min:"0", max:"3", step:"1", value:"2", "aria-label":"Paramètre de la règle"});
      var slWrap = h("label", {class:"hint", style:"flex:1;min-width:200px;margin:0"}); slWrap.appendChild(sl); ctr.appendChild(slWrap);
      sl.addEventListener("input", function(){ state.i = +sl.value; draw(); });
      function setSlider(){ var n = state.fam.rows.length; sl.max = String(n - 1); sl.value = String(state.i); sl.disabled = n < 2; slWrap.style.opacity = n < 2 ? .4 : 1; }
      var W = width(fig), small = W < 520, H = small ? 330 : 400, m = {l:small ? 44 : 56, r:14, t:small ? 26 : 16, b:44};
      var svg = el("svg", {viewBox:"0 0 " + W + " " + H, role:"img", "aria-label":"Occupation des salles en fonction du dépassement moyen, pour chaque règle de planification"});
      fig.insertBefore(svg, fig.querySelector(".tip"));
      var x = scale(0, 120, m.l, W - m.r), y = scale(0.68, 1.0, H - m.b, m.t);
      function draw(){
        while (svg.firstChild) svg.removeChild(svg.firstChild);
        axisY(svg, y, [0.7, 0.8, 0.9, 1.0], m.l, W - m.r, function(t){ return fmt(t * 100) + " %"; });
        axisX(svg, x, small ? [0, 40, 80, 120] : [0, 20, 40, 60, 80, 100, 120], H - m.b, function(t){ return t; });
        var lx = el("text", {x:(m.l + W - m.r) / 2, y:H - 6, "text-anchor":"middle"}, svg); lx.textContent = small ? "dépassement (min par salle et par jour) ← mieux" : "dépassement moyen par salle et par jour (minutes) — plus à gauche, c'est mieux";
        var ly = small ? el("text", {x:m.l, y:10, "text-anchor":"start"}, svg) : el("text", {x:14, y:(m.t + H - m.b) / 2, "text-anchor":"middle", transform:"rotate(-90 14 " + ((m.t + H - m.b) / 2) + ")"}, svg); ly.textContent = small ? "occupation des salles ↑ mieux" : "occupation des salles — plus haut, c'est mieux";
        FAM.forEach(function(f){
          var on = f === state.fam, col = css(f.color);
          if (f.rows.length > 1) el("polyline", {points:f.rows.map(function(r){ return x(r.overtime_min) + "," + y(r.utilisation); }).join(" "), fill:"none", stroke:col, "stroke-width":on ? 3 : 1.5, opacity:on ? 1 : .35}, svg);
          f.rows.forEach(function(r, i){ var sel = on && i === state.i;
            el("circle", {cx:x(r.overtime_min), cy:y(r.utilisation), r:sel ? 9 : on ? 5 : 3.5, fill:col, stroke:sel ? css("--sheet") : "none", "stroke-width":3, opacity:on ? 1 : .45}, svg); });
        });
        var r = state.fam.rows[state.i];
        fig.querySelector(".tip").innerHTML = "<b>" + state.fam.label + " · " + state.fam.fmtP(r.param) + "</b> — dépassement : <b>" + fmt(r.overtime_min) + " min</b> par salle et par jour (± " + fmt(r.overtime_se, 1) + ") · salles en retard : <b>" + fmt(r.rooms_in_overtime * 100) + " %</b> · occupation : <b>" + fmt(r.utilisation * 100, 1) + " %</b> · " + fmt(r.cases, 1) + " opérations par jour";
      }
      setSlider(); draw(); onTheme(draw);
    });
  }

  /* 2. Haut-Rhin accidents map, filterable by year and severity --------------------------------- */
  function accMap(fig){
    load("/data/roads68.json").then(function(data){
      var lat0 = 47.85, kx = Math.cos(lat0 * Math.PI / 180);
      var pts = data.outline, xs = pts.map(function(p){ return p[0] * kx; }), ys = pts.map(function(p){ return p[1]; });
      var x0 = Math.min.apply(null, xs), x1 = Math.max.apply(null, xs), y0 = Math.min.apply(null, ys), y1 = Math.max.apply(null, ys);
      var W = 520, H = Math.round(W * (y1 - y0) / (x1 - x0)), pad = 10;
      var X = scale(x0, x1, pad, W - pad), Y = scale(y0, y1, H - pad, pad);
      var P = function(lon, lat){ return [X(lon * kx), Y(lat)]; };
      var state = {year:0, fatal:false};
      var ctr = h("div", {class:"controls"}); fig.insertBefore(ctr, fig.querySelector(".tip"));
      chips(ctr, [{label:"2019–2024", y:0}].concat([2019, 2020, 2021, 2022, 2023, 2024].map(function(v){ return {label:String(v), y:v}; })),
        function(it){ state.year = it.y; draw(); }, "Année");
      var tog = h("button", {type:"button", class:"chip", "aria-pressed":"false"}, "Mortels seulement");
      tog.addEventListener("click", function(){ state.fatal = !state.fatal; tog.setAttribute("aria-pressed", String(state.fatal)); draw(); });
      ctr.appendChild(tog);
      var svg = el("svg", {viewBox:"0 0 " + W + " " + H, role:"img", "aria-label":"Carte des accidents corporels du Haut-Rhin, 2019-2024", style:"max-width:560px;margin:auto"});
      fig.insertBefore(svg, fig.querySelector(".tip"));
      var outline = el("path", {d:"M" + pts.map(function(p){ return P(p[0], p[1]).join(","); }).join("L") + "Z", "stroke-width":1.5}, svg);
      var g = el("g", {}, svg);
      var sorted = data.points.slice().sort(function(a, b){ return a[2] - b[2]; });
      var dots = sorted.map(function(p){ var c = P(p[0], p[1]); return {p:p, c:el("circle", {cx:c[0].toFixed(1), cy:c[1].toFixed(1)}, g)}; });
      [["Mulhouse", 7.3359, 47.7508], ["Colmar", 7.3585, 48.0794]].forEach(function(t){ var c = P(t[1], t[2]);
        var tx = el("text", {x:c[0] + 10, y:c[1] - 8, style:"font-weight:600"}, svg); tx.textContent = t[0]; });
      function draw(){
        outline.setAttribute("fill", css("--paper")); outline.setAttribute("stroke", css("--accent"));
        var blue = css("--d-blue"), red = css("--d-red"), n = 0, f = 0;
        dots.forEach(function(d){
          var show = (!state.year || d.p[3] === state.year) && (!state.fatal || d.p[2] > 0);
          d.c.setAttribute("r", show ? (d.p[2] > 0 ? 3.6 : 2) : 0);
          d.c.setAttribute("fill", d.p[2] > 0 ? red : blue); d.c.setAttribute("opacity", d.p[2] > 0 ? 1 : .55);
          if (show){ n++; if (d.p[2] > 0) f++; }
        });
        fig.querySelector(".tip").innerHTML = "<b>" + fmt(n) + "</b> accident" + (n > 1 ? "s" : "") + " affiché" + (n > 1 ? "s" : "") + (state.fatal ? "" : ", dont <b>" + fmt(f) + "</b> mortel" + (f > 1 ? "s" : "")) + " · " + (state.year ? state.year : "2019–2024");
      }
      draw(); onTheme(draw);
    });
  }

  /* 3. Regions: crude vs age-standardised spending per inhabitant, animated ranking ----------- */
  function regions(fig){
    load("/data/etudes/med_regions.json").then(function(rows){
      var W = width(fig), small = W < 520, state = {k:"crude"}, row = small ? 26 : 30, m = {l:small ? 172 : 236, r:small ? 50 : 70, t:8}, H = m.t + rows.length * row + 8;
      var ctr = h("div", {class:"controls"}); fig.insertBefore(ctr, fig.querySelector(".tip"));
      chips(ctr, [{label:"Dépense brute", k:"crude"}, {label:"À âge égal (standardisée)", k:"std"}], function(it){ state.k = it.k; draw(); }, "Mesure");
      var svg = el("svg", {viewBox:"0 0 " + W + " " + H, role:"img", "aria-label":"Dépense de médicaments par habitant et par région, brute et standardisée sur l'âge"});
      fig.insertBefore(svg, fig.querySelector(".tip"));
      var x = scale(small ? 320 : 300, 470, m.l, W - m.r);
      var items = rows.map(function(r){
        var g = el("g", {style:reduced ? "" : "transition:transform .7s cubic-bezier(.2,.7,.2,1)"}, svg);
        var name = el("text", {x:m.l - 8, y:row / 2 + 4, "text-anchor":"end"}, g); name.textContent = small ? r.name.replace("Provence-Alpes-Côte d'Azur", "PACA").replace("Bourgogne-Franche-Comté", "Bourgogne-F.-Comté").replace("Auvergne-Rhône-Alpes", "Auvergne-Rh.-Alpes") : r.name;
        var bar = el("rect", {x:m.l, y:5, height:row - 10, rx:2, style:reduced ? "" : "transition:width .7s cubic-bezier(.2,.7,.2,1)"}, g);
        var val = el("text", {y:row / 2 + 4}, g); var rank = el("text", {x:2, y:row / 2 + 4}, g);
        return {r:r, g:g, bar:bar, val:val, name:name, rank:rank};
      });
      function draw(){
        var order = rows.slice().sort(function(a, b){ return b[state.k] - a[state.k]; });
        items.forEach(function(it){
          var i = order.indexOf(it.r), v = it.r[state.k], hi = /Grand Est|Île-de-France/.test(it.r.name);
          it.g.setAttribute("transform", "translate(0," + (m.t + i * row) + ")");
          it.g.style.transform = "translate(0px," + (m.t + i * row) + "px)";
          it.bar.setAttribute("width", Math.max(2, x(v) - m.l).toFixed(1));
          it.bar.setAttribute("fill", hi ? css("--accent") : css("--d-blue")); it.bar.setAttribute("opacity", hi ? 1 : .55);
          it.val.setAttribute("x", (x(v) + 6).toFixed(1)); it.val.textContent = fmt(v) + " €";
          it.rank.textContent = ord(i + 1); it.name.style.fontWeight = hi ? "700" : "400"; it.name.style.fill = hi ? css("--ink") : "";
        });
        var c = rows.slice().sort(function(a, b){ return b.crude - a.crude; }), s = rows.slice().sort(function(a, b){ return b.std - a.std; });
        var idf = rows.filter(function(r){ return /Île-de-France/.test(r.name); })[0], ge = rows.filter(function(r){ return /Grand Est/.test(r.name); })[0];
        fig.querySelector(".tip").innerHTML = "Île-de-France : <b>" + ord(c.indexOf(idf) + 1) + "</b> en brut → <b>" + ord(s.indexOf(idf) + 1) + "</b> à âge égal (c'est la région la plus jeune) · Grand Est : " + ord(c.indexOf(ge) + 1) + " → " + ord(s.indexOf(ge) + 1);
      }
      draw(); onTheme(draw);
    });
  }

  /* 4. Patients over time: GLP-1 analogues and methylphenidate by age ------------------------- */
  function trends(fig){
    load("/data/etudes/med_trends.json").then(function(d){
      var S = [{label:"Analogues du GLP-1", k:"glp1", unit:"patients (milliers)", color:"--d-blue"},
               {label:"Méthylphénidate · moins de 20 ans", k:"mph_0", unit:"patients (milliers)", color:"--accent"},
               {label:"Méthylphénidate · 20-59 ans", k:"mph_20", unit:"patients (milliers)", color:"--d-red"}];
      var W = width(fig), small = W < 520, state = {s:S[0], hover:null}, H = small ? 240 : 300, m = {l:48, r:18, t:16, b:36};
      var ctr = h("div", {class:"controls"}); fig.insertBefore(ctr, fig.querySelector(".tip"));
      chips(ctr, S, function(s){ state.s = s; state.hover = null; draw(); }, "Série");
      var svg = el("svg", {viewBox:"0 0 " + W + " " + H, role:"img", "aria-label":"Nombre de patients par an, 2019-2025"});
      fig.insertBefore(svg, fig.querySelector(".tip"));
      var x = scale(2019, 2025, m.l, W - m.r);
      function draw(){
        while (svg.firstChild) svg.removeChild(svg.firstChild);
        var pts = d[state.s.k], max = Math.max.apply(null, pts.map(function(p){ return p[1]; }));
        var top = Math.ceil(max / 100) * 100, y = scale(0, top, H - m.b, m.t), col = css(state.s.color);
        var tk = [0, top / 4, top / 2, 3 * top / 4, top];
        axisY(svg, y, tk, m.l, W - m.r, function(t){ return fmt(t); });
        axisX(svg, x, small ? [2019, 2021, 2023, 2025] : [2019, 2020, 2021, 2022, 2023, 2024, 2025], H - m.b);
        el("path", {d:"M" + x(pts[0][0]) + "," + y(0) + pts.map(function(p){ return "L" + x(p[0]) + "," + y(p[1]); }).join("") + "L" + x(pts[pts.length - 1][0]) + "," + y(0) + "Z", fill:col, opacity:.12}, svg);
        el("polyline", {points:pts.map(function(p){ return x(p[0]) + "," + y(p[1]); }).join(" "), fill:"none", stroke:col, "stroke-width":3}, svg);
        pts.forEach(function(p){ var on = state.hover === p[0];
          el("circle", {cx:x(p[0]), cy:y(p[1]), r:on ? 7 : 4, fill:col, stroke:css("--sheet"), "stroke-width":2}, svg); });
        var p0 = pts[0], p1 = pts[pts.length - 1], hp = pts.filter(function(p){ return p[0] === state.hover; })[0];
        fig.querySelector(".tip").innerHTML = hp
          ? "<b>" + hp[0] + "</b> : <b>" + fmt(hp[1] * 1000) + "</b> patients — " + state.s.label
          : state.s.label + " : de <b>" + fmt(p0[1] * 1000) + "</b> patients en " + p0[0] + " à <b>" + fmt(p1[1] * 1000) + "</b> en " + p1[0] + " (×" + fmt(p1[1] / p0[1], 1) + "). Survolez un point.";
      }
      svg.addEventListener("pointermove", function(e){ var r = svg.getBoundingClientRect(), vx = (e.clientX - r.left) / r.width * W;
        var yr = Math.round(2019 + (vx - m.l) / (W - m.l - m.r) * 6); if (yr !== state.hover){ state.hover = yr; draw(); } });
      svg.addEventListener("pointerleave", function(){ state.hover = null; draw(); });
      draw(); onTheme(draw);
    });
  }


  /* 5. Coverage of the 80% intervals in each surgical context, method by method ---------------- */
  function coverage(fig){
    load("/data/etudes/bloc_coverage.json").then(function(d){
      var W = width(fig), small = W < 520, row = small ? 28 : 30, m = {l:small ? 150 : 210, r:small ? 46 : 60, t:22}, H = m.t + d.groups.length * row + 26;
      var state = {meth:"CQR"};
      var ctr = h("div", {class:"controls"}); fig.insertBefore(ctr, fig.querySelector(".tip"));
      var order = ["CQR", "Percentiles historiques", "Régression quantile", "Conforme (log)", "CQR par service"];
      chips(ctr, order.map(function(k){ return {label:k, k:k}; }), function(it){ state.meth = it.k; draw(); }, "Méthode");
      var svg = el("svg", {viewBox:"0 0 " + W + " " + H, role:"img", "aria-label":"Couverture des intervalles à 80 % selon le contexte chirurgical"});
      fig.insertBefore(svg, fig.querySelector(".tip"));
      var x = scale(0.4, 1.0, m.l, W - m.r);
      function draw(){
        while (svg.firstChild) svg.removeChild(svg.firstChild);
        axisX(svg, x, small ? [0.4, 0.6, 0.8, 1.0] : [0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0], H - 22, function(t){ return fmt(t * 100) + " %"; });
        var bad = 0;
        d.groups.forEach(function(g, i){
          var v = g.cov[state.meth], yy = m.t + i * row, low = v < 0.75;
          if (low) bad++;
          var t = el("text", {x:m.l - 8, y:yy + row / 2 + 4, "text-anchor":"end"}, svg); t.textContent = small ? g.g.replace("Service · ", "").replace("chirurgie", "chir.").replace("Voie · ", "voie ").replace("Durée prédite · ", "durée ") : g.g;
          var n = el("text", {x:m.l - 8, y:yy + row / 2 + 15, "text-anchor":"end", style:"font-size:9px;opacity:.7"}, svg); if (!small) n.textContent = g.n + " cas";
          el("rect", {x:m.l, y:yy + 6, width:Math.max(2, x(v) - m.l).toFixed(1), height:row - 12, rx:2, fill:low ? css("--d-red") : css("--d-blue"), opacity:low ? .9 : .6}, svg);
          var vt = el("text", {x:(x(v) + 6).toFixed(1), y:yy + row / 2 + 4}, svg); vt.textContent = fmt(v * 100) + " %";
        });
        el("line", {x1:x(0.8), x2:x(0.8), y1:m.t - 6, y2:H - 22, stroke:css("--accent"), "stroke-width":2.5, "stroke-dasharray":"5 4"}, svg);
        var tg = el("text", {x:x(0.8) + 4, y:m.t - 8, style:"fill:" + css("--accent-ink")}, svg); tg.textContent = "objectif 80 %";
        fig.querySelector(".tip").innerHTML = "<b>" + state.meth + "</b> : " + (bad ? "<b>" + bad + "</b> contexte" + (bad > 1 ? "s" : "") + " sous 75 % de couverture (en rouge)." : "aucun contexte sous 75 %.") + " Les petits groupes (moins de 70 cas) sont bruités.";
      }
      draw(); onTheme(draw);
    });
  }

  /* 6. Vigie: what happened to each evaluation question ---------------------------------------- */
  function vigieEval(fig){
    load("/data/etudes/vigie_eval.json").then(function(d){
      var W = width(fig), small = W < 520, H = small ? 92 : 84, m = {l:2, r:2}, state = {i:0};
      var ctr = h("div", {class:"controls"}); fig.insertBefore(ctr, fig.querySelector(".tip"));
      chips(ctr, d.sets.map(function(s, i){ return {label:s.label, i:i}; }), function(it){ state.i = it.i; draw(); }, "Jeu de questions");
      var svg = el("svg", {viewBox:"0 0 " + W + " " + H, role:"img"}); fig.insertBefore(svg, fig.querySelector(".tip"));
      var leg = h("ul", {class:"legend vleg"}); fig.insertBefore(leg, fig.querySelector(".tip"));
      var note = h("p", {class:"hint", style:"margin-top:10px"}); fig.insertBefore(note, fig.querySelector(".tip"));
      function say(c, v, n){ fig.querySelector(".tip").innerHTML = "<b>" + v + " sur " + n + "</b> : " + c.label.toLowerCase() + " (" + fmt(v / n * 100) + " %)."; }
      function draw(){
        while (svg.firstChild) svg.removeChild(svg.firstChild); leg.innerHTML = "";
        var s = d.sets[state.i], x = m.l, span = W - m.l - m.r, y0 = 10, bh = small ? 46 : 40;
        svg.setAttribute("aria-label", s.label + " : " + d.cats.filter(function(c){ return s.v[c.k]; }).map(function(c){ return s.v[c.k] + " " + c.label.toLowerCase(); }).join(", "));
        d.cats.forEach(function(c){
          var v = s.v[c.k]; if (!v) return;
          var w = v / s.n * span, col = css(c.color);
          var r = el("rect", {x:x.toFixed(1), y:y0, width:Math.max(1, w - 2).toFixed(1), height:bh, rx:2, fill:col, opacity:c.k === "ok" ? .75 : .9, tabindex:0, style:"cursor:pointer"}, svg);
          r.addEventListener("mouseenter", function(){ say(c, v, s.n); }); r.addEventListener("focus", function(){ say(c, v, s.n); }); r.addEventListener("click", function(){ say(c, v, s.n); });
          if (w > 26){ var t = el("text", {x:(x + w / 2 - 1).toFixed(1), y:y0 + bh / 2 + 5, "text-anchor":"middle", style:"font-size:13px;font-weight:600;fill:" + (c.k === "refused" ? css("--paper") : "#fff")}, svg); t.textContent = v; t.style.pointerEvents = "none"; }
          var li = h("li", null, '<i style="background:' + col + '"></i>' + c.label + " · <b>" + v + "</b>"); leg.appendChild(li);
          x += w;
        });
        var ax = el("text", {x:m.l, y:y0 + bh + 22}, svg); ax.textContent = "0";
        var ax2 = el("text", {x:W - m.r, y:y0 + bh + 22, "text-anchor":"end"}, svg); ax2.textContent = s.n + " questions";
        note.textContent = s.note;
        var ok = s.v.ok, cov = s.n - s.v.refused;
        fig.querySelector(".tip").innerHTML = "<b>" + ok + " sur " + cov + "</b> questions couvertes reçoivent une réponse juste" + (s.v.refused ? ", et <b>" + s.v.refused + " sur " + s.v.refused + "</b> questions hors corpus sont refusées." : ".") + " Survolez ou touchez une barre.";
      }
      draw(); onTheme(draw);
    });
  }

  /* 7. Vigie: the citation and number check, ported from src/core/grounding.cpp ------------------ */
  function vigieCheck(fig){
    var passages = [
      {t:"Livret A — Plafond", x:"Le plafond des versements sur un livret A est de 22 950 € pour une personne physique."},
      {t:"Livret A — Intérêts", x:"Les intérêts du livret A sont calculés par quinzaine."}
    ];
    var examples = [
      {label:"Réponse correcte", a:"Le plafond des versements sur un livret A est de 22 950 € pour une personne physique [1]."},
      {label:"Nombre inventé", a:"Le plafond d'un livret A est de 23 000 € [1]."},
      {label:"Mauvais extrait cité", a:"Les intérêts sont calculés par quinzaine, dans la limite de 22 950 € [2]."},
      {label:"Citation inexistante", a:"Le plafond est de 22 950 € [3]."},
      {label:"Sans citation", a:"Le plafond est de 22 950 €."},
      {label:"Phrase finale non citée", a:"Le plafond est de 22 950 € [1]. Il rapporte 3 % par an."}
    ];
    function isDigit(c){ return c >= "0" && c <= "9"; }
    function sep(s, p){ var c = s.charAt(p); return (c === " " || c === "." || c === " " || c === " ") ? 1 : 0; }
    function thousands(s, p){ return p + 2 < s.length && isDigit(s[p]) && isDigit(s[p + 1]) && isDigit(s[p + 2]) && (p + 3 === s.length || !isDigit(s[p + 3])); }
    function scaleAfter(s, p){ var r = s.slice(p + sep(s, p)); return r.indexOf("million") === 0 ? "000000" : r.indexOf("milliard") === 0 ? "000000000" : ""; }
    function numbers(s){
      var out = {}, p = 0;
      while (p < s.length){
        if (!isDigit(s[p])){ p++; continue; }
        var n = "";
        while (p < s.length){
          if (isDigit(s[p])){ n += s[p++]; continue; }
          var k = sep(s, p); if (!k || !thousands(s, p + k)) break; p += k;
        }
        out[n + scaleAfter(s, p)] = true;
      }
      return Object.keys(out);
    }
    function cites(a){
      var r = {nums:[], text:"", end:0}, p = 0;
      while (p < a.length){
        var o = a.indexOf("[", p); if (o < 0) break;
        r.text += a.slice(p, o);
        var c = a.indexOf("]", o), body = c < 0 ? "" : a.slice(o + 1, c);
        if (!/^[0-9][0-9, ]{0,23}$/.test(body)){ r.text += "["; p = o + 1; continue; }
        numbers(body).forEach(function(n){ var v = n.length > 3 ? 0 : +n; if (r.nums.indexOf(v) < 0) r.nums.push(v); });
        p = c + 1; r.end = p;
      }
      if (p < a.length) r.text += a.slice(p);
      return r;
    }
    function check(a){
      var steps = [];
      if (a.indexOf("INFORMATION NON TROUV") >= 0) return {v:"refus", steps:["Le modèle dit que les extraits ne répondent pas : Vigie affiche « Information non trouvée »."]};
      var f = cites(a);
      if (!f.nums.length) return {v:"no", steps:["Aucune citation [n] : rien ne relie le texte aux extraits."]};
      var kept = a.slice(0, f.end) + (a.charAt(f.end) === "." ? "." : "");
      if (kept.length < a.trim().length) steps.push("Ce qui suit la dernière citation n'est justifié par rien : coupé. Reste « " + kept + " »");
      var c = cites(kept), known = [];
      for (var i = 0; i < c.nums.length; i++){
        var n = c.nums[i];
        if (n < 1 || n > passages.length) return {v:"no", steps:steps.concat(["La citation [" + n + "] ne correspond à aucun extrait fourni (il y en a " + passages.length + ")."])};
        known = known.concat(numbers(passages[n - 1].t + " " + passages[n - 1].x));
      }
      steps.push(c.nums.length > 1 ? "Les citations " + c.nums.map(function(n){ return "[" + n + "]"; }).join(", ") + " existent." : "La citation [" + c.nums[0] + "] existe.");
      var said = numbers(c.text), miss = said.filter(function(n){ return known.indexOf(n) < 0; });
      if (miss.length) return {v:"no", steps:steps.concat([(miss.length > 1 ? "Nombres absents" : "Nombre absent") + " des extraits cités : " + miss.map(function(n){ return (+n).toLocaleString("fr-FR"); }).join(", ") + "."])};
      var fr = said.map(function(n){ return (+n).toLocaleString("fr-FR"); }).join(", ");
      steps.push(!said.length ? "Aucun nombre à vérifier." : said.length > 1 ? "Les nombres " + fr + " figurent dans les extraits cités." : "Le nombre " + fr + " figure dans l'extrait cité.");
      return {v:"ok", steps:steps, text:kept};
    }
    var box = h("div", {class:"vcheck"});
    box.innerHTML = '<ol class="vpass">' + passages.map(function(p, i){ return "<li><b>[" + (i + 1) + "] " + p.t + "</b><br>" + p.x + "</li>"; }).join("") + "</ol>";
    var ctr = h("div", {class:"controls"}); box.appendChild(ctr);
    var lab = h("label", {for:"vcheck-a", class:"hint", style:"display:block;margin:0 0 6px"}, "Réponse du modèle (modifiable) :"); box.appendChild(lab);
    var ta = h("textarea", {id:"vcheck-a", rows:"3", spellcheck:"false"}); box.appendChild(ta);
    var out = h("div", {class:"vout", "aria-live":"polite"}); box.appendChild(out);
    fig.insertBefore(box, fig.querySelector(".tip"));
    function run(){
      var r = check(ta.value);
      var head = r.v === "ok" ? '<p class="vv ok">✓ Réponse affichée</p>' : r.v === "refus" ? '<p class="vv">Refus</p>' : '<p class="vv no">✗ Réponse rejetée : Vigie affiche les extraits tels quels</p>';
      out.innerHTML = head + "<ul>" + r.steps.map(function(s){ return "<li>" + s.replace(/</g, "&lt;") + "</li>"; }).join("") + "</ul>";
    }
    chips(ctr, examples, function(it){ ta.value = it.a; run(); }, "Exemples de réponses");
    ta.value = examples[0].a; ta.addEventListener("input", run); run();
  }

  var MAP = {"bloc-rules":blocRules, "acc-map":accMap, "regions":regions, "trends":trends, "coverage":coverage, "vigie-eval":vigieEval, "vigie-check":vigieCheck};
  document.querySelectorAll("figure.chart[data-chart]").forEach(function(f){ var fn = MAP[f.dataset.chart]; if (fn) fn(f); });
})();
