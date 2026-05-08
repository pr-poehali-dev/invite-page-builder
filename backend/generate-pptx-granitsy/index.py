"""
Генерация PPTX-презентации 'Техника экологичного выставления границ'
в стиле Фуллерен: светлый серый фон, чёрный serif-шрифт, картинки пионов.
Возвращает файл в base64 для скачивания.
"""

import base64
import io
import urllib.request
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from PIL import Image


BLACK     = RGBColor(0x1A, 0x17, 0x14)
LIGHT_BG  = RGBColor(0xEB, 0xEB, 0xEB)
ORANGE    = RGBColor(0xC8, 0x6A, 0x1A)

SLIDE1_URL  = "https://cdn.poehali.dev/projects/a853d61a-73f8-407d-846b-967c4543637c/bucket/29d08a49-613a-4d33-8137-21a389ad93de.jpg"
SLIDE2_URL  = "https://cdn.poehali.dev/projects/a853d61a-73f8-407d-846b-967c4543637c/bucket/01d2305b-665f-4ebd-8bb7-319ae91c8478.jpg"
SLIDE3_URL  = "https://cdn.poehali.dev/projects/a853d61a-73f8-407d-846b-967c4543637c/bucket/51bfdabb-136e-4fa8-a103-c68df682d5f6.jpg"
SLIDE4_URL  = "https://cdn.poehali.dev/projects/a853d61a-73f8-407d-846b-967c4543637c/bucket/865d9958-544a-4eb6-a35b-d4a510138d0e.jpg"
SLIDE5_URL  = "https://cdn.poehali.dev/projects/a853d61a-73f8-407d-846b-967c4543637c/bucket/a7d3de70-0616-42db-8c1c-e0676af936dd.jpg"
LOGO_URL    = "https://cdn.poehali.dev/projects/a853d61a-73f8-407d-846b-967c4543637c/bucket/29d08a49-613a-4d33-8137-21a389ad93de.jpg"

SLIDE6_URL  = "https://cdn.poehali.dev/projects/a853d61a-73f8-407d-846b-967c4543637c/bucket/3de004e6-28d6-4ed4-8589-9189189d74d2.jpg"
SLIDE7_URL  = "https://cdn.poehali.dev/projects/a853d61a-73f8-407d-846b-967c4543637c/bucket/9e0ba4c7-ce81-4fc9-83e3-6c407afc0baf.jpg"
SLIDE8_URL  = "https://cdn.poehali.dev/projects/a853d61a-73f8-407d-846b-967c4543637c/bucket/815dddbc-f473-4a80-bfb3-98b99c1e176c.jpg"
SLIDE9_URL  = "https://cdn.poehali.dev/projects/a853d61a-73f8-407d-846b-967c4543637c/bucket/b7c290fb-7264-4bb8-a1ab-517664b763b9.jpg"
SLIDE10_URL = "https://cdn.poehali.dev/projects/a853d61a-73f8-407d-846b-967c4543637c/bucket/7026859a-cf33-4ce7-b1bf-efcca21cbfe8.jpg"
SLIDE11_URL = "https://cdn.poehali.dev/projects/a853d61a-73f8-407d-846b-967c4543637c/bucket/40618ec4-5ca0-47cd-9574-5014aae8e31b.jpg"
SLIDE12_URL = "https://cdn.poehali.dev/projects/a853d61a-73f8-407d-846b-967c4543637c/bucket/f9a5125d-39f7-49e4-a615-c812cab487c4.jpg"
SLIDE13_URL = "https://cdn.poehali.dev/projects/a853d61a-73f8-407d-846b-967c4543637c/bucket/ac33b6fc-0179-4405-8115-c0977a5f0585.jpg"
SLIDE14_URL = "https://cdn.poehali.dev/projects/a853d61a-73f8-407d-846b-967c4543637c/bucket/d053f5dc-f4de-45e4-acbe-93f27f9fa685.jpg"
SLIDE15_URL = "https://cdn.poehali.dev/projects/a853d61a-73f8-407d-846b-967c4543637c/bucket/55a41459-daa7-4807-888e-01e431cc5ff3.jpg"
SLIDE16_URL = "https://cdn.poehali.dev/projects/a853d61a-73f8-407d-846b-967c4543637c/bucket/81180375-d2f7-4702-94ba-9e1158282cee.jpg"
SLIDE17_URL = "https://cdn.poehali.dev/projects/a853d61a-73f8-407d-846b-967c4543637c/bucket/c0adf201-961e-43f8-a3ed-7e7f3c76aa4d.jpg"
SLIDE18_URL = "https://cdn.poehali.dev/projects/a853d61a-73f8-407d-846b-967c4543637c/bucket/d96f1c30-a985-406e-90a3-fa07d0d24f65.jpg"
SLIDE19_URL = "https://cdn.poehali.dev/projects/a853d61a-73f8-407d-846b-967c4543637c/bucket/f9dd08ee-b85d-4fa3-be7f-e9970371184a.jpg"
SLIDE20_URL = "https://cdn.poehali.dev/projects/a853d61a-73f8-407d-846b-967c4543637c/bucket/8247f3eb-be58-4e85-b7a1-d9c2b0706875.jpg"

RED = RGBColor(0xCC, 0x00, 0x00)


def download_image_as_jpg(url: str, max_dim: int = 1920, bg_color=(235, 235, 235)) -> io.BytesIO:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=25) as r:
        raw = io.BytesIO(r.read())
    img = Image.open(raw)
    if img.mode in ("RGBA", "P", "LA"):
        bg = Image.new("RGB", img.size, bg_color)
        if img.mode == "P":
            img = img.convert("RGBA")
        mask = img.split()[-1] if img.mode in ("RGBA", "LA") else None
        bg.paste(img.convert("RGBA") if img.mode not in ("RGBA",) else img, mask=mask)
        img = bg
    elif img.mode != "RGB":
        img = img.convert("RGB")
    w, h = img.size
    if max(w, h) > max_dim:
        ratio = max_dim / max(w, h)
        img = img.resize((int(w * ratio), int(h * ratio)), Image.LANCZOS)
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=85, optimize=True)
    buf.seek(0)
    return buf


def make_light_bg(width_px: int, height_px: int) -> io.BytesIO:
    img = Image.new("RGB", (width_px, height_px), (235, 235, 235))
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return buf


def set_bg_image(slide, img_buf: io.BytesIO, prs):
    img_buf.seek(0)
    W = prs.slide_width
    H = prs.slide_height
    pic = slide.shapes.add_picture(img_buf, 0, 0, W, H)
    slide.shapes._spTree.remove(pic._element)
    slide.shapes._spTree.insert(2, pic._element)


def add_textbox(slide, text, left, top, width, height,
                font_size=32, bold=False, color=BLACK,
                align=PP_ALIGN.CENTER, italic=False, font_name="Times New Roman"):
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
    run.font.name = font_name
    return txBox


def add_multiline_textbox(slide, lines, left, top, width, height,
                           font_sizes, bolds, colors, aligns,
                           font_name="Times New Roman"):
    txBox = slide.shapes.add_textbox(left, top, width, height)
    tf = txBox.text_frame
    tf.word_wrap = True
    for i, line in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = aligns[i] if i < len(aligns) else PP_ALIGN.CENTER
        run = p.add_run()
        run.text = line
        run.font.size = Pt(font_sizes[i] if i < len(font_sizes) else 32)
        run.font.bold = bolds[i] if i < len(bolds) else False
        run.font.color.rgb = colors[i] if i < len(colors) else BLACK
        run.font.name = font_name
        if i > 0:
            p.space_before = Pt(10)
    return txBox


def add_full_image_slide(prs, slide, url):
    try:
        img_buf = download_image_as_jpg(url)
        W = prs.slide_width
        H = prs.slide_height
        img_buf.seek(0)
        pil_img = Image.open(img_buf)
        orig_w, orig_h = pil_img.size
        scale = max(W / orig_w, H / orig_h)
        new_w = int(orig_w * scale)
        new_h = int(orig_h * scale)
        offset_x = (W - new_w) // 2
        offset_y = (H - new_h) // 2
        img_buf.seek(0)
        pic = slide.shapes.add_picture(img_buf, offset_x, offset_y, new_w, new_h)
        slide.shapes._spTree.remove(pic._element)
        slide.shapes._spTree.insert(2, pic._element)
    except Exception:
        pass


def handler(event: dict, context) -> dict:
    """Генерирует PPTX-презентацию 'Техника экологичного выставления границ' в стиле Фуллерен"""

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

    def safe_dl(url):
        try:
            return download_image_as_jpg(url)
        except Exception:
            return None

    def light_bg():
        return make_light_bg(1920, 1080)

    # ── Слайд 1: Титульный (полная картинка слайд1 как фон) ─────────────────
    slide1 = prs.slides.add_slide(blank)
    add_full_image_slide(prs, slide1, SLIDE1_URL)

    # ── Слайды 2-5: Картинки пионов (полноэкранные) ──────────────────────────
    for url in [SLIDE2_URL, SLIDE3_URL, SLIDE4_URL, SLIDE5_URL]:
        slide = prs.slides.add_slide(blank)
        add_full_image_slide(prs, slide, url)

    # ── Слайды 6-14: Текстовые на светлом фоне (полноэкранные картинки) ──────
    for url in [SLIDE6_URL, SLIDE7_URL, SLIDE8_URL, SLIDE9_URL,
                SLIDE10_URL, SLIDE11_URL, SLIDE12_URL, SLIDE13_URL, SLIDE14_URL]:
        slide = prs.slides.add_slide(blank)
        add_full_image_slide(prs, slide, url)

    # ── Слайды 15-20: Новые слайды (полноэкранные картинки) ──────────────────
    for url in [SLIDE15_URL, SLIDE16_URL, SLIDE17_URL,
                SLIDE18_URL, SLIDE19_URL, SLIDE20_URL]:
        slide = prs.slides.add_slide(blank)
        add_full_image_slide(prs, slide, url)

    # ── Сохраняем и отдаём base64 ─────────────────────────────────────────────
    buf = io.BytesIO()
    prs.save(buf)
    buf.seek(0)
    data = base64.b64encode(buf.read()).decode("utf-8")

    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Content-Type": "application/json",
        },
        "body": '{"filename":"granitsy_presentation.pptx","data":"' + data + '"}',
    }