from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from keyboards.menus import main_menu
from handlers.consulting import consulting_buttons




# ==========================
# دکمه بازگشت
# ==========================

def back_button():

    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "🔙 بازگشت به منوی اصلی",
                    callback_data="back_to_menu"
                )
            ]
        ]
    )




# ==========================
# بازگشت به منوی اصلی
# ==========================

async def back_to_menu(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()


    await query.message.reply_text(
        "🏠 منوی اصلی پرفورم:",
        reply_markup=main_menu()
    )





# ==========================
# ورود به طرح‌های مشاوره
# ==========================

async def plans(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()


    await query.message.reply_text(

        "🎓 طرح‌های مشاوره پرفورم\n\n"

        "پرفورم با ارائه مسیرهای مشاوره‌ای متناسب با نیاز هر دانش‌آموز، "
        "به شما کمک می‌کند با برنامه‌ریزی دقیق، نظارت مستمر و همراهی تخصصی "
        "به اهداف تحصیلی خود برسید.\n\n"

        "لطفاً یکی از گزینه‌های زیر را انتخاب کنید:",

        reply_markup=consulting_buttons()

    )