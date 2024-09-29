import time
import streamlit as st
import requests

API_URL = "http://backend:8000"

st.set_page_config(page_title="PDF 기반 RAG 시스템", layout="wide")

# 세션 상태 초기화
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

# 사이드바에 파일 업로드 기능 추가
with st.sidebar:
    st.header("PDF 업로드")
    uploaded_file = st.file_uploader(
        "PDF 파일을 업로드하세요. (하나의 파일이 완료된 후 x 버튼을 눌러 파일을 삭제하고 다른파일을 업로드해주세요)",
        type="pdf"
    )

    if uploaded_file is not None:
        if st.button("PDF 업로드"):
            with st.spinner("PDF 파일을 처리하고 있습니다..."):
                files = {'file': (uploaded_file.name, uploaded_file.getvalue(), 'application/pdf')}
                response = requests.post(f"{API_URL}/qa/upload", files=files)
                if response.status_code == 200:
                    st.success("PDF 파일이 성공적으로 업로드되고 처리되었습니다.")
                else:
                    st.error(response.json()["detail"])

            with st.spinner(f"{uploaded_file.name} 의 데이터를 업데이트 중입니다... (약 3 ~ 5분 소요)"):
                task_id = response.json()["task_id"]
                while True:
                    result_response = requests.get(f"{API_URL}/qa/result/retriever/{task_id}")
                    result = result_response.json()
                    if result["status"] == "completed":
                        st.success(f"{uploaded_file.name} 의 데이터를 업데이를 성공하였습니다.")
                        break
                    time.sleep(1)

# 메인 화면
st.title("PDF 기반 RAG 시스템")

# 채팅 히스토리 표시
for message in st.session_state['chat_history']:
    with st.chat_message(message["role"]):
        st.write(message["content"])

if prompt := st.chat_input("질문을 입력하세요."):
    result = requests.get(f"{API_URL}/qa/upload-file-check")
    if result.status_code == 400:
        st.error(result.json()["detail"])
    else:
        # 사용자 메시지 추가
        st.session_state['chat_history'].append({"role": "human", "content": prompt})
        with st.chat_message("human"):
            st.write(prompt)

        # AI 응답 생성
        with st.chat_message("ai"):
            message_placeholder = st.empty()
            data = {
                "question": prompt,
            }
            response = requests.post(f"{API_URL}/qa/query", json=data)
            if response.status_code == 200:
                task_id = response.json()["task_id"]
                full_response = ""
                with st.spinner("답변을 생성 중입니다..."):
                    while True:
                        result_response = requests.get(f"{API_URL}/qa/result/{task_id}")
                        result = result_response.json()
                        if result["status"] == "completed":
                            full_response = result["result"]
                            message_placeholder.markdown(full_response)
                            break
                        time.sleep(1)

                # AI 메시지 추가
                st.session_state['chat_history'].append({"role": "ai", "content": full_response})
            else:
                st.error("오류가 발생했습니다. 다시 시도해주세요.")
