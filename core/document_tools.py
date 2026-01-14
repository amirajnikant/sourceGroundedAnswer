import json
from pathlib import Path
from typing import List, Union
from langchain_core.documents import Document

class JsonFileIO:
    def save(self, docs: List[Document], path: str | Path):
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        json_docs = []

        for doc in docs:
            json_docs.append(
                {
                    "metadata": doc.metadata,
                    "page_content" : doc.page_content
                }
            )

        with open(path, "w", encoding="utf-8") as f:
            json.dump(json_docs, f, ensure_ascii=False, indent=2)

    def load(self, path: str | Path):
        path = Path(path)

        with open(path, "r", encoding="utf-8") as f:
            return json .load(f)
        
class Previewer:
    def preview(self, docs: List[Union[Document, dict]]) -> None:
        if not docs:
            print("No documents to preview.")
            return

        first = docs[0]

        if isinstance(first, Document):
            self._preview_langchain(docs)

        elif isinstance(first, dict):
            self._preview_json(docs)

        else:
            raise TypeError(
                f"Unsupported type in preview: {type(first)}"
            )

    def _preview_langchain(self, docs: List[Document]) -> None:
        print(f"\nTotal documents: {len(docs)}\n")
        for i, d in enumerate(docs):
            text = (d.page_content or "")[:150].replace("\n", " ")
            print(f"[{i}] {text}...")
            print(f"    metadata: {d.metadata}\n")

    def _preview_json(self, docs: List[dict]) -> None:
        print(f"\nTotal documents: {len(docs)}\n")
        for i, d in enumerate(docs):
            text = (d.get("page_content", "") or "")[:150].replace("\n", " ")
            print(f"[{i}] {text}...")
            print(f"    metadata: {d.get('metadata', {})}\n")