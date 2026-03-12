# utils/file_upload.py
# Helpers for handling paper file uploads safely.

import os
from werkzeug.utils import secure_filename

# Where uploaded files will be stored on disk
UPLOAD_FOLDER   = os.path.join(os.path.dirname(__file__), "..", "uploads")
ALLOWED_EXTENSIONS = {"pdf", "docx", "txt", "md", "png", "jpg", "jpeg"}


def allowed_file(filename: str) -> bool:
    """Return True if the file extension is in the allowed set."""
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )


def save_file(file):
    """
    Save a Werkzeug FileStorage object to UPLOAD_FOLDER.
    Returns the relative path string on success, or None if the file is invalid.
    """
    if file and allowed_file(file.filename):
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        filename  = secure_filename(file.filename)
        save_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(save_path)
        # Store only the relative path so the server can be moved freely
        return os.path.join("uploads", filename)
    return None
