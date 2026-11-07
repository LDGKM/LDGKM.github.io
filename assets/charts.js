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

  var MAP = {"bloc-rules":blocRules, "acc-map":accMap, "regions":regions, "trends":trends};
  document.querySelectorAll("figure.chart[data-chart]").forEach(function(f){ var fn = MAP[f.dataset.chart]; if (fn) fn(f); });
})();
