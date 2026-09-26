"""
[EN]    Diploma Digital (MEC) use case — 3 isolated signer endpoints, KMS custody.
        Start: uvicorn main:app --port 8097 --reload
        Step 1: POST http://localhost:8097/api/diploma/step1-representante
        Step 2: POST http://localhost:8097/api/diploma/step2-emissora-dados
        Step 3: POST http://localhost:8097/api/diploma/step3-envelope-final

[PT-BR] Caso de uso Diploma Digital (MEC) — 3 endpoints isolados por assinante, custódia KMS.
        Iniciar: uvicorn main:app --port 8097 --reload
"""

import logging

from fastapi import FastAPI, File, Form, UploadFile
from fastapi.responses import Response

from service import DiplomaSigningService

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s — %(message)s")

app = FastAPI(title="SolidSign — Diploma Digital Use Case")
service = DiplomaSigningService()


async def handle_step(document: UploadFile, kms_code: str, sign_fn, output_name: str) -> Response:
    content = await document.read()
    signed = sign_fn(content, document.filename, kms_code)
    if signed:
        return Response(
            content=signed,
            media_type="application/xml",
            headers={"Content-Disposition": f'attachment; filename="{output_name}"'},
        )
    return Response(content="Signing failed. Check logs.", status_code=500)


@app.post("/api/diploma/step1-representante")
async def step1(document: UploadFile = File(...), kmsCode: str = Form(...)):
    return await handle_step(document, kmsCode, service.sign_step1_representante, "diploma_step1_signed.xml")


@app.post("/api/diploma/step2-emissora-dados")
async def step2(document: UploadFile = File(...), kmsCode: str = Form(...)):
    return await handle_step(document, kmsCode, service.sign_step2_emissora_dados, "diploma_step2_signed.xml")


@app.post("/api/diploma/step3-envelope-final")
async def step3(document: UploadFile = File(...), kmsCode: str = Form(...)):
    return await handle_step(document, kmsCode, service.sign_step3_envelope_final, "diploma_step3_signed.xml")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8097)
