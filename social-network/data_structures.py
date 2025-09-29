class User:
    def __init__(self, user_id, name, region, is_student=True):
        self.user_id = user_id
        self.is_student = is_student
        self.name = name
        self.region = region
        self.school = set()
        self.workplace = set()
        self.hobbies = set()
        self.friends = set()
        self.groups = set()

    def add_friend(self, friend_id):
            self.friends.add(friend_id)

    def add_school(self,school):
        self.school.add(school)

    def add_workplace(self,workplace):
        self.workplace.add(workplace)

    def add_hobbies(self,hobbies):
        self.hobbies.add(hobbies)

    def add_group(self,group):
        self.groups.add(group)

    def remove_friend(self, friend_id):
        self.friends.remove(friend_id)

    def remove_school(self,school):
        self.school.remove(school)

    def remove_workplace(self,workplace):
        self.workplace.remove(workplace)

    def remove_hobbies(self,hobbies):
        self.hobbies.remove(hobbies)

    def remove_group(self,group):
        self.groups.remove(group)

class Group:
    def __init__(self, group_id, name, topic=""):
        self.group_id = group_id
        self.name = name
        self.topic = topic
        self.tags = set()
        self.members = set()

    def add_member(self, user_id):
        self.members.add(user_id)

    def remove_member(self,user_id):
        self.members.remove(user_id)

class SocialNetwork:
    def __init__(self):
        self.users = {}
        self.groups = {}
        self.user_id_counter = 1
        self.group_id_counter = 1
        self.recycled_user_ids = set()  # 存储已删除的用户ID
        self.recycled_group_ids = set()  # 存储已删除的群组ID

    def add_user(self, name, region="", is_student=True):
        # 优先使用回收的用户ID
        if self.recycled_user_ids:
            user_id = self.recycled_user_ids.pop()
        else:
            user_id = self.user_id_counter
            self.user_id_counter += 1
        self.users[user_id] = User(user_id, name, region, is_student)
        return user_id

    def add_group(self, name, topic=""):
        # 优先使用回收的群组ID
        if self.recycled_group_ids:
            group_id = self.recycled_group_ids.pop()
        else:
            group_id = self.group_id_counter
            self.group_id_counter += 1
        self.groups[group_id] = Group(group_id, name, topic)
        return group_id

    def remove_user(self, user_id):
        if user_id not in self.users:
            return False
        user = self.users[user_id]
        for friend_id in list(user.friends):
            friend = self.get_user(friend_id)
            if friend:
                friend.remove_friend(user_id)
        for group in self.groups.values():
            if user_id in group.members:
                group.remove_member(user_id)
        del self.users[user_id]
        self.recycled_user_ids.add(user_id)
        self.recycled_user_ids = set(sorted(self.recycled_user_ids))
        return True

    def remove_group(self, group_id):
        if group_id not in self.groups:
            return False
        for user in self.users.values():
            if group_id in user.groups:
                user.remove_group(group_id)
        del self.groups[group_id]
        self.recycled_group_ids.add(group_id)
        self.recycled_group_ids = set(sorted(self.recycled_group_ids))
        return True

    def get_user(self, user_id):
        return self.users.get(user_id)

    def get_group(self, group_id):
        return self.groups.get(group_id)

    def get_all_users(self):
        return list(self.users.values())

    def get_all_groups(self):
        return list(self.groups.values())

    def has_user(self, user_id):
        return user_id in self.users

    def has_group(self, group_id):
        return group_id in self.groups

    def get_user_count(self):
        return len(self.users)

    def get_group_count(self):
        return len(self.groups)
