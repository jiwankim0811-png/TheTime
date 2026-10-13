from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

app = FastAPI(title="Binary Search API", version="1.0")

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SearchRequest(BaseModel):
    array: List[int]
    target: int

@app.get("/")
def read_root():
    """서버가 정상 작동 중인지 확인하는 기본 루트 엔드포인트"""
    return {"message": "Binary Search API Server is running!"}

@app.get("/health")
def health_check():
    """상태 확인용 엔드포인트"""
    return {"status": "healthy"}

@app.post("/binary-search")
def binary_search_api(req: SearchRequest):
    """
    이진 검색 알고리즘 수행 API
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
