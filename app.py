import streamlit as st
from supabase import create_client
from streamlit_autorefresh import st_autorefresh
import hashlib
from datetime import datetime, timedelta
import uuid

# -------------------------
# SUPABASE
# -------------------------
SUPABASE_URL = "https://zfipvfodgngjfuukmeym.supabase.co"
SUPABASE_KEY = "sb_publishable_VVMaElC6qJpstOsTnCr63Q_WPcK5TAK"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# -------------------------
# CONFIG
# -------------------------
st.set_page_config(page_title="Salas", layout="wide")
st_autorefresh(interval=5000, key="reload")

# -------------------------
# LOGIN
# -------------------------
if "user" not in st.session_state:
    st.session_state.user = None

if "room" not in st.session_state:
    st.session_state.room = None

if st.session_state.user is None:
    st.title("Entrar")

    user = st.text_input("Seu nome")

    if st.button("Entrar"):
        if user:
            st.session_state.user = user
            st.rerun()

    st.stop()

user = st.session_state.user

# -------------------------
# COR DO USUÁRIO
# -------------------------
def get_color(name):
    colors = ["#FF4B4B", "#4B7BFF", "#4BFF88", "#FFB84B", "#B84BFF"]
    return colors[int(hashlib.md5(name.encode()).hexdigest(), 16) % len(colors)]

# -------------------------
# PRESENÇA
# -------------------------
def update_presence(room_id, user_name):
    supabase.table("presence").upsert({
        "room_id": str(room_id),
        "user_name": str(user_name),
        "last_seen": datetime.utcnow().isoformat()
    }).execute()

def get_presence(room_id):
    data = supabase.table("presence") \
        .select("*") \
        .eq("room_id", str(room_id)) \
        .execute().data

    now = datetime.utcnow()
    limit = now - timedelta(seconds=10)

    total = len(data)
    online = 0

    for u in data:
        if u.get("last_seen"):
            try:
                last = datetime.fromisoformat(u["last_seen"].replace("Z", ""))
                if last > limit:
                    online += 1
            except:
                pass

    return total, online

# -------------------------
# ENTRADA POR LINK (NOVO)
# -------------------------
room_code_param = st.query_params.get("room")

if room_code_param and st.session_state.room is None:
    room = supabase.table("rooms") \
        .select("*") \
        .eq("code", room_code_param) \
        .execute().data

    if room:
        st.session_state.room = room[0]

# -------------------------
# SIDEBAR - CRIAR SALA
# -------------------------
st.sidebar.title("Salas")

room_name = st.sidebar.text_input("Nova sala")
room_type = st.sidebar.selectbox("Tipo", ["public", "private"])
room_password = None

if room_type == "private":
    room_password = st.sidebar.text_input("Senha", type="password")

if st.sidebar.button("Criar sala"):
    if room_name:
        room_code = str(uuid.uuid4())[:8]

        supabase.table("rooms").insert({
            "name": room_name,
            "type": room_type,
            "password": room_password,
            "code": room_code,
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
        if st.button(f"Entrar em {r['name']}", key=str(r["id"])):
            st.session_state.room = r
            st.rerun()

    st.stop()

# -------------------------
# SALA
# -------------------------
room = st.session_state.room

update_presence(room["id"], user)

total, online = get_presence(room["id"])

st.title(room["name"])
st.caption(f"👥 {total} usuários • 🟢 {online} online")

# LINK DE CONVITE (NOVO)
st.code(f"?room={room['code']}")

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
if st.button("Sair"):
    st.session_state.room = None
    st.rerun()
