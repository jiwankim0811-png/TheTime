from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(title="Binary Search Server", version="1.0")

# CORS(Cross-Origin Resource Sharing) 설정
# GAS 및 모든 도메인에서의 클라이언트 요청을 허용하기 위해 설정합니다.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 실제 운영 환경에서는 허용할 도메인만 지정하는 것이 안전합니다.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SearchRequest(BaseModel):
    data: List[int]
    target: int

class SearchStep(BaseModel):
    step: int
    low: int
    high: int
    mid: int
    mid_value: Optional[int]
    status: str
    message: str

class SearchResponse(BaseModel):
    success: bool
    target: int
    found_index: Optional[int]
    total_steps: int
    steps: List[SearchStep]
    time_complexity: str
    space_complexity: str

@app.post("/api/binary-search", response_model=SearchResponse)
def binary_search_api(req: SearchRequest):
    """
    이진 검색 알고리즘을 수행하고 각 단계별 상태(State)와 복잡도 정보를 반환합니다.
    데이터는 반드시 오름차순으로 정렬되어 있어야 합니다.
    """
    arr = req.data
    target = req.target

    # 입력 데이터가 정렬되어 있지 않은 경우 정렬 수행
    # (안정적인 이진 검색을 위해 오름차순 정렬 보장)
    sorted_arr = sorted(arr)
    
    steps = []
    low = 0
    high = len(sorted_arr) - 1
    step_count = 0
    found_index = None

    while low <= high:
        step_count += 1
        mid = (low + high) // 2
        mid_value = sorted_arr[mid]

        if mid_value == target:
            found_index = mid
            steps.append(SearchStep(
                step=step_count,
                low=low,
                high=high,
                mid=mid,
                mid_value=mid_value,
                status="FOUND",
                message=f"단계 {step_count}: 인덱스 {mid}에서 타겟 값 {target}을(를) 찾았습니다!"
            ))
            break
        elif mid_value < target:
            steps.append(SearchStep(
                step=step_count,
                low=low,
                high=high,
                mid=mid,
                mid_value=mid_value,
                status="GO_RIGHT",
                message=f"단계 {step_count}: 중앙값({mid_value})이 타겟({target})보다 작으므로 오른쪽 구간으로 이동합니다."
            ))
            low = mid + 1
        else:
            steps.append(SearchStep(
                step=step_count,
                low=low,
                high=high,
                mid=mid,
                mid_value=mid_value,
                status="GO_LEFT",
                message=f"단계 {step_count}: 중앙값({mid_value})이 타겟({target})보다 크므로 왼쪽 구간으로 이동합니다."
            ))
            high = mid - 1

    if found_index is None:
        steps.append(SearchStep(
            step=step_count + 1,
            low=low,
            high=high,
            mid=-1,
            mid_value=None,
            status="NOT_FOUND",
            message=f"검색 실패: 데이터 안에 타겟 값 {target}이(가) 존재하지 않습니다."
        ))

    return SearchResponse(
        success=True,
        target=target,
        found_index=found_index,
        total_steps=len(steps),
        steps=steps,
        time_complexity="O(log N) - 매 단계마다 탐색 범위가 반으로 줄어듭니다.",
        space_complexity="O(1) - 추가적인 메모리 공간을 거의 사용하지 않습니다."
    )

@app.get("/")
def health_check():
    return {"status": "healthy", "message": "Binary Search Cloud Run Server is running."}
