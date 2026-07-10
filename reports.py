from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

from telegram.ext import ContextTypes

from datetime import date, timedelta

import jdatetime


from database import (
    get_user,
    get_db,
    get_subject_report,
    save_or_update_report,
    add_to_report
)


from keyboards.menus import main_menu



# ==================================================
# لیست دروس
# ==================================================


SUBJECTS = {


    # ================= دهم =================


    ("دهم", "تجربی"): [

        "فارسی",
        "عربی",
        "دین و زندگی",
        "زبان انگلیسی",
        "جغرافیا",

        "ریاضی",
        "زیست‌شناسی",
        "فیزیک",
        "شیمی"

    ],



    ("دهم", "ریاضی"): [

        "فارسی",
        "عربی",
        "دین و زندگی",
        "زبان انگلیسی",
        "جغرافیا",
        "آمادگی دفاعی",

        "ریاضی",
        "هندسه",
        "فیزیک",
        "شیمی"

    ],



    ("دهم", "انسانی"): [

        "فارسی",
        "عربی",
        "دین و زندگی",
        "زبان انگلیسی",
        "جغرافیای ایران",
        "آمادگی دفاعی",

        "ریاضی و آمار",
        "اقتصاد",
        "علوم و فنون ادبی",
        "جامعه‌شناسی",
        "منطق",
        "تاریخ",
        "جغرافیا",
        "روان‌شناسی"

    ],




    # ================= یازدهم =================


    ("یازدهم", "تجربی"): [

        "فارسی",
        "عربی",
        "دین و زندگی",
        "زبان انگلیسی",
        "انسان و محیط زیست",

        "ریاضی",
        "زیست‌شناسی",
        "فیزیک",
        "شیمی"

    ],



    ("یازدهم", "ریاضی"): [

        "فارسی",
        "عربی",
        "دین و زندگی",
        "زبان انگلیسی",
        "انسان و محیط زیست",

        "حسابان",
        "هندسه",
        "آمار و احتمال",
        "فیزیک",
        "شیمی"

    ],



    ("یازدهم", "انسانی"): [

        "فارسی",
        "عربی",
        "دین و زندگی",
        "زبان انگلیسی",
        "انسان و محیط زیست",

        "ریاضی و آمار",
        "علوم و فنون ادبی",
        "جامعه‌شناسی",
        "فلسفه",
        "روان‌شناسی",
        "تاریخ",
        "جغرافیا",
        "عربی تخصصی"

    ]

}





# ==================================================
# اختصاصی دوازدهم
# ==================================================


SPECIAL_12 = {


    "تجربی": [

        "ریاضی",
        "زیست‌شناسی",
        "فیزیک",
        "شیمی"

    ],



    "ریاضی": [

        "حسابان",
        "هندسه",
        "گسسته",
        "فیزیک",
        "شیمی"

    ],



    "انسانی": [

        "ریاضی و آمار",
        "علوم و فنون ادبی",
        "جامعه‌شناسی",
        "فلسفه",
        "تاریخ",
        "جغرافیا",
        "عربی تخصصی"

    ]

}






# ==================================================
# اختصاصی پایه دهم و یازدهم برای دوازدهمی‌ها
# ==================================================


OLD_BASE = {


    "تجربی": {

        "دهم": [

            "ریاضی دهم",
            "زیست‌شناسی دهم",
            "فیزیک دهم",
            "شیمی دهم"

        ],


        "یازدهم": [

            "ریاضی یازدهم",
            "زیست‌شناسی یازدهم",
            "فیزیک یازدهم",
            "شیمی یازدهم"

        ]

    },



    "ریاضی": {


        "دهم": [

            "ریاضی دهم",
            "هندسه دهم",
            "فیزیک دهم",
            "شیمی دهم"

        ],



        "یازدهم": [

            "حسابان یازدهم",
            "هندسه یازدهم",
            "آمار و احتمال",
            "فیزیک یازدهم",
            "شیمی یازدهم"

        ]

    },




    "انسانی": {


        "دهم": [

            "ریاضی و آمار دهم",
            "اقتصاد",
            "علوم و فنون ادبی دهم",
            "جامعه‌شناسی دهم",
            "منطق دهم",
            "تاریخ دهم",
            "جغرافیا دهم",
            "روان‌شناسی دهم"

        ],



        "یازدهم": [

            "ریاضی و آمار یازدهم",
            "علوم و فنون ادبی یازدهم",
            "جامعه‌شناسی یازدهم",
            "فلسفه یازدهم",
            "روان‌شناسی",
            "تاریخ یازدهم",
            "جغرافیا یازدهم",
            "عربی تخصصی یازدهم"

        ]

    }

}






# ==================================================
# کیبوردها
# ==================================================


def back_button(callback="back_report"):

    return InlineKeyboardButton(
        "🔙 بازگشت",
        callback_data=callback
    )




def make_keyboard(items, prefix):

    keyboard=[]


    for item in items:

        keyboard.append(

            [

                InlineKeyboardButton(

                    item,

                    callback_data=f"{prefix}{item}"

                )

            ]

        )


    keyboard.append(

        [

            back_button()

        ]

    )


    return InlineKeyboardMarkup(keyboard)






# ==================================================
# انتخاب تاریخ
# ==================================================


def date_keyboard():

    today=date.today()

    yesterday=today-timedelta(days=1)



    return InlineKeyboardMarkup(

        [

            [

                InlineKeyboardButton(

                    f"📅 امروز | {jdatetime.date.fromgregorian(date=today).strftime('%Y/%m/%d')}",

                    callback_data=f"date_{today}"

                )

            ],

            [

                InlineKeyboardButton(

                    f"📅 دیروز | {jdatetime.date.fromgregorian(date=yesterday).strftime('%Y/%m/%d')}",

                    callback_data=f"date_{yesterday}"

                )

            ],

            [

                back_button("back_to_menu")

            ]

        ]

    )






async def new_report(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query=update.callback_query

    await query.answer()


    await query.message.reply_text(

        "📚 ثبت گزارش مطالعه پرفورم\n\n"
        "📅 گزارش مربوط به کدام روز است؟",

        reply_markup=date_keyboard()

    )





async def choose_date(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query=update.callback_query

    await query.answer()


    selected=query.data.replace(
        "date_",
        ""
    )


    context.user_data["report_date"]=date.fromisoformat(selected)



    user=await get_user(query.from_user.id)


    context.user_data["grade"]=user["grade"]

    context.user_data["field"]=user["field"]



    if user["grade"]=="دوازدهم":


        await query.message.reply_text(

            "📚 نوع درس مورد نظر را انتخاب کن:",

            reply_markup=InlineKeyboardMarkup(

                [

                    [
                        InlineKeyboardButton(
                            "📖 عمومی",
                            callback_data="type_general"
                        )
                    ],

                    [
                        InlineKeyboardButton(
                            "🎯 اختصاصی دوازدهم",
                            callback_data="type_special12"
                        )
                    ],

                    [
                        InlineKeyboardButton(
                            "📚 اختصاصی پایه",
                            callback_data="type_old_base"
                        )
                    ],

                    [
                        back_button()
                    ]

                ]

            )

        )

        return
    else:

        await query.message.reply_text(

            "📖 درس مورد نظر را انتخاب کن:",

            reply_markup=make_keyboard(

                SUBJECTS[

                    (

                        user["grade"],

                        user["field"]

                    )

                ],

                "sub_"

            )

        )







# ==================================================
# مسیر دوازدهم - انتخاب نوع درس
# ==================================================


async def choose_type(

        update: Update,

        context: ContextTypes.DEFAULT_TYPE

):


    query=update.callback_query

    await query.answer()



    field=context.user_data.get(

        "field"

    )



    mode=query.data




    # عمومی دوازدهم

    if mode=="type_general":


        if field=="انسانی":


            subjects=[

                "فارسی",
                "نگارش",
                "عربی",
                "دین و زندگی",
                "زبان انگلیسی",
                "سلامت و بهداشت",
                "هویت اجتماعی"

            ]


        else:


            subjects=[

                "فارسی",
                "عربی",
                "دین و زندگی",
                "زبان انگلیسی",
                "سلامت و بهداشت",
                "هویت اجتماعی"

            ]




    # اختصاصی دوازدهم

    elif mode=="type_special12":


        subjects=SPECIAL_12[field]





    # اختصاصی پایه

    elif mode=="type_old_base":


        await query.message.reply_text(

            "📚 پایه مورد نظر را انتخاب کن:",


            reply_markup=InlineKeyboardMarkup(

                [

                    [

                        InlineKeyboardButton(

                            "📘 پایه دهم",

                            callback_data="old_10"

                        )

                    ],


                    [

                        InlineKeyboardButton(

                            "📗 پایه یازدهم",

                            callback_data="old_11"

                        )

                    ],


                    [

                        back_button()

                    ]

                ]

            )

        )


        return



    else:

        return





    await query.message.reply_text(

        "📖 درس مورد نظر را انتخاب کن:",

        reply_markup=make_keyboard(

            subjects,

            "sub_"

        )

    )







# ==================================================
# انتخاب پایه قدیمی دوازدهمی‌ها
# ==================================================


async def choose_old_base(

        update: Update,

        context: ContextTypes.DEFAULT_TYPE

):


    query=update.callback_query

    await query.answer()



    field=context.user_data.get(

        "field"

    )



    if query.data=="old_10":


        year="دهم"



    elif query.data=="old_11":


        year="یازدهم"



    else:

        return





    subjects=OLD_BASE[field][year]




    await query.message.reply_text(


        "📖 درس مورد نظر را انتخاب کن:",


        reply_markup=make_keyboard(

            subjects,

            "sub_"

        )

    )









# ==================================================
# انتخاب درس
# ==================================================


async def choose_subject(

        update: Update,

        context: ContextTypes.DEFAULT_TYPE

):


    query=update.callback_query

    await query.answer()



    subject=query.data.replace(

        "sub_",

        ""

    )



    context.user_data["current_subject"]=subject




    keyboard=[]

    row=[]




    for i in range(1,13):


        row.append(

            InlineKeyboardButton(

                f"{i} ساعت",

                callback_data=f"hour_{i}"

            )

        )



        if len(row)==3:

            keyboard.append(row)

            row=[]





    keyboard.append(

        [

            back_button()

        ]

    )




    await query.message.reply_text(

        f"⏱ میزان مطالعه {subject} را انتخاب کن:",

        reply_markup=InlineKeyboardMarkup(keyboard)

    )








# ==================================================
# انتخاب ساعت
# ==================================================


async def choose_hour(

        update: Update,

        context: ContextTypes.DEFAULT_TYPE

):


    query=update.callback_query

    await query.answer()



    hours=int(

        query.data.replace(

            "hour_",

            ""

        )

    )



    context.user_data["current_hours"]=hours




    keyboard=[]

    row=[]




    for i in range(0,301,10):


        row.append(

            InlineKeyboardButton(

                str(i),

                callback_data=f"test_{i}"

            )

        )



        if len(row)==3:

            keyboard.append(row)

            row=[]





    keyboard.append(

        [

            back_button()

        ]

    )





    await query.message.reply_text(

        "📝 تعداد تست‌های زده شده را انتخاب کن:",

        reply_markup=InlineKeyboardMarkup(keyboard)

    )
# ==================================================
# ذخیره گزارش
# ==================================================


async def save_report(

        update: Update,

        context: ContextTypes.DEFAULT_TYPE

):


    query=update.callback_query

    await query.answer()



    tests=int(

        query.data.replace(

            "test_",

            ""

        )

    )



    user_id=query.from_user.id



    subject=context.user_data.get(

        "current_subject"

    )



    hours=context.user_data.get(

        "current_hours"

    )



    target_date=context.user_data.get(

        "report_date",

        date.today()

    )





    old_report=await get_subject_report(

        user_id,

        subject,

        target_date

    )





    if old_report:



        context.user_data["pending_report"]={

            "subject":subject,

            "hours":hours,

            "tests":tests,

            "date":target_date

        }




        await query.message.reply_text(

            f"⚠️ برای {subject} قبلاً گزارش ثبت شده.\n\n"

            f"⏱ گزارش قبلی: {old_report['hours']} ساعت\n"

            f"📝 تست قبلی: {old_report['tests']} تست\n\n"

            "چه کاری انجام شود؟",

            reply_markup=InlineKeyboardMarkup(

                [

                    [

                        InlineKeyboardButton(

                            "🔄 جایگزین",

                            callback_data="replace_report"

                        )

                    ],


                    [

                        InlineKeyboardButton(

                            "➕ اضافه شود",

                            callback_data="add_report"

                        )

                    ],


                    [

                        InlineKeyboardButton(

                            "❌ لغو",

                            callback_data="cancel_report"

                        )

                    ]

                ]

            )

        )


        return





    await save_or_update_report(

        user_id,

        subject,

        hours,

        tests,

        target_date

    )




    await query.message.reply_text(

        "✅ گزارش با موفقیت ثبت شد.",

        reply_markup=next_keyboard()

    )








# ==================================================
# دکمه بعد از ثبت گزارش
# ==================================================


def next_keyboard():


    return InlineKeyboardMarkup(

        [

            [

                InlineKeyboardButton(

                    "➕ ثبت درس دیگر",

                    callback_data="new_report"

                )

            ],


            [

                InlineKeyboardButton(

                    "🏁 پایان گزارش روز",

                    callback_data="finish_report"

                )

            ],


            [

                back_button()

            ]

        ]

    )









# ==================================================
# جایگزین گزارش قبلی
# ==================================================


async def replace_report(

        update: Update,

        context: ContextTypes.DEFAULT_TYPE

):


    query=update.callback_query

    await query.answer()




    report=context.user_data.pop(

        "pending_report",

        None

    )





    if report:


        await save_or_update_report(

            query.from_user.id,

            report["subject"],

            report["hours"],

            report["tests"],

            report["date"]

        )




    await query.message.reply_text(

        "🔄 گزارش قبلی با موفقیت جایگزین شد.",

        reply_markup=next_keyboard()

    )








# ==================================================
# اضافه کردن گزارش
# ==================================================


async def add_report(

        update: Update,

        context: ContextTypes.DEFAULT_TYPE

):


    query=update.callback_query

    await query.answer()



    report=context.user_data.pop(

        "pending_report",

        None

    )





    if report:


        await add_to_report(

            query.from_user.id,

            report["subject"],

            report["hours"],

            report["tests"],

            report["date"]

        )





    await query.message.reply_text(

        "➕ گزارش جدید به گزارش قبلی اضافه شد.",

        reply_markup=next_keyboard()

    )








# ==================================================
# لغو گزارش
# ==================================================


async def cancel_report(

        update: Update,

        context: ContextTypes.DEFAULT_TYPE

):


    query=update.callback_query

    await query.answer()



    context.user_data.pop(

        "pending_report",

        None

    )



    await query.message.reply_text(

        "❌ ثبت گزارش لغو شد.",

        reply_markup=main_menu()

    )








# ==================================================
# پایان گزارش روز
# ==================================================


async def finish_report(

        update: Update,

        context: ContextTypes.DEFAULT_TYPE

):


    query=update.callback_query

    await query.answer()



    user_id=query.from_user.id



    target_date=context.user_data.get(

        "report_date",

        date.today()

    )




    pool=await get_db()



    async with pool.acquire() as conn:


        logs=await conn.fetch(

            """

            SELECT *

            FROM study_logs

            WHERE user_id=$1

            AND log_date=$2

            ORDER BY id

            """,

            user_id,

            target_date

        )






    if not logs:


        await query.message.reply_text(

            "❌ برای این تاریخ گزارشی ثبت نشده است.",

            reply_markup=main_menu()

        )


        return






    total_hours=sum(

        row["hours"]

        for row in logs

    )



    total_tests=sum(

        row["tests"]

        for row in logs

    )





    jalali_date=jdatetime.date.fromgregorian(

        date=target_date

    )





    text=(

        "📊 گزارش مطالعه پرفورم\n\n"

        f"📅 تاریخ: {jalali_date.strftime('%Y/%m/%d')}\n\n"

        "━━━━━━━━━━━━━━\n\n"

    )





    for row in logs:


        text += (

            f"📚 {row['subject']}\n"

            f"⏱ {row['hours']} ساعت\n"

            f"📝 {row['tests']} تست\n\n"

        )






    text += (

        "━━━━━━━━━━━━━━\n"

        f"🔥 مجموع مطالعه: {total_hours} ساعت\n"

        f"📝 مجموع تست: {total_tests}\n\n"

        "🌟 آفرین! مسیر پیشرفت با ثبت منظم ساخته می‌شود."

    )






    context.user_data.pop(

        "current_subject",

        None

    )


    context.user_data.pop(

        "current_hours",

        None

    )


    context.user_data.pop(

        "pending_report",

        None

    )





    await query.message.reply_text(

        text,

        reply_markup=main_menu()

    )









# ==================================================
# بازگشت در مسیر گزارش
# ==================================================


async def back_report(

        update: Update,

        context: ContextTypes.DEFAULT_TYPE

):


    query=update.callback_query

    await query.answer()



    await query.message.reply_text(

        "📚 عملیات گزارش مطالعه لغو شد.",

        reply_markup=main_menu()

    )