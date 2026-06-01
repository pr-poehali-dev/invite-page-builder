"""
Генерация PPTX-презентации по теме «Сатурн: кольца, их состав и происхождение»
(Солнечная система). 12 слайдов, академический стиль: тёмно-синий / золотой.
Студент: Иванов Иван Иванович, группа АС-21.
"""

import base64
import io
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from PIL import Image, ImageDraw, ImageFont


# ─── Цветовая палитра ────────────────────────────────────────────────────────
DARK_BLUE   = RGBColor(0x0D, 0x1B, 0x3E)   # фон
MID_BLUE    = RGBColor(0x1A, 0x31, 0x6B)   # акцент
GOLD        = RGBColor(0xD4, 0xA9, 0x17)   # золото
LIGHT_GOLD  = RGBColor(0xF0, 0xD0, 0x6A)   # светлое золото
WHITE       = RGBColor(0xFF, 0xFF, 0xFF)
LIGHT_GREY  = RGBColor(0xCC, 0xD6, 0xE8)
RING_BEIGE  = RGBColor(0xC8, 0xB5, 0x7A)


def make_dark_bg(w=1920, h=1080, title_slide=False):
    img = Image.new("RGB", (w, h), (13, 27, 62))
    draw = ImageDraw.Draw(img)
    # Градиент — полосы для объёма
    for i in range(0, h, 4):
        alpha = int(6 * (1 - i / h))
        draw.rectangle([0, i, w, i + 3], fill=(13 + alpha, 27 + alpha, 62 + alpha))
    # Золотая линия сверху
    draw.rectangle([0, 0, w, 6], fill=(212, 169, 23))
    draw.rectangle([0, 6, w, 10], fill=(180, 140, 10))
    # Золотая линия снизу
    draw.rectangle([0, h - 10, w, h - 6], fill=(180, 140, 10))
    draw.rectangle([0, h - 6, w, h], fill=(212, 169, 23))
    if title_slide:
        # Центральная горизонтальная декоративная полоса
        draw.rectangle([80, h // 2 + 60, w - 80, h // 2 + 64], fill=(212, 169, 23))
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return buf


def set_bg(slide, buf, prs):
    buf.seek(0)
    W, H = prs.slide_width, prs.slide_height
    pic = slide.shapes.add_picture(buf, 0, 0, W, H)
    slide.shapes._spTree.remove(pic._element)
    slide.shapes._spTree.insert(2, pic._element)


def txt(slide, text, left, top, width, height,
        size=28, bold=False, color=WHITE,
        align=PP_ALIGN.LEFT, italic=False, wrap=True):
    box = slide.shapes.add_textbox(left, top, width, height)
    tf = box.text_frame
    tf.word_wrap = wrap
    p = tf.paragraphs[0]
    p.alignment = align
    run = p.add_run()
    run.text = text
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.italic = italic
    run.font.color.rgb = color
    run.font.name = "Calibri"
    return box


def multiline(slide, lines, left, top, width, height,
              sizes, bolds, colors, aligns, spaces=None):
    box = slide.shapes.add_textbox(left, top, width, height)
    tf = box.text_frame
    tf.word_wrap = True
    for i, line in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = aligns[i] if i < len(aligns) else PP_ALIGN.LEFT
        if spaces and i < len(spaces) and spaces[i]:
            p.space_before = Pt(spaces[i])
        run = p.add_run()
        run.text = line
        run.font.size = Pt(sizes[i] if i < len(sizes) else 24)
        run.font.bold = bolds[i] if i < len(bolds) else False
        run.font.color.rgb = colors[i] if i < len(colors) else WHITE
        run.font.name = "Calibri"


def bullet_slide(prs, blank, title_text, bullets, bg_buf_fn=None):
    """Стандартный слайд с заголовком и маркированным списком."""
    s = prs.slides.add_slide(blank)
    set_bg(s, (bg_buf_fn or make_dark_bg)(), prs)
    W, H = prs.slide_width, prs.slide_height

    # Золотая полоска под заголовком
    bar = s.shapes.add_shape(1, Inches(0.5), Inches(1.55), Inches(12.33), Pt(3))
    bar.fill.solid()
    bar.fill.fore_color.rgb = GOLD
    bar.line.fill.background()

    txt(s, title_text, Inches(0.5), Inches(0.25), Inches(12.33), Inches(1.2),
        size=34, bold=True, color=GOLD, align=PP_ALIGN.LEFT)

    box = s.shapes.add_textbox(Inches(0.6), Inches(1.75), Inches(12.13), Inches(5.4))
    tf = box.text_frame
    tf.word_wrap = True
    for i, b in enumerate(bullets):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = PP_ALIGN.LEFT
        if i > 0:
            p.space_before = Pt(6)
        run = p.add_run()
        run.text = ("• " if not b.startswith("—") else "") + b
        run.font.size = Pt(22)
        run.font.color.rgb = LIGHT_GREY
        run.font.name = "Calibri"
    return s


def handler(event: dict, context) -> dict:
    """Генерирует PPTX 'Сатурн: кольца, их состав и происхождение' (Солнечная система)"""

    if event.get("httpMethod") == "OPTIONS":
        return {"statusCode": 200, "headers": {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type",
        }, "body": ""}

    prs = Presentation()
    prs.slide_width  = Inches(13.33)
    prs.slide_height = Inches(7.5)
    blank = prs.slide_layouts[6]
    W, H = prs.slide_width, prs.slide_height

    # ── Слайд 1: Титульный ────────────────────────────────────────────────────
    s1 = prs.slides.add_slide(blank)
    set_bg(s1, make_dark_bg(title_slide=True), prs)

    # Надпись сверху — дисциплина
    txt(s1, "АСТРОНОМИЯ  •  Солнечная система",
        Inches(0.5), Inches(0.4), Inches(12.33), Inches(0.6),
        size=18, color=GOLD, align=PP_ALIGN.CENTER, italic=True)

    # Заголовок
    multiline(s1,
        ["Сатурн:", "кольца, их состав", "и происхождение"],
        Inches(0.5), Inches(1.3), Inches(12.33), Inches(3.0),
        [52, 52, 44], [True, True, False],
        [GOLD, WHITE, LIGHT_GOLD],
        [PP_ALIGN.CENTER]*3, [0, 4, 8])

    # Разделитель
    bar = s1.shapes.add_shape(1, Inches(3.5), Inches(4.55), Inches(6.33), Pt(2))
    bar.fill.solid(); bar.fill.fore_color.rgb = GOLD; bar.line.fill.background()

    # Студент
    multiline(s1,
        ["Выполнил: Иванов Иван Иванович", "Группа: АС-21"],
        Inches(0.5), Inches(4.75), Inches(12.33), Inches(1.0),
        [22, 22], [False, False], [LIGHT_GREY, LIGHT_GREY],
        [PP_ALIGN.CENTER]*2, [0, 6])

    txt(s1, "Исследовательская работа",
        Inches(0.5), Inches(5.9), Inches(12.33), Inches(0.5),
        size=16, color=GOLD, align=PP_ALIGN.CENTER, italic=True)

    # ── Слайд 2: Актуальность, цель, гипотеза ────────────────────────────────
    s2 = prs.slides.add_slide(blank)
    set_bg(s2, make_dark_bg(), prs)
    bar2 = s2.shapes.add_shape(1, Inches(0.5), Inches(1.55), Inches(12.33), Pt(3))
    bar2.fill.solid(); bar2.fill.fore_color.rgb = GOLD; bar2.line.fill.background()
    txt(s2, "Введение: цель, актуальность, гипотеза",
        Inches(0.5), Inches(0.25), Inches(12.33), Inches(1.2),
        size=32, bold=True, color=GOLD)

    box2 = s2.shapes.add_textbox(Inches(0.6), Inches(1.75), Inches(12.13), Inches(5.4))
    tf2 = box2.text_frame; tf2.word_wrap = True
    entries = [
        ("АКТУАЛЬНОСТЬ:", GOLD, True,
         "Сатурн — вторая по размеру планета Солнечной системы и единственная, чьи кольца "
         "видны в любительский телескоп. Изучение их состава и происхождения помогает понять "
         "эволюцию планетных систем и возможные механизмы образования подобных структур вокруг других планет."),
        ("ЦЕЛЬ:", GOLD, True,
         "Исследовать строение, состав и происхождение колец Сатурна на основе данных "
         "космических миссий (Voyager, Cassini) и современных научных публикаций."),
        ("ГИПОТЕЗА:", GOLD, True,
         "Кольца Сатурна являются относительно молодым образованием (не более 100 млн лет), "
         "сформировавшимся в результате разрушения спутника или захвата кометного вещества, "
         "и продолжают медленно исчезать под действием «дождя» из частиц."),
    ]
    first = True
    for label, lcolor, lbold, body in entries:
        p = tf2.paragraphs[0] if first else tf2.add_paragraph()
        first = False
        if not first:
            p.space_before = Pt(10)
        run = p.add_run(); run.text = label
        run.font.size = Pt(20); run.font.bold = True
        run.font.color.rgb = lcolor; run.font.name = "Calibri"
        p2 = tf2.add_paragraph(); p2.space_before = Pt(2)
        r2 = p2.add_run(); r2.text = body
        r2.font.size = Pt(18); r2.font.color.rgb = LIGHT_GREY; r2.font.name = "Calibri"

    # ── Слайд 3: Сатурн как планета ─────────────────────────────────────────
    bullet_slide(prs, blank, "Сатурн: общая характеристика", [
        "Шестая планета от Солнца, газовый гигант, масса — 95 масс Земли.",
        "Среднее расстояние от Солнца: 1,43 млрд км (9,58 а. е.).",
        "Период обращения вокруг Солнца: 29,5 земных лет.",
        "Плотность: 0,687 г/см³ — единственная планета легче воды.",
        "Атмосфера: водород (96%), гелий (3%), следы метана, аммиака, воды.",
        "87 известных спутников; крупнейший — Титан, с плотной азотной атмосферой.",
        "Сильнейшие ветры в Солнечной системе: до 1800 км/ч в экваториальной зоне.",
    ])

    # ── Слайд 4: Строение кольцевой системы ──────────────────────────────────
    bullet_slide(prs, blank, "Строение кольцевой системы", [
        "Кольца простираются от ~7 000 до ~120 700 км над экватором планеты.",
        "Семь главных колец: D, C, B, A, F, G, E (от внутреннего к внешнему).",
        "Кольцо B — самое широкое и яркое (25 500 км), толщина: 5–15 м.",
        "Кольцо A отделено от B щелью Кассини (4 800 км) — влияние спутника Мимас.",
        "Кольцо E — самое протяжённое (~300 000 км), питается гейзерами Энцелада.",
        "Общая масса колец: ~1,5×10¹⁹ кг ≈ 40% массы спутника Мимас.",
        "Видимая толщина колец — от 10 м до 1 км при ширине в тысячи километров.",
    ])

    # ── Слайд 5: Состав колец ────────────────────────────────────────────────
    bullet_slide(prs, blank, "Состав колец Сатурна", [
        "Основа: водяной лёд (90–95%) — частицы от пылинок до глыб размером ~10 м.",
        "Примеси: силикатные минералы, органические соединения, следы железа.",
        "Данные Cassini (2004–2017): кольца чище, чем ожидалось — 95% чистый лёд.",
        "Кольцо C и щель Кассини содержат больше силикатов — тёмный цвет.",
        "«Дождь» из частиц: ежесекундно ~10 000 кг льда падает в атмосферу Сатурна.",
        "Столь высокая чистота льда указывает на молодость колец (геологически).",
        "Инфракрасный спектр Cassini подтвердил водно-ледяную природу частиц.",
    ])

    # ── Слайд 6: Происхождение колец ─────────────────────────────────────────
    bullet_slide(prs, blank, "Происхождение колец: основные гипотезы", [
        "Гипотеза 1 (Лаплас/Роше): кольца — вещество, не сформировавшееся в спутник из-за приливных сил.",
        "Гипотеза 2 (современная): разрушение одного или нескольких крупных спутников.",
        "Гипотеза 3: захват и разрушение кометы или группы астероидов.",
        "Данные Cassini-2017: «загрязнение» колец метеоритным веществом ~6–200 г/м²/год.",
        "По скорости загрязнения возраст колец: 10–100 млн лет (эпоха динозавров на Земле).",
        "Спорная гипотеза: разрушение спутника «протоСатурна» с ледяной мантией размером с Титан.",
        "Предел Роше для Сатурна (~2,5 радиуса) совпадает с внешним краем главных колец.",
    ])

    # ── Слайд 7: Динамика и эволюция колец ───────────────────────────────────
    bullet_slide(prs, blank, "Динамика и эволюция колец", [
        "Кольца нестабильны: через 100–300 млн лет они полностью исчезнут.",
        "«Кольцевой дождь»: магнитное поле Сатурна притягивает заряженные частицы льда.",
        "Спутники-пастухи (Прометей, Пандора) удерживают кольцо F от рассеивания.",
        "Щель Кассини поддерживается орбитальным резонансом 2:1 с Мимасом.",
        "Кольца взаимодействуют с верхними слоями атмосферы через ионосферу.",
        "Volны плотности в кольце A возникают от резонансов с несколькими спутниками.",
        "Данные радиозатмений Cassini: кольца не монолитны — «пропеллеры» и зазоры.",
    ])

    # ── Слайд 8: Миссии по изучению Сатурна ──────────────────────────────────
    bullet_slide(prs, blank, "Ключевые миссии по изучению Сатурна", [
        "Pioneer 11 (1979): первый пролёт мимо Сатурна, обнаружены новые кольца.",
        "Voyager 1 (1980): детальные снимки колец, открытие сложной структуры.",
        "Voyager 2 (1981): уточнение состава, обнаружение колец F и G.",
        "Cassini–Huygens (2004–2017): 13 лет на орбите, ~635 Гб научных данных.",
        "Cassini-финал (2017): «Великое завершение» — 22 пролёта между планетой и кольцами.",
        "Открытия Cassini: сезонные изменения, волны плотности, кольцевой дождь.",
        "Будущее: миссия Dragonfly (2028) к Титану, обсуждается новая орбитальная миссия.",
    ])

    # ── Слайд 9: Интересные факты ────────────────────────────────────────────
    bullet_slide(prs, blank, "Интересные факты о кольцах Сатурна", [
        "Кольца видны в телескоп при увеличении ×25 — первым их описал Галилей в 1610 г.",
        "Гюйгенс в 1655 г. первым правильно интерпретировал их как плоский диск.",
        "Угол наклона колец меняется с 0° до 27° при наблюдении с Земли — 15-летний цикл.",
        "В 1612 и 1907 гг. кольца были «невидимы» — планета смотрела ребром.",
        "Отражательная способность (альбедо) колец: 0,4–0,6 — как свежий снег.",
        "Вес всех колец можно сравнить с весом горы Эверест, умноженной на 40 000.",
        "Сатурн — не единственный: кольца есть у Юпитера, Урана и Нептуна, но они тёмные.",
    ])

    # ── Слайд 10: Вывод — 5 ограничений (что невозможно) ────────────────────
    s10 = prs.slides.add_slide(blank)
    set_bg(s10, make_dark_bg(), prs)
    bar10 = s10.shapes.add_shape(1, Inches(0.5), Inches(1.55), Inches(12.33), Pt(3))
    bar10.fill.solid(); bar10.fill.fore_color.rgb = GOLD; bar10.line.fill.background()
    txt(s10, "Вывод: что невозможно (5 пунктов)",
        Inches(0.5), Inches(0.25), Inches(12.33), Inches(1.2),
        size=32, bold=True, color=GOLD)

    box10 = s10.shapes.add_textbox(Inches(0.6), Inches(1.75), Inches(12.13), Inches(5.4))
    tf10 = box10.text_frame; tf10.word_wrap = True
    negatives = [
        "1. Невозможно точно установить дату образования колец: погрешность методов — десятки миллионов лет.",
        "2. Невозможно высадить аппарат на кольца: частицы разлетаются на скорости ~25 км/с, нет твёрдой поверхности.",
        "3. Невозможно «законсервировать» кольца: физические процессы (дождь, столкновения) неостановимы.",
        "4. Невозможно наблюдать кольца под нулевым углом с Земли: они исчезают с вида каждые ~15 лет.",
        "5. Невозможно подтвердить единственную гипотезу происхождения: все три модели имеют аргументы «за» и «против».",
    ]
    for i, line in enumerate(negatives):
        p = tf10.paragraphs[0] if i == 0 else tf10.add_paragraph()
        if i > 0: p.space_before = Pt(8)
        run = p.add_run(); run.text = line
        run.font.size = Pt(20); run.font.color.rgb = RGBColor(0xFF, 0xAA, 0xAA)
        run.font.name = "Calibri"

    # ── Слайд 11: Вывод — 5 реальных возможностей ────────────────────────────
    s11 = prs.slides.add_slide(blank)
    set_bg(s11, make_dark_bg(), prs)
    bar11 = s11.shapes.add_shape(1, Inches(0.5), Inches(1.55), Inches(12.33), Pt(3))
    bar11.fill.solid(); bar11.fill.fore_color.rgb = GOLD; bar11.line.fill.background()
    txt(s11, "Вывод: реальные возможности (5 пунктов)",
        Inches(0.5), Inches(0.25), Inches(12.33), Inches(1.2),
        size=32, bold=True, color=GOLD)

    box11 = s11.shapes.add_textbox(Inches(0.6), Inches(1.75), Inches(12.13), Inches(5.4))
    tf11 = box11.text_frame; tf11.word_wrap = True
    positives = [
        "1. Реально: рассчитать возраст колец с точностью ±20–30 млн лет по скорости их загрязнения.",
        "2. Реально: отправить новый орбитальный зонд для долгосрочного мониторинга динамики колец.",
        "3. Реально: использовать кольца как «лабораторию» для изучения процессов аккреции и образования планет.",
        "4. Реально: моделировать формирование экзопланетных колец по аналогии с Сатурном.",
        "5. Реально: добыча водяного льда из колец как ресурса для будущих межпланетных экспедиций.",
    ]
    for i, line in enumerate(positives):
        p = tf11.paragraphs[0] if i == 0 else tf11.add_paragraph()
        if i > 0: p.space_before = Pt(8)
        run = p.add_run(); run.text = line
        run.font.size = Pt(20); run.font.color.rgb = RGBColor(0xAA, 0xFF, 0xAA)
        run.font.name = "Calibri"

    # ── Слайд 12: Приложение — 7 вопросов ────────────────────────────────────
    s12 = prs.slides.add_slide(blank)
    set_bg(s12, make_dark_bg(), prs)
    bar12 = s12.shapes.add_shape(1, Inches(0.5), Inches(1.55), Inches(12.33), Pt(3))
    bar12.fill.solid(); bar12.fill.fore_color.rgb = GOLD; bar12.line.fill.background()
    txt(s12, "Приложение: контрольные вопросы",
        Inches(0.5), Inches(0.25), Inches(12.33), Inches(1.2),
        size=32, bold=True, color=GOLD)

    box12 = s12.shapes.add_textbox(Inches(0.6), Inches(1.75), Inches(12.13), Inches(5.4))
    tf12 = box12.text_frame; tf12.word_wrap = True
    questions = [
        "1. Сколько главных колец имеет Сатурн и как они обозначаются?",
        "2. Что такое щель Кассини и какой спутник её «поддерживает»?",
        "3. Из какого основного вещества состоят кольца Сатурна?",
        "4. Какие три гипотезы происхождения колец существуют в науке?",
        "5. Что такое «кольцевой дождь» и как он влияет на судьбу колец?",
        "6. Какая космическая миссия дала наибольший вклад в изучение колец и почему?",
        "7. Почему учёные считают кольца Сатурна геологически молодыми образованиями?",
    ]
    for i, q in enumerate(questions):
        p = tf12.paragraphs[0] if i == 0 else tf12.add_paragraph()
        if i > 0: p.space_before = Pt(8)
        run = p.add_run(); run.text = q
        run.font.size = Pt(20); run.font.color.rgb = LIGHT_GOLD
        run.font.name = "Calibri"

    # ── Сохраняем ─────────────────────────────────────────────────────────────
    buf = io.BytesIO()
    prs.save(buf)
    buf.seek(0)
    data = base64.b64encode(buf.read()).decode("utf-8")

    return {
        "statusCode": 200,
        "headers": {"Access-Control-Allow-Origin": "*", "Content-Type": "application/json"},
        "body": '{"filename":"saturn_rings.pptx","data":"' + data + '"}',
    }
