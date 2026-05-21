import streamlit as st
from supabase import create_client
from streamlit_autorefresh import st_autorefresh
import hashlib
from datetime import datetime, timedelta

# -------------------------
# SUPABASE
# -------------------------
SUPABASE_URL = "https://zfipvfodgngjfuukmeym.supabase.co"
SUPABASE_KEY = "sb_publishable_VVMaElC6qJpstOsTnCr63Q_WPcK5TAK"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# -------------------------
# CONFIG
# -------------------------
st.set_page_config(page_title="Rooms", layout="wide")

st_autorefresh(interval=5000, key="reload")

# -------------------------
# LOGIN PERSISTENTE
# -------------------------
if "user" not in st.session_state:
    st.session_state.user = None

if "room" not in st.session_state:
    st.session_state.room = None

if st.session_state.user is None:
    st.title("Entrar nas Salas")

    user = st.text_input("Seu nome")

    if st.button("Entrar"):
        if user:
            st.session_state.user = user
            st.rerun()

    st.stop()

user = st.session_state.user

# -------------------------
# COR POR USUÁRIO
# -------------------------
def get_color(name):
    colors = ["#FF4B4B", "#4B7BFF", "#4BFF88", "#FFB84B", "#B84BFF"]
    index = int(hashlib.md5(name.encode()).hexdigest(), 16)
    return colors[index % len(colors)]

# -------------------------
# PRESENÇA (ONLINE)
# -------------------------
def update_presence(room_id, user_name):
    supabase.table("presence").upsert({
        "room_id": room_id,
        "user_name": user_name,
        "last_seen": datetime.utcnow().isoformat()
    }).execute()

def get_presence(room_id):
    data = supabase.table("presence") \
        .select("*") \
        .eq("room_id", room_id) \
        .execute().data

    now = datetime.utcnow()
    online_limit = now - timedelta(seconds=10)

    online = 0

    for u in data:
        if u.get("last_seen"):
            try:
                last = datetime.fromisoformat(u["last_seen"].replace("Z", ""))
                if last > online_limit:
                    online += 1
            except:
                pass

    return len(data), online

# -------------------------
# SIDEBAR
# -------------------------
st.sidebar.title("Salas")

room_name = st.sidebar.text_input("Nova sala")

if st.sidebar.button("Criar sala"):
    if room_name:
        supabase.table("rooms").insert({
            "name": room_name,
            "type": "public",
            "password": None,
            "created_by": user
        }).execute()

st.sidebar.divider()

# -------------------------
# LISTA DE SALAS
# -------------------------
if st.session_state.room is None:
    st.title("Salas disponíveis")

    rooms = supabase.table("rooms").select("*").execute().data

    for r in rooms:
        if st.button(f"Entrar em {r['name']}", key=r["id"]):
            st.session_state.room = r
            st.rerun()

    st.stop()

# -------------------------
# SALA
# -------------------------
room = st.session_state.room

update_presence(room["id"], user)
def update_presence(room_id, user_name):
    supabase.table("presence").upsert({
        "room_id": room_id,
        "user_name": user_name,
        "last_seen": datetime.utcnow().isoformat()
    }, on_conflict="room_id,user_name").execute()

total_users, online_users = get_presence(room["id"])

st.title(room["name"])
st.caption(f"👥 {total_users} usuários • 🟢 {online_users} online")

# -------------------------
# MENSAGENS
# -------------------------
messages = supabase.table("messages") \
    .select("*") \
    .eq("room_id", room["id"]) \
    .order("created_at") \
    .execute().data

for m in messages:
    color = get_color(m["user_name"])

    st.markdown(
        f"<span style='color:{color}; font-weight:bold'>{m['user_name']}</span>: {m['text']}",
        unsafe_allow_html=True
    )

# -------------------------
# ENVIAR MENSAGEM
# -------------------------
msg = st.text_input("Mensagem")

if st.button("Enviar"):
    if msg:
        supabase.table("messages").insert({
            "room_id": room["id"],
            "user_name": user,
            "text": msg
        }).execute()

        st.rerun()

# -------------------------
# SAIR
# -------------------------
if st.button("Sair da sala"):
    st.session_state.room = None
    st.rerun()
