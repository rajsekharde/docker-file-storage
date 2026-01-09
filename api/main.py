from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import shutil
import uuid
import redis
from fastapi.responses import FileResponse

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
RESULTS = BASE_DIR / "results"

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

@app.get("/status/{job_id}")
def job_status(job_id: str):
    result_dir = Path("/data/results") / job_id
    upload_dir = Path("/data/uploads") / job_id

    if result_dir.exists():
        files = [f.name for f in result_dir.iterdir() if f.is_file()]
        return {"status": "done", "files": files}

    if upload_dir.exists():
        return {"status": "processing"}

    return {"status": "unknown"}


@app.get("/download/{job_id}/{filename}")
def download_file(job_id: str, filename: str):
    file_path = RESULTS / job_id / filename

    if not file_path.exists() or not file_path.is_file():
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(
        path=file_path,
        filename=filename,
        media_type="application/octet-stream"
    )


# 

'''
UploadFile- Streams files instead of loading into RAM
FileResponse- Streams files back to users
Path- safe file paths
shutil- copy streams of bytes

BASE_DIR = Path("/data")- File system root
/data inside containers == file-storage/ on the host



'''