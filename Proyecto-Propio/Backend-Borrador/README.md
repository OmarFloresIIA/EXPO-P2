# Proyecto propio — Backend y Base de Datos (Borrador)

Esta carpeta tiene solo lo necesario para levantar PostgreSQL, cargar los datos y conectar la página web mediante una API local.

## ¿Necesito Docker si ya tengo pgAdmin?
**Sí.** pgAdmin solo es la pantalla visual para ver y consultar bases de datos; **Docker** es el que ejecuta el servidor PostgreSQL 17 con tus tablas. Luego conectas pgAdmin a ese servidor.

## 1. Arrancar todo en un solo comando
Abre Docker Desktop, entra a esta carpeta en PowerShell y ejecuta:

```powershell
.\iniciar.ps1
```

Eso hace todo automáticamente:
1. Crea el archivo `.env` (si no existe).
2. Levanta PostgreSQL 17 en el puerto `5434` y aplica `esquema.sql`, migraciones y permisos.
3. Carga los 2,702 registros del Excel (sin duplicarlos si lo corres otra vez).
4. Enciende la API en `http://127.0.0.1:5000`.

Comprueba que funciona abriendo `http://127.0.0.1:5000/salud` en tu navegador.

## 2. Conectar en pgAdmin
En pgAdmin haz clic derecho en **Servers -> Register -> Server** y pon:
- **Name:** `Ventas Industriales`
- **Host:** `127.0.0.1`
- **Port:** `5434`
- **Maintenance database:** `ventas_industriales`
- **Username:** `postgres` (o `usuario_app`)
- **Password:** la contraseña que está en tu archivo `.env` (`POSTGRES_PASSWORD` o `APP_DB_PASSWORD`).

## 3. Conectar con la página web (ngrok)
En otra terminal, expón la API local:

```powershell
ngrok http 5000
```

Copia la URL `https://....ngrok-free.app` que te da ngrok y úsala en el `fetch()` de tu formulario web:
- `POST <URL_NGROK>/clientes` — registra un cliente nuevo.
- `POST <URL_NGROK>/pedidos` — registra un pedido nuevo.
- `GET <URL_NGROK>/clientes` — muestra los últimos 10 clientes.

## Detener o reiniciar desde cero
- Detener sin borrar datos: `docker compose down`
- Borrar todo y empezar limpio: `docker compose down -v`
