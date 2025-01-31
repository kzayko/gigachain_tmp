
# rag-vectara

This template performs RAG with vectara.

## Environment Setup

Also, ensure the following environment variables are set:
* `VECTARA_CUSTOMER_ID`
* `VECTARA_CORPUS_ID`
* `VECTARA_API_KEY`

## Usage

To use this package, you should first have the LangChain CLI installed:

```shell
pip install -U gigachain-cli
```

To create a new LangChain project and install this as the only package, you can do:

```shell
gigachain app new my-app --package rag-vectara
```

If you want to add this to an existing project, you can just run:

```shell
gigachain app add rag-vectara
```

And add the following code to your `server.py` file:
```python
from rag_vectara import chain as rag_vectara_chain

add_routes(app, rag_vectara_chain, path="/rag-vectara")
```

(Optional) Let's now configure LangSmith. 
LangSmith will help us trace, monitor and debug LangChain applications. 
You can sign up for LangSmith [here](https://smith.langchain.com/). 
If you don't have access, you can skip this section


```shell
export LANGCHAIN_TRACING_V2=true
export LANGCHAIN_API_KEY=<your-api-key>
export LANGCHAIN_PROJECT=<your-project>  # if not specified, defaults to "vectara-demo"
```

If you are inside this directory, then you can spin up a LangServe instance directly by:

```shell
gigachain serve
```

This will start the FastAPI app with a server is running locally at 
[http://localhost:8000](http://localhost:8000)

We can see all templates at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
We can access the playground at [http://127.0.0.1:8000/rag-vectara/playground](http://127.0.0.1:8000/rag-vectara/playground)  

We can access the template from code with:

```python
from langserve.client import RemoteRunnable

runnable = RemoteRunnable("http://localhost:8000/rag-vectara")
```
