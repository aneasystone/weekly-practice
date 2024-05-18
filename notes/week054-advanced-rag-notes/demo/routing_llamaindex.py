from llama_index.core import Settings
from llama_index.core import SimpleDirectoryReader

# load documents
documents = SimpleDirectoryReader("./data").load_data()
nodes = Settings.node_parser.get_nodes_from_documents(documents)

from llama_index.core import StorageContext

# initialize storage context (by default it's in-memory)
storage_context = StorageContext.from_defaults()
storage_context.docstore.add_documents(nodes)

from llama_index.core import SummaryIndex
from llama_index.core import VectorStoreIndex

# initialize indices and query engines
summary_index = SummaryIndex(nodes, storage_context=storage_context)
vector_index = VectorStoreIndex(nodes, storage_context=storage_context)

list_query_engine = summary_index.as_query_engine(
    response_mode="tree_summarize",
    use_async=True,
)
vector_query_engine = vector_index.as_query_engine()

from llama_index.core.tools import QueryEngineTool

# convert query engines to tools
list_tool = QueryEngineTool.from_defaults(
    query_engine=list_query_engine,
    description="Useful for summarization questions related to Paul Graham eassy on What I Worked On.",
)

vector_tool = QueryEngineTool.from_defaults(
    query_engine=vector_query_engine,
    description="Useful for retrieving specific context from Paul Graham essay on What I Worked On.",
)

from llama_index.core.query_engine import RouterQueryEngine
from llama_index.core.selectors import LLMSingleSelector, LLMMultiSelector
from llama_index.core.selectors import PydanticSingleSelector, PydanticMultiSelector

# routing engine tools with a selector
query_engine = RouterQueryEngine(
    selector=PydanticSingleSelector.from_defaults(),
    query_engine_tools=[
        list_tool,
        vector_tool,
    ],
)

response = query_engine.query("What is the summary of the document?")
print(str(response))

# response = query_engine.query("What did Paul Graham do after RICS?")
# print(str(response))