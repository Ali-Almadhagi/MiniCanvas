class UserManager:
    def __init__(self):
        self.user_list = []
        self.counter = 0

    def generate_id(self):
        self.counter += 1
        return self.counter
    
    def create_a_user(self, name, password, type):
        new_user_id = self.generate_id()
        new_user = User(new_user_id, name, password, type)
        self.user_list.append(new_user)

    def find_users(self, ids):
        users_found = []
        for user in self.user_list:
            if user.user_id in ids:
                users_found.append(user)
        
        return users_found

class User():
    def __init__(self, user_id: int, name: str, password: str, type: str):
        self.user_id = user_id
        self.name = name
        self.password = password
        self.type = type # type should be either student/teacher/admin
    
    def __str__(self):
        return f"ID: {self.user_id}, name: {self.name}, type: {self.type}"
    