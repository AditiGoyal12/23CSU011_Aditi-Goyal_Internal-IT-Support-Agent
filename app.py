import streamlit as st
import json
import os

from agent import get_ai_response


# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="Internal IT Support Agent",
    page_icon="🤖",
    layout="wide"
)


# ==========================================
# HEADER
# ==========================================

st.title("🤖 Internal IT Support Agent")

st.markdown(
    "### AI-powered first-level IT support for employees"
)

st.caption(
    "Resolve common IT issues • Search company knowledge • "
    "Detect risks • Escalate incidents • Create tickets"
)

st.divider()


# ==========================================
# SIDEBAR
# ==========================================

with st.sidebar:

    st.header("🛠️ Support Center")

    st.markdown("### Agent Capabilities")

    st.write("✅ Understand employee issues")
    st.write("✅ Search company knowledge")
    st.write("✅ Provide troubleshooting")
    st.write("✅ Ask follow-up questions")
    st.write("🛡️ Detect security risks")
    st.write("🚨 Escalate risky incidents")
    st.write("🎫 Create support tickets")
    st.write("📋 Maintain audit trail")

    st.divider()

    st.markdown("### Knowledge Sources")

    st.write("📧 Email Troubleshooting")
    st.write("🌐 VPN Troubleshooting")
    st.write("🔐 Password & Account Policy")
    st.write("💻 Hardware Support Policy")
    st.write("🚨 Security Incident Policy")

    st.divider()

    st.info(
        "The agent uses company-approved knowledge "
        "sources to support its responses."
    )


# ==========================================
# MAIN INPUT
# ==========================================

st.subheader("👤 Employee Support Request")

issue = st.text_area(
    "Describe your IT issue",
    placeholder=(
        "Example: My Outlook is not syncing new emails.\n\n"
        "You can also report issues such as VPN problems, "
        "laptop problems, or security incidents."
    ),
    height=150
)


# ==========================================
# SUBMIT
# ==========================================

if st.button(
    "🚀 Submit Issue",
    type="primary",
    use_container_width=True
):

    if not issue.strip():

        st.warning(
            "Please describe your IT issue before submitting."
        )

    else:

        # --------------------------------------
        # ISSUE RECEIVED
        # --------------------------------------

        st.success("Issue received successfully!")

        st.subheader("📝 Employee Issue")

        st.info(issue)

        # --------------------------------------
        # AI PROCESSING
        # --------------------------------------

        with st.spinner(
            "🤖 AI Agent is analyzing your request..."
        ):

            answer = get_ai_response(issue)

        # --------------------------------------
        # AGENT RESPONSE
        # --------------------------------------

        st.subheader("🤖 Agent Response")

        st.markdown(answer)

        st.divider()

        # ======================================
        # TICKET INFORMATION
        # ======================================

        if os.path.exists("tickets.json"):

            with open(
                "tickets.json",
                "r",
                encoding="utf-8"
            ) as file:

                tickets = json.load(file)

            matching_tickets = [
                ticket
                for ticket in tickets
                if ticket["issue"] == issue
            ]

            if matching_tickets:

                ticket = matching_tickets[-1]

                st.subheader("🎫 Support Ticket")

                col1, col2, col3 = st.columns(3)

                with col1:

                    st.metric(
                        "Ticket ID",
                        ticket["ticket_id"]
                    )

                with col2:

                    st.metric(
                        "Priority",
                        ticket["priority"]
                    )

                with col3:

                    st.metric(
                        "Status",
                        ticket["status"]
                    )

                st.write(
                    f"**Category:** {ticket['category']}"
                )

                st.write(
                    f"**Assigned Team:** "
                    f"{ticket['assigned_team']}"
                )

                if isinstance(
                    ticket["source"],
                    list
                ):

                    source_text = ", ".join(
                        ticket["source"]
                    )

                else:

                    source_text = ticket["source"]

                st.write(
                    f"**Knowledge Source:** "
                    f"{source_text}"
                )

                st.success(
                    "The request has been successfully "
                    "recorded in the support system."
                )

                st.divider()

        # ======================================
        # AUDIT TRAIL
        # ======================================

        if os.path.exists("audit_log.json"):

            with open(
                "audit_log.json",
                "r",
                encoding="utf-8"
            ) as file:

                logs = json.load(file)

            st.subheader("📋 Audit Trail")

            st.caption(
                "Recent actions performed by the agent"
            )

            recent_logs = logs[-10:]

            for log in reversed(recent_logs):

                with st.container():

                    st.write(
                        f"🕒 **{log['timestamp']}**"
                    )

                    st.write(
                        f"**{log['event']}**"
                    )

                    st.caption(
                        log["details"]
                    )

                    st.divider()