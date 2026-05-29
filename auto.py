from os import scandir, rename 
from shutil import move 
from time import sleep
from pathlib import Path
from os.path import splitext, exists, join
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from mutagen import File

# ── Directories ──────────────────────────────────────────────

source_dir         = r"C:\Users\Oisaa\Downloads"
dest_dir_sfx       = r"C:\Users\Oisaa\Downloads\SOUND"
dest_dir_music     = r"C:\Users\Oisaa\Downloads\MUSIC"
dest_dir_video     = r"C:\Users\Oisaa\Downloads\VIDEO"
dest_dir_image     = r"C:\Users\Oisaa\Downloads\IMAGES"
dest_dir_documents = r"C:\Users\Oisaa\Downloads\DOCUMENTS"

# Create destination folders if they don't exist
Path(dest_dir_sfx).mkdir(exist_ok=True)
Path(dest_dir_music).mkdir(exist_ok=True)
Path(dest_dir_video).mkdir(exist_ok=True)
Path(dest_dir_image).mkdir(exist_ok=True)
Path(dest_dir_documents).mkdir(exist_ok=True)

# ── Supported extensions ─────────────────────────────────────

image_extensions = [".jpg", ".jpeg", ".jpe", ".jif", ".jfif", ".jfi", ".png", ".gif", ".webp", ".tiff", ".tif", ".psd", ".raw", ".arw", ".cr2", ".nrw",
                    ".k25", ".bmp", ".dib", ".heif", ".heic", ".ind", ".indd", ".indt", ".jp2", ".j2k", ".jpf", ".jpf", ".jpx", ".jpm", ".mj2", ".svg", ".svgz", ".ai", ".eps", ".ico"]

video_extensions = [".webm", ".mpg", ".mp2", ".mpeg", ".mpe", ".mpv", ".ogg",
                    ".mp4", ".mp4v", ".m4v", ".avi", ".wmv", ".mov", ".qt", ".flv", ".swf", ".avchd"]

audio_extensions = [".m4a", ".flac", ".mp3", ".wav", ".wma", ".aac"]

document_extensions = [".doc", ".docx", ".odt",
                       ".pdf", ".xls", ".xlsx", ".ppt", ".pptx"]


def make_unique(dest, name):
    """Generate a unique name if a file with the same name already exists in the destination."""
    filename, extension = splitext(name)
    counter = 1

    while exists(f"{dest}/{name}"):
        name = f"{filename}({str(counter)}){extension}"
        counter += 1

    return name


def move_file(dest, entry, name):
    """Move the file to the destination. If a file with the same name already exists, rename the existing one before moving."""
    if exists(f"{dest}/{name}"):
        unique_name = make_unique(dest, name)
        oldName = join(dest, name)
        newName = join(dest, unique_name)
        rename(oldName, newName)
    move(entry, dest)


class MoverHandler(FileSystemEventHandler):
    """Folder watcher. Triggers on every change detected by watchdog."""

    def on_modified(self, event):
        """Scan source_dir and classify each file when a change is detected."""
        with scandir(source_dir) as entries:
            for entry in entries:
                name = entry.name
                self.check_audio_files(entry, name)
                self.check_video_files(entry, name)
                self.check_image_files(entry, name)
                self.check_document_files(entry, name)

    def check_audio_files(self, entry, name):
        """Classify audio files. Uses mutagen duration to separate SFX (under 30s) from music."""
        for audio_extension in audio_extensions:
            if name.endswith(audio_extension) or name.endswith(audio_extension.upper()):
                audio = File(entry.path)
                if audio and audio.info.length < 30:  # under 30 seconds = SFX
                    dest = dest_dir_sfx
                else:
                    dest = dest_dir_music
                move_file(dest, entry, name)
                logging.info(f"Moved audio file: {name}")

    def check_video_files(self, entry, name):
        """Move video files to dest_dir_video."""
        for video_extension in video_extensions:
            if name.endswith(video_extension) or name.endswith(video_extension.upper()):
                move_file(dest_dir_video, entry, name)
                logging.info(f"Moved video file: {name}")

    def check_image_files(self, entry, name):
        """Move image files to dest_dir_image."""
        for image_extension in image_extensions:
            if name.endswith(image_extension) or name.endswith(image_extension.upper()):
                move_file(dest_dir_image, entry, name)
                logging.info(f"Moved image file: {name}")

    def check_document_files(self, entry, name):
        """Move document files to dest_dir_documents."""
        if not dest_dir_documents:  # skip if destination is not defined
            return
        for documents_extension in document_extensions:
            if name.endswith(documents_extension) or name.endswith(documents_extension.upper()):
                move_file(dest_dir_documents, entry, name)
                logging.info(f"Moved document file: {name}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    path = source_dir
    event_handler = MoverHandler()
    observer = Observer()
    # watch source_dir for any file system changes
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        # keep the script running until interrupted
        while observer.is_alive():
            observer.join(1)
    finally:
        observer.stop()
        observer.join()