import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Enable logging to see errors in the console
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# Replace 'YOUR_BOT_TOKEN_HERE' with the HTTP API token you received from BotFather
TOKEN = "YOUR_BOT_TOKEN_HERE"


# 1. Main /start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [
            InlineKeyboardButton("⚽ Live Scores", callback_data="live_scores"),
            InlineKeyboardButton("📅 Fixtures", callback_data="fixtures"),
        ],
        [
            InlineKeyboardButton("📊 Standings", callback_data="standings"),
            InlineKeyboardButton("🔔 Alerts", callback_data="alerts"),
        ],
        [
            InlineKeyboardButton("❓ Help", callback_data="help")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    welcome_text = (
        "⚽ *Welcome to SB24 Lucky Bot!*\n\n"
        "Select an option below to get the latest football updates and statistics:"
    )

    await update.message.reply_text(welcome_text, parse_mode="Markdown", reply_markup=reply_markup)


# 2. Callback query handler for button clicks
async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    if query.data == "live_scores":
        response = (
            "🔴 *Live Matches*\n\n"
            "• Man City 1 - 0 Arsenal (65')\n"
            "• Real Madrid 2 - 1 Barcelona (80')\n\n"
            "_Stats update automatically._"
        )
    elif query.data == "fixtures":
        response = (
            "📅 *Upcoming Fixtures*\n\n"
            "• Liverpool vs Chelsea — 20:00 UTC\n"
            "• Bayern vs Dortmund — Tomorrow, 17:30 UTC"
        )
    elif query.data == "standings":
        response = (
            "📊 *Premier League Top 3*\n\n"
            "1. Man City - 45 pts\n"
            "2. Arsenal - 42 pts\n"
            "3. Liverpool - 40 pts"
        )
    elif query.data == "alerts":
        response = "🔔 *Notifications*\n\nYou are currently subscribed to live match goal alerts!"
    elif query.data == "help":
        response = (
            "❓ *Help & Support*\n\n"
            "Use the buttons below to navigate match updates and football statistics."
        )

    # Back button to return to main menu
    back_keyboard = [[InlineKeyboardButton("🔙 Back to Main Menu", callback_data="main_menu")]]
    reply_markup = InlineKeyboardMarkup(back_keyboard)

    if query.data == "main_menu":
        keyboard = [
            [
                InlineKeyboardButton("⚽ Live Scores", callback_data="live_scores"),
                InlineKeyboardButton("📅 Fixtures", callback_data="fixtures"),
            ],
            [
                InlineKeyboardButton("📊 Standings", callback_data="standings"),
                InlineKeyboardButton("🔔 Alerts", callback_data="alerts"),
            ],
            [
                InlineKeyboardButton("❓ Help", callback_data="help")
            ]
        ]
        await query.edit_message_text(
            "⚽ *Welcome to SB24 Lucky Bot!*\n\nSelect an option below:",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    else:
        await query.edit_message_text(response, parse_mode="Markdown", reply_markup=reply_markup)


def main():
    # Build application
    app = Application.builder().token(TOKEN).build()

    # Register handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_click))

    # Start the bot
    print("Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
