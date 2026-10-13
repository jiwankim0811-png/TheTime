from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Any
import os

app = FastAPI(
    title="Hash Search Algorithm Cloud Run Service",
    description="클라우드 런 기반 해시 테이블 및 검색 알고리즘 백엔드",
    version="1.0.0"
)

# CORS(Cross-Origin Resource Sharing) 설정
# 모든 도메인에서의 요청을 허용 (필요시 특정 도메인으로 제한 가능)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 해시 테이블을 메모리에 유지 (실무에서는 DB나 Redis 연동 가능)
# 구조: { index: [ (key1, value1), (key2, value2), ... ] } (체이닝 방식 충돌 해결)
class HashTable:
    def __init__(self, size: int = 10):
        self.size = size
        self.table: List[List[tuple]] = [[] for _ in range(size)]
        self.operations_count = 0

    def hash_value(self, key: str) -> int:
        """키 문자열을 받아 해시 인덱스를 계산합니다. (아스키 코드 합 방식)"""
        if not key:
            return 0
        return sum(ord(char) for char in str(key)) % self.size

    def add(self, key: str, value: Any) -> dict:
        """해시 테이블에 키-값 데이터를 추가합니다."""
        idx = self.hash_value(key)
        self.operations_count += 1
        
        # 이미 존재하는 키인지 확인 후 갱신
        for i, (k, v) in enumerate(self.table[idx]):
            if k == key:
                self.table[idx][i] = (key, value)
                return {"status": "updated", "index": idx, "key": key, "value": value}
        
        # 존재하지 않으면 체이닝 방식으로 추가
        self.table[idx].append((key, value))
        return {"status": "added", "index": idx, "key": key, "value": value}

    def search(self, key: str) -> dict:
        """해시 테이블에서 키를 검색합니다."""
        idx = self.hash_value(key)
        self.operations_count += 1
        
        for i, (k, v) in enumerate(self.table[idx]):
            if k == key:
                return {
                    "found": True,
                    "index": idx,
                    "step": i,
                    "key": k,
                    "value": v,
                    "complexity": f"O(1) 평균, 최악 O(N) [탐색 단계: {i+1}]"
                }
        return {
            "found": False,
            "index": idx,
            "key": key,
            "complexity": "O(1) 평균"
        }

    def remove(self, key: str) -> dict:
        """해시 테이블에서 키를 삭제합니다."""
        idx = self.hash_value(key)
        self.operations_count += 1
        
        for i, (k, v) in enumerate(self.table[idx]):
            if k == key:
                del self.table[idx][i]
                return {"status": "removed", "index": idx, "key": key}
        
        raise HTTPException(status_code=404, error="Key not found")

    def dump(self) -> dict:
        """현재 해시 테이블의 전체 구조를 반환합니다."""
        return {
            "size": self.size,
            "table": {str(i): bucket for i, bucket in enumerate(self.table)},
            "total_operations": self.operations_count
        }

# 전역 해시 테이블 인스턴스 생성 (기본 크기 7)
hash_table = HashTable(size=7)

# 요청 데이터 모델 정의
class KeyValueRequest(BaseModel):
    key: str
    value: Optional[Any] = None

class InitRequest(BaseModel):
    size: Optional[int] = 7

@app.post("/api/init")
def api_init(req: InitRequest):
    """해시 테이블 초기화 기능"""
    global hash_table
    size = req.size if req.size and req.size > 0 else 7
    hash_table = HashTable(size=size)
    return {"message": f"Hash table initialized with size {size}", "data": hash_table.dump()}

@app.post("/api/hash_value")
def api_hash_value(req: KeyValueRequest):
    """키의 해시값 계산 기능"""
    idx = hash_table.hash_value(req.key)
    return {"key": req.key, "hash_index": idx, "complexity": "O(L) (L은 키의 길이)"}

@app.post("/api/add")
def api_add(req: KeyValueRequest):
    """해시 테이블 데이터 추가 기능"""
    if not req.key:
        raise HTTPException(status_code=400, detail="Key is required")
    result = hash_table.add(req.key, req.value if req.value is not None else "default_val")
    return {"result": result, "dump": hash_table.dump()}

@app.post("/api/search")
def api_search(req: KeyValueRequest):
    """해시 테이블 검색 기능"""
    if not req.key:
        raise HTTPException(status_code=400, detail="Key is required")
    result = hash_table.search(req.key)
    return {"result": result, "dump": hash_table.dump()}

@app.post("/api/remove")
def api_remove(req: KeyValueRequest):
    """해시 테이블 삭제 기능"""
    if not req.key:
        raise HTTPException(status_code=400, detail="Key is required")
    try:
        result = hash_table.remove(req.key)
        return {"result": result, "dump": hash_table.dump()}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.get("/api/dump")
def api_dump():
    """해시 테이블 전체 덤프 기능"""
    return hash_table.dump()

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
