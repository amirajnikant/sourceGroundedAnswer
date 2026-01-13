# import json
# from pathlib import Path
# from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader, TextLoader, UnstructuredHTMLLoader, UnstructuredWordDocumentLoader, UnstructuredPowerPointLoader, WebBaseLoader
# from langchain_core.documents import Document


# # ---------- paths ----------
# RAW_DIR = Path(
#     "E:/OneDrive/Documents/GitHub/sourceGroundedAnswer/data/raw/"
# )

# PROCESSED_DIR = Path(
#     "E:/OneDrive/Documents/GitHub/sourceGroundedAnswer/data/processed/"
# )
# PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
# OUTPUT_FILE = PROCESSED_DIR / "all_documents.json"


# # ---------- base class ----------
# class MetadataLoaderStage1:
#     def load(self):
#         docs = self._load()

#         for d in docs:
#             source = Path(d.metadata.get("source", ""))
#             d.metadata["file_name"] = source.name
#             d.metadata["format"] = source.suffix.lstrip(".")

#         return docs

#     def save_all(self, docs):
#         data = [
#             {
#                 "page_content": d.page_content,
#                 "metadata": d.metadata
#             }
#             for d in docs
#         ]

#         with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
#             json.dump(data, f, indent=2, ensure_ascii=False)

#     def load_all(self):
#         with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
#             data = json.load(f)

#         docs= []
#         for item in data:
#             data.append(
#                 Document(
#                     page_content=item["page_content"],
#                     metadata=item["metadata"]
#                 )
#             )

#         return docs

#     def preview(self, docs, chars=200):
#         print(f"Total documents: {len(docs)}\n")

#         for i, d in enumerate(docs):
#             text = (d.page_content or "")[:chars].replace("\n", " ")
#             print(f"[{i}] {text}...")
#             print(f"    metadata: {d.metadata}\n")


# # ---------- child class ----------
# class PDFLoader(MetadataLoaderStage1):
#     def _load(self):
#         loader = DirectoryLoader(
#             path=str(RAW_DIR),
#             glob="**/*.pdf",
#             loader_cls=PyPDFLoader
#         )
#         return loader.load()


# class PPTLoader(MetadataLoaderStage1):
#     def _load(self):
#         loader = DirectoryLoader(
#             path=str(RAW_DIR),
#             glob="**/*.pptx",
#             loader_cls=UnstructuredPowerPointLoader
#         )
#         return loader.load()


# class TXTLoader(MetadataLoaderStage1):
#     def _load(self):
#         loader = DirectoryLoader(
#             path=str(RAW_DIR),
#             glob="**/*.txt",
#             loader_cls=TextLoader
#         )
#         return loader.load()


# class HTMLLoader(MetadataLoaderStage1):
#     def _load(self):
#         loader = DirectoryLoader(
#             path=str(RAW_DIR),
#             glob="**/*.html",
#             loader_cls=UnstructuredHTMLLoader
#         )
#         return loader.load()


# class DOCLoader(MetadataLoaderStage1):
#     def _load(self):
#         loader = DirectoryLoader(
#             path=str(RAW_DIR),
#             glob="**/*.docx",
#             loader_cls=UnstructuredWordDocumentLoader
#         )
#         return loader.load()


# class URLLoader(MetadataLoaderStage1):
#     def _load(self):
#         urls = [
#             "https://www.sciencenews.org/",
#             "https://www.sciencedaily.com/"
#         ]
#         loader = WebBaseLoader(urls)
#         return loader.load()


# # ---------- usage ----------
# if __name__ == "__main__":
#     pdf = PDFLoader()


# import json
# from pathlib import Path
# from typing import List, Dict, Type

# from langchain_community.document_loaders import (
#     DirectoryLoader,
#     PyPDFLoader,
#     TextLoader,
#     UnstructuredHTMLLoader,
#     UnstructuredWordDocumentLoader,
#     UnstructuredPowerPointLoader,
#     WebBaseLoader,
# )
# from langchain_core.documents import Document


# # ==============================
# # Paths
# # ==============================
# RAW_DIR = Path(
#     "E:/OneDrive/Documents/GitHub/sourceGroundedAnswer/data/raw/"
# )

# PROCESSED_DIR = Path(
#     "E:/OneDrive/Documents/GitHub/sourceGroundedAnswer/data/processed/"
# )
# PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

# OUTPUT_FILE = PROCESSED_DIR / "all_documents.json"


# # ==============================
# # Loader registry (CONFIG)
# # ==============================
# FILE_LOADERS: Dict[str, Type] = {
#     "**/*.pdf": PyPDFLoader,
#     "**/*.pptx": UnstructuredPowerPointLoader,
#     "**/*.txt": TextLoader,
#     "**/*.html": UnstructuredHTMLLoader,
#     "**/*.docx": UnstructuredWordDocumentLoader,
# }


# # ==============================
# # Base pipeline stage
# # ==============================
# class MetadataLoaderStage1:
#     """
#     Stage 1:
#     - Load raw documents
#     - Normalize metadata
#     - Save / reload
#     """

#     def load(self) -> List[Document]:
#         docs = self._load()

#         for d in docs:
#             source = Path(d.metadata.get("source", ""))
#             d.metadata["file_name"] = source.name
#             d.metadata["format"] = source.suffix.lstrip(".").lower()

#         return docs

#     def _load(self) -> List[Document]:
#         raise NotImplementedError

#     def save_all(self, docs: List[Document]) -> None:
#         data = [
#             {
#                 "page_content": d.page_content,
#                 "metadata": d.metadata,
#             }
#             for d in docs
#         ]

#         with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
#             json.dump(data, f, indent=2, ensure_ascii=False)

#     def load_all(self) -> List[Document]:
#         with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
#             data = json.load(f)

#         docs: List[Document] = []
#         for item in data:
#             docs.append(
#                 Document(
#                     page_content=item["page_content"],
#                     metadata=item["metadata"],
#                 )
#             )

#         return docs

#     def preview(self, docs: List[Document], chars: int = 200) -> None:
#         print(f"\nTotal documents: {len(docs)}\n")

#         for i, d in enumerate(docs):
#             text = (d.page_content or "")[:chars].replace("\n", " ")
#             print(f"[{i}] {text}...")
#             print(f"    metadata: {d.metadata}\n")


# # ==============================
# # Unified loader
# # ==============================
# class AllFileLoader(MetadataLoaderStage1):
#     def _load(self) -> List[Document]:
#         docs: List[Document] = []

#         # ---- local files ----
#         for glob_pattern, loader_cls in FILE_LOADERS.items():
#             loader = DirectoryLoader(
#                 path=str(RAW_DIR),
#                 glob=glob_pattern,
#                 loader_cls=loader_cls,
#             )
#             docs.extend(loader.load())

#         # ---- web sources ----
#         urls = [
#             "https://www.sciencenews.org/",
#             "https://www.sciencedaily.com/",
#         ]
#         docs.extend(WebBaseLoader(urls).load())

#         return docs


# # ==============================
# # Entry point
# # ==============================
# if __name__ == "__main__":
#     loader = AllFileLoader()

#     docs = loader.load()
#     loader.preview(docs)

#     loader.save_all(docs)

#     print(f"\nSaved {len(docs)} documents to:")
#     print(OUTPUT_FILE)




# import json
# from pathlib import Path
# from typing import List, Dict, Type, Optional

# from langchain_community.document_loaders import (
#     DirectoryLoader,
#     PyPDFLoader,
#     TextLoader,
#     UnstructuredHTMLLoader,
#     UnstructuredWordDocumentLoader,
#     UnstructuredPowerPointLoader,
#     WebBaseLoader,
# )
# from langchain_core.documents import Document


# # ==============================
# # Paths
# # ==============================
# RAW_DIR = Path(
#     "E:/OneDrive/Documents/GitHub/sourceGroundedAnswer/data/raw/"
# )

# PROCESSED_DIR = Path(
#     "E:/OneDrive/Documents/GitHub/sourceGroundedAnswer/data/processed/"
# )
# PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

# OUTPUT_FILE = PROCESSED_DIR / "all_documents.json"


# # ==============================
# # Loader registry (CONFIG)
# # ==============================
# FILE_LOADERS: Dict[str, Type] = {
#     "**/*.pdf": PyPDFLoader,
#     "**/*.pptx": UnstructuredPowerPointLoader,
#     "**/*.txt": TextLoader,
#     "**/*.html": UnstructuredHTMLLoader,
#     "**/*.docx": UnstructuredWordDocumentLoader,
# }


# # ==============================
# # Base pipeline stage
# # ==============================
# class MetadataLoaderStage1:
#     """
#     Stage 1:
#     - Load raw documents
#     - Normalize metadata
#     - Save / reload
#     """

#     def load(self) -> List[Document]:
#         docs = self._load()

#         for d in docs:
#             source = Path(d.metadata.get("source", ""))
#             d.metadata["file_name"] = source.name
#             d.metadata["format"] = source.suffix.lstrip(".").lower()

#         return docs

#     def _load(self) -> List[Document]:
#         raise NotImplementedError

#     def save_all(self, docs: List[Document]) -> None:
#         data = [
#             {
#                 "page_content": d.page_content,
#                 "metadata": d.metadata,
#             }
#             for d in docs
#         ]

#         with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
#             json.dump(data, f, indent=2, ensure_ascii=False)

#     def load_all(self) -> List[Document]:
#         with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
#             data = json.load(f)

#         docs: List[Document] = []
#         for item in data:
#             docs.append(
#                 Document(
#                     page_content=item["page_content"],
#                     metadata=item["metadata"],
#                 )
#             )

#         return docs

#     def preview(self, docs: List[Document], chars: int = 200) -> None:
#         print(f"\nTotal documents: {len(docs)}\n")

#         for i, d in enumerate(docs):
#             text = (d.page_content or "")[:chars].replace("\n", " ")
#             print(f"[{i}] {text}...")
#             print(f"    metadata: {d.metadata}\n")


# # ==============================
# # Unified configurable loader
# # ==============================
# class AllFileLoader(MetadataLoaderStage1):
#     def __init__(
#         self,
#         file_patterns: Optional[List[str]] = None,
#         urls: Optional[List[str]] = None,
#     ):
#         """
#         file_patterns:
#             None        -> load all supported file types
#             []          -> load no local files
#             list[str]   -> load only these glob patterns

#         urls:
#             Optional list of URLs to load
#         """
#         self.file_patterns = file_patterns
#         self.urls = urls or []

#     def _load(self) -> List[Document]:
#         docs: List[Document] = []

#         patterns = (
#             self.file_patterns
#             if self.file_patterns is not None
#             else FILE_LOADERS.keys()
#         )

#         # ---- local files ----
#         for pattern in patterns:
#             loader_cls = FILE_LOADERS.get(pattern)
#             if not loader_cls:
#                 raise ValueError(f"Unsupported file pattern: {pattern}")

#             loader = DirectoryLoader(
#                 path=str(RAW_DIR),
#                 glob=pattern,
#                 loader_cls=loader_cls,
#             )
#             docs.extend(loader.load())

#         # ---- web sources ----
#         if self.urls:
#             docs.extend(WebBaseLoader(self.urls).load())

#         return docs


# # ==============================
# # Entry point
# # ==============================
# if __name__ == "__main__":
#     # --------------------------
#     # EXAMPLES — pick ONE
#     # --------------------------

#     # 1️⃣ Load everything
#     loader = AllFileLoader()

#     # 2️⃣ Load only PDFs
#     # loader = AllFileLoader(file_patterns=["**/*.pdf"])

#     # 3️⃣ Load TXT + HTML only
#     # loader = AllFileLoader(file_patterns=["**/*.txt", "**/*.html"])

#     # 4️⃣ Load only URLs
#     # loader = AllFileLoader(
#     #     file_patterns=[],
#     #     urls=["https://www.sciencenews.org/"]
#     # )

#     docs = loader.load()
#     loader.preview(docs)
#     loader.save_all(docs)

#     print(f"\nSaved {len(docs)} documents to:")
#     print(OUTPUT_FILE)





import json
from pathlib import Path
from typing import Callable, Dict, List

from langchain_community.document_loaders import (
    DirectoryLoader,
    PyPDFLoader,
    TextLoader,
    UnstructuredHTMLLoader,
    UnstructuredWordDocumentLoader,
    UnstructuredPowerPointLoader,
    WebBaseLoader,
)
from langchain_core.documents import Document


# =====================================================
# Paths
# =====================================================
RAW_DIR = Path(
    "E:/OneDrive/Documents/GitHub/sourceGroundedAnswer/data/raw/"
)

PROCESSED_DIR = Path(
    "E:/OneDrive/Documents/GitHub/sourceGroundedAnswer/data/processed/"
)
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_FILE = PROCESSED_DIR / "all_documents.json"


# =====================================================
# Base pipeline stage (Stage 1: load + normalize)
# =====================================================
class MetadataLoaderStage1:
    def load(self) -> List[Document]:
        docs = self._load()

        # normalize metadata
        for d in docs:
            source = d.metadata.get("source", "")
            p = Path(source)

            d.metadata["file_name"] = p.name
            d.metadata["format"] = p.suffix.lstrip(".").lower()
            d.metadata.setdefault("source_type", "file")

        return docs

    def _load(self) -> List[Document]:
        raise NotImplementedError

    def save_all(self, docs: List[Document]) -> None:
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            json.dump(
                [
                    {
                        "page_content": d.page_content,
                        "metadata": d.metadata,
                    }
                    for d in docs
                ],
                f,
                indent=2,
                ensure_ascii=False,
            )

    def load_all(self) -> List[Document]:
        with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

        return [
            Document(
                page_content=item["page_content"],
                metadata=item["metadata"],
            )
            for item in data
        ]

    def preview(self, docs: List[Document], chars: int = 200) -> None:
        print(f"\nTotal documents: {len(docs)}\n")
        for i, d in enumerate(docs):
            text = (d.page_content or "")[:chars].replace("\n", " ")
            print(f"[{i}] {text}...")
            print(f"    metadata: {d.metadata}\n")


# =====================================================
# Loader factories (FILES + URL at same abstraction level)
# =====================================================
def make_directory_loader(
    glob_pattern: str,
    loader_cls,
) -> Callable[[], List[Document]]:
    def load():
        return DirectoryLoader(
            path=str(RAW_DIR),
            glob=glob_pattern,
            loader_cls=loader_cls,
        ).load()

    return load


def make_url_loader(urls: List[str]) -> Callable[[], List[Document]]:
    def load():
        return WebBaseLoader(urls).load()

    return load


# =====================================================
# Source registry (single source of truth)
# =====================================================
SOURCE_LOADERS: Dict[str, Callable[[], List[Document]]] = {
    "pdf": make_directory_loader("**/*.pdf", PyPDFLoader),
    "pptx": make_directory_loader("**/*.pptx", UnstructuredPowerPointLoader),
    "txt": make_directory_loader("**/*.txt", TextLoader),
    "html": make_directory_loader("**/*.html", UnstructuredHTMLLoader),
    "docx": make_directory_loader("**/*.docx", UnstructuredWordDocumentLoader),
    "url": make_url_loader(
        [
            "https://www.sciencenews.org/",
            "https://www.sciencedaily.com/",
        ]
    ),
}


# =====================================================
# Unified loader (no special cases)
# =====================================================
class AllSourceLoader(MetadataLoaderStage1):
    def __init__(self, sources: List[str] | None = None):
        # None = load all registered sources
        self.sources = sources or SOURCE_LOADERS.keys()

    def _load(self) -> List[Document]:
        docs: List[Document] = []

        for source_name in self.sources:
            loader_fn = SOURCE_LOADERS[source_name]
            docs.extend(loader_fn())

        return docs


# =====================================================
# Entry point
# =====================================================
if __name__ == "__main__":
    # Examples:
    # loader = AllSourceLoader()                 # everything
    # loader = AllSourceLoader(["pdf"])          # only PDFs
    # loader = AllSourceLoader(["pdf", "url"])   # PDFs + URLs

    loader = AllSourceLoader()

    docs = loader.load()
    loader.preview(docs)
    loader.save_all(docs)

    print(f"\nSaved {len(docs)} documents to:")
    print(OUTPUT_FILE)
