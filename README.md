# Internal IT Support Agent

## Project Overview

The **Internal IT Support Agent** is an AI-powered employee support system designed to handle common internal IT issues.

The agent understands an employee's problem, searches the company's internal knowledge base, provides relevant troubleshooting steps, asks for additional information when required, detects security-related risks, escalates unclear or risky issues, creates structured support tickets, and maintains an audit trail of its actions.

This project was developed as an **Internal Service Agent** for the IT function.



## Problem Statement

Employees often face common IT problems such as:

* Outlook or email issues
* VPN connection problems
* Laptop or desktop issues
* Password and account-related problems
* Security incidents

Handling these requests manually can take time and may result in inconsistent responses.

This project provides a first-level IT support agent that can handle common issues automatically while escalating risky or unsupported requests to the appropriate IT team.


## Key Features

### 1. Understand Employee Issues

The employee can describe an IT problem using natural language.

Example:

> My Outlook is not syncing new emails.

The agent analyzes the request and identifies the relevant support area.

### 2. Knowledge Base Search

The agent searches a local company knowledge base containing approved IT policies and troubleshooting documents.

Current knowledge sources include:

* Email Troubleshooting Guide
* VPN Troubleshooting Guide
* Password and Account Policy
* Hardware Support Policy
* Security Incident Policy

### 3. Troubleshooting

For supported issues, the agent provides step-by-step troubleshooting instructions based on the company knowledge base.

### 4. Follow-up Questions

If the available information is insufficient, the agent asks the employee for additional details such as:

* Affected device or application
* Error message or error code
* Device or application name
* What happened before the issue occurred

### 5. Security Risk Detection

Security-related requests are detected before normal troubleshooting.

Examples include:

* Shared passwords
* Phishing
* Suspicious links
* Unauthorized access
* Stolen credentials
* Lost or stolen company devices
* Malware or ransomware suspicion

Security incidents are immediately escalated to **IT Security** and assigned high priority.

### 6. Ticket Creation

The system creates structured tickets containing:

* Ticket ID
* Date and time
* Category
* Priority
* Status
* Assigned team
* Employee issue
* Knowledge source

### 7. Escalation

The agent can escalate:

* Security incidents → IT Security
* Unsupported but sufficiently detailed issues → IT Support

### 8. Source Transparency

The agent displays the knowledge-base document used to generate the response.

This allows employees and reviewers to understand where the answer came from.

### 9. Audit Trail

Important agent actions are recorded in an audit log, including:

* Issue received
* Risk check
* Knowledge-base search
* AI response generation
* Follow-up required
* Ticket creation
* Issue escalation
* Source displayed


## System Workflow

```text
Employee
   ↓
Describe IT Issue
   ↓
Internal IT Support Agent
   ↓
Risk Detection
   ├── Security Risk → IT Security → HIGH Priority Ticket
   │
   └── Normal Issue
          ↓
      Knowledge Base Search
          ↓
      Relevant Policy Found?
        ├── Yes → Troubleshooting / Follow-up
        │
        └── No → Ask for Details
                    ↓
              Enough Information?
                ├── Yes → IT Support Ticket
                └── No → Request More Information




## Technology Stack

* **Python** — Core application logic
* **Streamlit** — Web-based user interface
* **Google Gemini API** — Natural-language response generation
* **JSON** — Ticket and audit-log storage
* **Local TXT files** — Company knowledge base
* **GitHub** — Source-code repository



## Project Structure

```text
Internal-IT-Support-Agent_23CSU011_Aditi-Goyal/
│
├── knowledge_base/
│   ├── email_troubleshooting.txt
│   ├── vpn_troubleshooting.txt
│   ├── password_account_policy.txt
│   ├── hardware_support_policy.txt
│   └── security_incident_policy.txt
│
├── agent.py
├── app.py
├── knowledge_base.py
├── ticket_system.py
├── audit_log.py
├── .gitignore
└── README.md




## How It Works

### Step 1 — Employee submits an issue

The employee enters the problem through the Streamlit interface.

### Step 2 — Risk check

The agent checks whether the issue contains indicators of a security incident.

If a security risk is detected, normal troubleshooting is stopped and the request is escalated to IT Security.

### Step 3 — Knowledge-base retrieval

For normal IT issues, the system identifies the relevant knowledge-base document.

### Step 4 — AI response

Gemini generates a concise response using the retrieved company knowledge.

The system is instructed not to invent company policies or unsupported troubleshooting procedures.

### Step 5 — Ticket creation

If the issue requires escalation or the issue is unsupported but contains enough information, a structured ticket is created.

### Step 6 — Audit logging

The important actions performed by the agent are recorded in the audit trail.



## Example Use Cases

### Email Issue

**Employee:**

> My Outlook is not syncing new emails.

**Agent:**

Provides troubleshooting steps from the Email Troubleshooting Guide and displays the source document.



### VPN Issue

**Employee:**

> My company VPN is not connecting.

**Agent:**

Provides VPN troubleshooting steps and can ask for additional information if required.



### Security Incident

**Employee:**

> I accidentally shared my company password with someone.

**Agent:**

* Stops normal troubleshooting
* Identifies the security risk
* Creates a HIGH-priority ticket
* Assigns it to IT Security
* Records the escalation in the audit trail



### Unsupported Issue

**Employee:**

> My printer is showing error code E45 on my HP printer.

**Agent:**

If no matching company policy exists, the agent asks for additional information. Once sufficient information is available, it can create a General IT Support ticket for further investigation.



## Security Considerations

* The agent does not ask employees to provide their passwords.
* Security-related issues are escalated instead of being handled through normal troubleshooting.
* API keys are stored outside the source code using environment variables.
* Generated ticket and audit files are excluded from the GitHub repository.
* Sensitive credentials should never be committed to the repository.



## Ticketing System

For this assignment, ticket creation is implemented as a **local simulated ticketing system** using JSON storage.

In a production environment, this component could be integrated with an enterprise IT service-management platform such as ServiceNow or Jira.



## Limitations

* The current knowledge base contains a limited set of IT policies.
* Knowledge retrieval currently uses topic/keyword matching rather than a vector database.
* Ticket creation is simulated locally rather than connected to a production ITSM platform.
* AI responses depend on the availability and quota of the Gemini API.
* The system is designed as a first-level support agent and escalates issues that require further investigation.


## Future Improvements

Possible future enhancements include:

* Integration with ServiceNow or Jira
* Vector database-based semantic search
* Larger company knowledge base
* Employee authentication
* Role-based access control
* Email or Teams/Slack integration
* Real-time IT service monitoring
* Analytics dashboard for support tickets
* More advanced security incident classification

## Assignment Requirements Covered

| Requirement                     | Implementation                            |
| ------------------------------- | ----------------------------------------- |
| Understand employee issue       | Natural-language input + Gemini           |
| Find relevant policy/resolution | Internal knowledge-base retrieval         |
| Ask follow-up questions         | AI follow-up + missing-information checks |
| Resolve simple requests         | Knowledge-base troubleshooting            |
| Escalate risky requests         |                                           |
