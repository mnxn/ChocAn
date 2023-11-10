from abc import ABC, abstractmethod
from . import report


class User(ABC):
    name: str

    def __init__(self, name: str) -> None:
        self.name = name

    @abstractmethod
    def receive_report(self, report: report.Report) -> None:
        pass


class UserAccount(User):
    id: int
    address: str
    city: str
    state: str
    zip_code: int

    def __init__(
        self, name: str, id: int, address: str, city: str, state: str, zip_code: int
    ) -> None:
        super().__init__(name)

        if len(str(id)) != 9:
            raise ValueError("id must be 9 digits long")
        if len(address) > 25:
            raise ValueError("address cannot have more than 25 characters")
        if len(city) > 14:
            raise ValueError("city cannot have more than 14 characters")
        if len(state) != 2:
            raise ValueError("state must be 2 characters long")
        if len(str(zip_code)) != 5:
            raise ValueError("zip_code must be 5 digits long")

        self.id = id
        self.address = address
        self.city = city
        self.state = state
        self.zip_code = zip_code


class Manager(User):
    def __init__(self, name: str) -> None:
        super().__init__(name)

    def receive_report(self, report: report.Report) -> None:
        pass


class Member(UserAccount):
    suspended: bool

    def __init__(
        self,
        name: str,
        id: int,
        address: str,
        city: str,
        state: str,
        zip_code: int,
        suspended: bool,
    ) -> None:
        super().__init__(name, id, address, city, state, zip_code)
        self.suspended = suspended

    def receive_report(self, report: report.Report) -> None:
        pass


class Provider(UserAccount):
    def __init__(
        self, name: str, id: int, address: str, city: str, state: str, zip_code: int
    ) -> None:
        super().__init__(name, id, address, city, state, zip_code)

    def receive_report(self, report: report.Report) -> None:
        pass
