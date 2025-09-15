@echo off
echo 🚀 Probando MCP de Google Drive...
echo.

cd /d "%~dp0"

echo 📋 Configuración actual:
echo    Directorio: %CD%
echo    GDRIVE_CREDS_DIR: %GDRIVE_CREDS_DIR%
echo    GOOGLE_APPLICATION_CREDENTIALS: %GOOGLE_APPLICATION_CREDENTIALS%
echo.

echo 🔑 Verificando archivos de configuración...
if exist "credentials.json" (
    echo    ✅ credentials.json encontrado
) else (
    echo    ❌ credentials.json NO encontrado
)

if exist "tokens" (
    echo    ✅ Directorio tokens encontrado
    dir /b tokens 2>nul || echo       (vacío)
) else (
    echo    ❌ Directorio tokens NO encontrado
)
echo.

echo 📤 Ejecutando comando MCP...
echo Comando: node_modules\.bin\mcp-gdrive.cmd list_files --max-results 5
echo.

node_modules\.bin\mcp-gdrive.cmd list_files --max-results 5

echo.
echo 🏁 Comando MCP finalizado
echo.

echo 💡 Información adicional:
echo    - Si es la primera ejecución, el navegador se abrirá para autenticación OAuth
echo    - Los tokens se guardarán en el directorio 'tokens/'
echo    - La salida del comando se muestra arriba
echo.

pause