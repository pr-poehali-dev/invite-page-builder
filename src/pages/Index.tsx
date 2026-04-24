import { useState } from "react";
import Icon from "@/components/ui/icon";

const PPTX_URL = "https://functions.poehali.dev/027a6281-9bd8-45bf-a68a-f0f5bccd65da";

const Index = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleDownload = async () => {
    setLoading(true);
    setError("");
    try {
      const res = await fetch(PPTX_URL);
      if (!res.ok) throw new Error("Ошибка генерации");
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
      a.download = json.filename;
      a.click();
      URL.revokeObjectURL(url);
    } catch {
      setError("Не удалось сгенерировать файл. Попробуйте ещё раз.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div
      className="min-h-screen flex flex-col items-center justify-center"
      style={{
        background: "radial-gradient(ellipse at center, #0a1045 0%, #03072A 60%, #000510 100%)",
      }}
    >
      {/* Stars decoration */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        {Array.from({ length: 60 }).map((_, i) => (
          <div
            key={i}
            className="absolute rounded-full bg-white"
            style={{
              width: Math.random() * 2.5 + 0.5 + "px",
              height: Math.random() * 2.5 + 0.5 + "px",
              top: Math.random() * 100 + "%",
              left: Math.random() * 100 + "%",
              opacity: Math.random() * 0.7 + 0.2,
            }}
          />
        ))}
      </div>

      <div className="relative z-10 flex flex-col items-center gap-8 px-6 text-center max-w-xl">
        {/* Spiral logo */}
        <img
          src="https://cdn.poehali.dev/projects/a853d61a-73f8-407d-846b-967c4543637c/bucket/4083467d-4f30-4338-bbe4-204644e9c2bf.png"
          alt="Спираль"
          className="w-28 h-28 drop-shadow-lg"
        />

        <div>
          <h1 className="text-4xl md:text-5xl font-bold tracking-wide mb-3"
            style={{ color: "#FFD700", textShadow: "0 0 30px rgba(255,215,0,0.4)" }}>
            КВАНТОВАЯ ПЕДАГОГИКА
          </h1>
          <p className="text-lg" style={{ color: "#ADD8E6" }}>
            Центр квантовой педагогики и психологии «Фуллерен»
          </p>
        </div>

        <p className="text-white/70 text-base">
          Скачайте презентацию в формате PowerPoint (.pptx) — 5 слайдов в космическом стиле
        </p>

        <button
          onClick={handleDownload}
          disabled={loading}
          className="flex items-center gap-3 px-8 py-4 rounded-2xl text-lg font-semibold transition-all duration-200 disabled:opacity-60 disabled:cursor-not-allowed"
          style={{
            background: loading
              ? "rgba(255,215,0,0.3)"
              : "linear-gradient(135deg, #FFD700 0%, #FFA500 100%)",
            color: "#03072A",
            boxShadow: loading ? "none" : "0 0 30px rgba(255,215,0,0.4)",
          }}
        >
          {loading ? (
            <>
              <Icon name="Loader2" size={22} className="animate-spin" />
              Генерируем презентацию...
            </>
          ) : (
            <>
              <Icon name="Download" size={22} />
              Скачать презентацию (.pptx)
            </>
          )}
        </button>

        {error && (
          <p className="text-red-400 text-sm">{error}</p>
        )}

        <p className="text-white/30 text-xs">
          ✦ Файл генерируется автоматически, это может занять 10–30 секунд ✦
        </p>
      </div>
    </div>
  );
};

export default Index;
