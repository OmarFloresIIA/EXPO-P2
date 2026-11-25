# Guía rápida para la exposición de mañana (13 min)

## 1. Cómo funciona la conexión (Web -> ngrok -> API -> BD local)
Es el flujo más seguro para una prueba en vivo porque la página en GitHub Pages es estática:
1. **Página web (GitHub Pages):** Tiene el formulario y manda los datos en JSON con `fetch()`.
2. **ngrok:** Abre una URL `https://...ngrok-free.app` que apunta al puerto local de tu laptop.
3. **API local (Python con FastAPI o Flask):** Recibe el JSON, se conecta a PostgreSQL con `usuario_app` usando `.env` y hace el `INSERT`.
4. **PostgreSQL en Docker:** Guarda la fila en `ventas_industriales` (puerto `5434`). Luego la muestras con un `SELECT` en `psql`.

> Nota: Nunca pongas contraseñas en el HTML/JS. Todo se queda en el `.env` de tu laptop.

## 2. Reparto sugerido de tiempos (máx. 13 min)
- **Min 0–6 (Proyecto propio):**
  - Explicar el flujo Web -> ngrok -> API -> PostgreSQL (1.5 min).
  - Demo en vivo: llenar formulario y comprobar con `SELECT` en `psql` (2 min).
  - Reglas de integridad, permisos y scripts (1 min).
  - Práctica integrada 6, 7 y 8: 1 normalización + 1 consulta RelaX vs SQL (1.5 min).
- **Min 6–11 (Proyecto asignado):**
  - Mostrar fork publicado + qué hace + incidencia de montaje (2 min).
  - 3 consultas: pregunta, álgebra relacional, árbol y SQL en vivo (3 min).
- **Min 11–13 (Artículo y mejoras):**
  - Resumen del manuscrito extendido y avance vs Parcial 1 (1 min).
  - 2 propuestas de mejora (1 min).

## 3. Checklist rápido antes de exponer
- [ ] Juntar la práctica 6–8 y rellenar la diapositiva 7 (`normalizacion.md`, `algebra.md` y RelaX).
- [ ] Levantar API local + `ngrok` y probar que el formulario inserte en PostgreSQL.
- [ ] Anotar en la diapositiva 8 la incidencia real del montaje del proyecto asignado.
- [ ] Poner las 3 consultas definitivas del proyecto asignado en la diapositiva 9.
- [ ] Grabar un video corto (1–2 min) de respaldo por si falla el internet del laboratorio.
- [ ] Poner todos los enlaces y la cita en APA 7 al inicio del `README.md` del repositorio.
