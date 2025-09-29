import sys
from PyQt5.QtWidgets import (QMainWindow, QTabWidget, QWidget, QVBoxLayout,
                             QHBoxLayout, QPushButton, QLineEdit, QListWidget,
                             QListWidgetItem, QLabel, QGroupBox, QFormLayout,
                             QTextEdit, QMessageBox, QSplitter, QApplication,
                             QInputDialog, QDialog, QComboBox)
from PyQt5.QtGui import QFont, QIcon, QColor
from PyQt5.QtCore import Qt
from graph import SocialGraphWidget
from logic import SocialNetworkLogic
import random


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.logic = SocialNetworkLogic()
        self.current_user_id = None
        self.init_ui()
        self.init_test_data()

    def init_ui(self):
        #窗口基本设置
        self.setWindowTitle("社会关系网络系统-2352975陆彦翔")
        self.setGeometry(100, 100, 1600, 1200)
        self.setFont(QFont("SimHei", 10))
        # 中心部件和主布局
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        user_ops_layout = QHBoxLayout()
        # 用户ID输入
        self.le_user_id = QLineEdit()
        self.le_user_id.setPlaceholderText("输入用户ID")
        user_ops_layout.addWidget(QLabel("当前用户:"))
        user_ops_layout.addWidget(self.le_user_id)
        #加载用户按钮
        self.btn_load_user = QPushButton("加载用户")
        self.btn_load_user.clicked.connect(self.load_user)
        user_ops_layout.addWidget(self.btn_load_user)
        #添加用户按钮
        self.btn_add_user = QPushButton("新增用户")
        self.btn_add_user.clicked.connect(self.add_user_dialog)
        user_ops_layout.addWidget(self.btn_add_user)
        #删除用户按钮
        self.btn_delete_user = QPushButton("删除用户")
        self.btn_delete_user.clicked.connect(self.delete_user)
        user_ops_layout.addWidget(self.btn_delete_user)
        #添加群组按钮
        self.btn_add_group = QPushButton("新增群组")
        self.btn_add_group.clicked.connect(self.add_group_dialog)
        user_ops_layout.addWidget(self.btn_add_group)
        main_layout.addLayout(user_ops_layout)

        #创建标签页控件
        self.tabs = QTabWidget()
        #社会关系图标签页
        self.tab_graph = QWidget()
        graph_layout = QVBoxLayout(self.tab_graph)
        self.graph_widget = SocialGraphWidget()  # 关系图可视化组件
        graph_layout.addWidget(self.graph_widget)
        self.tabs.addTab(self.tab_graph, "社会关系图")
        #潜在好友推荐标签页
        self.tab_potential = QWidget()
        self.init_potential_tab()
        self.tabs.addTab(self.tab_potential, "潜在好友推荐")
        #兴趣群组推荐标签页
        self.tab_groups = QWidget()
        self.init_groups_tab()
        self.tabs.addTab(self.tab_groups, "兴趣群组推荐")
        #用户信息标签页
        self.tab_profile = QWidget()
        self.init_profile_tab()
        self.tabs.addTab(self.tab_profile, "用户信息")
        #群组管理标签页
        self.tab_group_manage = QWidget()
        self.init_group_manage_tab()
        self.tabs.addTab(self.tab_group_manage, "群组管理")
        #所有用户列表标签页
        self.tab_all_users = QWidget()
        self.init_all_users_tab()
        self.tabs.addTab(self.tab_all_users, "所有用户")
        #所有群组列表标签页
        self.tab_all_groups = QWidget()
        self.init_all_groups_tab()
        self.tabs.addTab(self.tab_all_groups, "所有群组")
        main_layout.addWidget(self.tabs)

    #初始化新标签页
    def init_all_users_tab(self):
        """初始化所有用户列表标签页"""
        layout = QVBoxLayout(self.tab_all_users)
        #刷新按钮
        btn_refresh = QPushButton("刷新用户列表")
        btn_refresh.clicked.connect(self.refresh_all_users)
        layout.addWidget(btn_refresh)
        #用户列表
        self.lw_all_users = QListWidget()
        self.lw_all_users.setAlternatingRowColors(True)
        self.lw_all_users.setSortingEnabled(False)
        layout.addWidget(self.lw_all_users)
        #初始加载
        self.refresh_all_users()

    #所有群组信息
    def init_all_groups_tab(self):
        layout = QVBoxLayout(self.tab_all_groups)
        #刷新群组
        ops_layout = QHBoxLayout()
        btn_refresh = QPushButton("刷新群组列表")
        btn_refresh.clicked.connect(self.refresh_all_groups)
        ops_layout.addWidget(btn_refresh)
        #选中群组按钮
        self.btn_join_group_from_all = QPushButton("加入选中群组")
        self.btn_join_group_from_all.clicked.connect(self.join_selected_group_from_all)
        ops_layout.addWidget(self.btn_join_group_from_all)
        layout.addLayout(ops_layout)
        #群组列表显示
        self.lw_all_groups = QListWidget()
        self.lw_all_groups.setAlternatingRowColors(True)
        self.lw_all_groups.setSortingEnabled(False)
        layout.addWidget(self.lw_all_groups)
        # 初始加载
        self.refresh_all_groups()

    #刷新用户列表
    def refresh_all_users(self):
        self.lw_all_users.clear()
        all_users = self.logic.network.get_all_users()
        all_users.sort(key=lambda user: user.user_id)
        for user in all_users:
            item_text = f"用户ID: {user.user_id} | 姓名: {user.name}"
            item = QListWidgetItem(item_text)
            self.lw_all_users.addItem(item)

    #刷新群组列表
    def refresh_all_groups(self):
        self.lw_all_groups.clear()
        all_groups = self.logic.network.get_all_groups()
        all_groups.sort(key=lambda group: group.group_id)
        for group in all_groups:
            item_text = f"群组ID: {group.group_id} | 名称: {group.name}"
            item = QListWidgetItem(item_text)
            self.lw_all_groups.addItem(item)

    #初始化潜在好友标签
    def init_potential_tab(self):
        """增强的潜在好友推荐标签页（保留搜索功能）"""
        layout = QVBoxLayout(self.tab_potential)

        # 推荐设置区域
        settings_group = QGroupBox("推荐设置")
        settings_layout = QHBoxLayout()

        settings_layout.addWidget(QLabel("排序方式:"))
        self.sort_criteria = QComboBox()
        self.sort_criteria.addItems(["按相似度", "按共同好友数", "按共同群组数"])
        settings_layout.addWidget(self.sort_criteria)

        settings_layout.addWidget(QLabel("推荐数量:"))
        self.le_limit_friends = QLineEdit("10")
        self.le_limit_friends.setFixedWidth(50)
        settings_layout.addWidget(self.le_limit_friends)

        self.btn_refresh_friends = QPushButton("刷新推荐")
        self.btn_refresh_friends.clicked.connect(self.refresh_potential_friends)
        settings_layout.addWidget(self.btn_refresh_friends)

        settings_group.setLayout(settings_layout)
        layout.addWidget(settings_group)

        # 搜索区域
        search_group = QGroupBox("搜索用户")
        search_layout = QHBoxLayout()

        search_layout.addWidget(QLabel("搜索好友:"))
        self.le_search_friend = QLineEdit()
        self.le_search_friend.setPlaceholderText("输入用户ID或姓名")
        search_layout.addWidget(self.le_search_friend)

        self.btn_search_friend = QPushButton("搜索")
        self.btn_search_friend.clicked.connect(self.search_friends)
        search_layout.addWidget(self.btn_search_friend)

        search_group.setLayout(search_layout)
        layout.addWidget(search_group)

        # 操作按钮区域
        btn_layout = QHBoxLayout()
        self.btn_add_friend = QPushButton("添加选中好友")
        self.btn_add_friend.clicked.connect(self.add_selected_friend)
        btn_layout.addWidget(self.btn_add_friend)

        self.btn_remove_friend = QPushButton("删除选中好友")
        self.btn_remove_friend.clicked.connect(self.remove_selected_friend)
        btn_layout.addWidget(self.btn_remove_friend)

        layout.addLayout(btn_layout)

        # 好友列表
        self.lw_potential = QListWidget()
        self.lw_potential.setAlternatingRowColors(True)
        layout.addWidget(self.lw_potential)

    def init_groups_tab(self):
        layout = QVBoxLayout(self.tab_groups)
        #推荐参数
        params_group = QGroupBox("推荐设置")
        params_layout = QHBoxLayout()
        params_layout.addWidget(QLabel("推荐数量:"))
        self.le_limit_groups = QLineEdit("5")
        self.le_limit_groups.setFixedWidth(50)
        params_layout.addWidget(self.le_limit_groups)
        self.btn_refresh_groups = QPushButton("刷新推荐")
        self.btn_refresh_groups.clicked.connect(self.refresh_recommended_groups)
        params_layout.addWidget(self.btn_refresh_groups)
        #加入群组按钮
        self.btn_join_group = QPushButton("加入选中群组")
        self.btn_join_group.clicked.connect(self.join_selected_group)
        params_layout.addWidget(self.btn_join_group)

        params_group.setLayout(params_layout)
        layout.addWidget(params_group)

        #推荐群组列表
        self.lw_groups = QListWidget()
        self.lw_groups.setAlternatingRowColors(True)
        layout.addWidget(self.lw_groups)

    def init_profile_tab(self):
        layout = QVBoxLayout(self.tab_profile)
        self.form_profile = QFormLayout()
        #用户信息
        self.le_name = QLineEdit()
        self.le_region = QLineEdit()
        self.le_schools = QLineEdit()
        self.le_workplaces = QLineEdit()
        self.le_hobbies = QLineEdit()
        self.form_profile.addRow("姓名:", self.le_name)
        self.form_profile.addRow("地区:", self.le_region)
        self.form_profile.addRow("学校(逗号分隔):", self.le_schools)
        self.form_profile.addRow("工作单位(逗号分隔):", self.le_workplaces)
        self.form_profile.addRow("爱好(逗号分隔):", self.le_hobbies)
        #操作按钮
        btn_layout = QHBoxLayout()
        self.btn_save_profile = QPushButton("保存信息")
        self.btn_save_profile.clicked.connect(self.save_profile)
        btn_layout.addWidget(self.btn_save_profile)

        layout.addLayout(self.form_profile)
        layout.addLayout(btn_layout)
        layout.addStretch()

    def init_group_manage_tab(self):
        layout = QVBoxLayout(self.tab_group_manage)
        #群组操作按钮
        ops_layout = QHBoxLayout()
        self.le_group_id = QLineEdit()
        self.le_group_id.setPlaceholderText("输入群组ID")
        ops_layout.addWidget(QLabel("群组ID:"))
        ops_layout.addWidget(self.le_group_id)
        self.btn_load_group = QPushButton("加载群组")
        self.btn_load_group.clicked.connect(self.load_group)
        ops_layout.addWidget(self.btn_load_group)
        self.btn_delete_group = QPushButton("删除群组")
        self.btn_delete_group.clicked.connect(self.delete_group)
        ops_layout.addWidget(self.btn_delete_group)
        self.btn_leave_group = QPushButton("退出选中群组")
        self.btn_leave_group.clicked.connect(self.leave_selected_group)
        ops_layout.addWidget(self.btn_leave_group)
        layout.addLayout(ops_layout)

        #群组信息
        self.form_group = QFormLayout()
        self.le_group_name = QLineEdit()
        self.le_group_topic = QLineEdit()
        self.le_group_tags = QLineEdit()  # 用逗号分隔多个标签
        self.form_group.addRow("群组名称:", self.le_group_name)
        self.form_group.addRow("群组主题:", self.le_group_topic)
        self.form_group.addRow("群组标签(逗号分隔):", self.le_group_tags)
        #保存
        self.btn_save_group = QPushButton("保存群组信息")
        self.btn_save_group.clicked.connect(self.save_group_profile)
        #成员
        self.lw_group_members = QListWidget()
        self.lw_group_members.setAlternatingRowColors(True)
        self.lw_group_members.setWindowTitle("群组成员")
        #布局
        form_widget = QWidget()
        form_widget.setLayout(self.form_group)
        layout.addWidget(form_widget)
        layout.addWidget(self.btn_save_group)
        layout.addWidget(QLabel("群组成员:"))
        layout.addWidget(self.lw_group_members)

    def load_user(self):
        #id有效，尝试查找用户id，如果不存在就返回错误值
        try:
            user_id = int(self.le_user_id.text())
            if not self.logic.network.has_user(user_id):
                QMessageBox.warning(self, "错误", "用户不存在")
                return

            self.current_user_id = user_id
            user = self.logic.network.get_user(user_id)
            #更新用户信息
            self.le_name.setText(user.name)
            self.le_region.setText(user.region)
            self.le_schools.setText(",".join(user.school))
            self.le_workplaces.setText(",".join(user.workplace))
            self.le_hobbies.setText(",".join(user.hobbies))
            #刷新关系图
            graph_data = self.logic.get_social_graph(user_id)
            self.graph_widget.update_graph(graph_data)
            #刷新推荐
            self.refresh_potential_friends()
            self.refresh_recommended_groups()
        #用户id无效
        except ValueError:
            QMessageBox.warning(self, "错误", "请输入有效的用户ID")

    def refresh_potential_friends(self):
        if not self.current_user_id:
            QMessageBox.warning(self, "提示", "请先加载用户")
            return

        try:
            limit = int(self.le_limit_friends.text())
            sort_criteria = self.sort_criteria.currentText()

            # 根据选择的排序标准调用不同的排序方式
            if sort_criteria == "按相似度":
                potential = self.logic.get_potential_friends(self.current_user_id, limit, "similarity")
            elif sort_criteria == "按共同好友数":
                potential = self.logic.get_potential_friends(self.current_user_id, limit, "common_friends")
            elif sort_criteria == "按共同群组数":
                potential = self.logic.get_potential_friends(self.current_user_id, limit, "common_groups")
            else:
                potential = []

            self.display_potential_friends(potential, sort_criteria)

        except ValueError:
            QMessageBox.warning(self, "错误", "请输入有效的推荐数量")

    def display_potential_friends(self, potential, sort_criteria):
        self.lw_potential.clear()

        # 显示当前好友
        current_user = self.logic.network.get_user(self.current_user_id)
        if current_user.friends:
            separator = QListWidgetItem("--- 当前好友 ---")
            separator.setFlags(Qt.ItemIsEnabled)
            self.lw_potential.addItem(separator)

            for friend_id in current_user.friends:
                friend = self.logic.network.get_user(friend_id)
                if friend:
                    common_friends = len(current_user.friends & friend.friends)
                    item_text = f"ID:{friend_id} 姓名:{friend.name} 【当前好友】 共同好友:{common_friends}"
                    item = QListWidgetItem(item_text)
                    item.setForeground(QColor(0, 128, 0))
                    self.lw_potential.addItem(item)

        # 显示推荐好友
        if potential:
            separator = QListWidgetItem(f"--- 潜在好友推荐（按{sort_criteria}排序） ---")
            separator.setFlags(Qt.ItemIsEnabled)
            self.lw_potential.addItem(separator)

            for p in potential:
                item_text = (f"ID:{p['user_id']} 姓名:{p['name']} "
                             f"共同好友:{p['共同好友数量']} "
                             f"共同群组:{p['共同群组数量']} "
                             f"相似度:{p['similarity_score']}")
                item = QListWidgetItem(item_text)
                self.lw_potential.addItem(item)
        else:
            item = QListWidgetItem("暂无推荐好友")
            self.lw_potential.addItem(item)

    def refresh_recommended_groups(self):
        if not self.current_user_id:
            QMessageBox.warning(self, "提示", "请先加载用户")
            return
        try:
            limit = int(self.le_limit_groups.text())
            groups = self.logic.recommend_groups(self.current_user_id, limit)
            self.lw_groups.clear()
            #获取用户已加入的群组
            joined_groups = self.logic.get_joined_groups(self.current_user_id)
            if joined_groups:
                separator = QListWidgetItem("--- 已加入群组 ---")
                separator.setFlags(Qt.ItemIsEnabled)  # 不可选中
                self.lw_groups.addItem(separator)
                for g in joined_groups:
                    item_text = (f"ID:{g['group_id']} 名称:{g['name']} "
                                 f"主题:{g['topic']}")
                    item = QListWidgetItem(item_text)
                    item.setForeground(QColor(0, 0, 128))
                    self.lw_groups.addItem(item)

            separator = QListWidgetItem("--- 群组推荐 ---")
            separator.setFlags(Qt.ItemIsEnabled)  # 不可选中
            self.lw_groups.addItem(separator)
            if groups:
                for g in groups:
                    item_text = (f"ID:{g['group_id']} 名称:{g['name']} "
                                 f"主题:{g['topic']} 匹配度:{g['match_point']}")
                    item = QListWidgetItem(item_text)
                    self.lw_groups.addItem(item)
            else:
                item_text = "暂无推荐群组"
                item = QListWidgetItem(item_text)
                self.lw_groups.addItem(item)
        except ValueError:
            QMessageBox.warning(self, "错误", "请输入有效的推荐数量")

    def save_profile(self):
        """保存用户信息修改（保持原有功能）"""
        if not self.current_user_id:
            QMessageBox.warning(self, "提示", "请先加载用户")
            return

        user = self.logic.network.get_user(self.current_user_id)
        # 更新基本信息
        user.name = self.le_name.text()
        user.region = self.le_region.text()

        # 更新多值属性（先清空再添加）
        user.school.clear()
        for school in self.le_schools.text().split(','):
            if school.strip():
                user.add_school(school.strip())

        user.workplace.clear()
        for workplace in self.le_workplaces.text().split(','):
            if workplace.strip():
                user.add_workplace(workplace.strip())

        user.hobbies.clear()
        for hobby in self.le_hobbies.text().split(','):
            if hobby.strip():
                user.add_hobbies(hobby.strip())

        QMessageBox.information(self, "成功", "用户信息已更新")

    def add_user_dialog(self):
        name, ok = QInputDialog.getText(self, "新增用户", "请输入用户名:")
        if ok and name.strip():
            region, _ = QInputDialog.getText(self, "新增用户", "请输入地区:")
            user_id = self.logic.network.add_user(name.strip(), region.strip())
            QMessageBox.information(self, "成功", f"用户创建成功，ID:{user_id}")
            self.le_user_id.setText(str(user_id))

    def add_group_dialog(self):
        name, ok = QInputDialog.getText(self, "新增群组", "请输入群组名称:")
        if not (ok and name.strip()):
            return  # 取消或空名称则退出

        topic, _ = QInputDialog.getText(self, "新增群组", "请输入群组主题:")
        group_id = self.logic.network.add_group(name.strip(), topic.strip())

        tags, _ = QInputDialog.getText(self, "新增群组", "请输入群组标签(逗号分隔):")
        if tags.strip():
            group = self.logic.network.get_group(group_id)
            for tag in tags.split(','):
                if tag.strip():
                    group.tags.add(tag.strip())

        QMessageBox.information(self, "成功", f"群组创建成功，ID:{group_id}")
        self.le_group_id.setText(str(group_id))  # 自动填充到群组管理页

    def load_group(self):
        """加载指定ID的群组信息到群组管理标签页"""
        try:
            group_id = int(self.le_group_id.text())
            group = self.logic.network.get_group(group_id)
            if not group:
                QMessageBox.warning(self, "错误", "群组不存在")
                return

            # 填充群组信息表单
            self.le_group_name.setText(group.name)
            self.le_group_topic.setText(group.topic)
            self.le_group_tags.setText(",".join(group.tags))

            # 加载群组成员列表
            self.lw_group_members.clear()
            for member_id in group.members:
                member = self.logic.network.get_user(member_id)
                if member:
                    item_text = f"用户ID:{member_id} 姓名:{member.name}"
                    self.lw_group_members.addItem(item_text)

        except ValueError:
            QMessageBox.warning(self, "错误", "请输入有效的群组ID")

    def save_group_profile(self):
        """保存群组信息修改（名称、主题、标签）"""
        try:
            group_id = int(self.le_group_id.text())
            group = self.logic.network.get_group(group_id)
            if not group:
                QMessageBox.warning(self, "错误", "群组不存在")
                return

            # 更新基本信息
            group.name = self.le_group_name.text()
            group.topic = self.le_group_topic.text()

            # 更新标签（先清空再添加）
            group.tags.clear()
            for tag in self.le_group_tags.text().split(','):
                if tag.strip():
                    group.tags.add(tag.strip())

            QMessageBox.information(self, "成功", "群组信息已更新")
            self.load_group()  # 重新加载以刷新成员列表

        except ValueError:
            QMessageBox.warning(self, "错误", "请输入有效的群组ID")

    def delete_group(self):
        """删除指定ID的群组"""
        try:
            group_id = int(self.le_group_id.text())
            if not self.logic.network.has_group(group_id):
                QMessageBox.warning(self, "错误", "群组不存在")
                return

            # 二次确认
            reply = QMessageBox.question(
                self, "确认删除",
                f"确定要删除ID为{group_id}的群组吗？",
                QMessageBox.Yes | QMessageBox.No, QMessageBox.No
            )
            if reply == QMessageBox.Yes:
                success = self.logic.network.remove_group(group_id)
                if success:
                    QMessageBox.information(self, "成功", "群组已删除")
                    self.le_group_id.clear()
                    self.le_group_name.clear()
                    self.le_group_topic.clear()
                    self.le_group_tags.clear()
                    self.lw_group_members.clear()
                    # 刷新当前用户的关系图（如果有）
                    if self.current_user_id:
                        self.refresh_recommended_groups()
                        graph_data = self.logic.get_social_graph(self.current_user_id)
                        self.graph_widget.update_graph(graph_data)

        except ValueError:
            QMessageBox.warning(self, "错误", "请输入有效的群组ID")

    def join_selected_group(self):
        """加入选中的推荐群组"""
        if not self.current_user_id:
            QMessageBox.warning(self, "提示", "请先加载用户")
            return

        selected_items = self.lw_groups.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "提示", "请先选择一个群组")
            return

        # 从选中项中提取群组ID（格式：ID:1 名称:...）
        item_text = selected_items[0].text()
        try:
            group_id = int(item_text.split("ID:")[1].split()[0])
            success = self.logic.join_group(self.current_user_id, group_id)
            if success:
                QMessageBox.information(self, "成功", "已加入该群组")
                self.refresh_recommended_groups()  # 刷新推荐列表
                # 刷新关系图
                graph_data = self.logic.get_social_graph(self.current_user_id)
                self.graph_widget.update_graph(graph_data)
            else:
                QMessageBox.warning(self, "失败", "加入群组失败（群组不存在）")
        except (IndexError, ValueError):
            QMessageBox.warning(self, "错误", "无法识别群组ID")

    def leave_selected_group(self):
        """退出当前加载的群组（如果当前用户是该群组成员）"""
        if not self.current_user_id:
            QMessageBox.warning(self, "提示", "请先加载用户")
            return

        try:
            group_id = int(self.le_group_id.text())
            if not self.logic.network.has_group(group_id):
                QMessageBox.warning(self, "错误", "群组不存在")
                return

            # 检查用户是否是该群组成员
            user = self.logic.network.get_user(self.current_user_id)
            if group_id not in user.groups:
                QMessageBox.information(self, "提示", "您不是该群组成员")
                return

            # 二次确认
            reply = QMessageBox.question(
                self, "确认退出",
                f"确定要退出ID为{group_id}的群组吗？",
                QMessageBox.Yes | QMessageBox.No, QMessageBox.No
            )
            if reply == QMessageBox.Yes:
                success = self.logic.leave_group(self.current_user_id, group_id)
                if success:
                    QMessageBox.information(self, "成功", "已退出该群组")
                    # 刷新群组信息和关系图
                    self.load_group()  # 重新加载群组信息
                    self.refresh_recommended_groups()  # 刷新推荐列表
                    graph_data = self.logic.get_social_graph(self.current_user_id)
                    self.graph_widget.update_graph(graph_data)
                else:
                    QMessageBox.warning(self, "失败", "退出群组失败")
        except ValueError:
            QMessageBox.warning(self, "错误", "请输入有效的群组ID")

    def remove_selected_friend(self):
        """删除选中的好友"""
        if not self.current_user_id:
            QMessageBox.warning(self, "提示", "请先加载用户")
            return

        selected_items = self.lw_potential.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "提示", "请先选择一个好友")
            return

        # 从选中项中提取用户ID（格式：ID:1 姓名:...）
        item_text = selected_items[0].text()
        try:
            friend_id = int(item_text.split("ID:")[1].split()[0])
            current_user = self.logic.network.get_user(self.current_user_id)

            # 检查是否是当前好友
            if friend_id not in current_user.friends:
                QMessageBox.warning(self, "错误", "该用户不是您的好友")
                return

            # 二次确认
            friend = self.logic.network.get_user(friend_id)
            reply = QMessageBox.question(
                self, "确认删除",
                f"确定要删除好友 {friend.name}（ID:{friend_id}）吗？",
                QMessageBox.Yes | QMessageBox.No, QMessageBox.No
            )
            if reply == QMessageBox.Yes:
                success = self.logic.remove_friend_relationship(self.current_user_id, friend_id)
                if success:
                    QMessageBox.information(self, "成功", "已删除该好友")
                    self.refresh_potential_friends()  # 刷新好友列表
                    # 刷新关系图
                    graph_data = self.logic.get_social_graph(self.current_user_id)
                    self.graph_widget.update_graph(graph_data)
                else:
                    QMessageBox.warning(self, "失败", "删除好友失败")
        except (IndexError, ValueError):
            QMessageBox.warning(self, "错误", "无法识别用户ID")

    def add_selected_friend(self):
        """添加选中的潜在好友"""
        if not self.current_user_id:
            QMessageBox.warning(self, "提示", "请先加载用户")
            return

        selected_items = self.lw_potential.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "提示", "请先选择一个用户")
            return

        # 从选中项中提取用户ID（格式：ID:1 姓名:...）
        item_text = selected_items[0].text()
        try:
            friend_id = int(item_text.split("ID:")[1].split()[0])
            current_user = self.logic.network.get_user(self.current_user_id)

            # 检查是否是自己或已为好友
            if friend_id == self.current_user_id:
                QMessageBox.warning(self, "错误", "不能添加自己为好友")
                return
            if friend_id in current_user.friends:
                QMessageBox.information(self, "提示", "已是好友")
                return

            # 执行添加
            success, msg = self.logic.add_friend(self.current_user_id, friend_id)
            if success:
                QMessageBox.information(self, "成功", msg)
                self.refresh_potential_friends()  # 刷新列表
                # 刷新关系图
                graph_data = self.logic.get_social_graph(self.current_user_id)
                self.graph_widget.update_graph(graph_data)
            else:
                QMessageBox.warning(self, "失败", msg)
        except (IndexError, ValueError):
            QMessageBox.warning(self, "错误", "无法识别用户ID")

    def join_selected_group_from_all(self):
        """从所有群组列表中加入选中的群组"""
        if not self.current_user_id:
            QMessageBox.warning(self, "提示", "请先加载用户")
            return

        selected_items = self.lw_all_groups.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "提示", "请先选择一个群组")
            return

        # 从选中项中提取群组ID（格式：群组ID: 1 | 名称:...）
        item_text = selected_items[0].text()
        try:
            group_id = int(item_text.split("群组ID:")[1].split("|")[0].strip())
            user = self.logic.network.get_user(self.current_user_id)

            # 检查是否已加入
            if group_id in user.groups:
                QMessageBox.information(self, "提示", "您已加入该群组")
                return

            # 执行加入
            success = self.logic.join_group(self.current_user_id, group_id)
            if success:
                QMessageBox.information(self, "成功", "已加入该群组")
                self.refresh_all_groups()  # 刷新所有群组列表
                self.refresh_recommended_groups()  # 刷新推荐列表
                # 刷新关系图
                graph_data = self.logic.get_social_graph(self.current_user_id)
                self.graph_widget.update_graph(graph_data)
            else:
                QMessageBox.warning(self, "失败", "加入群组失败（群组不存在）")
        except (IndexError, ValueError):
            QMessageBox.warning(self, "错误", "无法识别群组ID")

    def delete_user(self):
        """删除当前输入ID的用户"""
        try:
            user_id = int(self.le_user_id.text())
            if not self.logic.network.has_user(user_id):
                QMessageBox.warning(self, "错误", "用户不存在")
                return

            # 二次确认
            reply = QMessageBox.question(
                self, "确认删除",
                f"确定要删除ID为{user_id}的用户吗？\n相关好友关系和群组关联也会一并删除",
                QMessageBox.Yes | QMessageBox.No, QMessageBox.No
            )
            if reply == QMessageBox.Yes:
                # 检查是否是当前正在操作的用户
                if self.current_user_id == user_id:
                    self.current_user_id = None  # 清除当前用户

                success = self.logic.network.remove_user(user_id)
                if success:
                    QMessageBox.information(self, "成功", "用户已删除")
                    self.le_user_id.clear()
                    # 清空用户信息表单
                    self.le_name.clear()
                    self.le_region.clear()
                    self.le_schools.clear()
                    self.le_workplaces.clear()
                    self.le_hobbies.clear()
                    # 刷新所有相关列表和视图
                    self.refresh_potential_friends()
                    self.refresh_recommended_groups()
                    self.refresh_all_users()
                    self.graph_widget.update_graph({"nodes": [], "edges": []})
        except ValueError:
            QMessageBox.warning(self, "错误", "请输入有效的用户ID")

    def init_test_data(self):
        """初始化更大的测试数据集"""
        # 创建更多测试用户 (20个用户)
        user_ids = []
        for i in range(20):
            regions = ["上海", "北京", "广州", "深圳", "杭州", "南京", "武汉", "成都", "西安", "重庆"]
            names = ["小张", "小李", "小王", "小赵", "小钱", "小孙", "小周", "小吴",
                     "小郑", "小明", "小陈", "小林", "小黄", "小秦", "小彭",
                     "小亮", "小徐", "小陆", "小裴", "小吴"]

            user_id = self.logic.network.add_user(
                names[i],
                regions[i % len(regions)],
                is_student=(i % 4 != 0)  # 每4个用户中3个是学生
            )
            user_ids.append(user_id)

        # 设置用户属性
        schools = ["同济大学", "北京大学", "清华大学", "复旦大学", "上海交通大学",
                   "浙江大学", "南京大学", "武汉大学", "华中科技大学", "西安交通大学"]
        workplaces = ["腾讯", "阿里巴巴", "百度", "华为", "字节跳动", "美团", "京东", "小米", "网易", "拼多多"]
        hobbies = ["编程", "篮球", "音乐", "阅读", "电影", "游戏", "旅游", "摄影", "烹饪", "健身"]

        for i, uid in enumerate(user_ids):
            user = self.logic.network.get_user(uid)

            # 添加学校 (每个用户1-2所学校)
            school_count = random.randint(1, 2)
            for _ in range(school_count):
                school = random.choice(schools)
                user.add_school(school)

            # 添加工作单位 (非学生用户)
            if not user.is_student:
                workplace_count = random.randint(1, 2)
                for _ in range(workplace_count):
                    workplace = random.choice(workplaces)
                    user.add_workplace(workplace)

            # 添加爱好 (每个用户2-4个爱好)
            hobby_count = random.randint(2, 4)
            for _ in range(hobby_count):
                hobby = random.choice(hobbies)
                user.add_hobbies(hobby)

        # 创建更多测试群组 (8个群组)
        group_ids = []
        group_names = ["编程爱好者", "篮球俱乐部", "音乐交流", "读书会", "电影迷",
                       "游戏战队", "旅游达人", "摄影协会", "美食家", "健身小组"]
        group_topics = ["讨论编程技术", "组织篮球活动", "分享音乐作品", "交流读书心得",
                        "讨论电影剧情", "组队玩游戏", "分享旅行经验", "交流摄影技巧",
                        "分享美食食谱", "交流健身经验"]
        group_tags = [
            {"编程", "技术"},
            {"篮球", "运动"},
            {"音乐", "艺术"},
            {"阅读", "学习"},
            {"电影", "娱乐"},
            {"游戏", "娱乐"},
            {"旅游", "户外"},
            {"摄影", "艺术"},
            {"美食", "烹饪"},
            {"健身", "健康"}
        ]

        for i in range(8):
            group_id = self.logic.network.add_group(
                group_names[i],
                group_topics[i]
            )
            group = self.logic.network.get_group(group_id)
            group.tags = group_tags[i]
            group_ids.append(group_id)

        # 建立更复杂的好友关系网络
        # 确保每个用户至少有2个好友，最多有5个好友
        for uid in user_ids:
            user = self.logic.network.get_user(uid)
            friend_count = random.randint(2, 5)

            # 排除自己
            potential_friends = [fid for fid in user_ids if fid != uid and fid not in user.friends]

            # 如果潜在好友数量不足，跳过
            if len(potential_friends) < friend_count:
                continue

            # 随机选择好友
            selected_friends = random.sample(potential_friends, friend_count)
            for friend_id in selected_friends:
                self.logic.add_friend_relationship(uid, friend_id)

        # 确保每个群组至少有3个成员，最多有8个成员
        for gid in group_ids:
            group = self.logic.network.get_group(gid)
            member_count = random.randint(3, 8)

            # 随机选择成员
            selected_members = random.sample(user_ids, min(member_count, len(user_ids)))
            for member_id in selected_members:
                self.logic.join_group(member_id, gid)

        # 确保每个用户至少加入1个群组，最多加入3个群组
        for uid in user_ids:
            user = self.logic.network.get_user(uid)
            group_count = random.randint(1, 3)

            # 排除已加入的群组
            potential_groups = [gid for gid in group_ids if gid not in user.groups]

            # 如果潜在群组数量不足，跳过
            if len(potential_groups) < group_count:
                continue

            # 随机选择群组
            selected_groups = random.sample(potential_groups, group_count)
            for group_id in selected_groups:
                self.logic.join_group(uid, group_id)

        # 默认显示第一个用户
        self.le_user_id.setText(str(user_ids[0]))
        self.load_user()  # 自动加载第一个用户

    def search_friends(self):
        """搜索好友（按ID或姓名）"""
        if not self.current_user_id:
            QMessageBox.warning(self, "提示", "请先加载用户")
            return

        search_text = self.le_search_friend.text().strip()
        if not search_text:
            QMessageBox.warning(self, "提示", "请输入搜索内容")
            return

        all_users = self.logic.network.get_all_users()
        results = []

        # 尝试按ID搜索
        try:
            user_id = int(search_text)
            user = self.logic.network.get_user(user_id)
            if user:
                results.append(user)
        except ValueError:
            # 按姓名搜索（模糊匹配）
            results = [user for user in all_users if search_text in user.name]

        # 显示搜索结果
        self.lw_potential.clear()
        if not results:
            self.lw_potential.addItem("没有找到匹配的用户")
            return

        # 区分当前好友和其他用户
        current_user = self.logic.network.get_user(self.current_user_id)
        friends = current_user.friends

        # 显示搜索结果
        separator = QListWidgetItem("--- 搜索结果 ---")
        separator.setFlags(Qt.ItemIsEnabled)
        self.lw_potential.addItem(separator)

        for user in results:
            if user.user_id == self.current_user_id:
                item_text = f"ID:{user.user_id} 姓名:{user.name} 【自己】"
                item = QListWidgetItem(item_text)
                item.setForeground(QColor(128, 128, 128))
            elif user.user_id in friends:
                item_text = f"ID:{user.user_id} 姓名:{user.name} 【当前好友】"
                item = QListWidgetItem(item_text)
                item.setForeground(QColor(0, 128, 0))
            else:
                # 计算相似度
                sim_score = self.logic.calculate_similarity(self.current_user_id, user.user_id)
                common_friends = len(current_user.friends & self.logic.network.get_user(user.user_id).friends)
                common_groups = len(current_user.groups & self.logic.network.get_user(user.user_id).groups)
                item_text = (f"ID:{user.user_id} 姓名:{user.name} "
                             f"相似度:{sim_score} "
                             f"共同好友:{common_friends} "
                             f"共同群组:{common_groups}")
                item = QListWidgetItem(item_text)

            self.lw_potential.addItem(item)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())