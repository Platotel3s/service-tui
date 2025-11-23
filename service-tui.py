#!/usr/bin/env python3
"""
Service TUI manager for systemd (Fedora/Linux).

Features added/fixed in this version:
- Proper scrolling (visible window + offset) so selector never goes outside viewport
- Incremental search/filter (press '/' to start a search; Enter to apply; ESC or empty to clear)
- Shows filter string in header and count of visible services
- Keeps all original features: start/stop, enable/disable, mark/unmark, details with logs
- Marks still persisted to ~/.config/service-tui/marks.json

Usage: save as service-tui.py and run with `python3 service-tui.py` (or run with sudo if you prefer)

Notes:
- Actions call `sudo systemctl ...` so sudo password may be required.
- UI needs a terminal at least ~80 columns wide.

"""

import curses
import subprocess
import json
import os
import shutil
from typing import List, Dict, Tuple, Optional

CONFIG_DIR = os.path.expanduser("~/.config/service-tui")
MARKS_FILE = os.path.join(CONFIG_DIR, "marks.json")

HELP_TEXT = """
Keys:
  Up/Down, k/j   Move
  PgUp/PgDn       Page move
  Enter          Show service details
  s              Start / Stop (toggle)
  e              Enable / Disable (toggle)
  m              Mark / Unmark (remembered list)
  r              Refresh list
  /              Search / Filter
  n               Jump to next match (when searching)
  N               Jump to previous match
  q              Quit

Notes:
- Actions use `sudo systemctl` so you may see a password prompt in the terminal.
- Marked services are saved so you can see them later.
"""


def ensure_config():
    os.makedirs(CONFIG_DIR, exist_ok=True)
    if not os.path.exists(MARKS_FILE):
        with open(MARKS_FILE, "w") as f:
            json.dump([], f)


def load_marks() -> List[str]:
    try:
        with open(MARKS_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return []


def save_marks(marks: List[str]):
    try:
        with open(MARKS_FILE, "w") as f:
            json.dump(marks, f, indent=2)
    except Exception:
        pass


# Fetch systemd services
def fetch_services() -> List[Dict]:
    cmd = ["systemctl", "list-units", "--type=service", "--all", "--no-legend", "--no-pager", "--plain"]
    p = subprocess.run(cmd, capture_output=True, text=True)
    out = p.stdout
    services = []
    for line in out.splitlines():
        parts = line.split(None, 4)
        if len(parts) < 5:
            continue
        unit, load, active, sub, desc = parts
        services.append({
            "unit": unit,
            "load": load,
            "active": active,
            "sub": sub,
            "description": desc,
        })
    return services


def run_action(action: str, unit: str) -> Tuple[bool, str]:
    cmd = ["sudo", "systemctl", action, unit]
    try:
        p = subprocess.run(cmd, capture_output=True, text=True)
        ok = p.returncode == 0
        out = p.stdout + p.stderr
        return ok, out
    except Exception as e:
        return False, str(e)


def draw_main(stdscr, services: List[Dict], cursor: int, offset: int, marks: List[str], status_msg: str, filter_q: Optional[str], filtered_count: int):
    stdscr.erase()
    h, w = stdscr.getmaxyx()

    header = f" Service TUI — total: {len(services)} | visible: {filtered_count} | marked: {len(marks)}"
    if filter_q:
        header += f" | filter: '{filter_q}'"
    stdscr.addstr(0, 0, header[: w - 1], curses.A_REVERSE)

    # Layout columns
    col_unit = 32
    col_load = 8
    col_active = 10
    col_sub = 12

    # space for list: from line 1 to h-3
    top = 1
    bottom = h - 3
    max_lines = bottom - top + 1

    visible = services[offset: offset + max_lines]

    for i, svc in enumerate(visible):
        line_no = top + i
        is_selected = (offset + i) == cursor
        attr = curses.A_REVERSE if is_selected else curses.A_NORMAL
        mark_char = "*" if svc["unit"] in marks else " "
        unit = svc["unit"]
        load = svc["load"]
        active = svc["active"]
        sub = svc["sub"]
        desc = svc["description"]
        line = f"{mark_char} {unit:<{col_unit}} {load:<{col_load}} {active:<{col_active}} {sub:<{col_sub}} {desc}"
        try:
            stdscr.addnstr(line_no, 0, line, w - 1, attr)
        except curses.error:
            pass

    # footer
    footer = "[Enter]details  s=start/stop  e=enable/disable  m=mark  / search  r=refresh  q=quit"
    stdscr.addnstr(h - 2, 0, footer[: w - 1], w - 1, curses.A_REVERSE)

    # status
    stdscr.addnstr(h - 1, 0, (status_msg or "").ljust(w - 1)[: w - 1], w - 1)
    stdscr.refresh()


def show_details_popup(stdscr, svc: Dict):
    h, w = stdscr.getmaxyx()
    win_h = min(14, h - 4)
    win_w = min(100, w - 4)
    win_y = (h - win_h) // 2
    win_x = (w - win_w) // 2
    win = curses.newwin(win_h, win_w, win_y, win_x)
    win.box()
    lines = [f"Unit: {svc['unit']}", f"Load: {svc['load']}", f"Active: {svc['active']}", f"Sub: {svc['sub']}", "", "Description:", svc['description'], "", "Recent logs (last 10 lines):"]
    try:
        logs = subprocess.run(["journalctl", "-u", svc["unit"], "-n", "10", "--no-pager"], capture_output=True, text=True)
        log_lines = logs.stdout.splitlines()[-(win_h - len(lines) - 2) :]
    except Exception as e:
        log_lines = [str(e)]
    lines.extend(log_lines)
    for i, line in enumerate(lines):
        if i + 1 >= win_h - 1:
            break
        trimmed = line[: win_w - 2]
        try:
            win.addnstr(1 + i, 1, trimmed, win_w - 2)
        except curses.error:
            pass
    win.addnstr(win_h - 2, 1, "Press any key to close..."[: win_w - 2], win_w - 2, curses.A_DIM)
    win.refresh()
    win.getch()


def show_help(stdscr):
    h, w = stdscr.getmaxyx()
    lines = HELP_TEXT.strip().splitlines()
    win_h = min(len(lines) + 4, h - 4)
    win_w = min(max(len(l) for l in lines) + 6, w - 4)
    win_y = (h - win_h) // 2
    win_x = (w - win_w) // 2
    win = curses.newwin(win_h, win_w, win_y, win_x)
    win.box()
    for i, l in enumerate(lines):
        try:
            win.addnstr(1 + i, 2, l, win_w - 4)
        except curses.error:
            pass
    win.addnstr(win_h - 2, 2, "Press any key to close...", win_w - 4, curses.A_DIM)
    win.refresh()
    win.getch()


def confirm_prompt(stdscr, prompt: str) -> bool:
    h, w = stdscr.getmaxyx()
    win_h = 5
    win_w = min(len(prompt) + 10, w - 4)
    win_y = (h - win_h) // 2
    win_x = (w - win_w) // 2
    win = curses.newwin(win_h, win_w, win_y, win_x)
    win.box()
    win.addnstr(1, 2, prompt[: win_w - 4], win_w - 4)
    win.addnstr(2, 2, "y = yes, n = no", win_w - 4)
    win.refresh()
    while True:
        k = win.getch()
        if k in (ord("y"), ord("Y")):
            return True
        if k in (ord("n"), ord("N")):
            return False


def prompt_input(stdscr, prompt: str) -> Optional[str]:
    curses.echo()
    h, w = stdscr.getmaxyx()
    win = curses.newwin(3, w - 4, h - 4, 2)
    win.box()
    win.addnstr(1, 2, prompt, w - 8)
    win.refresh()
    win.move(1, 2 + len(prompt))
    try:
        s = win.getstr(1, 2 + len(prompt), 256)
        val = s.decode(errors="ignore").strip()
    except Exception:
        val = None
    curses.noecho()
    return val


def apply_filter(all_services: List[Dict], q: Optional[str]) -> List[Dict]:
    if not q:
        return list(all_services)
    ql = q.lower()
    out = []
    for s in all_services:
        if ql in s['unit'].lower() or ql in s['description'].lower():
            out.append(s)
    return out


def main_loop(stdscr):
    curses.curs_set(0)
    ensure_config()
    marks = load_marks()
    all_services = fetch_services()
    filter_q: Optional[str] = None
    services = apply_filter(all_services, filter_q)

    cursor = 0
    offset = 0
    status_msg = "ready"

    def clamp_cursor():
        nonlocal cursor
        if cursor < 0:
            cursor = 0
        if cursor >= len(services):
            cursor = max(0, len(services) - 1)

    while True:
        clamp_cursor()
        # compute offset so that cursor is visible
        h, w = stdscr.getmaxyx()
        top = 1
        bottom = h - 3
        max_lines = max(1, bottom - top + 1)

        if cursor < offset:
            offset = cursor
        elif cursor >= offset + max_lines:
            offset = cursor - max_lines + 1

        draw_main(stdscr, services, cursor, offset, marks, status_msg, filter_q, len(services))

        k = stdscr.getch()
        max_idx = len(services) - 1

        if k in (curses.KEY_DOWN, ord('j')):
            cursor = min(max_idx, cursor + 1)
        elif k in (curses.KEY_UP, ord('k')):
            cursor = max(0, cursor - 1)
        elif k == curses.KEY_NPAGE:  # Page Down
            cursor = min(max_idx, cursor + max(1, max_lines - 1))
        elif k == curses.KEY_PPAGE:  # Page Up
            cursor = max(0, cursor - max(1, max_lines - 1))
        elif k == ord('q'):
            save_marks(marks)
            break
        elif k == ord('r'):
            status_msg = "refreshing..."
            draw_main(stdscr, services, cursor, offset, marks, status_msg, filter_q, len(services))
            all_services = fetch_services()
            services = apply_filter(all_services, filter_q)
            status_msg = "refreshed"
        elif k == ord('h'):
            show_help(stdscr)
            status_msg = "help closed"
        elif k == ord('m'):
            if services:
                unit = services[cursor]["unit"]
                if unit in marks:
                    marks.remove(unit)
                    status_msg = f"unmarked {unit}"
                else:
                    marks.append(unit)
                    status_msg = f"marked {unit}"
                save_marks(marks)
        elif k == ord('\n') or k == curses.KEY_ENTER:
            if services:
                show_details_popup(stdscr, services[cursor])
        elif k == ord('s'):
            if services:
                unit = services[cursor]["unit"]
                cur_active = services[cursor]["active"]
                if cur_active == "active":
                    ok = confirm_prompt(stdscr, f"Stop {unit}? (will run sudo systemctl stop)")
                    if ok:
                        ok2, out = run_action("stop", unit)
                        status_msg = ("stopped" if ok2 else f"error: {out.strip()[:60]}")
                else:
                    ok = confirm_prompt(stdscr, f"Start {unit}? (will run sudo systemctl start)")
                    if ok:
                        ok2, out = run_action("start", unit)
                        status_msg = ("started" if ok2 else f"error: {out.strip()[:60]}")
                all_services = fetch_services()
                services = apply_filter(all_services, filter_q)
        elif k == ord('e'):
            if services:
                unit = services[cursor]["unit"]
                p = subprocess.run(["systemctl", "is-enabled", unit], capture_output=True, text=True)
                enabled = p.returncode == 0
                if enabled:
                    ok = confirm_prompt(stdscr, f"Disable {unit}? (will run sudo systemctl disable)")
                    if ok:
                        ok2, out = run_action("disable", unit)
                        status_msg = ("disabled" if ok2 else f"error: {out.strip()[:60]}")
                else:
                    ok = confirm_prompt(stdscr, f"Enable {unit}? (will run sudo systemctl enable)")
                    if ok:
                        ok2, out = run_action("enable", unit)
                        status_msg = ("enabled" if ok2 else f"error: {out.strip()[:60]}")
                all_services = fetch_services()
                services = apply_filter(all_services, filter_q)
        elif k == ord('/'):
            val = prompt_input(stdscr, "Search: ")
            if val is None or val == "":
                filter_q = None
            else:
                filter_q = val
            services = apply_filter(all_services, filter_q)
            cursor = 0
            offset = 0
            status_msg = f"filter set to '{filter_q}'" if filter_q else "filter cleared"
        elif k == ord('n'):
            # next marked match: move cursor to next service that matches filter_q (simple move)
            if filter_q and services:
                start = cursor + 1
                found = False
                for i in range(start, len(services)):
                    if filter_q.lower() in services[i]['unit'].lower() or filter_q.lower() in services[i]['description'].lower():
                        cursor = i
                        found = True
                        break
                if not found:
                    status_msg = "no more matches"
        elif k == ord('N'):
            if filter_q and services:
                start = cursor - 1
                found = False
                for i in range(start, -1, -1):
                    if filter_q.lower() in services[i]['unit'].lower() or filter_q.lower() in services[i]['description'].lower():
                        cursor = i
                        found = True
                        break
                if not found:
                    status_msg = "no previous match"
        else:
            status_msg = ""


def run():
    if shutil.get_terminal_size().columns < 80:
        print("Please enlarge your terminal (min width 80 columns)")
        return
    curses.wrapper(main_loop)


if __name__ == "__main__":
    run()
