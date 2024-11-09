import logging
import os

from dependency_injector import containers, providers
from langchain_ollama import OllamaEmbeddings

from db.chroma_client import ChromaDBHandler
from gptclients.ollama import OllamaClient
from services.pdf.pdf_processor import PDFProcessor
from services.pdf.pdf_service import PDFService
from services.rag.retrieval_service import RetrievalService
from util.pdf_to_text import PDFTextConverter


class Container(containers.DeclarativeContainer):
  config = providers.Configuration()

  logger = providers.Singleton(logging.getLogger, __name__)
  embeddings = providers.Singleton(OllamaEmbeddings,
                                   model=os.environ.get("MODEL_NAME"))
  gpt_client = providers.Singleton(OllamaClient)
  chroma = providers.Singleton(ChromaDBHandler)
  retrieval_service = providers.Factory(RetrievalService, chroma_client=chroma,
                                        embeddings_model=embeddings, gpt_client= gpt_client)
  converter = providers.Factory(PDFTextConverter, chroma_client=chroma,
                                embeddings_model=embeddings)
  pdf_service = providers.Factory(
      PDFService,
      converter=converter,
      upload_folder=config.upload_folder,
      allowed_extensions=config.allowed_extensions
  )
  pdf_processor = providers.Factory(PDFProcessor, pdf_service)
