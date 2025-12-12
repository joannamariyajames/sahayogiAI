import React, { useState, useRef } from "react";

const VoiceAssistant = () => {
  const [listening, setListening] = useState(false);
  const [transcript, setTranscript] = useState("");
  const [parsed, setParsed] = useState(null);

  const mediaRecorderRef = useRef(null);
  const audioChunksRef = useRef([]);

  const startListening = async () => {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });

    mediaRecorderRef.current = new MediaRecorder(stream, {
      mimeType: "audio/webm"
    });

    mediaRecorderRef.current.ondataavailable = (event) => {
      audioChunksRef.current.push(event.data);
    };

    mediaRecorderRef.current.onstop = async () => {
      const audioBlob = new Blob(audioChunksRef.current, { type: "audio/webm" });
      audioChunksRef.current = [];

      await sendToBackend(audioBlob);
    };

    mediaRecorderRef.current.start(1000); // collect 1 sec chunks (continuous)
    setListening(true);
  };

  const stopListening = () => {
    if (mediaRecorderRef.current) {
      mediaRecorderRef.current.stop();
      setListening(false);
    }
  };

  const sendToBackend = async (audioBlob) => {
    const formData = new FormData();
    formData.append("file", audioBlob, "audio.webm");
    formData.append("user_id", "test-user");

    const response = await fetch("http://127.0.0.1:8000/voice-command", {
      method: "POST",
      body: formData,
    });

    const data = await response.json();
    
    setTranscript(data.transcript || "");
    setParsed(data.parsed || null);
  };

  return (
    <div style={{ padding: "20px" }}>
      <h2>🎤 Continuous Voice Assistant</h2>

      {listening ? (
        <button
          onClick={stopListening}
          style={{ background: "red", padding: "10px 20px", color: "white" }}
        >
          🛑 Stop Listening
        </button>
      ) : (
        <button
          onClick={startListening}
          style={{ background: "green", padding: "10px 20px", color: "white" }}
        >
          🎙️ Start Listening
        </button>
      )}

      <h3>📝 Live Transcript:</h3>
      <div style={{ padding: "10px", background: "#f4f4f4" }}>{transcript}</div>

      {parsed && (
        <>
          <h3>📦 Parsed Command:</h3>
          <pre style={{ background: "#eee", padding: "10px" }}>
            {JSON.stringify(parsed, null, 2)}
          </pre>
        </>
      )}
    </div>
  );
};

export default VoiceAssistant;