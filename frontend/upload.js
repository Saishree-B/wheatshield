// upload.js — Single-page upload + prediction + Grad-CAM (Flask backend)

requireAuth();

const API_BASE = "http://127.0.0.1:5000";

// --------------------
// DOM ELEMENTS
// --------------------
const fileInput = document.getElementById("file-input");
const pickBtn = document.getElementById("pick-btn");
const dropArea = document.getElementById("drop-area");
const previewImg = document.getElementById("preview");
const gradcamImg = document.getElementById("gradcam-img");
const predictBtn = document.getElementById("api-btn");
const showGradcam = document.getElementById("show-gradcam");
const loader = document.getElementById("loader");

// Result fields
const diseaseEl = document.getElementById("disease");
const confidenceEl = document.getElementById("confidence");
const confidenceFill = document.getElementById("confidence-fill");
const severityEl = document.getElementById("severity");
const recTextEl = document.getElementById("rec-text");

// Logged-in user
const user = JSON.parse(localStorage.getItem("wheatshield_user") || "{}");

// --------------------
// FILE PICK / PREVIEW
// --------------------
pickBtn.addEventListener("click", () => fileInput.click());

fileInput.addEventListener("change", () => {
  if (fileInput.files[0]) {
    showPreview(fileInput.files[0]);
    resetResults();
  }
});

// Drag & drop
["dragenter", "dragover"].forEach(evt =>
  dropArea.addEventListener(evt, e => {
    e.preventDefault();
    dropArea.classList.add("drag");
  })
);

["dragleave", "drop"].forEach(evt =>
  dropArea.addEventListener(evt, e => {
    e.preventDefault();
    dropArea.classList.remove("drag");
  })
);

dropArea.addEventListener("drop", e => {
  const file = e.dataTransfer.files[0];
  if (file) {
    fileInput.files = e.dataTransfer.files;
    showPreview(file);
    resetResults();
  }
});

function showPreview(file) {
  previewImg.src = URL.createObjectURL(file);
  gradcamImg.style.display = "none";
  gradcamImg.src = "";
}

// --------------------
// PREDICT BUTTON
// --------------------
predictBtn.addEventListener("click", async () => {
  if (!fileInput.files[0]) {
    alert("Please upload an image first.");
    return;
  }

  try {
    loader.style.display = "flex";
    predictBtn.disabled = true;

    const formData = new FormData();
    formData.append("image", fileInput.files[0]);
    formData.append("user_id", user.id || user.email);

    const res = await fetch(`${API_BASE}/predict`, {
      method: "POST",
      body: formData
    });

    if (!res.ok) {
      throw new Error("Prediction failed");
    }

    const data = await res.json();

    // --------------------
    // DISPLAY RESULTS
    // --------------------
    diseaseEl.textContent = data.disease || "Unknown";

    const confPct = data.confidence
      ? Math.round(data.confidence * 100)
      : 0;

    confidenceEl.textContent = confPct + "%";
    confidenceFill.style.width = confPct + "%";

    // Confidence color
    confidenceFill.classList.remove("low", "med");
    if (confPct < 50) confidenceFill.classList.add("low");
    else if (confPct < 75) confidenceFill.classList.add("med");

    severityEl.textContent = data.severity || "—";

    // Severity color
    severityEl.style.color = "#27ae60";
    if (data.severity?.toLowerCase().includes("medium"))
      severityEl.style.color = "#f39c12";
    if (data.severity?.toLowerCase().includes("high"))
      severityEl.style.color = "#e74c3c";

    recTextEl.textContent =
      data.recommendation || "No recommendation available.";

    // --------------------
    // GRAD-CAM HANDLING
    // --------------------
    if (data.gradcam) {
      gradcamImg.src = `data:image/png;base64,${data.gradcam}`;
      gradcamImg.style.display = showGradcam.checked ? "block" : "none";
    }

  } catch (err) {
    console.error(err);
    alert("Something went wrong during prediction.");
  } finally {
    loader.style.display = "none";
    predictBtn.disabled = false;
  }
});

// --------------------
// GRAD-CAM TOGGLE
// --------------------
showGradcam.addEventListener("change", () => {
  if (!gradcamImg.src) return;
  gradcamImg.style.display = showGradcam.checked ? "block" : "none";
});

// --------------------
// RESET RESULTS
// --------------------
function resetResults() {
  diseaseEl.textContent = "—";
  confidenceEl.textContent = "—";
  confidenceFill.style.width = "0%";
  confidenceFill.classList.remove("low", "med");
  severityEl.textContent = "—";
  severityEl.style.color = "";
  recTextEl.textContent = "—";
}
