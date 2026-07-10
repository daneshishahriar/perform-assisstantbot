import os
from dotenv import load_dotenv

load_dotenv()


# ==========================
# تنظیمات ربات
# ==========================

BOT_TOKEN = os.getenv(
    "BOT_TOKEN"
)


DATABASE_URL = os.getenv(
    "DATABASE_URL"
)



# ==========================
# مدیریت ربات
# ==========================

ADMIN_ID = 5723306558