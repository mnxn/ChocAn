import unittest
from choc_an import system
from datetime import datetime
from choc_an import service, system, user
from decimal import Decimal

class TestSystemClass(unittest.TestCase):
    def test_system(self):
        nonexistent_path = "/path/that/does/not/exist"
        with self.assertRaises(FileNotFoundError) as cm:
            system.System(nonexistent_path)
        the_exception = cm.exception
        self.assertEqual(str(the_exception), f"The specified path does not exist: {nonexistent_path}")
        
    def test_load_files(self):
        sys = system.System("tests") 
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
        manager=user.Manager("Harris Martin")
        sys2.manager_list.append(manager)
        self.assertEqual(len(sys2.manager_list), 1)
        self.assertEqual(sys2.manager_list[0].name, "Harris Martin")
        for data in sys2.manager_list:
            if data.name == manager.name:
                sys2.manager_list.remove(data)
                sys2.write_files()
        #Each load function is almost the same, if one is correct then all are correct
    def test_write_files(self):
        sys = system.System("data") 
        member=user.Member("Member", 123456789, "address1", "Portland", "OR", 99999, False)
        sys.member_list.append(member)
        sys.write_files()
        
        member_confirm=sys.lookup_member(123456789)
        self.assertEqual(member.name, member_confirm.name)
        self.assertEqual(member.id, member_confirm.id)
        self.assertEqual(member.address, member_confirm.address)
        self.assertEqual(member.state, member_confirm.state)
        self.assertEqual(member.city, member_confirm.city)
        self.assertEqual(member.suspended, member_confirm.suspended)
        sys.remove_member(123456789)
        #The write_file() function just calls the write_data() function multiple times and only needs to test whether write_data() is correct, so it is enough to only test writing member.json
    def test_add_member(self):
        sys = system.System("data") 
        member=user.Member("Member2", 123456780, "address1", "Portland", "OR", 99999, False)
        sys.add_member(member)
        member_confirm=sys.lookup_member(123456780)
        self.assertEqual(member.name, member_confirm.name)
        self.assertEqual(member.id, member_confirm.id)
        self.assertEqual(member.address, member_confirm.address)
        self.assertEqual(member.state, member_confirm.state)
        self.assertEqual(member.city, member_confirm.city)
        self.assertEqual(member.suspended, member_confirm.suspended)

    def test_remove_member(self):
        sys = system.System("data") 
        sys.remove_member(123456780)
        with self.assertRaises(Exception) as context:
            sys.lookup_member(123456780)
        self.assertEqual(str(context.exception), "Member not Found")

    def test_suspend_member(self):
        sys = system.System("data") 
        sys.suspend_member(258137067)
        member_confirm=sys.lookup_member(258137067)
        self.assertEqual(True, member_confirm.suspended)
        sys.suspend_member(258137067)
        member_confirm=sys.lookup_member(258137067)
        self.assertEqual(False, member_confirm.suspended)

    def test_lookup_member(self):
        pass

    def test_add_provider(self):
        pass

    def test_remove_provider(self):
        pass

    def test_lookup_provider(self):
        pass

    def test_lookup_manager(self):
        pass

    def test_lookup_service(self):
        pass

    def test_record_service(self):
        pass

    def test_issue_member_report(self):
        pass

    def test_issue_provider_report(self):
        pass

    def test_issue_provider_directory(self):
        pass

    def test_issue_summary_report(self):
        pass

    def test_write_eft_data(self):
        pass