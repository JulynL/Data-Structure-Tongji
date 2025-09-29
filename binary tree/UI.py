import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QTextEdit, QGroupBox, QGridLayout, QAction, QStatusBar

from BITree import *
from Draw import *

class BiTreeApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.root = None  # 二叉树根节点
        self.init_ui()

    def init_ui(self):
        # 窗口基本设置
        self.setWindowTitle("二叉树操作工具")
        self.setGeometry(100, 100, 1600, 1200)

        # 创建菜单栏
        self.create_menu_bar()

        # 创建中心部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # 1. 输入区域
        input_group = QGroupBox("先序序列输入（用#表示空节点，逗号分隔，例如：A,B,#,#,C）")
        input_layout = QHBoxLayout()
        self.pre_order_input = QLineEdit()
        self.pre_order_input.setPlaceholderText("请输入先序序列...")
        self.btn_create = QPushButton("创建二叉树")
        self.btn_clear_input = QPushButton("清空输入")

        input_layout.addWidget(self.pre_order_input)
        input_layout.addWidget(self.btn_create)
        input_layout.addWidget(self.btn_clear_input)
        input_group.setLayout(input_layout)
        main_layout.addWidget(input_group)

        # 2. 功能按钮区域
        btn_group = QGroupBox("操作")
        btn_layout = QGridLayout()

        # 第一行：遍历按钮
        self.btn_pre_order = QPushButton("先序遍历")
        self.btn_mid_order = QPushButton("中序遍历")
        self.btn_post_order = QPushButton("后序遍历")

        # 第二行：线索化按钮
        self.btn_pre_thread = QPushButton("先序线索化")
        self.btn_mid_thread = QPushButton("中序线索化")
        self.btn_post_thread = QPushButton("后序线索化")

        # 第三行：其他功能按钮
        self.btn_count_leaves = QPushButton("统计叶子节点")
        self.btn_show_thread = QPushButton("显示线索信息")
        self.btn_show_information = QPushButton("显示开发人员信息")

        # 布局按钮
        btn_layout.addWidget(self.btn_pre_order, 0, 0)
        btn_layout.addWidget(self.btn_mid_order, 0, 1)
        btn_layout.addWidget(self.btn_post_order, 0, 2)
        btn_layout.addWidget(self.btn_pre_thread, 1, 0)
        btn_layout.addWidget(self.btn_mid_thread, 1, 1)
        btn_layout.addWidget(self.btn_post_thread, 1, 2)
        btn_layout.addWidget(self.btn_count_leaves, 2, 0)
        btn_layout.addWidget(self.btn_show_thread, 2, 1)
        btn_layout.addWidget(self.btn_show_information, 2, 2)

        btn_group.setLayout(btn_layout)
        main_layout.addWidget(btn_group)

        # 3. 输出区域
        output_group = QGroupBox("输出结果")
        output_layout = QVBoxLayout()
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        output_layout.addWidget(self.output_text)
        output_group.setLayout(output_layout)
        main_layout.addWidget(output_group, 1)  # 占更多空间

        # 状态栏
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.statusBar.showMessage("就绪")

        # 添加绘图区域（在输出区域上方或下方）
        self.draw_widget = DrawWidget(self)
        main_layout.addWidget(self.draw_widget, 2)  # 给绘图区域更多空间

        # 绑定信号与槽
        #self.btn_create.clicked.connect(self.on_create_tree)
        self.bind_signals()

    def create_menu_bar(self):
        """创建菜单栏"""
        menubar = self.menuBar()

        # 退出
        file_menu = menubar.addMenu("退出")
        exit_action = QAction("退出", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # 操作菜单
        op_menu = menubar.addMenu("操作")
        create_action1 = QAction("创建二叉树", self)
        create_action2 = QAction("清空输入", self)
        create_action3 = QAction("先序遍历", self)
        create_action4 = QAction("中序遍历", self)
        create_action5 = QAction("后序遍历", self)
        create_action6 = QAction("先序线索化", self)
        create_action7 = QAction("中序线索化", self)
        create_action8 = QAction("后序线索化", self)
        create_action9 = QAction("统计叶子节点", self)
        create_action10 = QAction("显示线索信息", self)
        create_action11 = QAction("显示开发人员信息", self)
        create_action1.triggered.connect(self.on_create_tree)
        create_action2.triggered.connect(lambda: self.pre_order_input.clear())
        create_action3.triggered.connect(self.on_pre_order)
        create_action4.triggered.connect(self.on_mid_order)
        create_action5.triggered.connect(self.on_post_order)
        create_action6.triggered.connect(self.on_pre_thread)
        create_action7.triggered.connect(self.on_mid_thread)
        create_action8.triggered.connect(self.on_post_thread)
        create_action9.triggered.connect(self.on_count_leaves)
        create_action10.triggered.connect(self.on_show_thread)
        create_action11.triggered.connect(self.on_show_information)
        op_menu.addAction(create_action1)
        op_menu.addAction(create_action2)
        op_menu.addAction(create_action3)
        op_menu.addAction(create_action4)
        op_menu.addAction(create_action5)
        op_menu.addAction(create_action6)
        op_menu.addAction(create_action7)
        op_menu.addAction(create_action8)
        op_menu.addAction(create_action9)
        op_menu.addAction(create_action10)
        op_menu.addAction(create_action11)

        # 帮助菜单
        help_menu = menubar.addMenu("帮助")
        about_action = QAction("操作说明", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

    def bind_signals(self):
        """绑定按钮事件"""
        self.btn_create.clicked.connect(self.on_create_tree)
        self.btn_clear_input.clicked.connect(lambda: self.pre_order_input.clear())
        self.btn_pre_order.clicked.connect(self.on_pre_order)
        self.btn_mid_order.clicked.connect(self.on_mid_order)
        self.btn_post_order.clicked.connect(self.on_post_order)
        self.btn_pre_thread.clicked.connect(self.on_pre_thread)
        self.btn_mid_thread.clicked.connect(self.on_mid_thread)
        self.btn_post_thread.clicked.connect(self.on_post_thread)
        self.btn_count_leaves.clicked.connect(self.on_count_leaves)
        self.btn_show_information.clicked.connect(self.on_show_information)
        self.btn_show_thread.clicked.connect(self.on_show_thread)

    # 按钮事件处理函数
    def on_create_tree(self):
        """创建二叉树"""
        pre_str = self.pre_order_input.text().strip()
        if not pre_str:
            self.output_text.append("错误：请输入先序序列！")
            return
        pre_order = pre_str.split(',')
        self.root = create_binary_tree(pre_order.copy())
        self.output_text.append("二叉树创建成功！")
        self.draw_widget.set_tree(self.root)  # 设置树并触发重绘
        self.statusBar.showMessage("二叉树创建成功")

    def on_pre_order(self):
        """先序遍历"""
        if not self.root:
            self.output_text.append("请先创建二叉树！")
            return
        reset_thread_tags(self.root)
        result = pre_order_traverse(self.root)
        self.output_text.append(f"先序遍历结果：{result}")

    def on_mid_order(self):
        """中序遍历"""
        if not self.root:
            self.output_text.append("请先创建二叉树！")
            return
        reset_thread_tags(self.root)
        result = mid_order_traverse(self.root)
        self.output_text.append(f"中序遍历结果：{result}")

    def on_post_order(self):
        """后序遍历"""
        if not self.root:
            self.output_text.append("请先创建二叉树！")
            return
        reset_thread_tags(self.root)
        result = post_order_traverse(self.root)
        self.output_text.append(f"后序遍历结果：{result}")

    def on_pre_thread(self):
        """先序线索化"""
        if not self.root:
            self.output_text.append("请先创建二叉树！")
            return
        reset_thread_tags(self.root)
        Thread.pre_order_threading(self.root)
        result = pre_order_thread_traverse(self.root)
        self.output_text.append(f"先序线索化完成，线索遍历结果：{result}")

    def on_mid_thread(self):
        """中序线索化"""
        if not self.root:
            self.output_text.append("请先创建二叉树！")
            return
        reset_thread_tags(self.root)
        Thread.mid_order_threading(self.root)
        result = mid_order_thread_traverse(self.root)
        self.output_text.append(f"中序线索化完成，线索遍历结果：{result}")

    def on_post_thread(self):
        """后序线索化"""
        if not self.root:
            self.output_text.append("请先创建二叉树！")
            return
        reset_thread_tags(self.root)
        Thread.post_order_threading(self.root)
        self.output_text.append(f"后序线索化完成")

    def on_count_leaves(self):
        """统计叶子节点"""
        if not self.root:
            self.output_text.append("请先创建二叉树！")
            return
        reset_thread_tags(self.root)
        count = count_node(self.root)
        count_leaf = count_leaf_node(self.root)
        self.output_text.append(f"总节点个数：{count}    ")
        self.output_text.append(f"叶子节点个数：{count_leaf}")

    def on_show_information(self):
        """显示开发人员信息"""
        self.output_text.append("开发人员信息：\n" + "姓名：陆彦翔\n" + "学号：2352975\n" + "专业：信息安全\n")

    def on_show_thread(self):
        """显示线索信息"""
        if not self.root:
            self.output_text.append("请先创建二叉树并进行线索化！")
            return
        thread_info = print_thread_info(self.root)
        self.output_text.append("线索化节点信息：\n" + thread_info)

    def show_about(self):
        """显示关于信息"""
        self.output_text.append("《数据结构》课程设计 - 二叉树操作工具使用说明：")
        self.output_text.append("在输入框中输入先序序列来构建二叉树，用逗号分隔每个节点，用'#'表示空节点。")
        self.output_text.append("构建完成后点击按钮或者使用菜单栏'操作'中的内容展示对应功能，构建线索完成后如要查看请立刻点击显示线索信息来查看，若使用其他操作可能导致指针重置无法展示新构建的线索。")
        self.output_text.append("绘制的二叉树信息可以使用ctrl+滚轮进行缩放，拖动画布进行移动\n")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BiTreeApp()
    window.show()
    sys.exit(app.exec_())