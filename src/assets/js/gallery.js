(() => {
  "use strict";

  const main = document.querySelector("main");
  if (!main || typeof HTMLDialogElement === "undefined") return;

  let activeItems = [];
  let activeIndex = 0;
  let opener = null;
  let scrollPosition = { x: 0, y: 0 };
  let previousBodyOverflow = "";

  const dialog = document.createElement("dialog");
  dialog.className = "lightbox";
  dialog.setAttribute("aria-label", "Prohlížeč fotografií");
  dialog.innerHTML = `
    <div class="lightbox__toolbar">
      <button class="lightbox__close" type="button" aria-label="Zavřít prohlížeč fotografií">Zavřít</button>
    </div>
    <div class="lightbox__content">
      <button class="lightbox__previous" type="button" aria-label="Předchozí fotografie">Předchozí</button>
      <figure class="lightbox__figure">
        <img class="lightbox__image" alt="">
        <figcaption class="lightbox__caption">
          <span class="lightbox__count" aria-live="polite"></span>
          <a class="lightbox__original" target="_blank" rel="noopener">Otevřít původní fotografii</a>
        </figcaption>
      </figure>
      <button class="lightbox__next" type="button" aria-label="Další fotografie">Další</button>
    </div>
    <p class="lightbox__error" role="alert" hidden>Fotografii se nepodařilo načíst. Můžete ji otevřít v původní velikosti.</p>
  `;
  document.body.append(dialog);

  const closeButton = dialog.querySelector(".lightbox__close");
  const previousButton = dialog.querySelector(".lightbox__previous");
  const nextButton = dialog.querySelector(".lightbox__next");
  const image = dialog.querySelector(".lightbox__image");
  const count = dialog.querySelector(".lightbox__count");
  const original = dialog.querySelector(".lightbox__original");
  const error = dialog.querySelector(".lightbox__error");

  const imageLinks = () => Array.from(main.querySelectorAll("a[href]")).filter((link) => link.querySelector("img"));

  const groupFor = (link) => {
    const galleryId = link.dataset.galleryId;
    if (!galleryId) return [link];

    return imageLinks().filter((candidate) => candidate.dataset.galleryId === galleryId);
  };

  const update = () => {
    const item = activeItems[activeIndex];
    const thumbnail = item.querySelector("img");
    const total = activeItems.length;

    previousButton.disabled = total < 2;
    nextButton.disabled = total < 2;
    count.textContent = total > 1 ? `Fotografie ${activeIndex + 1} z ${total}` : "Fotografie";
    original.href = item.href;
    image.alt = thumbnail ? thumbnail.alt : "Fotografie";
    error.hidden = true;
    dialog.classList.remove("lightbox--error");
    image.src = item.href;
  };

  const open = (link) => {
    activeItems = groupFor(link);
    activeIndex = activeItems.indexOf(link);
    opener = link;
    scrollPosition = { x: window.scrollX, y: window.scrollY };
    previousBodyOverflow = document.body.style.overflow;
    document.body.style.overflow = "hidden";
    update();
    dialog.showModal();
    closeButton.focus({ preventScroll: true });
  };

  const move = (direction) => {
    activeIndex = (activeIndex + direction + activeItems.length) % activeItems.length;
    update();
  };

  main.addEventListener("click", (event) => {
    const link = event.target.closest("a[href]");
    if (!link || !main.contains(link) || !link.querySelector("img")) return;
    if (event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
    if (typeof dialog.showModal !== "function") return;

    event.preventDefault();
    open(link);
  });

  closeButton.addEventListener("click", () => dialog.close());
  previousButton.addEventListener("click", () => move(-1));
  nextButton.addEventListener("click", () => move(1));

  dialog.addEventListener("keydown", (event) => {
    if (event.key === "Tab") {
      const controls = Array.from(dialog.querySelectorAll("button:not(:disabled), a[href]"))
        .filter((control) => control.getClientRects().length > 0);
      const first = controls[0];
      const last = controls[controls.length - 1];
      if (event.shiftKey && document.activeElement === first) {
        event.preventDefault();
        last.focus();
      } else if (!event.shiftKey && document.activeElement === last) {
        event.preventDefault();
        first.focus();
      }
    }
    if (event.key === "ArrowLeft" && activeItems.length > 1) {
      event.preventDefault();
      move(-1);
    }
    if (event.key === "ArrowRight" && activeItems.length > 1) {
      event.preventDefault();
      move(1);
    }
  });

  image.addEventListener("error", () => {
    dialog.classList.add("lightbox--error");
    error.hidden = false;
  });

  dialog.addEventListener("close", () => {
    document.body.style.overflow = previousBodyOverflow;
    const focusTarget = opener;
    const position = scrollPosition;
    requestAnimationFrame(() => {
      window.scrollTo(position.x, position.y);
      focusTarget?.focus({ preventScroll: true });
    });
  });
})();
