import logging

from dependency_injector import containers, providers

from db.chroma_client import ChromaDBHandler
from gptclients.gpt_client import OpenAIClient
from services.pdf.pdf_processor import PDFProcessor
from services.pdf.pdf_service import PDFService
from services.rag.retrieval_service import RetrievalService
from util.pdf_to_text import PDFTextConverter


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()
    logger = providers.Singleton(logging.getLogger, __name__)
    gpt_client = providers.Singleton(OpenAIClient)
    chroma = providers.Singleton(ChromaDBHandler)
    retrieval_service = providers.Factory(RetrievalService, chroma_client=chroma, gpt_client=gpt_client)
    converter = providers.Factory(PDFTextConverter, chroma_client=chroma,gpt_client=gpt_client)
    pdf_service = providers.Factory(
        PDFService,
        converter=converter,
        upload_folder=config.upload_folder,
        allowed_extensions=config.allowed_extensions
    )
    pdf_processor = providers.Factory(PDFProcessor, pdf_service)
