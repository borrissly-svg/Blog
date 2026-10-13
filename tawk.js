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
    <div class="zc-head"><div><div class="zc-title">Zenith Visitor Assistant</div><div class="zc-sub">Service guidance · Quotes · Agent follow-up</div></div><button class="zc-close" type="button" aria-label="Close chat">×</button></div>
    <div class="zc-messages" role="log" aria-live="polite"></div>
    <div class="zc-actions">
      <button class="zc-action" data-action="services">Our services</button>
      <button class="zc-action" data-action="case">Start an inquiry</button>\n      <button class="zc-action" data-action="quote">Request a quote</button>
      <button class="zc-action" data-action="agent">Speak with an agent</button>
      <button class="zc-action" data-action="safety">Safety tips</button>
    </div>
    <form class="zc-form"><input class="zc-input" aria-label="Ask a question" maxlength="700" placeholder="Type your question…" required><button class="zc-send" type="submit">Send</button></form>
  `;
  document.body.appendChild(launcher);
  document.body.appendChild(panel);

  const messages = panel.querySelector(".zc-messages");
  const input = panel.querySelector(".zc-input");
  const fields = { name: "", email: "", phone: "", company: "", service: "", details: "", quote: false };
  const requiredFields = ["name", "email", "phone", "company"];
  const fieldPrompts = {
    name: "May I have your name so we know who we’re assisting?",
    email: "What email address should we use to follow up with details or a quote?",
    phone: "Is there a phone number where our team can reach you if needed?",
    company: "What company or organization are you contacting us on behalf of?"
  };
  const serviceOptions = [
    "Vulnerability Assessment & Penetration Testing",
    "Web Application Security",
    "Network & Endpoint Testing",
    "Social Engineering & Configuration Reviews",
    "Forensics & Incident Response",
    "Threat Modeling & Consulting",
    "Lawful asset / crypto tracing",
    "General question"
  ];
  let stage = "welcome";
  let leadIntent = "support";
  let lastReply = "";
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
      addMessage("Hello, welcome to Zenith Hackers Intelligence. We can help with authorized cybersecurity, ethical hacking, forensics, incident response, threat modeling, remediation, verification, and lawful asset or crypto tracing. What can we help you with today?", "bot");
      messages.dataset.welcomed = "1";
    }
    input.focus();
  }
  function closePanel() { panel.classList.remove("open"); launcher.setAttribute("aria-expanded", "false"); }
  function nextMissingField() {
    return requiredFields.find(key => !fields[key]) || "";
  }
  function requestLeadDetails(intent) {
    leadIntent = intent || "support";
    const missing = nextMissingField();
    stage = missing ? "lead:" + missing : "lead:service";
    const prompt = missing ? fieldPrompts[missing] : "Which service best matches your request? You can name more than one.";
    addMessage(prompt, "bot");
  }
  function serviceSummary() {
    return "Which service best matches your request? You can name more than one: " + serviceOptions.join("; ") + ".";
  }
  function safeLeadSummary() {
    return [
      "New website chat inquiry for Zenith Hackers Intelligence",
      "Request type: " + leadIntent,
      "Name: " + fields.name,
      "Email: " + fields.email,
      "Phone: " + fields.phone,
      "Company: " + fields.company,
      "Service: " + (fields.service || "Not specified"),
      "Details: " + (fields.details || "Not provided")
    ].join("\n");
  }
  function contactUrl() {
    const u = new URL("/contact.html", window.location.origin);
    u.searchParams.set("type", leadIntent === "quote" ? "quote" : "case");
    u.searchParams.set("name", fields.name);
    u.searchParams.set("email", fields.email);
    u.searchParams.set("phone", fields.phone);
    u.searchParams.set("company", fields.company);
    u.searchParams.set("service", fields.service);
    u.searchParams.set("summary", fields.details);
    return u.href;
  }
  function finishLead() {
    stage = "done";
    addMessage("Thank you. We’ve captured the details you shared in this chat. Please use the contact form to send them to our team; a team member can review your request and follow up. We cannot promise a quote, tracing result, or recovery outcome before assessment.", "bot");
    addMessage("Open the contact form: " + contactUrl(), "bot");
    const link = document.createElement("a");
    link.href = contactUrl();
    link.textContent = "Continue to secure inquiry form";
    link.target = "_self";
    link.style.cssText = "color:#63edff;padding:0 14px 12px;overflow-wrap:anywhere";
    panel.appendChild(link);
    const copy = document.createElement("button");
    copy.type = "button";
    copy.className = "zc-action";
    copy.textContent = "Copy inquiry summary";
    copy.style.margin = "0 12px 12px";
    copy.addEventListener("click", () => {
      const blob = safeLeadSummary();
      if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(blob).then(() => addMessage("Inquiry summary copied. Please paste it into the contact form.", "bot")).catch(() => addMessage(blob, "bot"));
      else addMessage(blob, "bot");
    });
    panel.appendChild(copy);
  }
  function speakToAgent() {
    addMessage("We’ll try to open our live-agent chat. If no agent is available, please leave a message in Tawk.to or use our contact form.", "bot");
    try {
      if (window.Tawk_API && typeof window.Tawk_API.maximize === "function") {
        if (typeof window.Tawk_API.showWidget === "function") window.Tawk_API.showWidget();
        window.Tawk_API.maximize();
        return;
      }
    } catch (e) {}
    window.open("https://tawk.to/chat/6ac7f89bb255d834c35d1a33/default", "_blank", "noopener");
  }
  function submitCase() { requestLeadDetails("case"); }
  function classify(raw) {
    const q = raw.toLowerCase();
    if (/\\b(quote|quotation|estimate|pricing|price|cost|how much|fee|fees)\\b/.test(q)) return {type:"quote",text:"We can capture a quote request. Final pricing depends on the authorized scope, complexity, and evidence available; our team must assess it before confirming a quote."};
    if (/\\b(vulnerability|penetration|pentest|web application|network|endpoint|social engineering|configuration review|forensics|incident response|threat model|consulting|crypto|cryptocurrency|asset tracing|blockchain)\\b/.test(q)) return {type:"service",text:"We can help route requests for authorized cybersecurity and lawful investigations. We work to a defined scope and lawful authorization, use evidence-based methods, and cannot guarantee tracing or recovery outcomes."};
    return {type:"support",text:"We’ll do our best to help with information about our services and responsible next steps. I can’t verify every case-specific claim in this automated chat, so I’ll offer a team follow-up when needed."};
  }
  function answer(raw) {
    const q = raw.toLowerCase();
    if (/\\b(hello|hi|hey|good morning|good afternoon|good evening)\\b/.test(q)) return "Hello, welcome to Zenith Hackers Intelligence. What can we help you with today?";
    if (/\\b(service|services|what do you do|what can you do|offerings)\\b/.test(q)) return "Our services include Vulnerability Assessment & Penetration Testing; Web Application Security; Network & Endpoint Testing; Social Engineering & Configuration Reviews; Forensics & Incident Response; and Threat Modeling & Consulting. We also discuss lawful asset and crypto tracing. All work requires appropriate authorization and a defined scope.";
    if (/\\b(authori[sz]ation|permission|legal|lawful|scope)\\b/.test(q)) return "We only support work that has appropriate lawful authorization and a clearly defined scope. We do not assist with unauthorized access, credential theft, evading security controls, or invading someone’s privacy.";
    if (/\\b(crypto|cryptocurrency|blockchain|wallet|transaction|txid|asset tracing)\\b/.test(q)) return "For lawful asset or crypto tracing, preserve transaction hashes, wallet addresses, timestamps, platform names, receipts, and relevant communications. Never share private keys, seed/recovery phrases, passwords, or authentication codes. A trace does not guarantee funds can be recovered.";
    if (/\\b(hacked|incident|breach|ransomware|malware|phishing|compromised)\\b/.test(q)) return "For an active incident, use a trusted device to secure affected accounts, change compromised passwords, enable MFA, contact the relevant provider or bank, and preserve logs and messages. Avoid altering affected systems unnecessarily if evidence may be needed. We can capture details for a team follow-up.";
    if (/\\b(guarantee|guaranteed|recover|recovery|will i get|success rate)\\b/.test(q)) return "We cannot guarantee tracing, asset recovery, attribution, or a particular outcome. We assess available evidence and explain realistic options and limitations. Be cautious of anyone promising guaranteed recovery or asking for private keys or seed phrases.";
    if (/\\b(privacy|personal data|confidential)\\b/.test(q)) return "Please share only the information needed for an initial inquiry. Do not put passwords, authentication codes, private keys, seed phrases, or full payment-card details in chat. Use the contact form for case material and share sensitive evidence only through a team-approved secure method.";
    if (/\\b(agent|human|person|representative|team member|speak to someone|live support)\\b/.test(q)) { speakToAgent(); return ""; }
    const result = classify(raw);
    lastReply = result.text;
    leadIntent = result.type;
    return result.text + " If you’d like a team member to review your request, choose “Speak with an agent” or “Request a quote / follow-up.”";
  }
  function handleInput(raw) {
    const value = raw.trim();
    if (!value) return;
    addMessage(value, "user");
    if (stage.startsWith("lead:")) {
      const field = stage.slice(5);
      if (requiredFields.includes(field)) {
        if (field === "email" && !/^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$/.test(value)) { addMessage("That email format doesn’t look right. " + fieldPrompts.email, "bot"); return; }
        fields[field] = value.slice(0, 300);
        const missing = nextMissingField();
        if (missing) { stage = "lead:" + missing; addMessage(fieldPrompts[missing], "bot"); return; }
        stage = "lead:service";
        addMessage(serviceSummary(), "bot");
        return;
      }
      if (field === "service") {
        fields.service = value.slice(0, 500);
        stage = "lead:details";
        addMessage("Please briefly describe the scope or issue and what outcome you’re requesting. Do not include passwords, private keys, seed phrases, or authentication codes.", "bot");
        return;
      }
      if (field === "details") {
        fields.details = value.slice(0, 1500);
        finishLead();
        return;
      }
    }
    const response = answer(value);
    if (response) addMessage(response, "bot");
  }
  launcher.addEventListener("click", () => panel.classList.contains("open") ? closePanel() : openPanel());
  panel.querySelector(".zc-close").addEventListener("click", closePanel);
  panel.querySelectorAll("[data-action]").forEach(btn => btn.addEventListener("click", () => {
    const action = btn.dataset.action;
    if (action === "agent") { speakToAgent(); return; }
    if (action === "case") { submitCase(); return; }\n    if (action === "quote") { requestLeadDetails("quote"); return; }
    if (action === "services") addMessage("Our services include Vulnerability Assessment & Penetration Testing, Web Application Security, Network & Endpoint Testing, Social Engineering & Configuration Reviews, Forensics & Incident Response, and Threat Modeling & Consulting. We also support lawful asset and crypto tracing within an authorized scope.", "bot");
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
