import csv
import os
import re
import threading
import time
import tkinter as tk
from datetime import datetime

import keyboard
import pygetwindow as gw

LOG_PATH = os.path.abspath(
    r"D:\SteamLibrary\steamapps\common\Path of Exile\logs\LatestClient.txt"
)
DOCS_PATH = os.path.expanduser(r"~/Documents/My Games/Path of Exile")
CSV_LOG = os.path.join(DOCS_PATH, "trade_log.csv")
TIMEOUT_SECONDS = 180
open_popups = 0

if not os.path.exists(DOCS_PATH):
    os.makedirs(DOCS_PATH)

if not os.path.exists(CSV_LOG):
    with open(CSV_LOG, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Time", "Buyer", "Item", "Price"])


def parse_trade_whisper(line):
    pattern = r"@From (.+?): Hi, I would like to buy your (.+?) listed for (.+?) in"
    match = re.search(pattern, line)
    if match:
        buyer = match.group(1)
        item = match.group(2)
        price = match.group(3)

        # Remove guild name if present (e.g., <GuildName> PlayerName)
        buyer = re.sub(r"^<[^>]+>\s*", "", buyer)

        return buyer, item, price
    return None


def log_trade(buyer, item, price):
    with open(CSV_LOG, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([datetime.now().isoformat(), buyer, item, price])


def focus_poe_window():
    try:
        for window in gw.getWindowsWithTitle("Path of Exile"):
            if "Firefox" in window.title:
                continue
            if window.title == "Path of Exile" and not window.isActive:
                window.activate()
                time.sleep(0.1)
            return True
    except Exception as e:
        print(f"[!] Could not focus PoE window: {e}")
    return False


def send_chat_command(command):
    try:
        if focus_poe_window():
            keyboard.send("enter")
            time.sleep(0.1)
            keyboard.write(command)
            time.sleep(0.1)
            keyboard.send("enter")
        else:
            print("[!] Could not focus PoE window.")
    except Exception as e:
        print(f"[!] Failed to send command: {command} | {e}")


def show_trade_popup(buyer, item, price):
    global open_popups
    open_popups += 1

    box_width = 200
    box_height = 100
    offset_x = 300
    offset_y = 200 + (open_popups - 1) * box_height + 40  # each popup 40px lower

    popup = tk.Tk()
    popup.title(f"Trade: {buyer}")
    popup.geometry(f"{box_width}x{box_height}+{offset_x}+{offset_y}")

    popup.attributes("-topmost", True)
    popup.overrideredirect(True)

    frame = tk.Frame(popup, bg="black", bd=2)
    frame.pack(expand=True, fill="both")

    label = tk.Label(
        frame,
        text=f"{buyer} wants to buy:\n{item}\nfor {price}",
        wraplength=280,
        fg="white",
        bg="black",
    )
    label.pack(pady=10)

    step_index = {"i": 0}

    def invite_action():
        send_chat_command(f"/invite {buyer}")

    def trade_action():
        send_chat_command(f"/tradewith {buyer}")

    def kick_and_thanks_action():
        send_chat_command(f"/kick {buyer}")
        send_chat_command(f"@{buyer} Thanks! Stay sane, Exile..")
        log_trade(buyer, item, price)
        safe_destroy()

    steps = [
        ("Invite", invite_action),
        ("Trade", trade_action),
        ("Kick + Thanks", kick_and_thanks_action),
    ]

    def safe_destroy():
        nonlocal popup
        try:
            if popup and popup.winfo_exists():
                popup.destroy()
        except Exception:
            pass
        global open_popups
        open_popups -= 1

    def handle_click(event):
        if event.widget != action_button:
            return
        if event.num == 1:
            i = step_index["i"]
            if i < len(steps):
                _, action = steps[i]
                action()
                step_index["i"] += 1
                if step_index["i"] < len(steps):
                    action_button.config(text=steps[step_index["i"]][0])
                else:
                    safe_destroy()
        elif event.num == 3:
            safe_destroy()

    action_button = tk.Button(frame, text=steps[0][0], width=20)
    action_button.bind("<Button-1>", handle_click)
    action_button.bind("<Button-3>", handle_click)
    action_button.pack(pady=5)

    def auto_dismiss():
        time.sleep(TIMEOUT_SECONDS)
        safe_destroy()

    threading.Thread(target=auto_dismiss, daemon=True).start()
    popup.mainloop()


def poll_log_file():
    print("[*] Polling PoE log file...")
    last_size = 0
    if not os.path.exists(LOG_PATH):
        print("[!] Log file not found.")
        return

    with open(LOG_PATH, "r", encoding="utf-8") as f:
        f.seek(0, os.SEEK_END)
        last_size = f.tell()

    while True:
        try:
            current_size = os.path.getsize(LOG_PATH)
            if current_size > last_size:
                with open(LOG_PATH, "r", encoding="utf-8") as f:
                    f.seek(last_size)
                    new_lines = f.readlines()
                    last_size = f.tell()

                for line in new_lines:
                    if "@From" in line and "listed for" in line:
                        result = parse_trade_whisper(line)
                        if result:
                            buyer, item, price = result
                            print(f"[TRADE DETECTED] {buyer} wants {item} for {price}")
                            threading.Thread(
                                target=show_trade_popup,
                                args=(buyer, item, price),
                                daemon=True,
                            ).start()
            time.sleep(1)
        except Exception as e:
            print("[!] Error reading log file:", e)
            time.sleep(5)


def main():
    print("[*] Starting PoE Trade Helper...")
    if not os.path.exists(LOG_PATH):
        print("Error: Could not find Client.txt or LatestClient.txt")
        return

    try:
        with open(LOG_PATH, "r", encoding="utf-8") as f:
            lines = f.readlines()
            if lines:
                print("[*] Last line of log file:", lines[-1].strip())
            else:
                print("[*] Log file is empty.")
    except Exception as e:
        print("[!] Failed to read log file:", e)
        return

    try:
        poll_log_file()
    except KeyboardInterrupt:
        print("\n[!] Exiting. Goodbye!")


if __name__ == "__main__":
    main()
