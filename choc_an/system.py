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
	
    def load_files(self) -> None:
        self.member_list = load_files_array(self.path + '/member_list')
        self.provider_list = load_files_array(self.path + '/provider_list')
        self.manager_list = load_files_array(self.path + '/manager_list')
        self.service_list = load_files_array(self.path + '/service_list')
        self.record_list = load_files_array(self.path + '/record_list')
		
    #Another argument can be added to import certain type of files ex .txt
    def load_files_array(self, path) -> array:
        if (os.path.exists(path) == 0):
            return None
        jsons_files = []
        for file_data in glob.glob(os.path.join(path, '*.json')):
            with open(os.path.join(os.get.cwd(), file_data, 'r')) as current_data:
                jsons_files += [ json.loads(current_data) ]
        return jsons_files
    
    	

    def write_files(self) -> None:
        if (count(self.member_list)):
            write_files_array(self.member_list, self.path + '/member_list', 'id')
		
        if (count(self.provider_list)):
            write_files_array(self.provider_list, self.path + '/provider_list', 'id')
		
        if (count(self.manager_list)):
            write_files_array(self.manager_list, self.path + '/manager_list')
			
        if (count(self.service_list)):
            write_files_array(self.service_list, self.path + '/service_list')
			
        if (count(self.record_list)):
            write_files_array(self.record_list, self.path + '/record_list')
			
    def write_files_array(self, array_data, path, save_by) -> None:
        if (os.path.exists(path) == 0):
            mkdir(path)
        for data in array_data:
            write_data(data, path+'/'+data[save_by]+'.json')
			
    def write_data(self, save_data, path):
        type_write = 'w'
        if (os.path.exists(path)):
            type_write = 'x'
        with open(path, type_write, encodeing='utf-8') as data_location:
            json.dump(save_data, data_location, ensure_ascii=False, indent=4)

		

    def add_member(self, new_member: user.Member) -> None:
        new_member_json = member_json()
        new_member_json['id'] = new_member.id
        new_member_json['address'] = new_member.address
        new_member_json['city'] = new_member.city
        new_member_json['state'] = new_member.state
        new_member_json['zip_code'] = new_member.zip_code
        new_member_json['suspended'] = new_member.suspended
        
        self.member_list += [new_member_json]
        
        #instead of saving the entire array again, only the new member is saved
        write_files_array(new_memeber_json, self.path+'/member', 'id')
    
    def member_json() -> None:
        user_format = '{ "name":null, "id":null, "address":null, "city":null, "state":null, "zip_code":null, "suspended":null}'
        return json.loads(user_format)
        

    def remove_member(self, id: int) -> None:
        self.member_list = remove_data_array(self.member_list, id, 'id')
        path_location = path+'/member/'+str(id)+'.json'
        
        if (os.path.exists(path_location)):
            os.remove(path_location)
        
    def remove_data_array(self, data_delete, tag_name, tag_by):
        for data in data_delete:
            if (data[tag_by] == tag_name):
                data_delete.pop(data)
                return data_delete
        return data_delete

	# Since their is no unsuspend, if this was called by and they were
	#suspended, it will unsuspend.
    def suspend_member(self, id: int) -> None:
        for data in self.member_list:
            if (data['id'] == id):
                if (data['suspended'] == True):
                	data['suspended'] = False
                else:
                    data['suspended'] = True
					

				

    def lookup_member(self, id: int) -> user.Member:
        return find_data(self.member_list, id, 'id')
        
    def find_data(data_list, tag_name, tag_by):
        for data in data_list:
	        if (data[tag_by] == tag_name):
		        return data
        return None

    def add_provider(self, new_provider: user.Provider) -> None:
        new_prd = provider_json()
        new_prd['name'] = new_provider.name
        new_prd['id'] = new_provider.id
        new_prd['address'] = new_provider.address
        new_prd['city'] = new_provider.city
        new_prd['state'] = new_provider.state
        new_prd['zip_code'] = new_provider.zip_code
        
        self.provider_list += [new_prd]
        write_files_array(new_prd, self.path+'/provider', 'id')
        
        
    def provider_json() -> None:
        user_format = '{ "name":null, "id":null, "address":null, "city":null, "state":null, "zip_code":null}'
        return json.loads(user_format)
		
		
    def remove_provider(self, id: int) -> None:
        self.member_list = remove_data_array(self.provider_list, id, 'id')
        path_location = path+'/provider/'+str(id)+'.json'
        
        if (os.path.exists(path_location)):
            os.remove(path_location)

    def lookup_provider(self, id: int) -> user.Provider:
        for data in self.provider_list:
            if (data['id'] == id):
                return data
        return None

    def lookup_manager(self, name: str) -> user.Manager:
        for data in self.manager_list:
            if (data['name'] == name):
                return data
        return None

    def lookup_service(self, code: int) -> service.Service:
        for data in self.service_list:
            if (data['code'] == code):
                return data
        return None

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
