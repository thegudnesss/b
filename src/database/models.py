from typing import Optional
from pydantic import BaseModel


class User(BaseModel):
    _id: int
    xp: int = 0
    language: str = "en"
    shop_id: Optional[int] = None


class Shop(BaseModel):
    _id: int
    owner_id: int
    title: str
    description: Optional[str] = None


class XPLog(BaseModel):
    _id: str
    user_id: int
    amount: int
    reason: str


class Referral(BaseModel):
    _id: str
    inviter_id: int
    invitee_id: int
