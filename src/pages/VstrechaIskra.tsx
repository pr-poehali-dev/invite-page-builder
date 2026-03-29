import Icon from '@/components/ui/icon';

const heroBg = "https://cdn.poehali.dev/projects/a853d61a-73f8-407d-846b-967c4543637c/files/94f492aa-2b1c-4c56-8c68-51fcc7156018.jpg";
const speakerPhoto = "https://cdn.poehali.dev/projects/4d42a0ab-9035-47df-ab8c-33a5c4f90991/bucket/b6eaa3b7-790c-430c-a9b2-616513e17db5.jpg";

export default function VstrechaIskra() {
  return (
    <div className="iskra-page">

      {/* HERO */}
      <section className="iskra-hero" style={{ backgroundImage: `url(${heroBg})` }}>
        <div className="iskra-hero-overlay" />
        <div className="iskra-hero-content">
          <div className="iskra-badge">⚛ Центр квантовой педагогики и психологии</div>
          <h1 className="iskra-center-name">
            <span className="iskra-fullerene">⬡</span> Фуллерен
          </h1>
          <div className="iskra-divider" />
          <p className="iskra-invite-label">приглашает вас на</p>
          <h2 className="iskra-event-title">ИскРа</h2>
          <p className="iskra-event-subtitle">Женская встреча</p>
          <div className="iskra-event-details">
            <div className="iskra-detail-item">
              <Icon name="Calendar" size={20} />
              <span>4 апреля в 12:00</span>
            </div>
            <div className="iskra-detail-item">
              <Icon name="MapPin" size={20} />
              <span>Комсомольская Набережная, 22</span>
            </div>
          </div>
        </div>
      </section>

      {/* QUOTE */}
      <section className="iskra-quote-section">
        <div className="iskra-container">
          <blockquote className="iskra-quote">
            <span className="iskra-quote-mark">"</span>
            Женщина не хранительница семейного очага,<br />
            она сама очаг
            <span className="iskra-quote-mark">"</span>
          </blockquote>
        </div>
      </section>

      {/* О ЧЁМ ВСТРЕЧА */}
      <section className="iskra-topics-section">
        <div className="iskra-container">
          <h3 className="iskra-section-title">О чём мы будем говорить</h3>
          <div className="iskra-topics-grid">

            <div className="iskra-topic-card iskra-topic-no">
              <div className="iskra-topic-icon">✗</div>
              <h4 className="iskra-topic-heading">Не будем говорить о том</h4>
              <p className="iskra-topic-text">
                «Где женщина должна искать ресурс, что она должна делать»
              </p>
            </div>

            <div className="iskra-topic-card iskra-topic-yes">
              <div className="iskra-topic-icon">✦</div>
              <h4 className="iskra-topic-heading">Поговорим о том</h4>
              <p className="iskra-topic-text">
                «Что женщина <em>не должна делать</em>, чтобы сохранять себя и приумножать»
              </p>
            </div>

          </div>
        </div>
      </section>

      {/* СПИКЕР */}
      <section className="iskra-speaker-section">
        <div className="iskra-container">
          <h3 className="iskra-section-title">Спикер встречи</h3>
          <div className="iskra-speaker-card">
            <div className="iskra-speaker-photo-wrap">
              <img
                src={speakerPhoto}
                alt="Ефремова Мария Викторовна"
                className="iskra-speaker-photo"
              />
              <div className="iskra-speaker-photo-glow" />
            </div>
            <div className="iskra-speaker-info">
              <h4 className="iskra-speaker-name">Ефремова<br />Мария Викторовна</h4>
              <ul className="iskra-speaker-list">
                <li><span className="iskra-li-dot">✦</span> Многодетная мама</li>
                <li><span className="iskra-li-dot">✦</span> Специалист квантовой психологии и педагогики</li>
                <li><span className="iskra-li-dot">✦</span> Основатель Центра «Вдохновение»</li>
                <li><span className="iskra-li-dot">✦</span> Соавтор курса «ИскРа» для женщин</li>
                <li><span className="iskra-li-dot">✦</span> Просто счастливая женщина</li>
              </ul>
            </div>
          </div>
        </div>
      </section>

      {/* КНОПКИ */}
      <section className="iskra-cta-section">
        <div className="iskra-container">
          <h3 className="iskra-section-title">Присоединяйтесь</h3>
          <div className="iskra-buttons-grid">

            <a
              href="https://t.me/spark_true"
              target="_blank"
              rel="noopener noreferrer"
              className="iskra-btn iskra-btn-primary"
            >
              <Icon name="Send" size={20} />
              Присоединиться к сообществу в ТГ
            </a>

            <a
              href="https://dzen.ru/spaceark"
              target="_blank"
              rel="noopener noreferrer"
              className="iskra-btn iskra-btn-secondary"
            >
              <Icon name="BookOpen" size={20} />
              Канал на Дзен
            </a>

            <a
              href="https://wa.me/79270721673"
              target="_blank"
              rel="noopener noreferrer"
              className="iskra-btn iskra-btn-secondary"
            >
              <Icon name="MessageCircle" size={20} />
              Связаться с организатором в WhatsApp
            </a>

            <a
              href="https://www.fullerenclub.ru"
              target="_blank"
              rel="noopener noreferrer"
              className="iskra-btn iskra-btn-outline"
            >
              <Icon name="Globe" size={20} />
              Перейти на сайт
            </a>

          </div>
        </div>
      </section>

      {/* FOOTER */}
      <footer className="iskra-footer">
        <span>⬡ Центр «Фуллерен» · 2025</span>
      </footer>

    </div>
  );
}
