import { useState } from "react";
import Icon from "@/components/ui/icon";

const FUNC_URL = "https://functions.poehali.dev/f23c3d8c-f8a6-43d1-86b4-ffe77a9aeb1e";

const peonyImg = "https://cdn.poehali.dev/projects/a853d61a-73f8-407d-846b-967c4543637c/bucket/29d08a49-613a-4d33-8137-21a389ad93de.jpg";

export default function GranitsynPptx() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleDownload = async () => {
    setLoading(true);
    setError("");
    try {
      const res = await fetch(FUNC_URL);
      if (!res.ok) throw new Error("Ошибка сервера");
      const json = await res.json();
      const byteStr = atob(json.data);
      const bytes = new Uint8Array(byteStr.length);
      for (let i = 0; i < byteStr.length; i++) bytes[i] = byteStr.charCodeAt(i);
      const blob = new Blob([bytes], {
        type: "application/vnd.openxmlformats-officedocument.presentationml.presentation",
      });
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = json.filename || "presentation.pptx";
      a.click();
      URL.revokeObjectURL(url);
    } catch (e) {
      setError("Не удалось создать презентацию. Попробуйте ещё раз.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div
      style={{
        minHeight: "100vh",
        background: "#ebebeb",
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        fontFamily: "'Times New Roman', Times, serif",
        padding: "40px 20px",
      }}
    >
      <img
        src={peonyImg}
        alt="Пион"
        style={{
          width: "320px",
          maxWidth: "80vw",
          marginBottom: "40px",
          borderRadius: "8px",
        }}
      />

      <h1
        style={{
          fontSize: "clamp(22px, 4vw, 38px)",
          color: "#1a1714",
          textAlign: "center",
          marginBottom: "12px",
          fontWeight: "normal",
          maxWidth: "600px",
        }}
      >
        Техника экологичного выставления границ
      </h1>

      <p
        style={{
          fontSize: "clamp(14px, 2vw, 18px)",
          color: "#555",
          textAlign: "center",
          marginBottom: "48px",
          fontFamily: "sans-serif",
        }}
      >
        Центр квантовой педагогики и психологии «Фуллерен»
      </p>

      <button
        onClick={handleDownload}
        disabled={loading}
        style={{
          display: "flex",
          alignItems: "center",
          gap: "10px",
          background: loading ? "#aaa" : "#1a1714",
          color: "#ebebeb",
          border: "none",
          borderRadius: "8px",
          padding: "16px 40px",
          fontSize: "18px",
          fontFamily: "'Times New Roman', Times, serif",
          cursor: loading ? "not-allowed" : "pointer",
          transition: "background 0.2s",
        }}
      >
        {loading ? (
          <>
            <Icon name="Loader2" size={22} />
            Генерирую...
          </>
        ) : (
          <>
            <Icon name="Download" size={22} />
            Скачать презентацию .pptx
          </>
        )}
      </button>

      {error && (
        <p style={{ color: "#c0392b", marginTop: "20px", fontFamily: "sans-serif" }}>
          {error}
        </p>
      )}

      {loading && (
        <p style={{ color: "#666", marginTop: "16px", fontFamily: "sans-serif", fontSize: "14px" }}>
          Загружаю изображения и формирую файл — это займёт около 30 секунд...
        </p>
      )}
    </div>
  );
}
