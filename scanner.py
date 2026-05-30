#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import hashlib
from rich.console import Console
from rich.table import Table
from rich.progress import Progress

console = Console()

# Suspicious extensions
SUSPICIOUS_EXTENSIONS = {
    ".apk", ".exe", ".bat", ".cmd",
    ".sh", ".py", ".js", ".jar"
}

# Suspicious keywords
SUSPICIOUS_NAMES = [
    "hack", "payload", "keylogger",
    "stealer", "rat", "inject",
    "crack", "token", "spam"
]

REPORT_FOLDER = "reports"

if not os.path.exists(REPORT_FOLDER):
    os.makedirs(REPORT_FOLDER)


def calculate_hash(file_path):
    """SHA256 hash"""
    sha256 = hashlib.sha256()

    try:
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                sha256.update(chunk)

        return sha256.hexdigest()

    except Exception:
        return "HASH_ERROR"


def suspicious_check(file_path):
    """Check suspicious file"""
    name = os.path.basename(file_path).lower()

    ext = os.path.splitext(name)[1]

    score = 0
    reasons = []

    # Extension check
    if ext in SUSPICIOUS_EXTENSIONS:
        score += 2
        reasons.append(f"Suspicious extension ({ext})")

    # Keyword check
    for word in SUSPICIOUS_NAMES:
        if word in name:
            score += 3
            reasons.append(f"Keyword detected ({word})")

    # Hidden file
    if name.startswith("."):
        score += 1
        reasons.append("Hidden file")

    return score, reasons


def save_report(results):
    """Save scan report"""

    report_file = os.path.join(
        REPORT_FOLDER,
        "scan_report.txt"
    )

    with open(report_file, "w", encoding="utf-8") as f:

        f.write("==== CyberShield Scan Report ====\n\n")

        for item in results:
            f.write(
                f"FILE: {item['path']}\n"
            )

            f.write(
                f"SHA256: {item['hash']}\n"
            )

            f.write(
                f"SCORE: {item['score']}\n"
            )

            f.write(
                f"REASONS: {', '.join(item['reasons'])}\n"
            )

            f.write("-" * 60 + "\n")

    console.print(
        f"[green]Report saved:[/green] {report_file}"
    )


def full_scan(scan_path="/sdcard"):
    """Full storage scan"""

    console.print(
        f"\n[cyan]Scanning:[/cyan] {scan_path}"
    )

    results = []

    table = Table(
        title="CyberShield Scan Results"
    )

    table.add_column(
        "Risk",
        style="red"
    )

    table.add_column(
        "File",
        style="cyan"
    )

    table.add_column(
        "Reason",
        style="yellow"
    )

    files_list = []

    # Collect files
    for root, dirs, files in os.walk(scan_path):
        for file in files:
            full_path = os.path.join(
                root,
                file
            )
            files_list.append(full_path)

    total_files = len(files_list)

    console.print(
        f"[green]Total files:[/green] {total_files}"
    )

    with Progress() as progress:

        task = progress.add_task(
            "[green]Scanning...",
            total=total_files
        )

        for file_path in files_list:

            try:
                score, reasons = suspicious_check(
                    file_path
                )

                if score > 0:

                    file_hash = calculate_hash(
                        file_path
                    )

                    results.append({
                        "path": file_path,
                        "hash": file_hash,
                        "score": score,
                        "reasons": reasons
                    })

                    table.add_row(
                        str(score),
                        file_path[:50],
                        ", ".join(reasons)
                    )

            except Exception:
                pass

            progress.update(
                task,
                advance=1
            )

    console.print(table)

    console.print(
        f"\n[bold red]Suspicious files:[/bold red] {len(results)}"
    )

    save_report(results)
