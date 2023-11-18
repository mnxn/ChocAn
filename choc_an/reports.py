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
        returnString = "Member Report:\n"
        returnString += "\tMember name: " + self.member.name + "\n"
        returnString += "\tMember number: " + str(self.member.id) + "\n"
        returnString += "\tMember address: " + self.member.address + "\n"
        returnString += "\tMember city: " + self.member.city + "\n"
        returnString += "\tMember state: " + self.member.state + "\n"
        returnString += "\tMember zipcode: " + str(self.member.zip_code) + "\n"
        for record in self.record_list:
            returnString += "\t\tDate of service: " + str(record.service_date_time)
            returnString += "\t\tProvider name: " + str(record.provider.name)
            returnString += "\t\tService name: " + record.service.name

        return returnString
        


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

        returnString = "Provider Report:\n"
        returnString += "\tProvider name: " + self.provider.name + "\n"
        returnString += "\tProvider ID number: " + str(self.provider.id) + "\n"
        returnString += "\Provider address: " + self.provider.address + "\n"
        returnString += "\tProvider city: " + self.provider.city + "\n"
        returnString += "\tProvider state: " + self.provider.state + "\n"
        returnString += "\tProvider zip code: " + str(self.provider.zip_code) + "\n"
        for record in self.record_list:
            returnString += "\t\tService date: " + str(record.service_date_time) + "\n"
            returnString += "\t\tCurrent date: " + str(record.current_date_time) + "\n" 
            returnString += "\t\tMember name: " + record.member.name + "\n" 
            returnString += "\t\tMember number: " + str(record.member.id) + "\n" 
            returnString += "\t\tService code: " + str(record.service.code) + "\n" 
            returnString += "\t\tFee to be paid: " + str(record.service.fee) + "\n\n" 
        returnString += "\tTotal number of consultations: " + str(self.total_consultations) + "\n"
        returnString += "\tTotal fee for the week: " + str(self.total_fee) + "\n"
        return returnString
        


class ProviderDirectory(report.Report):
    service_list: list[service.Service]

    def __init__(self, service_list: list[service.Service]) -> None:
        self.service_list = service_list

    def output(self) -> str:
        returnString = ("Provider Directory:\n")
        for x in range(len(self.service_list)):
            returnString += ("\tService: " + str(self.service_list[x].name) + "Service code: "+ str(self.service_list[x].code) + "\n")
        return returnString

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
        returnString = "Summary Report:\n"

        for record in self.entries:
            returnString += "\tProvider" + str(record.provider) + "\n"
            returnString += "\tNumber of consultations " + str(record.number_of_consultations) + "\n"
            returnString += "\tTotal fee" + str(record.total_fee) + "\n\n"
        
        returnString += "\tTotal providers: " + str(self.total_providers) + "\n"
        returnString += "\tTotal consultations: " + str(self.total_consultations) + "\n"
        returnString += "\tTotal fees: " + str(self.total_fee) + "\n"

        return returnString
