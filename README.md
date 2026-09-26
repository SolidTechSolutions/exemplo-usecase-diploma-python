# 🇧🇷 SolidSign API - Caso de Uso: Diploma Digital (MEC) — Python

Este projeto demonstra a integração com a **SolidSign API** para o caso de uso real do **Diploma Digital** do MEC: um XML `DocumentacaoAcademicaRegistro` assinado por **3 assinantes diferentes**, em sequência, usando certificados custodiados no **KMS SolidSign**.

Diferente dos [exemplos genéricos de assinatura XML](https://github.com/SolidTechSolutions?q=integracao-xml), que expõem um único endpoint parametrizável, este repositório expõe **um endpoint isolado por etapa real do fluxo**, já pré-configurado com os valores corretos de `signatureNodeName`, `profile` e `isRemoveXPathExclusionFilter` de cada assinante.

## Fluxo (Diploma inicial)

| Etapa | Endpoint | Assinante | Certificado | Perfil | Nó assinado |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | `POST /api/diploma/step1-representante` | IES Representantes (reitor, decano…) | e-CPF | `ADRT` | `DadosDiploma` |
| 2 | `POST /api/diploma/step2-emissora-dados` | IES Emissora | e-CNPJ | `ADRT` | `DadosDiploma` (filtro XPath removido) |
| 3 | `POST /api/diploma/step3-envelope-final` | IES Emissora | e-CNPJ | `ADRA` | `DocumentacaoAcademicaRegistro` (envelope final) |

## Configuração (.env)

Veja `.env.example` para `SOLIDSIGN_API_*` e as variáveis por etapa `SOLIDSIGN_DIPLOMA_STEP{1,2,3}_*`, já pré-preenchidas com os valores reais do Diploma Digital do MEC.

## Stack
1. Python 3.10+
2. FastAPI + Uvicorn

## Como Executar

```bash
python -m venv venv && source venv/bin/activate   # ou venv\Scripts\activate no Windows
pip install -r requirements.txt
cp .env.example .env   # edite com seu token
uvicorn main:app --port 8097 --reload
```

```
curl -X POST http://localhost:8097/api/diploma/step1-representante \
  -F "document=@doc-academica.xml" -F "kmsCode=$KMS_REPRESENTANTE" -o step1-signed.xml

curl -X POST http://localhost:8097/api/diploma/step2-emissora-dados \
  -F "document=@step1-signed.xml" -F "kmsCode=$KMS_IES_EMISSORA" -o step2-signed.xml

curl -X POST http://localhost:8097/api/diploma/step3-envelope-final \
  -F "document=@step2-signed.xml" -F "kmsCode=$KMS_IES_EMISSORA" -o diploma-final.xml
```

## Outras variantes do Diploma Digital

Consulte a [documentação da trilha Diploma Digital](https://solidsign.com.br/developers/diploma) para outras variantes (Diploma + Registro, Histórico Escolar).

## Outros métodos de certificação

Para HSM em nuvem ou navegador (PKCS#1), use os mesmos parâmetros de etapa nos exemplos genéricos [`exemplo-python-integracao-xml-cloud`](https://github.com/SolidTechSolutions/exemplo-python-integracao-xml-cloud) e [`exemplo-python-integracao-xml-pkcs1`](https://github.com/SolidTechSolutions/exemplo-python-integracao-xml-pkcs1).

## Tratamento de Erros
O sistema loga o JSON detalhado de erro da SolidSign para facilitar o debug.

---

# 🇬🇧 SolidSign API - Use Case: Digital Diploma (MEC) — Python

This project demonstrates the integration with the **SolidSign API** for the real-world **Digital Diploma** use case: a `DocumentacaoAcademicaRegistro` XML signed by **3 different signers**, in sequence, using KMS-custodied certificates.

## Flow (initial Diploma)

| Step | Endpoint | Signer | Certificate | Profile | Signed node |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | `POST /api/diploma/step1-representante` | Institution representatives | e-CPF | `ADRT` | `DadosDiploma` |
| 2 | `POST /api/diploma/step2-emissora-dados` | Issuing institution | e-CNPJ | `ADRT` | `DadosDiploma` (XPath filter removed) |
| 3 | `POST /api/diploma/step3-envelope-final` | Issuing institution | e-CNPJ | `ADRA` | `DocumentacaoAcademicaRegistro` (final envelope) |

## Configuration (.env)

See `.env.example` for `SOLIDSIGN_API_*` and per-step `SOLIDSIGN_DIPLOMA_STEP{1,2,3}_*` variables.

## Stack
1. Python 3.10+
2. FastAPI + Uvicorn

## How to Run

```bash
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn main:app --port 8097 --reload
```

## Other Digital Diploma variants

See the [Digital Diploma trail docs](https://solidsign.com.br/developers/diploma).

## Other certification methods

For cloud HSM or browser (PKCS#1) signing, apply the same per-step parameters to [`exemplo-python-integracao-xml-cloud`](https://github.com/SolidTechSolutions/exemplo-python-integracao-xml-cloud) and [`exemplo-python-integracao-xml-pkcs1`](https://github.com/SolidTechSolutions/exemplo-python-integracao-xml-pkcs1).

## Error Handling
The system logs SolidSign's detailed error JSON for debugging.

---

# 🇪🇸 SolidSign API - Caso de Uso: Diploma Digital (MEC) — Python

Este proyecto demuestra la integración con la **SolidSign API** para el caso de uso real del **Diploma Digital**: un XML `DocumentacaoAcademicaRegistro` firmado por **3 firmantes diferentes**, en secuencia, usando certificados custodiados en el KMS.

## Flujo (Diploma inicial)

| Etapa | Endpoint | Firmante | Certificado | Perfil | Nodo firmado |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | `POST /api/diploma/step1-representante` | Representantes de la IES | e-CPF | `ADRT` | `DadosDiploma` |
| 2 | `POST /api/diploma/step2-emissora-dados` | IES Emisora | e-CNPJ | `ADRT` | `DadosDiploma` (filtro XPath eliminado) |
| 3 | `POST /api/diploma/step3-envelope-final` | IES Emisora | e-CNPJ | `ADRA` | `DocumentacaoAcademicaRegistro` (sobre final) |

## Configuración (.env)

Vea `.env.example` para las variables `SOLIDSIGN_API_*` y `SOLIDSIGN_DIPLOMA_STEP{1,2,3}_*`.

## Stack
1. Python 3.10+
2. FastAPI + Uvicorn

## Cómo Ejecutar

```bash
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn main:app --port 8097 --reload
```

## Otras variantes del Diploma Digital

Consulte la [documentación de la ruta Diploma Digital](https://solidsign.com.br/developers/diploma).

## Otros métodos de certificación

Para HSM en la nube o navegador (PKCS#1), aplique los mismos parámetros a [`exemplo-python-integracao-xml-cloud`](https://github.com/SolidTechSolutions/exemplo-python-integracao-xml-cloud) y [`exemplo-python-integracao-xml-pkcs1`](https://github.com/SolidTechSolutions/exemplo-python-integracao-xml-pkcs1).

## Gestión de Errores
El sistema registra el JSON detallado de errores de SolidSign.
