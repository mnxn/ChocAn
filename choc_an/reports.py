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
        pass


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
        pass


class ProviderDirectory(report.Report):
    service_list: list[service.Service]

    def __init__(self, service_list: list[service.Service]) -> None:
        self.service_list = service_list

    def output(self) -> str:
        pass


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
        pass
