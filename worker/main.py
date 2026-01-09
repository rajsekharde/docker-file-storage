import redis
from pathlib import Path
import shutil
from PIL import Image

r = redis.Redis(host="redis", port=6379, decode_responses=True)

BASE = Path("/data")
UPLOADS = BASE / "uploads"
RESULTS = BASE / "results"

UPLOADS.mkdir(exist_ok=True)
RESULTS.mkdir(exist_ok=True)

print("Worker started...")

while True:
    job_id = r.brpop("jobs")[1]

    input_dir = UPLOADS / job_id
    output_dir = RESULTS / job_id
    output_dir.mkdir(parents=True, exist_ok=True)

    files = [p for p in input_dir.iterdir() if p.is_file()]
    if not files:
        print("No files for job:", job_id)
        continue

    src = files[0]
    new_name = f"processed_{src.name}"
    dest = output_dir / new_name

    shutil.copy2(src, dest)

    print(f"Job {job_id} -> created {dest.name}")
