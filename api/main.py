from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import shutil
import uuid
import redis

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

r = redis.Redis(host="redis", port=6379, decode_responses=True)


@app.get("/")
def root():
    return {"Message": "Hello"}


BASE_DIR = Path("/data")
UPLOADS = BASE_DIR / "uploads"

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(status_code=400, detail="No filename")

    job_id = str(uuid.uuid4())
    job_dir = UPLOADS / job_id
    job_dir.mkdir(parents=True, exist_ok=True)

    safe_name = f"{uuid.uuid4()}_{Path(file.filename).name}"
    dest = job_dir / safe_name

    with dest.open("wb") as f:
        shutil.copyfileobj(file.file, f)

    # enqueue only after write completes
    r.lpush("jobs", job_id)

    return {"job_id": job_id, "file": safe_name}