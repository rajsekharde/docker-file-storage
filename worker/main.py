import redis
from pathlib import Path

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

    print("Processing job:", job_id)
    print("Input files:", [p.name for p in input_dir.iterdir() if p.is_file()])

    # do real work here
