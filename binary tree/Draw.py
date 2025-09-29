from PyQt5.QtGui import QPainter, QPen, QFont, QColor, QWheelEvent
from PyQt5.QtCore import Qt, QPointF, QRectF, QPoint
from PyQt5.QtWidgets import QWidget
import math


class DrawWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.root = None
        self.setMinimumSize(800, 400)
        self.setBackgroundRole(self.palette().Base)
        self.setAutoFillBackground(True)

        # 缩放和平移相关变量
        self.scale = 1.0
        self.offset = QPoint(0, 0)
        self.last_pos = QPoint()
        self.dragging = False

        # 缩放上下限
        self.min_scale = 0.1  # 最小缩放比例
        self.max_scale = 3.0  # 最大缩放比例

    def set_tree(self, root):
        self.root = root
        self.scale = 1.0  # 重置缩放
        self.offset = QPoint(0, 0)  # 重置偏移
        self.update()  # 触发paintEvent

    def paintEvent(self, event):
        if not self.root:
            return

        painter = QPainter(self)
        # 设置反锯齿
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setRenderHint(QPainter.TextAntialiasing)

        # 应用缩放和平移
        painter.save()
        painter.translate(self.width() // 2 + self.offset.x(), self.height() // 4 + self.offset.y())
        painter.scale(self.scale, self.scale)

        # 设置字体
        font = QFont()
        font.setPointSize(12)
        font.setBold(True)
        painter.setFont(font)

        # 设置画笔
        pen = QPen()
        pen.setWidth(2)
        pen.setColor(QColor(Qt.blue))
        pen.setStyle(Qt.SolidLine)
        pen.setCapStyle(Qt.FlatCap)
        pen.setJoinStyle(Qt.BevelJoin)
        painter.setPen(pen)

        # 计算树的高度和宽度
        tree_height = self.calculate_height(self.root)
        tree_width = self.calculate_width(self.root)
        if tree_height < 1 or tree_width < 1:
            painter.restore()
            return

        # 计算节点半径和层间距（根据树的大小动态调整）
        base_radius = 20
        max_possible_width = (self.width() * 0.8) / self.scale
        max_possible_height = (self.height() * 0.8) / self.scale

        # 根据树的宽度计算合适的节点半径
        r = min(base_radius, max_possible_width / (2 * tree_width))
        # 根据树的高度计算合适的层间距
        layer_height = max(60, min(150, max_possible_height / (tree_height - 1))) if tree_height > 1 else 100

        # 绘制树
        self.draw_tree(painter, self.root, 0, 0, r, layer_height, tree_height)

        painter.restore()

    def draw_tree(self, painter, node, x, y, radius, layer_height, tree_height, current_layer=1):
        """递归绘制树"""
        if not node:
            return

        # 保存当前状态
        painter.save()
        # 移动到当前节点位置
        painter.translate(x, y)
        # 绘制节点
        self.draw_node(painter, radius, node.data)

        # 计算子节点的水平偏移
        offset = (2 ** (tree_height - current_layer)) * radius

        # 绘制右子树
        if node.right_child and node.right_tag == 0:
            # 计算右子节点位置（转换为整数）
            right_x = int(offset)
            right_y = int(layer_height)

            # 绘制右分支（所有坐标转换为整数）
            painter.drawLine(0, int(radius), right_x, right_y - int(radius))

            # 递归绘制右子树
            self.draw_tree(painter, node.right_child, right_x, right_y, radius, layer_height, tree_height,
                           current_layer + 1)

        # 绘制左子树
        if node.left_child and node.left_tag == 0:
            # 计算左子节点位置（转换为整数）
            left_x = int(-offset)
            left_y = int(layer_height)

            # 绘制左分支（所有坐标转换为整数）
            painter.drawLine(0, int(radius), left_x, left_y - int(radius))

            # 递归绘制左子树
            self.draw_tree(painter, node.left_child, left_x, left_y, radius, layer_height, tree_height,
                           current_layer + 1)

        painter.restore()

    def draw_node(self, painter, radius, data):
        """绘制节点（圆形+文本）"""
        rect = QRectF(-radius, -radius, 2 * radius, 2 * radius)
        painter.drawEllipse(rect)
        painter.drawText(rect, Qt.AlignCenter, str(data))

    def calculate_height(self, node):
        """计算树的高度"""
        if not node:
            return 0
        left_height = self.calculate_height(node.left_child) if (node.left_child and node.left_tag == 0) else 0
        right_height = self.calculate_height(node.right_child) if (node.right_child and node.right_tag == 0) else 0
        return max(left_height, right_height) + 1

    def calculate_width(self, node):
        """计算树的宽度（最宽层的节点数）"""
        if not node:
            return 0

        max_width = 0
        # 使用层次遍历计算每一层的宽度
        queue = [node]

        while queue:
            level_width = len(queue)
            max_width = max(max_width, level_width)

            # 处理当前层的所有节点
            for _ in range(level_width):
                current = queue.pop(0)
                if current.left_child and current.left_tag == 0:
                    queue.append(current.left_child)
                if current.right_child and current.right_tag == 0:
                    queue.append(current.right_child)

        return max_width

    def wheelEvent(self, event: QWheelEvent):
        """鼠标滚轮事件：缩放（带上下限）"""
        delta = event.angleDelta().y()
        if delta > 0:
            # 放大：不超过最大缩放比例
            new_scale = self.scale * 1.1
            if new_scale <= self.max_scale:
                self.scale = new_scale
        else:
            # 缩小：不小于最小缩放比例
            new_scale = self.scale * 0.9
            if new_scale >= self.min_scale:
                self.scale = new_scale
        self.update()

    def mousePressEvent(self, event):
        """鼠标按下事件：开始拖动"""
        if event.button() == Qt.LeftButton:
            self.last_pos = event.pos()
            self.dragging = True

    def mouseMoveEvent(self, event):
        """鼠标移动事件：拖动平移"""
        if self.dragging:
            self.offset += event.pos() - self.last_pos
            self.last_pos = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        """鼠标释放事件：结束拖动"""
        if event.button() == Qt.LeftButton:
            self.dragging = False