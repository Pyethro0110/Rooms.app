import streamlit as st

st.set_page_config(page_title="Rooms", page_icon="R", layout="wide")

# -------------------------
# ESTADO
# -------------------------
if "user" not in st.session_state:
    st.session_state.user = None

if "room" not in st.session_state:
    st.session_state.room = None

if "rooms" not in st.session_state:
    st.session_state.rooms = {
        "madrugada": [],
        "music": [],
        "devs": []
    }

if "online" not in st.session_state:
    st.session_state.online = set()

# -------------------------
# CSS FUTURISTA
# -------------------------
st.markdown("""
<style>
body {
    background-color: #0b0f1a;
    color: #e6e6e6;
}

.stApp {
    background-color: #0b0f1a;
}

h1, h2, h3 {
    color: #ffffff;
    font-weight: 500;
}

div[data-testid="stSidebar"] {
    background-color: #0f1424;
    border-right: 1px solid #1f2a44;
}

button {
    background-color: #121a2b !important;
    color: #d6d6d6 !important;
    border: 1px solid #1f2a44 !important;
    border-radius: 8px !important;
}

button:hover {
    border: 1px solid #00d4ff !important;
    color: #00d4ff !important;
}

input {
    background-color: #0f1424 !important;
    color: white !important;
    border: 1px solid #1f2a44 !important;
}
</style>
""", unsafe_allow_html=True)

# -------------------------
# LOGIN
# -------------------------
if st.session_state.user is None:
    st.title("Rooms")

    user = st.text_input("Username")

    if st.button("Enter"):
        if user.strip():
            st.session_state.user = user
            st.session_state.online.add(user)
            st.rerun()

# -------------------------
# APP
# -------------------------
else:
    user = st.session_state.user

    # SIDEBAR
    st.sidebar.title("Rooms")

    new_room = st.sidebar.text_input("Create room")

    if st.sidebar.button("Create"):
        if new_room and new_room not in st.session_state.rooms:
            st.session_state.rooms[new_room] = []

    st.sidebar.divider()

    for room in st.session_state.rooms.keys():
        if st.sidebar.button(room):
            st.session_state.room = room

    st.sidebar.divider()
    st.sidebar.write("Online")
    st.sidebar.write(list(st.session_state.online))

    # -------------------------
    # ROOM VIEW
    # -------------------------
    if st.session_state.room is None:
        st.title("Select a room")

    else:
        room = st.session_state.room

        st.title(room)

        st.divider()

        for msg in st.session_state.rooms[room]:
            st.markdown(f"**{msg['user']}**  \n{msg['text']}")

        st.divider()

        msg = st.text_input("Message")

        if st.button("Send"):
            if msg.strip():
                st.session_state.rooms[room].append({
                    "user": user,
                    "text": msg
                })
                st.rerun()

        if st.button("Leave"):
            st.session_state.room = None
            st.rerun()
