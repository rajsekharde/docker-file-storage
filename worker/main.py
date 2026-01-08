import time
from pathlib import Path

print("Worker started..")

BASE_DIR = Path("/data")

while(True):
    for file in BASE_DIR.iterdir():
        if file.is_file():
            print("Worker sees:", file.name)
    time.sleep(5)