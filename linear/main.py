import os
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
# GAS 웹 앱 및 로컬 테스트 환경에서의 CORS 허용
CORS(app)

@app.route('/linear-search', methods=['POST'])
def linear_search():
    """
    선형 검색(Linear Search) 수행 API
    
    [Request Body JSON]
    {
        "array": [10, 20, 30, 40, 50],  # 검색 대상 배열 (숫자 리스트)
        "target": 30                     # 찾을 값
    }
    
    [Response JSON]
    {
        "array": [...],
        "target": ...,
        "found": True/False,
        "found_index": 인덱스 또는 -1,
        "steps": [
            {
                "step": 단계 번호(1부터 시작),
                "index": 현재 검사 중인 인덱스,
                "current_value": 현재 인덱스의 값,
                "is_match": 일치 여부 (True/False),
                "description": 단계별 설명 텍스트
            }, ...
        ],
        "complexity": {
            "time_best": "O(1)",
            "time_worst": "O(N)",
            "time_average": "O(N)",
            "space": "O(1)"
        }
    }
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "유효하지 않은 JSON 요청입니다."}), 400

        array = data.get('array', [])
        target = data.get('target', None)

        # 예외 처리: 데이터 입력 검증
        if not isinstance(array, list) or target is None:
            return jsonify({"error": "'array'(리스트)와 'target'(값) 필드가 필요합니다."}), 400

        # 선형 검색 알고리즘 수행 및 단계별 기록
        steps = []
        found = False
        found_index = -1

        for i in range(len(array)):
            current_val = array[i]
            is_match = (current_val == target)

            # 각 단계의 상태를 기록
            step_info = {
                "step": i + 1,
                "index": i,
                "current_value": current_val,
                "is_match": is_match,
                "description": f"Index {i}: 값 {current_val}을(를) 타겟 {target}과(와) 비교합니다. " + 
                               ("-> 일치!" if is_match else "-> 불일치")
            }
            steps.append(step_info)

            # 타겟을 찾은 경우 반복 종료
            if is_match:
                found = True
                found_index = i
                break

        # 시간 및 공간 복잡도 정보
        complexity = {
            "time_best": "O(1) - 첫 번째 요소에서 발견할 경우",
            "time_worst": "O(N) - 마지막 요소에 있거나 존재하지 않을 경우",
            "time_average": "O(N)",
            "space": "O(1) - 추가 메모리 거의 미사용"
        }

        # 결과 응답 반환
        return jsonify({
            "status": "success",
            "array": array,
            "target": target,
            "found": found,
            "found_index": found_index,
            "steps": steps,
            "total_steps": len(steps),
            "complexity": complexity
        }), 200

    except Exception as e:
        return jsonify({"error": f"서버 내부 오류 발생: {str(e)}"}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """서버 상태 확인용 헬스체크 엔드포인트"""
    return jsonify({"status": "ok", "message": "Cloud Run Server is running"}), 200

if __name__ == '__main__':
    # Cloud Run은 PORT 환경변수를 전달하므로 이를 기본값으로 설정
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
