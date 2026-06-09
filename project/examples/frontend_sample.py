class UserService:
    def login(self, token):
        user = self.validate(token)
        if user:
            self.cache[token] = user
        return user

    def validate(self, token):
        return token == "secret"