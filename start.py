from telegram import Update, ReplyKeyboardRemove
from telegram.ext import ContextTypes

from keyboards.buttons import phone_button
from keyboards.menus import (
    field_menu,
    main_menu,
    grade_menu
)

from database import save_user





async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    context.user_data.clear()


    await update.message.reply_text(
        "🌹 به پرفورم خوش آمدی\n\n"
        "برای ساخت پرونده تحصیلی، لطفاً نام و نام خانوادگی خودت را ارسال کن:"
    )


    context.user_data["step"] = "name"







async def save_name(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if context.user_data.get("step") != "name":
        return


    context.user_data["name"] = update.message.text

    context.user_data["step"] = "phone"



    await update.message.reply_text(
        "📱 شماره موبایل خودت را ارسال کن:",
        reply_markup=phone_button()
    )









async def save_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if context.user_data.get("step") != "phone":
        return


    context.user_data["phone"] = update.message.contact.phone_number

    context.user_data["step"] = "grade"



    await update.message.reply_text(
        "📚 پایه تحصیلی خودت را انتخاب کن:",
        reply_markup=ReplyKeyboardRemove()
    )


    await update.message.reply_text(
        "👇 یکی از گزینه‌ها را انتخاب کن:",
        reply_markup=grade_menu()
    )









async def save_grade(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query

    await query.answer()


    if context.user_data.get("step") != "grade":
        return


    grade = query.data.replace(
        "grade_",
        ""
    )


    context.user_data["grade"] = grade

    context.user_data["step"] = "field"



    await query.message.reply_text(
        "🎓 رشته تحصیلی خودت را انتخاب کن:",
        reply_markup=field_menu()
    )









async def save_field(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query

    await query.answer()



    field = query.data.replace(
        "field_",
        ""
    )



    user_id = query.from_user.id



    await save_user(
        user_id,
        context.user_data["name"],
        context.user_data["phone"],
        context.user_data["grade"],
        field
    )



    await query.message.reply_text(
        "✅ پرونده اولیه شما ساخته شد.\n\n"
        "به پرفورم خوش آمدی 🌟",
        reply_markup=main_menu()
    )