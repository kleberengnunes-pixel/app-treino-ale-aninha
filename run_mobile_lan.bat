@echo off
cd /d %~dp0
if not exist .venv (
    python -m venv .venv
)
call .venv\Scripts\activate.bat
pip install -r requirements.txt
echo.
echo App liberado na rede local.
echo Descubra o IPv4 do computador com: ipconfig
echo Depois acesse no celular: http://IP_DO_COMPUTADOR:8501
echo.
streamlit run app.py --server.address=0.0.0.0 --server.port=8501
pause
