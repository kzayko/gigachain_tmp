"""Methods for creating function specs in the style of OpenAI Functions"""

from __future__ import annotations

import collections
import inspect
import logging
import typing
import uuid
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Dict,
    List,
    Literal,
    Optional,
    Set,
    Tuple,
    Type,
    Union,
    cast,
)

from typing_extensions import Annotated, TypedDict, get_args, get_origin, is_typeddict

from langchain_core._api import deprecated
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, ToolMessage
from langchain_core.pydantic_v1 import BaseModel, Field, create_model
from langchain_core.utils.json_schema import dereference_refs
from langchain_core.utils.pydantic import is_basemodel_subclass

if TYPE_CHECKING:
    from langchain_core.tools import BaseTool

logger = logging.getLogger(__name__)

PYTHON_TO_JSON_TYPES = {
    "str": "string",
    "int": "integer",
    "float": "number",
    "bool": "boolean",
}


class FunctionDescription(TypedDict):
    """Representation of a callable function to send to an LLM."""

    name: str
    """The name of the function."""
    description: str
    """A description of the function."""
    parameters: dict


class GigaFunctionDescription(FunctionDescription):
    """The parameters of the function."""

    return_parameters: Optional[dict]
    """The result settings of the function."""
    few_shot_examples: Optional[list]
    """The examples of the function."""


class ToolDescription(TypedDict):
    """Representation of a callable function to the OpenAI API."""

    type: Literal["function"]
    """The type of the tool."""
    function: FunctionDescription
    """The function description."""


def _rm_titles(kv: dict, prev_key: str = "") -> dict:
    new_kv = {}
    for k, v in kv.items():
        if k == "title":
            if isinstance(v, dict) and prev_key == "properties" and "title" in v.keys():
                new_kv[k] = _rm_titles(v, k)
            else:
                continue
        elif isinstance(v, dict):
            new_kv[k] = _rm_titles(v, k)
        else:
            new_kv[k] = v
    return new_kv


@deprecated(
    "0.1.16",
    alternative="langchain_core.utils.function_calling.convert_to_openai_function()",
    removal="0.3.0",
)
def convert_pydantic_to_openai_function(
    model: Type[BaseModel],
    *,
    name: Optional[str] = None,
    description: Optional[str] = None,
    rm_titles: bool = True,
) -> FunctionDescription:
    """Converts a Pydantic model to a function description for the OpenAI API.

    Args:
        model: The Pydantic model to convert.
        name: The name of the function. If not provided, the title of the schema will be
            used.
        description: The description of the function. If not provided, the description
            of the schema will be used.
        rm_titles: Whether to remove titles from the schema. Defaults to True.

    Returns:
        The function description.
    """
    if hasattr(model, "model_json_schema"):
        schema = model.model_json_schema()  # Pydantic 2
    else:
        schema = model.schema()  # Pydantic 1
    schema = dereference_refs(schema)
    schema.pop("definitions", None)
    title = schema.pop("title", "")
    default_description = schema.pop("description", "")
    return {
        "name": name or title,
        "description": description or default_description,
        "parameters": _rm_titles(schema) if rm_titles else schema,
    }


def _convert_return_schema(
    return_model: Type[BaseModel],
) -> Dict[str, Any]:
    return_schema = dereference_refs(return_model.schema())
    return_schema.pop("definitions", None)
    return_schema.pop("title", None)

    for key in return_schema["properties"]:
        if "type" not in return_schema["properties"][key]:
            return_schema["properties"][key]["type"] = "object"
        if "description" not in return_schema["properties"][key]:
            return_schema["properties"][key]["description"] = ""

    return return_schema


def convert_pydantic_to_gigachat_function(
    model: Type[BaseModel],
    *,
    name: Optional[str] = None,
    description: Optional[str] = None,
    return_model: Optional[Type[BaseModel]] = None,
    few_shot_examples: Optional[List[dict]] = None,
) -> GigaFunctionDescription:
    """Converts a Pydantic model to a function description for the GigaChat API."""
    schema = dereference_refs(model.schema())
    schema.pop("definitions", None)
    title = schema.pop("title", None)
    if "properties" in schema:
        for key in schema["properties"]:
            if "type" not in schema["properties"][key]:
                schema["properties"][key]["type"] = "object"
            if "description" not in schema["properties"][key]:
                schema["properties"][key]["description"] = ""

    if return_model:
        return_schema = _convert_return_schema(return_model)
    else:
        return_schema = None

    return GigaFunctionDescription(
        name=name or title,
        description=description or schema["description"],
        parameters=schema,
        return_parameters=return_schema,
        few_shot_examples=few_shot_examples,
    )


@deprecated(
    "0.1.16",
    alternative="langchain_core.utils.function_calling.convert_to_openai_tool()",
    removal="0.3.0",
)
def convert_pydantic_to_openai_tool(
    model: Type[BaseModel],
    *,
    name: Optional[str] = None,
    description: Optional[str] = None,
) -> ToolDescription:
    """Converts a Pydantic model to a function description for the OpenAI API.

    Args:
        model: The Pydantic model to convert.
        name: The name of the function. If not provided, the title of the schema will be
            used.
        description: The description of the function. If not provided, the description
            of the schema will be used.

    Returns:
        The tool description.
    """
    function = convert_pydantic_to_openai_function(
        model, name=name, description=description
    )
    return {"type": "function", "function": function}


def _get_python_function_name(function: Callable) -> str:
    """Get the name of a Python function."""
    return function.__name__


def convert_python_function_to_gigachat_function(
    function: Callable,
) -> GigaFunctionDescription:
    """Convert a Python function to an GigaChat function-calling API compatible dict.

    Assumes the Python function has type hints and a docstring with a description. If
        the docstring has Google Python style argument descriptions, these will be
        included as well.

    Args:
        function: The Python function to convert.

    Returns:
        The GigaChat function description.
    """
    from langchain_core import tools

    func_name = _get_python_function_name(function)
    model = tools.create_schema_from_function(
        func_name,
        function,
        filter_args=(),
        parse_docstring=True,
        error_on_invalid_docstring=False,
        include_injected=False,
    )
    _return_schema = tools.create_return_schema_from_function(func_name, function)
    return convert_pydantic_to_gigachat_function(
        model,
        name=func_name,
        return_model=_return_schema,
        description=model.__doc__,
    )


@deprecated(
    "0.1.16",
    alternative="langchain_core.utils.function_calling.convert_to_openai_function()",
    removal="0.3.0",
)
def convert_python_function_to_openai_function(
    function: Callable,
) -> FunctionDescription:
    """Convert a Python function to an OpenAI function-calling API compatible dict.

    Assumes the Python function has type hints and a docstring with a description. If
        the docstring has Google Python style argument descriptions, these will be
        included as well.

    Args:
        function: The Python function to convert.

    Returns:
        The OpenAI function description.
    """
    from langchain_core import tools

    func_name = _get_python_function_name(function)
    model = tools.create_schema_from_function(
        func_name,
        function,
        filter_args=(),
        parse_docstring=True,
        error_on_invalid_docstring=False,
        include_injected=False,
    )
    return convert_pydantic_to_openai_function(
        model,
        name=func_name,
        description=model.__doc__,
    )


def _convert_typed_dict_to_openai_function(typed_dict: Type) -> FunctionDescription:
    visited: Dict = {}
    model = cast(
        Type[BaseModel],
        _convert_any_typed_dicts_to_pydantic(typed_dict, visited=visited),
    )
    return convert_pydantic_to_openai_function(model)


_MAX_TYPED_DICT_RECURSION = 25


def _convert_any_typed_dicts_to_pydantic(
    type_: Type,
    *,
    visited: Dict,
    depth: int = 0,
) -> Type:
    if type_ in visited:
        return visited[type_]
    elif depth >= _MAX_TYPED_DICT_RECURSION:
        return type_
    elif is_typeddict(type_):
        typed_dict = type_
        docstring = inspect.getdoc(typed_dict)
        annotations_ = typed_dict.__annotations__
        description, arg_descriptions = _parse_google_docstring(
            docstring, list(annotations_)
        )
        fields: dict = {}
        for arg, arg_type in annotations_.items():
            if get_origin(arg_type) is Annotated:
                annotated_args = get_args(arg_type)
                new_arg_type = _convert_any_typed_dicts_to_pydantic(
                    annotated_args[0], depth=depth + 1, visited=visited
                )
                field_kwargs = {
                    k: v for k, v in zip(("default", "description"), annotated_args[1:])
                }
                if (field_desc := field_kwargs.get("description")) and not isinstance(
                    field_desc, str
                ):
                    raise ValueError(
                        f"Invalid annotation for field {arg}. Third argument to "
                        f"Annotated must be a string description, received value of "
                        f"type {type(field_desc)}."
                    )
                elif arg_desc := arg_descriptions.get(arg):
                    field_kwargs["description"] = arg_desc
                else:
                    pass
                fields[arg] = (new_arg_type, Field(**field_kwargs))
            else:
                new_arg_type = _convert_any_typed_dicts_to_pydantic(
                    arg_type, depth=depth + 1, visited=visited
                )
                field_kwargs = {"default": ...}
                if arg_desc := arg_descriptions.get(arg):
                    field_kwargs["description"] = arg_desc
                fields[arg] = (new_arg_type, Field(**field_kwargs))
        model = create_model(typed_dict.__name__, **fields)
        model.__doc__ = description
        visited[typed_dict] = model
        return model
    elif (origin := get_origin(type_)) and (type_args := get_args(type_)):
        subscriptable_origin = _py_38_safe_origin(origin)
        type_args = tuple(
            _convert_any_typed_dicts_to_pydantic(arg, depth=depth + 1, visited=visited)
            for arg in type_args
        )
        return subscriptable_origin[type_args]
    else:
        return type_


@deprecated(
    "0.1.16",
    alternative="langchain_core.utils.function_calling.convert_to_gigachat_function()",
    removal="0.3.0",
)
def format_tool_to_gigachat_function(tool: BaseTool) -> GigaFunctionDescription:
    """Format tool into the GigaChat function API."""
    if tool.args_schema:
        return convert_pydantic_to_gigachat_function(
            tool.args_schema,
            name=tool.name,
            description=tool.description,
            return_model=tool.return_schema,
            few_shot_examples=tool.few_shot_examples,
        )
    else:
        if tool.return_schema:
            return_schema = _convert_return_schema(tool.return_schema)
        else:
            return_schema = None

        return {
            "name": tool.name,
            "description": tool.description,
            "parameters": {
                "properties": {},
                "type": "object",
            },
            "few_shot_examples": tool.few_shot_examples,
            "return_parameters": return_schema,
        }


@deprecated(
    "0.1.16",
    alternative="langchain_core.utils.function_calling.convert_to_openai_function()",
    removal="0.3.0",
)
def format_tool_to_openai_function(tool: BaseTool) -> FunctionDescription:
    """Format tool into the OpenAI function API.

    Args:
        tool: The tool to format.

    Returns:
        The function description.
    """
    if tool.tool_call_schema:
        return convert_pydantic_to_openai_function(
            tool.tool_call_schema, name=tool.name, description=tool.description
        )
    else:
        return {
            "name": tool.name,
            "description": tool.description,
            "parameters": {
                # This is a hack to get around the fact that some tools
                # do not expose an args_schema, and expect an argument
                # which is a string.
                # And Open AI does not support an array type for the
                # parameters.
                "properties": {
                    "__arg1": {"title": "__arg1", "type": "string"},
                },
                "required": ["__arg1"],
                "type": "object",
            },
        }


@deprecated(
    "0.1.16",
    alternative="langchain_core.utils.function_calling.convert_to_openai_tool()",
    removal="0.3.0",
)
def format_tool_to_openai_tool(tool: BaseTool) -> ToolDescription:
    """Format tool into the OpenAI function API.

    Args:
        tool: The tool to format.

    Returns:
        The tool description.
    """
    function = format_tool_to_openai_function(tool)
    return {"type": "function", "function": function}


def convert_to_openai_function(
    function: Union[Dict[str, Any], Type, Callable, BaseTool],
    *,
    strict: Optional[bool] = None,
) -> Dict[str, Any]:
    """Convert a raw function/class to an OpenAI function.

    .. versionchanged:: 0.2.29

        ``strict`` arg added.

    Args:
        function:
            A dictionary, Pydantic BaseModel class, TypedDict class, a LangChain
            Tool object, or a Python function. If a dictionary is passed in, it is
            assumed to already be a valid OpenAI function or a JSON schema with
            top-level 'title' and 'description' keys specified.
        strict:
            If True, model output is guaranteed to exactly match the JSON Schema
            provided in the function definition. If None, ``strict`` argument will not
            be included in function definition.

            .. versionadded:: 0.2.29

    Returns:
        A dict version of the passed in function which is compatible with the OpenAI
        function-calling API.

    Raises:
        ValueError: If function is not in a supported format.
    """
    from langchain_core.tools import BaseTool

    # already in OpenAI function format
    if isinstance(function, dict) and all(
        k in function for k in ("name", "description", "parameters")
    ):
        oai_function = function
    # a JSON schema with title and description
    elif isinstance(function, dict) and all(
        k in function for k in ("title", "description", "properties")
    ):
        function = function.copy()
        oai_function = {
            "name": function.pop("title"),
            "description": function.pop("description"),
            "parameters": function,
        }
    elif isinstance(function, type) and is_basemodel_subclass(function):
        oai_function = cast(Dict, convert_pydantic_to_openai_function(function))
    elif is_typeddict(function):
        oai_function = cast(
            Dict, _convert_typed_dict_to_openai_function(cast(Type, function))
        )
    elif isinstance(function, BaseTool):
        oai_function = cast(Dict, format_tool_to_openai_function(function))
    elif callable(function):
        oai_function = cast(Dict, convert_python_function_to_openai_function(function))
    else:
        raise ValueError(
            f"Unsupported function\n\n{function}\n\nFunctions must be passed in"
            " as Dict, pydantic.BaseModel, or Callable. If they're a dict they must"
            " either be in OpenAI function format or valid JSON schema with top-level"
            " 'title' and 'description' keys."
        )

    if strict is not None:
        oai_function["strict"] = strict
        # As of 08/06/24, OpenAI requires that additionalProperties be supplied and set
        # to False if strict is True.
        oai_function["parameters"]["additionalProperties"] = False
    return oai_function


def flatten_all_of(schema: Any) -> Any:
    """GigaChat не поддерживает allOf/anyOf, поэтому правим вложенную структуру"""
    if isinstance(schema, dict):
        obj_out: Any = {}
        for k, v in schema.items():
            if k == "title":
                continue
            if k == "allOf":
                obj = flatten_all_of(v[0])
                outer_description = schema.get("description")
                obj_out = {**obj_out, **obj}
                if outer_description:
                    # Внешнее описания приоритетнее внутреннего для ref
                    obj_out["description"] = outer_description
            elif isinstance(v, (list, dict)):
                obj_out[k] = flatten_all_of(v)
            else:
                obj_out[k] = v
        return obj_out
    elif isinstance(schema, list):
        return [flatten_all_of(el) for el in schema]
    else:
        return schema


def convert_to_gigachat_function(
    function: Union[Dict[str, Any], Type[BaseModel], Callable, BaseTool],
) -> Dict[str, Any]:
    """Convert a raw function/class to an OpenAI function.

    Args:
        function: Either a dictionary, a pydantic.BaseModel class, or a Python function.
            If a dictionary is passed in, it is assumed to already be a valid OpenAI
            function.

    Returns:
        A dict version of the passed in function which is compatible with the
            OpenAI function-calling API.
    """
    from langchain_core.tools import BaseTool

    if isinstance(function, dict):
        return function
    elif isinstance(function, type) and issubclass(function, BaseModel):
        function = cast(Dict, convert_pydantic_to_gigachat_function(function))
    elif isinstance(function, BaseTool):
        function = cast(Dict, format_tool_to_gigachat_function(function))
    elif callable(function):
        function = cast(Dict, convert_python_function_to_gigachat_function(function))
    else:
        raise ValueError(
            f"Unsupported function type {type(function)}. Functions must be passed in"
            f" as Dict, pydantic.BaseModel, or Callable."
        )
    return flatten_all_of(function)


def convert_to_openai_tool(
    tool: Union[Dict[str, Any], Type[BaseModel], Callable, BaseTool],
    *,
    strict: Optional[bool] = None,
) -> Dict[str, Any]:
    """Convert a raw function/class to an OpenAI tool.

    .. versionchanged:: 0.2.29

        ``strict`` arg added.

    Args:
        tool:
            Either a dictionary, a pydantic.BaseModel class, Python function, or
            BaseTool. If a dictionary is passed in, it is assumed to already be a valid
            OpenAI tool, OpenAI function, or a JSON schema with top-level 'title' and
            'description' keys specified.
        strict:
            If True, model output is guaranteed to exactly match the JSON Schema
            provided in the function definition. If None, ``strict`` argument will not
            be included in tool definition.

            .. versionadded:: 0.2.29

    Returns:
        A dict version of the passed in tool which is compatible with the
        OpenAI tool-calling API.
    """
    if isinstance(tool, dict) and tool.get("type") == "function" and "function" in tool:
        return tool
    oai_function = convert_to_openai_function(tool, strict=strict)
    oai_tool: Dict[str, Any] = {"type": "function", "function": oai_function}
    return oai_tool


def convert_to_gigachat_tool(
    tool: Union[Dict[str, Any], Type[BaseModel], Callable, BaseTool],
) -> Dict[str, Any]:
    """Convert a raw function/class to an GigaChat tool.

    Args:
        tool: Either a dictionary, a pydantic.BaseModel class, Python function, or
            BaseTool. If a dictionary is passed in, it is assumed to already be a valid
            GigaChat tool, GigaChat function,
            or a JSON schema with top-level 'title' and
            'description' keys specified.

    Returns:
        A dict version of the passed in tool which is compatible with the
            GigaChat tool-calling API.
    """
    if isinstance(tool, dict) and tool.get("type") == "function" and "function" in tool:
        return tool
    function = convert_to_gigachat_function(tool)
    return {"type": "function", "function": function}


def tool_example_to_messages(
    input: str, tool_calls: List[BaseModel], tool_outputs: Optional[List[str]] = None
) -> List[BaseMessage]:
    """Convert an example into a list of messages that can be fed into an LLM.

    This code is an adapter that converts a single example to a list of messages
    that can be fed into a chat model.

    The list of messages per example corresponds to:

    1) HumanMessage: contains the content from which content should be extracted.
    2) AIMessage: contains the extracted information from the model
    3) ToolMessage: contains confirmation to the model that the model requested a tool
        correctly.

    The ToolMessage is required because some chat models are hyper-optimized for agents
    rather than for an extraction use case.

    Arguments:
        input: string, the user input
        tool_calls: List[BaseModel], a list of tool calls represented as Pydantic
            BaseModels
        tool_outputs: Optional[List[str]], a list of tool call outputs.
            Does not need to be provided. If not provided, a placeholder value
            will be inserted. Defaults to None.

    Returns:
        A list of messages

    Examples:

        .. code-block:: python

            from typing import List, Optional
            from langchain_core.pydantic_v1 import BaseModel, Field
            from langchain_openai import ChatOpenAI

            class Person(BaseModel):
                '''Information about a person.'''
                name: Optional[str] = Field(..., description="The name of the person")
                hair_color: Optional[str] = Field(
                    ..., description="The color of the person's hair if known"
                )
                height_in_meters: Optional[str] = Field(
                    ..., description="Height in METERs"
                )

            examples = [
                (
                    "The ocean is vast and blue. It's more than 20,000 feet deep.",
                    Person(name=None, height_in_meters=None, hair_color=None),
                ),
                (
                    "Fiona traveled far from France to Spain.",
                    Person(name="Fiona", height_in_meters=None, hair_color=None),
                ),
            ]


            messages = []

            for txt, tool_call in examples:
                messages.extend(
                    tool_example_to_messages(txt, [tool_call])
                )
    """
    messages: List[BaseMessage] = [HumanMessage(content=input)]
    openai_tool_calls = []
    for tool_call in tool_calls:
        openai_tool_calls.append(
            {
                "id": str(uuid.uuid4()),
                "type": "function",
                "function": {
                    # The name of the function right now corresponds to the name
                    # of the pydantic model. This is implicit in the API right now,
                    # and will be improved over time.
                    "name": tool_call.__class__.__name__,
                    "arguments": tool_call.json(),
                },
            }
        )
    messages.append(
        AIMessage(content="", additional_kwargs={"tool_calls": openai_tool_calls})
    )
    tool_outputs = tool_outputs or ["You have correctly called this tool."] * len(
        openai_tool_calls
    )
    for output, tool_call_dict in zip(tool_outputs, openai_tool_calls):
        messages.append(ToolMessage(content=output, tool_call_id=tool_call_dict["id"]))  # type: ignore
    return messages


def _parse_google_docstring(
    docstring: Optional[str],
    args: List[str],
    *,
    error_on_invalid_docstring: bool = False,
) -> Tuple[str, dict]:
    """Parse the function and argument descriptions from the docstring of a function.

    Assumes the function docstring follows Google Python style guide.
    """
    if docstring:
        docstring_blocks = docstring.split("\n\n")
        if error_on_invalid_docstring:
            filtered_annotations = {
                arg for arg in args if arg not in ("run_manager", "callbacks", "return")
            }
            if filtered_annotations and (
                len(docstring_blocks) < 2 or not docstring_blocks[1].startswith("Args:")
            ):
                raise ValueError("Found invalid Google-Style docstring.")
        descriptors = []
        args_block = None
        past_descriptors = False
        for block in docstring_blocks:
            if block.startswith("Args:"):
                args_block = block
                break
            elif block.startswith("Returns:") or block.startswith("Example:"):
                # Don't break in case Args come after
                past_descriptors = True
            elif not past_descriptors:
                descriptors.append(block)
            else:
                continue
        description = " ".join(descriptors)
    else:
        if error_on_invalid_docstring:
            raise ValueError("Found invalid Google-Style docstring.")
        description = ""
        args_block = None
    arg_descriptions = {}
    if args_block:
        arg = None
        for line in args_block.split("\n")[1:]:
            if ":" in line:
                arg, desc = line.split(":", maxsplit=1)
                arg_descriptions[arg.strip()] = desc.strip()
            elif arg:
                arg_descriptions[arg.strip()] += " " + line.strip()
    return description, arg_descriptions


def _py_38_safe_origin(origin: Type) -> Type:
    origin_map: Dict[Type, Any] = {
        dict: Dict,
        list: List,
        tuple: Tuple,
        set: Set,
        collections.abc.Iterable: typing.Iterable,
        collections.abc.Mapping: typing.Mapping,
        collections.abc.Sequence: typing.Sequence,
        collections.abc.MutableMapping: typing.MutableMapping,
    }
    return cast(Type, origin_map.get(origin, origin))
