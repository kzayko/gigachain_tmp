# openai-functions-tool-retrieval-agent

The novel idea introduced in this template is the idea of using retrieval to select the set of tools to use to answer an agent query. This is useful when you have many many tools to select from. You cannot put the description of all the tools in the prompt (because of context length issues) so instead you dynamically select the N tools you do want to consider using at run time.

In this template we will create a somewhat contrived example. We will have one legitimate tool (search) and then 99 fake tools which are just nonsense. We will then add a step in the prompt template that takes the user input and retrieves tool relevant to the query.

This template is based on [this Agent How-To](https://python.langchain.com/v0.2/docs/templates/openai-functions-agent/).

## Environment Setup

The following environment variables need to be set:

Set the `OPENAI_API_KEY` environment variable to access the OpenAI models.

Set the `TAVILY_API_KEY` environment variable to access Tavily.

## Usage

To use this package, you should first have the LangChain CLI installed:

```shell
pip install -U gigachain-cli
```

To create a new LangChain project and install this as the only package, you can do:

```shell
langchain app new my-app --package openai-functions-tool-retrieval-agent
```

If you want to add this to an existing project, you can just run:

```shell
langchain app add openai-functions-tool-retrieval-agent
```

And add the following code to your `server.py` file:
```python
from openai_functions_tool_retrieval_agent import agent_executor as openai_functions_tool_retrieval_agent_chain

add_routes(app, openai_functions_tool_retrieval_agent_chain, path="/openai-functions-tool-retrieval-agent")
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
langchain serve
```

This will start the FastAPI app with a server is running locally at 
[http://localhost:8000](http://localhost:8000)

We can see all templates at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
We can access the playground at [http://127.0.0.1:8000/openai-functions-tool-retrieval-agent/playground](http://127.0.0.1:8000/openai-functions-tool-retrieval-agent/playground)  

We can access the template from code with:

```python
from langserve.client import RemoteRunnable

runnable = RemoteRunnable("http://localhost:8000/openai-functions-tool-retrieval-agent")
```
