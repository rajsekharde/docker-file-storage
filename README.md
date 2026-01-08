## Testing upload, download of files from frontend to backend and storing to shared docker volume

## Steps:

Run api, worker, frontend using docker compose

Project structure:

```bash
.
├── api
│   ├── Dockerfile
│   ├── main.py
├── docker-compose.yml
├── frontend
│   ├── Dockerfile
│   ├── index.html
│   ├── script.js
│   └── style.css
├── README.md
├── requirements.txt
└── worker
    ├── Dockerfile
    ├── main.py
├── file-storage # Create this folder
│   ├── downloads
│   └── uploads

```

Add shared volume to services in docker-compose.yml:

```bash
services:
    api:
        volumes:
            - ./file-storage:/data
    worker:
        volumes:
            - ./file-storage:/data
```

Anything api writes to /data will be available to worker and the host