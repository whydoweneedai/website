(function () {
  "use strict";

  var toggle = document.querySelector(".nav-toggle");
  var panel = document.getElementById("site-nav-panel");
  if (toggle && panel) {
    toggle.addEventListener("click", function () {
      var open = toggle.getAttribute("aria-expanded") === "true";
      toggle.setAttribute("aria-expanded", open ? "false" : "true");
      document.body.classList.toggle("nav-open", !open);
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && document.body.classList.contains("nav-open")) {
        toggle.setAttribute("aria-expanded", "false");
        document.body.classList.remove("nav-open");
        toggle.focus();
      }
    });
  }

  document.querySelectorAll("[data-share-copy]").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var url = btn.getAttribute("data-share-url") || window.location.href;
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(url).then(function () {
          var prev = btn.textContent;
          btn.textContent = "Copied";
          setTimeout(function () {
            btn.textContent = prev;
          }, 2000);
        });
      }
    });
  });

  var article = document.querySelector(".article-body");
  var tocFold = document.getElementById("article-toc");
  var tocRail = document.getElementById("article-toc-rail");
  var tocRailWrap = document.getElementById("article-toc-rail-wrap");
  if (article && (tocFold || tocRail)) {
    var heads = article.querySelectorAll("h2[id]");
    if (heads.length >= 3) {
      function fillNav(nav) {
        if (!nav) return;
        var list = document.createElement("ol");
        heads.forEach(function (h) {
          var li = document.createElement("li");
          var a = document.createElement("a");
          a.href = "#" + h.id;
          a.textContent = h.textContent;
          li.appendChild(a);
          list.appendChild(li);
        });
        nav.appendChild(list);
        nav.hidden = false;
      }
      fillNav(tocFold);
      fillNav(tocRail);
      if (tocRailWrap) {
        tocRailWrap.hidden = false;
      }
      var fold = document.getElementById("article-toc-fold");
      if (fold) {
        fold.hidden = false;
      }
    }
  }
})();
