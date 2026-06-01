import { useState } from "react";

const SATURN_URL = "https://functions.poehali.dev/d7442537-9494-4d2f-a3dc-1f8bdc5a4920";
const DWARFS_URL = "https://functions.poehali.dev/edc08e15-d80c-46c3-8b08-1a3ee7dcc455";

interface Presentation {
  id: string;
  title: string;
  subtitle: string;
  topic: string;
  slides: string;
  url: string;
  filename: string;
  accent: string;
  bg: string;
  border: string;
  badge: string;
  badgeBg: string;
  icon: string;
}

const presentations: Presentation[] = [
  {
    id: "saturn",
    title: "Сатурн: кольца, их состав и происхождение",
    subtitle: "Солнечная система",
    topic: "Астрономия",
    slides: "12 слайдов",
    url: SATURN_URL,
    filename: "saturn_rings.pptx",
    accent: "#D4A917",
    bg: "linear-gradient(135deg, #0D1B3E 0%, #1A316B 100%)",
    border: "#D4A917",
    badge: "#D4A917",
    badgeBg: "rgba(212,169,23,0.12)",
    icon: "🪐",
  },
  {
    id: "dwarfs",
    title: "Белые карлики: конец пути обычных звёзд",
    subtitle: "Строение Вселенной",
    topic: "Астрономия",
    slides: "12 слайдов",
    url: DWARFS_URL,
    filename: "white_dwarfs.pptx",
    accent: "#4DD0E1",
    bg: "linear-gradient(135deg, #0E072A 0%, #1E0F4A 100%)",
    border: "#4DD0E1",
    badge: "#4DD0E1",
    badgeBg: "rgba(77,208,225,0.12)",
    icon: "⭐",
  },
];

function DownloadCard({ pres }: { pres: Presentation }) {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [done, setDone] = useState(false);

  async function handleDownload() {
    setLoading(true);
    setError("");
    setDone(false);
    try {
      const res = await fetch(pres.url);
      if (!res.ok) throw new Error("Ошибка сервера");
      const json = await res.json();
      const binary = atob(json.data);
      const bytes = new Uint8Array(binary.length);
      for (let i = 0; i < binary.length; i++) bytes[i] = binary.charCodeAt(i);
      const blob = new Blob([bytes], {
        type: "application/vnd.openxmlformats-officedocument.presentationml.presentation",
      });
      const a = document.createElement("a");
      a.href = URL.createObjectURL(blob);
      a.download = pres.filename;
      a.click();
      URL.revokeObjectURL(a.href);
      setDone(true);
      setTimeout(() => setDone(false), 4000);
    } catch {
      setError("Не удалось сгенерировать файл. Попробуй ещё раз.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div
      style={{
        background: pres.bg,
        border: `1.5px solid ${pres.border}`,
        borderRadius: 20,
        padding: "36px 36px 32px",
        maxWidth: 520,
        width: "100%",
        boxShadow: `0 8px 40px rgba(0,0,0,0.45), 0 0 0 1px ${pres.border}22`,
        display: "flex",
        flexDirection: "column",
        gap: 20,
        position: "relative",
        overflow: "hidden",
      }}
    >
      {/* Звёздный фон — декор */}
      <div style={{
        position: "absolute", inset: 0, pointerEvents: "none",
        background: "radial-gradient(ellipse at 80% 20%, rgba(255,255,255,0.04) 0%, transparent 60%)",
      }} />

      {/* Иконка + бейджи */}
      <div style={{ display: "flex", alignItems: "flex-start", gap: 16 }}>
        <div style={{
          fontSize: 52, lineHeight: 1,
          filter: "drop-shadow(0 2px 8px rgba(0,0,0,0.5))",
        }}>
          {pres.icon}
        </div>
        <div style={{ display: "flex", flexDirection: "column", gap: 6 }}>
          <span style={{
            background: pres.badgeBg,
            border: `1px solid ${pres.badge}55`,
            color: pres.badge,
            borderRadius: 8,
            padding: "3px 12px",
            fontSize: 12,
            fontWeight: 600,
            letterSpacing: "0.07em",
            textTransform: "uppercase",
            width: "fit-content",
          }}>
            {pres.subtitle}
          </span>
          <span style={{
            background: "rgba(255,255,255,0.06)",
            border: "1px solid rgba(255,255,255,0.12)",
            color: "rgba(255,255,255,0.55)",
            borderRadius: 8,
            padding: "3px 12px",
            fontSize: 12,
            width: "fit-content",
          }}>
            {pres.slides}
          </span>
        </div>
      </div>

      {/* Заголовок */}
      <div>
        <div style={{
          color: pres.accent,
          fontSize: 11,
          fontWeight: 700,
          letterSpacing: "0.12em",
          textTransform: "uppercase",
          marginBottom: 8,
          opacity: 0.8,
        }}>
          {pres.topic}
        </div>
        <h2 style={{
          color: "#fff",
          fontSize: 22,
          fontWeight: 700,
          lineHeight: 1.35,
          margin: 0,
          fontFamily: "Georgia, serif",
        }}>
          {pres.title}
        </h2>
      </div>

      {/* Состав */}
      <div style={{
        background: "rgba(255,255,255,0.04)",
        borderRadius: 12,
        padding: "14px 16px",
        display: "flex",
        flexDirection: "column",
        gap: 7,
      }}>
        {[
          "Титульный слайд с Ф.И. студента и группой",
          "Актуальность, цель и гипотеза исследования",
          "7 содержательных слайдов по теме",
          "Вывод: 5 ограничений + 5 реальных возможностей",
          "Приложение: 7 контрольных вопросов",
        ].map((item, i) => (
          <div key={i} style={{ display: "flex", alignItems: "flex-start", gap: 10 }}>
            <span style={{ color: pres.accent, fontSize: 14, marginTop: 1, flexShrink: 0 }}>✓</span>
            <span style={{ color: "rgba(255,255,255,0.65)", fontSize: 14, lineHeight: 1.4 }}>{item}</span>
          </div>
        ))}
      </div>

      {/* Кнопка */}
      <button
        onClick={handleDownload}
        disabled={loading}
        style={{
          background: done
            ? "linear-gradient(135deg, #2E7D32, #43A047)"
            : `linear-gradient(135deg, ${pres.accent}, ${pres.accent}cc)`,
          color: done ? "#fff" : "#0D1B3E",
          border: "none",
          borderRadius: 12,
          padding: "14px 24px",
          fontSize: 16,
          fontWeight: 700,
          cursor: loading ? "not-allowed" : "pointer",
          width: "100%",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          gap: 10,
          transition: "all 0.2s",
          opacity: loading ? 0.7 : 1,
          boxShadow: `0 4px 20px ${pres.accent}44`,
        }}
      >
        {loading ? (
          <>
            <span style={{
              width: 18, height: 18, border: "2.5px solid rgba(13,27,62,0.3)",
              borderTopColor: "#0D1B3E", borderRadius: "50%",
              display: "inline-block", animation: "spin 0.8s linear infinite",
            }} />
            Генерирую PPTX...
          </>
        ) : done ? (
          <>✓ Файл скачан</>
        ) : (
          <>⬇ Скачать презентацию</>
        )}
      </button>

      {error && (
        <div style={{
          color: "#FF8A80", fontSize: 13, textAlign: "center",
          background: "rgba(255,100,100,0.08)", borderRadius: 8, padding: "8px 12px",
        }}>
          {error}
        </div>
      )}
    </div>
  );
}

export default function AstronomyPptx() {
  return (
    <div style={{
      minHeight: "100vh",
      background: "linear-gradient(160deg, #06040F 0%, #0D1B3E 50%, #0E072A 100%)",
      fontFamily: "system-ui, -apple-system, sans-serif",
      padding: "0 16px 60px",
    }}>
      <style>{`
        @keyframes spin { to { transform: rotate(360deg); } }
        @keyframes fadeUp {
          from { opacity: 0; transform: translateY(24px); }
          to   { opacity: 1; transform: translateY(0); }
        }
      `}</style>

      {/* Шапка */}
      <div style={{
        textAlign: "center",
        padding: "60px 16px 48px",
        animation: "fadeUp 0.6s ease both",
      }}>
        <div style={{
          display: "inline-block",
          background: "rgba(77,208,225,0.1)",
          border: "1px solid rgba(77,208,225,0.25)",
          borderRadius: 40,
          padding: "6px 20px",
          color: "#4DD0E1",
          fontSize: 13,
          fontWeight: 600,
          letterSpacing: "0.1em",
          textTransform: "uppercase",
          marginBottom: 20,
        }}>
          Учебные презентации · Астрономия
        </div>
        <h1 style={{
          color: "#fff",
          fontSize: "clamp(28px, 5vw, 46px)",
          fontWeight: 800,
          margin: "0 0 16px",
          fontFamily: "Georgia, serif",
          lineHeight: 1.2,
        }}>
          Исследовательские работы
        </h1>
        <p style={{
          color: "rgba(255,255,255,0.5)",
          fontSize: 18,
          margin: 0,
          maxWidth: 540,
          marginInline: "auto",
          lineHeight: 1.5,
        }}>
          Иванов Иван Иванович · Группа АС-21
        </p>
      </div>

      {/* Карточки */}
      <div style={{
        display: "flex",
        flexWrap: "wrap",
        gap: 32,
        justifyContent: "center",
        maxWidth: 1120,
        marginInline: "auto",
        animation: "fadeUp 0.7s ease 0.1s both",
      }}>
        {presentations.map((p) => (
          <DownloadCard key={p.id} pres={p} />
        ))}
      </div>

      {/* Подпись */}
      <p style={{
        textAlign: "center",
        color: "rgba(255,255,255,0.2)",
        fontSize: 13,
        marginTop: 48,
      }}>
        Файлы генерируются в формате .pptx · Microsoft PowerPoint / Google Slides
      </p>
    </div>
  );
}
