// Ethical Zenith visitor chat: Tawk.to live chat + lightweight FAQ assistant.
// The FAQ helper works without an API key. For open-ended AI answers, enable Tawk.to AI Assist in the dashboard.
var Tawk_API = window.Tawk_API || {};
var Tawk_LoadStart = new Date();
(function () {
  var s1 = document.createElement("script");
  var s0 = document.getElementsByTagName("script")[0];
  s1.async = true;
  s1.src = "https://embed.tawk.to/6ac7f89bb255d834c35d1a33/default";
  s1.charset = "UTF-8";
  s1.setAttribute("crossorigin", "*");
  s0.parentNode.insertBefore(s1, s0);
})();

(function () {
  if (window.__zenithChatInstalled) return;
  window.__zenithChatInstalled = true;

  const style = document.createElement("style");
  style.textContent = `
    #zenith-chat-launcher{position:fixed;right:20px;bottom:88px;z-index:2147483000;border:1px solid #63edff;border-radius:999px;background:linear-gradient(135deg,#11e6ff,#00a8d0);color:#00121c;padding:13px 18px;font:800 14px/1.2 Arial,sans-serif;box-shadow:0 10px 30px #0006;cursor:pointer}
    #zenith-chat-panel{position:fixed;right:20px;bottom:145px;z-index:2147483000;width:min(365px,calc(100vw - 28px));height:min(520px,calc(100vh - 180px));display:none;flex-direction:column;overflow:hidden;border:1px solid rgba(17,230,255,.55);border-radius:18px;background:#071a2a;color:#f3fbff;box-shadow:0 20px 70px #0009;font:14px/1.5 Arial,sans-serif}
    #zenith-chat-panel.open{display:flex}
    .zc-head{display:flex;align-items:center;justify-content:space-between;gap:10px;padding:15px;background:linear-gradient(120deg,#0d3c55,#092235);border-bottom:1px solid #1a6177}
    .zc-title{font-weight:800}.zc-sub{font-size:11px;color:#9fefff}.zc-close{border:0;background:transparent;color:#fff;font-size:23px;cursor:pointer}
    .zc-messages{flex:1;overflow:auto;padding:14px;display:flex;flex-direction:column;gap:10px}
    .zc-msg{max-width:92%;padding:10px 12px;border-radius:13px;white-space:pre-wrap;overflow-wrap:anywhere}
    .zc-bot{align-self:flex-start;background:#12364a;border:1px solid #24576d}.zc-user{align-self:flex-end;background:#0aa7c4;color:#00121c}
    .zc-actions{display:flex;flex-wrap:wrap;gap:7px;padding:0 12px 12px}
    .zc-action{border:1px solid #20cce6;border-radius:999px;background:#0a2a3d;color:#baf7ff;padding:8px 10px;font:700 12px Arial,sans-serif;cursor:pointer}
    .zc-form{display:flex;gap:8px;padding:12px;border-top:1px solid #21475b;background:#061522}
    .zc-input{flex:1;min-width:0;border:1px solid #31586b;border-radius:10px;background:#0b2536;color:white;padding:11px;font:14px Arial,sans-serif;outline:none}
    .zc-send{border:0;border-radius:10px;background:#11e6ff;color:#00121c;padding:0 13px;font-weight:800;cursor:pointer}
    @media(max-width:480px){#zenith-chat-launcher{right:12px;bottom:78px}#zenith-chat-panel{right:10px;bottom:132px;height:min(520px,calc(100vh - 155px))}}
  `;
  document.head.appendChild(style);

  const launcher = document.createElement("button");
  launcher.id = "zenith-chat-launcher";
  launcher.type = "button";
  launcher.setAttribute("aria-expanded", "false");
  launcher.textContent = "✦ Chat with Zenith";
  const panel = document.createElement("section");
  panel.id = "zenith-chat-panel";
  panel.setAttribute("aria-label", "Ethical Zenith visitor assistant");
  panel.innerHTML = `
    <div class="zc-head"><div><div class="zc-title">Zenith Visitor Assistant</div><div class="zc-sub">Quick answers · Case submissions · Agent support</div></div><button class="zc-close" type="button" aria-label="Close chat">×</button></div>
    <div class="zc-messages" role="log" aria-live="polite"></div>
    <div class="zc-actions">
      <button class="zc-action" data-action="services">Our services</button>
      <button class="zc-action" data-action="case">Submit a case</button>
      <button class="zc-action" data-action="agent">Speak with an agent</button>
      <button class="zc-action" data-action="safety">Safety tips</button>
    </div>
    <form class="zc-form"><input class="zc-input" aria-label="Ask a question" maxlength="700" placeholder="Type your question…" required><button class="zc-send" type="submit">Send</button></form>
  `;
  document.body.appendChild(launcher);
  document.body.appendChild(panel);

  const messages = panel.querySelector(".zc-messages");
  const input = panel.querySelector(".zc-input");
  function addMessage(text, who) {
    const el = document.createElement("div");
    el.className = "zc-msg " + (who === "user" ? "zc-user" : "zc-bot");
    el.textContent = text;
    messages.appendChild(el);
    messages.scrollTop = messages.scrollHeight;
  }
  function openPanel() {
    panel.classList.add("open");
    launcher.setAttribute("aria-expanded", "true");
    if (!messages.dataset.welcomed) {
      addMessage("Hello! I can help with common questions about this blog, cybersecurity education, digital-asset investigations, OSINT, and contacting our team. Choose an option or type a question. For questions I cannot answer reliably, I’ll direct you to an agent.", "bot");
      messages.dataset.welcomed = "1";
    }
    input.focus();
  }
  function closePanel() { panel.classList.remove("open"); launcher.setAttribute("aria-expanded", "false"); }
  function speakToAgent() {
    addMessage("Opening live chat. If an agent is offline, leave a message in the chat or use the contact form.", "bot");
    try {
      if (window.Tawk_API && typeof window.Tawk_API.maximize === "function") {
        if (typeof window.Tawk_API.showWidget === "function") window.Tawk_API.showWidget();
        window.Tawk_API.maximize();
        return;
      }
    } catch (e) {}
    window.open("https://tawk.to/chat/6ac7f89bb255d834c35d1a33/default", "_blank", "noopener");
  }
  function submitCase() {
    window.location.href = new URL("/contact.html?type=case", window.location.origin).href;
  }
  function reply(raw) {
    const q = raw.toLowerCase();
    if (/\b(hello|hi|hey|good morning|good afternoon)\b/.test(q)) return "Hello! What would you like help with today? You can ask about our content, choose Submit a case, or connect with a live agent.";
    if (/\b(service|services|what do you do|what can you do|offerings)\b/.test(q)) return "This site publishes educational content about cybersecurity, OSINT, digital-asset and blockchain awareness, investigations, identity protection, and risk/compliance. For a specific service request, please speak with an agent or submit an inquiry.";
    if (/\b(case|submit|report|stolen|scam|lost funds|investigation request)\b/.test(q)) return "To submit a case or inquiry, use our contact form. Include a clear summary and any non-sensitive reference details. Never submit passwords, private keys, seed/recovery phrases, authentication codes, or full payment-card details.";
    if (/\b(agent|human|person|representative|talk to someone|contact|support)\b/.test(q)) return "You can connect to live chat using “Speak with an agent”, or send a message through our contact form at support@zenithhackers.com.";
    if (/\b(crypto|cryptocurrency|blockchain|wallet|transaction|txid)\b/.test(q)) return "For a digital-asset inquiry, preserve transaction hashes, wallet addresses, platform names, timestamps, receipts, and communications. Never share your private key or recovery phrase. Use the contact form to describe the situation and request a follow-up.";
    if (/\b(osint|open source intelligence)\b/.test(q)) return "OSINT is the collection and evaluation of relevant publicly available information. Responsible work verifies sources, records context, protects privacy, and avoids conclusions that the evidence does not support. Browse our OSINT articles for more.";
    if (/\b(security|cybersecurity|hack|hacked|phishing|account compromised|malware)\b/.test(q)) return "For an account or security incident, use a trusted device to change compromised passwords, enable multi-factor authentication, contact the affected provider, and preserve evidence. If there is immediate financial risk, contact your bank or platform directly. Do not share credentials here.";
    if (/\b(price|cost|fee|guarantee|guaranteed recovery|recover funds|recovery)\b/.test(q)) return "I can’t confirm pricing, outcomes, or guarantee recovery through this automated helper. Please request a written response from an agent. Be cautious of anyone guaranteeing recovered funds or asking for seed phrases, private keys, or upfront payments to unlock funds.";
    if (/\b(privacy|data|personal information)\b/.test(q)) return "Please share only the information needed to explain your question. Do not enter passwords, authentication codes, private keys, seed phrases, or payment-card details. You can read our Privacy Policy from the website footer.";
    return "I’m not confident I can answer that accurately from the site’s published FAQ. Please choose “Speak with an agent” for a human response, or submit your question through the contact form. This basic helper does not have general-purpose AI enabled yet.";
  }
  launcher.addEventListener("click", () => panel.classList.contains("open") ? closePanel() : openPanel());
  panel.querySelector(".zc-close").addEventListener("click", closePanel);
  panel.querySelectorAll("[data-action]").forEach(btn => btn.addEventListener("click", () => {
    const action = btn.dataset.action;
    if (action === "agent") { speakToAgent(); return; }
    if (action === "case") { submitCase(); return; }
    if (action === "services") addMessage("Our publication covers cybersecurity education, OSINT, digital-asset and blockchain awareness, identity protection, investigations, and risk/compliance. For a specific request, speak with an agent.", "bot");
    if (action === "safety") addMessage("Never send passwords, authentication codes, private keys, seed/recovery phrases, or full card details. Be cautious of guaranteed recovery claims. Preserve evidence and contact the relevant bank or platform directly if money or an account is at risk.", "bot");
  }));
  panel.querySelector(".zc-form").addEventListener("submit", event => {
    event.preventDefault();
    const question = input.value.trim();
    if (!question) return;
    addMessage(question, "user");
    input.value = "";
    addMessage(reply(question), "bot");
  });
})();
