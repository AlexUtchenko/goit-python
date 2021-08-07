import re
import sys
from pathlib import Path
import shutil

CYRILLIC_SYMBOLS = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ'
TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "e", "u", "ja")

TRANS = {}

AUDIO = []
VIDEO = []
IMAGES = []
DOCUMENTS = []
ARCHIVES = []
FOLDERS = []

REGISTERED_EXTENSIONS = {
    "MP4": VIDEO,
    "JPG": IMAGES,
    "ZIP": ARCHIVES,
    "PDF": DOCUMENTS,
    "DOC": DOCUMENTS,
    "DOCX": DOCUMENTS,
    "MP3": AUDIO,
}

for cs, trl in zip(CYRILLIC_SYMBOLS, TRANSLATION):
    TRANS[ord(cs)] = trl
    TRANS[ord(cs.upper())] = trl.upper()


def normalize(name: str) -> str:
    trl_name = name.translate(TRANS)
    trl_name = re.sub(r"\W", "_", trl_name)
    return trl_name


def get_extension(file_name) -> str:
    return Path(file_name).suffix[1:].upper()


def scan(folder: Path):
    for item in folder.iterdir():
        if item.is_dir():
            if item.name not in ("VIDEO", "IMAGES", "ARCHIVES", "DOCUMENTS", "AUDIO"):
                FOLDERS.append(item)
                scan(item)
            continue
        else:
            extension = get_extension(item.name)
            new_name = folder / item.name
            try:
                current_container = REGISTERED_EXTENSIONS[extension]
                current_container.append(new_name)
            except KeyError:
                print(f"Unknown file type {new_name}")


def handle_file(file: Path, root_folder: Path, dist: str):
    target_folder = root_folder / dist
    target_folder.mkdir(exist_ok=True)
    ext = Path(file).suffix
    new_name = normalize(file.name.replace(ext, "")) + ext
    file.replace(target_folder / new_name)


def handle_other(file, root_folder, dist):
    target_folder = root_folder / dist
    target_folder.mkdir(exist_ok=True)
    ext = Path(file).suffix
    new_name = normalize(file.name.replace(ext, "")) + ext
    file.replace(target_folder / new_name)


def handle_archive(file: Path, root_folder: Path, dist):
    target_folder = root_folder / dist
    target_folder.mkdir(exist_ok=True)  # create folder ARCH
    ext = Path(file).suffix
    folder_for_arch = normalize(file.name.replace(ext, ""))
    archive_folder = target_folder / folder_for_arch
    archive_folder.mkdir(exist_ok=True)  # create folder ARCH/name_archives
    try:
        shutil.unpack_archive(str(file.resolve()), str(archive_folder.resolve()))
    except shutil.ReadError:
        archive_folder.rmdir()  # Если не успешно удаляем папку под  архив
        return
    file.unlink()  # Если успешно удаляем архив


def handle_folder(folder: Path):
    try:
        folder.rmdir()
    except OSError:
        print(f"Не удалось удалить папку {folder}")


def main(folder):
    scan(folder)

    for file in IMAGES:
        handle_file(file, folder, "IMAGES")

    for file in AUDIO:
        handle_file(file, folder, "AUDIO")

    for file in DOCUMENTS:
        handle_file(file, folder, "DOCUMENTS")

    for file in VIDEO:
        handle_file(file, folder, "VIDEO")

    for file in ARCHIVES:
        handle_archive(file, folder, "ARCHIVES")

    for f in FOLDERS:
        handle_folder(f)


if __name__ == "__main__":
    scan_path = sys.argv[1]
    print(f"Start in folder {scan_path}")

    sort_folder = Path(scan_path)
    print(sort_folder)
    print(sort_folder.resolve())
    main(sort_folder.resolve())