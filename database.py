import asyncpg

from config import DATABASE_URL

from datetime import date, timedelta

import jdatetime



db_pool = None







# ==========================
# اتصال دیتابیس
# ==========================


async def init_db():


    global db_pool



    db_pool = await asyncpg.create_pool(

        DATABASE_URL

    )



    async with db_pool.acquire() as conn:



        await conn.execute(

            """

            CREATE TABLE IF NOT EXISTS users (

                user_id BIGINT PRIMARY KEY,

                name TEXT,

                phone TEXT,

                grade TEXT,

                field TEXT,

                join_date DATE DEFAULT CURRENT_DATE

            );

            """

        )





        # فقط برای کاربران قدیمی که تاریخ عضویت ندارند

        await conn.execute(

            """

            UPDATE users

            SET join_date = CURRENT_DATE

            WHERE join_date IS NULL;

            """

        )







        await conn.execute(

            """

            CREATE TABLE IF NOT EXISTS study_logs (

                id SERIAL PRIMARY KEY,

                user_id BIGINT,

                subject TEXT,

                hours INTEGER DEFAULT 0,

                tests INTEGER DEFAULT 0,

                log_date DATE DEFAULT CURRENT_DATE

            );

            """

        )







        await conn.execute(

            """

            CREATE UNIQUE INDEX IF NOT EXISTS unique_daily_subject

            ON study_logs

            (

                user_id,

                subject,

                log_date

            );

            """

        )









# ==========================
# بستن دیتابیس
# ==========================


async def close_db():


    global db_pool



    if db_pool:


        await db_pool.close()










# ==========================
# دریافت اتصال
# ==========================


async def get_db():


    global db_pool



    if db_pool is None:


        raise Exception(

            "Database pool is not initialized"

        )



    return db_pool











# ==========================
# کاربران
# ==========================


async def save_user(

        user_id,

        name,

        phone,

        grade,

        field

):


    pool = await get_db()



    async with pool.acquire() as conn:



        await conn.execute(

            """

            INSERT INTO users

            (

                user_id,

                name,

                phone,

                grade,

                field

            )


            VALUES

            ($1,$2,$3,$4,$5)



            ON CONFLICT(user_id)

            DO UPDATE SET



            name=$2,

            phone=$3,

            grade=$4,

            field=$5



            """,


            user_id,

            name,

            phone,

            grade,

            field

        )












async def get_user(user_id):


    pool = await get_db()



    async with pool.acquire() as conn:



        return await conn.fetchrow(

            """

            SELECT *

            FROM users

            WHERE user_id=$1

            """,


            user_id

        )









# ==================================
# ویرایش اطلاعات تحصیلی
# ==================================


async def update_education_profile(

        user_id,

        grade,

        field

):


    pool = await get_db()



    async with pool.acquire() as conn:



        await conn.execute(

            """

            UPDATE users


            SET

            grade=$2,

            field=$3


            WHERE user_id=$1



            """,


            user_id,

            grade,

            field

        )









# ==================================
# حذف تاریخچه مطالعه
# ==================================


async def delete_user_study_history(

        user_id

):


    pool = await get_db()



    async with pool.acquire() as conn:



        await conn.execute(

            """

            DELETE FROM study_logs


            WHERE user_id=$1


            """,


            user_id

        )
# ==========================
# گزارش مطالعه
# ==========================



async def get_subject_report(

        user_id,

        subject,

        target_date

):


    pool = await get_db()



    async with pool.acquire() as conn:



        return await conn.fetchrow(

            """

            SELECT *

            FROM study_logs


            WHERE user_id=$1


            AND subject=$2


            AND log_date=$3



            """,


            user_id,

            subject,

            target_date

        )













async def save_or_update_report(

        user_id,

        subject,

        hours,

        tests,

        target_date

):


    pool = await get_db()



    async with pool.acquire() as conn:



        await conn.execute(

            """

            INSERT INTO study_logs

            (

                user_id,

                subject,

                hours,

                tests,

                log_date

            )



            VALUES

            ($1,$2,$3,$4,$5)



            ON CONFLICT

            (

                user_id,

                subject,

                log_date

            )



            DO UPDATE SET



            hours=$3,

            tests=$4



            """,


            user_id,

            subject,

            hours,

            tests,

            target_date

        )












async def add_to_report(

        user_id,

        subject,

        hours,

        tests,

        target_date

):


    pool = await get_db()



    async with pool.acquire() as conn:



        await conn.execute(

            """

            UPDATE study_logs



            SET



            hours = hours + $3,



            tests = tests + $4



            WHERE user_id=$1



            AND subject=$2



            AND log_date=$5



            """,


            user_id,

            subject,

            hours,

            tests,

            target_date

        )












async def get_day_report(

        user_id,

        target_date

):


    pool = await get_db()



    async with pool.acquire() as conn:



        return await conn.fetch(

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












# ==========================
# آمار کلی بازه‌ای
# ==========================



async def get_period_stats(

        user_id,

        start_date=None

):


    pool = await get_db()



    async with pool.acquire() as conn:



        if start_date:



            result = await conn.fetchrow(

                """

                SELECT


                COALESCE(SUM(hours),0) AS total_hours,


                COALESCE(SUM(tests),0) AS total_tests,


                COUNT(DISTINCT log_date) AS study_days



                FROM study_logs



                WHERE user_id=$1



                AND log_date >= $2



                """,


                user_id,

                start_date

            )



        else:



            result = await conn.fetchrow(

                """

                SELECT


                COALESCE(SUM(hours),0) AS total_hours,


                COALESCE(SUM(tests),0) AS total_tests,


                COUNT(DISTINCT log_date) AS study_days



                FROM study_logs



                WHERE user_id=$1



                """,


                user_id

            )






    days = result["study_days"]



    if days > 0:


        avg_hours = round(

            result["total_hours"] / days,

            1

        )


        avg_tests = round(

            result["total_tests"] / days

        )



    else:


        avg_hours = 0

        avg_tests = 0





    return {


        "total_hours": result["total_hours"],


        "total_tests": result["total_tests"],


        "avg_hours": avg_hours,


        "avg_tests": avg_tests

    }
# ==========================
# عملکرد دروس در یک بازه
# ==========================



async def get_period_subject_stats(

        user_id,

        start_date=None

):


    pool = await get_db()



    async with pool.acquire() as conn:



        if start_date:



            return await conn.fetch(

                """

                SELECT



                subject,



                SUM(hours) AS total_hours,



                SUM(tests) AS total_tests



                FROM study_logs



                WHERE user_id=$1



                AND log_date >= $2



                GROUP BY subject



                ORDER BY total_hours DESC



                """,


                user_id,

                start_date

            )




        else:



            return await conn.fetch(

                """

                SELECT



                subject,



                SUM(hours) AS total_hours,



                SUM(tests) AS total_tests



                FROM study_logs



                WHERE user_id=$1



                GROUP BY subject



                ORDER BY total_hours DESC



                """,


                user_id

            )













# ==========================
# آمار امروز
# ==========================



async def get_today_stats(user_id):


    return await get_period_stats(

        user_id,

        date.today()

    )








async def get_today_subject_stats(user_id):


    return await get_period_subject_stats(

        user_id,

        date.today()

    )












# ==========================
# هفته جاری شمسی
# شنبه تا امروز
# ==========================



def week_start():


    today = date.today()



    weekday = today.weekday()



    days_from_saturday = (

        weekday - 5

    ) % 7



    return today - timedelta(

        days=days_from_saturday

    )









async def get_week_stats(user_id):


    return await get_period_stats(

        user_id,

        week_start()

    )







async def get_week_subject_stats(user_id):


    return await get_period_subject_stats(

        user_id,

        week_start()

    )












# ==========================
# ماه جاری شمسی
# ==========================



def month_start():


    today = jdatetime.date.today()



    first_day = jdatetime.date(

        today.year,

        today.month,

        1

    )



    return first_day.togregorian()










async def get_month_stats(user_id):


    return await get_period_stats(

        user_id,

        month_start()

    )








async def get_month_subject_stats(user_id):


    return await get_period_subject_stats(

        user_id,

        month_start()

    )












# ==========================
# سه ماه اخیر شمسی
# ==========================



def three_month_start():


    today = jdatetime.date.today()



    year = today.year

    month = today.month



    month -= 2



    if month <= 0:


        month += 12

        year -= 1






    first_day = jdatetime.date(

        year,

        month,

        1

    )



    return first_day.togregorian()










async def get_three_month_stats(user_id):


    return await get_period_stats(

        user_id,

        three_month_start()

    )








async def get_three_month_subject_stats(user_id):


    return await get_period_subject_stats(

        user_id,

        three_month_start()

    )
# ==========================
# کل دوران عضویت
# ==========================



async def get_all_time_stats(user_id):


    return await get_period_stats(

        user_id,

        None

    )









async def get_all_time_subject_stats(user_id):


    return await get_period_subject_stats(

        user_id,

        None

    )












# ==========================
# حذف آخرین گزارش
# ==========================



async def delete_last_report(user_id):


    pool = await get_db()



    async with pool.acquire() as conn:



        await conn.execute(

            """

            DELETE FROM study_logs



            WHERE id =



            (


                SELECT id


                FROM study_logs


                WHERE user_id=$1


                ORDER BY id DESC


                LIMIT 1


            )



            """,


            user_id

        )









# ==========================
# پاکسازی کامل اطلاعات تحصیلی
# ==========================

# این تابع فقط تاریخچه مطالعه را حذف می‌کند.
# اطلاعات کاربر و تاریخ عضویت حفظ می‌شود.


async def reset_study_history(user_id):


    await delete_user_study_history(

        user_id

    )









# ==========================
# بررسی تغییر اطلاعات تحصیلی
# ==========================



async def education_changed(

        user_id,

        new_grade,

        new_field

):


    user = await get_user(

        user_id

    )



    if not user:

        return False




    if (

        user["grade"] != new_grade

        or

        user["field"] != new_field

    ):


        return True




    return False
# ==========================
# توابع مدیریت ربات
# ==========================


# دریافت لیست دانش آموزان با فیلتر پایه و رشته
async def get_students(
        grade=None,
        field=None
):

    pool = await get_db()

    async with pool.acquire() as conn:

        query = """
        SELECT
            user_id,
            name,
            phone,
            grade,
            field,
            join_date
        FROM users
        WHERE 1=1
        """

        values = []


        if grade:

            values.append(grade)

            query += f"""
            AND grade=${len(values)}
            """


        if field:

            values.append(field)

            query += f"""
            AND field=${len(values)}
            """


        query += """
        ORDER BY join_date DESC
        """


        return await conn.fetch(
            query,
            *values
        )





# دریافت اطلاعات کامل یک دانش آموز
async def get_student_profile(
        user_id
):

    pool = await get_db()

    async with pool.acquire() as conn:

        return await conn.fetchrow(
            """

            SELECT
                *
            FROM users

            WHERE user_id=$1

            """,

            user_id

        )






# دریافت آمار کامل یک دانش آموز برای مدیر
async def get_admin_student_stats(
        user_id
):

    pool = await get_db()


    async with pool.acquire() as conn:


        total = await conn.fetchrow(
            """

            SELECT

            COALESCE(SUM(hours),0) AS total_hours,

            COALESCE(SUM(tests),0) AS total_tests,

            COUNT(DISTINCT log_date) AS study_days


            FROM study_logs


            WHERE user_id=$1


            """,

            user_id

        )


        subjects = await conn.fetch(
            """

            SELECT

            subject,

            SUM(hours) AS hours,

            SUM(tests) AS tests


            FROM study_logs


            WHERE user_id=$1


            GROUP BY subject


            ORDER BY hours DESC


            """,

            user_id

        )


    return {

        "total": total,

        "subjects": subjects

    }






# گرفتن آیدی دانش آموزان برای ارسال پیام گروهی
async def get_user_ids(
        grade=None,
        field=None
):


    students = await get_students(
        grade,
        field
    )


    return [

        student["user_id"]

        for student in students

    ]






# تعداد کل کاربران
async def count_users():

    pool = await get_db()


    async with pool.acquire() as conn:


        result = await conn.fetchval(
            """

            SELECT COUNT(*)

            FROM users

            """
        )


    return result