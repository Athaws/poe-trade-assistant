# 🧙 PoE Trade Helper

**A simple automation overlay for Path of Exile traders**.
Tired of right-clicking and pressing `invite`, `kick`, and saying thanks?
This script pops up a clean little overlay with a button for each step of your trading process — so you can stay focused on mapping.

---

## 💡 Features

* 🧼 Clean popup UI with 1 button per trade step: Invite → Trade → Kick + Thanks
* 📥 Automatically detects trade messages from PoE's `Client.txt`
* 🧽 Removes guild tags like `<GuildName>` from player names
* 🗃 Logs all successful trades to CSV for reference
* 👋 Right-click the button to dismiss popup anytime
* 💤 Auto-dismisses if you ignore it for 3 minutes

---

## 🛠 Requirements

* Python 3.8+
* Run PoE in **Windowed Fullscreen**

Install requirements with:

```bash
pip install -r requirements.txt
```

---

## 🚀 How to Run

1. Clone this repo:

   ```bash
   git clone https://github.com/yourname/poe-trade-helper.git
   cd poe-trade-helper
   ```

2. Install Python dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Edit the `LOG_PATH` at the top of `assistant.py` if your `Client.txt` is in a different location.

4. Run it:

   ```bash
   python assistant.py
   ```
   
   OR

   Double-click `wrapper.bat`

> ✅ You should see a "\[\*] Starting PoE Trade Helper..." message.

---

## 📂 Output

Trades you successfully complete (i.e. click through all steps) are saved to:

```
~/Documents/My Games/Path of Exile/trade_log.csv
```

Each row has:

```
Time | Buyer | Item | Price
```

---


## 📜 License

MIT. Do whatever you want. Just don't resell it to Zana.

---

## 🦄 Credits

Made with ❤️ by an exile who hates clicking more than one button.

Stay sane, exile.
