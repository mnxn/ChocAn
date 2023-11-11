from . import user
from . import service
from . import reports


class System:
    path: str
    member_list: list[user.Member]
    provider_list: list[user.Provider]
    manager_list: list[user.Manager]
    service_list: list[service.Service]
    record_list: list[service.Record]

    def __init__(self, path: str) -> None:
        pass

    def load_files(self) -> None:
        pass

    def write_files(self) -> None:
        pass

    def add_member(self, new_member: user.Member) -> None:
        pass

    def remove_member(self, id: int) -> None:
        pass

    def suspend_member(self, id: int) -> None:
        pass

    def lookup_member(self, id: int) -> user.Member:
        pass

    def add_provider(self, new_provider: user.Provider) -> None:
        pass

    def remove_provider(self, id: int) -> None:
        pass

    def lookup_provider(self, id: int) -> user.Provider:
        pass

    def lookup_manager(self, id: int) -> user.Manager:
        pass

    def lookup_service(self, code: int) -> service.Service:
        pass

    def record_service(self, service_record: service.Record) -> None:
        pass

    def issue_member_report(self, member: user.Member) -> None:
        pass

    def issue_provider_report(self, provider: user.Provider) -> None:
        pass

    def issue_provider_directory(self, provider: user.Provider) -> None:
        pass

    def issue_summary_report(self, manager: user.Manager) -> None:
        pass

    def write_eft_data(self, record: service.Record) -> None:
        pass

    def weekly_actions(self) -> None:
        pass
