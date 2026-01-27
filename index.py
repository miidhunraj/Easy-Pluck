from flask import Flask, render_template, request, send_file, redirect, url_for, jsonify, after_this_request
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Use absolute path to ensure it works on cloud hosting like PythonAnywhere
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/")
def index():
    files = os.listdir(UPLOAD_FOLDER)
    return render_template("body-Struct.html", files=files)

@app.route("/upload", methods=["POST"])
def upload():
    if "file" not in request.files:
        return redirect("/")
    file = request.files["file"]
    if file.filename == "":
        return redirect("/")
    filename = secure_filename(file.filename)
    file.save(os.path.join(UPLOAD_FOLDER, filename))
    return redirect("/")

@app.route("/view/<filename>")
def view_file(filename):
    path = os.path.join(UPLOAD_FOLDER, filename)
    return send_file(path, as_attachment=False)

@app.route("/download/<filename>")
def download_file(filename):
    burn = request.args.get("burn")
    path = os.path.join(UPLOAD_FOLDER, filename)
    @after_this_request
    def burn_after(response):
        if burn == "true":
            try:
                os.remove(path)
            except:
                pass
        return response
    return send_file(path, as_attachment=True)

@app.route("/wipe", methods=["POST"])
def wipe():
    for f in os.listdir(UPLOAD_FOLDER):
        try:
            os.remove(os.path.join(UPLOAD_FOLDER, f))
        except:
            pass
    return jsonify({"message": "All files wiped successfully"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7777, debug=True)
    
