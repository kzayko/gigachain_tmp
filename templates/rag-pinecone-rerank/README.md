
# rag-pinecone-rerank

This template performs RAG using Pinecone and OpenAI along with [Cohere to perform re-ranking](https://txt.cohere.com/rerank/) on returned documents. 

Re-ranking provides a way to rank retrieved documents using specified filters or criteria.

## Environment Setup

This template uses Pinecone as a vectorstore and requires that `PINECONE_API_KEY`, `PINECONE_ENVIRONMENT`, and `PINECONE_INDEX` are set. 

Set the `OPENAI_API_KEY` environment variable to access the OpenAI models.

Set the `COHERE_API_KEY` environment variable to access the Cohere ReRank.

## Usage

To use this package, you should first have the LangChain CLI installed:

```shell
pip install -U gigachain-cli
```

To create a new LangChain project and install this as the only package, you can do:

```shell
gigachain app new my-app --package rag-pinecone-rerank
```

If you want to add this to an existing project, you can just run:

```shell
gigachain app add rag-pinecone-rerank
```

And add the following code to your `server.py` file:
```python
from rag_pinecone_rerank import chain as rag_pinecone_rerank_chain

add_routes(app, rag_pinecone_rerank_chain, path="/rag-pinecone-rerank")
```

(Optional) Let's now configure LangSmith. 
LangSmith will help us trace, monitor and debug LangChain applications. 
You can sign up for LangSmith [here](https://smith.langchain.com/). 
If you don't have access, you can skip this section


```shell
export LANGCHAIN_TRACING_V2=true
export LANGCHAIN_API_KEY=<your-api-key>
export LANGCHAIN_PROJECT=<your-project>  # if not specified, defaults to "default"
```

If you are inside this directory, then you can spin up a LangServe instance directly by:

```shell
gigachain serve
```

This will start the FastAPI app with a server is running locally at 
[http://localhost:8000](http://localhost:8000)

We can see all templates at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
We can access the playground at [http://127.0.0.1:8000/rag-pinecone-rerank/playground](http://127.0.0.1:8000/rag-pinecone-rerank/playground)  

We can access the template from code with:

```python
from langserve.client import RemoteRunnable

runnable = RemoteRunnable("http://localhost:8000/rag-pinecone-rerank")
```
