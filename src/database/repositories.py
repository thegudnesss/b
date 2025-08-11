from src.database.base import BaseRepository, mongo
from src.database.models import User, Shop, XPLog, Referral


class UserRepo(BaseRepository[User]):
    collection_name = "users"
    model = User


class ShopRepo(BaseRepository[Shop]):
    collection_name = "shops"
    model = Shop


class XPLogRepo(BaseRepository[XPLog]):
    collection_name = "xp_logs"
    model = XPLog


class ReferralRepo(BaseRepository[Referral]):
    collection_name = "referrals"
    model = Referral


# Global repository obyektlar
user_repo = UserRepo(mongo)
shop_repo = ShopRepo(mongo)
xp_log_repo = XPLogRepo(mongo)
referral_repo = ReferralRepo(mongo)
