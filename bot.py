import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler

# Enable logging to see errors in the Koyeb console
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

# Configuration - PASTE YOUR TOKEN HERE
BOT_TOKEN = "7220466960:AAEOxHqkbWu65Mk84V-LAU1o6LAzK_BY_lM"

# Define states for the conversation
GAMES, SKINS, COLLECTOR, RANK, PRICE, CONTACT, CHANNEL = range(7)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Sends a message when the command /start is issued."""
    await update.message.reply_text(
        "✨ ស្វាគមន៍មកកាន់ Vinzy Store Bot!\n"
        "ពាក្យបញ្ជាសម្រាប់បង្កើតការផ្សាយពាណិជ្ជកម្ម:\n"
        "👉 .gen roblox\n"
        "👉 .gen mlbb bypass\n"
        "👉 .gen smm"
    )

async def handle_gen(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Starts the advertisement generation process based on user command."""
    text = update.message.text.lower()
    
    if ".gen roblox" in text:
        context.user_data['type'] = 'roblox'
        await update.message.reply_text("🎮 **ROBLOX GEN**\nតើគណនីនេះលេងហ្គេមអ្វីខ្លះ? (ឧទាហរណ៍: Blox Fruit, Pet Sim)")
        return GAMES
    
    elif ".gen mlbb bypass" in text:
        context.user_data['type'] = 'mlbb'
        await update.message.reply_text("⚔️ **MLBB BYPASS GEN**\nតើមាន Skin សរុបចំនួនប៉ុន្មាន?")
        return SKINS
    
    elif ".gen smm" in text:
        context.user_data['type'] = 'smm'
        await update.message.reply_text("🚀 **SMM GEN**\nតើអ្នកចង់ដាក់សេវាកម្មអ្វី? (ឧទាហរណ៍: 1000 Followers)")
        return SKINS
    
    return ConversationHandler.END

async def get_games(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['games'] = update.message.text
    await update.message.reply_text("💰 តើតម្លៃប៉ុន្មាន?")
    return PRICE

async def get_skins(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['skins'] = update.message.text
    if context.user_data['type'] == 'mlbb':
        await update.message.reply_text("🏆 តើជាប្រភេទ Collector អ្វី?\n(ឧទាហរណ៍: Exalted collector, Mega collector, ឬ World collector)")
        return COLLECTOR
    await update.message.reply_text("💰 តើតម្លៃប៉ុន្មាន?")
    return PRICE

async def get_collector(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['collector'] = update.message.text
    await update.message.reply_text("🌟 តើ Rank ខ្ពស់បំផុត (Highest Rank) ជាអ្វី?")
    return RANK

async def get_rank(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['rank'] = update.message.text
    await update.message.reply_text("💰 តើតម្លៃប៉ុន្មាន?")
    return PRICE

async def get_price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['price'] = update.message.text
    await update.message.reply_text("📞 សូមដាក់ឈ្មោះ Contact @username")
    return CONTACT

async def get_contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['contact'] = update.message.text
    await update.message.reply_text("📢 សូមដាក់ Link ឆានែលរបស់អ្នក")
    return CHANNEL

async def finish_ad(update: Update, context: ContextTypes.DEFAULT_TYPE):
    channel = update.message.text
    data = context.user_data
    ad_type = data.get('type')
    
    if ad_type == 'roblox':
        template = (
            f"🛒 **លក់គណនី ROBLOX**\n\n"
            f"🎮 **ហ្គេមដែលលេង:** {data['games']}\n"
            f"💰 **តម្លៃ:** {data['price']}\n"
            f"📞 **ទំនាក់ទំនង:** {data['contact']}\n"
            f"📢 **ឆានែល:** {channel}\n\n"
            f"⚠️ *ទិញហើយមិនអាចដូរវិញបានទេ (No Refund)*"
        )
    elif ad_type == 'mlbb':
        template = (
            f"🔥 **VINZY STOCK** 🔥\n"
            f"🛡️ **MLBB BYPASS** 🛡️\n\n"
            f"🎭 **ចំនួន Skin:** {data['skins']}\n"
            f"🏆 **ប្រភេទ Collector:** {data['collector']}\n"
            f"🌟 **Rank ខ្ពស់បំផុត:** {data['rank']}\n"
            f"💰 **តម្លៃ:** {data['price']}\n"
            f"📞 **ទំនាក់ទំនង:** {data['contact']}\n"
            f"📢 **ឆានែលមេ:** {channel}\n\n"
            f"⚠️ *ទិញហើយមិនអាចដូរវិញបានទេ (No Refund)*"
        )
    else: # SMM
        template = (
            f"🚀 **សេវាកម្ម SMM BOOSTING**\n\n"
            f"📈 **សេវាកម្ម:** {data['skins']}\n"
            f"💰 **តម្លៃ:** {data['price']}\n"
            f"📞 **ទំនាក់ទំនង:** {data['contact']}\n"
            f"📢 **ឆានែល:** {channel}\n\n"
            f"✅ *ជឿជាក់ដោយ Vinzy Store*"
        )

    await update.message.reply_text(template, parse_mode="Markdown")
    # Clear data for next use
    context.user_data.clear()
    return ConversationHandler.END

def main():
    """Run the bot."""
    # Build the application with the token directly
    app = Application.builder().token(BOT_TOKEN).build()

    # Add the conversation handler
    conv_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.Regex(r'^\.gen'), handle_gen)],
        states={
            GAMES: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_games)],
            SKINS: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_skins)],
            COLLECTOR: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_collector)],
            RANK: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_rank)],
            PRICE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_price)],
            CONTACT: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_contact)],
            CHANNEL: [MessageHandler(filters.TEXT & ~filters.COMMAND, finish_ad)],
        },
        fallbacks=[CommandHandler("start", start)],
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(conv_handler)

    print("Vinzy Store Bot is now online...")
    app.run_polling()

if __name__ == '__main__':
    main()
