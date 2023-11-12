from . import user
from . import service
from . import reports
import os
import glob
import json
import array

from io import open



class System:
    path: str
    member_list: list[user.Member]
    provider_list: list[user.Provider]
    manager_list: list[user.Manager]
    service_list: list[service.Service]
    record_list: list[service.Record]

    def __init__(self, path: str) -> None:
        self.path = path
        self.member_list = []
        self.provider_list = []
        self.manager_list = []
        self.service_list = []
        self.record_list = []
        self.load_files()
	

    
    def load_files(self) -> None:
        self.load_members()
        self.load_providers()
        self.load_managers()
        self.load_services()
        self.load_records()
		
    #Another argument can be added to import certain type of files ex .tx

    	

    def write_files(self) -> None:
        if (len(self.member_list)):
            self.write_data(self.members_to_json(self.member_list), self.path + '/member/members.json')
		
        if (len(self.provider_list)):
            self.write_data(self.providers_to_json(self.provider_list), self.path + '/provider/providers.json')
		
        if (len(self.manager_list)):
            self.write_data(self.managers_to_json(self.manager_list), self.path + '/manager/managers.json')
			
        if (len(self.service_list)):
            self.write_data(self.services_to_json(self.service_list), self.path + '/service/services.json')
			
        if (len(self.record_list)):
            self.write_data(self.records_to_json(self.record_list), self.path+'/record/records')
		

    def add_member(self, new_member: user.Member) -> None:
        new_member_json = user.Member(new_member.name, new_member.id, new_member.address, new_member.city, new_member.state, new_member.zip_code, new_member.suspended)
        self.member_list += [new_member_json]
        self.write_files()
    

    def remove_member(self, id: int) -> None:
        for data in self.member_list:
            if (data.id == id):
                self.member_list.pop(data)
                self.write_files()

	# Since their is no unsuspend, if this was called by and they were
	#suspended, it will unsuspend.
    def suspend_member(self, id: int) -> None:
        for data in self.member_list:
            if (data.id == id):
                if (data.suspended == True):
                    data.suspended = False
                else:
                    data.suspended = True
					

				

    def lookup_member(self, id: int) -> user.Member:
        for member in self.member_list:
            if (member.id == id):
                return user.Member(member.name, member.id, member.address, member.city, member.state, member.zip_code, member.suspended)
        raise Exception("Member not Found")

    def add_provider(self, new_provider: user.Provider) -> None:
        new_prd = user.Provider(new_provider.name, new_provider.id, new_provider.address, new_provider.city, new_provider.state, new_provider.zip_code)
        
        self.provider_list += [new_prd]
        self.write_files()
	
		
    def remove_provider(self, id: int) -> None:
        for data in self.provider_list:
            if (data.id == id):
                self.member_list.pop(data)
        self.write_files()

    def lookup_provider(self, id: int) -> user.Provider:
        for data in self.provider_list:
            if (data.id == id):
                return user.Provider(data.name, data.id, data.address, data.city, data.state, data.zip_code)
        raise Exception("Provider Not Found")

    def lookup_manager(self, name: str) -> user.Manager:
        for data in self.manager_list:
            if (data.name == name):
                return user.Manager(data.name)
        raise Exception("Manger Not Found")

    def lookup_service(self, code: int) -> service.Service:
        for data in self.service_list:
            if (data.code == code):
                return service.Service(data.name, data.code, data.fee)
        raise Exception("Service Not Found")

    def issue_member_report(self, member: user.Member) -> None:
        pass

    def issue_provider_report(self, provider: user.Provider) -> None:
        pass

    def issue_provider_directory(self, provider: user.Provider) -> None:
        pass

    def issue_summary_report(self, manager: user.Manager) -> None:
        pass

    def write_eft_data(self, record: service.Record) -> None:
        pass

    def weekly_actions(self) -> None:
        pass



    def members_to_json(self, convert: list[user.Member]) -> list[dict]:
        json_data: list[dict] = []
        for data in convert:
            json_data += [self.member_to_json(data)]
        return json_data
    
    def member_to_json(self, convert: user.Member) -> dict:
        json_datas = '{ "name":null, "id":null, "address":null, "city":null, "state":null, "zip_code":null, "suspended":null}'
        json_data: dict = json.loads(json_datas)
        json_data["name"] = convert.name
        json_data["id"] = convert.id
        json_data["address"] = convert.address
        json_data["city"] = convert.city
        json_data["state"] = convert.state
        json_data["zip_code"] = convert.zip_code
        json_data["suspended"] = convert.suspended

        return json_data
    
    def json_to_members(self, convert: list[dict]) -> list[user.Member]:
        hold_list: list[user.Member] = []
        for data in convert:
            hold_list += [self.json_to_member(data)]
        return hold_list

    def json_to_member(self, convert: dict) -> user.Member:
        return user.Member(convert["name"], convert["id"], convert["address"], convert["city"], convert["state"], convert["zip_code"], convert["suspended"])

    def providers_to_json(self, convert: list[user.Provider]) -> list[dict]:
        json_data: list[dict] = []
        for data in convert:
            json_data += [self.provider_to_json(data)]
        return json_data

    def provider_to_json(self, convert: user.Provider) -> dict:
        json_datas = '{ "name":null, "id":null, "address":null, "city":null, "state":null, "zip_code":null}'
        json_data: dict = json.loads(json_datas)
        json_data["name"] = convert.name
        json_data["id"] = convert.id
        json_data["address"] = convert.address
        json_data["city"] = convert.city
        json_data["state"] = convert.state
        json_data["zip_code"] = convert.zip_code

        return json_data
    
    def json_to_providers(self, convert: list[dict]) -> list[user.Provider]:
        hold_list: list[user.Provider] = []
        for data in convert:
            hold_list += [self.json_to_provider(data)]
        return hold_list

    def json_to_provider(self, convert: dict) -> user.Provider:
        return user.Provider(convert["name"], convert["id"], convert["address"], convert["city"], convert["state"], convert["zip_code"])

    def managers_to_json(self, convert: list[user.Manager]) -> list[dict]:
        json_hold: list[dict] = []
        for data in convert:
            json_hold += [self.manager_to_json(data)]
        return json_hold
    
    def manager_to_json(self, convert: user.Manager) -> dict:
        json_datas = '{ "name":null}'
        json_data: dict = json.loads(json_datas)
        json_data["name"] = convert.name
        
        return json_data
    
    def json_to_managers(self, convert: list[dict]) -> list[user.Manager]:
        hold_list: list[user.Manager] = []
        for data in convert:
            hold_list += [self.json_to_manager(data)]
        
        return hold_list
    
    def json_to_manager(self, convert: dict) -> user.Manager:
        return user.Manager(convert["name"])
    
    def services_to_json(self, convert: list[service.Service]) -> list[dict]:
        json_list: list[dict] = []
        for data in convert:
            json_list += [self.service_to_json(data)]
        
        return json_list
    
    def service_to_json(self, convert: service.Service) -> dict:
        json_datas = '{"name":null, "code":null, "fee":null}'
        json_data: dict = json.loads(json_datas)
        json_data["name"] = convert.name
        json_data["code"] = convert.code
        json_data["fee"] = convert.fee

        return json_data
    
    def json_to_services(self, convert: list[dict]) -> list[service.Service]:
        hold_list: list[service.Service] = []
        for data in convert:
            hold_list += [self.json_to_service(data)]
        return hold_list
    
    def json_to_service(self, convert: dict) -> service.Service:
        return service.Service(convert["name"], convert["code"], convert["fee"])
    
    def records_to_json(self, convert: list[service.Record]) -> list[dict]:
        json_hold: list[dict] = []
        for data in convert:
            json_hold += [self.record_to_json(data)]
        
        return json_hold
    
    def record_to_json(self, convert: service.Record) -> dict:
        json_datas = '{ "current_date_time":null, "service_date_time":null, "provider":null, "member":null, "service":null, "comments":null }'
        json_data: dict = json.loads(json_datas)
        json_data["current_data_time"] = convert.current_date_time
        json_data["service_data_time"] = convert.service_date_time
        json_data["provider"] = self.provider_to_json(convert.provider)
        json_data["member"] = self.member_to_json(convert.member)
        json_data["service"] = self.service_to_json(convert.service)
        json_data["comments"] = convert.comments

        return json_data
    
    def json_to_records(self, convert: list[dict]) -> list[service.Record]:
        hold_list: list[service.Record] = []
        for data in convert:
            hold_list += [self.json_to_record(data)]
        
        return hold_list
    
    def json_to_record(self, convert: dict) -> service.Record:
        member_data = self.json_to_member(convert["member"])
        provider_data = self.json_to_provider(convert["provider"])
        service_data = self.json_to_service(convert["service"])

        return service.Record(convert["service_date_time"], provider_data, member_data, service_data, convert["comments"])
    


    #load and save data

    def load_members(self) -> None:
        if (os.path.exists(self.path + '/member/members.json')):
            with open(self.path + '/member/members.json', 'r') as data:
                hold_data: list[dict] = json.load(data)
                self.member_list = self.json_to_members(hold_data)

    def load_providers(self) -> None:
        if (os.path.exists(self.path + '/provider/providers.json')):
            with open(self.path + '/provider/providers.json', 'r') as data:
                info: list[dict] = json.load(data)
                self.provider_list = self.json_to_providers(info)

    def load_managers(self) -> None:
        if (os.path.exists(self.path + '/manger/mangers.json')):
            with open(self.path + '/manger/mangers.json', 'r') as data:
                info: list[dict] = json.load(data)
                self.manger_list = self.json_to_managers(info)

    def load_services(self) -> None:
        if (os.path.exists(self.path + '/service/services.json')):
            with open(self.path + '/service/services.json', 'r') as data:
                info: list[dict] = json.load(data)
                self.service_list = self.json_to_services(info)

    def load_records(self) -> None:
        if (os.path.exists(self.path + '/record/records.json')):
            with open(self.path + '/record/records.json', 'r') as data:
                info: list[dict] = json.load(data)
                self.record_list = self.json_to_records(info)


    def write_data(self, save_data: list, path: str):
        type_write: str = 'w'
        if (os.path.exists(path)):
            type_write = 'x'
        with open(path, type_write) as data_location:
            json.dump(save_data, data_location, ensure_ascii=False, indent=4)
