(() => {
  const menu = document.getElementById("nav");
  const toggle = document.getElementById("menuToggle");
  toggle?.addEventListener("click", () => {
    const open = menu.classList.toggle("open");
    toggle.setAttribute("aria-expanded", String(open));
  });
  menu?.querySelectorAll("a").forEach(link => link.addEventListener("click", () => {
    menu.classList.remove("open");
    toggle?.setAttribute("aria-expanded", "false");
  }));

  document.getElementById("year").textContent = new Date().getFullYear();

  // Gentle pointer parallax on the CSS-built turbine; reduced-motion users get a static scene.
  const stage = document.querySelector(".engine-stage");
  const core = document.querySelector(".engine-core");
  if (stage && core && !window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
    stage.addEventListener("pointermove", event => {
      const rect = stage.getBoundingClientRect();
      const x = (event.clientX - rect.left) / rect.width - 0.5;
      const y = (event.clientY - rect.top) / rect.height - 0.5;
      core.style.transform = `rotateX(${9 - y * 9}deg) rotateY(${-15 + x * 12}deg)`;
    });
    stage.addEventListener("pointerleave", () => core.style.transform = "");
  }

  const form = document.getElementById("contactForm");
  const status = document.getElementById("formStatus");
  form?.addEventListener("submit", async event => {
    event.preventDefault();
    status.textContent = "Sending your message…";
    status.classList.remove("error");
    const button = form.querySelector("button[type=submit]");
    button.disabled = true;
    try {
      const data = Object.fromEntries(new FormData(form).entries());
      const csrf = form.querySelector("[name=csrfmiddlewaretoken]")?.value;
      const response = await fetch(window.PORTFOLIO_API.contact, {
        method: "POST",
        headers: {"Content-Type": "application/json", "X-CSRFToken": csrf || ""},
        credentials: "same-origin",
        body: JSON.stringify(data)
      });
      const result = await response.json();
      if (!response.ok || !result.ok) throw new Error(result.error || "Unable to send your message.");
      status.textContent = result.message;
      form.reset();
    } catch (error) {
      status.textContent = error.message || "Something went wrong. Please email me directly.";
      status.classList.add("error");
    } finally {
      button.disabled = false;
    }
  });
})();
