import os
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from config import Config

app = Flask(__name__)
app.secret_key = "asupersecretsecret"
app.config.from_object(Config)


def file_allowed(filename):
    return "." in filename and \
        filename.rsplit(".", 1)[-1].lower() in app.config.get("ALLOWED_EXTS")


@app.route("/")
def index():
    return "File server running..."


@app.route("/", methods=["POST"])
def file_handler():
    if "file" not in request.files:
        return jsonify(msg="file not present", data=None), 400

    attached_file = request.files.get("file")
    if not attached_file:
        return jsonify(msg="No file attached", data=None), 400

    if not file_allowed(attached_file.filename):
        return jsonify(msg="Invalid file type", data=None), 400

    filename = secure_filename(attached_file.filename)
    print(attached_file.content_length)
    attached_file.save(os.path.join(app.config.get("UPLOAD_DIR"), filename))

    return jsonify(msg="File received", data=None)


@app.route("/multi", methods=["POST"])
def multi_file_handler():
    if "files" not in request.files:
        return jsonify(msg="files not present", data=None), 400

    attached_files = request.files.getlist("files")
    if not attached_files[0]:
        return jsonify(msg="files not present", data=None), 400

    for file in attached_files:
        if not file_allowed(file.filename):
            return jsonify(msg="An invalid file type was sent", data=None), 400

    for file in attached_files:
        file.save(os.path.join(app.config.get("UPLOAD_DIR"), file.filename))

    return jsonify(msg="File received", data=None)


@app.errorhandler(413)
def content_too_long(e):
    return jsonify(msg="File too large", data=None), 413


if __name__ == "__main__":
    app.run(port=5000, debug=True)
