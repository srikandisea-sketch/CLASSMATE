# ClassMate — English Productivity Schedule Assistant

A Streamlit chatbot for study planning, homework breakdowns, English practice, and productivity support.

## Model note
This project defaults to `gemini-3.8-flash` because your Gemini API error explicitly recommended that model. `gemini-1.5-flash` is an older model and may no longer be available to new users. If Google AI Studio shows a different current model for your account, set that exact model ID in `config.yaml`.

## Setup on Windows / VS Code
1. Extract this ZIP and open the `classmate-bot-rebuilt` folder in VS Code.
2. Copy `.env.example` to `.env`.
3. Open `.env` in the editor and replace the placeholder with your own API key. Do not paste your key into chat.
4. Open the VS Code terminal in the project folder and run:

   ```powershell
   py -m venv .venv
   .\.venv\Scripts\python.exe -m pip install -r requirements.txt
   .\.venv\Scripts\python.exe -m streamlit run app.py
   ```

5. Open the local URL shown by Streamlit, normally `http://localhost:8501`.

## Troubleshooting
- Missing key: confirm `.env` is beside `app.py`, not inside `.venv`.
- 404: check that the model ID in `config.yaml` is available to your API account.
- 401/403: check API key validity and permissions.
- 429: check quota and rate limits.
- Timeout: check internet, firewall, VPN, or network access.
- The app shows the returned error in the interface to simplify debugging.
