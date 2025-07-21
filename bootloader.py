import os

from unyx import FS

def bootloader():
    images : list[str] = list(filter(lambda s: s.endswith('.unyx'), os.listdir('instances')))
    for i, image in enumerate(images):
        print(f"{i}: {image}")
    choice = int(input("Select an image to boot: "))
    if 0 <= choice < len(images):
        fs = FS.FS(f"instances/{images[choice]}")
        fs.REPL()

if __name__ == "__main__":
    bootloader()