from google import genai
import os

from knowledge_base import search_knowledge_base
from ticket_system import create_ticket
from audit_log import log_event


# ==========================================
# CONNECT TO GEMINI
# ==========================================

api_key = os.getenv("GEMINI_API_KEY")

client = None

if api_key:
    client = genai.Client(
        api_key=api_key
    )


# ==========================================
# FALLBACK RESPONSE
# ==========================================

def create_fallback_response(issue, results):

    if not results:
        return """
I could not find a matching company knowledge-base document for this issue.

Please provide more details about the problem, such as:
- The affected device or application
- Any error message or error code
- What happened before the issue occurred

Once enough information is available, an IT support ticket can be created for further review.
"""

    document = results[0]

    content = document["content"]

    if "Recommended troubleshooting:" in content:

        troubleshooting = content.split(
            "Recommended troubleshooting:"
        )[1]

        if "Escalation:" in troubleshooting:

            troubleshooting = troubleshooting.split(
                "Escalation:"
            )[0]

        troubleshooting = troubleshooting.strip()

    else:

        troubleshooting = content

    return f"""
### Recommended Troubleshooting

Based on the company knowledge base, please follow these steps:

{troubleshooting}

If the issue continues after trying these steps, an IT support ticket should be created.
"""


# ==========================================
# CHECK WHETHER UNKNOWN ISSUE HAS ENOUGH INFO
# ==========================================

def has_enough_ticket_information(issue):

    issue_lower = issue.lower()

    useful_details = [
        "error",
        "error code",
        "model",
        "asset",
        "device",
        "printer",
        "laptop",
        "desktop",
        "computer",
        "screen",
        "application",
        "software"
    ]

    detail_count = sum(
        1
        for keyword in useful_details
        if keyword in issue_lower
    )

    # A reasonably detailed issue can be ticketed.
    return len(issue.split()) >= 8 and detail_count >= 2


# ==========================================
# MAIN AGENT
# ==========================================

def get_ai_response(issue):

    # ==========================================
    # STEP 1: ISSUE RECEIVED
    # ==========================================

    log_event(
        "ISSUE_RECEIVED",
        issue
    )

    # ==========================================
    # STEP 2: RISK DETECTION
    # ==========================================

    risk_keywords = [
        "password",
        "credential",
        "credentials",
        "phishing",
        "suspicious link",
        "suspicious email",
        "unauthorized access",
        "unauthorized login",
        "account compromised",
        "account compromise",
        "malware",
        "ransomware",
        "lost laptop",
        "stolen laptop",
        "lost device",
        "stolen device"
    ]

    issue_lower = issue.lower()

    is_risky = any(
        keyword in issue_lower
        for keyword in risk_keywords
    )

    log_event(
        "RISK_CHECK",
        f"Risk detected: {is_risky}"
    )

    # ==========================================
    # STEP 3: SECURITY ESCALATION
    # ==========================================

    if is_risky:

        ticket = create_ticket(
            issue=issue,
            category="Security Incident",
            priority="HIGH",
            status="ESCALATED",
            assigned_team="IT Security",
            source=[
                "password_account_policy.txt",
                "security_incident_policy.txt"
            ]
        )

        log_event(
            "TICKET_CREATED",
            f"Ticket {ticket['ticket_id']} created and assigned to IT Security"
        )

        log_event(
            "ISSUE_ESCALATED",
            "Security incident escalated as HIGH priority"
        )

        return f"""
🚨 **Security Escalation Required**

This issue may involve a security incident.

Standard troubleshooting has been stopped and the issue has been escalated to **IT Security**.

### 🎫 Ticket Created

**Ticket ID:** {ticket["ticket_id"]}

**Category:** Security Incident

**Priority:** HIGH

**Status:** ESCALATED

**Assigned Team:** IT Security

### Immediate Action

- Change your password using the official company password-reset process.
- Do not share your password with anyone.
- Do not provide your password to IT Support.

Please do not include passwords or sensitive credentials in your responses.

📚 **Source:** password_account_policy.txt, security_incident_policy.txt
"""

    # ==========================================
    # STEP 4: SEARCH KNOWLEDGE BASE
    # ==========================================

    results = search_knowledge_base(issue)

    log_event(
        "KNOWLEDGE_BASE_SEARCH",
        f"Found {len(results)} matching documents"
    )

    # ==========================================
    # STEP 5: UNKNOWN ISSUE HANDLING
    # ==========================================

    if not results:

        enough_information = has_enough_ticket_information(
            issue
        )

        if enough_information:

            ticket = create_ticket(
                issue=issue,
                category="General IT Support",
                priority="MEDIUM",
                status="OPEN",
                assigned_team="IT Support",
                source=[
                    "No matching company knowledge-base document"
                ]
            )

            log_event(
                "TICKET_CREATED",
                f"Ticket {ticket['ticket_id']} created for unsupported IT issue"
            )

            log_event(
                "ISSUE_ESCALATED",
                "Unsupported issue routed to IT Support"
            )

            return f"""
### 🎫 IT Support Ticket Created

I could not find a matching company knowledge-base document for this issue.

Since enough information was provided, I have created a support ticket for further investigation.

**Ticket ID:** {ticket["ticket_id"]}

**Category:** General IT Support

**Priority:** MEDIUM

**Status:** OPEN

**Assigned Team:** IT Support

### Next Step

An IT Support team member can review the issue and investigate further.

📚 **Source:** No matching company knowledge-base document found
"""

        else:

            log_event(
                "FOLLOW_UP_REQUIRED",
                "Additional information required before ticket creation"
            )

            return """
### 🔍 More Information Needed

I could not find a matching company knowledge-base document for this issue.

Please provide:

- The affected device or application
- The exact error message or error code
- The device/application model or name
- What happened before the issue occurred

Once enough information is available, an IT support ticket can be created.

📚 **Source:** No matching company knowledge-base document found
"""

    # ==========================================
    # STEP 6: CREATE KNOWLEDGE CONTEXT
    # ==========================================

    knowledge = ""

    for result in results:

        knowledge += (
            f"\n\nSOURCE: {result['filename']}\n"
            f"{result['content']}"
        )

    # ==========================================
    # STEP 7: TRY GEMINI
    # ==========================================

    ai_text = None

    if client and results:

        prompt = f"""
You are an Internal IT Support Agent for a company.

Your job is to help employees with IT problems.

IMPORTANT RULES:

1. Use the company knowledge base provided below.
2. Prefer company knowledge over general knowledge.
3. Do not invent company policies or troubleshooting procedures.
4. Give simple and practical troubleshooting steps.
5. If important information is missing, ask a follow-up question.
6. Be professional and concise.
7. Clearly explain the solution.
8. Never ask for passwords or sensitive credentials.
9. If the knowledge base does not contain enough information, say so.
10. Do not add troubleshooting steps that are not supported by the knowledge base.
11. Do not claim that a ticket was created unless the application has actually created one.

COMPANY KNOWLEDGE BASE:
{knowledge}

EMPLOYEE ISSUE:
{issue}
"""

        try:

            response = client.models.generate_content(
                model="gemini-3.6-flash",
                contents=prompt
            )

            ai_text = response.text

            log_event(
                "AI_RESPONSE_GENERATED",
                "Gemini generated the IT support response"
            )

        except Exception:

            log_event(
                "AI_SERVICE_ERROR",
                "AI service unavailable; fallback response activated"
            )

            ai_text = None

    # ==========================================
    # STEP 8: FALLBACK IF GEMINI UNAVAILABLE
    # ==========================================

    if ai_text is None:

        ai_text = create_fallback_response(
            issue,
            results
        )

        log_event(
            "FALLBACK_RESPONSE_USED",
            "Company knowledge-base response used"
        )

    # ==========================================
    # STEP 9: SOURCE
    # ==========================================

    source_names = ", ".join(
        result["filename"]
        for result in results
    )

    log_event(
        "SOURCE_SHOWN",
        source_names
    )

    # ==========================================
    # STEP 10: RETURN RESPONSE
    # ==========================================

    return (
        f"{ai_text}\n\n"
        f"📚 **Source:** {source_names}"
    )