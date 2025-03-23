from fastapi import HTTPException, status
from app.modules.users.helpers import register_user_helper, login_user_helper, get_support_members_helper

class UserController:
    @staticmethod
    def register_user(user_data, db):
        try:
            if not user_data.role_id:
                raise HTTPException(status_code=400, detail="User role is required")
            created_user = register_user_helper(user_data, db)
            return created_user
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    @staticmethod
    def login_user(username: str, password: str, db):
        try:
            token_data = login_user_helper(username, password, db)
            return token_data
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))

    @staticmethod
    def get_me(current_user):
        try:
            return current_user
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
    @staticmethod
    def get_support_members(db, current_user):
        try:
            if current_user.role_id != 3:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Not authorized to view support members."
                )
            return get_support_members_helper(db)
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
