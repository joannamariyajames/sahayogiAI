import React, { useState, useRef } from "react";

function VoiceRecorder() {
  const [recording, setRecording] = useState(false);
  const [audioURL, setAudioURL] = useState(null);
  const [response, setResponse] = useState(null);

  const mediaRecorderRef = useRef(null);
  const audioChunks = useRef([]);

  const startRecording = async () => {
    const stream = await navigator.mediaDevices.getUserMedia({
      audio: {
        echoCancellation: true,
        noiseSuppression: true,
        autoGainControl: true,
      },
    });

    mediaRecorderRef.current = new MediaRecorder(stream, {
      mimeType: "audio/webm",
    });

    audioChunks.current = [];

    mediaRecorderRef.current.ondataavailable = (e) => {
      if (e.data.size > 0) {
        audioChunks.current.push(e.data);
      }
    };

    mediaRecorderRef.current.onstop = handleStop;

    mediaRecorderRef.current.start();
    setRecording(true);
  };

  const stopRecording = () => {
    mediaRecorderRef.current.stop();
    setRecording(false);
  };

  const handleStop = async () => {
    const audioBlob = new Blob(audioChunks.current, {
      type: "audio/webm",
    });

    console.log("Audio blob size:", audioBlob.size);

    const url = URL.createObjectURL(audioBlob);
    setAudioURL(url);

    const formData = new FormData();
    formData.append("file", audioBlob, "voice.webm");
    formData.append("user_id", "demo-user");

    const res = await fetch("http://127.0.0.1:8000/voice-command", {
      method: "POST",
      body: formData,
    });

    const json = await res.json();
    setResponse(json);
  };

  return (
    <div>
      <h2>🎤 Voice Recorder</h2>

      {!recording ? (
        <button onClick={startRecording}>Start Recording</button>
      ) : (
        <button onClick={stopRecording}>Stop Recording</button>
      )}

      {audioURL && (
        <div>
          <h3>Playback:</h3>
          <audio controls src={audioURL}></audio>
        </div>
      )}

      {response && (
        <pre>{JSON.stringify(response, null, 2)}</pre>
      )}
    </div>
  );
}

export default VoiceRecorder;