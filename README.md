# 🇧🇷 SolidSign API - Caso de Uso: Diploma Digital (MEC) — Python

Este projeto demonstra a integração com a **SolidSign API** para o caso de uso completo do **Diploma Digital** do MEC, cobrindo os **5 documentos** da trilha, cada um com seus próprios assinantes e etapas, usando certificados custodiados no **KMS SolidSign**.

## Os 5 documentos

| # | Documento | Endpoints | Assinantes |
| :-: | :--- | :--- | :--- |
| 1 | Documentação Acadêmica de Registro | `documentacao-academica/step{1,2,3}-*` | IES Representantes (e-CPF, 1..n) → IES Emissora dados (e-CNPJ) → IES Emissora envelope final (e-CNPJ) |
| 2 | **Diploma Digital** | `diploma/assemble`, `diploma/step{1,2}-*` | *(montado a partir do doc. 1)* → Representante da Registradora (e-CPF) → IES Registradora envelope final (e-CNPJ) |
| 3 | Histórico Escolar Digital | `historico-escolar/step{1,2}-*` | *(parcial: só step2)* Representante da Secretaria (e-CPF) → IES Emissora envelope final (e-CNPJ) |
| 4 | Currículo Escolar Digital | `curriculo-escolar/step{1,2}-*` | Coordenador do Curso (e-CPF) → IES Emissora (e-CNPJ) — documento inteiro |
| 5 | Lista de Diplomas Anulados / Arquivo de Fiscalização | `lista-anulados/sign` | Instituição (e-CNPJ) — documento inteiro, etapa única |

## Documento 2 — montagem do Diploma

`POST /api/diploma/diploma/assemble` recebe a Documentação Acadêmica assinada (`signedDocumentacaoAcademica`), copia `<DadosDiploma>` pro template do envelope Diploma (`templates/diploma-template.xml`) usando `xml.etree.ElementTree` (biblioteca padrão do Python, `diploma_assembly_service.py`), e retorna o Diploma **ainda não assinado**.

## Configuração (.env)

Veja `.env.example` para `SOLIDSIGN_API_*` e as variáveis por documento/etapa, já pré-preenchidas com os valores reais do MEC.

## Stack
1. Python 3.10+
2. FastAPI + Uvicorn
3. `xml.etree.ElementTree` (biblioteca padrão) para a montagem do Diploma

## Como Executar

```bash
python -m venv venv && source venv/bin/activate   # ou venv\Scripts\activate no Windows
pip install -r requirements.txt
cp .env.example .env   # edite com seu token
uvicorn main:app --port 8097 --reload
```

```
curl -X POST http://localhost:8097/api/diploma/documentacao-academica/step1-representante -F "document=@doc-academica.xml" -F "kmsCode=$KMS_REPRESENTANTE" -o academica-step1.xml
curl -X POST http://localhost:8097/api/diploma/documentacao-academica/step2-emissora-dados -F "document=@academica-step1.xml" -F "kmsCode=$KMS_IES_EMISSORA" -o academica-step2.xml
curl -X POST http://localhost:8097/api/diploma/documentacao-academica/step3-envelope-final -F "document=@academica-step2.xml" -F "kmsCode=$KMS_IES_EMISSORA" -o academica-final.xml

curl -X POST http://localhost:8097/api/diploma/diploma/assemble -F "signedDocumentacaoAcademica=@academica-final.xml" -o diploma-montado.xml
curl -X POST http://localhost:8097/api/diploma/diploma/step1-registradora-dados -F "document=@diploma-montado.xml" -F "kmsCode=$KMS_REPRESENTANTE_REGISTRADORA" -o diploma-step1.xml
curl -X POST http://localhost:8097/api/diploma/diploma/step2-envelope-final -F "document=@diploma-step1.xml" -F "kmsCode=$KMS_IES_REGISTRADORA" -o diploma-final.xml
```

## Outros métodos de certificação

Para HSM em nuvem ou navegador (PKCS#1), use os mesmos parâmetros nos exemplos genéricos [`exemplo-python-integracao-xml-cloud`](https://github.com/SolidTechSolutions/exemplo-python-integracao-xml-cloud) e [`exemplo-python-integracao-xml-pkcs1`](https://github.com/SolidTechSolutions/exemplo-python-integracao-xml-pkcs1).

## Tratamento de Erros
O sistema loga o JSON detalhado de erro da SolidSign.

---

# 🇬🇧 SolidSign API - Use Case: Digital Diploma (MEC) — Python

Covers all **5 documents** of the MEC Digital Diploma trail, each with its own signers and steps, using KMS-custodied certificates.

## The 5 documents

| # | Document | Endpoints | Signers |
| :-: | :--- | :--- | :--- |
| 1 | Academic Registration Documentation | `documentacao-academica/step{1,2,3}-*` | Institution representatives → Issuing institution data → Issuing institution final envelope |
| 2 | **Digital Diploma** | `diploma/assemble`, `diploma/step{1,2}-*` | *(assembled from doc. 1)* → Registrar representative → Registering institution final envelope |
| 3 | Digital School Transcript | `historico-escolar/step{1,2}-*` | *(partial: step2 only)* Registry representative → Issuing institution final envelope |
| 4 | Digital School Curriculum | `curriculo-escolar/step{1,2}-*` | Course coordinator → Issuing institution — entire document |
| 5 | Annulled Diplomas List / Audit File | `lista-anulados/sign` | Institution — entire document, single step |

## Document 2 — Diploma assembly

`POST /api/diploma/diploma/assemble` copies `<DadosDiploma>` into the Diploma envelope template using Python's standard-library `xml.etree.ElementTree`, returning the **unsigned** Diploma.

## Stack
1. Python 3.10+
2. FastAPI + Uvicorn
3. `xml.etree.ElementTree` (standard library)

## How to Run

```bash
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn main:app --port 8097 --reload
```

## Other certification methods

For cloud HSM or browser (PKCS#1) signing, apply the same parameters to [`exemplo-python-integracao-xml-cloud`](https://github.com/SolidTechSolutions/exemplo-python-integracao-xml-cloud) and [`exemplo-python-integracao-xml-pkcs1`](https://github.com/SolidTechSolutions/exemplo-python-integracao-xml-pkcs1).

## Error Handling
The system logs SolidSign's detailed error JSON.

---

# 🇪🇸 SolidSign API - Caso de Uso: Diploma Digital (MEC) — Python

Cubre los **5 documentos** de la ruta del Diploma Digital del MEC, cada uno con sus propios firmantes y etapas.

## Los 5 documentos

| # | Documento | Endpoints | Firmantes |
| :-: | :--- | :--- | :--- |
| 1 | Documentación Académica de Registro | `documentacao-academica/step{1,2,3}-*` | Representantes de la IES → IES Emisora datos → IES Emisora sobre final |
| 2 | **Diploma Digital** | `diploma/assemble`, `diploma/step{1,2}-*` | *(armado del doc. 1)* → Representante de la Registradora → IES Registradora sobre final |
| 3 | Historial Escolar Digital | `historico-escolar/step{1,2}-*` | *(parcial: solo step2)* Representante de la Secretaría → IES Emisora sobre final |
| 4 | Currículo Escolar Digital | `curriculo-escolar/step{1,2}-*` | Coordinador del Curso → IES Emisora — documento entero |
| 5 | Lista de Diplomas Anulados / Archivo de Fiscalización | `lista-anulados/sign` | Institución — documento entero, etapa única |

## Documento 2 — armado del Diploma

`POST /api/diploma/diploma/assemble` copia `<DadosDiploma>` al template del sobre Diploma usando `xml.etree.ElementTree` (biblioteca estándar de Python), devolviendo el Diploma **sin firmar**.

## Stack
1. Python 3.10+
2. FastAPI + Uvicorn
3. `xml.etree.ElementTree` (biblioteca estándar)

## Cómo Ejecutar

```bash
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn main:app --port 8097 --reload
```

## Otros métodos de certificación

Para HSM en la nube o navegador (PKCS#1), aplique los mismos parámetros a [`exemplo-python-integracao-xml-cloud`](https://github.com/SolidTechSolutions/exemplo-python-integracao-xml-cloud) y [`exemplo-python-integracao-xml-pkcs1`](https://github.com/SolidTechSolutions/exemplo-python-integracao-xml-pkcs1).

## Gestión de Errores
El sistema registra el JSON detallado de errores de SolidSign.
