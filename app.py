# from flask import Flask, render_template, request, redirect, url_for, flash
# import os
# import cv2
# import time
# import pytesseract
# from pytesseract import Output
# from paddleocr import PaddleOCR
# from werkzeug.utils import secure_filename
# from werkzeug.exceptions import RequestEntityTooLarge
# from collections import defaultdict
# from htmlmin.main import minify

# app = Flask(__name__)
# app.secret_key = "secret"
# app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024
# UPLOAD_FOLDER = 'static/uploads'
# os.makedirs(UPLOAD_FOLDER, exist_ok=True)
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# ALLOWED_EXTENSIONS = {'png','jpg','jpeg'}
# ocr_engine = PaddleOCR(lang='en', use_angle_cls=True, show_log=False)
# def allowed_file(name):
#     return '.' in name and name.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS
# def cleanup_old_uploads(folder, max_age_seconds=300):
#     now = time.time()
#     for filename in os.listdir(folder):
#         file_path = os.path.join(folder, filename)
#         if os.path.isfile(file_path):
#             file_age = now - os.path.getmtime(file_path)
#             if file_age > max_age_seconds:
#                 try:
#                     os.remove(file_path)
#                 except Exception:
#                     pass
# def preprocess_image_for_ocr(img):
#     max_w = 1800
#     h, w = img.shape[:2]
#     if w < max_w:
#         scale = max_w / float(w)
#         img = cv2.resize(img, None, fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC)
#     gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#     gray = cv2.GaussianBlur(gray, (3,3), 0)
#     clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
#     gray = clahe.apply(gray)
#     _, th = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)    
#     return gray, th
# def reconstruct_text_from_data(data):
#     items_by_line = defaultdict(list)
#     n = len(data['text'])
#     for i in range(n):
#         text = data['text'][i].strip()
#         if not text:
#             continue
#         key = (data['block_num'][i], data['par_num'][i], data['line_num'][i])
#         left = data['left'][i]
#         items_by_line[key].append((left, text))
#     sorted_keys = sorted(items_by_line.keys())
#     lines = []
#     for key in sorted_keys:
#         words = items_by_line[key]
#         words_sorted = [w for _, w in sorted(words, key=lambda x: x[0])]
#         line_text = " ".join(words_sorted)
#         lines.append(line_text)
#     full_text = "\n".join(lines)
#     return lines, full_text
# @app.after_request
# def response_minify(response):
#     content_type = response.headers.get("Content-Type", "").lower()
#     if content_type.startswith("text/html"):
#         try:
#             minified = minify(
#                 response.get_data(as_text=True),
#                 remove_comments=True,
#                 remove_empty_space=False,
#                 reduce_boolean_attributes=True,
#             )
#             response.set_data(minified)
#         except Exception as e :
#             print("Minify error:", e)
#     return response
# @app.route("/", methods=["GET", "POST"])
# def index():
#     cleanup_old_uploads(app.config["UPLOAD_FOLDER"])
#     uploaded_file = None
#     ocr_data = []
#     orig_w = orig_h = None
#     full_text = ""
#     ocr_texts = []
#     data = {'text': []}
#     custom_config = r'--oem 3 --psm 3'
#     if request.method == "POST":
#         if 'clear' in request.form:
#             for f in os.listdir(app.config["UPLOAD_FOLDER"]):
#                 os.remove(os.path.join(app.config["UPLOAD_FOLDER"], f))
#             flash("image deleted successfully!", "success")
#             return redirect(url_for('index'))
#         file = request.files.get("image")
#         if file and allowed_file(file.filename):
#             filename = secure_filename(file.filename)
#             file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
#             file.save(file_path)
#             uploaded_file = filename
#             img = cv2.imread(file_path)
#             if img is None:
#                 flash("Gagal membaca gambar.", "danger")
#             else:
#                 orig_h, orig_w = img.shape[:2]
#                 gray, thresh = preprocess_image_for_ocr(img)
#                 custom_config_3 = r'--oem 3 --psm 3'
#                 data_3 = pytesseract.image_to_data(gray, output_type=Output.DICT, config=custom_config_3)
#                 lines_3, full_text_3 = reconstruct_text_from_data(data_3)
#                 if not full_text_3.strip() or len(full_text_3.split()) < 5 or len(full_text_3.strip()) < 20:
#                     custom_config = r'--oem 3 --psm 11'
#                     data = pytesseract.image_to_data(gray, output_type=Output.DICT, config=custom_config)
#                     lines, full_text = reconstruct_text_from_data(data)     
#                 else:
#                     custom_config = custom_config_3
#                     data = data_3
#                     full_text = full_text_3
#                     lines = lines_3
                  
#                 ocr_data = []
#                 for i in range(len(data['text'])):
#                     text = data['text'][i].strip()
#                     if text:
#                         x, y, w, h = data['left'][i], data['top'][i], data['width'][i], data['height'][i]
#                         roi = gray[y:y+h, x:x+w] if (h>0 and w>0) else None
#                         brightness = int(roi.mean()) if (roi is not None and roi.size>0) else 255
#                         bg_color = 'light' if brightness < 128 else 'dark'
#                         ocr_data.append({'text': text, 'x': int(x), 'y': int(y), 'w': int(w), 'h': int(h), 'bg': bg_color})  
#                 ocr_texts = [w for line in lines for w in line.split()]
#                 pass
#                 try:
#                     log_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{filename}.txt")
#                     with open(log_path, "w", encoding="utf-8") as f:
#                         f.write(full_text + "\n\n")
#                         for it in ocr_data:
#                              f.write(f"{it['text']}\t{it['x']}:{it['y']}:{it['w']}:{it['h']}\n")
#                 except Exception:
#                     pass
#                 flash("Image Success Uploaded!", "success")
#         elif file:
#             flash("Format file tidak diizinkan. Gunakan png/jpg/jpeg.", "danger")
#     return render_template("index.html",
#                            uploaded_file=uploaded_file,
#                            ocr_data=ocr_data,
#                            ocr_texts=ocr_texts,
#                            full_text=full_text,
#                            orig_w=orig_w,
#                            orig_h=orig_h)
# @app.route("/cleanup_temp", methods=["POST"])
# def cleanup_temp():
#     for f in os.listdir(app.config["UPLOAD_FOLDER"]):
#         os.remove(os.path.join(app.config["UPLOAD_FOLDER"], f))
#     return "OK"
# @app.errorhandler(RequestEntityTooLarge)
# def handle_large_file(e):
#     flash("File size is too large", "danger")
#     return redirect(url_for("index"))
# if __name__ == "__main__":
#     app.run(host='0.0.0.0', port=2025, ssl_context=("cert.pem", "key.pem"), debug=True)
from flask import Flask, render_template, request, redirect, url_for, flash
import os
import cv2
import time
from paddleocr import PaddleOCR
from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge
from collections import defaultdict
from htmlmin.main import minify

app = Flask(__name__)
app.secret_key = "secret"
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024
UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'png','jpg','jpeg'}
ocr_engine = PaddleOCR(lang='en', use_angle_cls=True, show_log=False)
def allowed_file(name):
    return '.' in name and name.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS
def cleanup_old_uploads(folder, max_age_seconds=300):
    now = time.time()
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        if os.path.isfile(file_path):
            file_age = now - os.path.getmtime(file_path)
            if file_age > max_age_seconds:
                try:
                    os.remove(file_path)
                except Exception:
                    pass
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
    cleanup_old_uploads(app.config["UPLOAD_FOLDER"])

    uploaded_file = None
    ocr_data = []
    orig_w = orig_h = None
    full_text = ""
    ocr_texts = []

    if request.method == "POST":

        if 'clear' in request.form:
            for f in os.listdir(app.config["UPLOAD_FOLDER"]):
                os.remove(os.path.join(app.config["UPLOAD_FOLDER"], f))
            flash("image deleted successfully!", "success")
            return redirect(url_for('index'))

        file = request.files.get("image")
        if file and allowed_file(file.filename):
            ext = file.filename.rsplit('.',1)[1].lower()
            filename = f"{int(time.time())}_{os.urandom(4).hex()}.{ext}"
            file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(file_path)
            # time.sleep(0.1)
            uploaded_file = filename

            img = cv2.imread(file_path)
            if img is None:
                flash("Gagal membaca gambar.", "danger")
            else:
                orig_h, orig_w = img.shape[:2]
                gray, thresh = preprocess_image_for_ocr(img)

                try:
                    result = ocr_engine.ocr(gray, cls=True)
                except Exception as e:
                    flash("OCR processing error.", "danger")
                    return redirect(url_for('index'))

                lines = []
                full_text = ""
                ocr_data = []

                for line in result:
                    for box, (text, conf) in line:

                        lines.append(text)
                        full_text += text + " "

                        x_min = int(min([p[0] for p in box]))
                        y_min = int(min([p[1] for p in box]))
                        w = int(max([p[0] for p in box]) - x_min)
                        h = int(max([p[1] for p in box]) - y_min)

                        roi = gray[y_min:y_min+h, x_min:x_min+w] if (h>0 and w>0) else None
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

                ocr_texts = full_text.split()

                try:
                    log_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{filename}.txt")
                    with open(log_path, "w", encoding="utf-8") as f:
                        f.write(full_text + "\n\n")
                        for it in ocr_data:
                            f.write(f"{it['text']}\t{it['x']}:{it['y']}:{it['w']}:{it['h']}\n")
                except:
                    pass

                flash("Image Success Uploaded!", "success")
        elif file:
            flash("Format file tidak diizinkan. Gunakan png/jpg/jpeg.", "danger")
    return render_template("index.html",
        uploaded_file=uploaded_file,
        ocr_data=ocr_data,
        ocr_texts=ocr_texts,
        full_text=full_text,
        orig_w=orig_w,
        orig_h=orig_h,
        timestamp=int(time.time())
    )

@app.route("/cleanup_temp", methods=["POST"])
def cleanup_temp():
    for f in os.listdir(app.config["UPLOAD_FOLDER"]):
        os.remove(os.path.join(app.config["UPLOAD_FOLDER"], f))
    return "OK"

@app.errorhandler(RequestEntityTooLarge)
def handle_large_file(e):
    flash("File size is too large", "danger")
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=2025, ssl_context=("cert.pem", "key.pem"), debug=True)
