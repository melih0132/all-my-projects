const images = document.querySelectorAll(".lightbox");
const body = document.body;

images.forEach(img => {
  img.addEventListener("click", function () {
    openLightbox(img.src, img.alt);
  });
});

function openLightbox(src, altText) {
  const bg = document.createElement("div");
  bg.id = "bg";

  const lightbox = document.createElement("div");
  lightbox.id = "lightbox";

  const img = document.createElement("img");
  img.src = src;
  img.alt = altText;

  const description = document.createElement('p');
  description.textContent = altText;

  const closeBtn = document.createElement("button");
  closeBtn.id = "close-btn";
  closeBtn.innerHTML = "X";

  lightbox.appendChild(img);
  lightbox.appendChild(description);
  lightbox.appendChild(closeBtn);
  bg.appendChild(lightbox);
  body.appendChild(bg);

  body.style.overflow = "hidden";

  closeBtn.addEventListener("click", closeLightbox);
  document.addEventListener("keyup", function (e) {
    if (e.key === "Escape") {
      closeLightbox();
    }
  });

  centerLightbox();

  function closeLightbox() {
    bg.remove();
    body.style.overflow = "visible";
  }

  function centerLightbox() {
    lightbox.style.top = '50%';
    lightbox.style.left = '50%';
    lightbox.style.transform = 'translate(-50%, -50%)';
  }
}