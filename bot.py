import os
import json
import urllib.request
import urllib.parse
import time

# Retrieve token from Railway environment variables
TOKEN = os.environ.get("BOT_TOKEN")

if not TOKEN:
    print("ERROR: BOT_TOKEN variable is not set in Railway!")
    exit(1)

BASE_URL = f"https://api.telegram.org/bot{TOKEN}"


def make_request(method, data=None):
    """Helper function to talk directly to Telegram API"""
    url = f"{BASE_URL}/{method}"
    try:
        if data:
            payload = json.dumps(data).encode('utf-8')
            req = urllib.request.Request(
                url, data=payload, headers={'Content-Type': 'application/json'}
            )
        else:
            req = urllib.request.Request(url)

        with urllib.request.urlopen(req, timeout=35) as response:
            return json.loads(response.read().decode())
    except Exception as e:
        print(f"API Request Error ({method}): {e}")
        return None


def get_updates(offset=None):
    """Fetch unread messages from Telegram"""
    method = f"getUpdates?timeout=30" + (f"&offset={offset}" if offset else "")
    result = make_request(method)
    return result.get("result", []) if result else []


def send_menu(chat_id):
    """Sends the main football menu with interactive buttons"""
    data = {
        "chat_id": chat_id,
        "text": "⚽ *Welcome to SB24 Lucky Bot!*\n\nSelect an option below for live updates:",
        "parse_mode": "Markdown",
        "reply_markup": {
            "inline_keyboard": [
                [
                    {"text": "⚽ Live Scores", "callback_data": "live_scores"},
                    {"text": "📅 Fixtures", "callback_data": "fixtures"}
                ],
                [
                    {"text": "📊 Standings", "callback_data": "standings"},
                    {"text": "🔔 Goal Alerts", "callback_data": "alerts"}
                ]
            ]
        }
    }
    make_request("sendMessage", data)


def handle_callback(callback_query):
    """Handles user button clicks"""
    query_id = callback_query["id"]
    chat_id = callback_query["message"]["chat"]["id"]
    message_id = callback_query["message"]["message_id"]
    data = callback_query["data"]

    # Acknowledge the button press to remove the loading animation on Telegram
    make_request("answerCallbackQuery", {"callback_query_id": query_id})

    if data == "live_scores":
        text = "🔴 *Live Matches*\n\n• Man City 1 - 0 Arsenal (65')\n• Real Madrid 2 - 1 Barcelona (80')\n\n_Updated live!_"
    elif data == "fixtures":
        text = "📅 *Upcoming Fixtures*\n\n• Liverpool vs Chelsea — 20:00 UTC\n• Bayern vs Dortmund — Tomorrow 17:30 UTC"
    elif data == "standings":
        text = "📊 *Premier League Top 3*\n\n1. Man City - 45 pts\n2. Arsenal - 42 pts\n3. Liverpool - 40 pts"
    elif data == "alerts":
        text = "🔔 *Goal Alerts*\n\nYou are now subscribed to live goal notifications!"
    elif data == "main_menu":
        send_menu(chat_id)
        return

    # Edit existing message with response and add a back button
    update_data = {
        "chat_id": chat_id,
        "message_id": message_id,
        "text": text,
        "parse_mode": "Markdown",
        "reply_markup": {
            "inline_keyboard": [
                [{"text": "🔙 Back to Main Menu", "callback_data": "main_menu"}]
            ]
        }
    }
    make_request("editMessageText", update_data)


def main():
    print("Bot started successfully! Polling for updates...")
    offset = None

    while True:
        updates = get_updates(offset)
        for update in updates:
            offset = update["update_id"] + 1

            # Handle user typing commands (e.g. /start)
            if "message" in update and "text" in update["message"]:
                text = update["message"]["text"]
                chat_id = update["message"]["chat"]["id"]

                if text.startswith("/start"):
                    send_menu(chat_id)

            # Handle interactive button clicks
            elif "callback_query" in update:
                handle_callback(update["callback_query"])

        time.sleep(1)


if __name__ == "__main__":
    main()
