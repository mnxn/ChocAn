from decimal import Decimal
from datetime import datetime
from . import user


class Service:
    name: str
    code: int
    fee: Decimal

    def __init__(self, name: str, code: int, fee: Decimal) -> None:
        pass


class Record:
    current_date_time: datetime
    service_date_time: datetime
    provider: user.Provider
    member: user.Member
    service: Service
    comments: str

    def __init__(
        self,
        service_date_time: datetime,
        provider: user.Provider,
        member: user.Member,
        service: Service,
        comments: str,
    ) -> None:
        pass
