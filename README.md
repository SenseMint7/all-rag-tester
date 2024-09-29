# all-rag-tester

## 개발 환경
- MacBook M1 Pro
- macOS Sonoma 14.5

## Skill
- python >= 3.11
- LangChain
- LangSmith
- Streamlt
- FastAPI
- Dependency Injector
- Chroma
- redis
- celery

## 실행 방법
### docker compose 를 통한 실행
```sh
$ docker compose up -d
```
### UI 접속방법
- http://localhost:8501

## 테스트 방법
1. 챗봇으로 만들고 싶은 pdf 파일을 업로드 합니다.
2. 여러 파일의 pdf 문서기반 챗봇을 만들고 싶으시면 화면의 가이드를 따라주세요.
3. 모든 pdf 파일을 업로드 후 원하는 질문을 해보세요!

### 추가 설명
- RedisChatMessageHistory 를 사용하여 멀티턴 에이전트를 구현하였습니다.
- Layered Architecture 와 Dependency Injector를 사용하여 확장 가능한 프로젝트 구조를 만들었습니다.
- Celery를 사용하여 요청에 대한 동시성을 해결하였습니다.
- retriever 는 BM25 + ParentDocumentRetriever 를 사용한 EnsembleRetriever 사용하여 구현하였습니다.
- OpenAI 의 text-embedding-3-large 를 사용하여 chunk를 embedding 하였습니다.
- uv 패키지 관리자를 사용하여 빠른 패키지 설치 및 빌드가 가능합니다.
- ruff 를 이용한 formating 을 통해 코드 품질을 관리하였습니다.

### 유의 사항
- 300 페이지 정도의 PDF 파일 업로드시 업로드부터 임베딩 작업까지 약 8분 정도 소요됩니다.
- 많은 페이지의 pdf 파일 업로드시 서버가 다운될 수 있습니다. 이경우 경우 서버를 다시 시작하여 주세요.
