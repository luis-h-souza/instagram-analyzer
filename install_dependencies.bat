@echo off
echo Instalando dependencias do Instagram Analyzer...

echo.
echo Instalando dependencias Python...
pip install -r requirements.txt

echo.
echo Instalando dependencias Node.js...
npm install

echo.
echo Configurando arquivo de ambiente...
if not exist .env (
    copy env.example .env
    echo Arquivo .env criado! Configure suas chaves de API.
) else (
    echo Arquivo .env ja existe.
)

echo.
echo Instalacao concluida!
echo.
echo Proximos passos:
echo 1. Configure o arquivo .env com suas chaves de API
echo 2. Execute start_backend.bat para iniciar a API
echo 3. Execute start_frontend.bat para iniciar o frontend
echo.
pause
