from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes


from database import (

    get_today_stats,
    get_today_subject_stats,

    get_week_stats,
    get_week_subject_stats,

    get_month_stats,
    get_month_subject_stats,

    get_three_month_stats,
    get_three_month_subject_stats,

    get_all_time_stats,
    get_all_time_subject_stats

)





# ==========================
# منوی بازه های آماری
# ==========================


def stats_menu():

    return InlineKeyboardMarkup(

        [

            [
                InlineKeyboardButton(
                    "📊 تحلیل امروز",
                    callback_data="stats_today"
                )
            ],

            [
                InlineKeyboardButton(
                    "📈 تحلیل هفتگی",
                    callback_data="stats_week"
                )
            ],

            [
                InlineKeyboardButton(
                    "📅 تحلیل ماهانه",
                    callback_data="stats_month"
                )
            ],

            [
                InlineKeyboardButton(
                    "📚 تحلیل ۳ ماه اخیر",
                    callback_data="stats_three_month"
                )
            ],

            [
                InlineKeyboardButton(
                    "🗂 تحلیل کل دوران عضویت",
                    callback_data="stats_all"
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







# ==========================
# ورود به داشبورد تحلیل
# ==========================


async def stats(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()


    await query.message.reply_text(

        "📊 داشبورد تحلیلی پرفورم\n\n"
        "بازه مورد نظر برای تحلیل عملکرد را انتخاب کنید:",

        reply_markup=stats_menu()

    )








# ==========================
# نمایش تحلیل
# ==========================


async def show_stats(

        update: Update,
        context: ContextTypes.DEFAULT_TYPE

):

    query = update.callback_query

    await query.answer()


    user_id = query.from_user.id


    mode = query.data



    if mode == "stats_today":

        title = "📊 تحلیل امروز"

        profile = await get_today_stats(user_id)

        subjects = await get_today_subject_stats(user_id)



    elif mode == "stats_week":

        title = "📈 تحلیل هفتگی"

        profile = await get_week_stats(user_id)

        subjects = await get_week_subject_stats(user_id)




    elif mode == "stats_month":

        title = "📅 تحلیل ماهانه"

        profile = await get_month_stats(user_id)

        subjects = await get_month_subject_stats(user_id)




    elif mode == "stats_three_month":

        title = "📚 تحلیل ۳ ماه اخیر"

        profile = await get_three_month_stats(user_id)

        subjects = await get_three_month_subject_stats(user_id)




    elif mode == "stats_all":

        title = "🗂 تحلیل کل دوران عضویت"

        profile = await get_all_time_stats(user_id)

        subjects = await get_all_time_subject_stats(user_id)



    else:

        return






    text = (

        "📊 داشبورد تحلیلی پرفورم\n\n"

        f"{title}\n\n"


        "━━━━━━━━━━━━━━\n"

        "🔥 عملکرد کلی\n\n"


        f"⏱ مجموع مطالعه:\n"
        f"{profile['total_hours']} ساعت\n\n"


        f"📝 مجموع تست:\n"
        f"{profile['total_tests']} تست\n\n"


        f"📈 میانگین مطالعه روزانه:\n"
        f"{profile['avg_hours']} ساعت\n\n"


        "━━━━━━━━━━━━━━\n"

        "📚 عملکرد دروس\n\n"

    )





    if subjects:


        for item in subjects:


            text += (

                f"📖 {item['subject']}\n"

                f"⏱ {item['total_hours']} ساعت"

                f" | 📝 {item['total_tests']} تست\n\n"

            )



    else:


        text += (

            "برای این بازه هنوز گزارشی ثبت نشده است.\n\n"

        )





    await query.message.reply_text(

        text,

        reply_markup=stats_menu()

    )