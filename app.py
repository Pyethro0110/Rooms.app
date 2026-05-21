import streamlit as st
import hashlib

st.set_page_config(page_title="Rooms", layout="wide")

# -------------------------
# ESTADO
# -------------------------
if "user" not in st.session_state:
    st.session_state.user = None

if "room" not in st.session_state:
    st.session_state.room = None

if "rooms" not in st.session_state:
    st.session_state.rooms = {}

if "messages" not in st.session_state:
    st.session_state.messages = {}

# -------------------------
# CORES POR USUÁRIO
# -------------------------
def user_color(name):
    colors = [
        "#00d4ff", "#ff4d6d", "#7c4dff",
        "#00ffa3", "#ffb703", "#4cc9f0"
    ]
    h = int(hashlib.md5(name.encode()).hexdigest(), 16)
    return colors[h % len(colors)]

# -------------------------
# LOGIN
# -------------------------
if st.session_state.user is None:
    st.title("Rooms")

    user = st.text_input("Username")

    if st.button("Enter"):
        if user.strip():
            st.session_state.user = user
            st.rerun()

# -------------------------
# APP
# -------------------------
else:
    user = st.session_state.user

    st.sidebar.title("Rooms")

    # criar sala
    room_name = st.sidebar.text_input("Room name")
    room_type = st.sidebar.selectbox("Type", ["Public", "Private"])
    password = st.sidebar.text_input("Password (private only)", type="password")
    invite_user = st.sidebar.text_input("Invite user (optional)")

    if st.sidebar.button("Create room"):
        if room_name:
            st.session_state.rooms[room_name] = {
                "type": room_type,
                "password": password if room_type == "Private" else None,
                "allowed": {user, invite_user} if invite_user else {user}
            }
            st.session_state.messages[room_name] = []

    st.sidebar.divider()

    # listar salas
    for room, data in st.session_state.rooms.items():
        label = f"{room} ({data['type']})"

        if st.sidebar.button(label):
            st.session_state.room = room

    # -------------------------
    # SALA
    # -------------------------
    if st.session_state.room is None:
        st.title("Select a room")

    else:
        room = st.session_state.room
        data = st.session_state.rooms[room]

        st.title(room)

        # verificação privada
        if data["type"] == "Private":
            pass_input = st.text_input("Password")

            if pass_input != data["password"]:
                st.warning("Wrong password")
                st.stop()

            if user not in data["allowed"]:
                st.warning("You are not invited")
                st.stop()

        st.divider()

        # mensagens
        for msg in st.session_state.messages[room]:
            color = user_color(msg["user"])

            st.markdown(
                f"""
                <div style="margin-bottom:10px;">
                    <span style="color:{color}; font-weight:600;">
                        {msg['user']}
                    </span>
                    <div style="color:#cfcfcf; margin-left:6px;">
                        {msg['text']}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        st.divider()

        # enviar mensagem
        text = st.text_input("Message")

        if st.button("Send"):
            if text.strip():
                st.session_state.messages[room].append({
                    "user": user,
                    "text": text
                })
                st.rerun()

        if st.button("Leave"):
            st.session_state.room = None
            st.rerun()
