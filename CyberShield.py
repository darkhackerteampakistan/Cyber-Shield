#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import time
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.progress import Progress, BarColumn, TextColumn

# Import modules
try:
    from scanner import full_scan
    from permissions import apk_permission_scan
    from monitor import start_monitor
    from blacklist import blacklist_check
except Exception as e:
    print(f"[ERROR] Missing module: {e}")
    print("Make sure scanner.py, permissions.py, monitor.py, blacklist.py exist.")
    sys.exit(1)

console = Console()


def clear():
    os.system("clear")


def banner():
    clear()
    console.print(Panel.fit(
        "[bold cyan]CyberShield Security Tool[/bold cyan]\n"
        "[green]Antivirus + Firewall Style Scanner[/green]\n"
        "[yellow]Termux / Python Edition[/yellow]",
        border_style="blue"
    ))


def loading(text="Loading"):
    with Progress(
        TextColumn("[cyan]{task.description}"),
        BarColumn(),
        TextColumn("[green]{task.percentage:>3.0f}%")
    ) as progress:

        task = progress.add_task(text, total=100)

        for _ in range(100):
            time.sleep(0.01)
            progress.update(task, advance=1)


def menu():
    while True:
        banner()

        console.print("""
[1] Full Storage Scan
[2] Suspicious APK Permission Check
[3] IP / Domain Blacklist Checker
[4] Real-Time File Monitor
[5] Exit
""")

        choice = Prompt.ask(
            "[bold green]Select option[/bold green]"
        )

        if choice == "1":
            loading("Scanning storage...")
            path = Prompt.ask(
                "Enter path",
                default="/sdcard"
            )
            full_scan(path)

        elif choice == "2":
            loading("Checking APK permissions...")
            apk_path = Prompt.ask(
                "Enter APK path"
            )
            apk_permission_scan(apk_path)

        elif choice == "3":
            loading("Checking blacklist...")
            target = Prompt.ask(
                "Enter IP or domain"
            )
            blacklist_check(target)

        elif choice == "4":
            loading("Starting monitor...")
            monitor_path = Prompt.ask(
                "Enter monitor path",
                default="/sdcard"
            )
            start_monitor(monitor_path)

        elif choice == "5":
            console.print(
                "[red]Exiting CyberShield...[/red]"
            )
            sys.exit()

        else:
            console.print(
                "[bold red]Invalid option![/bold red]"
            )

        input("\nPress Enter to continue...")


if __name__ == "__main__":
    menu()
