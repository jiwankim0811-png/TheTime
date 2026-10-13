from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

app = FastAPI(title="Binary Search API", version="1.0")

# CORS(Cross-Origin Resource Sharing) 설정
# 구글 앱스 스크립트나 브라우저에서 클라우드 런 서버로 안전하게 요청을 보낼 수 있도록 허용합니다.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 실제 운영 환경에서는 허용할 도메인만 지정하는 것이 안전합니다.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 요청 데이터 구조 정의 (Pydantic 모델)
class SearchRequest(BaseModel):
    array: List[int]
    target: int

@app.post("/binary-search")
def binary_search_api(req: SearchRequest):
    """
    이진 검색 알고리즘 수행 API
    - 입력: 정렬된 정수 리스트(array)와 찾고자 하는 값(target)
    - 출력: 검색 과정의 단계별 기록(steps), 최종 결과 인덱스, 시간/공간 복잡도 정보
    """
    arr = req.array
    target = req.target

    # 이진 검색을 수행하기 전에 배열이 정렬되어 있는지 확인
    if arr != sorted(arr):
        raise HTTPException(status_code=400, detail="입력된 배열이 오름차순으로 정렬되어 있어야 합니다.")

    left = 0
    right = len(arr) - 1
    steps = []
    found_index = -1
    comparisons = 0

    # 이진 검색 핵심 로직
    while left <= right:
        mid = (left + right) // 2
        comparisons += 1
        
        # 현재 탐색 구간의 상태를 단계별 기록에 저장
        step_info = {
            "left": left,
            "right": right,
            "mid": mid,
            "mid_value": arr[mid],
            "message": f"범위 [{left}, {right}]의 중간 인덱스 {mid} (값: {arr[mid]})와 목표값 {target} 비교"
        }
        steps.append(step_info)

        if arr[mid] == target:
            found_index = mid
            step_info["message"] += " -> 목표값 찾음!"
            break
        elif arr[mid] < target:
            step_info["message"] += f" -> 목표값이 더 큼, 왼쪽 범위를 {mid + 1}(으)로 이동"
            left = mid + 1
        else:
            step_info["message"] += f" -> 목표값이 더 작음, 오른쪽 범위를 {mid - 1}(으)로 이동"
            right = mid - 1

    if found_index == -1:
        steps.append({
            "left": left,
            "right": right,
            "mid": -1,
            "mid_value": None,
            "message": "목표값이 배열에 존재하지 않습니다."
        })

    # 복잡도 정보 포함 반환
    return {
        "target": target,
        "array": arr,
        "found_index": found_index,
        "steps": steps,
        "complexity": {
            "time": "O(log N)",
            "space": "O(1)",
            "comparisons": comparisons
        }
    }

@app.post("/binary-search")
def binary_search_api(req: SearchRequest):
    # ... 로직 ...}
