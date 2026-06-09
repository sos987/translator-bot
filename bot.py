import os
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
)

from openai import OpenAI

print("TG_TOKEN =", bool(os.getenv("TG_TOKEN")))
print("OPENAI_API_KEY =", bool(os.getenv("OPENAI_API_KEY")))

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

BOT_TOKEN = os.getenv("TG_TOKEN")


async def translate(update: Update, prompt: str):
    text = update.message.text.split(" ", 1)

    if len(text) < 2:
        await update.message.reply_text("Nedostaje tekst.")
        return

    user_text = text[1]

    response = client.chat.completions.create(
        model="gpt-5",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": user_text},
        ],
    )

    await update.message.reply_text(
        response.choices[0].message.content
    )


async def sr(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await translate(
        update,
        """
        Prevedi na srpski jezik.
        Koristi latinicu bez dijakritika:
        č->c
        ć->c
        š->s
        ž->z
        đ->dj

        Vrati samo prevod.
        """,
    )


async def ru(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await translate(
        update,
        """
        Переведи на русский язык.
        Возвращай только перевод.
        """,
    )


async def check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await translate(
        update,
        """
        Ispravi gramatiku i stil srpskog teksta.
        Zadrzi isti smisao.
        Koristi latinicu bez dijakritika.

        Vrati samo ispravljenu verziju.
        """,
    )


async def formal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await translate(
        update,
        """
        Prepravi tekst u ljubazan i sluzben stil.

        Koristi srpsku latinicu bez dijakritika.

        Vrati samo gotov tekst.
        """,
    )


app = Application.builder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("sr", sr))
app.add_handler(CommandHandler("ru", ru))
app.add_handler(CommandHandler("check", check))
app.add_handler(CommandHandler("formal", formal))

app.run_polling()
