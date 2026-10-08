@echo off
cd /d "%~dp0"
echo Servindo o visualizador em http://localhost:8123  (Ctrl+C para parar)
start "" http://localhost:8123/index.html
python -m http.server 8123
