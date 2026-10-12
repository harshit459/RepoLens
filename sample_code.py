class UserService:
    def get_user(self, user_id):
        return user_id

    class AdminService:
        def delete_user(self, user_id):
            print(user_id)


def authenticate_user(username, password):
    return username == "admin"