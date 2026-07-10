from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes



# ==========================
# دکمه‌های اصلی شرایط مشاوره
# ==========================

def consulting_buttons():

    return InlineKeyboardMarkup(

        [

            [
                InlineKeyboardButton(
                    "🥉 طرح C | پرفورم پایه",
                    callback_data="plan_C"
                )
            ],

            [
                InlineKeyboardButton(
                    "🥈 طرح B | پرفورم پیشرفته",
                    callback_data="plan_B"
                )
            ],

            [
                InlineKeyboardButton(
                    "🥇 طرح A | پرفورم VIP",
                    callback_data="plan_A"
                )
            ],

            [
                InlineKeyboardButton(
                    "📝 ثبت نام",
                    callback_data="register_plan"
                )
            ],

            [
                InlineKeyboardButton(
                    "ℹ️ کسب اطلاعات بیشتر",
                    callback_data="more_info"
                )
            ],

            [
                InlineKeyboardButton(
                    "🏠 بازگشت به منوی اصلی",
                    callback_data="back_to_menu"
                )
            ]

        ]

    )







# ==========================
# دکمه‌های بازگشت
# ==========================


def plan_back_buttons():

    return InlineKeyboardMarkup(

        [

            [
                InlineKeyboardButton(
                    "🔙 بازگشت به طرح‌ها",
                    callback_data="plans"
                )
            ],

            [
                InlineKeyboardButton(
                    "🏠 بازگشت به منوی اصلی",
                    callback_data="back_to_menu"
                )
            ]

        ]

    )






def simple_back_buttons():

    return InlineKeyboardMarkup(

        [

            [
                InlineKeyboardButton(
                    "🔙 بازگشت به طرح‌ها",
                    callback_data="plans"
                )
            ],

            [
                InlineKeyboardButton(
                    "🏠 بازگشت به منوی اصلی",
                    callback_data="back_to_menu"
                )
            ]

        ]

    )







# ==========================
# صفحه اصلی مشاوره
# ==========================


async def consulting(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()



    text = """

🎓 طرح‌های مشاوره‌ای پرفورم


پرفورم با ارائه مسیرهای مشاوره‌ای متناسب با نیاز هر دانش‌آموز، تلاش می‌کند بهترین سطح همراهی، برنامه‌ریزی و نظارت تحصیلی را برای شما فراهم کند.


لطفاً یکی از طرح‌های زیر را انتخاب کنید:

"""



    await query.message.reply_text(

        text,

        reply_markup=consulting_buttons()

    )







# ==========================
# نمایش طرح
# ==========================


async def show_plan(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()



    plan = query.data



    if plan == "plan_C":


        text = """

🥉 طرح C | پرفورم پایه

💰 ۱,۷۰۰,۰۰۰ تومان در ماه


مناسب دانش‌آموزانی که می‌خواهند با هزینه‌ای اقتصادی، از یک سیستم مشاوره حرفه‌ای و نظارت مستمر بهره‌مند شوند.


خدمات طرح:

✅ مشاوره و برنامه‌ریزی توسط مشاور ارشد پرفورم

✅ طراحی استراتژی مطالعاتی متناسب با سطح و اهداف دانش‌آموز

✅ برنامه‌ریزی هفتگی اختصاصی

✅ بررسی روزانه گزارش‌های مطالعاتی

✅ پیگیری مستمر روند اجرای برنامه

✅ تشکیل گروه اختصاصی تلگرام با حضور دانش‌آموز، مشاور ارشد و دکتر دانشی

✅ نظارت مستقیم دکتر دانشی بر برنامه‌ها، گزارش‌ها و روند پیشرفت دانش‌آموز


مناسب برای:

دانش‌آموزانی که به دنبال یک مشاوره حرفه‌ای، مطمئن و اقتصادی هستند.

"""


    elif plan == "plan_B":


        text = """

🥈 طرح B | پرفورم پیشرفته

💰 ۲,۷۰۰,۰۰۰ تومان در ماه


مناسب دانش‌آموزانی که علاوه بر مشاوره مستمر، به ارزیابی منظم عملکرد و ارتباط مستقیم دوره‌ای با دکتر دانشی نیاز دارند.


تمامی خدمات طرح پایه، به‌علاوه:


✅ آزمون‌های ارزیابی ماهانه

✅ تحلیل عملکرد و بررسی نقاط قوت و ضعف پس از هر آزمون

✅ پیگیری و نظارت گسترده‌تر بر روند مطالعه

✅ یک جلسه اختصاصی تلفنی با دکتر دانشی هر دو هفته یک‌بار

✅ اصلاح ساختار مطالعه و استراتژی آموزشی توسط دکتر دانشی


مناسب برای:

دانش‌آموزانی که می‌خواهند مسیر مطالعاتی خود را منظم ارزیابی و اصلاح کنند.

"""
    elif plan == "plan_A":


        text = """

🥇 طرح A | پرفورم VIP

💰 ۴,۷۰۰,۰۰۰ تومان در ماه


بالاترین سطح خدمات مشاوره‌ای پرفورم


در این طرح تمامی مراحل مشاوره، برنامه‌ریزی، پیگیری و ارزیابی مستقیماً توسط دکتر دانشی انجام می‌شود.


خدمات طرح:

⭐ تمامی جلسات برنامه‌ریزی و مشاوره با دکتر دانشی

⭐ تحلیل گزارش‌های مطالعاتی توسط دکتر دانشی

⭐ ارتباط مستقیم و بدون واسطه

⭐ امکان دریافت راهنمایی در مواقع نیاز

⭐ آزمون‌های ارزیابی هر دو هفته یک‌بار

⭐ تحلیل اختصاصی آزمون‌ها

⭐ شخصی‌سازی کامل برنامه


مناسب برای:

دانش‌آموزانی که به دنبال بالاترین سطح پشتیبانی و مسیر کاملاً اختصاصی هستند.

"""




    await query.message.reply_text(

        text,

        reply_markup=plan_back_buttons()

    )









# ==========================
# ثبت نام
# ==========================


async def register_plan(

        update: Update,

        context: ContextTypes.DEFAULT_TYPE

):


    query = update.callback_query

    await query.answer()



    text = """

📝 ثبت نام در طرح‌های مشاوره‌ای پرفورم


برای ثبت نام، هزینه طرح انتخابی را به شماره کارت زیر واریز کنید:


💳 شماره کارت:

6219861933276981

👤 به نام شهریار دانشی


پس از واریز، تصویر رسید پرداخت ، مشخصات و شماره تماس خود را برای:

📩 مدیریت ثبت‌نام پرفورم به آیدی زیر ارسال کنید.

@S_Soleimanii


پس از بررسی رسید، مراحل فعال‌سازی مشاوره انجام خواهد شد.

"""



    await query.message.reply_text(

        text,

        reply_markup=simple_back_buttons()

    )









# ==========================
# اطلاعات بیشتر
# ==========================


async def more_info(

        update: Update,

        context: ContextTypes.DEFAULT_TYPE

):


    query = update.callback_query

    await query.answer()



    text = """

ℹ️ کسب اطلاعات بیشتر درباره طرح‌های مشاوره‌ای پرفورم


اگر درباره انتخاب طرح مناسب، نحوه مشاوره یا جزئیات خدمات سوالی دارید، می‌توانید با مدیریت ثبت‌نام پرفورم در ارتباط باشید:


📩 @S_Soleimanii


همکاران ما پاسخگوی سوالات شما خواهند بود.

"""



    await query.message.reply_text(

        text,

        reply_markup=simple_back_buttons()

    )
