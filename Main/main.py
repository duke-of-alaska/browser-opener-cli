import json
import os
import subprocess
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE = os.path.join(
    BASE_DIR, "..", "JSON Config", "config.json"
)

def load_config():
    """Reads user-defined browser paths from the JSON config file."""
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            print(
                f"Warning: '{CONFIG_FILE}' is corrupted. Using default paths."
            )

    return {"chrome_path": "", "firefox_path": "", "edge_path": ""}

def get_browser_path(browser_name, config):
    """Finds the browser path from config, or drops back to Windows defaults."""
    config_key = f"{browser_name.lower()}_path"
    if config.get(config_key):
        return config[config_key]
    defaults = {
        "chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        "firefox": r"C:\Program Files\Mozilla Firefox\firefox.exe",
        "edge": r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    }

    return defaults.get(browser_name.lower())

def open_browser(browser_name, url):
    """Launches the selected browser with the given URL."""
    config = load_config()
    browser_path = get_browser_path(browser_name, config)

    # Ensure the path actually exists on the system before attempting launch
    if not browser_path or not os.path.exists(browser_path):
        print(f"\n[ERROR] Could not find executable for '{browser_name}'.")
        print(f"Looked at destination: {browser_path}")
        print(f"Please update the custom path inside: {CONFIG_FILE}\n")
        return

    print(f"Launching {browser_name.capitalize()} to open: {url}")

    # Popen launches the executable asynchronously (doesn't lock up your terminal)
    subprocess.Popen([browser_path, url])

if __name__ == "__main__":
    # Standard CLI validation syntax: python main.py <browser> <url>
    if len(sys.argv) < 3:
        print("\n=== Browser Opener CLI ===")
        print("Usage:   python main.py [chrome|firefox|edge] [url]")
        print("Example: python main.py chrome https://github.com\n")
        sys.exit(1)

    chosen_browser = sys.argv[1]
    target_url = sys.argv[2]

    # Quick auto-formatting to ensure URL starts cleanly
    if not target_url.startswith(("http://", "https://")):
        target_url = "https://" + target_url

    open_browser(chosen_browser, target_url)


