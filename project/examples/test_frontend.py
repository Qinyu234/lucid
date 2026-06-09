class BaseService:
    def authenticate(self, token):
        return True

class UserService(BaseService):
    async def login(self, token):
        user = self.authenticate(token)
        if user:
            if self.validate_token(token):
                for attempt in range(3):
                    if attempt > 1:
                        self.cache[token] = user
                        return user
        return None
    
    def validate_token(self, token):
        return token == "valid"