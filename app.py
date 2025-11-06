from flask import Flask, render_template, request, redirect, url_for, flash, session
import os
import cv2
import time
import base64
import numpy as np
from paddleocr import PaddleOCR
from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge
from collections import defaultdict
from htmlmin.main import minify
from io import BytesIO
from mimetypes import guess_type

app = Flask(__name__)
app.secret_key = "secret"
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024
ALLOWED_EXTENSIONS = {'png','jpg','jpeg'}
ocr_engine = PaddleOCR(lang='en', use_angle_cls=True, show_log=False)
def allowed_file(name):
    return '.' in name and name.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS
def preprocess_image_for_ocr(img):
    max_w = 1800
    h, w = img.shape[:2]
    if w < max_w:
        scale = max_w / float(w)
        img = cv2.resize(img, None, fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (3,3), 0)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
    gray = clahe.apply(gray)
    _, th = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return gray, th

@app.after_request
def response_minify(response):
    content_type = response.headers.get("Content-Type", "").lower()
    if content_type.startswith("text/html"):
        try:
            minified = minify(
                response.get_data(as_text=True),
                remove_comments=True,
                remove_empty_space=False,
                reduce_boolean_attributes=True,
            )
            response.set_data(minified)
        except Exception as e:
            print("Minify error:", e)
    return response

@app.route("/", methods=["GET", "POST"])
def index():
    uploaded_file = None
    ocr_data = []
    orig_w = orig_h = None
    full_text = ""
    ocr_texts = []
    mime_type = None

    if request.method == "GET":
        session.pop('_flashes', None)
    if request.method == "POST":
        if 'clear' in request.form:
            flash("Image cleared!", "success")
            return redirect(url_for("index"))

        file = request.files.get("image")
        if file and allowed_file(file.filename):
            try:
                file_bytes = np.frombuffer(file.read(), np.uint8)
                img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
                if img is None:
                    flash("Failed to read image.", "danger")
                    return redirect(url_for("index"))

                orig_h, orig_w = img.shape[:2]
                gray, thresh = preprocess_image_for_ocr(img)

                try:
                    result = ocr_engine.ocr(gray, cls=True)
                except Exception:
                    flash("OCR processing error.", "danger")
                    return redirect(url_for("index"))

                ocr_data = []

                lines_by_y = []

                for line in result:
                    for box, (text, conf) in line:

                        x_min = int(min([p[0] for p in box]))
                        y_min = int(min([p[1] for p in box]))
                        w = int(max([p[0] for p in box]) - x_min)
                        h = int(max([p[1] for p in box]) - y_min)

                        roi = gray[y_min:y_min + h, x_min:x_min + w] if (h > 0 and w > 0) else None
                        brightness = int(roi.mean()) if (roi is not None and roi.size > 0) else 255
                        bg_color = 'light' if brightness < 128 else 'dark'

                        ocr_data.append({
                            'text': text,
                            'x': x_min,
                            'y': y_min,
                            'w': w,
                            'h': h,
                            'bg': bg_color
                        })

                        lines_by_y.append((y_min, x_min, text))

                lines_by_y.sort(key=lambda x: (x[0], x[1]))

                full_text = ""
                current_line = []
                last_y = None

                for y, x, text in lines_by_y:
                    if last_y is None or abs(y - last_y) <= 25:
                        current_line.append(text)
                    else:
                        full_text += " ".join(current_line) + "\n"
                        current_line = [text]
                    last_y = y

                if current_line:
                    full_text += " ".join(current_line)

                ocr_texts = full_text.split()

                ext = file.filename.rsplit('.',1)[1].lower()
                if ext in ['jpg','jpeg']:
                    mime_type = "image/jpeg"
                    encode_ext = ".jpg"
                elif ext == 'png':
                    mime_type = "image/png"
                    encode_ext = ".png"
                else:
                    mime_type = "application/octet-stream"
                    encode_ext = ".png"

                _, buffer = cv2.imencode(encode_ext, img)
                uploaded_file = base64.b64encode(buffer).decode("utf-8")
                flash("Image uploaded & processed successfully!", "success")

            except Exception as e:
                print("ERROR:", e)
                flash("Processing error.", "danger")
                return redirect(url_for("index"))

        else:
            flash("Invalid file format. Use png/jpg/jpeg.", "danger")

    return render_template("index.html",
        uploaded_file=uploaded_file,
        mime_type=mime_type,
        ocr_data=ocr_data,
        ocr_texts=ocr_texts,
        full_text=full_text,
        orig_w=orig_w,
        orig_h=orig_h,
        timestamp=int(time.time())
    )

@app.errorhandler(RequestEntityTooLarge)
def handle_large_file(e):
    flash("File size is too large", "danger")
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=2025, ssl_context=("cert.pem", "key.pem"), debug=True)
