#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import socket
from rich.console import Console
from rich.table import Table

console = Console()

DATABASE_FOLDER = "database"
BLACKLIST_FILE = os.path.join(
    DATABASE_FOLDER,
    "blacklist.txt"
)

# Default suspicious domains/IPs
DEFAULT_BLACKLIST = [
    "malware.test",
    "phishing.test",
    "127.0.0.2",
    "bad-domain.com",
    "evil-site.net"
]


def setup_database():
    """
    Create blacklist database
    """

    os.makedirs(
        DATABASE_FOLDER,
        exist_ok=True
    )

    if not os.path.exists(
        BLACKLIST_FILE
    ):
        with open(
            BLACKLIST_FILE,
            "w",
            encoding="utf-8"
        ) as file:

            for item in DEFAULT_BLACKLIST:
                file.write(
                    item + "\n"
                )


def load_blacklist():
    """
    Load blacklist
    """

    setup_database()

    with open(
        BLACKLIST_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        return set(
            line.strip().lower()
            for line in file
            if line.strip()
        )


def resolve_domain(target):
    """
    Resolve domain -> IP
    """

    try:
        return socket.gethostbyname(
            target
        )

    except Exception:
        return None


def blacklist_check(target):
    """
    Check IP/domain
    """

    blacklist = load_blacklist()

    target = target.lower().strip()

    ip_address = None

    # Domain হলে IP বের করবে
    if "." in target and not target.replace(".", "").isdigit():

        ip_address = resolve_domain(
            target
        )

    table = Table(
        title="CyberShield Blacklist Scan"
    )

    table.add_column(
        "Target",
        style="cyan"
    )

    table.add_column(
        "Status",
        style="red"
    )

    table.add_column(
        "Details",
        style="yellow"
    )

    found = False

    # Domain check
    if target in blacklist:

        found = True

        table.add_row(
            target,
            "BLACKLISTED",
            "Matched blacklist database"
        )

    # IP check
    elif ip_address and ip_address in blacklist:

        found = True

        table.add_row(
            target,
            "BLACKLISTED",
            f"Resolved IP: {ip_address}"
        )

    else:

        table.add_row(
            target,
            "SAFE",
            (
                f"Resolved IP: {ip_address}"
                if ip_address
                else "No issue found"
            )
        )

    console.print(table)

    # Save report
    os.makedirs(
        "reports",
        exist_ok=True
    )

    report_file = (
        "reports/blacklist_report.txt"
    )

    with open(
        report_file,
        "a",
        encoding="utf-8"
    ) as report:

        report.write(
            f"Target: {target}\n"
        )

        report.write(
            f"Resolved IP: "
            f"{ip_address}\n"
        )

        report.write(
            f"Status: "
            f"{'BLACKLISTED' if found else 'SAFE'}\n"
        )

        report.write(
            "-" * 50 + "\n"
        )

    console.print(
        f"\n[green]Report saved:[/green] "
        f"{report_file}"
    )
