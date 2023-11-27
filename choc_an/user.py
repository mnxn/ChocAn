import os
from abc import ABC, abstractmethod
from datetime import datetime
from . import report


class User(ABC):
    name: str

    @abstractmethod
    def __init__(self, name: str) -> None:
        self.name = name

    def receive_report(self, report: report.Report) -> None:
        try:
            filename = f"{self.name}_{datetime.now().strftime('%Y-%m-%d')}.txt"
            os.makedirs("reports", exist_ok=True)
            with open(os.path.join("reports", filename), "w") as file:
                file.write(report.output())
            print(f"Report saved to {os.path.join('reports', filename)}")
        except Exception as error:
            print("fail to write report")
            raise


class UserAccount(User):
    id: int
    address: str
    city: str
    state: str
    zip_code: int

    @abstractmethod
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


class Provider(UserAccount):
    def __init__(
        self, name: str, id: int, address: str, city: str, state: str, zip_code: int
    ) -> None:
        super().__init__(name, id, address, city, state, zip_code)
