WheatShield — Frontend Demo

What this folder contains:
- `index.html` — interactive demo UI (image upload, preview, demo predictions)
- `styles.css` — pleasant and accessible styling
- `upload.js` — upload page client logic and backend hook
- `auth.js` — simple client-side auth helpers for demo
- `result.js`, `history.js` — result and history page scripts
- `assets/logo.svg` — simple logo

How to preview locally:
1. Open `frontend/index.html` in a browser (double-click or use Live Server extension)
2. Upload an image using the button or drag & drop
3. Click "Run Demo Prediction" to see sample disease, confidence, severity and Grad-CAM overlay

Connecting to your backend:
- Set `API_URL` at the top of `script.js` to your /predict endpoint (full URL recommended)
- The frontend POSTs the image as `FormData` with key `image` and expects JSON: `{ disease, confidence, severity, gradcam }`
- `gradcam` can be base64 PNG (optional)

Notes:
- The demo uses simulated Grad-CAM drawing; replace with real Grad-CAM PNG from backend for production.
- This is purposely lightweight and easy for farmers to use. Customize colors and copy in `styles.css` and `index.html`.

If you want, I can:
- Add a small Flask/FastAPI example backend with `/predict` stub
- Add responsive improvements or translations (local languages)
- Replace demo heatmap with real overlay rendering from backend

