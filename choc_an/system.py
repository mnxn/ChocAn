import os
import json
from io import open
from datetime import datetime
from decimal import Decimal
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
    readonly: bool = False

    def __init__(self, path: str) -> None:
        self.path = path
        self.member_list = []
        self.provider_list = []
        self.manager_list = []
        self.service_list = []
        self.record_list = []
        self.readonly = readonly
        self.load_files()

    def load_files(self) -> None:
        self.load_members()
        self.load_providers()
        self.load_managers()
        self.load_services()
        self.load_records()

    # Another argument can be added to import certain type of files ex .tx

    def write_files(self) -> None:
        if len(self.member_list):
            self.write_data(
                self.members_to_json(self.member_list),
                self.path + "/member/members.json",
            )

        if len(self.provider_list):
            self.write_data(
                self.providers_to_json(self.provider_list),
                self.path + "/provider/providers.json",
            )

        if len(self.manager_list):
            self.write_data(
                self.managers_to_json(self.manager_list),
                self.path + "/manager/managers.json",
            )

        if len(self.service_list):
            self.write_data(
                self.services_to_json(self.service_list),
                self.path + "/service/services.json",
            )

        if len(self.record_list):
            self.write_data(
                self.records_to_json(self.record_list),
                self.path + "/record/records.json",
            )

    def add_member(self, new_member: user.Member) -> None:
        self.member_list.append(new_member)
        if not self.readonly:
            self.write_files()

    def remove_member(self, id: int) -> None:
        for data in self.member_list:
            if data.id == id:
                self.member_list.remove(data)
                if not self.readonly:
                    self.write_files()
                return

    # Since their is no unsuspend, if this was called by and they were
    # suspended, it will unsuspend.
    def suspend_member(self, id: int) -> None:
        for data in self.member_list:
            if data.id == id:
                if data.suspended == True:
                    data.suspended = False
                else:
                    data.suspended = True
                return

    def lookup_member(self, id: int) -> user.Member:
        for member in self.member_list:
            if member.id == id:
                return member
        raise Exception("Member not Found")

    def add_provider(self, new_provider: user.Provider) -> None:
        self.provider_list.append(new_provider)
        if not self.readonly:
            self.write_files()

    def remove_provider(self, id: int) -> None:
        for data in self.provider_list:
            if data.id == id:
                self.provider_list.remove(data)
                if not self.readonly:
                    self.write_files()
                return

    def lookup_provider(self, id: int) -> user.Provider:
        for data in self.provider_list:
            if data.id == id:
                return data
        raise Exception("Provider Not Found")

    def lookup_manager(self, name: str) -> user.Manager:
        for data in self.manager_list:
            if data.name == name:
                return data
        raise Exception("Manager Not Found")

    def lookup_service(self, code: int) -> service.Service:
        for data in self.service_list:
            if data.code == code:
                return data
        raise Exception("Service Not Found")

    def record_service(self, record: service.Record) -> None:
        self.record_list.append(record)
        if not self.readonly:
            self.write_files()

    def issue_member_report(self, member: user.Member) -> None:
        records: list[service.Record] = []
        report: reports.MemberReport
        for record in self.record_list:
            if record.member.id == member.id:
                records.append(record)
        report = reports.MemberReport(member, records)
        member.receive_report(report)

    def issue_provider_report(self, provider: user.Provider) -> None:
        records: list[service.Record] = []
        total_consultations: int = 0
        total_fee: Decimal = Decimal(0)
        # Yeah: the 0 is an Int, Converting it to Dec fixed it
        report: reports.ProviderReport
        for record in self.record_list:
            if record.provider.id == provider.id:
                records.append(record)
                total_consultations += 1
                total_fee += record.service.fee
        report = reports.ProviderReport(
            provider, records, total_consultations, total_fee
        )
        provider.receive_report(report)

    def issue_provider_directory(self, provider: user.Provider) -> None:
        report: reports.ProviderDirectory = reports.ProviderDirectory(self.service_list)
        provider.receive_report(report)

    def issue_summary_report(self, manager: user.Manager) -> None:
        entries: list[reports.SummaryReportEntry] = []
        total_providers: int = 0
        total_consultations: int = 0
        grand_total_fee: Decimal = Decimal(0)

        report: reports.SummaryReport

        for provider in self.provider_list:
            consultations: int = 0
            total_fee: Decimal = Decimal(0)
            for record in self.record_list:
                if record.provider.id == provider.id:
                    consultations += 1
                    total_fee += record.service.fee
            entries.append(
                reports.SummaryReportEntry(provider, consultations, (total_fee))
            )
            total_providers += 1
            grand_total_fee += total_fee
            total_consultations += consultations

        report = reports.SummaryReport(
            entries, total_providers, total_consultations, grand_total_fee
        )
        manager.receive_report(report)

    def write_eft_data(
        self, provider: user.Provider, provider_fee: Decimal, path: str
    ) -> None:
        data = f"{provider.name}, {provider.id}, {provider_fee}"

        # Create the directory if it doesn't exist
        os.makedirs(os.path.dirname(path), exist_ok=True)

        # Write data to path
        with open(path, "a") as eft_file:
            json.dump(data, eft_file, ensure_ascii=False, indent=2)
            eft_file.write("\n")

    def weekly_actions(self) -> None:
        for member in self.member_list:
            self.issue_member_report(member)

        for provider in self.provider_list:
            self.issue_provider_report(provider)

        for manager in self.manager_list:
            self.issue_summary_report(manager)

        for provider in self.provider_list:
            provider_fee: Decimal = Decimal(0)
            for record in self.record_list:
                if record.provider.id == provider.id:
                    provider_fee += record.service.fee
            if provider_fee != 0:
                self.write_eft_data(
                    provider, provider_fee, self.path + "/record/eft.txt"
                )

    def members_to_json(self, convert: list[user.Member]) -> list[dict]:
        json_data: list[dict] = []
        for data in convert:
            json_data.append(self.member_to_json(data))
        return json_data

    def member_to_json(self, convert: user.Member) -> dict:
        return {
            "name": convert.name,
            "id": convert.id,
            "address": convert.address,
            "city": convert.city,
            "state": convert.state,
            "zip_code": convert.zip_code,
            "suspended": convert.suspended,
        }

    def json_to_members(self, convert: list[dict]) -> list[user.Member]:
        hold_list: list[user.Member] = []
        for data in convert:
            hold_list.append(self.json_to_member(data))
        return hold_list

    def json_to_member(self, convert: dict) -> user.Member:
        return user.Member(
            convert["name"],
            convert["id"],
            convert["address"],
            convert["city"],
            convert["state"],
            convert["zip_code"],
            convert["suspended"],
        )

    def providers_to_json(self, convert: list[user.Provider]) -> list[dict]:
        json_data: list[dict] = []
        for data in convert:
            json_data.append(self.provider_to_json(data))
        return json_data

    def provider_to_json(self, convert: user.Provider) -> dict:
        return {
            "name": convert.name,
            "id": convert.id,
            "address": convert.address,
            "city": convert.city,
            "state": convert.state,
            "zip_code": convert.zip_code,
        }

    def json_to_providers(self, convert: list[dict]) -> list[user.Provider]:
        hold_list: list[user.Provider] = []
        for data in convert:
            hold_list.append(self.json_to_provider(data))
        return hold_list

    def json_to_provider(self, convert: dict) -> user.Provider:
        return user.Provider(
            convert["name"],
            convert["id"],
            convert["address"],
            convert["city"],
            convert["state"],
            convert["zip_code"],
        )

    def managers_to_json(self, convert: list[user.Manager]) -> list[dict]:
        json_hold: list[dict] = []
        for data in convert:
            json_hold.append(self.manager_to_json(data))
        return json_hold

    def manager_to_json(self, convert: user.Manager) -> dict:
        return {"name": convert.name}

    def json_to_managers(self, convert: list[dict]) -> list[user.Manager]:
        hold_list: list[user.Manager] = []
        for data in convert:
            hold_list.append(self.json_to_manager(data))

        return hold_list

    def json_to_manager(self, convert: dict) -> user.Manager:
        return user.Manager(convert["name"])

    def services_to_json(self, convert: list[service.Service]) -> list[dict]:
        json_list: list[dict] = []
        for data in convert:
            json_list.append(self.service_to_json(data))

        return json_list

    def service_to_json(self, convert: service.Service) -> dict:
        return {"name": convert.name, "code": convert.code, "fee": convert.fee}

    def json_to_services(self, convert: list[dict]) -> list[service.Service]:
        hold_list: list[service.Service] = []
        for data in convert:
            hold_list.append(self.json_to_service(data))
        return hold_list

    def json_to_service(self, convert: dict) -> service.Service:
        return service.Service(convert["name"], convert["code"], convert["fee"])

    def records_to_json(self, convert: list[service.Record]) -> list[dict]:
        json_hold: list[dict] = []
        for data in convert:
            json_hold.append(self.record_to_json(data))

        return json_hold

    def record_to_json(self, convert: service.Record) -> dict:
        return {
            "current_date_time": convert.current_date_time.timestamp(),
            "service_date_time": convert.service_date_time.timestamp(),
            "provider": convert.provider.id,
            "member": convert.member.id,
            "service": convert.service.code,
            "comments": convert.comments,
        }

    def json_to_records(self, convert: list[dict]) -> list[service.Record]:
        hold_list: list[service.Record] = []
        for data in convert:
            hold_list.append(self.json_to_record(data))

        return hold_list

    def json_to_record(self, convert: dict) -> service.Record:
        member_data = self.lookup_member(convert["member"])
        # no current Exception is placed.
        provider_data = self.lookup_provider(convert["provider"])
        service_data = self.lookup_service(convert["service"])

        record = service.Record(
            datetime.fromtimestamp(convert["service_date_time"]),
            provider_data,
            member_data,
            service_data,
            convert["comments"],
        )
        record.current_date_time = datetime.fromtimestamp(convert["current_date_time"])
        return record

    # load and save data

    def load_members(self) -> None:
        if os.path.exists(self.path + "/member/members.json"):
            with open(self.path + "/member/members.json", "r") as data:
                hold_data: list[dict] = json.load(data)
                self.member_list = self.json_to_members(hold_data)

    def load_providers(self) -> None:
        if os.path.exists(self.path + "/provider/providers.json"):
            with open(self.path + "/provider/providers.json", "r") as data:
                info: list[dict] = json.load(data)
                self.provider_list = self.json_to_providers(info)

    def load_managers(self) -> None:
        if os.path.exists(self.path + "/manager/managers.json"):
            with open(self.path + "/manager/managers.json", "r") as data:
                info: list[dict] = json.load(data)
                self.manager_list = self.json_to_managers(info)

    def load_services(self) -> None:
        if os.path.exists(self.path + "/service/services.json"):
            with open(self.path + "/service/services.json", "r") as data:
                info: list[dict] = json.load(data)
                self.service_list = self.json_to_services(info)

    def load_records(self) -> None:
        if os.path.exists(self.path + "/record/records.json"):
            with open(self.path + "/record/records.json", "r") as data:
                info: list[dict] = json.load(data)
                self.record_list = self.json_to_records(info)

    def write_data(self, save_data: list, path: str):
        if os.path.exists(path):
            os.remove(path)
        with open(path, "w") as data_location:
            json.dump(save_data, data_location, ensure_ascii=False, indent=4)
