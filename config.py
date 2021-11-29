import os


base_dir = os.getcwd()
upload_dir = os.path.join(base_dir, 'uploads')


if not os.path.isdir(upload_dir):
    os.mkdir(upload_dir)


class Config:
    # Allow 16mb
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    UPLOAD_DIR = upload_dir
    ALLOWED_EXTS = set(['pdf', 'png', 'jpg', 'jpeg'])