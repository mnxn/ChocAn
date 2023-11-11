import unittest
from datetime import datetime
from decimal import Decimal
from choc_an import reports, service, user


class TestConstructors(unittest.TestCase):
    def test_member(self) -> None:
        name = "name"
        user_id = 123456789
        address = "Address"
        city = "City"
        state = "AB"
        zip_code = 12345
        suspended = False

        with self.assertRaises(ValueError, msg="id too short"):
            user.Member(name, 1, address, city, state, zip_code, suspended)

        with self.assertRaises(ValueError, msg="id too long"):
            user.Member(name, 1234567890, address, city, state, zip_code, suspended)

        with self.assertRaises(ValueError, msg="address too long"):
            user.Member(name, user_id, "a" * 26, city, state, zip_code, suspended)

        with self.assertRaises(ValueError, msg="city too long"):
            user.Member(name, user_id, address, "a" * 15, state, zip_code, suspended)

        with self.assertRaises(ValueError, msg="state too short"):
            user.Member(name, user_id, address, city, "A", zip_code, suspended)

        with self.assertRaises(ValueError, msg="state too long"):
            user.Member(name, user_id, address, city, "ABC", zip_code, suspended)

        with self.assertRaises(ValueError, msg="id too short"):
            user.Member(name, user_id, address, city, state, 1, suspended)

        with self.assertRaises(ValueError, msg="id too long"):
            user.Member(name, user_id, address, city, state, 123456, suspended)

        user.Member(name, user_id, address, city, state, zip_code, suspended)

    def test_provider_report(self):
        provider = user.Provider(
            name="name",
            id=123456789,
            address="Address",
            city="City",
            state="AB",
            zip_code=12345,
        )
        record_list = []
        total_consultations = 1
        total_fee = Decimal("123.45")

        with self.assertRaises(ValueError, msg="total_consultations too long"):
            reports.ProviderReport(provider, record_list, 1234, total_fee)

        with self.assertRaises(ValueError, msg="total_fee too long"):
            reports.ProviderReport(
                provider, record_list, total_consultations, Decimal("1234.56")
            )

        reports.ProviderReport(provider, record_list, total_consultations, total_fee)

    def test_summary_report_entry(self):
        provider = user.Provider(
            name="name",
            id=123456789,
            address="Address",
            city="City",
            state="AB",
            zip_code=12345,
        )
        number_of_consultations = 1
        total_fee = Decimal("12345.67")

        with self.assertRaises(ValueError, msg="number_of_consultations too long"):
            reports.SummaryReportEntry(provider, 1234, total_fee)

        with self.assertRaises(ValueError, msg="total_fee too long"):
            reports.SummaryReportEntry(
                provider, number_of_consultations, Decimal("123456.78")
            )

        reports.SummaryReportEntry(provider, number_of_consultations, total_fee)

    def test_service(self):
        name = "name"
        code = 123456
        fee = Decimal("123.45")

        with self.assertRaises(ValueError, msg="name too long"):
            service.Service("a" * 21, code, fee)

        with self.assertRaises(ValueError, msg="code too short"):
            service.Service(name, 1, fee)

        with self.assertRaises(ValueError, msg="code too long"):
            service.Service(name, 1234567, fee)

        with self.assertRaises(ValueError, msg="fee too long"):
            service.Service(name, code, Decimal("1233.56"))

        service.Service(name, code, fee)

    def test_record(self):
        city = "City"
        state = "AB"
        zip_code = 12345

        service_date_time = datetime.now()
        provider = user.Provider(
            "provider", 123456789, "address1", city, state, zip_code
        )
        member = user.Member(
            "member", 978654321, "address2", city, state, zip_code, False
        )
        provided_service = service.Service("name", 123456, Decimal("123.45"))
        comments = ""

        with self.assertRaises(ValueError, msg="comments too long"):
            service.Record(
                service_date_time, provider, member, provided_service, "a" * 101
            )

        service.Record(service_date_time, provider, member, provided_service, comments)


if __name__ == "__main__":
    unittest.main()
