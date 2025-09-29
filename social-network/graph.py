from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtGui import (QPainter, QPen, QBrush, QColor, QFont,QFontMetrics)
from PyQt5.QtCore import Qt, QPointF, QPoint
import math
import random


class SocialGraphWidget(QWidget):
    """社会关系图可视化组件（优化节点布局，支持缩放和平移）"""

    def __init__(self):
        super().__init__()
        self.graph_data = {"nodes": [], "edges": []}
        self.node_positions = {}
        self.init_ui()

        # 缩放和平移相关变量
        self.scale_factor = 1.0
        self.min_scale = 0.5
        self.max_scale = 2.0
        self.offset = QPoint(0, 0)
        self.last_pos = QPoint()

    def init_ui(self):
        self.setMinimumSize(800, 600)
        main_layout = QVBoxLayout(self)
        legend = QLabel("图例：蓝色-自己 | 绿色-好友 | 橙色-群组 | 鼠标滚轮缩放 | 拖动平移")
        legend.setFont(QFont("SimHei", 9))
        main_layout.addWidget(legend)
        main_layout.addStretch(1)
        self.setLayout(main_layout)
        self.setMouseTracking(True)

    def update_graph(self, data):
        if not isinstance(data, dict) or "nodes" not in data or "edges" not in data:
            self.graph_data = {"nodes": [], "edges": []}
            self.node_positions = {}
            self.update()
            return
        self.graph_data = data
        self.calculate_node_positions()
        self.update()

    def calculate_node_positions(self):
        nodes = self.graph_data["nodes"]
        if not nodes:
            self.node_positions = {}
            return

        current_width = max(self.width(), 800)
        current_height = max(self.height(), 600)
        center_x = current_width // 2
        center_y = current_height // 2
        # 增大最大半径，让节点分布范围更广，更离散
        max_radius = min(center_x, center_y) - 50  # 减少边距，增加分布范围

        # 找到自己的节点
        self_node = next((n for n in nodes if n["type"] == "self"), None)
        if self_node:
            self_node_id = self_node["id"]
            self.node_positions[self_node_id] = QPointF(center_x, center_y)

            # 分离好友和群组节点
            friend_nodes = [n for n in nodes if n["type"] == "friend"]
            group_nodes = [n for n in nodes if n["type"] == "group"]

            # 扩大半径范围，增加节点离散性
            friend_radius_range = (max_radius * 0.3, max_radius * 0.7)  # 扩大好友半径范围
            group_radius_range = (max_radius * 0.6, max_radius * 0.95)  # 扩大群组半径范围，更靠近边缘

            self._arrange_nodes_with_spread(friend_nodes, center_x, center_y, friend_radius_range)
            self._arrange_nodes_with_spread(group_nodes, center_x, center_y, group_radius_range)

    def _arrange_nodes_with_spread(self, nodes, center_x, center_y, radius_range):
        """
        优化的节点排列算法：
        1. 在指定半径范围内随机分布
        2. 角度均匀分配
        3. 添加随机扰动避免节点重叠
        """
        count = len(nodes)
        if count == 0:
            return

        min_radius, max_radius = radius_range
        angle_step = 2 * math.pi / count  # 基础角度间隔

        for i, node in enumerate(nodes):
            node_id = node["id"]
            # 增大角度扰动（从±15%增加到±40%），使线条角度变化更大
            angle = angle_step * i + random.uniform(-angle_step * 0.4, angle_step * 0.4)

            # 增大半径随机范围，使节点更离散，线条长度变化更大
            radius = random.uniform(min_radius, max_radius)

            # 额外添加径向扰动，进一步增加离散性
            radius += random.uniform(-max_radius * 0.1, max_radius * 0.1)
            radius = max(min_radius, min(radius, max_radius))  # 确保在范围内

            # 计算坐标
            x = center_x + radius * math.cos(angle)
            y = center_y + radius * math.sin(angle)

            # 放宽边界限制，让节点可以更靠近边缘
            x = max(30, min(x, self.width() - 30))
            y = max(30, min(y, self.height() - 30))

            self.node_positions[node_id] = QPointF(x, y)

    def paintEvent(self, event):
        try:
            painter = QPainter(self)
            painter.setRenderHint(QPainter.Antialiasing)

            # 应用缩放和平移
            painter.translate(self.offset)
            painter.scale(self.scale_factor, self.scale_factor)

            # 先绘制线条（底层）
            self.draw_edges(painter)
            # 再绘制节点（顶层）
            self.draw_nodes(painter)
        except Exception as e:
            print(f"绘制错误: {str(e)}")

    def draw_edges(self, painter):
        # 线条颜色调得更深（从100,100,100改为60,60,60），线条宽度增加
        painter.setPen(QPen(QColor(60, 60, 60), 2.5, Qt.SolidLine))  # 更深的灰色，稍粗的线条

        for edge in self.graph_data["edges"]:
            if "source" not in edge or "target" not in edge:
                continue

            source_id = edge["source"]
            target_id = edge["target"]

            if source_id in self.node_positions and target_id in self.node_positions:
                painter.drawLine(
                    self.node_positions[source_id],
                    self.node_positions[target_id]
                )

    def draw_nodes(self, painter):
        font = QFont("SimHei", 8)
        painter.setFont(font)

        for node in self.graph_data["nodes"]:
            if "id" not in node or "name" not in node or "type" not in node:
                continue

            node_id = node["id"]
            if node_id not in self.node_positions:
                continue

            pos = self.node_positions[node_id]
            name = node["name"]

            # 设置节点颜色和大小
            if node["type"] == "self":
                painter.setBrush(QBrush(QColor(70, 130, 180), Qt.SolidPattern))
                node_size = 30
            elif node["type"] == "friend":
                painter.setBrush(QBrush(QColor(107, 142, 35), Qt.SolidPattern))
                node_size = 20
            else:
                painter.setBrush(QBrush(QColor(255, 165, 0), Qt.SolidPattern))
                node_size = 40

            painter.setPen(QPen(Qt.black, 2))
            painter.drawEllipse(pos, node_size, node_size)

            self._draw_text_with_wrap(painter,
                                      int(pos.x()),
                                      int(pos.y()),
                                      node_size,
                                      name)

    def _draw_text_with_wrap(self, painter, pos_x, pos_y, node_size, text):
        metrics = QFontMetrics(painter.font())
        # 增加文本宽度，允许更多文字显示
        text_width = node_size * 3
        text_x = pos_x - text_width // 2  # 居中显示
        text_y = pos_y + node_size + 5

        wrapped_text = []
        current_line = ""

        for word in text.split():
            test_line = f"{current_line} {word}" if current_line else word
            if metrics.width(test_line) <= text_width:
                current_line = test_line
            else:
                wrapped_text.append(current_line)
                current_line = word
        if current_line:
            wrapped_text.append(current_line)

        # 移除只显示前3行的限制，显示所有行
        for i, line in enumerate(wrapped_text):
            painter.drawText(
                text_x,
                text_y + i * metrics.height(),
                text_width,
                metrics.height(),
                Qt.AlignCenter,
                line
            )

    # 缩放功能
    def wheelEvent(self, event):
        delta = event.angleDelta().y()
        if delta > 0:
            new_scale = self.scale_factor * 1.1
        else:
            new_scale = self.scale_factor / 1.1

        if self.min_scale <= new_scale <= self.max_scale:
            self.scale_factor = new_scale
            self.update()

    # 平移功能
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.last_pos = event.pos()

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            delta = event.pos() - self.last_pos
            self.last_pos = event.pos()
            self.offset += delta
            self.update()

    def resizeEvent(self, event):
        self.calculate_node_positions()
        super().resizeEvent(event)