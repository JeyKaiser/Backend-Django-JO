# Script de Despliegue para JO System - Red Local
# Ejecutar como Administrador

Write-Host "🚀 Iniciando despliegue de JO System..." -ForegroundColor Green

# Verificar permisos de administrador
$currentUser = [Security.Principal.WindowsIdentity]::GetCurrent()
$principal = New-Object Security.Principal.WindowsPrincipal($currentUser)
$adminRole = [Security.Principal.WindowsBuiltInRole]::Administrator

if (-not $principal.IsInRole($adminRole)) {
    Write-Host "❌ Este script debe ejecutarse como Administrador" -ForegroundColor Red
    exit 1
}

# Configurar Firewall
Write-Host "🔥 Configurando Firewall..." -ForegroundColor Yellow
try {
    netsh advfirewall firewall add rule name="JO System Backend" dir=in action=allow protocol=TCP localport=8000 remoteip=192.168.0.0/24
    netsh advfirewall firewall add rule name="JO System Frontend" dir=in action=allow protocol=TCP localport=3000 remoteip=192.168.0.0/24
    Write-Host "✅ Firewall configurado correctamente" -ForegroundColor Green
} catch {
    Write-Host "⚠️ Error configurando firewall: $_" -ForegroundColor Yellow
}

# Verificar servicios
Write-Host "🔍 Verificando servicios..." -ForegroundColor Yellow

# Verificar si Django está ejecutándose
$djangoProcess = Get-Process python -ErrorAction SilentlyContinue | Where-Object { $_.CommandLine -like "*manage.py runserver*" }
if ($djangoProcess) {
    Write-Host "✅ Backend Django ejecutándose (PID: $($djangoProcess.Id))" -ForegroundColor Green
} else {
    Write-Host "❌ Backend Django no está ejecutándose" -ForegroundColor Red
}

# Verificar si Next.js está ejecutándose
$nextProcess = Get-Process node -ErrorAction SilentlyContinue | Where-Object { $_.CommandLine -like "*next*" }
if ($nextProcess) {
    Write-Host "✅ Frontend Next.js ejecutándose (PID: $($nextProcess.Id))" -ForegroundColor Green
} else {
    Write-Host "❌ Frontend Next.js no está ejecutándose" -ForegroundColor Red
}

# Verificar conectividad
Write-Host "🌐 Verificando conectividad..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://192.168.0.40:8000" -TimeoutSec 5 -ErrorAction Stop
    Write-Host "✅ Backend accesible en http://192.168.0.40:8000" -ForegroundColor Green
} catch {
    Write-Host "❌ Backend no accesible: $_" -ForegroundColor Red
}

try {
    $response = Invoke-WebRequest -Uri "http://192.168.0.40:3000" -TimeoutSec 5 -ErrorAction Stop
    Write-Host "✅ Frontend accesible en http://192.168.0.40:3000" -ForegroundColor Green
} catch {
    Write-Host "❌ Frontend no accesible: $_" -ForegroundColor Red
}

Write-Host "`n🎉 Despliegue completado!" -ForegroundColor Green
Write-Host "📋 URLs de acceso:" -ForegroundColor Cyan
Write-Host "   Backend:  http://192.168.0.40:8000" -ForegroundColor White
Write-Host "   Frontend: http://192.168.0.40:3000" -ForegroundColor White
Write-Host "   API Docs: http://192.168.0.40:8000/api/" -ForegroundColor White