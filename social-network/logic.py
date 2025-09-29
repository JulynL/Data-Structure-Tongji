from data_structures import *

class SocialNetworkLogic:
    def __init__(self):
        self.network = SocialNetwork()

    '''
    相似度计算，用于获取和其他用户的相似度分数来进行潜在好友的推荐
    '''
    def calculate_similarity(self, user_id, candidate_id):
        #用户相似度用于好友推荐
        user = self.network.get_user(user_id)
        candidate = self.network.get_user(candidate_id)
        if not user or not candidate:
            return 0
        similarity_score = 0
        #共同好友（30%）共同群组（20%）共同学校（15%）共同单位（15%）相同地区（5%）共同爱好（15%）
        common_friends = len(user.friends & candidate.friends)
        similarity_score += min(5 * common_friends,30)
        common_groups = len(user.groups & candidate.groups)
        similarity_score += min(5 * common_groups,20)
        common_schools = len(user.school & candidate.school)
        similarity_score += min(5 * common_schools,15)
        common_workplaces = len(user.workplace & candidate.workplace)
        similarity_score += min(7.5 * common_workplaces,15)
        if user.region == candidate.region and user.region != "":
            similarity_score += 5
        common_hobbies = len(user.hobbies & candidate.hobbies)
        similarity_score += min(5 * common_hobbies,15)

        return round(similarity_score, 2)

    '''
    获取好友推荐列表
    '''
    def get_potential_friends(self, user_id, limit=10, sort_by="similarity"):
        target_user = self.network.users.get(user_id)
        if not target_user:
            return []

        candidates = set()
        for anyone in target_user.friends:
            friend = self.network.get_user(anyone)
            if friend:
                candidates.update(friend.friends)
        for anygroup in target_user.groups:
            group = self.network.get_group(anygroup)
            if group:
                candidates.update(group.members)
        candidates = [candidate for candidate in candidates if
                      candidate != user_id and candidate not in target_user.friends and self.network.has_user(
                          candidate)]

        new_friends = []
        for candidate in candidates:
            friend = self.network.get_user(candidate)
            common_friends = len(target_user.friends & friend.friends)
            common_groups = len(target_user.groups & friend.groups)
            sim_score = self.calculate_similarity(user_id, candidate)

            new_friends.append({
                "user_id": candidate,
                "name": friend.name,
                "共同好友数量": common_friends,
                "共同群组数量": common_groups,
                "similarity_score": sim_score
            })

        # 根据不同的排序标准进行排序
        if sort_by == "common_friends":
            return sorted(new_friends, key=lambda x: x["共同好友数量"], reverse=True)[:limit]
        elif sort_by == "common_groups":
            return sorted(new_friends, key=lambda x: x["共同群组数量"], reverse=True)[:limit]
        else:  # 默认按相似度排序
            return sorted(new_friends, key=lambda x: x["similarity_score"], reverse=True)[:limit]

    '''
    获取潜在群组推荐列表
    '''
    def recommend_groups(self, user_id, limit=5):
        target_user = self.network.users.get(user_id)
        if not target_user:
            return []
        if not target_user.hobbies:
            return []
        all_groups = self.network.get_all_groups()
        unjoined_groups = [group for group in all_groups if group.group_id not in target_user.groups]
        recommended_groups = []
        for group in unjoined_groups:
            match_point = 0
            match_point = len(target_user.hobbies & group.tags) * 5 + 5 * len(target_user.school & group.tags) + 5 * len(target_user.workplace & group.tags)
            if match_point > 0:
                recommended_groups.append({"group_id":group.group_id, "name":group.name, "topic":group.topic, "tag":group.tags, "match_point":match_point})
        return sorted(recommended_groups,key=lambda x: x["match_point"], reverse=True)[:limit]

    '''
    构建用户社交网络图
    '''
    def get_social_graph(self, user_id):
        if not self.network.has_user(user_id):
            return {"nodes":[], "edges":[]}
        user = self.network.get_user(user_id)
        nodes = []
        nodes.append({"id": f"user{user_id}", "name": user.name, "type": "self"})
        edges = []
        for anyone in user.friends:
            friend = self.network.get_user(anyone)
            if friend:
                nodes.append({"id": f"user{friend.user_id}", "name": friend.name, "type": "friend"})
                edges.append({"source": f"user{user_id}", "target": f"user{friend.user_id}"})

        for anygroup in user.groups:
            group = self.network.get_group(anygroup)
            if group:
                nodes.append({"id": f"group{group.group_id}", "name": group.name, "type": "group"})
                edges.append({"source": f"user{user_id}", "target": f"group{group.group_id}"})

        return {"nodes":nodes, "edges":edges}

    '''
    添加好友，这个只用于初始化
    '''
    def add_friend_relationship(self, user_id1, user_id2):
        if (not self.network.has_user(user_id1) or
                not self.network.has_user(user_id2) or
                user_id1 == user_id2):
            return False
        user1 = self.network.get_user(user_id1)
        user2 = self.network.get_user(user_id2)
        user1.add_friend(user_id2)
        user2.add_friend(user_id1)
        return True

    '''
    添加好友
    '''
    def add_friend(self, user_id, friend_id):
        if (not self.network.has_user(user_id) or
                not self.network.has_user(friend_id) or
                user_id == friend_id):
            return False, "用户不存在或不能添加自己为好友"
        user = self.network.get_user(user_id)
        friend = self.network.get_user(friend_id)
        if friend_id in user.friends:
            return False, "已是好友"
        user.add_friend(friend_id)
        friend.add_friend(user_id)
        return True, "添加成功"

    '''
    删除好友
    '''
    def remove_friend_relationship(self, user_id1, user_id2):
        if (not self.network.has_user(user_id1) or
                not self.network.has_user(user_id2) or
                user_id1 == user_id2):
            return False
        user1 = self.network.get_user(user_id1)
        user2 = self.network.get_user(user_id2)
        if user_id2 in user1.friends and user_id1 in user2.friends:
            user1.remove_friend(user_id2)
            user2.remove_friend(user_id1)
            return True
        return False

    '''
    加入群组
    '''
    def join_group(self, user_id, group_id):
        if (not self.network.has_user(user_id) or
                not self.network.has_group(group_id)):
            return False
        user = self.network.get_user(user_id)
        group = self.network.get_group(group_id)
        user.groups.add(group_id)
        group.add_member(user_id)
        return True

    '''
    退出群组
    '''
    def leave_group(self, user_id, group_id):
        if (not self.network.has_user(user_id) or
                not self.network.has_group(group_id)):
            return False
        user = self.network.get_user(user_id)
        group = self.network.get_group(group_id)
        if group_id in user.groups:
            user.groups.remove(group_id)
        if user_id in group.members:
            group.members.remove(user_id)
        return True

    '''
    获取已加入的群组
    '''
    def get_joined_groups(self, user_id):
        user = self.network.get_user(user_id)
        if not user:
            return []
        joined_groups = []
        for group_id in user.groups:
            group = self.network.get_group(group_id)
            if group:  # 确保群组仍存在
                joined_groups.append({
                    "group_id": group.group_id,
                    "name": group.name,
                    "topic": group.topic,
                    "tags": group.tags,
                    "member_count": len(group.members)
                })
        return sorted(joined_groups, key=lambda x: x["group_id"])

