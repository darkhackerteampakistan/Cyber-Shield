#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import time
from rich.console import Console
from rich.table import Table

console = Console()

try:
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler
except ImportError:
    console.print(
        "[bold red]watchdog not installed![/bold red]"
    )
    console.print(
        "[cyan]Run:[/cyan] pip install watchdog"
    )
    exit()


class CyberMonitor(FileSystemEventHandler):
    """
    Real-time file monitor
    """

    def __init__(self):
        self.events_log = []

    def log_event(self, event_type, path):

        filename = os.path.basename(path)

        event_info = {
            "type": event_type,
            "path": path
        }

        self.events_log.append(event_info)

        table = Table(
            title="CyberShield Monitor Alert"
        )

        table.add_column(
            "Event",
            style="red"
        )

        table.add_column(
            "File",
            style="cyan"
        )

        table.add_column(
            "Path",
            style="yellow"
        )

        table.add_row(
            event_type,
            filename,
            path[:70]
        )

        console.print(table)

        self.save_log(
            event_type,
            path
        )

    def save_log(
        self,
        event_type,
        path
    ):
        """
        Save monitor logs
        """

        os.makedirs(
            "reports",
            exist_ok=True
        )

        log_file = (
            "reports/monitor_log.txt"
        )

        with open(
            log_file,
            "a",
            encoding="utf-8"
        ) as log:

            log.write(
                f"[{time.ctime()}] "
                f"{event_type} -> {path}\n"
            )

    def on_created(
        self,
        event
    ):
        if not event.is_directory:
            self.log_event(
                "CREATED",
                event.src_path
            )

    def on_deleted(
        self,
        event
    ):
        if not event.is_directory:
            self.log_event(
                "DELETED",
                event.src_path
            )

    def on_modified(
        self,
        event
    ):
        if not event.is_directory:
            self.log_event(
                "MODIFIED",
                event.src_path
            )

    def on_moved(
        self,
        event
    ):
        if not event.is_directory:
            self.log_event(
                "MOVED",
                event.dest_path
            )


def start_monitor(
    monitor_path="/sdcard"
):
    """
    Start realtime monitor
    """

    if not os.path.exists(
        monitor_path
    ):
        console.print(
            "[bold red]Path not found![/bold red]"
        )
        return

    console.print(
        f"\n[green]Monitoring:[/green] "
        f"{monitor_path}"
    )

    console.print(
        "[yellow]Press CTRL + C to stop[/yellow]"
    )

    event_handler = CyberMonitor()

    observer = Observer()

    observer.schedule(
        event_handler,
        monitor_path,
        recursive=True
    )

    observer.start()

    try:
        while True:
            time.sleep(1)

    except KeyboardInterrupt:

        observer.stop()

        console.print(
            "\n[bold red]Monitor stopped[/bold red]"
        )

    observer.join()
