$ErrorActionPreference = "Stop"

# 1. Crear .env si no existe
if (-not (Test-Path ".env")) {
    Copy-Item ".env.example" ".env"
    Write-Host "Se creo .env desde .env.example (puedes cambiar las claves cuando gustes)." -ForegroundColor Yellow
}

# Cargar variables de .env en la sesion actual
Get-Content ".env" | ForEach-Object {
    if ($_ -match '^\s*([^#][^=]+)=(.*)$') {
        [Environment]::SetEnvironmentVariable($matches[1].Trim(), $matches[2].Trim(), "Process")
    }
}

# 2. Levantar PostgreSQL en Docker (aplica esquema, migraciones y permisos automaticamente)
Write-Host "`n[1/3] Levantando PostgreSQL 17 en Docker..." -ForegroundColor Cyan
docker compose up -d

Write-Host "Esperando a que PostgreSQL acepte conexiones..." -ForegroundColor Cyan
for ($i = 0; $i -lt 20; $i++) {
    docker compose exec -T db pg_isready -U postgres -d ventas_industriales *> $null
    if ($LASTEXITCODE -eq 0) { break }
    Start-Sleep -Seconds 1
}

# 3. Preparar Python y cargar datos del Excel (no duplica si ya se cargaron)
Write-Host "`n[2/3] Preparando entorno Python y cargando datos..." -ForegroundColor Cyan
if (-not (Test-Path ".venv\Scripts\python.exe")) {
    python -m venv .venv
    .\.venv\Scripts\python.exe -m pip install -r backend\requirements.txt
}

.\.venv\Scripts\python.exe db\poblar.py

# 4. Iniciar la API local
Write-Host "`n[3/3] Iniciando API en http://127.0.0.1:$($env:API_PORT) ..." -ForegroundColor Green
Write-Host "Prueba en tu navegador: http://127.0.0.1:$($env:API_PORT)/salud" -ForegroundColor Green
.\.venv\Scripts\python.exe backend\app.py
