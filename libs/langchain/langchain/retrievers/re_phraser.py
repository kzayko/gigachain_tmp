import logging
from typing import List

from langchain_core.callbacks import (
    AsyncCallbackManagerForRetrieverRun,
    CallbackManagerForRetrieverRun,
)
from langchain_core.documents import Document
from langchain_core.language_models import BaseLLM
from langchain_core.prompts import BasePromptTemplate
from langchain_core.prompts.prompt import PromptTemplate
from langchain_core.retrievers import BaseRetriever

from langchain.chains.llm import LLMChain

logger = logging.getLogger(__name__)

# Default template
DEFAULT_TEMPLATE = """Ты помощник, задача которого состоит в том, \
чтобы принять запрос на естественном языке от пользователя и \
преобразовать его в запрос для векторного хранилища. \
В этом процессе ты отсеиваешь информацию, которая не имеет отношения \
к задаче извлечения. Вот пользовательский запрос: {question}"""

# Default prompt
DEFAULT_QUERY_PROMPT = PromptTemplate.from_template(DEFAULT_TEMPLATE)


class RePhraseQueryRetriever(BaseRetriever):
    """Given a query, use an LLM to re-phrase it.
    Then, retrieve docs for the re-phrased query."""

    retriever: BaseRetriever
    llm_chain: LLMChain

    @classmethod
    def from_llm(
        cls,
        retriever: BaseRetriever,
        llm: BaseLLM,
        prompt: BasePromptTemplate = DEFAULT_QUERY_PROMPT,
    ) -> "RePhraseQueryRetriever":
        """Initialize from llm using default template.

        The prompt used here expects a single input: `question`

        Args:
            retriever: retriever to query documents from
            llm: llm for query generation using DEFAULT_QUERY_PROMPT
            prompt: prompt template for query generation

        Returns:
            RePhraseQueryRetriever
        """

        llm_chain = LLMChain(llm=llm, prompt=prompt)
        return cls(
            retriever=retriever,
            llm_chain=llm_chain,
        )

    def _get_relevant_documents(
        self,
        query: str,
        *,
        run_manager: CallbackManagerForRetrieverRun,
    ) -> List[Document]:
        """Get relevant documents given a user question.

        Args:
            query: user question

        Returns:
            Relevant documents for re-phrased question
        """
        response = self.llm_chain(query, callbacks=run_manager.get_child())
        re_phrased_question = response["text"]
        logger.info(f"Re-phrased question: {re_phrased_question}")
        docs = self.retriever.invoke(
            re_phrased_question, config={"callbacks": run_manager.get_child()}
        )
        return docs

    async def _aget_relevant_documents(
        self,
        query: str,
        *,
        run_manager: AsyncCallbackManagerForRetrieverRun,
    ) -> List[Document]:
        raise NotImplementedError
