#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from rich.console import Console
from rich.table import Table

console = Console()

# Dangerous permissions
DANGEROUS_PERMISSIONS = {
    "android.permission.READ_SMS",
    "android.permission.SEND_SMS",
    "android.permission.RECEIVE_SMS",
    "android.permission.READ_CONTACTS",
    "android.permission.WRITE_CONTACTS",
    "android.permission.RECORD_AUDIO",
    "android.permission.CAMERA",
    "android.permission.ACCESS_FINE_LOCATION",
    "android.permission.ACCESS_COARSE_LOCATION",
    "android.permission.READ_CALL_LOG",
    "android.permission.WRITE_CALL_LOG",
    "android.permission.SYSTEM_ALERT_WINDOW",
    "android.permission.REQUEST_INSTALL_PACKAGES",
    "android.permission.QUERY_ALL_PACKAGES",
    "android.permission.BIND_ACCESSIBILITY_SERVICE",
    "android.permission.READ_EXTERNAL_STORAGE",
    "android.permission.WRITE_EXTERNAL_STORAGE",
    "android.permission.MANAGE_EXTERNAL_STORAGE"
}


def apk_permission_scan(apk_path):
    """
    Scan APK dangerous permissions
    """

    if not os.path.exists(apk_path):
        console.print(
            "[bold red]APK file not found![/bold red]"
        )
        return

    try:
        from androguard.misc import AnalyzeAPK

    except ImportError:
        console.print(
            "[yellow]androguard not installed[/yellow]"
        )
        console.print(
            "[cyan]Run:[/cyan] pip install androguard"
        )
        return

    console.print(
        f"\n[cyan]Scanning APK:[/cyan] {apk_path}"
    )

    try:
        a, d, dx = AnalyzeAPK(apk_path)

        permissions = a.get_permissions()

        if not permissions:
            console.print(
                "[green]No permissions found[/green]"
            )
            return

        table = Table(
            title="APK Permission Report"
        )

        table.add_column(
            "Permission",
            style="cyan"
        )

        table.add_column(
            "Risk",
            style="red"
        )

        dangerous_count = 0

        for permission in permissions:

            if permission in DANGEROUS_PERMISSIONS:

                risk = "HIGH RISK"
                dangerous_count += 1

            else:
                risk = "Normal"

            table.add_row(
                permission,
                risk
            )

        console.print(table)

        console.print(
            f"\n[bold red]Dangerous Permissions:[/bold red] "
            f"{dangerous_count}"
        )

        # Save report
        os.makedirs(
            "reports",
            exist_ok=True
        )

        report_path = (
            "reports/apk_permissions_report.txt"
        )

        with open(
            report_path,
            "w",
            encoding="utf-8"
        ) as report:

            report.write(
                "==== APK Permission Report ====\n\n"
            )

            report.write(
                f"APK: {apk_path}\n\n"
            )

            for permission in permissions:

                status = (
                    "HIGH RISK"
                    if permission in
                    DANGEROUS_PERMISSIONS
                    else "Normal"
                )

                report.write(
                    f"{permission} -> {status}\n"
                )

        console.print(
            f"\n[green]Report saved:[/green] "
            f"{report_path}"
        )

    except Exception as e:
        console.print(
            f"[bold red]Scan Error:[/bold red] {e}"
        )
