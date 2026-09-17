import json
import os
from datetime import datetime


AUDIT_FILE = "audit_log.json"


def log_event(event, details):

    audit_entry = {
        "timestamp": datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        ),
        "event": event,
        "details": details
    }

    # Load existing audit logs
    if os.path.exists(AUDIT_FILE):

        with open(
            AUDIT_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            logs = json.load(file)

    else:

        logs = []

    # Add new event
    logs.append(audit_entry)

    # Save audit log
    with open(
        AUDIT_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            logs,
            file,
            indent=4
        )
        