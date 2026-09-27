"""
[EN]    Assembles the Diploma XML by copying the (already signed) <DadosDiploma> node out of
        the Documentação Acadêmica de Registro document and inserting it into the Diploma
        envelope template (templates/diploma-template.xml), right before <DadosRegistro>.
        Result is an UNSIGNED Diploma XML.

[PT-BR] Monta o XML do Diploma copiando o nó <DadosDiploma> (já assinado) de dentro do
        documento de Documentação Acadêmica de Registro e inserindo-o no template do envelope
        Diploma, logo antes de <DadosRegistro>. O resultado é um XML AINDA NÃO ASSINADO.
"""

import copy
import logging
import os
import xml.etree.ElementTree as ET
from typing import Optional

logger = logging.getLogger(__name__)

MEC_NAMESPACE = "http://portal.mec.gov.br/diplomadigital/arquivos-em-xsd"
TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), "templates", "diploma-template.xml")

ET.register_namespace("", MEC_NAMESPACE)


def _find_by_local_name(root: ET.Element, local_name: str) -> Optional[ET.Element]:
    for elem in root.iter():
        if elem.tag.split("}")[-1] == local_name:
            return elem
    return None


def assemble(signed_documentacao_academica_xml: bytes) -> Optional[bytes]:
    try:
        academic_root = ET.fromstring(signed_documentacao_academica_xml)
        dados_diploma = _find_by_local_name(academic_root, "DadosDiploma")
        if dados_diploma is None:
            logger.error("Could not find <DadosDiploma> in the supplied Documentação Acadêmica document.")
            return None

        diploma_tree = ET.parse(TEMPLATE_PATH)
        diploma_root = diploma_tree.getroot()
        dados_registro = _find_by_local_name(diploma_root, "DadosRegistro")
        if dados_registro is None:
            logger.error("Diploma template is missing <DadosRegistro>.")
            return None

        inf_diploma = _find_parent(diploma_root, dados_registro)
        index = list(inf_diploma).index(dados_registro)
        inf_diploma.insert(index, copy.deepcopy(dados_diploma))

        return ET.tostring(diploma_root, encoding="utf-8", xml_declaration=True)
    except Exception as e:
        logger.error("Unexpected error assembling the Diploma XML: %s", e)
        return None


def _find_parent(root: ET.Element, target: ET.Element) -> Optional[ET.Element]:
    for elem in root.iter():
        if target in list(elem):
            return elem
    return None
