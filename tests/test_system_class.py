import unittest
import os
import shutil
from datetime import datetime
from decimal import Decimal
from choc_an import service, system, user


class TestSystemClass(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        # Try to remove any reports generated by previous test runs.
        shutil.rmtree("reports", ignore_errors=True)

    def test_system(self) -> None:
        nonexistent_path = "/path/that/does/not/exist"
        with self.assertRaises(FileNotFoundError) as cm:
            system.System(nonexistent_path)
        the_exception = cm.exception
        self.assertEqual(
            str(the_exception), f"The specified path does not exist: {nonexistent_path}"
        )

    def test_load_files(self) -> None:
        sys = system.System("tests", load=False)
        with self.assertRaises(FileNotFoundError):
            sys.load_members()

        with self.assertRaises(FileNotFoundError):
            sys.load_providers()

        with self.assertRaises(FileNotFoundError):
            sys.load_managers()

        with self.assertRaises(FileNotFoundError):
            sys.load_services()

        with self.assertRaises(FileNotFoundError):
            sys.load_records()

        sys2 = system.System("data")
        self.assertEqual(len(sys2.manager_list), 10)
        self.assertEqual(sys2.manager_list[0].name, "Harris Martin")
        # Each load function is almost the same, if one is correct then all are correct

    def test_write_files(self) -> None:
        sys = system.System("data")
        member = user.Member(
            "Member", 123456789, "address1", "Portland", "OR", 99999, False
        )
        sys.member_list.append(member)
        sys.write_files()
        sys.load_files()
        member_confirm = sys.lookup_member(123456789)
        self.assertEqual(member.name, member_confirm.name)
        self.assertEqual(member.id, member_confirm.id)
        self.assertEqual(member.address, member_confirm.address)
        self.assertEqual(member.state, member_confirm.state)
        self.assertEqual(member.city, member_confirm.city)
        self.assertEqual(member.suspended, member_confirm.suspended)
        sys.remove_member(123456789)
        # The write_file() function just calls the write_data() function multiple times and only needs to test whether write_data() is correct, so it is enough to only test writing member.json

    def test_add_member(self) -> None:
        sys = system.System("data")
        member = user.Member(
            "Member2", 123456780, "address1", "Portland", "OR", 99999, False
        )
        sys.add_member(member)
        member_confirm = sys.lookup_member(123456780)
        self.assertEqual(member.name, member_confirm.name)
        self.assertEqual(member.id, member_confirm.id)
        self.assertEqual(member.address, member_confirm.address)
        self.assertEqual(member.state, member_confirm.state)
        self.assertEqual(member.city, member_confirm.city)
        self.assertEqual(member.suspended, member_confirm.suspended)

    def test_remove_member(self) -> None:
        sys = system.System("data")
        sys.remove_member(123456780)
        with self.assertRaises(Exception) as context:
            sys.lookup_member(123456780)
        self.assertEqual(str(context.exception), "Member not Found")

    def test_suspend_member(self) -> None:
        sys = system.System("data")
        sys.suspend_member(258137067)
        member_confirm = sys.lookup_member(258137067)
        self.assertEqual(True, member_confirm.suspended)
        sys.suspend_member(258137067)
        member_confirm = sys.lookup_member(258137067)
        self.assertEqual(False, member_confirm.suspended)

    def test_lookup_member(self) -> None:
        current_system = system.System("data")
        member_confirm = current_system.lookup_member(628574130)
        known_member = user.Member(
            name="Harris Martin",
            id=628574130,
            address="2 Homestead St. ",
            city="Sheffield",
            state="AR",
            zip_code=51810,
            suspended=False,
        )

        self.assertEqual(known_member.name, member_confirm.name)
        self.assertEqual(known_member.id, member_confirm.id)
        self.assertEqual(known_member.state, member_confirm.state)
        self.assertEqual(known_member.city, member_confirm.city)
        self.assertEqual(known_member.suspended, member_confirm.suspended)

    def test_add_provider(self) -> None:
        current_system = system.System("data")
        test_provider = user.Provider(
            name="Austin Myers",
            id=123456789,
            address="308 Negra Arroyo Lane",
            city="Albuquerque",
            state="NM",
            zip_code=90210,
        )

        current_system.add_provider(test_provider)

        confirm_provider = current_system.lookup_provider(123456789)
        self.assertEqual(test_provider.name, confirm_provider.name)
        self.assertEqual(test_provider.id, confirm_provider.id)
        self.assertEqual(test_provider.address, confirm_provider.address)
        self.assertEqual(test_provider.city, confirm_provider.city)
        self.assertEqual(test_provider.state, confirm_provider.state)
        self.assertEqual(test_provider.zip_code, confirm_provider.zip_code)
        current_system.remove_provider(123456789)

    def test_remove_provider(self) -> None:
        current_system = system.System("data")
        test_provider = user.Provider(
            name="Austin Myers",
            id=987654321,
            address="308 Negra Arroyo Lane",
            city="Albuquerque",
            state="NM",
            zip_code=90210,
        )

        current_system.add_provider(test_provider)
        # Act: Remove the provider from the system
        current_system.remove_provider(987654321)

        # Assert: Check if the provider is no longer in the provider_list
        with self.assertRaises(Exception) as context:
            current_system.lookup_provider(987654321)
        self.assertEqual(str(context.exception), "Provider Not Found")

    def test_lookup_provider(self) -> None:
        current_system = system.System("data")
        provider_confirm = current_system.lookup_provider(186972363)
        known_provider = user.Provider(
            name="Miller Nelson",
            id=186972363,
            address="7304 St Louis St. ",
            city="Anchorage",
            state="NC",
            zip_code=60337,
        )

        self.assertEqual(known_provider.name, provider_confirm.name)
        self.assertEqual(known_provider.id, provider_confirm.id)
        self.assertEqual(known_provider.address, provider_confirm.address)
        self.assertEqual(known_provider.state, provider_confirm.state)
        self.assertEqual(known_provider.city, provider_confirm.city)
        self.assertEqual(known_provider.zip_code, provider_confirm.zip_code)

    def test_lookup_manager(self) -> None:
        current_system = system.System("data")
        manager_confirm = current_system.lookup_manager("Gaven Martin")
        known_manager = user.Manager(name="Gaven Martin")

        self.assertEqual(known_manager.name, manager_confirm.name)

    def test_lookup_service(self) -> None:
        current_system: system.System = system.System("data")
        service_name: str = "chocvaccination"
        service_code: int = 388592
        service_fee: Decimal = Decimal(454)
        find_service: service.Service = current_system.lookup_service(service_code)

        self.assertEqual(service_name, find_service.name)
        self.assertEqual(service_code, find_service.code)
        self.assertEqual(service_fee, find_service.fee)

    def test_record_service(self) -> None:
        current_system = system.System("data", readonly=True)
        service_date_time = datetime.now()

        provider = current_system.lookup_provider(404008286)
        member = current_system.lookup_member(518959495)
        provided_service = current_system.lookup_service(350353)
        comments = ""
        record = service.Record(
            service_date_time, provider, member, provided_service, comments
        )

        before_append = len(current_system.record_list)
        current_system.record_service(record)
        after_append = len(current_system.record_list)

        self.assertEqual(
            before_append + 1, after_append, msg="record not added to record list"
        )

    def test_issue_member_report(self) -> None:
        current_system = system.System("data", readonly=True)
        member = current_system.lookup_member(628574130)

        date = datetime.now().strftime("%Y-%m-%d")

        path = f"reports/Harris Martin_{date}.txt"
        current_system.issue_member_report(member)
        check_file = os.path.exists(path)

        self.assertTrue(check_file, msg="report not made")

    def test_issue_provider_report(self) -> None:
        current_system = system.System("data", readonly=True)
        provider = current_system.lookup_provider(186972363)

        date = datetime.now().strftime("%Y-%m-%d")

        path = f"reports/Miller Nelson_{date}.txt"
        current_system.issue_provider_report(provider)
        check_file = os.path.exists(path)

        self.assertTrue(check_file, msg="report not made")

    def test_issue_provider_directory(self) -> None:
        current_system = system.System("data", readonly=True)
        provider = current_system.lookup_provider(207695080)

        date = datetime.now().strftime("%Y-%m-%d")

        path = f"reports/Thompson Taylor_{date}.txt"
        current_system.issue_provider_directory(provider)
        check_file = os.path.exists(path)

        self.assertTrue(check_file, msg="service directory not issued")

    def test_issue_summary_report(self) -> None:
        current_system = system.System("data", readonly=True)
        manager = current_system.lookup_manager("Adam Striven")

        date = datetime.now().strftime("%Y-%m-%d")

        path = f"reports/Adam Striven_{date}.txt"
        current_system.issue_summary_report(manager)
        check_file = os.path.exists(path)

        self.assertTrue(check_file, msg="summary report not made")

    def test_write_eft_data(self) -> None:

        sys=system.System("data")
        provider=sys.lookup_provider(570619233)
        date = datetime.now().strftime("%Y-%m-%d")
        test_path = f"reports/eft_{date}.txt"
        sys.write_eft_data(provider,Decimal('999.99'),test_path)
        self.assertTrue(os.path.exists(test_path), "EFT file does not exist.")
        with open(test_path, 'r') as file:
            data = file.read()
            expected_data = f"{provider.name}, {provider.id}, {Decimal('999.99')}"
            self.assertIn(expected_data, data, "The file does not contain the expected data.")
        os.remove(test_path)
