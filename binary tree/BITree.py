class Node:
    def __init__(self,data):
        self.data = data    #数值
        self.left_child = None  #左孩子/线索
        self.right_child = None #右孩子/线索
        self.left_tag = 0   #0为左孩子，1为左线索
        self.right_tag = 0  #0为右孩子，1为右线索

def create_binary_tree(pre_order):
    if not pre_order:
        return None
    data = pre_order.pop(0)
    if data == '#':
        return None
    node = Node(data)
    node.left_child = create_binary_tree(pre_order)
    node.right_child = create_binary_tree(pre_order)
    return node

def pre_order_traverse(node, result=None):
    if result is None:
        result = []
    if node:
        result.append(node.data)
        pre_order_traverse(node.left_child, result)
        pre_order_traverse(node.right_child, result)
    return result

def mid_order_traverse(node, result=None):
    if result is None:
        result = []
    if node:
        mid_order_traverse(node.left_child, result)
        result.append(node.data)
        mid_order_traverse(node.right_child, result)
    return result

def post_order_traverse(node, result=None):
    if result is None:
        result = []
    if node:
        post_order_traverse(node.left_child, result)
        post_order_traverse(node.right_child, result)
        result.append(node.data)
    return result

def count_node(node):
    if not node:
        return 0
    if not node.left_child and not node.right_child:
        return 1
    return count_node(node.left_child) + count_node(node.right_child) + 1

def count_leaf_node(node):
    if not node:
        return 0
    if not node.left_child and not node.right_child:
        return 1
    return count_leaf_node(node.left_child) + count_leaf_node(node.right_child)

class Thread:
    @staticmethod
    def mid_order_threading(root):
        pre = None
        def thread(node):
            nonlocal pre
            if not node:
                return
            thread(node.left_child)
            if not node.left_child:
                node.left_tag = 1
                node.left_child = pre
            if pre and not pre.right_child:
                pre.right_tag = 1
                pre.right_child = node
            pre = node
            thread(node.right_child)
        if root:
            thread(root)
            if pre and not pre.right_child:
                pre.right_tag = 1
                pre.right_child = None

    @staticmethod
    def pre_order_threading(root):
        pre = None
        def thread(node):
            nonlocal pre
            if not node:
                return
            if not node.left_child:
                node.left_tag = 1
                node.left_child = pre
            if pre and not pre.right_child:
                pre.right_tag = 1
                pre.right_child = node
            pre = node
            if node.left_tag == 0:
                thread(node.left_child)
            if node.right_tag == 0:
                thread(node.right_child)
        if root:
            thread(root)
            if pre and not pre.right_child:
                pre.right_tag = 1
                pre.right_child = None

    @staticmethod
    def post_order_threading(root):
        """后序线索化"""
        pre = None

        def thread(node):
            nonlocal pre
            if not node:
                return
            thread(node.left_child)
            thread(node.right_child)
            # 处理左线索
            if not node.left_child:
                node.left_tag = 1
                node.left_child = pre
            # 处理前驱节点的右线索
            if pre and not pre.right_child:
                pre.right_tag = 1
                pre.right_child = node
            pre = node

        if root:
            thread(root)
            if pre and not pre.right_child:
                pre.right_tag = 1
                pre.right_child = None

def mid_order_thread_traverse(root):
    """中序线索树遍历"""
    result = []
    if not root:
        return result
    node = root
    while node:
        # 找到最左节点
        while node.left_tag == 0:
            node = node.left_child
        result.append(node.data)
        # 沿右线索遍历
        while node.right_tag == 1 and node.right_child:
            node = node.right_child
            result.append(node.data)
        # 进入右子树
        node = node.right_child
    return result

def pre_order_thread_traverse(root):
    """先序线索树遍历"""
    result = []
    if not root:
        return result
    node = root
    while node:
        result.append(node.data)
        # 左孩子存在时优先遍历左子树
        if node.left_tag == 0:
            node = node.left_child
        # 否则通过右线索跳转
        else:
            node = node.right_child
    return result

def reset_thread_tags(root):
    """重置所有节点的线索标记和指针为初始状态（仅保留真实孩子节点）"""
    if not root:
        return
    # 递归重置左子树
    if root.left_tag == 0:  # 只有左孩子是真实节点时才递归（线索不需要处理）
        reset_thread_tags(root.left_child)
    else:
        # 还原左线索为None（恢复空指针）
        root.left_child = None
        root.left_tag = 0
    # 递归重置右子树
    if root.right_tag == 0:  # 只有右孩子是真实节点时才递归
        reset_thread_tags(root.right_child)
    else:
        # 还原右线索为None（恢复空指针）
        root.right_child = None
        root.right_tag = 0


def print_thread_info(root):
    """生成线索化节点信息文本"""
    result = []

    def _collect(node):
        if not node:
            return
        l_info = f"左{'线索' if node.left_tag == 1 else '孩子'}: {node.left_child.data if node.left_child else 'None'}"
        r_info = f"右{'线索' if node.right_tag == 1 else '孩子'}: {node.right_child.data if node.right_child else 'None'}"
        result.append(f"节点 {node.data}: {l_info}, {r_info}")
        if node.left_tag == 0:
            _collect(node.left_child)
        if node.right_tag == 0:
            _collect(node.right_child)

    _collect(root)
    return "\n".join(result)