"""
Генерация PPTX-презентации "Квантовая педагогика" в космическом стиле.
Возвращает файл в base64 для скачивания.
"""

import base64
import io
import os
import urllib.request
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.util import Inches, Pt


def add_space_background(slide, prs):
    """Добавляет тёмно-синий космический фон"""
    from pptx.util import Inches
    from pptx.dml.color import RGBColor
    bg = slide.background
    fill = bg.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(0x03, 0x07, 0x2A)


def download_image(url):
    """Скачивает изображение по URL и возвращает BytesIO"""
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=15) as response:
        return io.BytesIO(response.read())


def add_textbox(slide, text, left, top, width, height, font_size=24, bold=False,
                color=RGBColor(0xFF, 0xFF, 0xFF), align=PP_ALIGN.CENTER, italic=False):
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


def handler(event: dict, context) -> dict:
    """Генерирует PPTX-презентацию о квантовой педагогике и возвращает base64"""

    if event.get('httpMethod') == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Max-Age': '86400'
            },
            'body': ''
        }

    prs = Presentation()
    prs.slide_width = Inches(13.33)
    prs.slide_height = Inches(7.5)

    blank_layout = prs.slide_layouts[6]

    # Цвета
    GOLD = RGBColor(0xFF, 0xD7, 0x00)
    WHITE = RGBColor(0xFF, 0xFF, 0xFF)
    LIGHT_BLUE = RGBColor(0xAD, 0xD8, 0xE6)
    GOLD_LIGHT = RGBColor(0xFF, 0xE8, 0x80)

    W = prs.slide_width
    H = prs.slide_height

    # ===== СЛАЙД 1 =====
    slide1 = prs.slides.add_slide(blank_layout)
    add_space_background(slide1, prs)

    # Логотип спирали по центру сверху
    try:
        spiral_url = "https://cdn.poehali.dev/projects/a853d61a-73f8-407d-846b-967c4543637c/bucket/4083467d-4f30-4338-bbe4-204644e9c2bf.png"
        spiral_img = download_image(spiral_url)
        spiral_size = Inches(2.2)
        spiral_left = (W - spiral_size) // 2
        slide1.shapes.add_picture(spiral_img, spiral_left, Inches(0.6), spiral_size, spiral_size)
    except:
        pass

    # Заголовок
    add_textbox(slide1, "КВАНТОВАЯ ПЕДАГОГИКА",
                Inches(0.5), Inches(3.1), W - Inches(1), Inches(1.2),
                font_size=48, bold=True, color=GOLD)

    # Подзаголовок
    add_textbox(slide1, 'Центр квантовой педагогики и психологии "Фуллерен"',
                Inches(0.5), Inches(4.4), W - Inches(1), Inches(0.9),
                font_size=22, bold=False, color=LIGHT_BLUE)

    # Декоративные звёзды
    for star_text, lft, tp in [("✦", Inches(0.5), Inches(0.3)), ("✦", Inches(12.5), Inches(0.3)),
                                ("✦", Inches(0.5), Inches(7.0)), ("✦", Inches(12.5), Inches(7.0))]:
        add_textbox(slide1, star_text, lft, tp, Inches(0.5), Inches(0.5), font_size=18, color=GOLD_LIGHT)

    # ===== СЛАЙД 2 =====
    slide2 = prs.slides.add_slide(blank_layout)
    add_space_background(slide2, prs)

    # Заголовок слайда
    add_textbox(slide2, "Владимир Филиппович Базарный",
                Inches(0.3), Inches(0.2), W - Inches(0.6), Inches(0.7),
                font_size=28, bold=True, color=GOLD)

    # Фото Базарного — по центру
    try:
        bazarny_url = "https://cdn.poehali.dev/projects/a853d61a-73f8-407d-846b-967c4543637c/bucket/2b075abe-8b7b-4015-bfb3-71ee7198df9a.png"
        bazarny_img = download_image(bazarny_url)
        img_w = Inches(5.5)
        img_h = Inches(5.8)
        img_left = (W - img_w) // 2
        slide2.shapes.add_picture(bazarny_img, img_left, Inches(1.0), img_w, img_h)
    except:
        pass

    add_textbox(slide2, "В.Ф. Базарный",
                Inches(0.3), Inches(6.9), W - Inches(0.6), Inches(0.45),
                font_size=16, bold=False, color=LIGHT_BLUE)

    # ===== СЛАЙД 3 =====
    slide3 = prs.slides.add_slide(blank_layout)
    add_space_background(slide3, prs)

    photos_3 = [
        ("https://cdn.poehali.dev/projects/a853d61a-73f8-407d-846b-967c4543637c/bucket/1589e3bb-bdc7-4e1e-9977-28bab6bc26a9.png",
         "М.П. Щетинин"),
        ("https://cdn.poehali.dev/projects/a853d61a-73f8-407d-846b-967c4543637c/bucket/c70ffe39-d7ee-4e81-87cc-89864954889a.png",
         "Ш.А. Амонашвили"),
        ("https://cdn.poehali.dev/projects/a853d61a-73f8-407d-846b-967c4543637c/bucket/8aa076ab-aa1c-43c5-b471-b901927f46f7.png",
         "В.Ф. Шаталов"),
    ]

    photo_w = Inches(3.5)
    photo_h = Inches(3.8)
    gap = (W - photo_w * 3) // 4
    for i, (url, name) in enumerate(photos_3):
        left = gap + i * (photo_w + gap)
        try:
            img_data = download_image(url)
            slide3.shapes.add_picture(img_data, left, Inches(0.5), photo_w, photo_h)
        except:
            pass
        add_textbox(slide3, name, left, Inches(4.4), photo_w, Inches(0.5),
                    font_size=16, bold=True, color=GOLD)

    add_textbox(slide3,
                '"Почему мы не можем с таким же успехом повторить опыт этих личностей?"',
                Inches(0.5), Inches(5.1), W - Inches(1), Inches(1.8),
                font_size=22, bold=False, italic=True, color=WHITE)

    # ===== СЛАЙД 4 =====
    slide4 = prs.slides.add_slide(blank_layout)
    add_space_background(slide4, prs)

    for i, (url, name) in enumerate(photos_3):
        left = gap + i * (photo_w + gap)
        try:
            img_data = download_image(url)
            slide4.shapes.add_picture(img_data, left, Inches(0.5), photo_w, photo_h)
        except:
            pass
        add_textbox(slide4, name, left, Inches(4.4), photo_w, Inches(0.5),
                    font_size=16, bold=True, color=GOLD)

    add_textbox(slide4,
                "Учит не методика этих людей",
                Inches(0.5), Inches(5.1), W - Inches(1), Inches(1.8),
                font_size=30, bold=True, color=GOLD_LIGHT)

    # ===== СЛАЙД 5 =====
    slide5 = prs.slides.add_slide(blank_layout)
    add_space_background(slide5, prs)

    for i, (url, name) in enumerate(photos_3):
        left = gap + i * (photo_w + gap)
        try:
            img_data = download_image(url)
            slide5.shapes.add_picture(img_data, left, Inches(0.5), photo_w, photo_h)
        except:
            pass
        add_textbox(slide5, name, left, Inches(4.4), photo_w, Inches(0.5),
                    font_size=16, bold=True, color=GOLD)

    add_textbox(slide5,
                "Сама ЛИЧНОСТЬ преОБРАЗует пространство",
                Inches(0.5), Inches(5.1), W - Inches(1), Inches(1.8),
                font_size=30, bold=True, color=GOLD)

    # Сохраняем в байты
    output = io.BytesIO()
    prs.save(output)
    output.seek(0)
    pptx_b64 = base64.b64encode(output.read()).decode('utf-8')

    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Content-Type': 'application/json',
        },
        'body': f'{{"filename": "kvantovaya_pedagogika.pptx", "data": "{pptx_b64}"}}'
    }
