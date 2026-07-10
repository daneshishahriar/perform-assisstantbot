from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Update
)

from telegram.ext import ContextTypes

from database import (
    get_db,
    get_user,
    get_period_stats,
    get_period_subject_stats,
    get_user_ids,
    week_start,
    month_start
)

from datetime import datetime, timedelta, date as gdate

import jdatetime


ADMIN_IDS = [
    5723306558
]


def is_admin(user_id):
    return user_id in ADMIN_IDS



# ==========================
# تبدیل تاریخ میلادی به شمسی
# ==========================

PERSIAN_MONTHS = [
    "فروردین", "اردیبهشت", "خرداد",
    "تیر", "مرداد", "شهریور",
    "مهر", "آبان", "آذر",
    "دی", "بهمن", "اسفند"
]


def gregorian_to_jalali(date):

    try:
        from jdatetime import date as jdate

        j = jdate.fromgregorian(
            date=date
        )

        return f"{j.day} {PERSIAN_MONTHS[j.month - 1]} {j.year}"

    except:

        return str(date)



# ==========================
# شروع سال شمسی جاری
# ==========================

def year_start():

    today = jdatetime.date.today()

    first_day = jdatetime.date(
        today.year,
        1,
        1
    )

    return first_day.togregorian()



# ==========================
# تعیین تاریخ شروع بازه برای دانش‌آموزان برتر
# ==========================

def get_top_period_start(period):

    if period == "today":

        return gdate.today(), True

    elif period == "week":

        return week_start(), False

    elif period == "month":

        return month_start(), False

    elif period == "year":

        return year_start(), False

    return None, False



TOP_PERIOD_LABELS = {
    "today": "امروز",
    "week": "این هفته",
    "month": "این ماه",
    "year": "امسال"
}

# ==========================
# پنل مدیریت
# ==========================

def admin_keyboard():

    return InlineKeyboardMarkup([

        [
            InlineKeyboardButton(
                "👥 لیست دانش‌آموزان",
                callback_data="admin_students"
            )
        ],

        [
            InlineKeyboardButton(
                "📊 آمار کلی کاربران",
                callback_data="admin_general_stats"
            )
        ],

        [
            InlineKeyboardButton(
                "🏆 دانش‌آموزان برتر",
                callback_data="admin_top_students"
            )
        ],

        [
            InlineKeyboardButton(
                "📋 گزارش دانش‌آموزان",
                callback_data="admin_students_report"
            )
        ],

        [
            InlineKeyboardButton(
                "📊 لیست خروجی کامل",
                callback_data="admin_excel"
            )
        ],

        [
            InlineKeyboardButton(
                "📢 ارسال پیام گروهی",
                callback_data="admin_broadcast"
            )
        ]

    ])




# ==========================
# ورود ادمین
# ==========================

async def admin_start(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
):

    if not is_admin(
        update.effective_user.id
    ):

        await update.message.reply_text(
            "⛔ دسترسی غیرمجاز"
        )

        return


    await update.message.reply_text(

        "👨‍💼 پنل مدیریت پرفورم",

        reply_markup=admin_keyboard()

    )



async def admin_panel(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()


    await query.message.reply_text(

        "👨‍💼 پنل مدیریت پرفورم",

        reply_markup=admin_keyboard()

    )



# ==========================
# مدیریت دانش‌آموزان
# ==========================


async def admin_students(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()


    await query.message.reply_text(

        "👥 نوع نمایش دانش‌آموزان:",

        reply_markup=InlineKeyboardMarkup([


            [
                InlineKeyboardButton(
                    "📋 لیست کلی",
                    callback_data="admin_all_students"
                )
            ],


            [
                InlineKeyboardButton(
                    "🎯 تفکیکی",
                    callback_data="admin_separated_students"
                )
            ],


            [
                InlineKeyboardButton(
                    "🔙 بازگشت",
                    callback_data="admin_panel"
                )
            ]

        ])

    )



# ==========================
# لیست کلی دانش‌آموزان
# ==========================


async def admin_all_students(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()


    pool = await get_db()


    async with pool.acquire() as conn:

        students = await conn.fetch(

            """
            SELECT
                user_id,
                name,
                phone,
                grade,
                field,
                join_date

            FROM users

            ORDER BY grade,name

            """

        )



    keyboard=[]


    for student in students:

        keyboard.append([

            InlineKeyboardButton(

                student["name"],

                callback_data=f"admin_user_{student['user_id']}"

            )

        ])



    keyboard.append([

        InlineKeyboardButton(

            "🔙 بازگشت",

            callback_data="admin_students"

        )

    ])



    await query.message.reply_text(

        f"""
📋 لیست دانش‌آموزان

👥 تعداد:
{len(students)} نفر
""",

        reply_markup=InlineKeyboardMarkup(
            keyboard
        )

    )



# ==========================
# انتخاب تفکیک
# ==========================


async def admin_separated_students(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()


    await query.message.reply_text(

        "نوع تفکیک را انتخاب کنید:",

        reply_markup=InlineKeyboardMarkup([


            [

                InlineKeyboardButton(
                    "🎓 رشته محور",
                    callback_data="admin_field_based"
                )

            ],


            [

                InlineKeyboardButton(
                    "📚 پایه محور",
                    callback_data="admin_grade_based"
                )

            ],


            [

                InlineKeyboardButton(
                    "🔙 بازگشت",
                    callback_data="admin_students"
                )

            ]

        ])

    )
# ==========================
# رشته محور
# ==========================

async def admin_field_based(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()


    await query.message.reply_text(

        "🎓 رشته را انتخاب کنید:",

        reply_markup=InlineKeyboardMarkup([


            [
                InlineKeyboardButton(
                    "🧪 تجربی",
                    callback_data="filter_field_تجربی"
                )
            ],


            [
                InlineKeyboardButton(
                    "📐 ریاضی",
                    callback_data="filter_field_ریاضی"
                )
            ],


            [
                InlineKeyboardButton(
                    "📚 انسانی",
                    callback_data="filter_field_انسانی"
                )
            ],


            [
                InlineKeyboardButton(
                    "🔙 بازگشت",
                    callback_data="admin_separated_students"
                )
            ]

        ])

    )




async def admin_field_grade(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()


    field = query.data.replace(
        "filter_field_",
        ""
    )


    context.user_data["filter_field"] = field


    await query.message.reply_text(

        f"📚 پایه {field}:",

        reply_markup=InlineKeyboardMarkup([


            [
                InlineKeyboardButton(
                    "دهم",
                    callback_data="filter_field_grade_دهم"
                )
            ],


            [
                InlineKeyboardButton(
                    "یازدهم",
                    callback_data="filter_field_grade_یازدهم"
                )
            ],


            [
                InlineKeyboardButton(
                    "دوازدهم",
                    callback_data="filter_field_grade_دوازدهم"
                )
            ],


            [
                InlineKeyboardButton(
                    "همه",
                    callback_data="filter_field_grade_all"
                )
            ]

        ])

    )



# ==========================
# پایه محور
# ==========================


async def admin_grade_based(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()


    await query.message.reply_text(

        "📚 پایه را انتخاب کنید:",

        reply_markup=InlineKeyboardMarkup([


            [
                InlineKeyboardButton(
                    "دهم",
                    callback_data="filter_grade_دهم"
                )
            ],


            [
                InlineKeyboardButton(
                    "یازدهم",
                    callback_data="filter_grade_یازدهم"
                )
            ],


            [
                InlineKeyboardButton(
                    "دوازدهم",
                    callback_data="filter_grade_دوازدهم"
                )
            ],


            [
                InlineKeyboardButton(
                    "🔙 بازگشت",
                    callback_data="admin_students"
                )
            ]

        ])

    )




# ==========================
# نمایش فیلتر شده
# ==========================


async def show_filtered_students(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()


    data = query.data

    pool = await get_db()


    async with pool.acquire() as conn:


        if data.startswith(
            "filter_field_grade_"
        ):


            grade = data.replace(
                "filter_field_grade_",
                ""
            )


            field = context.user_data.get(
                "filter_field"
            )


            if grade == "all":


                students = await conn.fetch(

                    """
                    SELECT
                        user_id,
                        name,
                        phone,
                        grade,
                        field

                    FROM users

                    WHERE field=$1

                    ORDER BY grade,name

                    """,

                    field

                )


            else:


                students = await conn.fetch(

                    """
                    SELECT
                        user_id,
                        name,
                        phone,
                        grade,
                        field

                    FROM users

                    WHERE field=$1
                    AND grade=$2

                    ORDER BY name

                    """,

                    field,
                    grade

                )



        elif data.startswith(
            "filter_grade_"
        ):


            grade = data.replace(
                "filter_grade_",
                ""
            )


            students = await conn.fetch(

                """
                SELECT
                    user_id,
                    name,
                    phone,
                    grade,
                    field

                FROM users

                WHERE grade=$1

                ORDER BY field,name

                """,

                grade

            )


        else:

            return




    if not students:


        await query.message.reply_text(
            "❌ دانش‌آموزی پیدا نشد."
        )

        return



    keyboard=[]


    for student in students:


        keyboard.append([

            InlineKeyboardButton(

                f"{student['name']} | {student['grade']} | {student['field']}",

                callback_data=f"admin_user_{student['user_id']}"

            )

        ])



    await query.message.reply_text(

        f"👥 تعداد دانش‌آموزان: {len(students)}",

        reply_markup=InlineKeyboardMarkup(
            keyboard
        )

    )
# ==========================
# پروفایل دانش‌آموز
# ==========================

async def admin_user_profile(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()


    user_id = int(
        query.data.replace(
            "admin_user_",
            ""
        )
    )


    user = await get_user(user_id)


    if not user:

        await query.message.reply_text(
            "❌ اطلاعات پیدا نشد."
        )

        return



    await query.message.reply_text(

f"""
👤 پروفایل دانش‌آموز

نام:
{user['name']}

📱 شماره تماس:
{user['phone']}

📚 پایه:
{user['grade']}

🎯 رشته:
{user['field']}

📅 تاریخ عضویت:
{gregorian_to_jalali(user['join_date'])}

""",

reply_markup=InlineKeyboardMarkup([

    [

        InlineKeyboardButton(
            "📊 مشاهده عملکرد",
            callback_data=f"admin_performance_{user_id}"
        )

    ],

    [

        InlineKeyboardButton(
            "📩 ارسال پیام اختصاصی",
            callback_data=f"admin_direct_message_{user_id}"
        )

    ],

    [

        InlineKeyboardButton(
            "🗑 حذف دانش‌آموز",
            callback_data=f"delete_user_{user_id}"
        )

    ]

])

    )



# ==========================
# عملکرد دانش‌آموز
# ==========================


async def admin_performance(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()


    user_id = int(

        query.data.replace(
            "admin_performance_",
            ""
        )

    )


    user = await get_user(user_id)


    stats = await get_period_stats(user_id)

    subjects = await get_period_subject_stats(user_id)



    text=f"""

📊 گزارش عملکرد دانش‌آموز

👤 {user['name']}

━━━━━━━━━━━━

🔥 مجموع مطالعه:
{stats.get('total_hours',0)} ساعت

📝 مجموع تست:
{stats.get('total_tests',0)}

📅 روزهای مطالعه:
{stats.get('study_days',0)}

📈 میانگین:
{stats.get('avg_hours',0)}

━━━━━━━━━━━━

📚 عملکرد دروس:

"""



    for item in subjects:


        text += f"""

📖 {item['subject']}

⏱ {item.get('total_hours',0)} ساعت

📝 {item.get('total_tests',0)} تست

"""



    await query.message.reply_text(

        text,

        reply_markup=InlineKeyboardMarkup([

            [

                InlineKeyboardButton(
                    "📩 ارسال پیام",
                    callback_data=f"admin_direct_message_{user_id}"
                )

            ],

            [

                InlineKeyboardButton(
                    "🔙 بازگشت",
                    callback_data=f"admin_user_{user_id}"
                )

            ]

        ])

    )



# ==========================
# حذف دانش‌آموز
# ==========================


async def delete_user_confirm(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()


    user_id=int(

        query.data.replace(
            "delete_user_",
            ""
        )

    )


    await query.message.reply_text(

        "⚠️ آیا از حذف این دانش‌آموز مطمئن هستید؟",

        reply_markup=InlineKeyboardMarkup([


            [

                InlineKeyboardButton(
                    "✅ حذف شود",
                    callback_data=f"confirm_delete_{user_id}"
                )

            ],


            [

                InlineKeyboardButton(
                    "❌ لغو",
                    callback_data=f"admin_user_{user_id}"
                )

            ]

        ])

    )





async def delete_user_final(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
):

    query=update.callback_query

    await query.answer()


    user_id=int(

        query.data.replace(
            "confirm_delete_",
            ""
        )

    )


    pool=await get_db()


    async with pool.acquire() as conn:

        await conn.execute(

            """
            DELETE FROM users
            WHERE user_id=$1
            """,

            user_id

        )


    await query.message.reply_text(
        "✅ دانش‌آموز حذف شد."
    )



# ==========================
# گزارش متنی دانش‌آموزان
# ==========================


async def admin_students_report(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()


    pool = await get_db()


    async with pool.acquire() as conn:


        students = await conn.fetch(

            """
            SELECT
                name,
                phone,
                grade,
                field,
                join_date

            FROM users

            ORDER BY grade,name

            """

        )



    if not students:

        await query.message.reply_text(
            "❌ دانش‌آموزی وجود ندارد."
        )

        return



    result = "📋 گزارش دانش‌آموزان پرفورم\n\n"



    current_grade = None



    for s in students:


        if current_grade != s["grade"]:


            current_grade=s["grade"]


            result += f"""

━━━━━━━━━━━━

📚 پایه {current_grade}

━━━━━━━━━━━━

"""



        result += f"""

👤 {s['name']}

📱 {s['phone']}

🎯 {s['field']}

📅 {gregorian_to_jalali(s['join_date'])}


"""



        if len(result)>3500:


            await query.message.reply_text(
                result
            )

            result=""



    if result:


        await query.message.reply_text(
            result
        )
# ==========================
# خروجی متنی دانش آموزان
# جایگزین کامل admin_excel
# ==========================

async def admin_excel(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()


    pool = await get_db()


    async with pool.acquire() as conn:

        students = await conn.fetch(

            """
            SELECT

                user_id,
                name,
                phone,
                grade,
                field,
                join_date

            FROM users

            ORDER BY
                grade,
                field,
                name

            """

        )


    if not students:

        await query.message.reply_text(

            "❌ دانش‌آموزی وجود ندارد."

        )

        return



    text = """
📋 لیست کامل دانش‌آموزان پرفورم


"""


    current_grade = None



    for student in students:


        if current_grade != student["grade"]:


            current_grade = student["grade"]


            text += f"""

━━━━━━━━━━━━━━

📚 پایه {current_grade}

━━━━━━━━━━━━━━

"""



        date = gregorian_to_jalali(student["join_date"])


        text += f"""

👤 نام:
{student['name']}

📱 شماره:
{student['phone']}

🎯 رشته:
{student['field']}

📅 عضویت:
{date}

--------------------

"""



        if len(text) > 3500:


            await query.message.reply_text(
                text
            )

            text = ""



    if text:


        await query.message.reply_text(

            text,

            reply_markup=InlineKeyboardMarkup([

                [

                    InlineKeyboardButton(

                        "🔙 پنل مدیریت",

                        callback_data="admin_panel"

                    )

                ]

            ])

        )
# ==========================
# آمار کلی کاربران
# ==========================

async def admin_general_stats(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()


    pool = await get_db()


    today = datetime.now().date()

    week = today - timedelta(days=7)

    month = today - timedelta(days=30)



    async with pool.acquire() as conn:


        total = await conn.fetchval(

            """
            SELECT COUNT(*)
            FROM users
            """

        )


        today_count = await conn.fetchval(

            """
            SELECT COUNT(*)
            FROM users
            WHERE DATE(join_date)=CURRENT_DATE
            """

        )


        week_count = await conn.fetchval(

            """
            SELECT COUNT(*)
            FROM users
            WHERE join_date >= $1
            """,

            week

        )


        month_count = await conn.fetchval(

            """
            SELECT COUNT(*)
            FROM users
            WHERE join_date >= $1
            """,

            month

        )



    await query.message.reply_text(

f"""
📊 آمار کلی پرفورم


👥 تعداد کل دانش‌آموزان:
{total} نفر


🆕 ثبت‌نام امروز:
{today_count} نفر


📅 ثبت‌نام ۷ روز اخیر:
{week_count} نفر


📆 ثبت‌نام ۳۰ روز اخیر:
{month_count} نفر

""",

reply_markup=InlineKeyboardMarkup([

    [

        InlineKeyboardButton(
            "🔙 پنل مدیریت",
            callback_data="admin_panel"
        )

    ]

])

)
# ==========================
# دانش‌آموزان برتر
# ==========================

async def admin_top_students(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()


    await query.message.reply_text(

        "🏆 دانش‌آموزان برتر\n\nمعیار امتیازدهی را انتخاب کنید:",

        reply_markup=InlineKeyboardMarkup([

            [
                InlineKeyboardButton(
                    "🔥 بر اساس ساعت مطالعه",
                    callback_data="top_metric_hours"
                )
            ],

            [
                InlineKeyboardButton(
                    "📝 بر اساس تعداد تست",
                    callback_data="top_metric_tests"
                )
            ],

            [
                InlineKeyboardButton(
                    "🔙 پنل مدیریت",
                    callback_data="admin_panel"
                )
            ]

        ])

    )



# ==========================
# انتخاب بازه زمانی
# ==========================

async def top_metric_period(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()


    metric = query.data.replace(
        "top_metric_",
        ""
    )


    context.user_data["top_metric"] = metric


    await query.message.reply_text(

        "📅 بازه زمانی را انتخاب کنید:",

        reply_markup=InlineKeyboardMarkup([

            [
                InlineKeyboardButton(
                    "📆 برتر روز",
                    callback_data="top_period_today"
                )
            ],

            [
                InlineKeyboardButton(
                    "📅 برتر هفته",
                    callback_data="top_period_week"
                )
            ],

            [
                InlineKeyboardButton(
                    "🗓 برتر ماه",
                    callback_data="top_period_month"
                )
            ],

            [
                InlineKeyboardButton(
                    "📊 برتر سال",
                    callback_data="top_period_year"
                )
            ],

            [
                InlineKeyboardButton(
                    "🔙 بازگشت",
                    callback_data="admin_top_students"
                )
            ]

        ])

    )



async def show_top_students(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()


    period = query.data.replace(
        "top_period_",
        ""
    )


    metric = context.user_data.get(
        "top_metric",
        "hours"
    )


    start_date, is_single_day = get_top_period_start(period)


    period_label = TOP_PERIOD_LABELS.get(
        period,
        period
    )


    if metric == "tests":

        column = "tests"

        title = f"🏆 ۱۰ دانش‌آموز برتر بر اساس تست ({period_label}):\n\n"

        icon = "📝"

        unit = "تست"

    else:

        column = "hours"

        title = f"🏆 ۱۰ دانش‌آموز برتر بر اساس مطالعه ({period_label}):\n\n"

        icon = "🔥"

        unit = "ساعت"



    pool = await get_db()


    async with pool.acquire() as conn:


        if is_single_day:


            students = await conn.fetch(

                f"""
                SELECT
                    users.name,
                    SUM(study_logs.{column}) AS total

                FROM users

                JOIN study_logs

                ON users.user_id = study_logs.user_id

                WHERE study_logs.log_date = $1

                GROUP BY users.name

                ORDER BY total DESC

                LIMIT 10

                """,

                start_date

            )


        else:


            students = await conn.fetch(

                f"""
                SELECT
                    users.name,
                    SUM(study_logs.{column}) AS total

                FROM users

                JOIN study_logs

                ON users.user_id = study_logs.user_id

                WHERE study_logs.log_date >= $1

                GROUP BY users.name

                ORDER BY total DESC

                LIMIT 10

                """,

                start_date

            )



    if not students:

        text = title + "برای این بازه هنوز گزارشی ثبت نشده است."


    else:

        text = title


        for i, student in enumerate(students, start=1):

            text += f"""

{i}️⃣ {student['name']}

{icon} {student['total']} {unit}

"""



    await query.message.reply_text(

        text,

        reply_markup=InlineKeyboardMarkup([

            [

                InlineKeyboardButton(
                    "🔙 پنل مدیریت",
                    callback_data="admin_panel"
                )

            ]

        ])

    )

# ==========================
# پیام مستقیم به دانش‌آموز
# ==========================

async def admin_direct_message(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()


    user_id = int(

        query.data.replace(
            "admin_direct_message_",
            ""
        )

    )


    context.user_data["direct_user_id"] = user_id

    context.user_data["admin_step"] = "direct_message"


    await query.message.reply_text(

        "📩 متن پیام را ارسال کنید:"

    )



async def send_direct_message(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
):

    user_id = context.user_data.get(
        "direct_user_id"
    )


    if not user_id:

        return



    text = update.message.text



    try:

        await context.bot.send_message(

            chat_id=user_id,

            text=f"""

📩 پیام از مدیریت پرفورم:

{text}

"""

        )


        await update.message.reply_text(

            "✅ پیام ارسال شد."

        )


    except:


        await update.message.reply_text(

            "❌ ارسال پیام ناموفق بود."

        )



    context.user_data.pop(
        "direct_user_id",
        None
    )


    context.user_data.pop(
        "admin_step",
        None
    )

# ==========================
# پیام گروهی (Broadcast)
# ==========================

async def admin_broadcast_menu(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()


    await query.message.reply_text(

        "📢 ارسال پیام گروهی\n\nمخاطبین پیام را انتخاب کنید:",

        reply_markup=InlineKeyboardMarkup([

            [
                InlineKeyboardButton(
                    "👥 همه دانش‌آموزان",
                    callback_data="broadcast_all"
                )
            ],

            [
                InlineKeyboardButton(
                    "🎯 فیلتر بر اساس رشته/پایه",
                    callback_data="broadcast_filter"
                )
            ],

            [
                InlineKeyboardButton(
                    "🔙 بازگشت",
                    callback_data="admin_panel"
                )
            ]

        ])

    )



async def broadcast_filter(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()


    await query.message.reply_text(

        "نوع فیلتر را انتخاب کنید:",

        reply_markup=InlineKeyboardMarkup([

            [
                InlineKeyboardButton(
                    "🎓 بر اساس رشته",
                    callback_data="broadcast_field"
                )
            ],

            [
                InlineKeyboardButton(
                    "📚 بر اساس پایه",
                    callback_data="broadcast_grade"
                )
            ],

            [
                InlineKeyboardButton(
                    "🔙 بازگشت",
                    callback_data="admin_broadcast"
                )
            ]

        ])

    )



async def broadcast_field(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()


    await query.message.reply_text(

        "🎓 رشته مورد نظر را انتخاب کنید:",

        reply_markup=InlineKeyboardMarkup([

            [
                InlineKeyboardButton(
                    "🧪 تجربی",
                    callback_data="msg_field_تجربی"
                )
            ],

            [
                InlineKeyboardButton(
                    "📐 ریاضی",
                    callback_data="msg_field_ریاضی"
                )
            ],

            [
                InlineKeyboardButton(
                    "📚 انسانی",
                    callback_data="msg_field_انسانی"
                )
            ],

            [
                InlineKeyboardButton(
                    "🔙 بازگشت",
                    callback_data="broadcast_filter"
                )
            ]

        ])

    )



async def broadcast_grade(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()


    await query.message.reply_text(

        "📚 پایه مورد نظر را انتخاب کنید:",

        reply_markup=InlineKeyboardMarkup([

            [
                InlineKeyboardButton(
                    "دهم",
                    callback_data="msg_grade_دهم"
                )
            ],

            [
                InlineKeyboardButton(
                    "یازدهم",
                    callback_data="msg_grade_یازدهم"
                )
            ],

            [
                InlineKeyboardButton(
                    "دوازدهم",
                    callback_data="msg_grade_دوازدهم"
                )
            ],

            [
                InlineKeyboardButton(
                    "🔙 بازگشت",
                    callback_data="broadcast_filter"
                )
            ]

        ])

    )



# انتخاب رشته انجام شد -> حالا پایه را می‌پرسیم
# (پترن این تابع در main.py باید msg_field_ را بگیرد
#  ولی msg_field_grade_ را نگیرد، چون آن مرحله بعدی است)

async def broadcast_field_grade(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()


    field = query.data.replace(
        "msg_field_",
        ""
    )


    context.user_data["broadcast_field"] = field


    await query.message.reply_text(

        f"📚 پایه (رشته {field}) را انتخاب کنید:",

        reply_markup=InlineKeyboardMarkup([

            [
                InlineKeyboardButton(
                    "دهم",
                    callback_data="msg_field_grade_دهم"
                )
            ],

            [
                InlineKeyboardButton(
                    "یازدهم",
                    callback_data="msg_field_grade_یازدهم"
                )
            ],

            [
                InlineKeyboardButton(
                    "دوازدهم",
                    callback_data="msg_field_grade_دوازدهم"
                )
            ],

            [
                InlineKeyboardButton(
                    "همه پایه‌ها",
                    callback_data="msg_field_grade_all"
                )
            ]

        ])

    )



# ==========================
# نهایی کردن فیلتر و دریافت متن پیام
# ==========================

async def admin_start_broadcast(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()


    data = query.data


    grade = None

    field = None


    if data == "broadcast_all":

        pass


    elif data.startswith("msg_field_grade_"):

        grade = data.replace("msg_field_grade_", "")

        if grade == "all":
            grade = None

        field = context.user_data.get("broadcast_field")


    elif data.startswith("msg_grade_"):

        grade = data.replace("msg_grade_", "")


    else:

        return



    context.user_data["broadcast_target"] = {

        "grade": grade,

        "field": field

    }


    context.user_data["admin_step"] = "broadcast_text"


    await query.message.reply_text(

        "📝 متن پیام گروهی را ارسال کنید:\n\n"
        "(این پیام برای همه‌ی دانش‌آموزان مطابق فیلتر انتخابی ارسال می‌شود)"

    )



async def admin_send_broadcast_text(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
):

    target = context.user_data.get(
        "broadcast_target",
        {}
    )


    grade = target.get("grade")

    field = target.get("field")


    text = update.message.text


    user_ids = await get_user_ids(
        grade=grade,
        field=field
    )


    sent = 0

    failed = 0


    for user_id in user_ids:

        try:

            await context.bot.send_message(

                chat_id=user_id,

                text=f"""

📢 پیام از مدیریت پرفورم:

{text}

"""

            )

            sent += 1


        except:

            failed += 1



    await update.message.reply_text(

        f"✅ پیام ارسال شد.\n\n"
        f"📤 موفق: {sent} نفر\n"
        f"❌ ناموفق: {failed} نفر",

        reply_markup=InlineKeyboardMarkup([

            [

                InlineKeyboardButton(
                    "🔙 پنل مدیریت",
                    callback_data="admin_panel"
                )

            ]

        ])

    )


    context.user_data.pop("broadcast_target", None)

    context.user_data.pop("admin_step", None)