import asyncio
import json
import os

from doctran import Doctran
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import PyPDFLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.schema import Document
from langchain.vectorstores import FAISS


class PDFProcessor:

    def __init__(self):
        self.loaded_content = None
        self.qa_db = None
        api_key = os.getenv("OPENAI_API_KEY")
        self.OPENAI_MODEL = "gpt-4"
        self.OPENAI_TOKEN_LIMIT = 8000
        self.embeddings = OpenAIEmbeddings(openai_api_key=api_key)
        self.doctran = Doctran(openai_api_key=api_key)
        self.docs = []
        self.qa_db = None
        self.qa=None
        self.qa_docs=[]
        self.chat_history = []

    def load_pdf(self, pdf_path):
        try:
            loader = PyPDFLoader(pdf_path)
            document_content = loader.load_and_split()
            self.loaded_content = document_content

            return True  # No hay error

        except Exception as e:
            # Captura cualquier excepción y proporciona información sobre el error
            error_message = f"Error al cargar el PDF: {str(e)}"
            return False

    async def process_loaded_pdf_async(self):
        try:

            for tes in self.loaded_content[:5]:
                text = tes.page_content
                doc = self.doctran.parse(content=text)
                self.docs.append(await doc.interrogate().execute())
            qa_docs = []
            for doc in self.docs:
                self.qa_docs.extend([Document(page_content=json.dumps(qa), metadata={"raw_text": doc.raw_content}) for qa in
                                doc.extracted_properties["questions_and_answers"]])

            qa_db = FAISS.from_documents(self.qa_docs, self.embeddings)
            # create conversation chain
            self.qa = self.get_conversation_chain(qa_db)
            return True  # No hay error

        except Exception as e:
            # Captura el error
            error_message = f"Error al cargar el PDF: {str(e)}"
            return False

    def process_loaded_pdf(self):
        # Inicia el bucle de eventos de asyncio
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        # Ejecuta la función asíncrona en el bucle de eventos
        result = loop.run_until_complete(self.process_loaded_pdf_async())

        # Cierra el bucle de eventos
        loop.close()

        return result

    def get_conversation_chain(self, vectorstore):
        print("get_conversation_chain")
        llm = ChatOpenAI(temperature=0, model_name='gpt-3.5-turbo')
        qa = ConversationalRetrievalChain.from_llm(llm=llm, retriever=vectorstore.as_retriever(search_kwargs={'k': 2}),
                                                   return_source_documents=False, verbose=False)
        return qa

    def bot_response(self, query):

        result = self.qa({"question": query, "chat_history": self.chat_history})

        return result.get("answer")
