import unittest
from datetime import datetime
from decimal import Decimal
from choc_an import user, service, reports


class TestReportOutput(unittest.TestCase):
    def test_member_output(self) -> None:
        member = user.Member(
            "Member", 123456789, "address1", "Portland", "OR", 99999, False
        )
        provider = user.Provider(
            "Provider", 987654321, "address2", "Portland", "OR", 99999
        )
        services = service.Service("Services", 123456, Decimal("999.99"))
        records = [
            service.Record(datetime(2023, 1, 1), provider, member, services, "ABCDE")
        ]
        member_report = reports.MemberReport(member, records)
        expected_output = """
Member Report:
\tMember name: Member
\tMember number: 123456789
\tMember address: address1
\tMember city: Portland
\tMember state: OR
\tMember zipcode: 99999
\t\tDate of service: 01-01-2023
\t\tProvider name: Provider
\t\tService name: Services
"""
        self.assertEqual(member_report.output().strip(), expected_output.strip())

    def test_provider_output(self) -> None:
        provider = user.Provider(
            "Provider", 987654321, "address2", "Portland", "OR", 99999
        )
        member = user.Member(
            "Member", 123456789, "address1", "Portland", "OR", 99999, False
        )
        services = service.Service("Services", 123456, Decimal("999.99"))
        records = [
            service.Record(datetime(2023, 1, 1), provider, member, services, "ABCDE")
        ]
        provider_report = reports.ProviderReport(
            provider, records, 10, Decimal("999.99")
        )
        output = provider_report.output()
        self.assertIn("Provider Report:", output)
        self.assertIn("Provider name: Provider", output)
        self.assertIn("Provider ID number: 987654321", output)
        self.assertIn("Provider address: address2", output)
        self.assertIn("Provider city: Portland", output)
        self.assertIn("Provider state: OR", output)
        self.assertIn("Provider zip code: 99999", output)
        self.assertIn("Service date: 01-01-2023", output)
        self.assertIn("Member name: Member", output)
        self.assertIn("Member number: 123456789", output)
        self.assertIn("Service code: 123456", output)
        self.assertIn("Fee to be paid: 999.99", output)
        self.assertIn("Total number of consultations: 10", output)
        self.assertIn("Total fee for the week: 999.99", output)
        # This is done because I cannot effectively predict the current_date data

    def test_summary_output(self) -> None:
        provider = user.Provider("name", 987654321, "address2", "Portland", "OR", 99999)
        lists = [reports.SummaryReportEntry(provider, 10, Decimal("9999.99"))]
        summary_report = reports.SummaryReport(lists, 1, 10, Decimal("9999.99"))
        expected_output = """
Summary Report:
\tProvider: name
\tNumber of consultations: 10
\tTotal fee: 9999.99

\tTotal providers: 1
\tTotal consultations: 10
\tTotal fees: 9999.99
"""
        self.assertEqual(summary_report.output().strip(), expected_output.strip())

    def test_provider_directory(self) -> None:
        services_list = [
            service.Service("Services1", 123456, Decimal("999.99")),
            service.Service("Services2", 654321, Decimal("199.99")),
        ]
        provider_directory = reports.ProviderDirectory(services_list)
        expected_output = """
Provider Directory:
\tService: Services1
\t\tCode: 123456
\t\tFee: 999.99
\tService: Services2
\t\tCode: 654321
\t\tFee: 199.99
"""
        self.assertEqual(provider_directory.output().strip(), expected_output.strip())
