#!/usr/bin/env bash
set -e
cd "$(dirname "$0")"
if [ ! -d .venv ]; then
  python3 -m venv .venv
fi
source .venv/bin/activate
pip install -r requirements.txt
echo "App liberado na rede local. Acesse pelo celular: http://IP_DO_COMPUTADOR:8501"
streamlit run app.py --server.address=0.0.0.0 --server.port=8501
