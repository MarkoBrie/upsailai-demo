import os
import json
from langchain_openai import ChatOpenAI

from chains.retriever import load_retriever
from chains.stylist_chain import build_stylist_chain
from chains.sale_assistant_chain import build_sale_assistant_chain

print(f". importing /discord/chains/chain_manager.py)")

class ChainManager:
    def __init__(self, persist_directory, docstore_path, openai_token):
        os.environ["OPENAI_API_KEY"] = openai_token

        self.retriever = load_retriever(persist_directory, docstore_path)
        self.llm_4o_mini = ChatOpenAI(model="gpt-4o-mini")
        self.llm_4o = ChatOpenAI(model="gpt-4o", temperature=1.0)

        self.stylist_chain_with_image = build_stylist_chain(
            self.llm_4o, with_image=True
        )
        self.stylist_chain_without_image = build_stylist_chain(
            self.llm_4o, with_image=False
        )
        self.sale_assistant_chain = build_sale_assistant_chain(self.llm_4o_mini)

    def retrieve_products(self, queries):
        print(f"file chain_manager.py: retrieve_products()")
        print(f"queries: {queries}")

        retrieved_products = {}
        retrieved_docs = {}
        for query in queries:
            docs = self.retriever.invoke(query)
            for doc in docs:
                product = json.loads(doc.page_content)
                if len(product["image_encodings"]) == 0:
                    continue
                retrieved_products[product["url"]] = {
                    "name": product["title"],
                    "description": product["description"],
                    # "image_base64": product["image_encodings"][-1],
                    "product_url": product["url"],
                    "category": product["category"],
                    "image_url": product["image_urls"][0],
                }
                retrieved_docs[product["url"]] = doc
        return retrieved_products, retrieved_docs

    def build_question(self, style_suggestions, customer_query):
        print(f"file chain_manager.py: build_question)}}()")
        print(f"style suggestions: {style_suggestions}")
        print(f"customer query: {customer_query}")

        question = f"""
        A customer is looking for {customer_query}
         
        Customer's clothing or style: 
        {style_suggestions['customer_style']}

        Stylist's opinion:
        {style_suggestions['stylist_opinion']}

        Stylist's advice:
        {style_suggestions['stylist_explanation']}
        """
        return question

    def organize_products(self, recommend_products, retrieved_products):
        products = {}
        for product in recommend_products["products"]:
            retrieved_product = retrieved_products.get(product["url"])
            if not retrieved_product:
                continue
            retrieved_product["description"] = product["description"]
            category = retrieved_product["category"]
            products.setdefault(category, {})[
                retrieved_product["product_url"]
            ] = retrieved_product
        return products


#  first call -> go to chat gpt and ask for
# for {style_suggestions['user_clothes']}
