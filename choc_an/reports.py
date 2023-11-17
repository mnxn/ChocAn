from decimal import Decimal
from . import report
from . import user
from . import service


class MemberReport(report.Report):
    member: user.Member
    record_list: list[service.Record]

    def __init__(self, member: user.Member, record_list: list[service.Record]) -> None:
        self.member = member
        self.record_list = record_list

    def output(self) -> str:
        print("Member Report:")
        print("\tMember: " + self.member.name)
        for x in range(len(self.record_list)):
            print("\t\t" + self.record_list[x].service.name)
        


class ProviderReport(report.Report):
    provider: user.Provider
    record_list: list[service.Record]
    total_consultations: int
    total_fee: Decimal

    def __init__(
        self,
        provider: user.Provider,
        record_list: list[service.Record],
        total_consultations: int,
        total_fee: Decimal,
    ) -> None:
        if total_consultations > 999:
            raise ValueError("total_consultations cannot have more than 3 digits")
        if total_fee > Decimal("999.99"):
            raise ValueError("total_fee cannot be more than $999.99")

        self.provider = provider
        self.record_list = record_list
        self.total_consultations = total_consultations
        self.total_fee = total_fee

    def output(self) -> str:
        print("Provider Report:")
        print("\tProvider: " + self.provider.name)
        print("\tTotal consultations: " + self.total_consultations)
        print("\tTotal charges: " + self.total_fee)
        for x in range(len(self.record_list)):
            print("\t\tRecord: " + self.record_list[x].service.name)
        


class ProviderDirectory(report.Report):
    service_list: list[service.Service]

    def __init__(self, service_list: list[service.Service]) -> None:
        self.service_list = service_list

    def output(self) -> str:
        print("Provider Directory:")
        for x in range(len(self.service_list)):
            print("\tService: " + self.service_list[x].name + "Service code: "+ self.service_list[x].code)


class SummaryReportEntry:
    provider: user.Provider
    number_of_consultations: int
    total_fee: Decimal

    def __init__(
        self,
        provider: user.Provider,
        number_of_consultations: int,
        total_fee: Decimal,
    ) -> None:
        if number_of_consultations > 999:
            raise ValueError("number_of_consultations cannot have more than 3 digits")
        if total_fee > Decimal("99999.99"):
            raise ValueError("total_fee cannot be more than $99,999.99")

        self.provider = provider
        self.number_of_consultations = number_of_consultations
        self.total_fee = total_fee


class SummaryReport(report.Report):
    entries: list[SummaryReportEntry]
    total_providers: int
    total_consultations: int
    total_fee: Decimal

    def __init__(
        self,
        entries: list[SummaryReportEntry],
        total_providers: int,
        total_consultations: int,
        total_fee: Decimal,
    ) -> None:
        self.entries = entries
        self.total_providers = total_providers
        self.total_consultations = total_consultations
        self.total_fee = total_fee

    def output(self) -> str:
        print("Summar Report:")
        print("\tTotal providers: " + self.total_providers)
        print("\tTotal consultations: " + self.total_consultations)
        print("\tTotal fees: " + self.total_fee)
        for x in range(len(self.entries)):
            print("\t\tProvider" + self.entries[x].provider)
            print("\t\tNumber of consultations " + self.entries[x].number_of_consultations)
            print("\t\tTotal fee" + self.entries[x].total_fee)
