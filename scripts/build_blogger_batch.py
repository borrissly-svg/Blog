#!/usr/bin/env python3
"""Generate 500 Blogger-ready educational articles: 100 in each of five categories."""
import html
import json
from pathlib import Path

OUT = Path("blogger-batch.json")
BRAND = "Zenith Hackers Intelligence"
CONTACT = "https://zenithhackers.com/"
BLOG = "https://ethicalzenithhackers.online/"

categories = [
    {
        "name": "Blockchain tracing fundamentals",
        "topics": [
            ("Wallet addresses", "A wallet address is a public identifier used to receive assets on a network. It is not, by itself, proof of the owner's real-world identity."),
            ("Transaction hashes and TXIDs", "A transaction hash or TXID is a network-specific identifier for a transaction. Verify it on the correct chain and compare its status, time, assets, and destination."),
            ("Blockchain explorers", "A blockchain explorer presents public ledger data in a searchable interface. Confirm the network and use more than one reputable source when a result is important."),
            ("Confirmations and finality", "Confirmations indicate how a transaction is included in a chain's history. The meaning of finality and the practical confirmation threshold vary by network and service."),
            ("Transaction histories", "A transaction history is a sequence of recorded events, not a complete explanation of intent or identity. Preserve the source and timestamps for every observation."),
            ("Inputs, outputs, and transfers", "Transaction structures differ between chains. Interpret inputs, outputs, token transfers, fees, and contract interactions using the relevant network's model."),
            ("Timestamps and block heights", "Block timestamps and heights help organize events, but they should be recorded with the network and time zone and not treated as exact proof of a person's actions."),
            ("Token transfers and contract events", "Token movements may be represented by contract events rather than a simple native-coin transfer. Check the token contract and network before drawing conclusions."),
            ("Transaction fees and network costs", "Fees can help explain transaction mechanics but do not identify a sender or prove a transfer was fraudulent. Record the fee unit and network context."),
            ("Building a trace timeline", "A defensible timeline records the transaction identifier, observed time, network, addresses, asset, amount, source, and confidence level for each step.")
        ],
        "actions": [
            "Start by confirming the network and copying the transaction identifier directly from the wallet or exchange record.",
            "Open a reputable explorer for that network and compare the displayed details with the original record.",
            "Record the URL, access date, time zone, transaction status, and relevant addresses without editing the source evidence.",
            "Separate observed ledger facts from assumptions about who controlled an address or why a transfer occurred.",
            "If an exchange or custodian may be involved, preserve the transaction record and use that provider's official reporting channel."
        ],
        "limits": "Public ledger data may show movement between addresses, but it does not automatically reveal a person's identity, intent, or ability to return funds."
    },
    {
        "name": "Scam investigation and fraud evidence",
        "topics": [
            ("Investment scams", "Investment fraud often uses unrealistic returns, urgency, fabricated dashboards, or repeated demands for deposits. Preserve the pitch and payment trail before contacting the platform."),
            ("Impersonation scams", "Impersonation may involve copied profiles, spoofed names, or lookalike domains. Preserve the exact account, URL, message headers where available, and timestamps."),
            ("Romance scams", "Romance scams may build trust before introducing urgent financial requests or investment opportunities. Preserve messages and payment records without sending more money."),
            ("Fake exchanges and trading platforms", "A fake exchange may show balances that cannot be withdrawn or demand extra fees. A displayed dashboard balance is not independent proof that assets exist."),
            ("Recovery scams", "Recovery fraud targets people after an earlier loss and may promise guaranteed returns or demand advance fees. No legitimate review can guarantee that stolen assets will be returned."),
            ("Phishing and account takeover", "Phishing may expose login details or one-time codes. Preserve alerts and messages, secure accounts from a trusted device, and contact the relevant provider directly."),
            ("Advance-fee fraud", "Advance-fee fraud conditions a supposed payout on another payment. Document each demand and avoid paying additional fees based solely on a promise."),
            ("Fake support agents", "Fake support agents may contact victims through social media or messaging apps. Verify support through the official website or app rather than the contact details in the message."),
            ("Pig-butchering and long-con fraud", "Long-con investment fraud can combine relationship-building with fake trading platforms. Preserve the conversation timeline and all payment requests."),
            ("Business email and payment diversion", "Payment diversion may use compromised or lookalike business email. Verify changed bank details using a previously trusted phone number and preserve original email headers.")
        ],
        "actions": [
            "Stop sending funds while the claim is being checked; do not pay a new fee merely to unlock a supposed balance or recovery.",
            "Preserve original messages, profile URLs, emails, receipts, transaction IDs, wallet addresses, and the names of payment platforms.",
            "Build a dated timeline that distinguishes what you personally observed from what another person claimed.",
            "Report the incident to the relevant bank, exchange, payment provider, platform, or law-enforcement agency through its official channel.",
            "Be wary of anyone who guarantees recovery, pressures you to act immediately, or requests passwords, seed phrases, or remote access."
        ],
        "limits": "Evidence can support a report or investigation, but it cannot by itself guarantee attribution, a refund, asset freezing, or recovery."
    },
    {
        "name": "Evidence collection and reporting",
        "topics": [
            ("Transaction documentation", "A useful transaction record includes the network, transaction ID, addresses, asset and amount, timestamp, explorer URL, and source of the information."),
            ("Preserving messages and emails", "Keep original messages and emails where possible. Screenshots help provide context, while original files and email headers may preserve additional details."),
            ("Creating an incident timeline", "A timeline organizes events in chronological order and notes the source, time zone, and confidence for each entry."),
            ("Exchange and payment records", "Provider records may include account notices, deposits, withdrawals, support tickets, and reference numbers. Request them through official channels."),
            ("Screenshots and source records", "Screenshots should show enough context to identify the page or conversation. Keep unedited originals and document when and how each copy was captured."),
            ("Evidence integrity and file hashes", "A cryptographic file hash can help detect whether a file changed after collection. Record the algorithm, digest, filename, and collection time."),
            ("Case summaries", "A clear case summary explains what happened, when it happened, what is known, what evidence exists, and which steps have already been taken."),
            ("Reporting to exchanges", "A concise report helps an exchange locate relevant activity. Include transaction identifiers and account references, but never send passwords or recovery phrases."),
            ("Bank and law-enforcement reports", "Use official reporting channels and keep the submission confirmation or case number. Reporting requirements vary by jurisdiction and institution."),
            ("Privacy-aware evidence sharing", "Share only information necessary for the recipient to assess the incident. Redact unrelated personal information and use an approved secure transfer method for sensitive files.")
        ],
        "actions": [
            "Preserve the original item first, then create a working copy for annotations or redactions.",
            "Label every item with a unique evidence number and record where it came from and when it was collected.",
            "Keep a chronology of relevant events, including the first suspicious contact, transfers, alerts, and reports made.",
            "Mark each statement as observed, reported by another party, or still unverified.",
            "Store copies securely and share them only with the provider, adviser, or authority that needs them."
        ],
        "limits": "Evidence quality depends on provenance, completeness, and context. A screenshot or isolated transaction record may not establish the full story on its own."
    },
    {
        "name": "Blockchain networks and tracing limitations",
        "topics": [
            ("Bitcoin tracing", "Bitcoin transactions use a UTXO model. Inputs, outputs, change, and address reuse must be interpreted carefully, and common-input heuristics are not proof of shared ownership."),
            ("Ethereum tracing", "Ethereum supports account-based transactions and smart-contract interactions. Internal calls and token events may require additional context beyond the top-level transaction."),
            ("Stablecoin transfers", "Stablecoins can exist on several networks and may have issuer-specific controls. Confirm the token contract and chain before interpreting a transfer."),
            ("Cross-chain bridges", "Cross-chain activity can involve lock-and-mint, burn-and-release, liquidity, or messaging mechanisms. Match events on both networks and account for bridge-specific identifiers."),
            ("Privacy coins and privacy tools", "Privacy-focused designs and mixing services can reduce the visibility of transaction relationships. Public observations may be incomplete and should not be overstated."),
            ("Exchange deposit and withdrawal flows", "Custodial services may pool funds and use internal accounting that is not visible on a public ledger. Public addresses may not map one-to-one to customers."),
            ("Smart contracts and DeFi", "Decentralized finance transactions may call multiple contracts and emit events. Interpret contract code, token events, and protocol context before describing the economic result."),
            ("Address attribution limits", "Attribution claims need independent corroboration. An address label from a third-party source can be outdated, incomplete, or wrong."),
            ("Network reorganizations and pending transactions", "Pending status and chain reorganizations can affect whether a transaction is treated as settled. Confirm the current status and the relevant service's finality rules."),
            ("Bridges, mixers, and fragmented trails", "A trail may cross multiple chains, services, and time periods. Document every inference and the evidence supporting each connection.")
        ],
        "actions": [
            "Identify the exact chain, asset contract if applicable, and transaction identifier before following the trail.",
            "Use the network's own explorer and reputable documentation to understand what each field means.",
            "Keep separate records for direct observations, heuristic links, third-party labels, and confirmed real-world information.",
            "Check for custodial or bridge steps that may break a simple one-address-to-one-person assumption.",
            "State what cannot be established from available public data and what additional records might be needed."
        ],
        "limits": "Tracing is probabilistic in some contexts and constrained by privacy features, custodial records, incomplete data, and cross-chain complexity. A trace does not guarantee recovery."
    },
    {
        "name": "Prevention, professional guidance, and next steps",
        "topics": [
            ("Avoiding repeat scams", "After a suspected scam, secure accounts, revoke suspicious sessions, enable multifactor authentication, and be cautious of follow-up contacts offering recovery."),
            ("Choosing legitimate investigation help", "A credible provider explains scope, methods, limitations, privacy handling, fees, and deliverables in writing, without promising a guaranteed outcome."),
            ("Preparing for a consultation", "A useful consultation summary lists the incident timeline, known transaction IDs, involved services, steps already taken, and the questions that remain."),
            ("Wallet and account security", "Use unique passwords, hardware-backed or app-based multifactor authentication where appropriate, and carefully verified wallet backups."),
            ("Verifying service providers", "Verify a provider's identity, business details, references, and contract terms independently. Do not rely only on testimonials or unsolicited direct messages."),
            ("Incident response planning", "A response plan defines roles, escalation paths, evidence preservation, communication channels, and recovery priorities before an incident occurs."),
            ("Recovery claims and red flags", "Guaranteed recovery claims, upfront unlock fees, pressure tactics, and requests for secret credentials are strong warning signs that require independent verification."),
            ("Questions to ask a professional", "Ask what authorization is required, what work is in scope, what deliverables you will receive, how data is protected, and what outcomes cannot be promised."),
            ("Securely sharing case material", "Use a verified, access-controlled channel and share the minimum information required. Never include private keys, seed phrases, or passwords in a case summary."),
            ("Understanding next steps", "Next steps may include securing accounts, notifying providers, preserving evidence, making reports, and obtaining qualified advice appropriate to the jurisdiction.")
        ],
        "actions": [
            "Secure affected accounts and devices using trusted channels, and revoke unknown sessions or keys where safe to do so.",
            "Preserve the records before deleting messages, resetting devices, or making changes that may remove useful evidence.",
            "Verify any professional or recovery service independently and insist on a written scope, costs, privacy terms, and limitations.",
            "Prepare a short factual summary and a list of unresolved questions before a consultation.",
            "Use official bank, exchange, wallet, platform, and government reporting channels where applicable."
        ],
        "limits": "Professional guidance can clarify evidence and options, but no provider can honestly guarantee that a transaction can be reversed or assets recovered."
    }
]

angles = [
    ("A Practical Guide", "Explain the core concepts in plain language and show how to apply them carefully."),
    ("A Step-by-Step Checklist", "Turn the topic into a sequence of checks that can be followed without skipping evidence or safety steps."),
    ("Common Mistakes to Avoid", "Focus on errors that can lead to misleading conclusions, lost records, or additional risk."),
    ("Evidence to Preserve", "Describe the records that are most useful, how to preserve originals, and how to record provenance."),
    ("Questions to Ask Before Acting", "Provide questions that help readers verify claims and choose a responsible next step."),
    ("How to Build a Timeline", "Show how to organize events chronologically while recording sources, time zones, and uncertainty."),
    ("What the Records Can and Cannot Prove", "Distinguish direct observations from assumptions and explain important limitations."),
    ("A Guide for Individuals", "Apply the topic to a person documenting an incident and deciding which official channels to contact."),
    ("A Guide for Organizations", "Apply the topic to teams that need clear roles, controlled evidence handling, and documented decisions."),
    ("A Reporting and Follow-Up Guide", "Explain how to prepare a concise report and track follow-up with relevant providers or authorities.")
]

def paragraph(text):
    return "<p>" + html.escape(text) + "</p>"

def make_post(category, topic, angle, idx):
    cat = category["name"]
    subject, detail = topic
    angle_title, angle_guidance = angle
    title = f"{subject}: {angle_title} ({cat})"
    title = title[:145]
    actions = category["actions"]
    # Rotate and combine practical actions so each topic/angle gets a distinct emphasis.
    offset = (idx + angles.index(angle)) % len(actions)
    selected = [actions[(offset + j) % len(actions)] for j in range(3)]
    intro = f"This educational article covers {subject.lower()} within {cat.lower()}. {detail}"
    body = [
        paragraph(intro),
        "<h2>Why this matters</h2>",
        paragraph(f"{angle_guidance} In real cases, the quality of the record often matters as much as the first observation. Work from sources that can be checked later and avoid filling gaps with guesses."),
        "<h2>Practical approach</h2>",
        paragraph(selected[0]),
        paragraph(selected[1]),
        paragraph(selected[2]),
        "<h2>Keep the record defensible</h2>",
        paragraph("Record the date and time with the time zone, the source used, and the exact identifier or URL where relevant. Preserve originals, make separate working copies, and label uncertain conclusions as unverified. If a record is updated or a provider responds later, add the new information rather than silently overwriting the earlier entry."),
        "<h2>Privacy and safety</h2>",
        paragraph("Do not share passwords, one-time authentication codes, private keys, seed phrases, recovery phrases, or remote-access credentials with a supposed investigator. Verify service providers through independently obtained contact details and use official reporting channels. If money or an account is at immediate risk, contact the relevant bank, exchange, wallet provider, or platform promptly."),
        "<h2>Limitations</h2>",
        paragraph(category["limits"] + " The available evidence, jurisdiction, provider policies, and technical details determine which next steps are realistic."),
        "<h2>How Zenith Hackers Intelligence may help</h2>",
        f"<p>{BRAND} supports authorized cybersecurity, digital forensics, incident response, evidence review, and lawful asset or crypto-tracing inquiries within a defined scope. We use evidence-based methods, explain limitations, and do not guarantee attribution or recovery. For a consultation, visit <a href=\"{CONTACT}\">Zenith Hackers Intelligence</a> or review our <a href=\"{BLOG}\">educational blog</a>. Share only non-sensitive initial details; never submit passwords, private keys, or recovery phrases.</p>",
        paragraph("This article is educational information, not legal, financial, or investment advice. Reporting options and legal requirements vary by location.")
    ]
    labels = [cat, subject, "Zenith Hackers Intelligence", "Blockchain Safety", "Digital Evidence"]
    return {
        "id": f"{idx:03d}",
        "category": cat,
        "title": title,
        "labels": list(dict.fromkeys(labels)),
        "content": "\n".join(body)
    }

def main():
    posts = []
    idx = 1
    for category in categories:
        for topic in category["topics"]:
            for angle in angles:
                posts.append(make_post(category, topic, angle, idx))
                idx += 1
    assert len(posts) == 500, f"Expected 500 posts, got {len(posts)}"
    counts = {}
    for post in posts:
        counts[post["category"]] = counts.get(post["category"], 0) + 1
    assert all(count == 100 for count in counts.values()), counts
    OUT.write_text(json.dumps(posts, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Generated {len(posts)} Blogger articles: " + "; ".join(f"{name}: {count}" for name, count in counts.items()))

if __name__ == "__main__":
    main()
