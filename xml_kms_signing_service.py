"""
[EN]    Generic single-document XAdES signing call via a SolidSign KMS-custodied certificate
        (POST /solidsign/dsig/xml/sign-kms). Shared by every document/step of the Diploma
        Digital use case; when node_name is falsy, the whole document is signed (no
        signatureNodeName/signatureNodeNamespace sent).

[PT-BR] Chamada genérica de assinatura XAdES via certificado custodiado no KMS da SolidSign.
        Compartilhada por todos os documentos/etapas; quando node_name é vazio, o documento
        inteiro é assinado.
"""

import logging
import os
from typing import Optional

import requests

logger = logging.getLogger(__name__)


def sign(
    content: bytes, filename: str, kms_code: str,
    node_name: Optional[str], namespace: Optional[str], profile: str, remove_xpath_filter: bool,
) -> Optional[bytes]:
    base_url = os.getenv("SOLIDSIGN_API_BASE_URL", "").rstrip("/")
    authorization = os.getenv("SOLIDSIGN_API_AUTHORIZATION", "")
    hash_algorithm = os.getenv("SOLIDSIGN_DIPLOMA_HASH_ALGORITHM", "SHA256")
    signature_packaging = os.getenv("SOLIDSIGN_DIPLOMA_SIGNATURE_PACKAGING", "ENVELOPED")
    canonicalization_method = os.getenv("SOLIDSIGN_DIPLOMA_CANONICALIZATION_METHOD", "EXCLUSIVE")

    sign_url = base_url + "/solidsign/dsig/xml/sign-kms"
    headers = {"Authorization": authorization}
    files = {"document[0]": (filename, content, "application/xml")}
    data = {
        "kmsCode": kms_code,
        "profile": profile,
        "hashAlgorithm": hash_algorithm,
        "signaturePackaging": signature_packaging,
        "canonicalizationMethod": canonicalization_method,
        "isRemoveXPathExclusionFilter": "true" if remove_xpath_filter else "false",
    }
    if node_name:
        data["signatureNodeName[0]"] = node_name
        data["signatureNodeNamespace[0]"] = namespace or ""

    try:
        resp = requests.post(sign_url, headers=headers, files=files, data=data, timeout=120)
        resp.raise_for_status()
        sign_resp = resp.json()

        documents = sign_resp.get("documents", [])
        if not documents:
            logger.error("SolidSign response had no documents.")
            return None

        doc = documents[0]
        links_obj = doc.get("_links") or {}
        download_url = (links_obj.get("self") or {}).get("href")
        if not download_url:
            download_url = next(
                (lnk["href"] for lnk in doc.get("links", []) if lnk.get("rel") == "self"), None,
            )
        if not download_url:
            logger.error("SolidSign response had no download link.")
            return None

        dl = requests.get(download_url, headers=headers, timeout=120)
        return dl.content if dl.status_code == 200 else None

    except requests.HTTPError as e:
        logger.error("SolidSign API error %s: %s", e.response.status_code, e.response.text)
    except Exception as e:
        logger.error("Unexpected error during signing: %s", e)

    return None
