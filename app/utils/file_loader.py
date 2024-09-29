import os

import yaml
from langchain_community.document_loaders import PDFPlumberLoader


def load_yaml(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"yaml 파일을 찾을 수 없습니다: {file_path}")
    with open(file_path) as f:
        return yaml.safe_load(f)


def load_pdf(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"pdf 파일을 찾을 수 없습니다: {file_path}")
    loader = PDFPlumberLoader(file_path)
    docs = loader.load()
    return docs


def load_all_pdf(folder_dir):
    all_docs = []
    for filename in os.listdir(folder_dir):
        if filename.endswith(".pdf"):
            file_path = os.path.join(folder_dir, filename)
            docs = load_pdf(file_path)
            all_docs.extend(docs)
    return all_docs
