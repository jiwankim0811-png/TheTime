# -*- coding: utf-8 -*-
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
# CORS 설정: 모든 도메인에서의 요청을 허용 (필요시 특정 도메인으로 제한 가능)
CORS(app, resources={r"/*": {"origins": "*"}})

# ---------------------------------------------------------
# 1. 이진 검색 트리(Binary Search Tree) 자료구조 정의
# ---------------------------------------------------------
class Node:
    """이진 검색 트리의 각 노드를 정의하는 클래스"""
    def __init__(self, key, value=None):
        self.key = key          # 노드의 키 (정렬 기준)
        self.value = value      # 노드에 저장될 부가 데이터
        self.left = None        # 왼쪽 자식 노드 레퍼런스
        self.right = None       # 오른쪽 자식 노드 레퍼런스

    def to_dict(self):
        """트리 시각화를 위해 노드 정보를 딕셔너리 형태로 변환 (재귀적)"""
        return {
            "key": self.key,
            "value": self.value,
            "left": self.left.to_dict() if self.left else None,
            "right": self.right.to_dict() if self.right else None
        }


class BinarySearchTree:
    """이진 검색 트리 핵심 로직을 구현한 클래스"""
    def __init__(self):
        self.root = None

    def add(self, key, value=None):
        """새로운 키와 값을 트리에 삽입"""
        def _add(node, key, value):
            if node is None:
                return Node(key, value)
            if key < node.key:
                node.left = _add(node.left, key, value)
            elif key > node.key:
                node.right = _add(node.right, key, value)
            else:
                # 이미 존재하는 키일 경우 값 갱신
                node.value = value
            return node

        self.root = _add(self.root, key, value)

    def search(self, key):
        """특정 키를 검색하여 존재 여부 및 값 반환"""
        current = self.root
        while current is not None:
            if key == current.key:
                return {"found": True, "key": current.key, "value": current.value}
            elif key < current.key:
                current = current.left
            else:
                current = current.right
        return {"found": False, "key": key, "value": None}

    def remove(self, key):
        """특정 키를 가진 노드를 삭제"""
        def _min_value_node(node):
            current = node
            while current.left is not None:
                current = current.left
            return current

        def _remove(node, key):
            if node is None:
                return None
            
            if key < node.key:
                node.left = _remove(node.left, key)
            elif key > node.key:
                node.right = _remove(node.right, key)
            else:
                # 1. 자식이 없거나 하나인 경우
                if node.left is None:
                    return node.right
                elif node.right is None:
                    return node.left
                
                # 2. 두 자식이 모두 있는 경우: 오른쪽 서브트리의 최소값을 현재 노드에 복사
                temp = _min_value_node(node.right)
                node.key = temp.key
                node.value = temp.value
                node.right = _remove(node.right, temp.key)
            return node

        self.root = _remove(self.root, key)

    def dump(self):
        """전체 트리의 구조를 반환 (중위 순회 결과 및 계층형 구조)"""
        elements = []
        def _inorder(node):
            if node:
                _inorder(node.left)
                elements.append({"key": node.key, "value": node.value})
                _inorder(node.right)
        
        _inorder(self.root)
        return {
            "inorder": elements,
            "tree_structure": self.root.to_dict() if self.root else None
        }

    def min_key(self):
        """트리 내 최소 키 반환"""
        if self.root is None:
            return None
        current = self.root
        while current.left is not None:
            current = current.left
        return {"min_key": current.key, "value": current.value}

    def max_key(self):
        """트리 내 최대 키 반환"""
        if self.root is None:
            return None
        current = self.root
        while current.right is not None:
            current = current.right
        return {"max_key": current.key, "value": current.value}


# 전역 BST 인스턴스 생성 (서버 메모리 상에 유지)
bst = __import__('sys').modules[__name__] # 보조용 변수 할당 방지
bst_instance = BinarySearchTree()


# ---------------------------------------------------------
# 2. API 엔드포인트 라우팅 설정
# ---------------------------------------------------------
@app.route("/", methods=["GET"])
def health_check():
    """서버 상태 확인 엔드포인트"""
    return jsonify({"status": "online", "message": "Cloud Run BST Server is running successfully."}), 200


@app.route("/bst/<action>", methods=["POST"])
def handle_bst_action(action):
    """
    이진 검색 트리 연산 처리 엔드포인트
    action 종류: add, search, remove, dump, min_key, max_key
    """
    try:
        data = request.get_json() or {}
        key = data.get("key")
        value = data.get("value")

        result = {}
        if action == "add":
            if key is None:
                return jsonify({"error": "Key is required for insertion."}), 400
            bst_instance.add(int(key), value)
            result = {"message": f"Key {key} added successfully.", "tree": bst_instance.dump()}
            
        elif action == "search":
            if key is None:
                return jsonify({"error": "Key is required for search."}), 400
            result = bst_instance.search(int(key))
            
        elif action == "remove":
            if key is None:
                return jsonify({"error": "Key is required for removal."}), 400
            bst_instance.remove(int(key))
            result = {"message": f"Key {key} removed successfully.", "tree": bst_instance.dump()}
            
        elif action == "dump":
            result = bst_instance.dump()
            
        elif action == "min_key":
            result = bst_instance.min_key()
            
        elif action == "max_key":
            result = bst_instance.max_key()
            
        else:
            return jsonify({"error": f"Invalid action: {action}"}), 400

        return jsonify({"success": True, "action": action, "result": result}), 200

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
