from rich.console import Console
from rich.table import Table
from rich import box

import datetime
from rich.layout import Layout
from itertools import cycle

from rich.progress import Progress
import shutil

class settings:
    ENVIRONMENT = "DEVELOPMENT"

def print_list(data, table):
    for item in data:
        print_recursive(item, table)


def print_non_dict(key, value, table):
    if value is None or key == value:
        table.add_row(f"[italic]{key}[/italic]", "")
    elif isinstance(value, str):
        table.add_row(
            f"[italic]{key}[/italic]",
            f"[blue]{value}[/blue]",
        )
    elif isinstance(value, int) or isinstance(value, float):
        table.add_row(
            f"[italic]{key}[/italic]",
            f"[green]{value}[/green]",
        )
    elif isinstance(value, datetime.date):
        table.add_row(
            f"[italic]{key}[/italic]",
            f"[cyan]{value.strftime('%m/%d/%Y')}[/cyan]",
        )
    elif isinstance(value, list):
        if all(
            not (isinstance(element, dict) or isinstance(element, list))
            for element in value
        ):
            table.add_row(
                f"[italic]{key}[/italic]",
                f"[magenta]{', '.join([str(element) for element in value])}[/magenta]",
            )

        else:
            subtable = Table(show_header=False, title=None)
            subtable.box = box.SIMPLE
            print_list(value, subtable)
            table.add_row(f"[italic yellow]{key}[/italic yellow]", subtable)

    else:
        table.add_row(
            f"[italic]{key}[/italic]",
            f"[red]{value}[/red]",
        )


def print_recursive(data, table, heading=None):
    if heading:
        table.add_row(f"[blue]{heading}[/blue]")

    if not isinstance(data, dict):
        print_recursive({"": data}, table)
        return

    for key, value in data.items():
        if isinstance(value, dict):
            subtable = Table(show_header=False, title=None)
            subtable.box = box.SIMPLE
            print_recursive(value, subtable)
            table.add_row(f"[italic yellow]{key}[/italic yellow]", subtable)
        else:
            print_non_dict(key, value, table)


def print_rich_info(data, heading=None, use_layout=False):
    if settings.ENVIRONMENT != "DEVELOPMENT":
        return
    console = Console(color_system="truecolor")
    table = Table(heading or "Data", show_header=True)
    print_recursive(data, table)
    table.box = box.ASCII2
    layout = Layout(table) if use_layout else table
    console.print(layout)


test_infos = {
    "text": "test_1",
    "number": 123,
    "date": datetime.date.today(),
    "list": ["one", "two", "three"],
    "dict": {
        "dict_key_text": "test_2",
        "dict_key_number": 456,
        "dict_key_date": datetime.date.today() + datetime.timedelta(days=3),
        "dict_key_list": ["four", "five", "six"],
        "dict_key_mixed_list": [
            "seven",
            8,
            datetime.date.today() + datetime.timedelta(days=4),
        ],
        "dict_key_dict": {
            "subdict_key_text": "test_2",
            "subdict_key_number": 789,
            "subdict_key_date": datetime.date.today() + datetime.timedelta(days=6),
            "subdict_key_list": ["seven", "eight", "nine"],
        },
        "dict_key_mega_mixed_list": [
            "ten",
            11,
            datetime.date.today() + datetime.timedelta(days=5),
            {
                "subdict_key_text": "test_2",
                "subdict_key_number": 789,
                "subdict_key_date": datetime.date.today() + datetime.timedelta(days=6),
                "subdict_key_list": ["seven", "eight", "nine"],
            },
        ],
    },
}


def print_exception():
    console = Console(color_system="truecolor")
    terminal_width = shutil.get_terminal_size().columns or 500
    console.print_exception(width=terminal_width, show_locals=True)


class TaskManager:
    def __init__(self):
        self.progress = None
        self.color_cycle = cycle(["red", "green", "blue", "yellow", "magenta", "cyan"])
        self.task_ids = {}

    def add_task(self, task_name, total):
        if settings.ENVIRONMENT != "DEVELOPMENT":
            return None
        if self.progress is None:
            self.progress = Progress()
        color = next(self.color_cycle)
        task = self.progress.add_task(f"[{color}]{task_name} [{total} steps]", total=total)
        task_id = len(self.progress.tasks) - 1
        self.task_ids[task_id] = {'total': total, 'completed': 0, 'task': task}
        return task_id

    def update_progress(self, task_id, auto_remove=True):
        if settings.ENVIRONMENT != "DEVELOPMENT":
            return
        task_data = self.task_ids.get(task_id)
        if task_data:
            task_data['completed'] += 1
            self.progress.update(task_data['task'], completed=task_data['completed'])
            if auto_remove and task_data['completed'] >= task_data['total']:
                self.remove_task(task_id)

    def remove_task(self, task_id):
        if settings.ENVIRONMENT != "DEVELOPMENT":
            return
        task_data = self.task_ids.pop(task_id, None)
        if task_data:
            self.progress.remove_task(task_data['task'])
            if not self.task_ids:
                self.stop()

    def start(self):
        if settings.ENVIRONMENT != "DEVELOPMENT":
            return
        self.progress.start()

    def stop(self):
        if settings.ENVIRONMENT != "DEVELOPMENT":
            return
        if self.progress is not None:
            self.progress.stop()
            self.progress = None    




