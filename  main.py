import streamlit as st
from chatbot import get_conversation_chain

st.set_page_config(
    page_title="مساعد لوائح الكلية الذكي", page_icon="🎓", layout="centered"
)

st.title("🎓 نظام الـ AI للإجابة عن لوائح وإرشادات الكلية")
st.write(
    "اطرح أي سؤال بخصوص اللائحة الدراسية أو دليل الطالب وسيتم الرد عليك"
    " مباشرة بناءً على المستندات المعتمدة."
)

# تهيئة سلسلة المحادثة وحفظها في الـ Session State
if "conversation" not in st.session_state:
  with st.spinner("جاري تحميل ومعالجة مستندات الكلية..."):
    st.session_state.conversation = get_conversation_chain()

if "chat_history" not in st.session_state:
  st.session_state.chat_history = []

# استقبال سؤال المستخدم
user_query = st.text_input("اكتب سؤالك هنا:")

if user_query:
  with st.spinner("جاري البحث في اللوائح وصياغة الإجابة..."):
    response = st.session_state.conversation({"question": user_query})
    st.session_state.chat_history = response["chat_history"]

# عرض سجل المحادثة
if st.session_state.chat_history:
  for i, message in enumerate(st.session_state.chat_history):
    if i % 2 == 0:
      st.markdown(f"**👤 أنت:** {message.content}")
    else:
      st.markdown(f"**🤖 المساعد الذكي:** {message.content}")
