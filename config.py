import os

# مسارات المجلدات والملفات
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
REGULATIONS_DIR = os.path.join(BASE_DIR, "regulations")
DB_DIR = os.path.join(BASE_DIR, "database", "college_ai.db")

# مفتاح نموذج الذكاء الاصطناعي (يمكن وضعه هنا أو عبر متغيرات البيئة)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "your-openai-api-key-here")
