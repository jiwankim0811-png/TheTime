def insert(self, key):
    """새로운 키를 트리에 삽입하고 단계별 기록을 반환"""
    steps = []
    steps.append(f"값 {key} 삽입 시작")
    
    new_node = Node(key)
    if not self.root:
        self.root = new_node
        steps.append(f"루트 노드로 {key} 설정됨")
        return steps

    curr = self.root
    while True:
        if key < curr.key:
            steps.append(f"현재 노드({curr.key})보다 작으므로 왼쪽으로 이동")
            if not curr.left:
                curr.left = new_node
                steps.append(f"왼쪽 자식으로 {key} 삽입 완료")
                break
            curr = curr.left
        elif key > curr.key:
            steps.append(f"현재 노드({curr.key})보다 크므로 오른쪽으로 이동")
            if not curr.right:
                curr.right = new_node
                steps.append(f"오른쪽 자식으로 {key} 삽입 완료")
                break
            curr = curr.right
        else:
            steps.append(f"값 {key}이(가) 이미 존재합니다.")
            break
    return steps

def search(self, key):
    """특정 키를 검색하고 경로를 단계별로 기록"""
    steps = []
    curr = self.root
    while curr:
        steps.append(f"현재 노드({curr.key}) 확인 중...")
        if key == curr.key:
            steps.append(f"키 {key} 발견 성공!")
            return True, steps
        elif key < curr.key:
            steps.append(f"찾는 값({key})이 작으므로 왼쪽으로 이동")
            curr = curr.left
        else:
            steps.append(f"찾는 값({key})이 크므로 오른쪽으로 이동")
            curr = curr.right
    steps.append(f"키 {key}를 트에서 찾지 못했습니다.")
    return False, steps

def _min_value_node(self, node):
    """주어진 서브트리의 최솟값 노드를 반환"""
    curr = node
    while curr.left is not None:
        curr = curr.left
    return curr

def remove(self, key):
    """노드를 삭제하고 삭제 과정을 단계별로 기록"""
    steps = []
    steps.append(f"값 {key} 삭제 시도")

    def _remove_recursive(node, key):
        if not node:
            steps.append(f"삭제할 노드 {key}를 찾지 못함")
            return None
        
        if key < node.key:
            steps.append(f"왼쪽 서브트리에서 {key} 탐색")
            node.left = _remove_recursive(node.left, key)
        elif key > node.key:
            steps.append(f"오른쪽 서브트리에서 {key} 탐색")
            node.right = _remove_recursive(node.right, key)
        else:
            steps.append(f"삭제할 노드({node.key}) 발견")
            # Case 1: 자식이 없거나 하나인 경우
            if not node.left:
                steps.append(f"노드 {node.key}: 왼쪽 자식 없음, 오른쪽 자식 대체")
                return node.right
            elif not node.right:
                steps.append(f"노드 {node.key}: 오른쪽 자식 없음, 왼쪽 자식 대체")
                return node.left
            
            # Case 2: 두 자식이 모두 있는 경우 (오른쪽 서브트리의 최솟값 가져오기)
            steps.append(f"노드 {node.key}: 두 자식이 모두 존재, 오른쪽 서브트리 최소값 탐색")
            temp = self._min_value_node(node.right)
            node.key = temp.key
            steps.append(f"대체된 값으로 노드 갱신: {temp.key}")
            node.right = _remove_recursive(node.right, temp.key)
        
        return node

    self.root = _remove_recursive(self.root, key)
    steps.append(f"값 {key} 삭제 프로세스 완료")
    return steps

def dump(self):
    """트리 전체 구조를 계층형 리스트(JSON 직렬화 가능 형태)로 반환"""
    def _to_dict(node):
        if not node:
            return None
        return {
            "key": node.key,
            "left": _to_dict(node.left),
            "right": _to_dict(node.right)
        }
    return _to_dict(self.root)

def min_key(self):
    """트리 내 최소 키 반환"""
    if not self.root:
        return None
    curr = self.root
    while curr.left:
        curr = curr.left
    return curr.key

def max_key(self):
    """트리 내 최대 키 반환"""
    if not self.root:
        return None
    curr = self.root
    while curr.right:
        curr = curr.right
    return curr.keys
