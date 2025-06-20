import easyocr
from pdf2image import convert_from_path
import numpy as np
import cv2
import os
import json

def rotate_crop(img, x1, y1, x2, y2, angle=90):
    crop = img[y1:y2, x1:x2]
    if angle == 90:
        crop = cv2.rotate(crop, cv2.ROTATE_90_CLOCKWISE)
    elif angle == 270:
        crop = cv2.rotate(crop, cv2.ROTATE_90_COUNTERCLOCKWISE)
    return crop

def ocr_barcode_vertical(img_cv, x1, y1, x2, y2, angle=90, show_img=False):
    crop = rotate_crop(img_cv, x1, y1, x2, y2, angle)
    if show_img:
        import matplotlib.pyplot as plt
        plt.imshow(crop, cmap='gray')
        plt.title("Barcode Vertical Crop")
        plt.show()
    results = reader.readtext(crop)
    print("Barcode OCR Results:", results)
    # รวมเลขจากทุก group
    numbers = []
    for _, text, conf in results:
        text_onlynum = ''.join([c for c in text if c.isdigit()])
        if len(text_onlynum) >= 6:
            numbers.append(text_onlynum)
    barcode = ''.join(numbers)
    return barcode if barcode else ""

def ocr_vertical_date_specimen(img_cv, x1, y1, x2, y2, angle=90):
    crop = rotate_crop(img_cv, x1, y1, x2, y2, angle)
    results = reader.readtext(crop)
    texts = [text for _, text, conf in results if conf > 0.2]
    return texts

output_dir = 'pages'
os.makedirs(output_dir, exist_ok=True)

# ปรับ path ตามที่ใช้งานจริง
pages = convert_from_path('barcode_tube.pdf', 300, poppler_path=r'C:\poppler-24.08.0\Library\bin')
reader = easyocr.Reader(['th', 'en'], gpu=False)

data = []

for i, page in enumerate(pages):
    print(f'\n=== หน้า {i+1} ===')
    img_path = os.path.join(output_dir, f'page_{i+1}.png')
    page.save(img_path, 'PNG')
    img_cv = np.array(page)
    img_cv = cv2.cvtColor(img_cv, cv2.COLOR_RGB2BGR)

    # OCR ทั้งหน้า
    results = reader.readtext(img_cv)
    texts = [(text, conf) for _, text, conf in results if conf > 0.3]
    
    name = ""
    lab_source = ""
    specimen_note = ""

    # ดึง name, lab_source, specimen_note
    for text, conf in texts:
        if not name and (("นาย" in text or "mr." in text.lower()) and len(text) > 6):
            name = text
        elif not lab_source and ("โรงพยาบาล" in text or "hospital" in text.lower()):
            lab_source = text
        elif not specimen_note and ("hb typing" in text.lower() or "note" in text.lower()):
            specimen_note = text

    if not specimen_note:
        for text, conf in texts:
            if conf > 0.5 and all(ord(c) < 128 for c in text):
                specimen_note = text
                break

    # barcode, date, specimen_type (แนวตั้ง)
    if i == 0:
        barcode = ocr_barcode_vertical(img_cv, x1=20, y1=30, x2=45, y2=300, angle=90, show_img=True)
        date_spec = ocr_vertical_date_specimen(img_cv, x1=500, y1=20, x2=600, y2=360, angle=90)
    else:
        barcode = ocr_barcode_vertical(img_cv, x1=20, y1=30, x2=45, y2=300, angle=90, show_img=True)
        date_spec = ocr_vertical_date_specimen(img_cv, x1=500, y1=20, x2=600, y2=360, angle=90)

    date_raw = date_spec[0] if len(date_spec) > 0 else ""
    specimen_raw = date_spec[1] if len(date_spec) > 1 else ""
    date_clean = date_raw.replace(']un', 'Jun').replace(')un', 'Jun').replace(']an', 'Jan')
    specimen_clean = specimen_raw.strip().capitalize()

    # debug barcode
    print(f"หน้า {i+1}: barcode = {barcode}")

    data.append({
        "name": name,
        "lab_source": lab_source,
        "specimen_note": specimen_note,
        "date": date_clean,
        "specimen_type": specimen_clean,
        "barcode": barcode
    })

with open('output_custom.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("บันทึกผลลัพธ์: output_custom.json")
