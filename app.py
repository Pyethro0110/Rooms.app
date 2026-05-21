import streamlit as st

st.set_page_config(page_title="Rooms", page_icon="🌐")

# estado das salas (simples)
if "room" not in st.session_state:
    st.session_state.room = None

if "messages" not in st.session_state:
    st.session_state.messages = {
        "madrugada": [],
        "musica": [],
        "devs": [],
        "aleatorio": []
    }

ROOMS = {
    "madrugada": "🌙 madrugada",
    "musica": "🎧 manda música",
    "devs": "💻 devs online",
    "aleatorio": "😂 aleatório"
}

# -------------------------
# TELA 1: SALAS
# -------------------------
if st.session_state.room is None:

    st.title("🌐 Rooms")
    st.write("Entre em uma sala e converse")

    for room_id, room_name in ROOMS.items():
        if st.button(room_name):
            st.session_state.room = room_id

# -------------------------
# TELA 2: CHAT DA SALA
# -------------------------
else:
    room_id = st.session_state.room

    st.title(ROOMS[room_id])

    if st.button("← voltar"):
        st.session_state.room = None

    st.divider()

    # mostrar mensagens
    for msg in st.session_state.messages[room_id]:
        st.write(f"**{msg['user']}**: {msg['text']}")

    st.divider()

    # input de mensagem
    user_msg = st.text_input("Digite uma mensagem")

    if st.button("enviar"):
        if user_msg.strip():
            st.session_state.messages[room_id].append({
                "user": "Você",
                "text": user_msg
            })
            st.rerun()
