// Supabase browser configuration for Ethical Zenith Hackers Intelligence Blog.
// This file contains only the public/publishable key. Never put a service-role/secret key here.
window.SUPABASE_CONFIG = {
  url: "https://zehcbzpewiwmiwmvrotn.supabase.co",
  publishableKey: "sb_publishable_Y03QGuQGJC8b4auZXw1Luw_oHzwhjMo"
};

// Give every article a polished, immersive cybersecurity background.
if (location.pathname.includes("/articles/")) {
  const style = document.createElement("style");
  style.textContent = `
    html { background: #020812; }
    body {
      position: relative;
      min-height: 100vh;
      background:
        linear-gradient(180deg, rgba(2,8,18,.58), rgba(2,12,24,.88)),
        radial-gradient(circle at 15% 15%, rgba(0,220,255,.18), transparent 32%),
        radial-gradient(circle at 85% 80%, rgba(70,90,255,.16), transparent 34%),
        url("https://borrissly-svg.github.io/Blog/hero-blog.png") center center / cover fixed no-repeat !important;
      overflow-x: hidden;
    }
    body::before {
      content: "";
      position: fixed;
      inset: 0;
      pointer-events: none;
      z-index: 0;
      background:
        linear-gradient(115deg, transparent 0%, rgba(85,234,255,.045) 48%, transparent 52%),
        radial-gradient(circle at 50% 0%, rgba(85,234,255,.10), transparent 42%);
      animation: ezGlow 10s ease-in-out infinite alternate;
    }
    main {
      position: relative;
      z-index: 1;
    }
    main > a {
      display: inline-block;
      margin-bottom: 18px;
      padding: 9px 15px;
      border: 1px solid rgba(85,234,255,.28);
      border-radius: 999px;
      background: rgba(4,18,31,.62);
      backdrop-filter: blur(10px);
      text-decoration: none;
      box-shadow: 0 8px 30px rgba(0,0,0,.22);
    }
    article {
      background: linear-gradient(145deg, rgba(7,25,42,.90), rgba(5,17,30,.84)) !important;
      border: 1px solid rgba(85,234,255,.30) !important;
      box-shadow:
        0 24px 70px rgba(0,0,0,.45),
        0 0 45px rgba(0,210,255,.08);
      backdrop-filter: blur(14px);
    }
    .comments {
      background: rgba(3,16,28,.78) !important;
      backdrop-filter: blur(12px);
    }
    @keyframes ezGlow {
      from { opacity: .65; transform: scale(1); }
      to { opacity: 1; transform: scale(1.015); }
    }
    @media (max-width: 700px) {
      body { background-attachment: scroll !important; }
      article { backdrop-filter: blur(8px); }
    }
  `;
  document.head.appendChild(style);
}
