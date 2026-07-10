import threading

from flask import Flask

from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters
)

from config import BOT_TOKEN
from database import init_db


# ==========================
# ثبت نام
# ==========================

from handlers.start import (
    start,
    save_name,
    save_phone,
    save_grade,
    save_field
)


# ==========================
# پروفایل
# ==========================

from handlers.profile import (
    profile,
    edit_profile,
    confirm_edit_profile,
    cancel_edit_profile,
    edit_grade,
    edit_field,
    save_edited_profile,
    back_profile
)


# ==========================
# آمار
# ==========================

from handlers.stats import (
    stats,
    show_stats
)


# ==========================
# گزارش مطالعه
# ==========================

from handlers.reports import (
    new_report,
    choose_date,
    choose_type,
    choose_old_base,
    choose_subject,
    choose_hour,
    save_report,
    finish_report,
    replace_report,
    add_report,
    cancel_report,
    back_report
)


# ==========================
# منو
# ==========================

from handlers.menu import (
    plans,
    back_to_menu
)


# ==========================
# مشاوره
# ==========================

from handlers.consulting import (
    show_plan,
    register_plan,
    more_info
)


# ==========================
# مدیریت
# ==========================

from handlers.admin import (

    admin_start,
    admin_panel,

    admin_students,
    admin_all_students,
    admin_separated_students,

    admin_field_based,
    admin_field_grade,
    admin_grade_based,

    show_filtered_students,

    admin_user_profile,
    admin_performance,

    admin_general_stats,

    # گزارش متنی جایگزین اکسل
    admin_excel,

    # برترها
    admin_top_students,
    top_metric_period,
    show_top_students,

    # پیام اختصاصی
    admin_direct_message,
    send_direct_message,

    # حذف
    delete_user_confirm,
    delete_user_final,

    # پیام گروهی
    admin_broadcast_menu,
    broadcast_filter,
    broadcast_field,
    broadcast_grade,
    broadcast_field_grade,
    admin_start_broadcast,
    admin_send_broadcast_text

)



# ==========================
# دیتابیس
# ==========================

async def post_init(app):

    await init_db()



# ==========================
# پیام متنی
# ==========================

async def text_handler(update, context):


    if context.user_data.get(
        "admin_step"
    ) == "broadcast_text":


        await admin_send_broadcast_text(
            update,
            context
        )

        return



    if context.user_data.get(
        "admin_step"
    ) == "direct_message":


        await send_direct_message(
            update,
            context
        )

        return



    step = context.user_data.get(
        "step"
    )


    if step == "name":


        await save_name(
            update,
            context
        )

        return



# ==========================
# سرور وب برای باز نگه داشتن پورت (Render)
# ==========================

web_app = Flask('')


@web_app.route('/')
def home():
    return "ربات پرفورم روشن است ✅"


def run_web():

    import os

    port = int(
        os.environ.get(
            "PORT",
            10000
        )
    )

    web_app.run(
        host="0.0.0.0",
        port=port
    )


def keep_alive():

    t = threading.Thread(
        target=run_web
    )

    t.start()



# ==========================
# اجرای ربات
# ==========================

def main():


    app = (

        ApplicationBuilder()

        .token(BOT_TOKEN)

        .post_init(post_init)

        .build()

    )



    # شروع

    app.add_handler(
        CommandHandler(
            "start",
            start
        )
    )


    app.add_handler(
        CommandHandler(
            "admin",
            admin_start
        )
    )



    # متن

    app.add_handler(

        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            text_handler
        )

    )



    # تماس

    app.add_handler(

        MessageHandler(
            filters.CONTACT,
            save_phone
        )

    )



    # ثبت نام

    app.add_handler(
        CallbackQueryHandler(
            save_grade,
            pattern="^grade_"
        )
    )


    app.add_handler(
        CallbackQueryHandler(
            save_field,
            pattern="^field_(?!students_)"
        )
    )
    # ==========================
    # پروفایل
    # ==========================

    app.add_handler(
        CallbackQueryHandler(
            profile,
            pattern="^profile$"
        )
    )


    app.add_handler(
        CallbackQueryHandler(
            edit_profile,
            pattern="^edit_profile$"
        )
    )


    app.add_handler(
        CallbackQueryHandler(
            confirm_edit_profile,
            pattern="^confirm_edit_profile$"
        )
    )


    app.add_handler(
        CallbackQueryHandler(
            cancel_edit_profile,
            pattern="^cancel_edit_profile$"
        )
    )


    app.add_handler(
        CallbackQueryHandler(
            back_profile,
            pattern="^back_profile$"
        )
    )


    app.add_handler(
        CallbackQueryHandler(
            edit_grade,
            pattern="^edit_grade_"
        )
    )


    app.add_handler(
        CallbackQueryHandler(
            edit_field,
            pattern="^edit_field_"
        )
    )


    app.add_handler(
        CallbackQueryHandler(
            save_edited_profile,
            pattern="^save_edited_profile$"
        )
    )



    # ==========================
    # آمار
    # ==========================

    app.add_handler(
        CallbackQueryHandler(
            stats,
            pattern="^stats$"
        )
    )


    app.add_handler(
        CallbackQueryHandler(
            show_stats,
            pattern="^stats_"
        )
    )



    # ==========================
    # مشاوره
    # ==========================

    app.add_handler(
        CallbackQueryHandler(
            plans,
            pattern="^plans$"
        )
    )


    app.add_handler(
        CallbackQueryHandler(
            show_plan,
            pattern="^plan_"
        )
    )


    app.add_handler(
        CallbackQueryHandler(
            register_plan,
            pattern="^register_plan$"
        )
    )


    app.add_handler(
        CallbackQueryHandler(
            more_info,
            pattern="^more_info$"
        )
    )



    # ==========================
    # گزارش مطالعه
    # ==========================

    app.add_handler(
        CallbackQueryHandler(
            new_report,
            pattern="^new_report$"
        )
    )


    app.add_handler(
        CallbackQueryHandler(
            choose_date,
            pattern="^date_"
        )
    )


    app.add_handler(
        CallbackQueryHandler(
            choose_type,
            pattern="^type_"
        )
    )


    app.add_handler(
        CallbackQueryHandler(
            choose_old_base,
            pattern="^old_"
        )
    )


    app.add_handler(
        CallbackQueryHandler(
            choose_subject,
            pattern="^sub_"
        )
    )


    app.add_handler(
        CallbackQueryHandler(
            choose_hour,
            pattern="^hour_"
        )
    )


    app.add_handler(
        CallbackQueryHandler(
            save_report,
            pattern="^test_"
        )
    )


    app.add_handler(
        CallbackQueryHandler(
            replace_report,
            pattern="^replace_report$"
        )
    )


    app.add_handler(
        CallbackQueryHandler(
            add_report,
            pattern="^add_report$"
        )
    )


    app.add_handler(
        CallbackQueryHandler(
            cancel_report,
            pattern="^cancel_report$"
        )
    )


    app.add_handler(
        CallbackQueryHandler(
            finish_report,
            pattern="^finish_report$"
        )
    )


    app.add_handler(
        CallbackQueryHandler(
            back_report,
            pattern="^back_report$"
        )
    )



    # ==========================
    # پنل مدیریت
    # ==========================

    app.add_handler(
        CallbackQueryHandler(
            admin_panel,
            pattern="^admin_panel$"
        )
    )


    app.add_handler(
        CallbackQueryHandler(
            admin_students,
            pattern="^admin_students$"
        )
    )


    app.add_handler(
        CallbackQueryHandler(
            admin_all_students,
            pattern="^admin_all_students$"
        )
    )


    app.add_handler(
        CallbackQueryHandler(
            admin_separated_students,
            pattern="^admin_separated_students$"
        )
    )


    app.add_handler(
        CallbackQueryHandler(
            admin_field_based,
            pattern="^admin_field_based$"
        )
    )


    app.add_handler(
        CallbackQueryHandler(
            admin_field_grade,
            pattern="^filter_field_"
        )
    )


    app.add_handler(
        CallbackQueryHandler(
            admin_grade_based,
            pattern="^admin_grade_based$"
        )
    )


    app.add_handler(
        CallbackQueryHandler(
            show_filtered_students,
            pattern="^(filter_field_grade_|filter_grade_)"
        )
    )



    # پروفایل دانش آموز مدیریت

    app.add_handler(
        CallbackQueryHandler(
            admin_user_profile,
            pattern="^admin_user_"
        )
    )


    app.add_handler(
        CallbackQueryHandler(
            admin_performance,
            pattern="^admin_performance_"
        )
    )



    # پیام اختصاصی

    app.add_handler(
        CallbackQueryHandler(
            admin_direct_message,
            pattern="^admin_direct_message_"
        )
    )



    # ==========================
    # دانش آموزان برتر
    # ==========================

    app.add_handler(
        CallbackQueryHandler(
            admin_top_students,
            pattern="^admin_top_students$"
        )
    )


    app.add_handler(
        CallbackQueryHandler(
            top_metric_period,
            pattern="^top_metric_"
        )
    )


    app.add_handler(
        CallbackQueryHandler(
            show_top_students,
            pattern="^top_period_"
        )
    )



    # حذف دانش آموز

    app.add_handler(
        CallbackQueryHandler(
            delete_user_confirm,
            pattern="^delete_user_"
        )
    )


    app.add_handler(
        CallbackQueryHandler(
            delete_user_final,
            pattern="^confirm_delete_"
        )
    )



    # آمار کلی

    app.add_handler(
        CallbackQueryHandler(
            admin_general_stats,
            pattern="^admin_general_stats$"
        )
    )



    # لیست دانش آموزان متنی

    app.add_handler(
        CallbackQueryHandler(
            admin_excel,
            pattern="^admin_excel$"
        )
    )
    # ==========================
    # پیام گروهی
    # ==========================

    app.add_handler(
        CallbackQueryHandler(
            admin_broadcast_menu,
            pattern="^admin_broadcast$"
        )
    )


    app.add_handler(
        CallbackQueryHandler(
            broadcast_filter,
            pattern="^broadcast_filter$"
        )
    )


    app.add_handler(
        CallbackQueryHandler(
            broadcast_field,
            pattern="^broadcast_field$"
        )
    )


    app.add_handler(
        CallbackQueryHandler(
            broadcast_grade,
            pattern="^broadcast_grade$"
        )
    )


    app.add_handler(
        CallbackQueryHandler(
            broadcast_field_grade,
            pattern="^msg_field_(?!grade_)"
        )
    )


    app.add_handler(
        CallbackQueryHandler(
            admin_start_broadcast,
            pattern="^(broadcast_all|msg_field_grade_|msg_grade_)"
        )
    )



    # ==========================
    # بازگشت منو
    # ==========================

    app.add_handler(
        CallbackQueryHandler(
            back_to_menu,
            pattern="^back_to_menu$"
        )
    )



    keep_alive()


    print(
        "BOT RUNNING..."
    )



    app.run_polling()



if __name__ == "__main__":

    main()
