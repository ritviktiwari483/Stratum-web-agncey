# 🚀 StratumWeb Backend Guide

This guide helps you connect your live website (GitHub Pages) to your local Python backend so you can receive leads and view the dashboard while developing.

## 1. The Mobile/Live Problem
Your website is on **HTTPS** (GitHub), but your local laptop is on **HTTP**. Browsers block this for security ("Mixed Content").
To fix this for testing on your phone or the live site, you need a secure tunnel.

## 2. Quick Fix: Using Ngrok (Recommended)
Ngrok gives your local laptop a temporary public HTTPS address that the live website can talk to.

1.  **Download Ngrok:** [ngrok.com](https://ngrok.com/)
2.  **Run your Backend:** Open a terminal and run `python main.py` (or use `run_backend.bat`).
3.  **Start the Tunnel:** In a new terminal, type:
    ```bash
    ngrok http 8000
    ```
4.  **Update main.js:**
    - Copy the `https://....ngrok-free.app` URL from the ngrok terminal.
    - Open `assist/main.js` and paste it into `PRODUCTION_API_URL`:
      ```javascript
      PRODUCTION_API_URL: "https://your-unique-id.ngrok-free.app",
      ```
5.  **Commit & Push:** Save, commit, and push your changes to GitHub. Now your live site will talk to your laptop!

---

## 3. Permanent Fix: Render.com
If you want the backend to stay online forever (even when your laptop is off), host it on **Render**:

1.  Create a free account on [Render.com](https://render.com/).
2.  Click **New +** -> **Web Service**.
3.  Connect your GitHub repository.
4.   Set the **Start Command** to: `python main.py` (or `gunicorn main:app` for better performance).
5.  Update `PRODUCTION_API_URL` in `main.js` with your new Render URL.

## 4. Local Testing Tip
If you just want to test on your laptop, use `http://localhost:8000`. The code is already set to handle this automatically!
