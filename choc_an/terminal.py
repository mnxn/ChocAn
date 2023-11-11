from . import system
from . import user


class ProviderTerminal:
    current_system: system.System
    current_provider: user.Provider | None
    current_member: user.Member | None

    def __init__(self, system: system.System) -> None:
        self.current_system = system
        self.current_provider = None
        self.current_member = None

    def login_provider(self) -> None:
        pass

    def logout_provider(self) -> None:
        pass

    def login_member(self) -> None:
        pass

    def logout_member(self) -> None:
        pass

    def request_provider_directory(self) -> None:
        pass

    def validate_service_code(self) -> None:
        pass

    def bill(self) -> None:
        pass


class ManagerTerminal(ProviderTerminal):
    current_manager: user.Manager | None

    def __init__(self, system: system.System) -> None:
        super().__init__(system)
        self.current_manager = None

    def login_manager(self) -> None:
        pass

    def logout_manager(self) -> None:
        pass

    def request_member_report(self) -> None:
        pass

    def request_provider_report(self) -> None:
        pass

    def request_summary_report(self) -> None:
        pass
