"""
Portfolio Sample Notice:
This is a sanitized and simplified portfolio version of an automation project.
Sensitive data, credentials, and proprietary implementation details have been removed.

Purpose:
Sync NinjaOne tickets into ClickUp tasks using REST APIs and local ID mapping.
"""

import json
import sys
from pathlib import Path
from datetime import datetime

import requests


BASE_DIR = Path(__file__).parent
CONFIG_FILE = BASE_DIR / "config.local.json"
MAPPING_FILE = BASE_DIR / "mapping.json"


def log(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")


def load_json(path, default):
    if not path.exists():
        return default

    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def save_json(path, data):
    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2)


def validate_config(config):
    required_fields = [
        "ninja_base_url",
        "ninja_client_id",
        "ninja_client_secret",
        "ninja_board_id",
        "clickup_token",
        "clickup_list_id"
    ]

    missing = []

    for field in required_fields:
        if not config.get(field):
            missing.append(field)

    if missing:
        raise ValueError(f"Missing required config values: {', '.join(missing)}")


def get_ninja_token(config):
    log("Authenticating with NinjaOne API")

    url = f"{config['ninja_base_url'].rstrip('/')}/ws/oauth/token"

    data = {
        "grant_type": "client_credentials",
        "client_id": config["ninja_client_id"],
        "client_secret": config["ninja_client_secret"],
        "scope": "monitoring management"
    }

    response = requests.post(url, data=data, timeout=30)
    response.raise_for_status()

    return response.json()["access_token"]


def get_ninja_tickets(config, token):
    log("Retrieving tickets from NinjaOne")

    url = (
        f"{config['ninja_base_url'].rstrip('/')}"
        f"/api/v2/ticketing/trigger/board/{config['ninja_board_id']}/run"
    )

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json"
    }

    response = requests.post(url, headers=headers, json={}, timeout=30)
    response.raise_for_status()

    data = response.json()

    if isinstance(data, list):
        return data

    if isinstance(data, dict):
        return (
            data.get("tickets")
            or data.get("data")
            or data.get("results")
            or []
        )

    return []


def normalize_ticket(ticket):
    ticket_id = str(ticket.get("id", "")).strip()

    subject = (
        ticket.get("subject")
        or ticket.get("title")
        or ticket.get("name")
        or f"Ninja Ticket {ticket_id}"
    )

    description = (
        ticket.get("description")
        or ticket.get("summary")
        or ticket.get("body")
        or "No description provided."
    )

    status = (
        ticket.get("status")
        or ticket.get("state")
        or "Unknown"
    )

    priority = (
        ticket.get("priority")
        or "Unknown"
    )

    return {
        "id": ticket_id,
        "subject": subject,
        "description": description,
        "status": status,
        "priority": priority
    }


def create_clickup_task(config, ticket):
    log(f"Creating ClickUp task for Ninja ticket {ticket['id']}")

    url = f"https://api.clickup.com/api/v2/list/{config['clickup_list_id']}/task"

    headers = {
        "Authorization": config["clickup_token"],
        "Content-Type": "application/json"
    }

    payload = {
        "name": f"[Ninja #{ticket['id']}] {ticket['subject']}",
        "description": (
            "Portfolio Sample Sync\n\n"
            "This task was created by a sanitized NinjaOne → ClickUp sync script.\n\n"
            f"Ninja Ticket ID: {ticket['id']}\n"
            f"Status: {ticket['status']}\n"
            f"Priority: {ticket['priority']}\n\n"
            f"Description:\n{ticket['description']}"
        ),
        "tags": ["ninjaone", "portfolio-sample"]
    }

    response = requests.post(url, headers=headers, json=payload, timeout=30)
    response.raise_for_status()

    return response.json()["id"]


def sync_tickets():
    log("Starting NinjaOne → ClickUp sync")

    config = load_json(CONFIG_FILE, {})
    validate_config(config)

    mapping = load_json(MAPPING_FILE, {})

    token = get_ninja_token(config)
    raw_tickets = get_ninja_tickets(config, token)

    created_count = 0
    skipped_count = 0
    invalid_count = 0

    for raw_ticket in raw_tickets:
        ticket = normalize_ticket(raw_ticket)

        if not ticket["id"]:
            invalid_count += 1
            log("Skipping ticket with missing ID")
            continue

        if ticket["id"] in mapping:
            skipped_count += 1
            continue

        clickup_task_id = create_clickup_task(config, ticket)

        mapping[ticket["id"]] = {
            "clickup_task_id": clickup_task_id,
            "synced_at": datetime.now().isoformat()
        }

        created_count += 1
        log(f"Created ClickUp task {clickup_task_id} for Ninja ticket {ticket['id']}")

    save_json(MAPPING_FILE, mapping)

    log("Sync complete")
    log(f"Created: {created_count}")
    log(f"Skipped existing: {skipped_count}")
    log(f"Invalid tickets skipped: {invalid_count}")


if __name__ == "__main__":
    try:
        sync_tickets()
    except Exception as error:
        log(f"ERROR: {error}")
        sys.exit(1)
