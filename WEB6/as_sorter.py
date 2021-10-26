import datetime
from aiopath import AsyncPath
import re
from pathlib import Path
import asyncio
import logging
import collections

logging.basicConfig(level=logging.DEBUG, filename='log.txt', filemode='a', format='[%(asctime)s] - %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S')

FOLDERS = []
UNKNOWN = set()
EXTENSIONS = set()

# class AsyncDict(dict, collections.AsyncIterable):
#     pass


# DESTINATIONS_AS = AsyncDict()



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


def scan(folder: Path):
    for item in folder.iterdir():
        if item.is_dir():
            if item.name not in ('Images', 'Audio', 'Video', 'Documents', 'Archives'):
                FOLDERS.append(item)
                scan(item)
            continue
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



# async def scan_as(folder: Path):
#     a_folder = AsyncPath(folder)
#     async for item in a_folder.iterdir():
#         if item.is_dir():
#             if item.name not in ('Images', 'Audio', 'Video', 'Documents', 'Archives'):
#                 FOLDERS_AS.append(item)
#                 await scan_as(item)
#             continue
#         extension = get_extensions(item.name)
#         new_name = a_folder / item.name
#         if not extension:
#             DESTINATIONS['Other'].append(new_name)
#         else:
#             try:
#                 REGISTERED_EXTENSIONS[extension].append(new_name)
#                 EXTENSIONS.add(extension)
#
#             except KeyError:
#                 UNKNOWN.add(extension)
#                 DESTINATIONS['Other'].append(new_name)



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


def error_handler(func):
    def inner(*args):
        try:
            func(*args)
        except FileNotFoundError:
            print("File not found")
        except OSError:
            print(f"Deleting folder error.")

    return inner


def error_handler_as(func):
    async def inner(*args):
        try:
            await func(*args)
        except FileNotFoundError:
            print("File not found")
        except OSError:
            print(f"Deleting folder error.")

    return inner


def normalize(text):
    text = text.translate(table)
    clean_text = re.sub(r'[^\w\s]', '_', text)
    text = clean_text
    return text


@error_handler
def file_transition(file: Path, root_folder: Path, dist: str):
    target_folder = root_folder / dist
    target_folder.mkdir(exist_ok=True)
    ext = Path(file).suffix
    new_name = normalize(file.name.replace(ext, '')) + ext
    file.replace(target_folder / new_name)


@error_handler_as
async def file_transition_as(file: Path, root_folder: Path, dist: str):
    a_file = AsyncPath(file)
    a_root_folder = AsyncPath(root_folder)
    target_folder = a_root_folder / dist
    await target_folder.mkdir(exist_ok=True)
    ext = AsyncPath(file).suffix
    new_name = normalize(a_file.name.replace(ext, '')) + ext
    await a_file.replace(target_folder / new_name)


@error_handler
def delete_folder(folder: Path):
    folder.rmdir()


@error_handler_as
async def delete_folder_as(folder: Path):
    a_folder = AsyncPath(folder)
    await a_folder.rmdir()


def mode_wrapper(func):
    def wrapper(*args):
        time = datetime.datetime.now()
        print(f"{'-' * 50}\nSorting has been started...\n{'-' * 50}")
        func(*args)
        print(f"{'-' * 50}\nSorting is completed!\n{'=' * 50}")
        print(f"The sorting process took {datetime.datetime.now() - time} seconds.\nGood buy!")
        logging.debug(
            f"{str(sort_folder)}, mode = asynchronic-task, time = {datetime.datetime.now() - time} seconds")
    return wrapper


@mode_wrapper
def main_sync(folder):
    scan(folder)
    for key, value in DESTINATIONS.items():
        for file in value:
            file_transition(file, folder, key)
    FOLDERS.reverse()
    for f in FOLDERS:
        delete_folder(f)


def mode_wrapper_as(func):
    async def wrapper(*args):
        time = datetime.datetime.now()
        print(f"{'-' * 50}\nSorting has been started...\n{'-' * 50}")
        await func(*args)
        print(f"{'-' * 50}\nSorting is completed!\n{'=' * 50}")
        print(f"The sorting process took {datetime.datetime.now() - time} seconds.\nGood buy!")
        logging.debug(
            f"{str(sort_folder)}, mode = asynchronic-task, time = {datetime.datetime.now() - time} seconds")
    return wrapper


@mode_wrapper_as
async def main_async_task(folder):
    scan(folder)
    tasks = []
    for key, value in DESTINATIONS.items():
        for file in value:
            task_name = file.name[:-4]
            tasks.append(asyncio.create_task(file_transition_as(file, folder, key), name=task_name))

    done, pending = await asyncio.wait(tasks)

    for t in done:
        print(f"{t.get_name():<50} | is replaced")

    FOLDERS.reverse()
    for f in FOLDERS:
        await delete_folder_as(f)

@mode_wrapper_as
async def main_async(folder):
    scan(folder)
    for key, value in DESTINATIONS.items():
        for file in value:
            await file_transition_as(file, folder, key)

    FOLDERS.reverse()
    for f in FOLDERS:
        await delete_folder_as(f)


@mode_wrapper_as
async def main_async_gath(folder):
    scan(folder)
    # for key, value in DESTINATIONS:
    #     DESTINATIONS_AS[key] = value
    await asyncio.gather(*[[file_transition_as(file, folder, key) for file in l] for key, l in DESTINATIONS.items()])

    FOLDERS.reverse()
    for f in FOLDERS:
        await delete_folder_as(f)


if __name__ == '__main__':
    print(f"\n{' ' * 20}*** Welcome to async sorter app! ***\n")
    while True:
        sort_folder = Path(input(f"{'=' * 50}\nEnter the directory for sorting\n>>>  "))
        if str(sort_folder) == ".":
            print("Choose another folder. The app is here")
            continue
        while True:
            mode = input("Choose the sorting mode. Asynchronic (a), asynchronic-task (t), asynchronic-gather (g) or synchronic (s)\n>>> ").lower()
            if mode == "s":
                main_sync(sort_folder)
                break
            elif mode == "t":
                asyncio.run(main_async_task(sort_folder))
                break
            elif mode == "a":
                asyncio.run(main_async(sort_folder))
                break
            elif mode == "g":
                asyncio.run(main_async_gath(sort_folder))
                break
            else:
                print("The answer should be 'a' or 's'. Try again.")
        break
