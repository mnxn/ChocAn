from abc import ABC, abstractmethod
import report


class User(ABC):
    name: str

    def __init__(self, name: str) -> None:
        pass

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
        self, name: str, id: int, address: str, city: str, state: str, zip_code: str
    ) -> None:
        pass


class Manager(User):
    def __init__(self, name: str) -> None:
        pass

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
        zip_code: str,
        suspended: bool,
    ) -> None:
        pass

    def receive_report(self, report: report.Report) -> None:
        pass


class Provider(UserAccount):
    def __init__(
        self, name: str, id: int, address: str, city: str, state: str, zip_code: str
    ) -> None:
        pass

    def receive_report(self, report: report.Report) -> None:
        pass
