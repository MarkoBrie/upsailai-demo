from app.core.config import settings
import json
from chains.chain_manager import ChainManager
from chains.utils.formatter import format_docs
from langchain_openai import ChatOpenAI
from langchain_core.messages.ai import AIMessageChunk

from langgraph.prebuilt import ToolNode, tools_condition


# Print the OpenAI token to the terminal
#print(f"OpenAI Token:   {settings['OPENAI_API_KEY2']}")
#print(f"DOC_STORE_PATH: {settings['DOC_STORE_PATH']}")

print(f"5. importing /discord/app/chat/chain.py)")

manager = ChainManager(
    persist_directory=settings["DB_PATH"],
    docstore_path=settings["DOC_STORE_PATH"],
    openai_token=settings["OPENAI_API_KEY2"],
)



from langchain.callbacks.base import BaseCallbackHandler

from app.utils.logging import logger


class RawResponseHandler(BaseCallbackHandler):

    def on_chat_model_start(self, serialized, messages, **kwargs):
        print(serialized)

    def on_llm_new_token(self, token: str, chunk, **kwargs):
        print(token)

    # def on_llm_end(self, response, **kwargs):
    #     self.raw_response = response.llm_output["text"]


class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, AIMessageChunk):
            return obj.__dict__  # Convert to dict or define your transformation
        return super().default(obj)


async def get_stream(query):

    try:
        events = manager.llm_4o_mini.astream_events(query, version="v2")

        async for event in events:

            # print(json.dumps(event, cls=CustomEncoder, indent=4))

            if event["event"] == "on_chat_model_stream":

                message_obj = {
                    "choices": [
                        {
                            "index": 0,
                            "delta": {
                                "role": "assistant",
                                "content": event["data"]["chunk"].content,
                            },
                        }
                    ]
                }
                message = f"data: {json.dumps(message_obj)}\n\n"
                yield message.encode("utf-8")  # Encode as bytes for StreamingResponse

    except Exception as e:
        logger.error(f"Unhandled exception in chain: {e}", exc_info=True)
        # Log the error here if needed
        yield f"data: ERROR\n\n"  # Yield an error message to the client
        return  # End the generator


async def get_recommended_products(
    recommended_products,
    stylist_explanation,
    stylist_opinion,
    customer_style,
    customer_query,
):
    try:
        retrieved_products, retrieved_docs = manager.retrieve_products(
            recommended_products
        )

        question = manager.build_question(
            {
                "recommended_products": recommended_products,
                "stylist_explanation": stylist_explanation,
                "customer_style": customer_style,
                "stylist_opinion": stylist_opinion,
            },
            customer_query,
        )

        print(question)

        recommend_products = manager.sale_assistant_chain.invoke(
            {
                "context": format_docs(retrieved_docs.values()),
                "question": question,
            }
        )

        return manager.organize_products(recommend_products, retrieved_products)

    except Exception as e:
        logger.error(f"Unhandled exception in chain: {e}", exc_info=True)
        # Log the error here if needed
        raise e
