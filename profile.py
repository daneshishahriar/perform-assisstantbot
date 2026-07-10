from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

from telegram.ext import ContextTypes

from datetime import date

import jdatetime


from database import (
    get_user
)





# =====================================
# دکمه‌های پروفایل
# =====================================


def profile_buttons():

    return InlineKeyboardMarkup(

        [

            [

                InlineKeyboardButton(
                    "✏️ ویرایش اطلاعات تحصیلی",
                    callback_data="edit_profile"
                )

            ],

            [

                InlineKeyboardButton(
                    "🔙 بازگشت به منوی اصلی",
                    callback_data="back_to_menu"
                )

            ]

        ]

    )








# =====================================
# تایید ویرایش
# =====================================


def edit_confirm_buttons():

    return InlineKeyboardMarkup(

        [

            [

                InlineKeyboardButton(
                    "✅ ادامه و ویرایش",
                    callback_data="confirm_edit_profile"
                )

            ],

            [

                InlineKeyboardButton(
                    "❌ انصراف",
                    callback_data="cancel_edit_profile"
                )

            ]

        ]

    )








# =====================================
# انتخاب پایه جدید
# =====================================


def edit_grade_buttons():

    return InlineKeyboardMarkup(

        [

            [

                InlineKeyboardButton(
                    "دهم",
                    callback_data="edit_grade_دهم"
                ),

                InlineKeyboardButton(
                    "یازدهم",
                    callback_data="edit_grade_یازدهم"
                )

            ],


            [

                InlineKeyboardButton(
                    "دوازدهم",
                    callback_data="edit_grade_دوازدهم"
                )

            ],


            [

                InlineKeyboardButton(
                    "🔙 بازگشت",
                    callback_data="back_profile"
                )

            ]

        ]

    )








# =====================================
# انتخاب رشته جدید
# =====================================


def edit_field_buttons():

    return InlineKeyboardMarkup(

        [

            [

                InlineKeyboardButton(
                    "🧬 علوم تجربی",
                    callback_data="edit_field_تجربی"
                )

            ],


            [

                InlineKeyboardButton(
                    "📐 ریاضی فیزیک",
                    callback_data="edit_field_ریاضی"
                )

            ],


            [

                InlineKeyboardButton(
                    "📚 علوم انسانی",
                    callback_data="edit_field_انسانی"
                )

            ],


            [

                InlineKeyboardButton(
                    "🔙 بازگشت",
                    callback_data="back_profile"
                )

            ]

        ]

    )








# =====================================
# نمایش پروفایل
# =====================================


async def profile(

        update: Update,

        context: ContextTypes.DEFAULT_TYPE

):


    query = update.callback_query

    await query.answer()



    user_id = query.from_user.id



    user = await get_user(

        user_id

    )



    if not user:


        await query.message.reply_text(

            "❌ هنوز پرونده تحصیلی شما در پرفورم ساخته نشده است.",

            reply_markup=profile_buttons()

        )

        return





    join_date = user["join_date"]



    if join_date:


        jalali_join = jdatetime.date.fromgregorian(

            date=join_date

        )


        join_text = jalali_join.strftime(

            "%Y/%m/%d"

        )


        days = (

            date.today() - join_date

        ).days



    else:


        join_text = "ثبت نشده"

        days = 0






    text = (

        "🎓 داشبورد تحصیلی پرفورم\n\n"

        "━━━━━━━━━━━━━━\n"

        "👤 اطلاعات دانش‌آموز\n\n"


        f"نام و نام خانوادگی:\n"
        f"{user['name']}\n\n"


        f"📱 شماره تماس:\n"
        f"{user['phone']}\n\n"


        f"📚 پایه تحصیلی:\n"
        f"{user['grade']}\n\n"


        f"🎯 رشته تحصیلی:\n"
        f"{user['field']}\n\n"


        "━━━━━━━━━━━━━━\n"


        "📅 عضویت در پرفورم\n\n"


        f"🗓 تاریخ عضویت:\n"
        f"{join_text}\n\n"


        f"⏳ مدت همراهی:\n"
        f"{days} روز\n\n"


        "━━━━━━━━━━━━━━\n"


        "🌟 مسیر پیشرفتت را با پرفورم ادامه بده."

    )



    await query.message.reply_text(

        text,

        reply_markup=profile_buttons()

    )









# =====================================
# شروع ویرایش
# =====================================


async def edit_profile(

        update: Update,

        context: ContextTypes.DEFAULT_TYPE

):


    query = update.callback_query

    await query.answer()



    await query.message.reply_text(

        "✏️ ویرایش اطلاعات تحصیلی\n\n"

        "⚠️ توجه مهم:\n\n"

        "در صورت تغییر پایه یا رشته تحصیلی، "

        "تمام تاریخچه مطالعه، گزارش‌ها و تحلیل‌های عملکردی شما پاک خواهد شد.\n\n"

        "🗓 تاریخ عضویت شما در پرفورم هرگز تغییر نخواهد کرد.\n\n"

        "آیا مطمئن هستید؟",

        reply_markup=edit_confirm_buttons()

    )
# =====================================
# تایید شروع ویرایش
# =====================================


async def confirm_edit_profile(

        update: Update,

        context: ContextTypes.DEFAULT_TYPE

):


    query = update.callback_query

    await query.answer()



    context.user_data["editing_profile"] = True



    await query.message.reply_text(

        "📚 پایه تحصیلی جدید خود را انتخاب کن:",

        reply_markup=edit_grade_buttons()

    )








# =====================================
# لغو ویرایش
# =====================================


async def cancel_edit_profile(

        update: Update,

        context: ContextTypes.DEFAULT_TYPE

):


    query = update.callback_query

    await query.answer()



    context.user_data.pop(

        "editing_profile",

        None

    )


    await query.message.reply_text(

        "❌ ویرایش اطلاعات تحصیلی لغو شد.",

        reply_markup=profile_buttons()

    )








# =====================================
# انتخاب پایه جدید
# =====================================


async def edit_grade(

        update: Update,

        context: ContextTypes.DEFAULT_TYPE

):


    query = update.callback_query

    await query.answer()



    grade = query.data.replace(

        "edit_grade_",

        ""

    )



    context.user_data["new_grade"] = grade



    await query.message.reply_text(

        "🎯 رشته تحصیلی جدید خود را انتخاب کن:",

        reply_markup=edit_field_buttons()

    )








# =====================================
# انتخاب رشته جدید
# =====================================


async def edit_field(

        update: Update,

        context: ContextTypes.DEFAULT_TYPE

):


    query = update.callback_query

    await query.answer()



    field = query.data.replace(

        "edit_field_",

        ""

    )



    context.user_data["new_field"] = field



    keyboard = InlineKeyboardMarkup(

        [

            [

                InlineKeyboardButton(

                    "✅ ذخیره تغییرات",

                    callback_data="save_edited_profile"

                )

            ],


            [

                InlineKeyboardButton(

                    "❌ لغو",

                    callback_data="cancel_edit_profile"

                )

            ]

        ]

    )



    await query.message.reply_text(

        "اطلاعات جدید:\n\n"

        f"📚 پایه: {context.user_data.get('new_grade')}\n"

        f"🎯 رشته: {field}\n\n"

        "آیا ذخیره شود؟",

        reply_markup=keyboard

    )









# =====================================
# ذخیره نهایی تغییرات
# =====================================


async def save_edited_profile(

        update: Update,

        context: ContextTypes.DEFAULT_TYPE

):


    query = update.callback_query

    await query.answer()



    user_id = query.from_user.id



    new_grade = context.user_data.get(

        "new_grade"

    )


    new_field = context.user_data.get(

        "new_field"

    )



    user = await get_user(

        user_id

    )



    if not user:


        await query.message.reply_text(

            "❌ خطا: پرونده پیدا نشد."

        )

        return






    old_grade = user["grade"]

    old_field = user["field"]





    # اینجا بعد از اضافه شدن تابع دیتابیس اجرا می‌شود

    # اگر پایه یا رشته تغییر کرده باشد تاریخچه پاک می‌شود


    if (

        old_grade != new_grade

        or

        old_field != new_field

    ):

        from database import delete_user_study_history

        await delete_user_study_history(

            user_id

        )






    from database import update_education_profile



    await update_education_profile(

        user_id,

        new_grade,

        new_field

    )






    context.user_data.pop(

        "editing_profile",

        None

    )


    context.user_data.pop(

        "new_grade",

        None

    )


    context.user_data.pop(

        "new_field",

        None

    )





    await query.message.reply_text(

        "✅ اطلاعات تحصیلی شما با موفقیت تغییر کرد.\n\n"

        "📌 تاریخ عضویت شما در پرفورم حفظ شده است.",

        reply_markup=profile_buttons()

    )








# =====================================
# بازگشت از منوی ویرایش
# =====================================


async def back_profile(

        update: Update,

        context: ContextTypes.DEFAULT_TYPE

):


    query = update.callback_query

    await query.answer()



    await query.message.reply_text(

        "🎓 پروفایل تحصیلی پرفورم",

        reply_markup=profile_buttons()

    )