from pathlib import Path
from html import escape
import json
from datetime import date

BASE = "https://borrissly-svg.github.io/Blog"
TODAY = "2026-10-08"

topics = [
("crypto-recovery","Crypto Asset Recovery","crypto recovery, digital asset recovery, blockchain tracing"),
("blockchain-tracing","Blockchain Transaction Tracing","blockchain tracing, transaction analysis, crypto investigations"),
("wallet-security","Crypto Wallet Security","crypto wallet security, wallet compromise, digital assets"),
("exchange-investigations","Crypto Exchange Investigations","crypto exchange investigation, transaction records, asset tracing"),
("scam-response","Crypto Scam Response","crypto scam response, fraud evidence, transaction hash"),
("osint","OSINT for Digital Investigations","OSINT, open source intelligence, digital investigations"),
("identity-security","Identity and Account Security","identity protection, account security, incident response"),
("phishing","Phishing and Social Engineering","phishing protection, social engineering, cybersecurity"),
("aml-compliance","AML and Digital Asset Compliance","AML, crypto compliance, transaction monitoring"),
("evidence","Digital Evidence Preservation","digital evidence, evidence preservation, cyber investigation"),
("bank-tracing","Bank Wire Investigation Basics","bank wire tracing, payment investigation, fraud response"),
("nft","NFT Investigation Basics","NFT investigation, digital collectibles, blockchain analysis"),
("defi","DeFi Transaction Analysis","DeFi investigation, smart contracts, crypto risk"),
("ransomware","Ransomware Incident Response","ransomware response, cybersecurity incident, digital evidence"),
("account-recovery","Account Recovery Security","account recovery, MFA, password security"),
("fraud-awareness","Digital Fraud Awareness","fraud prevention, recovery scam awareness, cybersecurity"),
("private-keys","Private Key and Seed Phrase Security","seed phrase security, private keys, crypto safety"),
("transaction-hash","Transaction Hash and TXID Analysis","TXID, transaction hash, blockchain evidence"),
("cyber-intelligence","Cyber Intelligence","cyber intelligence, threat awareness, security"),
("incident-response","Digital Incident Response","incident response, cybersecurity checklist, digital forensics"),
]
audiences = [
"for individuals",
"for organizations",
"for suspected fraud victims",
"for security teams",
"for beginners",
"for compliance teams",
"for small businesses",
"for families",
"for investigators",
"for people evaluating recovery services",
]
formats = [
"A Practical Guide",
"Step-by-Step Overview",
"Evidence and Documentation Guide",
"Common Mistakes to Avoid",
"Questions to Ask Before Taking Action",
]

out = Path("articles")
out.mkdir(exist_ok=True)

def slug(s):
    return "".join(c.lower() if c.isalnum() else "-" for c in s).strip("-")

urls = []
n = 1
for key, topic, keywords in topics:
    for audience in audiences:
        for fmt in formats:
            title = f"{topic} — {fmt} {audience}"
            filename = f"{n:04d}-{key}-{slug(fmt)}-{slug(audience)}.html"
            url = f"{BASE}/articles/{filename}"
            tags = " ".join("#" + slug(k).replace("-", "") for k in keywords.split(", "))
            description = f"Educational guidance about {keywords}, evidence preservation, verification, security and responsible investigative next steps."
            body = f"""
<p>When a digital incident affects money, accounts or online assets, the first priority is a reliable record of what happened. This educational guide covers <strong>{escape(topic.lower())}</strong> {escape(audience)} and focuses on evidence-led, responsible investigation.</p>
<p>Begin with a timeline. Record the last known successful access, the first sign of suspicious activity, transaction dates, platform names and actions taken afterward. Preserve original emails, messages, receipts, screenshots, wallet addresses, transaction identifiers and account notifications. Keep originals unchanged and make working copies for analysis.</p>
<p>For blockchain incidents, a transaction hash or TXID can help locate a transfer on a public ledger. Public records may show addresses, timestamps, amounts and transaction relationships. An address alone does not automatically identify a person, so attribution should never be presented as fact without independent supporting evidence.</p>
<p>Good investigative practice distinguishes verified facts from hypotheses. Check sources, compare timestamps, document uncertainty and preserve provenance. If a bank, exchange, payment provider or law-enforcement agency is relevant, use its official reporting and evidence-preservation procedures.</p>
<p>Protect access throughout the process. Never give a supposed recovery provider a password, one-time code, private key, seed phrase or recovery phrase. Be cautious of guaranteed-recovery promises, pressure to pay quickly, or requests for secret credentials.</p>
<p>The goal is a clear, defensible record of what happened, what evidence exists, what can be independently verified and which next steps are appropriate. Cybersecurity and investigative work cannot guarantee that assets will be recovered, and a blockchain trace alone does not prove that funds can be returned.</p>
"""
            html = f"""<!doctype html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{escape(title)} | Ethical Zenith Hackers Intelligence</title>
<meta name="description" content="{escape(description)}">
<meta name="keywords" content="{escape(keywords)}">
<meta name="robots" content="index,follow,max-image-preview:large">
<link rel="canonical" href="{url}">
<meta property="og:type" content="article"><meta property="og:title" content="{escape(title)}">
<meta property="og:description" content="{escape(description)}"><meta property="og:url" content="{url}">
<meta name="twitter:card" content="summary">
<script type="application/ld+json">{json.dumps({"@context":"https://schema.org","@type":"Article","headline":title,"description":description,"datePublished":TODAY,"dateModified":TODAY,"author":{"@type":"Organization","name":"Ethical Zenith Hackers Intelligence"},"mainEntityOfPage":url}, ensure_ascii=False)}</script>
<style>body{{margin:0;background:#071827;color:#eaf7ff;font:17px/1.8 Arial,sans-serif}}main{{max-width:850px;margin:auto;padding:55px 22px}}a{{color:#55eaff}}article{{background:#0d2638;border:1px solid #28536b;border-radius:18px;padding:30px}}h1{{font-size:clamp(34px,6vw,58px);line-height:1.08}}.tag,.hashtags{{color:#55eaff}}.notice{{padding:15px;border-left:3px solid #55eaff;background:#102f42}}footer{{margin-top:35px;color:#9bb4c4;font-size:13px}}</style>
</head><body><main><a href="../index.html">← Ethical Zenith Hackers Intelligence Blog</a>
<article><div class="tag">DIGITAL INTELLIGENCE • ARTICLE {n}</div><h1>{escape(title)}</h1>
<p class="hashtags">{escape(tags)} #Cybersecurity #DigitalAssets #OSINT #AssetTracing #SecurityAwareness</p>
<p class="notice"><strong>Educational notice:</strong> This publication provides general cybersecurity and investigative information. It does not guarantee recovery of assets and is not legal, financial or law-enforcement advice.</p>
{body}
<h2>Key takeaways</h2><ul><li>Preserve original evidence and build a precise timeline.</li><li>Use transaction IDs and public records carefully.</li><li>Never disclose passwords, private keys or recovery phrases.</li><li>Verify claims and use official reporting channels.</li><li>Be skeptical of guaranteed recovery promises.</li></ul>
<p class="hashtags">{escape(tags)}</p></article><footer>© 2026 Ethical Zenith Hackers Intelligence Blog · <a href="../index.html">All articles</a></footer></main></body></html>"""
            (out / filename).write_text(html, encoding="utf-8")
            urls.append(url)
            n += 1

sitemap = ['<?xml version="1.0" encoding="UTF-8"?>','<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
for u in [f"{BASE}/", *urls]:
    sitemap.append(f"  <url><loc>{u}</loc><lastmod>{TODAY}</lastmod></url>")
sitemap.append("</urlset>")
Path("sitemap.xml").write_text("\n".join(sitemap), encoding="utf-8")
Path("robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {BASE}/sitemap.xml\n", encoding="utf-8")
print(f"Generated {len(urls)} articles, sitemap.xml and robots.txt")
