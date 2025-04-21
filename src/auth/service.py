from sqlalchemy.ext.asyncio.session import AsyncSession
from src.auth.schemas import UserRegister
from src.auth.models import User
from typing import Optional
from sqlmodel import select, or_
from src.auth.utils import generate_password_hash, verify_passwd

class AuthService:

    async def register_user(self, user_data: UserRegister, session: AsyncSession):
        # import ipdb; ipdb.set_trace()
        user_data_dict = user_data.model_dump()
        
        user_data_dict["email"] = user_data_dict["email"].lower()
        user_data_dict["password"] = generate_password_hash(user_data_dict["password"])
        
        new_user = User(**user_data_dict)
        session.add(new_user)
        await session.commit()
        return new_user
    
    async def user_exists(self, email:str, session: AsyncSession):
        statement = select(User).where(User.email == email)
        result = await session.exec(statement)
        user = result.first()

        return True if user else False
        

    async def get_user(self, user_id: Optional[str], email: Optional[str], session: AsyncSession):
        if not user_id and not email:
            return None
        
        conditions = []
        if user_id:
            conditions.append(User.id == user_id)
        if email:
            conditions.append(User.email == email)

        statement = select(User).where(or_(*conditions))    
        result = await session.exec(statement)
        return result.first()
    
    async def login_user(self, email: str, password: str, session: AsyncSession):
        statement = select(User).where(User.email == email)
        result = await session.exec(statement)
        user = result.first()

        if not user:
            return None
    
        if not verify_passwd(password, user.password):
            return None
        
        return user


auth_service = AuthService()
    

