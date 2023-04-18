# -*- coding: utf-8 -*-
"""
Created on Thu Jan 26 13:42:55 2023

@author: DELL
"""

import discord, copy

def get_guild(client, guild_id) :
    guild = [guild for guild in client.guilds if guild.id == guild_id] or None # returns None if no matches.
    return guild

def decrypt_data(row_message_object, split_delim) :
    row = row_message_object.content
    message_id = row_message_object.id
    row_sample = row.split(split_delim)
    row_data = {row_sample[k] : row_sample[(k + 1)] for k in range(0, len(row_sample), 2)}
    row_info = {'row_data' : row_data, 'message_id' : message_id}
    return row_info

class UniformBranch() :
    # Keys are the same for every row.
    def __init__(self, perm_db, channel) :
        self.channel = channel
        self.data = []
        self.name = self.channel.name
        self.perm_db = perm_db
        self.split_delim = ' [:|=|:] '
        self.setted_up = False
        return
    
    async def setup(self) :
        await self.refresh()
        self.setted_up = True
        return
    
    async def refresh(self) :
        self.data = []
        async for row_message_object in self.channel.history(limit = None) :
            # row = row_message_object.content
            # message_id = row_message_object.id
            # row_sample = row.split(self.split_delim)
            # row_data = {row_sample[k] : row_sample[(k + 1)] for k in range(0, len(row_sample), 2)}
            row_info = decrypt_data(row_message_object, self.split_delim)
            self.data.append(row_info)
        return
    
    async def store(self, values) :
        # Values should be a dictionary with {key : value} format for storage.
        storage_str = self.split_delim.join([k + self.split_delim + values[k] for k in values])
        message = await self.channel.send(storage_str)
        row_info = {'row_data' : copy.deepcopy(values), 'message_id' : message.id}
        self.data.append(row_info)
        return row_info
    
    async def modify(self, search_values, modif_values) :
        filtered_data = await self.fetch_results(search_values)
        for info in filtered_data :
            try :
                new_values = copy.deepcopy(info['row_data'])
                msg_id = info['message_id']
                index = self.data.index(info)
                for k in modif_values :
                    new_values[k] = modif_values[k]
                    self.data[index]['row_data'][k] = copy.deepcopy(modif_values[k])
                    continue
                message = await self.channel.fetch_message(msg_id)
                storage_str = self.split_delim.join([k + self.split_delim + new_values[k] for k in new_values])
                await message.edit(content = storage_str)
                continue
            except :
                print('Row has been deleted/doesn\'t exist anymore or couldn\'t be retrieved[Try again, since the internal cache might not have been refreshed.]')
                return None
        return
    
    async def delete(self, search_values) :
        filtered_data = await self.fetch_results(search_values)
        for info in filtered_data :
            message = await self.channel.fetch_message(info['message_id'])
            await message.delete()
            self.data = [copy.deepcopy(k) for k in self.data.copy() if k['message_id'] != info['message_id']].copy()
            continue
        return
    
    # async def store(self, key, value) :
    #     await self.channel.send('{key}{delim}{value}'.format(key = key, value = value, delim = self.split_delim))
    #     return
    
    async def fetch_all(self) :
        return self.data.copy()
    
    async def fetch_results(self, search_values) :
        # ## OLD CODE
        # # sample = [row async for row in self.channel.history(limit = None) if row.author == self.perm_db.client and row.content.startswith('{key}{delim}'.format(key = key, delim = self.split_delim))]
        
        # # EXPLANATION OF ARGS -:
        # # SEARCH_VALUES KWARGS WILL TAKE IN KEYS TO SEARCH FOR AS ARGUMENTS.
        # data = []
        # async for row_message_object in self.channel.history(limit = lim) :
        #     row = row_message_object.content
        #     row_sample = row.split(self.split_delim)
        #     row_data = {row_sample[k] : row_sample[(k + 1)] for k in range(0, len(row_sample), 2)}
        #     flag = False
        #     for value in search_values :
        #         if value not in list(row_data.keys()) : break
        #         if row_data[value] == search_values[value] :
        #             flag = True
        #             continue
        #         else :
        #             flag = False
        #             break
        #         pass
        #     if flag :
        #         message_id = row_message_object.id
        #         row_info = {'row_data' : row_data, 'message_id' : message_id}
        #         data.append(row_info)
        #     continue
        
        # new code, once done, comment the old one
        filtered_data = []
        for row_info in self.data :
            row_data = row_info['row_data']
            flag = False
            for value in search_values :
                if value not in list(row_data.keys()) : break
                if row_data[value] == search_values[value] :
                    flag = True
                    continue
                else :
                    flag = False
                    break
                pass
            if flag :
                filtered_data.append(row_info)
            continue
        return filtered_data
    
    def fetch_row(self, msg_id) :
        return [k for k in self.data if k['message_id'] == msg_id][0]
    
    # async def fetch_results(self, key) :
    #     data = [row async for row in self.channel.history(limit = None) if row.author == self.perm_db.client and row.content.startswith('{key}{delim}'.format(key = key, delim = self.split_delim))]
    #     return data
    
    pass

class NonUniformBranch() :
    # Keys may differ for every row.
    def __init__(self, perm_db, channel) :
        self.channel = channel
        self.data = []
        self.name = self.channel.name
        self.perm_db = perm_db
        self.split_delim = ' [:|=|:] '
        self.setted_up = False
        return
    
    async def setup(self) :
        await self.refresh()
        self.setted_up = True
        return
    
    async def refresh(self) :
        self.data = []
        async for row_message_object in self.channel.history(limit = None) :
            # row = row_message_object.content
            # message_id = row_message_object.id
            # row_sample = row.split(self.split_delim)
            # row_data = {row_sample[k] : row_sample[(k + 1)] for k in range(0, len(row_sample), 2)}
            row_info = decrypt_data(row_message_object, self.split_delim)
            self.data.append(row_info)
        return
    
    async def store(self, values) :
        # Values should be a dictionary with {key : value} format for storage.
        storage_str = self.split_delim.join([k + self.split_delim + values[k] for k in values])
        message = await self.channel.send(storage_str)
        row_info = {'row_data' : copy.deepcopy(values), 'message_id' : message.id}
        self.data.append(row_info)
        return row_info
    
    async def modify(self, search_values, modif_values) :
        filtered_data = await self.fetch_results(search_values)
        for info in filtered_data :
            try :
                new_values = copy.deepcopy(info['row_data'])
                msg_id = info['message_id']
                index = self.data.index(info)
                for k in modif_values :
                    new_values[k] = modif_values[k]
                    self.data[index]['row_data'][k] = copy.deepcopy(modif_values[k])
                    continue
                message = await self.channel.fetch_message(msg_id)
                storage_str = self.split_delim.join([k + self.split_delim + new_values[k] for k in new_values])
                await message.edit(content = storage_str)
                continue
            except :
                print('Row has been deleted/doesn\'t exist anymore or couldn\'t be retrieved[Try again, since the internal cache might not have been refreshed.]')
                return None
        return
    
    async def delete(self, search_values) :
        filtered_data = await self.fetch_results(search_values)
        for info in filtered_data :
            message = await self.channel.fetch_message(info['message_id'])
            await message.delete()
            self.data = [copy.deepcopy(k) for k in self.data.copy() if k['message_id'] != info['message_id']].copy()
            continue
        return
    
    # async def store(self, key, value) :
    #     await self.channel.send('{key}{delim}{value}'.format(key = key, value = value, delim = self.split_delim))
    #     return
    
    async def fetch_all(self) :
        return self.data.copy()
    
    async def fetch_results(self, search_values) :
        # ## OLD CODE
        # # sample = [row async for row in self.channel.history(limit = None) if row.author == self.perm_db.client and row.content.startswith('{key}{delim}'.format(key = key, delim = self.split_delim))]
        
        # # EXPLANATION OF ARGS -:
        # # SEARCH_VALUES KWARGS WILL TAKE IN KEYS TO SEARCH FOR AS ARGUMENTS.
        # data = []
        # async for row_message_object in self.channel.history(limit = lim) :
        #     row = row_message_object.content
        #     row_sample = row.split(self.split_delim)
        #     row_data = {row_sample[k] : row_sample[(k + 1)] for k in range(0, len(row_sample), 2)}
        #     flag = False
        #     for value in search_values :
        #         if value not in list(row_data.keys()) : break
        #         if row_data[value] == search_values[value] :
        #             flag = True
        #             continue
        #         else :
        #             flag = False
        #             break
        #         pass
        #     if flag :
        #         message_id = row_message_object.id
        #         row_info = {'row_data' : row_data, 'message_id' : message_id}
        #         data.append(row_info)
        #     continue
        
        # new code, once done, comment the old one
        filtered_data = []
        for row_info in self.data :
            row_data = row_info['row_data']
            flag = False
            for value in search_values :
                if value not in list(row_data.keys()) : break
                if row_data[value] == search_values[value] :
                    flag = True
                    continue
                else :
                    flag = False
                    break
                pass
            if flag :
                filtered_data.append(row_info)
            continue
        return filtered_data
    
    def fetch_row(self, msg_id) :
        return [k for k in self.data if k['message_id'] == msg_id][0]
    
    # async def fetch_results(self, key) :
    #     data = [row async for row in self.channel.history(limit = None) if row.author == self.perm_db.client and row.content.startswith('{key}{delim}'.format(key = key, delim = self.split_delim))]
    #     return data
    
    pass

class PermanentDatabase() :
    def __init__(self, client, serv_id, dump_category = 'BOWBOTDB') :
        self.client = client
        self.serv_id = serv_id
        
        if self.serv_id not in [serv.id for serv in self.client.guilds] : 
            print('ERROR: The client is not a part of the guild(the id of which has been given.)')
            return
        self.server = self.client.get_guild(self.serv_id)
        
        self.dump_category = dump_category
        # print(self.server.name, self.server.categories)
        try :
            self.storage_category = [category for category in self.server.categories if category.name == self.dump_category][0]
            self.load_info()
        except Exception as e :
            print('STORAGE CATEGORY INITIALIZATION DIDNT WORK[{0}]'.format(e))
            self.branches, self.branch_names = [], []
        return
    
    def set_serv_id(self, serv_id) : self.serv_id = serv_id
    
    async def set_dump_category(self, dump_category) :
        # dump_category is a STRING.
        self.dump_category = dump_category
        if len([category for category in self.server.categories if category.name == self.dump_category]) == 0 :
            try :
                print('creating category')
                self.storage_category = await self.server.create_category_channel(name = self.dump_category)
            except Exception as e :
                print('failed to create category[{0}]'.format(e))
        else :
            self.storage_category = [category for category in self.server.categories if category.name == self.dump_category][0]
        return
    
    def load_info(self) :
        self.branches = [Branch(self, channel) for channel in self.storage_category.channels]
        self.branch_names = [branch.name for branch in self.branches]
        pass
    
    async def get_branch(self, name) :
        branch = [branch for branch in self.branches if branch.name == name][0]
        if not branch.setted_up : await branch.setup()
        return branch
    
    async def create_branch(self, name) :
        self.load_info()
        if name not in self.branch_names :
            if self.dump_category not in [category.name for category in self.server.categories] :
                self.storage_category = await self.server.create_category_channel(self.dump_category)
            channel = await self.server.create_text_channel(name, category = self.storage_category)
            branch = Branch(self, channel)
            self.load_info()
            await branch.setup()
            return branch
        else :
            print('The branch requested for creation already exists.' + name)
    
    def print_info(self) :
        print('Perm DB \n\nServer ID:{server_id}\nBranches:{branches}\n\n'.format(server_id = self.serv_id, branches = self.branch_names))
        return
    
    pass

class GlobalDatabase(PermanentDatabase) :
    def __init__(self, client) :
        super().__init__(client = client, serv_id = 1058974341670375535, dump_category = 'GLOBALBOWBOTDB')
        
        # self.client = client
        # self.serv_id = 1058974341670375535
        # self.server = self.client.get_guild(self.serv_id)
        # print(self.server, self.server.name)
        # self.dump_category = 'BOWBOTDB'
        # self.storage_category = [category for category in self.server.categories if category.name == self.dump_category][0]
        # self.load_info()
        return
    
    # ...
    
    pass


# ...create temporary database class.