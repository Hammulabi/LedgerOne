#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

python_bin="python3"
if ! command -v "$python_bin" >/dev/null 2>&1; then
  python_bin="python"
fi

cd "$ROOT_DIR/backend"
if [ ! -d ".venv" ]; then
  "$python_bin" -m venv .venv
fi
source .venv/bin/activate
pip install -r requirements.txt
python scripts/init_db.py

uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload &
BACKEND_PID=$!

cd "$ROOT_DIR"
$python_bin -m http.server 8080 --directory frontend &
FRONTEND_PID=$!

echo "Backend: http://127.0.0.1:8000"
echo "Frontend: http://127.0.0.1:8080"

echo "Press Ctrl+C to stop both services"
trap 'kill $BACKEND_PID $FRONTEND_PID' INT TERM
wait
