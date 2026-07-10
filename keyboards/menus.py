from telegram import InlineKeyboardButton, InlineKeyboardMarkup



# ==========================
# منوی اصلی پرفورم
# ==========================

def main_menu():

    keyboard = [

        [
            InlineKeyboardButton(
                "👤 پروفایل تحصیلی من در پرفورم",
                callback_data="profile"
            )
        ],


        [
            InlineKeyboardButton(
                "📝 ثبت گزارش مطالعه روزانه",
                callback_data="new_report"
            )
        ],


        [
            InlineKeyboardButton(
                "📊 داشبورد تحلیلی پرفورم و آنالیز من",
                callback_data="stats"
            )
        ],


        [
            InlineKeyboardButton(
                "🎓 طرح‌های مشاوره‌ای پرفورم",
                callback_data="plans"
            )
        ]

    ]


    return InlineKeyboardMarkup(
        keyboard
    )





# ==========================
# انتخاب رشته
# ==========================

def field_menu():

    keyboard = [

        [
            InlineKeyboardButton(
                "🧬 رشته تجربی",
                callback_data="field_تجربی"
            )
        ],


        [
            InlineKeyboardButton(
                "📐 رشته ریاضی",
                callback_data="field_ریاضی"
            )
        ],


        [
            InlineKeyboardButton(
                "📚 رشته انسانی",
                callback_data="field_انسانی"
            )
        ]

    ]


    return InlineKeyboardMarkup(
        keyboard
    )





# ==========================
# انتخاب پایه
# ==========================

def grade_menu():

    keyboard = [

        [
            InlineKeyboardButton(
                " پایه دهم",
                callback_data="grade_دهم"
            )
        ],


        [
            InlineKeyboardButton(
                " پایه یازدهم",
                callback_data="grade_یازدهم"
            )
        ],


        [
            InlineKeyboardButton(
                " پایه دوازدهم",
                callback_data="grade_دوازدهم"
            )
        ]

    ]


    return InlineKeyboardMarkup(
        keyboard
    )