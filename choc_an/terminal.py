from datetime import datetime
from . import user
from . import system
from .service import Record


class ProviderTerminal:
    current_system: system.System
    current_provider: user.Provider | None
    current_member: user.Member | None

    def __init__(self, system: system.System) -> None:
        self.current_system = system
        self.current_provider = None
        self.current_member = None

    def run_command_menu(self) -> bool:
        print("Commands:")
        print("\t(1) Provider Login")
        print("\t(2) Provider Logout")
        print("\t(3) Member Login")
        print("\t(4) Member Logout")
        print("\t(5) Request Provider Directory")
        print("\t(6) Validate Service Code")
        print("\t(7) Bill")
        print()
        print("\t(8) Exit")
        choice = input("Enter Command (1-8): ")
        print()

        if choice == "1":
            self.login_provider()
        elif choice == "2":
            self.logout_provider()
        elif choice == "3":
            self.login_member()
        elif choice == "4":
            self.logout_member()
        elif choice == "5":
            self.request_provider_directory()
        elif choice == "6":
            self.validate_service_code()
        elif choice == "7":
            self.bill()
        elif choice == "8":
            return False
        else:
            raise Exception(f"Invalid command choice ({choice}).")

        return True

    def login_provider(self) -> None:
        if self.current_provider is not None:
            raise Exception("Error. Must logout to login.")
        id = int(input("Enter Provider ID: "))

        try:
            self.current_provider = self.current_system.lookup_provider(id)
        except Exception as e:
            print(e)

    def logout_provider(self) -> None:
        if self.current_provider is None:
            raise Exception("Error. No provider is logged in.")
        self.current_provider = None
        self.current_member = None

    def login_member(self) -> None:
        if self.current_member is not None:
            raise Exception("Error. A member is already logged in.")
        id = int(input("Enter Member ID: "))

        self.current_member = self.current_system.lookup_member(id)
        print("Validated.")

    def logout_member(self) -> None:
        if self.current_member is None:
            raise Exception("Error. No member is logged in.")
        self.current_member = None

    def request_provider_directory(self) -> None:
        if self.current_provider is None:
            raise Exception("Error. Must be logged in.")
        else:
            self.current_system.issue_provider_directory(self.current_provider)

    def validate_service_code(self) -> None:
        service_code = int(input("Enter Service Code: "))

        service = self.current_system.lookup_service(service_code)
        print(service.name)

    def bill(self) -> None:
        if self.current_member is None:
            raise Exception("Error. No member logged in.")
        if self.current_provider is None:
            raise Exception("Error. No provider logged in.")

        id = int(input("Enter Member ID: "))
        if id != self.current_member.id:
            raise Exception("Error. Incorrect member ID.")

        self.current_system.lookup_member(id)
        print("Validated.")

        date = input("Enter the service date (MM-DD-YYYY): ")
        month, day, year = map(int, date.split("-"))
        service_date = datetime(year, month, day)

        while True:
            code = int(input("Enter the service code"))
            service = self.current_system.lookup_service(code)
            print(service.name)
            user = str(input("Is this the correct service?(y/n) "))
            if user == "Y" or user == "y":
                break

        comments = str(input("Enter Comments: "))
        record = Record(
            service_date, self.current_provider, self.current_member, service, comments
        )
        self.current_system.record_service(record)


class ManagerTerminal(ProviderTerminal):
    current_manager: user.Manager | None

    def __init__(self, system: system.System) -> None:
        super().__init__(system)
        self.current_manager = None

    def run_command_menu(self) -> bool:
        print("Commands:")
        print("\t(1)  Manager Login")
        print("\t(2)  Manager Logout")
        print("\t(3)  Request Member Report")
        print("\t(4)  Request Provider Report")
        print("\t(5)  Request Summary Report")
        print()
        print("\t(6)  Provider Login")
        print("\t(7)  Provider Logout")
        print("\t(8)  Member Login")
        print("\t(9)  Member Logout")
        print("\t(10) Request Provider Directory")
        print("\t(11) Validate Service Code")
        print("\t(12) Bill")
        print()
        print("\t(13) Exit")
        choice = input("Enter Command (1-13): ")
        print()

        if choice == "1":
            self.login_manager()
        elif choice == "2":
            self.logout_manager()
        elif choice == "3":
            self.request_member_report()
        elif choice == "4":
            self.request_provider_report()
        elif choice == "5":
            self.request_summary_report()
        elif choice == "6":
            self.login_provider()
        elif choice == "7":
            self.logout_provider()
        elif choice == "8":
            self.login_member()
        elif choice == "9":
            self.logout_member()
        elif choice == "10":
            self.request_provider_directory()
        elif choice == "11":
            self.validate_service_code()
        elif choice == "12":
            self.bill()
        elif choice == "13":
            return False
        else:
            raise Exception(f"Invalid command choice ({choice}).")

        return True

    def login_manager(self) -> None:
        if self.current_manager is not None:
            raise Exception("Error. Must logout to login.")
        name = str(input("Enter Your Name: "))

        self.current_manager = self.current_system.lookup_manager(name)

    def logout_manager(self) -> None:
        if self.current_manager is None:
            raise Exception("Error. No manager is logged in.")
        self.current_manager = None

    def request_member_report(self) -> None:
        if self.current_manager is None:
            raise Exception("Error. No manager is logged in.")
        id = int(input("Enter member ID: "))

        member = self.current_system.lookup_member(id)
        self.current_system.issue_member_report(member)

    def request_provider_report(self) -> None:
        if self.current_manager is None:
            raise Exception("Error. No manager is logged in.")
        id = int(input("Enter provider ID: "))

        provider = self.current_system.lookup_provider(id)
        self.current_system.issue_provider_report(provider)

    def request_summary_report(self) -> None:
        if self.current_manager is None:
            raise Exception("Error. No manager is logged in.")
        self.current_system.issue_summary_report(self.current_manager)


class InteractiveMode:
    current_system: system.System

    def __init__(self, system: system.System) -> None:
        self.current_system = system

    def run_command_menu(self) -> bool:
        print("Commands:")
        print("\t(1) Add Member")
        print("\t(2) Delete Member")
        print("\t(3) Update Member Information")
        print("\t(4) Add Provider")
        print("\t(5) Delete Provider")
        print("\t(6) Update Provider Information")
        print("\t(7) Run Weekly Actions")
        print()
        print("\t(8) Exit")
        choice = input("Enter Command (1-8): ")
        print()

        if choice == "1":
            self.add_member()
        elif choice == "2":
            self.delete_member()
        elif choice == "3":
            self.update_member()
        elif choice == "4":
            self.add_provider()
        elif choice == "5":
            self.delete_provider()
        elif choice == "6":
            self.update_provider()
        elif choice == "7":
            self.run_weekly_actions()
        elif choice == "8":
            return False
        else:
            raise Exception(f"Invalid command choice ({choice}).")

        return True

    def add_member(self) -> None:
        name = input("Enter member name: ")
        id = int(input("Enter member id: "))
        address = input("Enter member address: ")
        city = input("Enter member city: ")
        state = input("Enter member state: ")
        zip_code = int(input("Enter member zip code: "))

        self.current_system.add_member(
            user.Member(name, id, address, city, state, zip_code, False)
        )

    def delete_member(self):
        id = int(input("Enter member id: "))
        self.current_system.remove_member(id)

    def update_member(self) -> None:
        id = int(input("Enter member id: "))
        member = self.current_system.lookup_member(id)

        print("Member information:")
        print("\t(1) Name")
        print("\t(2) Address")
        print("\t(3) City")
        print("\t(4) State")
        print("\t(5) Zip Code")
        print("\t(6) Suspended Status")
        choice = input("Select information to edit (1-6): ")
        print()

        if choice == "1":
            member.name = input("New member name: ")
        elif choice == "2":
            member.address = input("New member address: ")
        elif choice == "3":
            member.city = input("New member city: ")
        elif choice == "4":
            member.state = input("New member state: ")
        elif choice == "5":
            member.zip_code = int(input("New member zip code: "))
        elif choice == "6":
            self.current_system.suspend_member(id)
            print(f"Member suspended status set to {member.suspended}")
        else:
            raise Exception(f"Invalid choice ({choice}).")

        self.current_system.write_files()

    def add_provider(self) -> None:
        name = input("Enter provider name: ")
        id = int(input("Enter provider id: "))
        address = input("Enter provider address: ")
        city = input("Enter provider city: ")
        state = input("Enter provider state: ")
        zip_code = int(input("Enter provider zip code: "))

        self.current_system.add_provider(
            user.Provider(name, id, address, city, state, zip_code)
        )

    def delete_provider(self):
        id = int(input("Enter provider id: "))
        self.current_system.remove_provider(id)

    def update_provider(self) -> None:
        id = int(input("Enter provider id: "))
        provider = self.current_system.lookup_provider(id)

        print("Provider information:")
        print("\t(1) Name")
        print("\t(2) Address")
        print("\t(3) City")
        print("\t(4) State")
        print("\t(5) Zip Code")
        choice = input("Select information to edit (1-5): ")
        print()

        if choice == "1":
            provider.name = input("New provider name: ")
        elif choice == "2":
            provider.address = input("New provider address: ")
        elif choice == "3":
            provider.city = input("New provider city: ")
        elif choice == "4":
            provider.state = input("New provider state: ")
        elif choice == "5":
            provider.zip_code = int(input("New provider zip code: "))
        else:
            raise Exception(f"Invalid choice ({choice}).")

        self.current_system.write_files()

    def run_weekly_actions(self):
        self.current_system.weekly_actions()
        print("Weekly Actions Completed")
