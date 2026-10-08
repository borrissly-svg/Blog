(() => {
  const link = document.createElement("a");
  link.className = "whatsapp-float";
  link.href = "https://wa.me/447552486027?text=Hello%20Ethical%20Zenith%20Hackers%20Intelligence";
  link.target = "_blank";
  link.rel = "noopener noreferrer";
  link.setAttribute("aria-label", "Chat with us on WhatsApp");
  link.title = "Chat with us on WhatsApp";
  link.innerHTML = '<span class="wa-icon" aria-hidden="true"><svg viewBox="0 0 32 32" role="img"><path fill="currentColor" d="M19.11 17.21c-.27-.14-1.59-.78-1.84-.87-.25-.09-.43-.14-.61.14-.18.27-.7.87-.86 1.05-.16.18-.32.2-.59.07-.27-.14-1.13-.42-2.15-1.33-.79-.7-1.32-1.56-1.48-1.83-.16-.27-.02-.42.12-.56.12-.12.27-.32.41-.48.14-.16.18-.27.27-.45.09-.18.05-.34-.02-.48-.07-.14-.61-1.47-.84-2.02-.22-.53-.45-.46-.61-.47h-.52c-.18 0-.48.07-.73.34-.25.27-.95.93-.95 2.27 0 1.34.98 2.63 1.11 2.81.14.18 1.93 2.95 4.68 4.14.65.28 1.16.45 1.55.57.65.21 1.24.18 1.71.11.52-.08 1.59-.65 1.82-1.28.23-.63.23-1.17.16-1.28-.07-.11-.25-.18-.52-.32z"/><path fill="currentColor" d="M16.03 3.2c-7.08 0-12.83 5.75-12.83 12.83 0 2.26.59 4.46 1.71 6.4L3.1 28.8l6.52-1.71a12.76 12.76 0 0 0 6.4 1.72h.01c7.07 0 12.82-5.76 12.82-12.83S23.1 3.2 16.03 3.2zm0 23.48h-.01a10.61 10.61 0 0 1-5.41-1.48l-.39-.23-3.87 1.01 1.03-3.77-.25-.39a10.65 10.65 0 1 1 8.9 4.86z"/></svg></span><span class="wa-label">WhatsApp</span>';
  const style = document.createElement("style");
  style.textContent = `
    .whatsapp-float {
      position: fixed;
      bottom: 20px;
      left: 18px;
      z-index: 2147483647;
      display: flex;
      align-items: center;
      gap: 8px;
      padding: 10px 15px 10px 11px;
      border-radius: 999px;
      background: #25D366;
      color: #fff !important;
      text-decoration: none !important;
      font: 800 14px/1 Arial, sans-serif;
      box-shadow: 0 8px 28px rgba(0,0,0,.35), 0 0 22px rgba(37,211,102,.25);
      transition: transform .2s ease, box-shadow .2s ease;
    }
    .whatsapp-float:hover {
      transform: translateY(-2px) scale(1.03);
      box-shadow: 0 11px 34px rgba(0,0,0,.4), 0 0 30px rgba(37,211,102,.38);
    }
    .wa-icon { width: 24px; height: 24px; display: grid; place-items: center; }
    .wa-icon svg { width: 24px; height: 24px; }
    @media (max-width: 600px) {
      .whatsapp-float { bottom: 14px; left: 12px; padding: 9px 11px; }
      .wa-label { display: none; }
      .wa-icon, .wa-icon svg { width: 27px; height: 27px; }
    }
  `;
  document.head.appendChild(style);
  document.body.appendChild(link);
})();