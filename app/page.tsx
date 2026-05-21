"use client";

import { useState } from "react";

type Message = {
  user: string;
  text: string;
};

const ROOMS = [
  { id: "madrugada", name: "🌙 madrugada" },
  { id: "musica", name: "🎧 manda música" },
  { id: "devs", name: "💻 devs online" },
  { id: "aleatorio", name: "😂 aleatório" },
];

export default function Page() {
  const [currentRoom, setCurrentRoom] = useState<string | null>(null);
  const [messages, setMessages] = useState<Record<string, Message[]>>({});
  const [input, setInput] = useState("");

  function sendMessage() {
    if (!currentRoom || !input.trim()) return;

    const newMsg: Message = {
      user: "Você",
      text: input,
    };

    setMessages((prev) => ({
      ...prev,
      [currentRoom]: [...(prev[currentRoom] || []), newMsg],
    }));

    setInput("");
  }

  // 📌 TELA DE SALAS
  if (!currentRoom) {
    return (
      <div style={styles.container}>
        <h1 style={styles.title}>🌐 Rooms</h1>
        <p style={styles.subtitle}>Entre em uma sala e converse em tempo real</p>

        <div style={styles.grid}>
          {ROOMS.map((room) => (
            <button
              key={room.id}
              onClick={() => setCurrentRoom(room.id)}
              style={styles.room}
            >
              {room.name}
            </button>
          ))}
        </div>
      </div>
    );
  }

  // 📌 TELA DA SALA
  const roomMessages = messages[currentRoom] || [];
  const roomName = ROOMS.find((r) => r.id === currentRoom)?.name;

  return (
    <div style={styles.container}>
      <button style={styles.back} onClick={() => setCurrentRoom(null)}>
        ← voltar
      </button>

      <h2 style={styles.title}>{roomName}</h2>

      <div style={styles.chat}>
        {roomMessages.length === 0 && (
          <p style={{ opacity: 0.5 }}>Nenhuma mensagem ainda...</p>
        )}

        {roomMessages.map((msg, i) => (
          <div key={i} style={styles.msg}>
            <strong>{msg.user}: </strong>
            {msg.text}
          </div>
        ))}
      </div>

      <div style={styles.inputBox}>
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Digite uma mensagem..."
          style={styles.input}
        />
        <button onClick={sendMessage} style={styles.button}>
          enviar
        </button>
      </div>
    </div>
  );
}

const styles: Record<string, React.CSSProperties> = {
  container: {
    maxWidth: 700,
    margin: "0 auto",
    padding: 20,
    fontFamily: "Arial",
  },

  title: {
    fontSize: 28,
    marginBottom: 5,
  },

  subtitle: {
    opacity: 0.6,
    marginBottom: 20,
  },

  grid: {
    display: "grid",
    gap: 10,
  },

  room: {
    padding: 16,
    borderRadius: 12,
    border: "1px solid #ddd",
    background: "#f5f5f5",
    cursor: "pointer",
    textAlign: "left",
    fontSize: 16,
  },

  back: {
    marginBottom: 10,
    cursor: "pointer",
    background: "transparent",
    border: "none",
    fontSize: 14,
  },

  chat: {
    height: 350,
    border: "1px solid #ddd",
    borderRadius: 12,
    padding: 12,
    overflowY: "auto",
    marginBottom: 10,
    background: "#fff",
  },

  msg: {
    marginBottom: 8,
  },

  inputBox: {
    display: "flex",
    gap: 10,
  },

  input: {
    flex: 1,
    padding: 12,
    borderRadius: 10,
    border: "1px solid #ccc",
  },

  button: {
    padding: "12px 16px",
    borderRadius: 10,
    border: "none",
    background: "black",
    color: "white",
    cursor: "pointer",
  },
};
