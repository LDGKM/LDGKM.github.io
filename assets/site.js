/* deogratias-loutou.fr — shared behaviour: theme toggle, mobile menu, back to top, language memory. */
(function(){
  "use strict";
  var root = document.documentElement, fr = (root.lang || "fr").indexOf("fr") === 0;
  var store = { get: function(k){ try { return localStorage.getItem(k); } catch(e){ return null; } },
                set: function(k, v){ try { localStorage.setItem(k, v); } catch(e){} } };

  // theme: the early inline script already applied a saved choice; the button flips light/dark
  var themeBtn = document.querySelector(".site-theme");
  function current(){ return root.dataset.theme || (matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light"); }
  function paint(){
    if (!themeBtn) return;
    var dark = current() === "dark";
    themeBtn.setAttribute("aria-pressed", String(dark));
    themeBtn.setAttribute("aria-label", dark ? (fr ? "Passer en thème clair" : "Switch to light theme") : (fr ? "Passer en thème sombre" : "Switch to dark theme"));
    themeBtn.innerHTML = dark
      ? '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>'
      : '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"/></svg>';
  }
  if (themeBtn){
    paint();
    themeBtn.addEventListener("click", function(){
      var next = current() === "dark" ? "light" : "dark";
      root.dataset.theme = next; store.set("site-theme", next); paint();
    });
    matchMedia("(prefers-color-scheme: dark)").addEventListener("change", paint);
  }

  // mobile menu
  var menuBtn = document.querySelector(".site-menu"), nav = document.getElementById("site-nav");
  if (menuBtn && nav){
    menuBtn.addEventListener("click", function(){
      var open = nav.classList.toggle("open"); menuBtn.setAttribute("aria-expanded", String(open));
    });
    nav.addEventListener("click", function(e){ if (e.target.closest("a")){ nav.classList.remove("open"); menuBtn.setAttribute("aria-expanded", "false"); } });
    document.addEventListener("keydown", function(e){ if (e.key === "Escape" && nav.classList.contains("open")){ nav.classList.remove("open"); menuBtn.setAttribute("aria-expanded", "false"); menuBtn.focus(); } });
  }

  // remember the language a visitor picks (the 3D story reads it)
  document.querySelectorAll("[data-setlang]").forEach(function(a){ a.addEventListener("click", function(){ store.set("chezdeo-lang", a.dataset.setlang); }); });

  // back to top
  var top = document.createElement("button");
  top.type = "button"; top.className = "to-top"; top.textContent = "↑";
  top.setAttribute("aria-label", fr ? "Revenir en haut de la page" : "Back to top");
  top.addEventListener("click", function(){ window.scrollTo({top:0, behavior: matchMedia("(prefers-reduced-motion: reduce)").matches ? "auto" : "smooth"}); });
  document.body.appendChild(top);
  var onScroll = function(){ top.classList.toggle("show", window.scrollY > window.innerHeight * 1.2); };
  addEventListener("scroll", onScroll, {passive:true}); onScroll();
})();
