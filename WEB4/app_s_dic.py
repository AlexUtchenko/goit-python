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


table = {ord('??'): 'a', ord('??'): 'b', ord(
    '??'): 'v', ord('??'): 'h', ord('??'): 'g',
    ord('??'): 'd', ord('??'): 'e', ord('??'): 'ie',
    ord('??'): 'zh', ord('??'): 'z', ord('??'): 'y',
    ord('??'): 'i', ord('??'): 'i', ord('??'): 'i',
    ord('??'): 'k', ord('??'): 'l', ord('??'): 'm',
    ord('??'): 'n', ord('??'): 'o', ord('??'): 'p',
    ord('??'): 'r', ord('??'): 's', ord('??'): 't',
    ord('??'): 'u', ord('??'): 'f', ord('??'): 'kh',
    ord('??'): 'ts', ord('??'): 'ch', ord('??'): 'sh',
    ord('??'): 'shch', ord('??'): 'iu', ord('??'): 'ia',
    ord('??'): 'A', ord('??'): 'B', ord(
    '??'): 'V', ord('??'): 'H', ord('??'): 'G',
    ord('??'): 'D', ord('??'): 'E', ord('??'): 'Ye',
    ord('??'): 'Zh', ord('??'): 'Z', ord('??'): 'Y',
    ord('??'): 'I', ord('??'): 'Yi', ord('??'): 'Y',
    ord('??'): 'K', ord('??'): 'L', ord('??'): 'M',
    ord('??'): 'N', ord('??'): 'O', ord('??'): 'P',
    ord('??'): 'R', ord('??'): 'S', ord('??'): 'T',
    ord('??'): 'U', ord('??'): 'F', ord('??'): 'Kh',
    ord('??'): 'Ts', ord('??'): 'Ch', ord('??'): 'Sh',
    ord('??'): 'Shch', ord('??'): 'Yu', ord('??'): 'Ya',
    ord('??'): '', ord('???'): ''}


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


def main_sem(folder, sn=5):
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

def interface():
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
                            return switcher,mw
                        except ValueError:
                            print("Value error. Use integer and try again!")
                elif answer == "n":
                    mw = 7
                    return switcher, mw
                else:
                    print("Your answer should be 'y' or 'n'!")
                    continue
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
                            return switcher,sn
                        except ValueError:
                            print("Value error. Use integer and try again!")
                elif answer == "n":
                    sn = 7
                    return switcher,sn
                else:
                    print("Your answer should be 'y' or 'n'!")
                    continue
            break
        else:
            print('Value error. You should enter "p" for pool-mode or "s" for semaphore-mode. Please try again..')

if __name__ == '__main__':
    print("*** Welcome to multithreading sorter app! ***\n")
    mode, threads = interface()
    input_arg = input('===============================\nEnter the directory for sorting\n>>>  ')
    time1 = datetime.datetime.now()
    sort_folder = Path(input_arg)
    print(f"-------------------------------\nSorting has been started with {threads} threads...")
    if mode == "p":
        main_pool(sort_folder, threads)
        print("Sorting is completed!")
        print(f"Sorting process took {datetime.datetime.now() - time1} seconds.\nGood buy!")
    elif mode == "s":
        main_sem(sort_folder, threads)
        print("Sorting is completed!")
        print(f"Sorting process took {datetime.datetime.now() - time1} seconds.\nGood buy!")
    else:
        print("Interface error. Please contact the developers")


