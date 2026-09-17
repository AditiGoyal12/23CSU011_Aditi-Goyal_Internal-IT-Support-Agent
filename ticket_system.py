import json
import os
from datetime import datetime


TICKET_FILE = "tickets.json"


def create_ticket(
    issue,
    category,
    priority,
    status,
    assigned_team,
    source
):
    # Create ticket ID
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    ticket_id = f"IT-{timestamp}"

    # Create ticket
    ticket = {
        "ticket_id": ticket_id,
        "created_at": datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        ),
        "category": category,
        "priority": priority,
        "status": status,
        "assigned_team": assigned_team,
        "issue": issue,
        "source": source
    }

    # Load existing tickets
    if os.path.exists(TICKET_FILE):

        with open(
            TICKET_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            tickets = json.load(file)

    else:

        tickets = []

    # Add new ticket
    tickets.append(ticket)

    # Save tickets
    with open(
        TICKET_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            tickets,
            file,
            indent=4
        )

    return ticket