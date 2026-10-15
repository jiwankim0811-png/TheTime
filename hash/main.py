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

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class HashTable:
    def __init__(self, size: int = 10):
        self.size = size
        self.table: List[List[tuple]] = [[] for _ in range(size)]
        self.operations_count = 0

    def hash_value(self, key: str) -> int:
        if not key:
            return 0
        return sum(ord(char) for char in str(key)) % self.size

    def add(self, key: str, value: Any) -> dict:
        idx = self.hash_value(key)
        self.operations_count += 1
        
        for i, (k, v) in enumerate(self.table[idx]):
            if k == key:
                self.table[idx][i] = (key, value)
                return {"status": "updated", "index": idx, "key": key, "value": value}
        
        self.table[idx].append((key, value))
        return {"status": "added", "index": idx, "key": key, "value": value}

    def search(self, key: str) -> dict:
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
        idx = self.hash_value(key)
        self.operations_count += 1
        
        for i, (k, v) in enumerate(self.table[idx]):
            if k == key:
                del self.table[idx][i]
                return {"status": "removed", "index": idx, "key": key}
        
        # [수정] error -> detail로 변경
        raise HTTPException(status_code=404, detail="Key not found")

    def dump(self) -> dict:
        return {
            "size": self.size,
            "table": {str(i): bucket for i, bucket in enumerate(self.table)},
            "total_operations": self.operations_count
        }

hash_table = HashTable(size=7)

class KeyValueRequest(BaseModel):
    key: str
    value: Optional[Any] = None

class InitRequest(BaseModel):
    size: Optional[int] = 7

@app.post("/api/init")
def api_init(req: InitRequest):
    global hash_table
    size = req.size if req.size and req.size > 0 else 7
    hash_table = HashTable(size=size)
    return {"message": f"Hash table initialized with size {size}", "data": hash_table.dump()}

@app.post("/api/hash_value")
def api_hash_value(req: KeyValueRequest):
    idx = hash_table.hash_value(req.key)
    return {"key": req.key, "hash_index": idx, "complexity": "O(L) (L은 키의 길이)"}

@app.post("/api/add")
def api_add(req: KeyValueRequest):
    if not req.key:
        raise HTTPException(status_code=400, detail="Key is required")
    result = hash_table.add(req.key, req.value if req.value is not None else "default_val")
    return {"result": result, "dump": hash_table.dump()}

@app.post("/api/search")
def api_search(req: KeyValueRequest):
    if not req.key:
        raise HTTPException(status_code=400, detail="Key is required")
    result = hash_table.search(req.key)
    return {"result": result, "dump": hash_table.dump()}

@app.post("/api/remove")
def api_remove(req: KeyValueRequest):
    if not req.key:
        raise HTTPException(status_code=400, detail="Key is required")
    try:
        result = hash_table.remove(req.key)
        return {"result": result, "dump": hash_table.dump()}
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=404, detail=str(e))

@app.get("/api/dump")
def api_dump():
    return hash_table.dump()

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
