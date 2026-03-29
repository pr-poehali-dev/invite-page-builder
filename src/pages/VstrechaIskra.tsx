import Icon from '@/components/ui/icon';

const heroBg = "https://cdn.poehali.dev/projects/a853d61a-73f8-407d-846b-967c4543637c/bucket/6dabf95d-21cc-4a45-a957-b6d0e8f1a030.jpg";
const speakerPhoto = "https://cdn.poehali.dev/projects/a853d61a-73f8-407d-846b-967c4543637c/bucket/4578094e-a3b0-4edc-ae34-fb4ff7f44768.jpg";
const iskraLogo = "https://cdn.poehali.dev/projects/a853d61a-73f8-407d-846b-967c4543637c/bucket/89cdd506-e3ac-49c2-b8c7-5d38c21a08a2.png";

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
          <p className="iskra-invite-label">приглашает вас на женскую встречу</p>
          <img src={iskraLogo} alt="ИскРа" className="iskra-logo-img" />
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

      <div className="iskra-sep"><span>✦</span></div>

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

      <div className="iskra-sep"><span>✦</span></div>

      {/* О ЧЁМ ВСТРЕЧА */}
      <section className="iskra-topics-section">
        <div className="iskra-container">
          <h3 className="iskra-section-title">О чём мы будем говорить</h3>
          <div className="iskra-topics-grid">

            <div className="iskra-topic-card iskra-topic-no">
              <div className="iskra-topic-icon">✗</div>
              <h4 className="iskra-topic-heading">Не будем говорить о том</h4>
              <p className="iskra-topic-text">
                «Что женщина должна делать»
              </p>
            </div>

            <div className="iskra-topic-card iskra-topic-yes">
              <div className="iskra-topic-icon">✦</div>
              <h4 className="iskra-topic-heading">Поговорим о том</h4>
              <p className="iskra-topic-text">
                «Как женщина может сохранять и приумножать свой ресурс привлекательности»
              </p>
            </div>

          </div>
        </div>
      </section>

      <div className="iskra-sep"><span>✦</span></div>

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
                <li><span className="iskra-li-dot">✦</span> Соавтор и ведущая курса «ИскРа» для женщин</li>
                <li><span className="iskra-li-dot">✦</span> Просто счастливая женщина</li>
              </ul>
            </div>
          </div>
        </div>
      </section>

      <div className="iskra-sep"><span>✦</span></div>

      {/* КНОПКИ */}
      <section className="iskra-cta-section">
        <div className="iskra-container">
          <div className="iskra-buttons-grid">

            <a
              href="https://t.me/spark_true"
              target="_blank"
              rel="noopener noreferrer"
              className="iskra-btn iskra-btn-primary"
            >
              <Icon name="Send" size={20} />
              Сообщество в ТГ
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
              Сайт центра
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