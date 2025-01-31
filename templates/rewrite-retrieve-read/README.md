
# rewrite_retrieve_read

This template implemenets a method for query transformation (re-writing) in the paper [Query Rewriting for Retrieval-Augmented Large Language Models](https://arxiv.org/pdf/2305.14283.pdf) to optimize for RAG. 

## Environment Setup

Set the `OPENAI_API_KEY` environment variable to access the OpenAI models.

## Usage

To use this package, you should first have the LangChain CLI installed:

```shell
pip install -U gigachain-cli
```

To create a new LangChain project and install this as the only package, you can do:

```shell
gigachain app new my-app --package rewrite_retrieve_read
```

If you want to add this to an existing project, you can just run:

```shell
gigachain app add rewrite_retrieve_read
```

And add the following code to your `server.py` file:
```python
from rewrite_retrieve_read.chain import chain as rewrite_retrieve_read_chain

add_routes(app, rewrite_retrieve_read_chain, path="/rewrite-retrieve-read")
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
We can access the playground at [http://127.0.0.1:8000/rewrite_retrieve_read/playground](http://127.0.0.1:8000/rewrite_retrieve_read/playground)  

We can access the template from code with:

```python
from langserve.client import RemoteRunnable

runnable = RemoteRunnable("http://localhost:8000/rewrite_retrieve_read")
```
