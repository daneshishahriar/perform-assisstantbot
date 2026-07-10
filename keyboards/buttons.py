from telegram import KeyboardButton, ReplyKeyboardMarkup


def phone_button():
    keyboard = [
        [
            KeyboardButton(
                "📱 ارسال شماره موبایل",
                request_contact=True
            )
        ]
    ]

    return ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True,
        one_time_keyboard=True
    )