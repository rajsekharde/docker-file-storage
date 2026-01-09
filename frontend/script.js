function log(msg) {
  console.log(msg);
}

// Upload
document.getElementById("uploadBtn").onclick = async () => {
  const file = document.getElementById("fileInput").files[0];
  if (!file) return;

  const formData = new FormData();
  formData.append("file", file);

  const res = await fetch("http://localhost:8000/upload", {
    method: "POST",
    body: formData
  });

  const data = await res.json();
  console.log("UPLOAD:", data);

  watchJob(data.job_id);
};

// Poll Status
async function watchJob(jobId) {
  while (true) {
    await new Promise(r => setTimeout(r, 2000));

    const res = await fetch(`http://localhost:8000/status/${jobId}`);
    const data = await res.json();

    console.log("STATUS:", data);

    if (data.status === "done") {
      log("Job finished.");
      showDownloads(jobId, data.files);
      break;
    }

    log("Status: " + data.status);
  }
}

// Download
function showDownloads(jobId, files) {
  console.log("RENDER FILES:", files);

  const container = document.createElement("div");
  container.innerHTML = "<h3>Results</h3>";

  for (const file of files) {
    const a = document.createElement("a");
    a.href = `http://localhost:8000/download/${jobId}/${encodeURIComponent(file)}`;
    a.textContent = "Download " + file;
    a.download = file;
    a.style.display = "block";
    container.appendChild(a);
  }

  document.body.appendChild(container);
}
