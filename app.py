import streamlit as st
from supabase import create_client

SUPABASE_URL = "https://zfipvfodgngjfuukmeym.supabase.co"

SUPABASE_KEY = "sb_publishable_VVMaElC6qJpstOsTnCr63Q_WPcK5TAK"

supabase = create_client("https://zfipvfodgngjfuukmeym.supabase.co", "sb_publishable_VVMaElC6qJpstOsTnCr63Q_WPcK5TAK")

st.set_page_config(page_title="Rooms", layout="wide")

# -------------------------
# LOGIN SIMPLES
# -------------------------
if "user" not in st.session_state:
    st.session_state.user = None

if "room" not in st.session_state:
    st.session_state.room = None

if st.session_state.user is None:
    st.title("Rooms")

    user = st.text_input("Username")

    if st.button("Enter"):
        if user:
            st.session_state.user = user
            st.rerun()

# -------------------------
# APP
# -------------------------
else:
    user = st.session_state.user

    st.sidebar.title("Rooms")

    # criar sala
    room_name = st.sidebar.text_input("New room")

    if st.sidebar.button("Create"):
        if room_name:
            supabase.table("rooms").insert({
                "name": room_name,
                "type": "public",
                "password": None,
                "created_by": user
            }).execute()

    st.sidebar.divider()

    # listar salas (CATÁLOGO REAL)
    rooms = supabase.table("rooms").select("*").execute().data

    for r in rooms:
        if st.sidebar.button(r["name"]):
            st.session_state.room = r

    # -------------------------
    # SALA
    # -------------------------
    if st.session_state.room is None:
        st.title("Select a room")

    else:
        room = st.session_state.room

        st.title(room["name"])

        # mensagens
        messages = supabase.table("messages") \
            .select("*") \
            .eq("room_id", room["id"]) \
            .order("created_at") \
            .execute().data

        for m in messages:
            st.write(f"**{m['user_name']}**: {m['text']}")

        msg = st.text_input("Message")

        if st.button("Send"):
            if msg:
                supabase.table("messages").insert({
                    "room_id": room["id"],
                    "user_name": user,
                    "text": msg
                }).execute()

                st.rerun()

        if st.button("Leave"):
            st.session_state.room = None
            st.rerun()
