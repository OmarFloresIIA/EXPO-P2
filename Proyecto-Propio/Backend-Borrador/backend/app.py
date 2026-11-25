import os
from datetime import date
from pathlib import Path

import psycopg2
from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flask_cors import CORS

# Carga las credenciales desde el archivo .env en la raíz de Backend-Borrador
ROOT = Path(__file__).resolve().parents[1]
load_dotenv(ROOT / ".env")

app = Flask(__name__)
# Permite peticiones desde la página publicada en GitHub Pages
CORS(app)


def conectar_bd():
    password = os.environ.get("APP_DB_PASSWORD")
    if not password:
        raise RuntimeError("Falta APP_DB_PASSWORD en el archivo .env")
    return psycopg2.connect(
        host=os.environ.get("DB_HOST", "127.0.0.1"),
        port=int(os.environ.get("DB_PORT", "5434")),
        dbname=os.environ.get("DB_NAME", "ventas_industriales"),
        user=os.environ.get("DB_USER", "usuario_app"),
        password=password,
    )


@app.get("/salud")
def salud():
    try:
        with conectar_bd() as conn, conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM cliente;")
            total_clientes = cur.fetchone()[0]
        return jsonify({"ok": True, "bd": "conectada", "clientes": total_clientes})
    except Exception as exc:
        return jsonify({"ok": False, "error": str(exc)}), 500


@app.get("/clientes")
def listar_clientes():
    with conectar_bd() as conn, conn.cursor() as cur:
        cur.execute(
            """
            SELECT numerocliente, razonsocial, correocliente, telefonocliente, tipocliente
            FROM cliente
            ORDER BY numerocliente DESC
            LIMIT 10;
            """
        )
        filas = [
            {
                "numeroCliente": f[0],
                "razonSocial": f[1],
                "correoCliente": f[2],
                "telefonoCliente": f[3],
                "tipoCliente": f[4],
            }
            for f in cur.fetchall()
        ]
    return jsonify(filas)


@app.post("/clientes")
def registrar_cliente():
    datos = request.get_json(silent=True) or {}
    tipo = (datos.get("tipoCliente") or "NACIONAL").strip().upper()

    conn = conectar_bd()
    try:
        with conn.cursor() as cur:
            numero = datos.get("numeroCliente")
            if not numero:
                cur.execute("SELECT COALESCE(MAX(numerocliente), 0) + 1 FROM cliente;")
                numero = cur.fetchone()[0]

            if tipo == "NACIONAL":
                rfc = datos.get("RFC")
                regimen = datos.get("regimenFiscal")
                estado = datos.get("estadoOrigen")
                id_fiscal, pais = None, None
            else:
                rfc, regimen, estado = None, None, None
                id_fiscal = datos.get("idFiscalGlobal")
                pais = datos.get("paisReceptor")

            cur.execute(
                """
                INSERT INTO cliente (
                    numerocliente, razonsocial, correocliente, telefonocliente,
                    tipocliente, rfc, regimenfiscal, estadoorigen,
                    idfiscalglobal, paisreceptor
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING numerocliente, razonsocial, correocliente;
                """,
                (
                    int(numero),
                    datos.get("razonSocial"),
                    datos.get("correoCliente"),
                    datos.get("telefonoCliente"),
                    tipo,
                    rfc,
                    regimen,
                    estado,
                    id_fiscal,
                    pais,
                ),
            )
            creado = cur.fetchone()
        conn.commit()
        return jsonify(
            {
                "ok": True,
                "mensaje": "Cliente registrado correctamente",
                "numeroCliente": creado[0],
                "razonSocial": creado[1],
                "correoCliente": creado[2],
            }
        ), 201
    except psycopg2.Error as exc:
        conn.rollback()
        return jsonify({"ok": False, "error": exc.pgerror or str(exc)}), 400
    except Exception as exc:
        conn.rollback()
        return jsonify({"ok": False, "error": str(exc)}), 400
    finally:
        conn.close()


@app.post("/pedidos")
def registrar_pedido():
    datos = request.get_json(silent=True) or {}
    hoy = date.today()

    conn = conectar_bd()
    try:
        with conn.cursor() as cur:
            folio = datos.get("folio")
            if not folio:
                cur.execute("SELECT COALESCE(MAX(folio), 0) + 1 FROM pedido;")
                folio = cur.fetchone()[0]

            cur.execute(
                """
                INSERT INTO pedido (folio, numerocliente, estatus, dia, mes, anio)
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING folio, numerocliente, estatus;
                """,
                (
                    int(folio),
                    int(datos["numeroCliente"]),
                    (datos.get("estatus") or "REGISTRADO").strip().upper(),
                    int(datos.get("dia") or hoy.day),
                    int(datos.get("mes") or hoy.month),
                    int(datos.get("anio") or hoy.year),
                ),
            )
            creado = cur.fetchone()
        conn.commit()
        return jsonify(
            {
                "ok": True,
                "mensaje": "Pedido registrado correctamente",
                "folio": creado[0],
                "numeroCliente": creado[1],
                "estatus": creado[2],
            }
        ), 201
    except psycopg2.Error as exc:
        conn.rollback()
        return jsonify({"ok": False, "error": exc.pgerror or str(exc)}), 400
    except Exception as exc:
        conn.rollback()
        return jsonify({"ok": False, "error": str(exc)}), 400
    finally:
        conn.close()


if __name__ == "__main__":
    puerto = int(os.environ.get("API_PORT", "5000"))
    app.run(host="127.0.0.1", port=puerto, debug=True)
