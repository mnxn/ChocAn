from decimal import Decimal
from datetime import datetime
from choc_an import user


class Service:
    name: str
    code: int
    fee: Decimal

    def __init__(self, name: str, code: int, fee: Decimal) -> None:
        if len(name) > 30:
            raise ValueError("name cannot have more than 30 characters")
        if len(str(code)) != 6:
            raise ValueError("code must be 6 digits long")
        if fee > Decimal("999.99"):
            raise ValueError("fee cannot be more than $999.99")

        self.name = name
        self.code = code
        self.fee = fee


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
        if len(comments) > 100:
            raise ValueError("comments cannot have more than 100 characters")

        self.current_date_time = datetime.now()
        self.service_date_time = service_date_time
        self.provider = provider
        self.member = member
        self.service = service
        self.comments = comments
