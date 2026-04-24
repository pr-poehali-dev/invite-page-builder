"""
Генерация PPTX-презентации "Квантовая педагогика" в золотисто-тёмном стиле.
Возвращает файл в base64 для скачивания.
"""

import base64
import io
import urllib.request
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.oxml.ns import qn
from lxml import etree
from PIL import Image, ImageDraw, ImageFilter
import math


# ── Цвета ────────────────────────────────────────────────────────────────────
DARK_BG   = RGBColor(0x0A, 0x08, 0x00)   # почти чёрный
GOLD      = RGBColor(0xFF, 0xD7, 0x00)
GOLD2     = RGBColor(0xFF, 0xA5, 0x00)
GOLD3     = RGBColor(0xC8, 0x85, 0x00)
WHITE     = RGBColor(0xFF, 0xFF, 0xFF)
OFF_WHITE = RGBColor(0xF0, 0xE8, 0xD0)
DARK_GOLD = RGBColor(0x3A, 0x28, 0x00)


def download_image(url: str) -> io.BytesIO:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=20) as r:
        return io.BytesIO(r.read())


def make_bg_image(width_px: int, height_px: int) -> io.BytesIO:
    """
    Генерирует фоновое изображение:
    - левая половина: тёмно-чёрная с лёгкими формульными символами
    - правая половина: золотой градиент
    - плавное смешение по центру
    """
    img = Image.new("RGB", (width_px, height_px), (10, 8, 0))
    draw = ImageDraw.Draw(img)

    # Золотой градиент на правой части
    for x in range(width_px // 2, width_px):
        ratio = (x - width_px // 2) / (width_px // 2)
        # от тёмного к золотому
        r = int(10 + ratio * (180 - 10))
        g = int(8  + ratio * (120 - 8))
        b = int(0  + ratio * (0))
        for y in range(height_px):
            draw.point((x, y), fill=(r, g, b))

    # Полупрозрачный затемнённый слой сверху и снизу (виньетка) — через чёрные полосы
    for y in range(height_px):
        alpha = 0
        if y < height_px * 0.15:
            alpha = int(120 * (1 - y / (height_px * 0.15)))
        elif y > height_px * 0.85:
            alpha = int(120 * ((y - height_px * 0.85) / (height_px * 0.15)))
        if alpha > 0:
            for x in range(width_px):
                px = img.getpixel((x, y))
                blended = tuple(int(c * (1 - alpha/255)) for c in px)
                draw.point((x, y), fill=blended)

    # Символы-формулы по левой части (декоративно)
    formula_symbols = [
        (50,  60,  "= 2"),
        (120, 130, "∫ dx"),
        (30,  200, "E = mc²"),
        (180, 80,  "λ"),
        (80,  300, "Δ = b²-4ac"),
        (200, 250, "∑"),
        (50,  380, "∇ψ"),
        (150, 350, "ħ"),
        (250, 150, "quantum"),
        (20,  450, "φ = 1.618"),
        (160, 430, "π"),
        (300, 320, "∞"),
        (90,  500, "Ω"),
        (220, 490, "α β γ"),
        (350, 80,  "-2/3"),
        (320, 200, "0 · 1"),
        (380, 400, "db"),
        (450, 130, "v = f·λ"),
        (430, 300, "h·ν"),
        (480, 450, "⊕"),
    ]
    for (fx, fy, sym) in formula_symbols:
        opacity_r, opacity_g, opacity_b = 60, 50, 10
        draw.text((fx, fy), sym, fill=(opacity_r, opacity_g, opacity_b))

    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return buf


def make_photo_bg(width_px: int, height_px: int) -> io.BytesIO:
    """Фон для слайдов с фотографиями: тёмный с золотым свечением снизу"""
    img = Image.new("RGB", (width_px, height_px), (8, 6, 0))
    draw = ImageDraw.Draw(img)

    # Золотое свечение снизу
    for y in range(height_px // 2, height_px):
        ratio = (y - height_px // 2) / (height_px // 2)
        r = int(8  + ratio * 60)
        g = int(6  + ratio * 40)
        b = 0
        for x in range(width_px):
            draw.point((x, y), fill=(r, g, b))

    # Боковое золотое свечение справа
    for x in range(width_px * 3 // 4, width_px):
        ratio = (x - width_px * 3 // 4) / (width_px // 4)
        r = int(8  + ratio * 50)
        g = int(6  + ratio * 30)
        b = 0
        for y in range(height_px):
            px = img.getpixel((x, y))
            draw.point((x, y), fill=(min(255, px[0] + r), min(255, px[1] + g), px[2]))

    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return buf


def set_bg_image(slide, img_buf: io.BytesIO, prs):
    """Устанавливает картинку как фон слайда через XML"""
    from pptx.util import Inches
    W = prs.slide_width
    H = prs.slide_height
    img_buf.seek(0)
    pic = slide.shapes.add_picture(img_buf, 0, 0, W, H)
    # Отправляем на задний план
    slide.shapes._spTree.remove(pic._element)
    slide.shapes._spTree.insert(2, pic._element)


def add_textbox(slide, text, left, top, width, height,
                font_size=24, bold=False, color=WHITE,
                align=PP_ALIGN.LEFT, italic=False, shadow=False):
    txBox = slide.shapes.add_textbox(left, top, width, height)
    tf = txBox.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.alignment = align
    run = p.add_run()
    run.text = text
    run.font.size = Pt(font_size)
    run.font.bold = bold
    run.font.italic = italic
    run.font.color.rgb = color
    return txBox


def add_photo_proportional(slide, img_buf, left, top, max_w, max_h):
    """Вставляет фото сохраняя пропорции, центрируя в заданной области"""
    img_buf.seek(0)
    pil_img = Image.open(img_buf)
    orig_w, orig_h = pil_img.size

    ratio_w = max_w / orig_w
    ratio_h = max_h / orig_h
    ratio = min(ratio_w, ratio_h)

    new_w = int(orig_w * ratio)
    new_h = int(orig_h * ratio)

    offset_x = (max_w - new_w) // 2
    offset_y = (max_h - new_h) // 2

    img_buf.seek(0)
    slide.shapes.add_picture(img_buf, left + offset_x, top + offset_y, new_w, new_h)


def handler(event: dict, context) -> dict:
    """Генерирует PPTX-презентацию о квантовой педагогике (золотой стиль) и возвращает base64"""

    if event.get("httpMethod") == "OPTIONS":
        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type",
                "Access-Control-Max-Age": "86400",
            },
            "body": "",
        }

    prs = Presentation()
    prs.slide_width  = Inches(13.33)
    prs.slide_height = Inches(7.5)
    blank = prs.slide_layouts[6]

    W = prs.slide_width
    H = prs.slide_height

    # px размер для генерации фона (1333×750 → уменьшим в 4x для скорости)
    BG_W, BG_H = 1333, 750

    SPIRAL_URL   = "https://cdn.poehali.dev/projects/a853d61a-73f8-407d-846b-967c4543637c/bucket/4083467d-4f30-4338-bbe4-204644e9c2bf.png"
    BAZARNY_URL  = "https://cdn.poehali.dev/projects/a853d61a-73f8-407d-846b-967c4543637c/bucket/2b075abe-8b7b-4015-bfb3-71ee7198df9a.png"
    SHCHET_URL   = "https://cdn.poehali.dev/projects/a853d61a-73f8-407d-846b-967c4543637c/bucket/1589e3bb-bdc7-4e1e-9977-28bab6bc26a9.png"
    AMON_URL     = "https://cdn.poehali.dev/projects/a853d61a-73f8-407d-846b-967c4543637c/bucket/c70ffe39-d7ee-4e81-87cc-89864954889a.png"
    SHAT_URL     = "https://cdn.poehali.dev/projects/a853d61a-73f8-407d-846b-967c4543637c/bucket/8aa076ab-aa1c-43c5-b471-b901927f46f7.png"

    # Скачиваем фото заранее
    try: bazarny_raw = download_image(BAZARNY_URL)
    except: bazarny_raw = None
    try: shchet_raw  = download_image(SHCHET_URL)
    except: shchet_raw = None
    try: amon_raw    = download_image(AMON_URL)
    except: amon_raw = None
    try: shat_raw    = download_image(SHAT_URL)
    except: shat_raw = None
    try: spiral_raw  = download_image(SPIRAL_URL)
    except: spiral_raw = None

    photos_3 = [
        (shchet_raw,  "Михаил Петрович\nЩетинин"),
        (amon_raw,    "Шалва Александрович\nАмонашвили"),
        (shat_raw,    "Виктор Фёдорович\nШаталов"),
    ]

    # ── Фоны ────────────────────────────────────────────────────────────────
    bg_title = make_bg_image(BG_W, BG_H)
    bg_photo = make_photo_bg(BG_W, BG_H)

    # ===== СЛАЙД 1 — титульный =====
    s1 = prs.slides.add_slide(blank)
    bg_title.seek(0)
    set_bg_image(s1, bg_title, prs)

    # Большой белый заголовок слева (как на образце)
    add_textbox(s1, "КВАНТОВАЯ\nПЕДАГОГИКА",
                Inches(0.6), Inches(1.0), Inches(6.5), Inches(4.0),
                font_size=60, bold=True, color=WHITE, align=PP_ALIGN.LEFT)

    # Подзаголовок слева
    add_textbox(s1, 'Центр квантовой педагогики и психологии',
                Inches(0.6), Inches(5.2), Inches(6.5), Inches(0.7),
                font_size=20, bold=False, color=OFF_WHITE, align=PP_ALIGN.LEFT)

    # Спираль справа по центру
    if spiral_raw:
        spiral_raw.seek(0)
        s1.shapes.add_picture(spiral_raw, Inches(8.8), Inches(1.8), Inches(2.8), Inches(2.8))

    # Название центра справа снизу
    add_textbox(s1, "СОЗНАНИЕ ФУЛЛЕРЕНА",
                Inches(7.5), Inches(4.9), Inches(5.5), Inches(0.6),
                font_size=22, bold=True, color=GOLD, align=PP_ALIGN.CENTER)
    add_textbox(s1, "Центр квантовой педагогики и психологии",
                Inches(7.5), Inches(5.5), Inches(5.5), Inches(0.5),
                font_size=13, bold=False, color=OFF_WHITE, align=PP_ALIGN.CENTER)

    # Горизонтальная золотая линия
    from pptx.util import Pt as PtU
    line = s1.shapes.add_shape(
        1,  # MSO_SHAPE_TYPE.LINE — используем rectangle как разделитель
        Inches(0.6), Inches(6.5), Inches(12.0), Inches(0.03)
    )
    line.fill.solid()
    line.fill.fore_color.rgb = GOLD
    line.line.fill.background()

    # ===== СЛАЙД 2 — Базарный =====
    s2 = prs.slides.add_slide(blank)
    bg_photo.seek(0)
    set_bg_image(s2, bg_photo, prs)

    # Золотая полоса сверху
    top_bar = s2.shapes.add_shape(1, 0, 0, W, Inches(0.55))
    top_bar.fill.solid()
    top_bar.fill.fore_color.rgb = DARK_GOLD
    top_bar.line.fill.background()

    add_textbox(s2, "Владимир Филиппович Базарный",
                Inches(0.4), Inches(0.05), W - Inches(0.8), Inches(0.45),
                font_size=26, bold=True, color=GOLD, align=PP_ALIGN.LEFT)

    if bazarny_raw:
        bazarny_raw.seek(0)
        add_photo_proportional(s2, bazarny_raw,
                               left=Inches(3.5), top=Inches(0.7),
                               max_w=Inches(6.5), max_h=Inches(6.2))

    # Нижняя золотая полоса
    bot_bar = s2.shapes.add_shape(1, 0, H - Inches(0.5), W, Inches(0.5))
    bot_bar.fill.solid()
    bot_bar.fill.fore_color.rgb = DARK_GOLD
    bot_bar.line.fill.background()

    # ===== Вспомогательная функция для слайдов 3-5 =====
    def build_three_photo_slide(slide_obj, bottom_text, bottom_italic=False):
        bg_photo.seek(0)
        set_bg_image(slide_obj, bg_photo, prs)

        top_bar2 = slide_obj.shapes.add_shape(1, 0, 0, W, Inches(0.45))
        top_bar2.fill.solid()
        top_bar2.fill.fore_color.rgb = DARK_GOLD
        top_bar2.line.fill.background()

        photo_max_w = Inches(3.9)
        photo_max_h = Inches(4.2)
        total_photos_w = photo_max_w * 3
        gap = (W - total_photos_w) // 4

        for i, (raw, name) in enumerate(photos_3):
            left = gap + i * (photo_max_w + gap)
            if raw:
                raw.seek(0)
                add_photo_proportional(slide_obj, raw,
                                       left=left, top=Inches(0.55),
                                       max_w=photo_max_w, max_h=photo_max_h)
            # Подпись под фото
            add_textbox(slide_obj, name,
                        left, Inches(4.85), photo_max_w, Inches(0.75),
                        font_size=14, bold=True, color=GOLD, align=PP_ALIGN.CENTER)

        # Нижняя золотая полоса с текстом
        bot_bar2 = slide_obj.shapes.add_shape(1, 0, H - Inches(1.5), W, Inches(1.5))
        bot_bar2.fill.solid()
        bot_bar2.fill.fore_color.rgb = DARK_GOLD
        bot_bar2.line.fill.background()

        add_textbox(slide_obj, bottom_text,
                    Inches(0.5), H - Inches(1.45), W - Inches(1), Inches(1.4),
                    font_size=26, bold=not bottom_italic, italic=bottom_italic,
                    color=WHITE, align=PP_ALIGN.CENTER)

    # ===== СЛАЙД 3 =====
    s3 = prs.slides.add_slide(blank)
    build_three_photo_slide(
        s3,
        '"Почему мы не можем с таким же успехом\nповторить опыт этих личностей?"',
        bottom_italic=True
    )

    # ===== СЛАЙД 4 =====
    s4 = prs.slides.add_slide(blank)
    build_three_photo_slide(s4, "Учит не методика этих людей")

    # ===== СЛАЙД 5 =====
    s5 = prs.slides.add_slide(blank)
    build_three_photo_slide(s5, "Сама ЛИЧНОСТЬ преОБРАЗует пространство")

    # Финальный акцент на слайде 5 — цвет текста золотой
    # (переопределяем последний textbox)
    last_shapes = s5.shapes
    for shape in last_shapes:
        if shape.has_text_frame:
            for para in shape.text_frame.paragraphs:
                for run in para.runs:
                    if "ЛИЧНОСТЬ" in run.text or "преОБРАЗует" in run.text:
                        run.font.color.rgb = GOLD

    # ── Сохраняем ───────────────────────────────────────────────────────────
    output = io.BytesIO()
    prs.save(output)
    output.seek(0)
    pptx_b64 = base64.b64encode(output.read()).decode("utf-8")

    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Content-Type": "application/json",
        },
        "body": f'{{"filename": "kvantovaya_pedagogika.pptx", "data": "{pptx_b64}"}}',
    }
