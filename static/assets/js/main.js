(function () {
  "use strict";

  const body = document.body;
  const header = document.getElementById("site-header");
  const navToggle = document.querySelector(".mobile-nav-toggle");
  const navLinks = document.querySelectorAll(".site-nav a");
  const scrollTop = document.querySelector(".scroll-top");
  const progressBar = document.querySelector("[data-reading-progress] span");
  const revealItems = document.querySelectorAll(".reveal");
  const filterButtons = document.querySelectorAll("[data-filter-group] [data-filter]");
  const filterCards = document.querySelectorAll("[data-filter-targets] [data-category]");

  function updateHeaderState() {
    if (!header) {
      return;
    }

    const isScrolled = window.scrollY > 18;
    header.classList.toggle("is-scrolled", isScrolled);
    document.documentElement.style.setProperty("--header-height", `${header.offsetHeight}px`);
  }

  function closeNav() {
    body.classList.remove("nav-open");
    if (navToggle) {
      navToggle.setAttribute("aria-expanded", "false");
    }
  }

  if (navToggle) {
    navToggle.addEventListener("click", function () {
      const willOpen = !body.classList.contains("nav-open");
      body.classList.toggle("nav-open", willOpen);
      navToggle.setAttribute("aria-expanded", String(willOpen));
    });
  }

  navLinks.forEach(function (link) {
    link.addEventListener("click", closeNav);
  });

  function updateScrollTop() {
    if (!scrollTop) {
      return;
    }

    scrollTop.classList.toggle("is-visible", window.scrollY > 320);
  }

  if (scrollTop) {
    scrollTop.addEventListener("click", function (event) {
      event.preventDefault();
      window.scrollTo({ top: 0, behavior: "smooth" });
    });
  }

  function updateReadingProgress() {
    if (!progressBar) {
      return;
    }

    const article = document.querySelector("[data-article-body]");
    if (!article) {
      progressBar.style.width = "0%";
      return;
    }

    const articleRect = article.getBoundingClientRect();
    const articleTop = window.scrollY + articleRect.top;
    const articleHeight = article.offsetHeight;
    const viewportHeight = window.innerHeight;
    const maxScroll = Math.max(articleHeight - viewportHeight, 1);
    const currentScroll = Math.min(Math.max(window.scrollY - articleTop, 0), maxScroll);
    const progress = (currentScroll / maxScroll) * 100;

    progressBar.style.width = `${progress}%`;
  }

  if ("IntersectionObserver" in window) {
    const revealObserver = new IntersectionObserver(
      function (entries, observer) {
        entries.forEach(function (entry) {
          if (!entry.isIntersecting) {
            return;
          }

          entry.target.classList.add("is-visible");
          observer.unobserve(entry.target);
        });
      },
      {
        threshold: 0.12,
        rootMargin: "0px 0px -8% 0px",
      }
    );

    revealItems.forEach(function (item) {
      revealObserver.observe(item);
    });
  } else {
    revealItems.forEach(function (item) {
      item.classList.add("is-visible");
    });
  }

  filterButtons.forEach(function (button) {
    button.addEventListener("click", function () {
      const selectedFilter = button.dataset.filter;

      filterButtons.forEach(function (chip) {
        chip.classList.toggle("is-active", chip === button);
      });

      filterCards.forEach(function (card) {
        const shouldShow = selectedFilter === "all" || card.dataset.category === selectedFilter;
        card.classList.toggle("is-hidden", !shouldShow);
      });
    });
  });

  window.addEventListener("scroll", function () {
    updateHeaderState();
    updateScrollTop();
    updateReadingProgress();
  });

  window.addEventListener("resize", updateHeaderState);
  window.addEventListener("load", function () {
    updateHeaderState();
    updateScrollTop();
    updateReadingProgress();
  });

  document.addEventListener("click", function (event) {
    const navPanel = document.querySelector("[data-nav-panel]");
    if (!body.classList.contains("nav-open") || !navPanel || !navToggle) {
      return;
    }

    if (!navPanel.contains(event.target) && !navToggle.contains(event.target)) {
      closeNav();
    }
  });
})();
