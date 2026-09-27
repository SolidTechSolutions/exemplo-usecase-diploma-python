"""
[EN]    Diploma Digital (MEC) use case — all 5 documents, KMS custody.
        Start: uvicorn main:app --port 8097 --reload

[PT-BR] Caso de uso Diploma Digital (MEC) — os 5 documentos, custódia KMS.
        Iniciar: uvicorn main:app --port 8097 --reload
"""

import logging
import os

from dotenv import load_dotenv
from fastapi import FastAPI, File, Form, UploadFile
from fastapi.responses import Response

import diploma_assembly_service
import xml_kms_signing_service

load_dotenv()
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s — %(message)s")

app = FastAPI(title="SolidSign — Diploma Digital Use Case (all 5 documents)")


def step_from_env(prefix: str) -> dict:
    return {
        "node_name": os.getenv(f"{prefix}_NODE_NAME"),
        "namespace": os.getenv(f"{prefix}_NAMESPACE"),
        "profile": os.getenv(f"{prefix}_PROFILE", ""),
        "remove_xpath_filter": os.getenv(f"{prefix}_REMOVE_XPATH_FILTER", "false") == "true",
    }


async def handle_step(document: UploadFile, kms_code: str, step: dict, output_name: str) -> Response:
    content = await document.read()
    signed = xml_kms_signing_service.sign(
        content, document.filename, kms_code,
        step["node_name"], step["namespace"], step["profile"], step["remove_xpath_filter"],
    )
    if signed:
        return Response(
            content=signed, media_type="application/xml",
            headers={"Content-Disposition": f'attachment; filename="{output_name}"'},
        )
    return Response(content="Signing failed. Check logs.", status_code=500)


# ─── Documento 1/5 — Documentação Acadêmica de Registro ────────────────────
@app.post("/api/diploma/documentacao-academica/step1-representante")
async def documentacao_academica_step1(document: UploadFile = File(...), kmsCode: str = Form(...)):
    return await handle_step(document, kmsCode, step_from_env("SOLIDSIGN_DOCACAD_STEP1"), "documentacao_academica_step1_signed.xml")


@app.post("/api/diploma/documentacao-academica/step2-emissora-dados")
async def documentacao_academica_step2(document: UploadFile = File(...), kmsCode: str = Form(...)):
    return await handle_step(document, kmsCode, step_from_env("SOLIDSIGN_DOCACAD_STEP2"), "documentacao_academica_step2_signed.xml")


@app.post("/api/diploma/documentacao-academica/step3-envelope-final")
async def documentacao_academica_step3(document: UploadFile = File(...), kmsCode: str = Form(...)):
    return await handle_step(document, kmsCode, step_from_env("SOLIDSIGN_DOCACAD_STEP3"), "documentacao_academica_step3_signed.xml")


# ─── Documento 2/5 — Diploma Digital (montagem + 2 etapas) ─────────────────
@app.post("/api/diploma/diploma/assemble")
async def diploma_assemble(signedDocumentacaoAcademica: UploadFile = File(...)):
    content = await signedDocumentacaoAcademica.read()
    assembled = diploma_assembly_service.assemble(content)
    if assembled:
        return Response(
            content=assembled, media_type="application/xml",
            headers={"Content-Disposition": 'attachment; filename="diploma_montado.xml"'},
        )
    return Response(content="Assembly failed. Check logs.", status_code=400)


@app.post("/api/diploma/diploma/step1-registradora-dados")
async def diploma_step1(document: UploadFile = File(...), kmsCode: str = Form(...)):
    return await handle_step(document, kmsCode, step_from_env("SOLIDSIGN_DIPLOMA_STEP1"), "diploma_step1_signed.xml")


@app.post("/api/diploma/diploma/step2-envelope-final")
async def diploma_step2(document: UploadFile = File(...), kmsCode: str = Form(...)):
    return await handle_step(document, kmsCode, step_from_env("SOLIDSIGN_DIPLOMA_STEP2"), "diploma_step2_signed.xml")


# ─── Documento 3/5 — Histórico Escolar Digital ─────────────────────────────
@app.post("/api/diploma/historico-escolar/step1-secretaria-dados")
async def historico_escolar_step1(document: UploadFile = File(...), kmsCode: str = Form(...)):
    return await handle_step(document, kmsCode, step_from_env("SOLIDSIGN_HISTESC_STEP1"), "historico_escolar_step1_signed.xml")


@app.post("/api/diploma/historico-escolar/step2-envelope-final")
async def historico_escolar_step2(document: UploadFile = File(...), kmsCode: str = Form(...)):
    return await handle_step(document, kmsCode, step_from_env("SOLIDSIGN_HISTESC_STEP2"), "historico_escolar_step2_signed.xml")


# ─── Documento 4/5 — Currículo Escolar Digital (documento inteiro) ─────────
@app.post("/api/diploma/curriculo-escolar/step1-coordenador")
async def curriculo_escolar_step1(document: UploadFile = File(...), kmsCode: str = Form(...)):
    return await handle_step(document, kmsCode, step_from_env("SOLIDSIGN_CURRESC_STEP1"), "curriculo_escolar_step1_signed.xml")


@app.post("/api/diploma/curriculo-escolar/step2-envelope-final")
async def curriculo_escolar_step2(document: UploadFile = File(...), kmsCode: str = Form(...)):
    return await handle_step(document, kmsCode, step_from_env("SOLIDSIGN_CURRESC_STEP2"), "curriculo_escolar_step2_signed.xml")


# ─── Documento 5/5 — Lista de Diplomas Anulados / Arquivo de Fiscalização ──
@app.post("/api/diploma/lista-anulados/sign")
async def lista_anulados_sign(document: UploadFile = File(...), kmsCode: str = Form(...)):
    return await handle_step(document, kmsCode, step_from_env("SOLIDSIGN_LISTAANUL"), "lista_anulados_signed.xml")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8097)
