from . import user
from . import service
from . import reports
import os
import glob
import json
import array


#Date 11/10/2023 or etc, however this file is not finshed, until record service.
#Another thing, member_list is made of json data, not classes of the datas
#which can be changed, Another thing, instead of saving the entire list in one file
#they are saved by user ids, in the folders belonging to member/provider/etc
#which can be changed.
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
	
    def load_files_array(self, path):
        if (os.path.exists(path) == 0):
            return None
        jsons_files = []
        for file_data in glob.glob(os.path.join(path, '*.json')):
            with open(os.path.join(os.get.cwd(), file_data, 'r')) as current_data:
                jsons_files += [ json.loads(current_data) ]
        return jsons_files
    
    def load_files(self) -> None:
        self.member_list = self.load_files_array(self.path + '/member_list')
        self.provider_list = self.load_files_array(self.path + '/provider_list')
        self.manager_list = self.load_files_array(self.path + '/manager_list')
        self.service_list = self.load_files_array(self.path + '/service_list')
        self.record_list = self.load_files_array(self.path + '/record_list')
		
    #Another argument can be added to import certain type of files ex .tx

    	

    def write_files(self) -> None:
        if (len(self.member_list)):
            self.write_data(self.members_json(self.member_list), self.path + '/member_list')
		
        if (len(self.provider_list)):
            self.write_data(self.providers_json(self.provider_list), self.path + '/provider_list')
		
        if (len(self.manager_list)):
            self.write_data(self.managers_json(self.manager_list), self.path + '/manager_list')
			
        if (len(self.service_list)):
            self.write_data(self.services_json(self.service_list), self.path + '/service_list')
			
        #This part can be changed, unlike the tops, this might override files because of the
        #naming of the files
        if (len(self.record_list)):
            self.write_files_array(self.record_list, self.path + '/record_list', 'service_date_time')
	

			
    def write_data(self, save_data, path):
        type_write = 'w'
        if (os.path.exists(path)):
            type_write = 'x'
        with open(path, type_write, encodeing='utf-8') as data_location:
            json.dump(save_data, data_location, ensure_ascii=False, indent=4)

		

    def add_member(self, new_member: user.Member) -> None:
        new_member_json = user.member(new_member.name, new_member.id, new_member.address, new_member.city, new_member.state, new_member.zip_code, new_member.suspended)
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
            if (data['id'] == id):
                if (data.suspended == True):
                    data.suspended = False
                else:
                    data.suspended = True
					

				

    def lookup_member(self, id: int) -> user.Member:
        for member in self.member_list:
            if (member.id == id):
                return user.member(member.name, member.id, member.address, member.city, member.state, member.zip_code, member.suspended)
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
                return user.Provider(data['name'], data['id'], data['address'], data['city'], data['state'], data['zip_code'])
        raise Exception("Provider Not Found")

    def lookup_manager(self, name: str) -> user.Manager:
        for data in self.manager_list:
            if (data.name == name):
                return user.Manager(data['name'])
        raise Exception("Manger Not Found")

    def lookup_service(self, code: int) -> service.Service:
        for data in self.service_list:
            if (data.code == code):
                return service.Service(data['name'], data['code'], data['fee'])
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
