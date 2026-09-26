"""
[EN]    Signs the Diploma Digital XML at a specific stage of the MEC "Diploma Digital" flow
        using a SolidSign KMS-custodied certificate (POST /solidsign/dsig/xml/sign-kms).
        Each stage corresponds to a different real-world signer role and is exposed as an
        isolated endpoint in main.py — this service does not chain the 3 stages together,
        since each one is normally executed by a different signer/system.

[PT-BR] Assina o XML do Diploma Digital em uma etapa específica do fluxo do MEC "Diploma
        Digital" via KMS SolidSign. Cada etapa corresponde a um papel real de assinante
        distinto e é exposta como um endpoint isolado em main.py.
"""

import logging
import os
from typing import Optional

import requests
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)


class DiplomaSigningService:

    def __init__(self):
        self.base_url = os.getenv("SOLIDSIGN_API_BASE_URL", "").rstrip("/")
        self.authorization = os.getenv("SOLIDSIGN_API_AUTHORIZATION", "")
        self.hash_algorithm = os.getenv("SOLIDSIGN_DIPLOMA_HASH_ALGORITHM", "SHA256")
        self.signature_packaging = os.getenv("SOLIDSIGN_DIPLOMA_SIGNATURE_PACKAGING", "ENVELOPED")
        self.canonicalization_method = os.getenv("SOLIDSIGN_DIPLOMA_CANONICALIZATION_METHOD", "EXCLUSIVE")

    def _step_config(self, step: int) -> dict:
        prefix = f"SOLIDSIGN_DIPLOMA_STEP{step}_"
        return {
            "node_name": os.getenv(prefix + "NODE_NAME", ""),
            "namespace": os.getenv(prefix + "NAMESPACE", ""),
            "profile": os.getenv(prefix + "PROFILE", ""),
            "remove_xpath_filter": os.getenv(prefix + "REMOVE_XPATH_FILTER", "false"),
        }

    def sign_step1_representante(self, content: bytes, filename: str, kms_code: str) -> Optional[bytes]:
        return self._sign(1, content, filename, kms_code)

    def sign_step2_emissora_dados(self, content: bytes, filename: str, kms_code: str) -> Optional[bytes]:
        return self._sign(2, content, filename, kms_code)

    def sign_step3_envelope_final(self, content: bytes, filename: str, kms_code: str) -> Optional[bytes]:
        return self._sign(3, content, filename, kms_code)

    def _sign(self, step: int, content: bytes, filename: str, kms_code: str) -> Optional[bytes]:
        """
        [EN]    Calls SolidSign's XML KMS signing endpoint for a single document and returns the
                signed XML bytes downloaded from the response link.
        [PT-BR] Chama o endpoint de assinatura XML via KMS da SolidSign para um único documento e
                retorna os bytes do XML assinado baixados do link da resposta.
        """
        cfg = self._step_config(step)
        sign_url = self.base_url + "/solidsign/dsig/xml/sign-kms"
        headers = {"Authorization": self.authorization}

        files = {"document[0]": (filename, content, "application/xml")}
        data = {
            "kmsCode": kms_code,
            "profile": cfg["profile"],
            "hashAlgorithm": self.hash_algorithm,
            "signaturePackaging": self.signature_packaging,
            "canonicalizationMethod": self.canonicalization_method,
            "signatureNodeName[0]": cfg["node_name"],
            "signatureNodeNamespace[0]": cfg["namespace"],
            "isRemoveXPathExclusionFilter": cfg["remove_xpath_filter"],
        }

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
            if dl.status_code == 200:
                return dl.content
            return None

        except requests.HTTPError as e:
            logger.error("SolidSign API error %s: %s", e.response.status_code, e.response.text)
        except Exception as e:
            logger.error("Unexpected error during Diploma signing: %s", e)

        return None
