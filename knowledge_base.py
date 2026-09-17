import os
import re


KNOWLEDGE_BASE_FOLDER = "knowledge_base"


def load_knowledge_base():

    documents = []

    for filename in os.listdir(KNOWLEDGE_BASE_FOLDER):

        if filename.endswith(".txt"):

            file_path = os.path.join(
                KNOWLEDGE_BASE_FOLDER,
                filename
            )

            with open(
                file_path,
                "r",
                encoding="utf-8"
            ) as file:

                content = file.read()

            documents.append({
                "filename": filename,
                "content": content
            })

    return documents


def search_knowledge_base(query):

    documents = load_knowledge_base()

    query_lower = query.lower()

    # ------------------------------------------
    # Detect specific IT topics
    # ------------------------------------------

    topic_keywords = {

        "email": [
            "outlook",
            "email",
            "emails",
            "mailbox",
            "mail"
        ],

        "vpn": [
            "vpn"
        ],

        "hardware": [
            "laptop",
            "desktop",
            "computer",
            "hardware",
            "charger",
            "power",
            "screen",
            "device"
        ],

        "security": [
            "password",
            "credential",
            "credentials",
            "phishing",
            "suspicious",
            "unauthorized",
            "compromised",
            "malware",
            "ransomware",
            "stolen",
            "lost device"
        ]
    }

    detected_topic = None

    for topic, keywords in topic_keywords.items():

        if any(
            keyword in query_lower
            for keyword in keywords
        ):

            detected_topic = topic
            break

    # ------------------------------------------
    # Map topic to approved knowledge document
    # ------------------------------------------

    topic_documents = {

        "email": "email_troubleshooting.txt",

        "vpn": "vpn_troubleshooting.txt",

        "hardware": "hardware_support_policy.txt",

        "security": "security_incident_policy.txt"
    }

    # ------------------------------------------
    # If a known topic is detected,
    # return only its relevant document
    # ------------------------------------------

    if detected_topic in topic_documents:

        target_document = topic_documents[detected_topic]

        for document in documents:

            if document["filename"] == target_document:

                return [{
                    "filename": document["filename"],
                    "content": document["content"],
                    "score": 1
                }]

        return []

    # ------------------------------------------
    # Unknown topic
    # ------------------------------------------

    return []