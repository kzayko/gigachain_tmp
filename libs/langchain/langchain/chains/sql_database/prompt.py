# flake8: noqa
from langchain_core.output_parsers.list import CommaSeparatedListOutputParser
from langchain_core.prompts.prompt import PromptTemplate


PROMPT_SUFFIX = """Используйте только следующие таблицы:
{table_info}

Question: {input}"""

_DEFAULT_TEMPLATE = """По заданному вопросу сначала создайте синтаксически правильный запрос на {dialect}, затем просмотрите результаты запроса и верните ответ. Если пользователь не указывает конкретное количество примеров, которые он хочет получить, всегда ограничивайте свой запрос не более чем {top_k} результатами. Вы можете упорядочить результаты по соответствующему столбцу, чтобы вернуть наиболее интересные примеры в базе данных.

Никогда не запрашивайте все столбцы из конкретной таблицы, запрашивайте только несколько необходимых столбцов, исходя из вопроса.

Обратите внимание, что используются только имена столбцов, которые вы видите в описании схемы. Будьте внимательны, чтобы не запрашивать столбцы, которых не существует. Также обратите внимание, какой столбец находится в какой таблице.

Используйте следующий формат:

Question: Вопрос
SQLQuery: SQL-запрос для выполнения
SQLResult: Разультат выполнения запроса
Answer: Итоговый ответ

"""

PROMPT = PromptTemplate(
    input_variables=["input", "table_info", "dialect", "top_k"],
    template=_DEFAULT_TEMPLATE + PROMPT_SUFFIX,
)


_DECIDER_TEMPLATE = """По заданному вопросу и списку потенциальных таблиц выведите список имен таблиц, разделенных запятыми, которые могут понадобиться для ответа на этот вопрос.

Question: {query}

Имена таблиц: {table_names}

Соответствующие имена таблиц:"""
DECIDER_PROMPT = PromptTemplate(
    input_variables=["query", "table_names"],
    template=_DECIDER_TEMPLATE,
    output_parser=CommaSeparatedListOutputParser(),
)

_cratedb_prompt = """Вы являетесь экспертом по CrateDB. По заданному вопросу сначала создайте синтаксически правильный запрос CrateDB для выполнения, затем просмотрите результаты запроса и верните ответ на входной вопрос.
Если пользователь не указывает в вопросе конкретное количество примеров для получения, запрашивайте не более {top_k} результатов, используя ключевое слово LIMIT, как в CrateDB. Вы можете упорядочить результаты, чтобы вернуть наиболее информативные данные в базе данных.
Никогда не запрашивайте все столбцы из таблицы. Вы должны запрашивать только те столбцы, которые необходимы для ответа на вопрос. Оберните каждое имя столбца в двойные кавычки (") для обозначения их как ограниченных идентификаторов.
Обратите внимание, что используются только имена столбцов, которые вы видите в таблицах ниже. Будьте внимательны, чтобы не запрашивать столбцы, которых не существует. Также обратите внимание, какой столбец находится в какой таблице.
Обратите внимание, что для получения текущей даты, если вопрос связан с "сегодня", используйте функцию CURRENT_DATE.

Regenerate

Use the following format:

Question: Вопрос
SQLQuery: SQL-запрос для выполнения
SQLResult: Разультат выполнения запроса
Answer: Итоговый ответ

"""

CRATEDB_PROMPT = PromptTemplate(
    input_variables=["input", "table_info", "top_k"],
    template=_cratedb_prompt + PROMPT_SUFFIX,
)

_duckdb_prompt = """Вы являетесь экспертом по DuckDB. По заданному вопросу сначала создайте синтаксически правильный запрос DuckDB для выполнения, затем просмотрите результаты запроса и верните ответ на входной вопрос.
Если пользователь не указывает в вопросе конкретное количество примеров для получения, запрашивайте не более {top_k} результатов, используя ключевое слово LIMIT, как в DuckDB. Вы можете упорядочить результаты, чтобы вернуть наиболее информативные данные в базе данных.
Никогда не запрашивайте все столбцы из таблицы. Вы должны запрашивать только те столбцы, которые необходимы для ответа на вопрос. Оберните каждое имя столбца в двойные кавычки (") для обозначения их как ограниченных идентификаторов.
Обратите внимание, что используются только имена столбцов, которые вы видите в таблицах ниже. Будьте внимательны, чтобы не запрашивать столбцы, которых не существует. Также обратите внимание, какой столбец находится в какой таблице.
Обратите внимание, что для получения текущей даты, если вопрос связан с "сегодня", используйте функцию today.

Используйте следующий формат:

Question: Вопрос
SQLQuery: SQL-запрос для выполнения
SQLResult: Разультат выполнения запроса
Answer: Итоговый ответ

"""

CRATEDB_PROMPT = PromptTemplate(
    input_variables=["input", "table_info", "top_k"],
    template=_cratedb_prompt + PROMPT_SUFFIX,
)

_duckdb_prompt = """Вы являетесь экспертом по DuckDB. По заданному вопросу сначала создайте синтаксически правильный запрос DuckDB для выполнения, затем просмотрите результаты запроса и верните ответ на входной вопрос.
Если пользователь не указывает в вопросе конкретное количество примеров для получения, запрашивайте не более {top_k} результатов, используя ключевое слово LIMIT, как в DuckDB. Вы можете упорядочить результаты, чтобы вернуть наиболее информативные данные в базе данных.
Никогда не запрашивайте все столбцы из таблицы. Вы должны запрашивать только те столбцы, которые необходимы для ответа на вопрос. Оберните каждое имя столбца в двойные кавычки (") для обозначения их как ограниченных идентификаторов.
Обратите внимание, что используются только имена столбцов, которые вы видите в таблицах ниже. Будьте внимательны, чтобы не запрашивать столбцы, которых не существует. Также обратите внимание, какой столбец находится в какой таблице.
Обратите внимание, что для получения текущей даты, если вопрос связан с "сегодня", используйте функцию today.

Используйте следующий формат:

Question: Вопрос
SQLQuery: SQL-запрос для выполнения
SQLResult: Разультат выполнения запроса
Answer: Итоговый ответ

"""

DUCKDB_PROMPT = PromptTemplate(
    input_variables=["input", "table_info", "top_k"],
    template=_duckdb_prompt + PROMPT_SUFFIX,
)

_googlesql_prompt = """Вы являетесь экспертом по GoogleSQL. По заданному вопросу сначала создайте синтаксически правильный запрос GoogleSQL для выполнения, затем просмотрите результаты запроса и верните ответ на входной вопрос.
Если пользователь не указывает в вопросе конкретное количество примеров для получения, запрашивайте не более {top_k} результатов, используя ключевое слово LIMIT, как в GoogleSQL. Вы можете упорядочить результаты, чтобы вернуть наиболее информативные данные в базе данных.
Никогда не запрашивайте все столбцы из таблицы. Вы должны запрашивать только те столбцы, которые необходимы для ответа на вопрос. Оберните каждое имя столбца в обратные кавычки (`) для обозначения их как ограниченных идентификаторов.
Обратите внимание, что используются только имена столбцов, которые вы видите в таблицах ниже. Будьте внимательны, чтобы не запрашивать столбцы, которых не существует. Также обратите внимание, какой столбец находится в какой таблице.
Обратите внимание, что для получения текущей даты, если вопрос связан с "сегодня", используйте функцию CURRENT_DATE().

Используйте следующий формат:

Question: Вопрос
SQLQuery: SQL-запрос для выполнения
SQLResult: Разультат выполнения запроса
Answer: Итоговый ответ

"""

GOOGLESQL_PROMPT = PromptTemplate(
    input_variables=["input", "table_info", "top_k"],
    template=_googlesql_prompt + PROMPT_SUFFIX,
)


_mssql_prompt = """Вы являетесь экспертом по MS SQL. По заданному вопросу сначала создайте синтаксически правильный запрос MS SQL для выполнения, затем просмотрите результаты запроса и верните ответ на входной вопрос.
Если пользователь не указывает в вопросе конкретное количество примеров для получения, запрашивайте не более {top_k} результатов, используя ключевое слово TOP, как в MS SQL. Вы можете упорядочить результаты, чтобы вернуть наиболее информативные данные в базе данных.
Никогда не запрашивайте все столбцы из таблицы. Вы должны запрашивать только те столбцы, которые необходимы для ответа на вопрос. Оберните каждое имя столбца в квадратные скобки ([]) для обозначения их как ограниченных идентификаторов.
Обратите внимание, что используются только имена столбцов, которые вы видите в таблицах ниже. Будьте внимательны, чтобы не запрашивать столбцы, которых не существует. Также обратите внимание, какой столбец находится в какой таблице.
Обратите внимание, что для получения текущей даты, если вопрос связан с "сегодня", используйте функцию CAST(GETDATE() as date).

Используйте следующий формат:

Question: Вопрос
SQLQuery: SQL-запрос для выполнения
SQLResult: Разультат выполнения запроса
Answer: Итоговый ответ

"""

MSSQL_PROMPT = PromptTemplate(
    input_variables=["input", "table_info", "top_k"],
    template=_mssql_prompt + PROMPT_SUFFIX,
)


_mysql_prompt = """Вы являетесь экспертом по MySQL. По заданному вопросу сначала создайте синтаксически правильный запрос MySQL для выполнения, затем просмотрите результаты запроса и верните ответ на входной вопрос.
Если пользователь не указывает в вопросе конкретное количество примеров для получения, запрашивайте не более {top_k} результатов, используя ключевое слово LIMIT, как в MySQL. Вы можете упорядочить результаты, чтобы вернуть наиболее информативные данные в базе данных.
Никогда не запрашивайте все столбцы из таблицы. Вы должны запрашивать только те столбцы, которые необходимы для ответа на вопрос. Оберните каждое имя столбца в обратные кавычки (`) для обозначения их как ограниченных идентификаторов.
Обратите внимание, что используются только имена столбцов, которые вы видите в таблицах ниже. Будьте внимательны, чтобы не запрашивать столбцы, которых не существует. Также обратите внимание, какой столбец находится в какой таблице.
Обратите внимание, что для получения текущей даты, если вопрос связан с "сегодня", используйте функцию CURDATE().

Используйте следующий формат:

Question: Вопрос
SQLQuery: SQL-запрос для выполнения
SQLResult: Разультат выполнения запроса
Answer: Итоговый ответ

"""

MYSQL_PROMPT = PromptTemplate(
    input_variables=["input", "table_info", "top_k"],
    template=_mysql_prompt + PROMPT_SUFFIX,
)


_mariadb_prompt = """Вы являетесь экспертом по MariaDB. По заданному вопросу сначала создайте синтаксически правильный запрос MariaDB для выполнения, затем просмотрите результаты запроса и верните ответ на входной вопрос.
Если пользователь не указывает в вопросе конкретное количество примеров для получения, запрашивайте не более {top_k} результатов, используя ключевое слово LIMIT, как в MariaDB. Вы можете упорядочить результаты, чтобы вернуть наиболее информативные данные в базе данных.
Никогда не запрашивайте все столбцы из таблицы. Вы должны запрашивать только те столбцы, которые необходимы для ответа на вопрос. Оберните каждое имя столбца в обратные кавычки (`) для обозначения их как ограниченных идентификаторов.
Обратите внимание, что используются только имена столбцов, которые вы видите в таблицах ниже. Будьте внимательны, чтобы не запрашивать столбцы, которых не существует. Также обратите внимание, какой столбец находится в какой таблице.
Обратите внимание, что для получения текущей даты, если вопрос связан с "сегодня", используйте функцию CURDATE().

Используйте следующий формат:

Question: Вопрос
SQLQuery: SQL-запрос для выполнения
SQLResult: Разультат выполнения запроса
Answer: Итоговый ответ

"""

MARIADB_PROMPT = PromptTemplate(
    input_variables=["input", "table_info", "top_k"],
    template=_mariadb_prompt + PROMPT_SUFFIX,
)


_oracle_prompt = """Вы являетесь экспертом по Oracle SQL. По заданному вопросу сначала создайте синтаксически правильный запрос Oracle SQL для выполнения, затем просмотрите результаты запроса и верните ответ на входной вопрос.
Если пользователь не указывает в вопросе конкретное количество примеров для получения, запрашивайте не более {top_k} результатов, используя ключевое слово FETCH FIRST n ROWS ONLY, как в Oracle SQL. Вы можете упорядочить результаты, чтобы вернуть наиболее информативные данные в базе данных.
Никогда не запрашивайте все столбцы из таблицы. Вы должны запрашивать только те столбцы, которые необходимы для ответа на вопрос. Оберните каждое имя столбца в двойные кавычки (") для обозначения их как ограниченных идентификаторов.
Обратите внимание, что используются только имена столбцов, которые вы видите в таблицах ниже. Будьте внимательны, чтобы не запрашивать столбцы, которых не существует. Также обратите внимание, какой столбец находится в какой таблице.
Обратите внимание, что для получения текущей даты, если вопрос связан с "сегодня", используйте функцию TRUNC(SYSDATE).

Используйте следующий формат:

Question: Вопрос
SQLQuery: SQL-запрос для выполнения
SQLResult: Разультат выполнения запроса
Answer: Итоговый ответ

"""

ORACLE_PROMPT = PromptTemplate(
    input_variables=["input", "table_info", "top_k"],
    template=_oracle_prompt + PROMPT_SUFFIX,
)


_postgres_prompt = """Вы являетесь экспертом по PostgreSQL. По заданному вопросу сначала создайте синтаксически правильный запрос PostgreSQL для выполнения, затем просмотрите результаты запроса и верните ответ на входной вопрос.
Если пользователь не указывает в вопросе конкретное количество примеров для получения, запрашивайте не более {top_k} результатов, используя ключевое слово LIMIT, как в PostgreSQL. Вы можете упорядочить результаты, чтобы вернуть наиболее информативные данные в базе данных.
Никогда не запрашивайте все столбцы из таблицы. Вы должны запрашивать только те столбцы, которые необходимы для ответа на вопрос. Оберните каждое имя столбца в двойные кавычки (") для обозначения их как ограниченных идентификаторов.
Обратите внимание, что используются только имена столбцов, которые вы видите в таблицах ниже. Будьте внимательны, чтобы не запрашивать столбцы, которых не существует. Также обратите внимание, какой столбец находится в какой таблице.
Обратите внимание, что для получения текущей даты, если вопрос связан с "сегодня", используйте функцию CURRENT_DATE.

Используйте следующий формат:

Question: Вопрос
SQLQuery: SQL-запрос для выполнения
SQLResult: Разультат выполнения запроса
Answer: Итоговый ответ

"""

POSTGRES_PROMPT = PromptTemplate(
    input_variables=["input", "table_info", "top_k"],
    template=_postgres_prompt + PROMPT_SUFFIX,
)


_sqlite_prompt = """Вы являетесь экспертом по SQLite. По заданному вопросу сначала создайте синтаксически правильный запрос SQLite для выполнения, затем просмотрите результаты запроса и верните ответ на входной вопрос.
Если пользователь не указывает в вопросе конкретное количество примеров для получения, запрашивайте не более {top_k} результатов, используя ключевое слово LIMIT, как в SQLite. Вы можете упорядочить результаты, чтобы вернуть наиболее информативные данные в базе данных.
Никогда не запрашивайте все столбцы из таблицы. Вы должны запрашивать только те столбцы, которые необходимы для ответа на вопрос. Оберните каждое имя столбца в двойные кавычки (") для обозначения их как ограниченных идентификаторов.
Обратите внимание, что используются только имена столбцов, которые вы видите в таблицах ниже. Будьте внимательны, чтобы не запрашивать столбцы, которых не существует. Также обратите внимание, какой столбец находится в какой таблице.
Обратите внимание, что для получения текущей даты, если вопрос связан с "сегодня", используйте функцию date('now').

Используйте следующий формат:

Question: Вопрос
SQLQuery: SQL-запрос для выполнения
SQLResult: Разультат выполнения запроса
Answer: Итоговый ответ

"""

SQLITE_PROMPT = PromptTemplate(
    input_variables=["input", "table_info", "top_k"],
    template=_sqlite_prompt + PROMPT_SUFFIX,
)

_clickhouse_prompt = """Вы являетесь экспертом по ClickHouse. По заданному вопросу сначала создайте синтаксически правильный запрос ClickHouse для выполнения, затем просмотрите результаты запроса и верните ответ на входной вопрос.
Если пользователь не указывает в вопросе конкретное количество примеров для получения, запрашивайте не более {top_k} результатов, используя ключевое слово LIMIT, как в ClickHouse. Вы можете упорядочить результаты, чтобы вернуть наиболее информативные данные в базе данных.
Никогда не запрашивайте все столбцы из таблицы. Вы должны запрашивать только те столбцы, которые необходимы для ответа на вопрос. Оберните каждое имя столбца в двойные кавычки (") для обозначения их как ограниченных идентификаторов.
Обратите внимание, что используются только имена столбцов, которые вы видите в таблицах ниже. Будьте внимательны, чтобы не запрашивать столбцы, которых не существует. Также обратите внимание, какой столбец находится в какой таблице.
Обратите внимание, что для получения текущей даты, если вопрос связан с "сегодня", используйте функцию today().

Используйте следующий формат:

Question: Вопрос
SQLQuery: SQL-запрос для выполнения
SQLResult: Разультат выполнения запроса
Answer: Итоговый ответ

"""

CLICKHOUSE_PROMPT = PromptTemplate(
    input_variables=["input", "table_info", "top_k"],
    template=_clickhouse_prompt + PROMPT_SUFFIX,
)

_prestodb_prompt = """Вы являетесь экспертом по PrestoDB. По заданному вопросу сначала создайте синтаксически правильный запрос PrestoDB для выполнения, затем просмотрите результаты запроса и верните ответ на входной вопрос.
Если пользователь не указывает в вопросе конкретное количество примеров для получения, запрашивайте не более {top_k} результатов, используя ключевое слово LIMIT, как в PrestoDB. Вы можете упорядочить результаты, чтобы вернуть наиболее информативные данные в базе данных.
Никогда не запрашивайте все столбцы из таблицы. Вы должны запрашивать только те столбцы, которые необходимы для ответа на вопрос. Оберните каждое имя столбца в двойные кавычки (") для обозначения их как ограниченных идентификаторов.
Обратите внимание, что используются только имена столбцов, которые вы видите в таблицах ниже. Будьте внимательны, чтобы не запрашивать столбцы, которых не существует. Также обратите внимание, какой столбец находится в какой таблице.
Обратите внимание, что для получения текущей даты, если вопрос связан с "сегодня", используйте функцию current_date.

Используйте следующий формат:

Question: Вопрос
SQLQuery: SQL-запрос для выполнения
SQLResult: Разультат выполнения запроса
Answer: Итоговый ответ

"""

PRESTODB_PROMPT = PromptTemplate(
    input_variables=["input", "table_info", "top_k"],
    template=_prestodb_prompt + PROMPT_SUFFIX,
)


SQL_PROMPTS = {
    "crate": CRATEDB_PROMPT,
    "duckdb": DUCKDB_PROMPT,
    "googlesql": GOOGLESQL_PROMPT,
    "mssql": MSSQL_PROMPT,
    "mysql": MYSQL_PROMPT,
    "mariadb": MARIADB_PROMPT,
    "oracle": ORACLE_PROMPT,
    "postgresql": POSTGRES_PROMPT,
    "sqlite": SQLITE_PROMPT,
    "clickhouse": CLICKHOUSE_PROMPT,
    "prestodb": PRESTODB_PROMPT,
}
