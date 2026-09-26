/**
 * Afsha's Henna — Mobile-First Interactive JS
 * Handles: Nav, Scroll effects, Scroll reveal, Count-up, Lightbox,
 *          Product/Design qty, WhatsApp ordering, Gallery filter
 */

/* ============================================================
   UTILITY
   ============================================================ */
const $ = (sel, ctx = document) => ctx.querySelector(sel);
const $$ = (sel, ctx = document) => [...ctx.querySelectorAll(sel)];
const WA_BASE = "https://wa.me/";

function getWaNumber(el) {
  return el?.dataset?.waNumber || el?.closest("[data-wa-number]")?.dataset?.waNumber || "";
}

function openWa(number, message) {
  if (!number) return;
  window.open(`${WA_BASE}${number}?text=${encodeURIComponent(message)}`, "_blank", "noopener");
}

/* ============================================================
   NAV — HAMBURGER / DRAWER / OVERLAY
   ============================================================ */
function initNav() {
  const menuBtn  = $("#menu-btn");
  const navLinks = $("#nav-links");
  const overlay  = $("#nav-overlay");
  const header   = $("#site-header");
  if (!menuBtn || !navLinks) return;

  function openNav() {
    navLinks.classList.add("open");
    overlay?.classList.add("visible");
    document.body.classList.add("nav-open");
    menuBtn.classList.add("active");
    menuBtn.setAttribute("aria-expanded", "true");
    menuBtn.setAttribute("aria-label", "Close navigation menu");
  }

  function closeNav() {
    navLinks.classList.remove("open");
    overlay?.classList.remove("visible");
    document.body.classList.remove("nav-open");
    menuBtn.classList.remove("active");
    menuBtn.setAttribute("aria-expanded", "false");
    menuBtn.setAttribute("aria-label", "Open navigation menu");
  }

  menuBtn.addEventListener("click", () =>
    navLinks.classList.contains("open") ? closeNav() : openNav()
  );

  overlay?.addEventListener("click", closeNav);

  // Close on nav link click (mobile & tablet UX)
  $$("a", navLinks).forEach(link => {
    link.addEventListener("click", () => {
      if (navLinks.classList.contains("open")) closeNav();
    });
  });

  // Escape key closes drawer
  document.addEventListener("keydown", e => {
    if (e.key === "Escape" && navLinks.classList.contains("open")) closeNav();
  });

  // Scroll-aware header shadow
  const onScroll = () => {
    header.classList.toggle("scrolled", window.scrollY > 20);
  };
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();
}

/* ============================================================
   SCROLL REVEAL (IntersectionObserver)
   ============================================================ */
function initScrollReveal() {
  if (!("IntersectionObserver" in window)) {
    // Fallback: just show everything
    $$(".reveal, .reveal-scale").forEach(el => el.classList.add("revealed"));
    return;
  }

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add("revealed");
          observer.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.12, rootMargin: "0px 0px -40px 0px" }
  );

  $$(".reveal, .reveal-scale").forEach(el => observer.observe(el));
}

/* ============================================================
   COUNT-UP ANIMATION
   ============================================================ */
function initCountUp() {
  const counters = $$(".count-up");
  if (!counters.length || !("IntersectionObserver" in window)) return;

  const easeOut = t => 1 - Math.pow(1 - t, 3);

  function animateCounter(el) {
    const raw    = el.dataset.target || el.textContent;
    const suffix = raw.replace(/[\d,]/g, "");        // e.g. "+", "%", " Yrs"
    const target = parseInt(raw.replace(/\D/g, ""), 10);
    if (isNaN(target)) return;

    const duration = 1400;
    const start    = performance.now();

    function tick(now) {
      const elapsed = now - start;
      const progress = Math.min(elapsed / duration, 1);
      const current  = Math.round(easeOut(progress) * target);
      el.textContent = current.toLocaleString("en-IN") + suffix;
      if (progress < 1) requestAnimationFrame(tick);
    }
    requestAnimationFrame(tick);
  }

  const observer = new IntersectionObserver(
    entries => entries.forEach(entry => {
      if (entry.isIntersecting) {
        animateCounter(entry.target);
        observer.unobserve(entry.target);
      }
    }),
    { threshold: 0.5 }
  );

  counters.forEach(el => {
    // Store original text as data-target if not already set
    if (!el.dataset.target) el.dataset.target = el.textContent.trim();
    observer.observe(el);
  });
}

/* ============================================================
   LIGHTBOX
   ============================================================ */
let lightboxImages = [];
let lightboxIndex  = 0;

function initLightbox() {
  const overlay    = $("#lightbox");
  if (!overlay) return;

  const img        = $("#lightbox-img");
  const title      = $("#lightbox-title");
  const cat        = $("#lightbox-cat");
  const orderBtn   = $("#lightbox-order-btn");
  const closeBtn   = $("#lightbox-close");
  const prevBtn    = $("#lightbox-prev");
  const nextBtn    = $("#lightbox-next");

  function buildIndex() {
    lightboxImages = $$(".design-image-wrap").map((wrap, i) => ({
      src:      $("img", wrap)?.src || "",
      alt:      $("img", wrap)?.alt || "",
      title:    wrap.closest(".design-card")?.dataset?.title || "",
      category: wrap.closest(".design-card")?.dataset?.category || "",
      price:    wrap.closest(".design-card")?.dataset?.price || "",
      waNumber: wrap.closest(".design-card")?.dataset?.waNumber || "",
    }));
  }

  function showLightbox(index) {
    buildIndex();
    if (!lightboxImages.length) return;
    lightboxIndex = ((index % lightboxImages.length) + lightboxImages.length) % lightboxImages.length;
    const item = lightboxImages[lightboxIndex];

    img.src = item.src;
    img.alt = item.alt;
    title.textContent = item.title;
    cat.textContent   = item.category;

    // Update order button
    orderBtn.onclick = () => {
      const priceStr = item.price
        ? `Approx. Price: ₹${parseFloat(item.price).toLocaleString("en-IN")}\n`
        : "";
      const msg = `Hello, I would like to book this henna design:\nDesign: ${item.title}\nCategory: ${item.category}\n${priceStr}Please confirm availability and appointment details.`;
      openWa(item.waNumber, msg);
    };

    overlay.classList.add("open");
    document.body.classList.add("nav-open"); // prevent bg scroll
    closeBtn.focus();

    // Show/hide nav buttons
    prevBtn.style.display = lightboxImages.length > 1 ? "flex" : "none";
    nextBtn.style.display = lightboxImages.length > 1 ? "flex" : "none";
  }

  function hideLightbox() {
    overlay.classList.remove("open");
    document.body.classList.remove("nav-open");
  }

  // Open on image wrap click
  document.addEventListener("click", e => {
    const wrap = e.target.closest(".design-image-wrap");
    if (!wrap) return;
    buildIndex();
    const index = $$(".design-image-wrap").indexOf(wrap);
    if (index >= 0) showLightbox(index);
  });

  closeBtn.addEventListener("click", hideLightbox);
  overlay.addEventListener("click", e => { if (e.target === overlay) hideLightbox(); });
  prevBtn.addEventListener("click", e => { e.stopPropagation(); showLightbox(lightboxIndex - 1); });
  nextBtn.addEventListener("click", e => { e.stopPropagation(); showLightbox(lightboxIndex + 1); });

  document.addEventListener("keydown", e => {
    if (!overlay.classList.contains("open")) return;
    if (e.key === "Escape")      hideLightbox();
    if (e.key === "ArrowLeft")   showLightbox(lightboxIndex - 1);
    if (e.key === "ArrowRight")  showLightbox(lightboxIndex + 1);
  });

  // Touch swipe in lightbox
  let touchStartX = 0;
  overlay.addEventListener("touchstart", e => { touchStartX = e.touches[0].clientX; }, { passive: true });
  overlay.addEventListener("touchend", e => {
    const dx = e.changedTouches[0].clientX - touchStartX;
    if (Math.abs(dx) > 50) {
      dx < 0 ? showLightbox(lightboxIndex + 1) : showLightbox(lightboxIndex - 1);
    }
  });
}

/* ============================================================
   PRODUCT QUANTITY & WHATSAPP ORDER
   ============================================================ */
function initProductCards() {
  $$(".product-card").forEach(card => {
    const minus      = $(".qty-btn.minus", card);
    const plus       = $(".qty-btn.plus", card);
    const qtyInput   = $(".qty-input", card);
    const totalEl    = $(".estimated-total-val", card);
    const orderBtn   = $(".btn-order-product", card);
    const unitPrice  = parseFloat(card.dataset.price || "0");
    const name       = card.dataset.name || "Henna Product";
    const waNum      = getWaNumber(card);

    function updateTotal() {
      let qty = Math.max(1, parseInt(qtyInput.value, 10) || 1);
      qtyInput.value = qty;
      if (totalEl) totalEl.textContent = "₹" + (qty * unitPrice).toLocaleString("en-IN");
      return qty;
    }

    minus?.addEventListener("click", () => {
      qtyInput.value = Math.max(1, (parseInt(qtyInput.value, 10) || 1) - 1);
      updateTotal();
    });
    plus?.addEventListener("click", () => {
      qtyInput.value = (parseInt(qtyInput.value, 10) || 1) + 1;
      updateTotal();
    });
    qtyInput?.addEventListener("input", updateTotal);

    orderBtn?.addEventListener("click", e => {
      e.preventDefault();
      const qty   = updateTotal();
      const total = qty * unitPrice;
      const msg =
`Hello, I would like to order:
Product: ${name}
Quantity: ${qty}
Price per item: ₹${unitPrice.toLocaleString("en-IN")}
Estimated total: ₹${total.toLocaleString("en-IN")}
Please confirm availability and delivery details.`;
      openWa(waNum, msg);
    });
  });
}

/* ============================================================
   DESIGN QUANTITY & WHATSAPP BOOKING
   ============================================================ */
function initDesignCards() {
  $$(".design-card").forEach(card => {
    const minus    = $(".design-qty-btn.minus", card);
    const plus     = $(".design-qty-btn.plus", card);
    const qtyInput = $(".design-qty-input", card);
    const orderBtn = $(".btn-order-design", card);
    const title    = card.dataset.title    || "Henna Design";
    const category = card.dataset.category || "Henna Art";
    const price    = card.dataset.price;
    const waNum    = getWaNumber(card);

    function getQty() {
      let q = parseInt(qtyInput?.value, 10) || 1;
      if (q < 1) { q = 1; if (qtyInput) qtyInput.value = 1; }
      return q;
    }

    minus?.addEventListener("click", () => {
      if (qtyInput) qtyInput.value = Math.max(1, getQty() - 1);
    });
    plus?.addEventListener("click", () => {
      if (qtyInput) qtyInput.value = getQty() + 1;
    });

    orderBtn?.addEventListener("click", e => {
      e.preventDefault();
      const qty      = getQty();
      const priceStr = price ? `Approx. Price: ₹${parseFloat(price).toLocaleString("en-IN")}\n` : "";
      const msg =
`Hello, I would like to book:
Design: ${title}
Category: ${category}
Quantity / Persons: ${qty}
${priceStr}Please confirm availability and appointment details.`;
      openWa(waNum, msg);
    });
  });
}

/* ============================================================
   GALLERY CATEGORY FILTER (CLIENT-SIDE)
   ============================================================ */
function initGalleryFilter() {
  const filterBtns = $$(".filter-btn");
  const cards      = $$(".gallery-grid .design-card");
  if (!filterBtns.length || !cards.length) return;

  filterBtns.forEach(btn => {
    btn.addEventListener("click", function (e) {
      e.preventDefault();

      filterBtns.forEach(b => b.classList.remove("active"));
      this.classList.add("active");

      const target = this.dataset.filter;

      cards.forEach(card => {
        const match = target === "all" || card.dataset.categorySlug === target;
        if (match) {
          card.style.display = "";
          requestAnimationFrame(() => {
            card.style.opacity  = "1";
            card.style.transform = "translateY(0)";
          });
        } else {
          card.style.opacity  = "0";
          card.style.transform = "translateY(14px)";
          setTimeout(() => { if (card.style.opacity === "0") card.style.display = "none"; }, 260);
        }
      });
    });
  });
}

/* ============================================================
   ADD REVEAL CLASSES TO KEY ELEMENTS (progressive enhancement)
   ============================================================ */
function tagRevealElements() {
  // Sections to reveal on scroll
  const sectionSelectors = [
    ".hero-badge",
    ".hero-title",
    ".hero-description",
    ".hero-actions",
    ".hero-stats-strip",
    ".flow-step-card",
    ".trust-card",
    ".design-card",
    ".product-card",
    ".value-box",
    ".custom-inquiry-banner",
    ".cta-inner",
    ".about-img-frame",
    ".about-info-column > *",
  ];

  sectionSelectors.forEach((sel, sectionIdx) => {
    $$(sel).forEach((el, i) => {
      if (!el.classList.contains("reveal") && !el.classList.contains("reveal-scale")) {
        el.classList.add("reveal");
        // Stagger within groups
        const d = i % 4;
        if (d) el.classList.add(`reveal-d${d}`);
      }
    });
  });

  // Count-up: tag stat numbers
  $$(".stat-num, .stat-highlight").forEach(el => {
    if (!el.classList.contains("count-up")) {
      el.classList.add("count-up");
    }
  });

  // Add tap overlay to design image wraps (gallery lightbox hint)
  $$(".design-image-wrap").forEach(wrap => {
    if (!$(".tap-overlay", wrap)) {
      const overlay = document.createElement("div");
      overlay.className = "tap-overlay";
      overlay.innerHTML = `<span class="tap-overlay-label">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor"><path d="M15.5 14h-.79l-.28-.27A6.471 6.471 0 0 0 16 9.5 6.5 6.5 0 1 0 9.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z"/></svg>
        View Design</span>`;
      wrap.appendChild(overlay);
    }
  });
}

/* ============================================================
   MAIN INIT
   ============================================================ */
document.addEventListener("DOMContentLoaded", () => {
  // Tag elements before observing
  tagRevealElements();

  // Core features
  initNav();
  initScrollReveal();
  initCountUp();
  initLightbox();
  initProductCards();
  initDesignCards();
  initGalleryFilter();
});
