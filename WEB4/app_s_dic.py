import datetime
from pathlib import Path
import re
import threading
import concurrent.futures



FOLDERS = []
UNKNOWN = set()
EXTENSIONS = set()

DESTINATIONS = {
    "Images": [],
    "Audio": [],
    "Video": [],
    "Documents": [],
    "Archives": [],
    "Other": []
}

REGISTERED_EXTENSIONS = {
    'JPEG': DESTINATIONS['Images'],
    'PNG': DESTINATIONS['Images'],
    'JPG': DESTINATIONS['Images'],
    'SVG': DESTINATIONS['Images'],
    'AVI': DESTINATIONS['Video'],
    'MP4': DESTINATIONS['Video'],
    'MOV': DESTINATIONS['Video'],
    'MKV': DESTINATIONS['Video'],
    'DOC': DESTINATIONS['Documents'],
    'DOCX': DESTINATIONS['Documents'],
    'TXT': DESTINATIONS['Documents'],
    'PDF': DESTINATIONS['Documents'],
    'XLSX': DESTINATIONS['Documents'],
    'PPTX': DESTINATIONS['Documents'],
    'DJVU': DESTINATIONS['Documents'],
    'DJV': DESTINATIONS['Documents'],
    'MP3': DESTINATIONS['Audio'],
    'OGG': DESTINATIONS['Audio'],
    'WAV': DESTINATIONS['Audio'],
    'AMR': DESTINATIONS['Audio'],
    'FLAC': DESTINATIONS['Audio'],
    'AAC': DESTINATIONS['Audio'],
    'ZIP': DESTINATIONS['Archives'],
    'GZ': DESTINATIONS['Archives'],
    'TAR': DESTINATIONS['Archives']
}


def get_extensions(file_name) -> str:
    return Path(file_name).suffix[1:].upper()


def scan(folder: Path): #added extra thread for scan of inner folders using Thread and Rlock in part of writing results
        lock_obj = threading.RLock()
        for item in folder.iterdir():
            if item.is_dir():
                if item.name not in ('Images', 'Audio', 'Video', 'Documents', 'Archives'):
                    FOLDERS.append(item)
                    t1 = threading.Thread(target=scan, args=(item,))
                    t1.start()
                continue
            lock_obj.acquire()
            extension = get_extensions(item.name)
            new_name = folder / item.name
            if not extension:
                DESTINATIONS['Other'].append(new_name)
            else:
                try:
                    REGISTERED_EXTENSIONS[extension].append(new_name)
                    EXTENSIONS.add(extension)

                except KeyError:
                    UNKNOWN.add(extension)
                    DESTINATIONS['Other'].append(new_name)
            lock_obj.release()


table = {ord('а'): 'a', ord('б'): 'b', ord(
    'в'): 'v', ord('г'): 'h', ord('ґ'): 'g',
    ord('д'): 'd', ord('е'): 'e', ord('є'): 'ie',
    ord('ж'): 'zh', ord('з'): 'z', ord('и'): 'y',
    ord('і'): 'i', ord('ї'): 'i', ord('й'): 'i',
    ord('к'): 'k', ord('л'): 'l', ord('м'): 'm',
    ord('н'): 'n', ord('о'): 'o', ord('п'): 'p',
    ord('р'): 'r', ord('с'): 's', ord('т'): 't',
    ord('у'): 'u', ord('ф'): 'f', ord('х'): 'kh',
    ord('ц'): 'ts', ord('ч'): 'ch', ord('ш'): 'sh',
    ord('щ'): 'shch', ord('ю'): 'iu', ord('я'): 'ia',
    ord('А'): 'A', ord('Б'): 'B', ord(
    'В'): 'V', ord('Г'): 'H', ord('Ґ'): 'G',
    ord('Д'): 'D', ord('Е'): 'E', ord('Є'): 'Ye',
    ord('Ж'): 'Zh', ord('З'): 'Z', ord('И'): 'Y',
    ord('І'): 'I', ord('Ї'): 'Yi', ord('Й'): 'Y',
    ord('К'): 'K', ord('Л'): 'L', ord('М'): 'M',
    ord('Н'): 'N', ord('О'): 'O', ord('П'): 'P',
    ord('Р'): 'R', ord('С'): 'S', ord('Т'): 'T',
    ord('У'): 'U', ord('Ф'): 'F', ord('Х'): 'Kh',
    ord('Ц'): 'Ts', ord('Ч'): 'Ch', ord('Ш'): 'Sh',
    ord('Щ'): 'Shch', ord('Ю'): 'Yu', ord('Я'): 'Ya',
    ord('ь'): '', ord('’'): ''}


def normalize(text):

    text = text.translate(table)
    clean_text = re.sub(r'[^\w\s]', '_', text)
    text = clean_text
    return text


def file_transition(file: Path, root_folder: Path, dist: str):
    target_folder = root_folder / dist
    target_folder.mkdir(exist_ok=True)
    ext = Path(file).suffix
    new_name = normalize(file.name.replace(ext, '')) + ext
    file.replace(target_folder / new_name)


def delete_folder(folder: Path):
    f = False
    while not f:
        try:
            folder.rmdir()
            f = True
        except OSError:
            f = False


def delete_folder_sem(folder: Path, s):
    s.acquire()
    f = False
    while not f:
        try:
            folder.rmdir()
            f = True
        except OSError:
            f = False
    s.release()


def main_pool(folder, mw=7):
    folder = Path(folder)
    scan(folder)
    with concurrent.futures.ThreadPoolExecutor(max_workers=mw) as executor: #MT using pool
        for key, value in DESTINATIONS.items():
            for file in value:
                executor.submit(file_transition, file, folder, key)
        for f in FOLDERS:
            executor.submit(delete_folder, f)


def main_sem(folder, sn=10):
    s = threading.Semaphore(sn)
    folder = Path(folder)
    scan(folder)
    for key, value in DESTINATIONS.items():
        for file in value:
            t = threading.Thread(target=file_transition_sem, args=(file, folder, key, s))
            t.start()
    for f in FOLDERS:
        t2 = threading.Thread(target=delete_folder_sem, args=(f, s))
        t2.start()



def file_transition_sem(file: Path, root_folder: Path, dist: str, s):
    s.acquire()
    target_folder = root_folder / dist
    target_folder.mkdir(exist_ok=True)
    ext = Path(file).suffix
    new_name = normalize(file.name.replace(ext, '')) + ext
    file.replace(target_folder / new_name)
    s.release()


if __name__ == '__main__':
    print("*** Welcome to multithreading sorter app! ***\n")
    while True:
        switcher = input("Choose multithreading mode:\n- pool(p)\n- semaphore(s)\n>>> ").lower()
        if switcher == 'p':
            mw = None
            while mw is None:
                answer = input("Do you want to change number of threads (y) or use default settings (n)?\n>>> ").lower()
                if answer == "y":
                    while not mw:
                        try:
                            mw = int(input("Enter number of threads.\n>>> "))
                        except ValueError:
                            print("Value error. Use integer and try again!")
                elif answer == "n":
                    mw = 7
                else:
                    print("Your answer should be 'y' or 'n'!")
            input_arg = input('===============================\nEnter the directory for sorting\n>>>  ')
            time1 = datetime.datetime.now()
            sort_folder = Path(input_arg)
            print(f"-------------------------------\nSorting has been started with {mw} threads...")
            main_pool(sort_folder, mw)
            print("Sorting is completed!")
            print(f"Sorting process took {datetime.datetime.now() - time1} seconds.\nGood buy!")
            break
        elif switcher == 's':
            sn = None
            while sn is None:
                answer = input(
                    "Do you want to change number of threads (y) or use default settings (n)?\n>>> ").lower()
                if answer == "y":
                    while not sn:
                        try:
                            sn = int(input("Enter number of threads.\n>>> "))
                        except ValueError:
                            print("Value error. Use integer and try again!")
                elif answer == "n":
                    sn = 7
                else:
                    print("Your answer should be 'y' or 'n'!")
            input_arg = input('===============================\nEnter the directory for sorting\n>>>  ')
            time1 = datetime.datetime.now()
            sort_folder = Path(input_arg)
            print(f"-------------------------------\nSorting has been started with {sn} threads...")
            main_sem(sort_folder, sn)
            print("Sorting is completed!")
            print(f"Sorting process took {datetime.datetime.now() - time1} seconds.\nGood buy!")
            break
        else:
            print('Value error. You should enter "p" for pool-mode or "s" for semaphore-mode. Please try again..')