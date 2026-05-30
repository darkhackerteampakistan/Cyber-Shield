#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import time
from rich.console import Console
from rich.panel import Panel
from rich.progress import (
    Progress,
    SpinnerColumn,
    BarColumn,
    TextColumn,
    TimeElapsedColumn
)
from rich.table import Table
from rich.align import Align

console = Console()


def clear():
    """
    Clear terminal
    """
    os.system("clear")


def banner():
    """
    CyberShield banner
    """

    clear()

    title = r"""
 ██████╗██╗   ██╗██████╗ ███████╗██████╗ 
██╔════╝╚██╗ ██╔╝██╔══██╗██╔════╝██╔══██╗
██║      ╚████╔╝ ██████╔╝█████╗  ██████╔╝
██║       ╚██╔╝  ██╔══██╗██╔══╝  ██╔══██╗
╚██████╗   ██║   ██████╔╝███████╗██║  ██║
 ╚═════╝   ╚═╝   ╚═════╝ ╚══════╝╚═╝  ╚═╝
"""

    panel = Panel.fit(
        f"[bold cyan]{title}[/bold cyan]\n"
        "[bold green]CyberShield Security Suite[/bold green]\n"
        "[yellow]Antivirus + Firewall Style Scanner[/yellow]\n"
        "[white]Termux / Python Edition[/white]",
        border_style="bright_blue"
    )

    console.print(
        Align.center(panel)
    )


def loading_screen(
    text="Loading..."
):
    """
    Progress bar
    """

    with Progress(
        SpinnerColumn(),
        TextColumn(
            "[cyan]{task.description}"
        ),
        BarColumn(),
        TextColumn(
            "[green]{task.percentage:>3.0f}%"
        ),
        TimeElapsedColumn(),
        console=console
    ) as progress:

        task = progress.add_task(
            text,
            total=100
        )

        for _ in range(100):
            time.sleep(0.01)
            progress.update(
                task,
                advance=1
            )


def menu():
    """
    Main menu UI
    """

    table = Table(
        title="CyberShield Menu",
        border_style="blue"
    )

    table.add_column(
        "Option",
        justify="center",
        style="cyan"
    )

    table.add_column(
        "Feature",
        style="green"
    )

    table.add_row(
        "1",
        "Full Storage Scan"
    )

    table.add_row(
        "2",
        "APK Permission Checker"
    )

    table.add_row(
        "3",
        "IP / Domain Blacklist"
    )

    table.add_row(
        "4",
        "Real-Time Monitor"
    )

    table.add_row(
        "5",
        "Exit"
    )

    console.print(table)


def success(
    message
):
    """
    Success message
    """

    console.print(
        f"[bold green][✓][/bold green] "
        f"{message}"
    )


def error(
    message
):
    """
    Error message
    """

    console.print(
        f"[bold red][✗][/bold red] "
        f"{message}"
    )


def warning(
    message
):
    """
    Warning message
    """

    console.print(
        f"[bold yellow][!][/bold yellow] "
        f"{message}"
    )


def info(
    message
):
    """
    Info message
    """

    console.print(
        f"[bold cyan][*][/bold cyan] "
        f"{message}"
    )
