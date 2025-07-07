from pydantic import BaseModel
from typing import List, Optional

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

class User(BaseModel):
    id: int
    name: str
    email: str
    roles: Optional[List[int]]

class ResponseLoginCredentials(BaseModel):
    credentials: Token
    user: User

class TokenData(BaseModel):
    id: int 
    email: str | None = None