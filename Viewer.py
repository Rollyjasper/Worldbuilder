
from pathlib import Path
import math
import os
import tkinter as tk
import tkinter.filedialog as tk_file
import json
import list_obj

class Core():
    def __init__(self):
        self.root = os.getcwd()
        self.path = '\\data'

        self.vehicle_cat = [
            'Basic_Info',
            'AuxCraft_Loadout',
            'Crew_Loadout',
            'Description',
            'Shield_Loadout',
            'System_Loadout',
            'Weapon_Loadout',
            'In_Service',
            'Roles',
        ]
    
    def folders(self):
        f = sorted(os.listdir(self.root + self.path))
        files = []
        for file in f:
            if file == '__pycache__':
                continue
            elif '.' in file:
                continue
            else:
                files.append(file)
        return files
    
    def docs(self):
        f = sorted(os.listdir(self.root + self.path))
        files = []
        for file in f:
            if not '.' in file:
                continue
            else:
                files.append(file)
        return files
    
    def down_lv(self,dir):
        self.path += '\\'+dir
    
    def up_lv(self):
        path = self.path.split('\\')[1:-1]
        new_path = ''
        for dir in path:
            new_path += '\\'+dir
        self.path = new_path

    def load_doc(self,doc):
        cat,doc_type = doc.split('.')
        if doc_type == 'json':
            with open('{}{}\\{}'.format(self.root,self.path,doc),'r') as file:
                data = json.load(file)
        return data,cat
    
    def save_doc(self,data,cat):
        with open('{}{}\\{}.json'.format(self.root,self.path,cat),'w') as loc:
            data_str = json.dump(data,loc,indent=4)
    
    def load_vehicle(self,name:str):
        name_breakdown = name.split('_')
        self.down_lv(name)
        docs = {}
        for cat in self.vehicle_cat:
            data = self.load_doc(cat+'.json')[0]
            docs[cat] = data
        
        vehicle = Vehicle(docs)
        self.up_lv()
        return vehicle

    def save_vehicle(self,vehicle:object):
        data = vehicle.data

        name = vehicle.get_name()

        split_path = self.path.split('\\')
        path = self.path

        if len(split_path) == 3:
            vec_type = int(vehicle.class_type)
            if vec_type <=299:
                path += '\\'+'001-299 Spacecraft'
            elif vec_type <=399:
                path += '\\'+'301-399 Landcraft'
            elif vec_type <=499:
                path += '\\'+'401-499 Aircraft'
            elif vec_type <=699:
                path += '\\'+'501-699 Watercraft'
            elif vec_type <=799:
                path += '\\'+'701-799 Instillations'
        
        if len(split_path) <= 4:
            vec_type = vehicle.class_type
            vec_type_name = vehicle.class_type_name
            path += '\\{}-{}'.format(vec_type,vec_type_name)

        Path(self.root+path+'\\'+name).mkdir(parents=True,exist_ok=True)

        temp = self.path

        self.path = path

        self.down_lv(name)

        for cat in self.vehicle_cat:
            self.save_doc(data[cat],cat)

        self.up_lv()

        self.path = temp
    
    def create_vehicle_types(self):
        types = self.get_lore('Tech\\Vehicle\\Types')
        for num,name in types.items():
            type_id = int(num)
            path = '\\data\\Vehicle'
            if type_id <=299:
                path += '\\'+'001-299 Spacecraft'
            elif type_id <=399:
                path += '\\'+'301-399 Landcraft'
            elif type_id <=499:
                path += '\\'+'401-499 Aircraft'
            elif type_id <=699:
                path += '\\'+'501-699 Watercraft'
            elif type_id <=799:
                path += '\\'+'701-799 Instillations'
            
            dir_name = '{}-{}'.format(num,name.replace(' ','_'))
            Path(self.root+path+'\\'+dir_name).mkdir(parents=True,exist_ok=True)

    def get_lore(self,file):
        path = '\\data\\Lore\\'+file
        with open(self.root+path+'.json','r') as f:
                data = json.load(f)
        return data
    
    def get_vehicle_list(self,type_id:tuple):
        path = '\\data\\Vehicle'
        if int(type_id[0]) < 300:
            path += '\\001-299 Spacecraft'
        elif int(type_id[0]) < 400:
            path += '\\301-399 Landcraft'
        elif int(type_id[0]) < 500:
            path += '\\401-499 Aircraft'
        elif int(type_id[0]) < 700:
            path += '\\501-699 Watercraft'
        elif int(type_id[0]) < 800:
            path += '\\701-799 Instillations'
        
        path += '\\{}-{}'.format(*type_id).replace(' ','_')

        craft = os.listdir(self.root + path)
        return craft
    
    def load_template(self,flag):
        if flag == 'Vehicle':
            path = '\\data\\Lore\\Templates\\000-Template\\'
            docs = {}
            for cat in self.vehicle_cat:
                with open(self.root+path+cat+'.json','r') as file:
                    data = json.load(file)
                docs[cat] = data
            return docs
    
    def get_structure(self,data):
        structure = {}
        for key,value in data.items():
            if isinstance(value,list):
                structure[key] = 'list'
            elif isinstance(value,dict):
                if value != {}:
                    ishead = True
                else:
                    ishead = False
                for v in value.values():
                    if not isinstance(v,dict):
                        ishead = False
                        break
                
                if ishead == True:
                    structure[key] = 'header'
                else:
                    structure[key] = 'section'
            else:
                structure[key] = 'attr'
        return structure

    def get_stats(self):
        ships_type,ships_gen,ships_core,ships_total,ship_names = self.stats_ships()

        ship_stats = {
            'ships_type':ships_type,
            'ships_gen':ships_gen,
            'ships_core':ships_core,
            'ships_total':ships_total,
            'ship_names':ship_names
        }
        return ship_stats

    def stats_ships(self):
        class_types = self.get_lore('Tech\\Vehicle\\Types')
        ships_type = {}
        ships_gen = {}
        ships_core = {}
        ships_total = 0
        ship_names = {}
        
        for num,name in class_types.items():
            type_id = int(num)
            path = '\\data\\Vehicle'
            if type_id <=299:
                path += '\\'+'001-299 Spacecraft'
            elif type_id <=399:
                path += '\\'+'301-399 Landcraft'
            elif type_id <=499:
                path += '\\'+'401-499 Aircraft'
            elif type_id <=699:
                path += '\\'+'501-699 Watercraft'
            elif type_id <=799:
                path += '\\'+'701-799 Instillations'
            
            path += '\\{}-{}'.format(num,name.replace(' ','_'))

            ship_classes = os.listdir(self.root+path)
            for ship in ship_classes:
                name = ship.split('_')
                gen = name[1]
                core = name[2]
                if gen in ships_gen:
                    ships_gen[gen] += 1
                else:
                    ships_gen[gen] = 1

                if core in ships_core:
                    ships_core[core] += 1
                else:
                    ships_core[core] = 1
                
                with open(self.root+path+'\\'+ship+'\\In_Service.json','r') as file:
                    names = json.load(file)['List']

                for name in names.values():
                    split_name = name.split('-')
                    if len(split_name) == 2:
                        if not split_name[0] in ship_names:
                            ship_names[split_name[0]] = [1,[ship]]
                        else:
                            if not ship in ship_names[split_name[0]][1]:
                                ship_names[split_name[0]][1].append(ship)
                                ship_names[split_name[0]][0] += 1

                    elif name in ship_names:
                        ship_names[name][1].append(ship)
                        ship_names[name][0] += 1
                    else:
                        ship_names[name] = [1,[ship]]

            ships_type[num] = len(ship_classes)
            ships_total += len(ship_classes)
        
        ship_names_copy = ship_names.copy()
        ship_names = {}
        ship_names = {key:ship_names_copy[key] for key in sorted(ship_names_copy)}
        
        return ships_type,ships_gen,ships_core,ships_total,ship_names

    def add_attr_vehicle(self,file,name,default_val,keys=[]):
        class_types = self.get_lore('Tech\\Vehicle\\Types')
        
        for num,_type in class_types.items():
            type_id = int(num)
            path = '\\data\\Vehicle'
            if type_id <=299:
                path += '\\'+'001-299 Spacecraft'
            elif type_id <=399:
                path += '\\'+'301-399 Landcraft'
            elif type_id <=499:
                path += '\\'+'401-499 Aircraft'
            elif type_id <=699:
                path += '\\'+'501-699 Watercraft'
            elif type_id <=799:
                path += '\\'+'701-799 Instillations'
            
            path += '\\{}-{}'.format(num,_type.replace(' ','_'))

            ship_classes = os.listdir(self.root+path)
            for vehicle in ship_classes:
                vehicle_path = path
                vehicle_path += '\\{}\\{}'.format(vehicle,file)

                with open(self.root+vehicle_path,'r') as f:
                    data = json.load(f)

                if len(keys) == 0:
                    data[name] = default_val
                elif len(keys) == 1:
                    data[keys[0]][name] = default_val

                with open(self.root+vehicle_path,'w') as f:
                    json.dump(data,f,indent=4)

    def get_crew_total(self,name,section,vehicle_class):
        path = '\\data\\Vehicle\\{}\\{}\\{}\\Crew_Loadout.json'.format(section,vehicle_class.replace(' ','_'),name)

        with open(self.root+path,'r') as file:
            data = json.load(file)
        
        return data['Totals']['Total std']

    def evershield_reset(self):
        class_types = self.get_lore('Tech\\Vehicle\\Types')
        evr_list = self.get_lore('Tech\\Defencive\\Evershield_Bay')
        
        for num,_type in class_types.items():
            type_id = int(num)
            path = '\\data\\Vehicle'
            if type_id <=299:
                path += '\\'+'001-299 Spacecraft'
            elif type_id <=399:
                path += '\\'+'301-399 Landcraft'
            elif type_id <=499:
                path += '\\'+'401-499 Aircraft'
            elif type_id <=699:
                path += '\\'+'501-699 Watercraft'
            elif type_id <=799:
                path += '\\'+'701-799 Instillations'
            
            path += '\\{}-{}'.format(num,_type.replace(' ','_'))

            self.path = path
            evrshld = evr_list[num]
            ship_classes = os.listdir(self.root+path)
            for vehicle in ship_classes:
                v = self.load_vehicle(vehicle)
                v.data['Shield_Loadout']['Ever-Shield']['Generation'] = evrshld['Generation']
                v.data['Shield_Loadout']['Ever-Shield']['Bay Size'] = evrshld['Size']
                v.data['Shield_Loadout']['Ever-Shield']['Bay Count'] = evrshld['Num']
                self.save_vehicle(v)

    def remove_name(self,ship,name,section):
        class_types = self.get_lore('Tech\\Vehicle\\Types')
        split_ship = ship.split('_')
        num = split_ship[0]
        order = split_ship[-2]
        vehicle_class = '{}-{}'.format(num,class_types[num].replace(' ','_'))
        path = '\\data\\Vehicle\\{}\\{}\\{}\\In_Service.json'.format(section,vehicle_class,ship)
        with open(self.root+path,'r') as file:
            in_serv = json.load(file)
        
        for reg,serv_name in in_serv['List'].items():
            if serv_name == name:
                break
        del in_serv['List'][reg]
        in_serv['Totals']['Commissioned'] -= 1
        in_serv['Totals']['Active'] -= 1

        fixed_ships = {}
        for i,(ship,name) in enumerate(in_serv['List'].items()):
            split_reg = ship.split('-')
            num = split_reg.pop(-1)
            if i < 9:
                expected = '{}0{}'.format(order,i+1)
            else:
                expected = '{}{}'.format(order,i+1)
            if expected != num:
                fix_reg = '{}-{}-{}-{}'.format(*split_reg,expected)
                ship = fix_reg

            fixed_ships[ship] = name
        
        in_serv['List'] = fixed_ships
        
        with open(self.root+path,'w') as file:
            json.dump(in_serv,file,indent=4)

class Vehicle(object):
    def __init__(self,data) -> None:
        self.class_name = data['Basic_Info']['Info']['Class Name']
        self.class_type = data['Basic_Info']['Info']['Class Type']
        self.class_type_name = data['Basic_Info']['Info']['Class Type Name']
        self.class_subtype = data['Basic_Info']['Info']['Class Sub-Type']
        self.generation = data['Basic_Info']['Info']['Generation']
        self.core_type = data['Basic_Info']['Info']['Core Type']
        self.order = data['Basic_Info']['Info']['Order']
        self.data = data
    
    def get_name(self):
        name = '{}_{}_{}_{}_{}'.format(self.class_type,self.generation,self.core_type,self.order,self.class_name)
        return name
    
    def get_registry(self):
        reg = '{}-{}-{}-{}XX'.format(self.class_type,self.generation,self.core_type,self.order)
        return reg

class FolderButton():
    def __init__(self,root,master,row,folder) -> None:
        self.root = root
        self.master = master
        self.row = row
        self.folder = folder

        self.button_width = 40

        self.show()
    
    def show(self):
        self.button = tk.Button(self.root,text = self.folder,width=self.button_width,command=self.on_click)
        self.button.grid(row=self.row)
    
    def on_click(self):
        self.master.core.down_lv(self.folder)
        self.master.reset_page()
        self.master.update()

class VehicleButton(FolderButton):
    def __init__(self, root, master, row, folder) -> None:
        super().__init__(root, master, row, folder)

        self.button.config(text=folder.replace('_','-'))

    def on_click(self):
        vehicle = self.master.core.load_vehicle(self.folder)
        self.master.current_vehicle = vehicle

        self.master.show_vehicle()

class LoreButton(FolderButton):
    def __init__(self, root, master, row, folder) -> None:
        super().__init__(root, master, row, folder)

        self.button.config(text=folder.split('.')[0].replace('_','-'))
    
    def on_click(self):
        folder_name = self.folder.split('.')[0]
        path = self.master.core.path.split('\\')[3:]
        lore_path = '{}\\{}\\{}'.format(*path,folder_name)
        lore = self.master.core.get_lore(lore_path)
        self.master.show_lore(lore,self.folder)
    
class Window():
    def __init__(self,root) -> None:
        self.root = root

        self.frame = tk.Frame(root)
        self.frame.grid()

        self.core = Core()

        self.current_vehicle = Vehicle(
            {
                'Basic_Info':{
                        'Info':{
                            "Class Name":"",
                            "Class Type":"",
                            "Class Type Name":"",
                            "Class Sub-Type":"",
                            "Generation":"",
                            "Core Type":"",
                            "Order":""
                        }
                }
            }
        )

        self.page_no = 0
        self.page_max = 0
        self.page_no_var = tk.IntVar(value=1)
        self.page_size = 15

        self.section = 'home'

        self.get_stats_on_click(False)

        self.start_page()
    
    def start_page(self):
        self.page_frame = tk.Frame(self.frame)
        self.page_frame.grid(row=1)

        self.lore_button = tk.Button(self.page_frame,text = 'Lore',width = 40,command=self.lore_on_click)
        self.lore_button.grid(row=0)

        self.vehicle_button = tk.Button(self.page_frame,text = 'Vehicles',width = 40,command=self.vehicles_on_click)
        self.vehicle_button.grid(row=1)

        self.stats_button = tk.Button(self.page_frame,text = 'Statistics',width = 40,command=self.stats_on_click)
        self.stats_button.grid(row=2)
    
    def static_page(self):
        self.static_frame = tk.LabelFrame(self.frame)
        self.static_frame.grid(row=0)

        self.home_button = tk.Button(self.static_frame,text='Home',width = 15,command=self.home_on_click)
        self.home_button.grid(row=0,column=3)

        self.reload_button = tk.Button(self.static_frame,text='Reload',width = 10,command=self.reload_on_click)
        self.reload_button.grid(row=0,column=1,columnspan=2)

        self.next_page_button = tk.Button(self.static_frame,text='--->',width = 15,command=self.next_page)
        self.next_page_button.grid(row=1,column=3)

        self.prev_page_button = tk.Button(self.static_frame,text='<---',width = 15,command=self.prev_page)
        self.prev_page_button.grid(row=1,column=0)

        self.page_no_label = tk.Label(self.static_frame,textvariable=self.page_no_var,width = 10)
        self.page_no_label.grid(row=1,column=1,columnspan=2)
        
        self.reset_page()

    def lore_on_click(self):
        self.lore_button.destroy()
        self.vehicle_button.destroy()
        self.stats_button.destroy()

        self.section = 'lore'
        self.core.down_lv('Lore')

        self.static_page()

        self.add_lore_button = tk.Button(self.static_frame,text = 'Add Lore',width = 15,command = self.add_lore_on_click)
        self.add_lore_button.grid(row=0,column=0)

        self.update()
    
    def vehicles_on_click(self):
        self.lore_button.destroy()
        self.vehicle_button.destroy()
        self.stats_button.destroy()

        self.section = 'vehicles'
        self.core.down_lv('Vehicle')

        self.static_page()

        self.add_vehicle_button = tk.Button(self.static_frame,text = 'Add Vehicle',width = 15,command = self.add_vehicle_on_click)
        self.add_vehicle_button.grid(row=0,column=0)

        self.update()
    
    def stats_on_click(self):
        self.lore_button.destroy()
        self.vehicle_button.destroy()
        self.stats_button.destroy()

        self.section = 'stats'
        
        self.stats_page()
    
    def stats_page(self):
        self.stat_frame = ScrollFrame(self.frame)
        self.stat_frame.grid(row=1)

        self.static_frame = tk.Frame(self.frame)
        self.static_frame.grid(row=0)

        self.home_button = tk.Button(self.static_frame,text='Home',width = 20,command=self.home_on_click)
        self.home_button.grid(row=0,column=1)

        self.get_stats_button = tk.Button(self.static_frame,text='Get Stats',width=20,command=self.get_stats_on_click)
        self.get_stats_button.grid(row=0,column=0)

        self.name_button = tk.Button(self.static_frame,text='Name De-duplicate',width=20,command=self.ship_name_dedup)
        self.name_button.grid(row=0,column=2)

        row = 0
        for sect,stat_sect in self.stats.items():
            title_label = tk.Label(self.stat_frame.frame,text=sect)
            title_label.grid(row=row)

            for i,(stat,values) in enumerate(stat_sect.items()):
                i+=1
                stats = stat.replace('_',' ').title()
                if isinstance(values,dict):
                    stat_sect_frame = tk.LabelFrame(self.stat_frame.frame,text=stats)
                    stat_sect_frame.grid(row=row+i)
                    for j,(k,v) in enumerate(values.items()):
                        if v == 0:
                            continue
                        elif stat == 'ship_names':
                            if v[0] >= 2:
                                stat_label = tk.Label(stat_sect_frame,text='{}: {}'.format(k,v))
                            else:
                                stat_label = tk.Label(stat_sect_frame,text='{}'.format(k))
                            stat_label.grid(row=j)
                        else:
                            stat_label = tk.Label(stat_sect_frame,text='{}: {}'.format(k,v))
                            stat_label.grid(row=j)
                else:
                    stat_label = tk.Label(self.stat_frame.frame,text='{}: {}'.format(stats,values))
                    stat_label.grid(row=row+i)
            
            row += i+1
        self.root.update()
        self.stat_frame.set_width()

    def page_draw(self):
        path = self.core.path.split('\\')
        if len(path) == 5:
            if self.section == 'vehicles':
                #docs
                files = self.core.folders()
                self.page_max == len(files)//self.page_size

                for i in range(self.page_size*self.page_no,self.page_size*(self.page_no+1)):
                    if i >= len(files):
                        break
                    
                    file = files[i]
                    button = VehicleButton(self.page_frame,self,i+1,file)
            elif self.section == 'lore':
                #lore
                files = self.core.docs()
                self.page_max == len(files)//self.page_size

                for i in range(self.page_size*self.page_no,self.page_size*(self.page_no+1)):
                    if i >= len(files):
                        break
                    
                    file = files[i]
                    button = LoreButton(self.page_frame,self,i+1,file)
        else:
            files = self.core.folders()
            self.page_max == len(files)//self.page_size

            for i in range(self.page_size*self.page_no,self.page_size*(self.page_no+1)):
                if i >= len(files):
                    break
                
                file = files[i]
                if file == 'Templates':
                    continue
                else:
                    button = FolderButton(self.page_frame,self,i+1,file)
            
        self.back_button = tk.Button(self.page_frame,text='Back',width=40,command=self.back_on_click)
        self.back_button.grid(row=0)
    
    def add_lore_on_click(self):
        win = tk.Toplevel(self.root)
        page = AddLoreWin(win,self.core)
    
    def add_vehicle_on_click(self):
        win = tk.Toplevel(self.root)
        page = AddVehicleWin(win,self.core)
    
    def get_stats_on_click(self,flag=True):
        self.stats = {}
        ship_stats = self.core.get_stats()
        self.stats['Ship'] = ship_stats

        self.reload_stats_page(flag)

    def home_on_click(self):
        self.frame.destroy()

        self.frame = tk.Frame(self.root)
        self.frame.grid()

        self.core.path = '\\data'

        self.current_vehicle = None

        self.page_no = 0
        self.page_no_var = tk.IntVar(value = self.page_no+1)

        self.section = 'home'

        self.start_page()
    
    def back_on_click(self):
        self.core.up_lv()
        path = self.core.path.split('\\')
        if len(path) == 2:
            self.home_on_click()
        else:
            self.reset_page()
            self.update()

    def reload_on_click(self):
        self.reset_page()
        self.update()

    def reload_stats_page(self,flag=None):
        if flag == True:
            self.stat_frame.destroy()
            self.static_frame.destroy()
            self.stats_page()

    def next_page(self):
        if self.page_no != self.page_max:
            self.page_no += 1
            self.page_no_var.set(self.page_no+1)
        self.update()
   
    def prev_page(self):
        if self.page_no != 0:
            self.page_no -= 1
            self.page_no_var.set(self.page_no+1)
        self.update()

    def page_check(self):
        if self.page_no == 0:
            self.prev_page_button.config(state='disabled')
        else:
            self.prev_page_button.config(state='active')

        if self.page_no == self.page_max:
            self.next_page_button.config(state='disabled')
        else:
            self.next_page_button.config(state='active')

    def page_clear(self):
        self.page_frame.destroy()
        self.page_frame = tk.Frame(self.frame)
        self.page_frame.grid(row=1)
    
    def page_info(self):
        files = self.core.folders()
        num = len(files)
        self.page_max = math.floor(num/self.page_size)
    
    def reset_page(self):
        self.page_no = 0
        self.page_no_var.set(1)
        self.page_info()
    
    def update(self):
        self.page_clear()
        self.page_check()
        self.page_draw()
    
    def show_vehicle(self):
        win = tk.Toplevel(self.root)
        page = VehicleWindow(win,self.current_vehicle,self.core)
    
    def show_lore(self,lore,filename):
        win = tk.Toplevel(self.root)
        page = LoreWindow(win,lore,self.core,filename)

    def ship_name_dedup(self):
        win = tk.Toplevel(self.root)
        app = NameDeDuper(win,self.core,self.stats['Ship']['ship_names'])

class AddVehicleWin():
    def __init__(self,root,core) -> None:
        self.root = root
        self.core = core

        self.frame = tk.Frame(self.root)
        self.frame.grid()
        
        self.static_frame = tk.Frame(self.frame)
        self.static_frame.grid(row=0)
        
        self.dynamic_frame = ScrollFrame(self.frame)
        self.dynamic_frame.grid(row=1)

        self.active_tab = 'Basic_Info'

        self.tab_list = []

        self.data= self.core.load_template('Vehicle')

        self.get_lists()

        self.set_init_basic_info()

        self.static()
        self.dynamic()
    
    def get_lists(self):
        self.vehicles_types = self.core.get_lore('Tech\\Vehicle\\Types')

        self.allowed_aux_list = self.core.get_lore('Tech\\Vehicle\\Allowed_Aux_Types')

        self.dropship_types = []
        for i in range(290,300,1):
            i = str(i)
            try:
                self.vehicles_types[i]
            except KeyError:
                continue
            else:
                name = '{}-{}'.format(i,self.vehicles_types[i])
                self.dropship_types.append(name)
                del self.vehicles_types[i]
        
        self.crew_types = self.core.get_lore('Social\\Employment\\Jobs')['Millitary']

        self.crew_multi = self.core.get_lore('Tech\\Vehicle\\Crew_Multi')

        self.chara_list = self.core.get_lore('Tech\\Vehicle\\Characteristics')['Dimentions']

        self.shld_list = self.core.get_lore('Tech\\Defencive\\Shields')
        self.hull_list = self.core.get_lore('Tech\\Defencive\\Hulls')
        self.evr_bay_list = self.core.get_lore('Tech\\Defencive\\Evershield_Bay')

        self.pwr_list = self.core.get_lore('Tech\\Auxillary\\Power_Core')
        self.comp_list = self.core.get_lore('Tech\\Auxillary\\Computer')
        self.prop_list = self.core.get_lore('Tech\\Auxillary\\Propultion')
        self.other_list = self.core.get_lore('Tech\\Auxillary\\Other')

        self.lightning_cannon_to_core = self.core.get_lore('Tech\\Auxillary\\Lcore_to_Lcannon')

        self.wep_list = {
            'Semi-Hardlight Beam Weapon':self.core.get_lore('Tech\\Offencive\\Weapon_Hardlight'),
            'Kinetic':self.core.get_lore('Tech\\Offencive\\Weapon_Kinetic'),
            'Torpedo':self.core.get_lore('Tech\\Offencive\\Weapon_Torpedo'),
            'Missile':self.core.get_lore('Tech\\Offencive\\Weapon_Missile'),
            'Bomb':self.core.get_lore('Tech\\Offencive\\Weapon_Bomb'),
            'Mine':self.core.get_lore('Tech\\Offencive\\Weapon_Mine'),
            'Point-Defence Cannon':self.core.get_lore('Tech\\Offencive\\Weapon_PDC'),
            'Lightning Cannon':self.core.get_lore('Tech\\Offencive\\Weapon_Lightning'),
            'Superweapon':self.core.get_lore('Tech\\Offencive\\Weapon_Superweapon'),
            'Other':self.core.get_lore('Tech\\Offencive\\Weapon_Other'),
        }

        self.hvy_wep_list = {}
        self.hvy_wep_list['Lightning Cannon'] = self.wep_list['Lightning Cannon']['Miscellaneous']
        self.hvy_wep_list['Massdrivers'] = self.wep_list['Kinetic']['Massdrivers']
        self.hvy_wep_list['Superweapon'] = self.wep_list['Superweapon']['Miscellaneous']
        self.hvy_wep_list['Railgun'] = {'Icechild':self.wep_list['Kinetic']['Ice Type Railgun']['Icechild']}
        del self.wep_list['Lightning Cannon']
        del self.wep_list['Kinetic']['Massdrivers']
        del self.wep_list['Superweapon']
        del self.wep_list['Kinetic']['Ice Type Railgun']['Icechild']

        self.pdc_list = self.wep_list['Point-Defence Cannon']
        del self.wep_list['Point-Defence Cannon']

        self.wep_lim_keys = self.core.get_lore('Tech\\Offencive\\Weapon_Key')

        self.phaser_style_list = self.core.get_lore('Tech\\Offencive\\Phaser_Style')

        self.drone_bay_list = self.core.get_lore('Tech\\Offencive\\Drone_Bay')

        self.wep_locs_list = self.core.get_lore('Tech\\Offencive\\Locations')

        self.role_list = self.core.get_lore('Tech\\Vehicle\\Roles')

        self.core_list = self.core.get_lore('Tech\\Vehicle\\Core_Types')
        self.vehicle_subtype = self.core.get_lore('Tech\\Vehicle\\SubTypes')

        self.dropship_mounts = self.core.get_lore('Tech\\Auxillary\\Dropship_Mounts')
        self.dropship_name = self.core.get_lore('Tech\\Vehicle\\Dropship_Naming')

        self.range_const = self.core.get_lore('Tech\\Vehicle\\Class_Range_Const')

    def set_init_basic_info(self):
        loc = self.core.path.split('\\')
        if loc[-1] == '001-299 Spacecraft':
            self.class_type = '110'
            self.core_type = 'NX'
            self.class_type_name = 'Carrier'
        elif loc[-1] == '301-399 Landcraft':
            self.class_type = '301'
            self.core_type = 'XCV'
            self.class_type_name = 'Minerva1'
        elif loc[-1] == '401-499 Aircraft':
            self.class_type = '401'
            self.core_type = 'AAX'
            self.class_type_name = 'Interceptor'
        elif loc[-1] == '501-699 Watercraft':
            self.class_type = '501'
            self.core_type = 'XCN'
            self.class_type_name = 'Patrol_Corvette'
        elif loc[-1] == '701-799 Instillations':
            self.class_type = '701'
            self.core_type = 'Base'
            self.class_type_name = ''
        elif len(loc[-1].split(' ')) == 1 and loc[-1] != 'Vehicle':
            self.class_type = loc[-1].split('-')[0]
            self.class_type_name = loc[-1].split('-')[1]
            if loc[-2] == '001-299 Spacecraft':
                self.core_type = 'NX'
            elif loc[-2] == '301-399 Landcraft':
                self.core_type = 'XCV'
            elif loc[-2] == '401-499 Aircraft':
                self.core_type = 'AAX'
            elif loc[-2] == '501-699 Watercraft':
                self.core_type = 'XCN'
            elif loc[-2] == '701-799 Instillations':
                self.core_type = 'Base'

        else:
            self.class_type = '110'
            self.core_type = 'NX'
            self.class_type_name = 'Carrier'


        self.class_name = ''
        self.class_subtype = 'None'
        self.generation = '2'
        self.order = '0'

        self.data['Basic_Info']['Info']['Class Name'] = self.class_name
        self.data['Basic_Info']['Info']['Class Type'] = self.class_type
        self.data['Basic_Info']['Info']['Class Type Name'] = self.class_type_name
        self.data['Basic_Info']['Info']['Class Sub-Type'] = self.class_subtype
        self.data['Basic_Info']['Info']['Generation'] = self.generation
        self.data['Basic_Info']['Info']['Core Type'] = self.core_type
        self.data['Basic_Info']['Info']['Order'] = self.order

    def get_range(self):
        try:
            class_const = self.range_const[self.class_type]
            core_type = self.data['System_Loadout']['Power Core']['Primary_Type']
            core_const = self.pwr_list['Cores'][core_type]['Range Factor']
            FTL_type = self.data['System_Loadout']['Propultion']['FTL'][0][0].split(' ')
            if FTL_type[0] == 'Heavy':
                if FTL_type[1] == 'Long-range':
                    FTL_factor = 2.0
            elif FTL_type[0] == 'Long-range':
                FTL_factor = 1.5
            elif FTL_type[0] == 'Short-range':
                FTL_factor = 0.5
            elif FTL_type[0] == '' and int(self.class_type) <= 299:
                FTL_factor = 0.0
            else:
                FTL_factor = 1.0
        except KeyError:
            class_const,core_const,FTL_factor = (1,1,0)

        if int(self.class_type) <=299:
            base_range = 1000
            range_units = 'MPc'
        elif int(self.class_type) <=399:
            base_range = 1000
            range_units = 'Km'
        elif int(self.class_type) <=499:
            base_range = 50000
            range_units = 'Km'
        elif int(self.class_type) <=699:
            base_range = 10000
            range_units = 'Km'
        elif int(self.class_type) <=799:
            base_range = 0
            range_units = 'Km'
        
        vehicle_range = base_range*class_const*core_const*FTL_factor

        return [vehicle_range,range_units]

    def tab_re_colour(self,active):
        for tab in self.tab_list:
            if tab.tab == active:
                tab.button.config(bg=tab.active_colour)
            else:
                tab.button.config(bg=tab.base_colour)
    
    def save_on_click(self):
        self.data['Basic_Info']['Info']['Range'] = self.get_range()
        vehicle = Vehicle(self.data)
        self.core.save_vehicle(vehicle)
        self.back_on_click()

    def back_on_click(self):
        self.root.destroy()
    
    def static(self):
        for i,key in enumerate(self.core.vehicle_cat):
            self.tab_list.append(WinTabButton(self.static_frame,self,i,key))
        
        self.save_button = tk.Button(self.static_frame,text='Save Vehicle',width=16,bg= '#c1c1c1',command=self.save_on_click)
        self.save_button.grid(row=0,column=i+1)

        self.back_button = tk.Button(self.static_frame,text='Back',width=16,bg= '#c1c1c1',command=self.back_on_click)
        self.back_button.grid(row=0,column=i+2)

        self.tab_re_colour(self.active_tab)

    def dynamic(self):
        self.clear_dynamic()
        if self.active_tab == 'AuxCraft_Loadout':
            self.show_aux()
        elif self.active_tab == 'Crew_Loadout':
            self.show_crew()
        elif self.active_tab == 'Description':
            self.show_desc()
        elif self.active_tab == 'Shield_Loadout':
            self.show_shld()
        elif self.active_tab == 'System_Loadout':
            self.show_sys()
        elif self.active_tab == 'Weapon_Loadout':
            self.show_wep()
        elif self.active_tab == 'In_Service':
            self.show_serv()
        elif self.active_tab == 'Roles':
            self.show_role()
        elif self.active_tab == 'Basic_Info':
            self.show_basic()
    
    def clear_dynamic(self):
        self.dynamic_frame.destroy()
        self.data['Basic_Info']['Info']['Range'] = self.get_range()
        self.dynamic_frame = ScrollFrame(self.frame)
        self.dynamic_frame.grid(row=1)
    
    def show_aux(self):
        filtered_types = self.filter_aux_types()
        #Main        
        aux_type_var = tk.StringVar(value='Select Aux Craft Type')
        aux_type = tk.OptionMenu(self.dynamic_frame.frame,aux_type_var,*filtered_types,command=self.aux_on_select)
        aux_type.config(width=30)
        aux_type.grid(row=0,column=1)

        craft = []
        self.aux_craft_var = tk.StringVar(value='Select Aux Craft')
        aux_selection = tk.OptionMenu(self.dynamic_frame.frame,self.aux_craft_var,'Select Aux Craft',*craft)
        aux_selection.config(width=30)
        aux_selection.grid(row=0,column=2)

        aux_craft_no = tk.Entry(self.dynamic_frame.frame,width=25)
        aux_craft_no.grid(row=0,column=3)

        add_aux_button = tk.Button(
            self.dynamic_frame.frame,
            text = 'Add Auxillary Vehicle',
            command=lambda:self.add_aux_on_click(
                self.aux_craft_var.get(),
                int(aux_craft_no.get()),
                aux_type_var.get()
                )
            )
        add_aux_button.grid(row=0,column=0)

        self.aux_craft_frame = tk.LabelFrame(self.dynamic_frame.frame,text = 'Main')
        self.aux_craft_frame.grid(row=1,column=0,columnspan=4)

        aux_craft_list = []
        for i,(aux_craft,num) in enumerate(self.data['AuxCraft_Loadout']['Main'].items()):
            aux_craft_list.append(list_obj.AuxCraftLabel(self.aux_craft_frame,i,self,aux_craft,num))
        
        if filtered_types[0] == 'No Aux Craft':
            aux_type_var.set('No Aux Craft')
            aux_type.config(state='disabled')
            aux_selection.config(state='disabled')
            aux_craft_no.config(state='disabled')
            add_aux_button.config(state='disabled')
        
        
        #Dropship        
        self.drop_type_var = tk.StringVar(value='Select Dropship Type')
        drop_type = tk.OptionMenu(self.dynamic_frame.frame,self.drop_type_var,*self.dropship_types,command=self.drop_on_select)
        drop_type.config(width=30)
        drop_type.grid(row=2,column=2)

        self.drop_branch_var = tk.StringVar(value='Avingarde')
        drop_branch_menu = tk.OptionMenu(self.dynamic_frame.frame,self.drop_branch_var,*self.dropship_name['Branch'])
        drop_branch_menu.grid(row=2,column=1)


        mount = []
        self.mount_var = tk.StringVar(value='Select Mount')
        mount_selection = tk.OptionMenu(self.dynamic_frame.frame,self.mount_var,'Select Mount',*mount)
        mount_selection.config(width=30)
        mount_selection.grid(row=2,column=3)

        drop_craft_no = tk.Entry(self.dynamic_frame.frame,width=25)
        drop_craft_no.grid(row=2,column=4)

        add_drop_button = tk.Button(
            self.dynamic_frame.frame,
            text = 'Add Dropship',
            command=lambda:self.add_drop_on_click(
                int(drop_craft_no.get())
                )
            )
        add_drop_button.grid(row=2,column=0)

        self.drop_craft_frame = tk.LabelFrame(self.dynamic_frame.frame,text = 'Dropships')
        self.drop_craft_frame.grid(row=3,column=0,columnspan=4)

        drop_craft_list = []
        i = 0
        for drop_craft,mounts in self.data['AuxCraft_Loadout']['Dropships'].items():
            for mount,num in mounts:
                drop_craft_list.append(list_obj.DropshipLabel(self.drop_craft_frame,i,self,drop_craft,num,mount))
                i += 1
        
        notes_str = ''
        notes = self.data['AuxCraft_Loadout']['Notes']
        for i,line in notes.items():
            notes_str += line
            if int(i) != len(notes):
                notes_str += '\n'
        self.notes_box = tk.Text(self.dynamic_frame.frame,width=100,height=5,)
        self.notes_box.insert('insert',notes_str)
        self.notes_box.grid(row=4,column=0,columnspan=4)

        notes_button = tk.Button(self.dynamic_frame.frame,text = 'Save Notes',command=self.aux_save_notes)
        notes_button.grid(row=5,column=0,columnspan=4)

        self.root.update()
        self.dynamic_frame.set_width()

    def show_crew(self):
        #breakdown
        self.crew_vars = []
        for row,role in enumerate(self.crew_types):
            label = tk.Label(self.dynamic_frame.frame,text = role+':',width=15)
            label.grid(row=row,column=0)
            
            value = self.data['Crew_Loadout']['Breakdown'][role]
            var = tk.IntVar(value=value)

            entry = tk.Entry(self.dynamic_frame.frame,textvariable=var)
            entry.grid(row=row,column=1)

            self.crew_vars.append(var)
        
        save_button = tk.Button(self.dynamic_frame.frame,text='Save Crew Loadout',command=self.add_crew_on_click)
        save_button.grid(row=row+1,column=0,columnspan=2)

        crew_totals_frame = tk.LabelFrame(self.dynamic_frame.frame,text='Totals')
        crew_totals_frame.grid(row=row+2,column=0,columnspan=2)

        for row,(total,num) in enumerate(self.data['Crew_Loadout']['Totals'].items()):
            string = '{}: {}'.format(total,num)
            label = tk.Label(crew_totals_frame,text=string,width=15)
            label.grid(row=row)

        self.root.update()
        self.dynamic_frame.set_width()
    
    def show_desc(self):
        add_chara_button = tk.Button(self.dynamic_frame.frame,text='Add Measure',command=self.add_chara_on_click)
        add_chara_button.grid(row=0,column=0)

        self.add_chara_var = tk.StringVar(value='Dimention')
        add_chara_menu = tk.OptionMenu(self.dynamic_frame.frame,self.add_chara_var,*self.chara_list)
        add_chara_menu.grid(row=0,column=1)

        add_chara_label = tk.Label(self.dynamic_frame.frame,text = 'Value(s), seperate with comma\",\":')
        add_chara_label.grid(row = 0,column=2)

        self.add_chara_entry = tk.Entry(self.dynamic_frame.frame)
        self.add_chara_entry.grid(row=0,column=3)

        self.chara_frame = tk.LabelFrame(self.dynamic_frame.frame,text = 'Characteristics')
        self.chara_frame.grid(row=1,column=0,columnspan=4)

        chara_list = []
        for i,(chara,value) in enumerate(self.data['Description']['Characteristics'].items()):
            chara_list.append(list_obj.CharacteristicLabel(self.chara_frame,i,self,chara,value))

        desc_str = ''
        desc = self.data['Description']['Description']
        for i,line in desc.items():
            desc_str += line
            if int(i) != len(desc):
                desc_str += '\n'
        self.desc_box = tk.Text(self.dynamic_frame.frame,width=100,height=10,)
        self.desc_box.insert('insert',desc_str)
        self.desc_box.grid(row=2,column=0,columnspan=4)

        desc_button = tk.Button(self.dynamic_frame.frame,text = 'Save Description',command=self.desc_save)
        desc_button.grid(row=3,column=0,columnspan=4)

        self.root.update()
        self.dynamic_frame.set_width()
    
    def show_shld(self):
        std_shld = self.shld_list['Standard']
        evr_shld = self.shld_list['Ever-Shield']
        nav_shld = self.shld_list['Navigational']

        #Standard
        string_list = ['Primary','Secondary','Tertiary']
        obj_list = []
        for i in range(3):
            type_val = self.data['Shield_Loadout'][string_list[i]]['Type']
            subt_val = self.data['Shield_Loadout'][string_list[i]]['Sub-Type']
            vers_val = self.data['Shield_Loadout'][string_list[i]]['Version']
            obj_list.append(list_obj.ShldMenu(self.dynamic_frame.frame,2*i,self,type_val,subt_val,vers_val,string_list[i],std_shld))
        
        row = 2*i+1

        #Evershield
        evr_label = tk.Label(self.dynamic_frame.frame,text='Ever-Shield (Generation,Bay Size,Numer of Bays):')
        evr_label.grid(row=row+1,column=0,columnspan=4)

        self.evr_gen_var = tk.StringVar(value=self.data['Shield_Loadout']['Ever-Shield']['Generation'])
        evr_gen_menu = tk.OptionMenu(self.dynamic_frame.frame,self.evr_gen_var,*evr_shld['Generation'])
        evr_gen_menu.config(width=15)
        evr_gen_menu.grid(row=row+2,column=0)

        self.evr_size_var = tk.StringVar(value=self.data['Shield_Loadout']['Ever-Shield']['Bay Size'])
        evr_size_menu = tk.OptionMenu(self.dynamic_frame.frame,self.evr_size_var,*evr_shld['Bay Size'])
        evr_size_menu.config(width=15)
        evr_size_menu.grid(row=row+2,column=1)

        self.evr_count_var = tk.IntVar(value=self.data['Shield_Loadout']['Ever-Shield']['Bay Count'])
        evr_count = tk.Entry(self.dynamic_frame.frame,textvariable=self.evr_count_var,width=15)
        evr_count.grid(row=row+2,column=2)

        self.set_evershield()

        evr_button = tk.Button(self.dynamic_frame.frame,text='Save Ever-Shield',width=15,command=self.evr_on_click)
        evr_button.grid(row=row+2,column=3)

        #Nav
        nav_label = tk.Label(self.dynamic_frame.frame,text='Navigational Shield (Mount, Version):')
        nav_label.grid(row=row+3,column=0,columnspan=4)

        self.nav_mount_var = tk.StringVar(value=self.data['Shield_Loadout']['Navigational']['Mount'])
        nav_mount_menu = tk.OptionMenu(self.dynamic_frame.frame,self.nav_mount_var,*nav_shld['Mount'])
        nav_mount_menu.config(width=15)
        nav_mount_menu.grid(row=row+4,column=0)

        self.nav_vers_var = tk.StringVar(value=self.data['Shield_Loadout']['Navigational']['Version'])
        nav_vers_menu = tk.OptionMenu(self.dynamic_frame.frame,self.nav_vers_var,*nav_shld['Version'])
        nav_vers_menu.config(width=15)
        nav_vers_menu.grid(row=row+4,column=1)

        nav_button = tk.Button(self.dynamic_frame.frame,text='Save Navigational Shield',width=30,command=self.nav_on_click)
        nav_button.grid(row=row+4,column=2,columnspan=2)

        #Hull
        hull_label = tk.Label(self.dynamic_frame.frame,text='Hull Type:')
        hull_label.grid(row=row+5,column=0,columnspan=4)

        self.hull_type_var = tk.StringVar(value=self.data['Shield_Loadout']['Hull']['Type'])
        self.hull_type_menu = tk.OptionMenu(self.dynamic_frame.frame,self.hull_type_var,*self.hull_list,command=self.hull_type_on_select)
        self.hull_type_menu.config(width=15)
        self.hull_type_menu.grid(row=row+6,column=0,columnspan=4)
        
        #Notes
        notes_str = ''
        notes = self.data['Shield_Loadout']['Notes']
        for i,line in notes.items():
            notes_str += line
            if int(i) != len(notes):
                notes_str += '\n'
        self.notes_box = tk.Text(self.dynamic_frame.frame,width=100,height=5,)
        self.notes_box.insert('insert',notes_str)
        self.notes_box.grid(row=row+7,column=0,columnspan=4)

        notes_button = tk.Button(self.dynamic_frame.frame,text = 'Save Notes',command=self.shld_save_notes)
        notes_button.grid(row=row+8,column=0,columnspan=4)

        self.root.update()
        self.dynamic_frame.set_width()

    def show_sys(self):
        self.pwr_frame = tk.LabelFrame(self.dynamic_frame.frame,text='Power Core')
        self.pwr_frame.grid(row=0)
        self.prop_frame = tk.LabelFrame(self.dynamic_frame.frame,text='Propultion')
        self.prop_frame.grid(row=1)
        self.comp_frame = tk.LabelFrame(self.dynamic_frame.frame,text='Computer Core')
        self.comp_frame.grid(row=2)
        self.other_frame = tk.LabelFrame(self.dynamic_frame.frame,text='Other')
        self.other_frame.grid(row=3)

        #Power Core
        string_list = ['Primary','Secondary','Tertiary']
        obj_list = []
        added_lcore_info = False
        for i in range(3):
            type_val = self.data['System_Loadout']["Power Core"][string_list[i]+'_Type']
            style_val = self.data['System_Loadout']["Power Core"][string_list[i]+'_Style']
            vers_val = self.data['System_Loadout']["Power Core"][string_list[i]+'_Version']
            var_val = self.data['System_Loadout']["Power Core"][string_list[i]+'_Variation']
            if added_lcore_info == False and type_val == 'Lightning':
                try:
                    lightning_core_info_label = tk.Label(self.pwr_frame,
                        text='Current cannon with current lightning core: {}'.format(self.lightning_cannon_to_core[style_val])
                    )
                    lightning_core_info_label.grid(row=1,column=0,columnspan=4)
                    added_lcore_info = True
                except KeyError:
                    pass
            obj_list.append(list_obj.PwrMenu(self.pwr_frame,2*(i+1),self,type_val,vers_val,style_val,var_val,string_list[i]))

        #Propultion
        for i,form in enumerate(self.prop_list.keys()):
            drive_data = self.data['System_Loadout']['Propultion'][form]
            for j,prop in enumerate(drive_data):
                drive,count,mod = prop
                obj_list.append(list_obj.PropMenu(self.prop_frame,i,self,form,drive,mod,count,j))
        
        #Computer Core
        self.astr_var = tk.StringVar(value=self.data['System_Loadout']['Computer Core']['A.S.T.R'])
        self.ai_var = tk.StringVar(value=self.data['System_Loadout']['Computer Core']['AI'])
        self.core_var = tk.StringVar(value=self.data['System_Loadout']['Computer Core']['Main Type'])
        self.core_num_var = tk.IntVar(value=self.data['System_Loadout']['Computer Core']['Main Core Count'])

        core_label = tk.Label(self.comp_frame,text='Core Type:')
        core_label.grid(row = 0,column=0)

        core_menu = tk.OptionMenu(self.comp_frame,self.core_var,*self.comp_list['Core'])
        core_menu.config(width=25)
        core_menu.grid(row = 0,column=1)

        core_count_label = tk.Label(self.comp_frame,text='Number of Cores:')
        core_count_label.grid(row = 1,column=0)

        core_count_entry = tk.Entry(self.comp_frame,textvariable=self.core_num_var,width=5)
        core_count_entry.grid(row=1,column=1)

        ai_label = tk.Label(self.comp_frame,text='Highest AI:')
        ai_label.grid(row = 2,column=0)

        ai_menu = tk.OptionMenu(self.comp_frame,self.ai_var,*self.comp_list['AI'])
        ai_menu.config(width=25)
        ai_menu.grid(row = 2,column=1)

        astr_label = tk.Label(self.comp_frame,text='A.S.T.R.:')
        astr_label.grid(row = 3,column=0)

        astr_menu = tk.OptionMenu(self.comp_frame,self.astr_var,*self.comp_list['ASTR'])
        astr_menu.config(width=25)
        astr_menu.grid(row = 3,column=1)

        comp_save_button = tk.Button(self.comp_frame,text='Save Computer Core',width=25,command=self.comp_core_save)
        comp_save_button.grid(row=4,column=0,columnspan=2)

        #Other
        self.other_type_var = tk.StringVar(value='Select System Type')
        other_type = tk.OptionMenu(self.other_frame,self.other_type_var,*self.other_list.keys(),command=self.other_on_select)
        other_type.config(width=30)
        other_type.grid(row=0,column=1)

        other_sys = []
        self.system_var = tk.StringVar(value='Select System')
        sys_selection = tk.OptionMenu(self.other_frame,self.system_var,'Select System Craft',*other_sys)
        sys_selection.config(width=30)
        sys_selection.grid(row=0,column=2)

        num_entry = tk.Entry(self.other_frame,width=25)
        num_entry.grid(row=0,column=3)

        add_sys_button = tk.Button(
            self.other_frame,
            text = 'Add System',
            command=lambda:self.add_other_on_click(
                self.system_var.get(),
                int(num_entry.get())
                )
            )
        add_sys_button.grid(row=0,column=0)

        self.other_sys_frame = tk.LabelFrame(self.other_frame,text = 'Systems:')
        self.other_sys_frame.grid(row=1,column=0,columnspan=4)

        other_sys_list = []
        for i,(sys,num) in enumerate(self.data['System_Loadout']['Other'].items()):
            other_sys_list.append(list_obj.OtherSysLabel(self.other_sys_frame,i,self,sys,num))
        
        #Notes
        notes_str = ''
        notes = self.data['System_Loadout']['Notes']
        for i,line in notes.items():
            notes_str += line
            if int(i) != len(notes):
                notes_str += '\n'
        self.notes_box = tk.Text(self.dynamic_frame.frame,width=100,height=5,)
        self.notes_box.insert('insert',notes_str)
        self.notes_box.grid(row=4,column=0)

        notes_button = tk.Button(self.dynamic_frame.frame,text = 'Save Notes',command=self.sys_save_notes)
        notes_button.grid(row=5,column=0)

        self.root.update()
        self.dynamic_frame.set_width()

    def show_wep(self):
        #Create weapon frames
        pri_frame = tk.LabelFrame(self.dynamic_frame.frame,text='Primary Weapons:')
        pri_frame.grid(row=0,column=0)
        sec_frame = tk.LabelFrame(self.dynamic_frame.frame,text='Secondary Weapons:')
        sec_frame.grid(row=1,column=0)
        hvy_frame = tk.LabelFrame(self.dynamic_frame.frame,text='Heavy Weapons:')
        hvy_frame.grid(row=2,column=0)
        pod_frame = tk.LabelFrame(self.dynamic_frame.frame,text='Pod Weapons:')
        pod_frame.grid(row=3,column=0)
        pdc_frame = tk.LabelFrame(self.dynamic_frame.frame,text='Point Defence Weapons:')
        pdc_frame.grid(row=4,column=0)
        drone_frame = tk.LabelFrame(self.dynamic_frame.frame,text='Drone Weapon:')
        drone_frame.grid(row=5,column=0)

        #get_locations
        if int(self.class_type) <=299:
            loc_key = 'Space'
            drone_loc = 'Internal'
        elif int(self.class_type) <=399:
            loc_key = 'Land'
            drone_loc = 'Body'
        elif int(self.class_type) <=499:
            loc_key = 'Air'
            drone_loc = 'Dorsal'
        elif int(self.class_type) <=699:
            loc_key = 'Water'
            drone_loc = 'Internal'
        elif int(self.class_type) <=799:
            loc_key = 'Static'
            drone_loc = 'Underground'

        #set Drone
        drone_bay_size = self.drone_bay_list[self.class_type]['Size']
        drone_bay_num = self.drone_bay_list[self.class_type]['Num']
        self.data['Weapon_Loadout']['Drone'][drone_bay_size] = [drone_bay_num,drone_loc]

        #show weapons
        wep_list = []
        levels = ['Primary','Secondary','Heavy','Pod','Point Defence Grid','Drone']
        self.add_wep_lv = levels.copy()
        self.add_wep_lv.remove('Pod')
        self.add_wep_lv.remove('Drone')
        frames = [pri_frame,sec_frame,hvy_frame,pod_frame,pdc_frame,drone_frame]
        for i,level in enumerate(levels):
            for j,(wep,val) in enumerate(self.data['Weapon_Loadout'][level].items()):
                wep_list.append(list_obj.WepLabel(frames[i],j,self,wep,val,level,self.wep_locs_list[loc_key]))
        
        #choose Weapons
        add_weapons_button = tk.Button(self.dynamic_frame.frame,text='Add Weapons',command=self.add_weapons_on_click)
        add_weapons_button.grid(row=6,column=0)
        
        #Notes
        notes_str = ''
        notes = self.data['Weapon_Loadout']['Notes']
        for i,line in notes.items():
            notes_str += line
            if int(i) != len(notes):
                notes_str += '\n'
        self.notes_box = tk.Text(self.dynamic_frame.frame,width=100,height=5,)
        self.notes_box.insert('insert',notes_str)
        self.notes_box.grid(row=7,column=0)

        notes_button = tk.Button(self.dynamic_frame.frame,text = 'Save Notes',command=self.wep_save_notes)
        notes_button.grid(row=8,column=0)

        self.root.update()
        self.dynamic_frame.set_width()
    
    def show_serv(self):
        name_frame = tk.LabelFrame(self.dynamic_frame.frame,text='In Service')
        name_frame.grid(row=0,column=0,columnspan=2)

        ships = self.data['In_Service']['List']
        fixed_ships = {}
        ship_list = []
        for i,(ship,name) in enumerate(ships.items()):
            ship = self.check_reg(i,ship)
            fixed_ships[ship] = name
            if len(ships) == i+1:
                last = True
            else:
                last = False

            ship_list.append(list_obj.ServLabel(name_frame,i,self,ship,name,last))
        
        self.data['In_Service']['List'] = fixed_ships
        
        self.name_var = tk.StringVar()
        name_entry = tk.Entry(self.dynamic_frame.frame,textvariable=self.name_var)
        name_entry.grid(row=1,column=0)

        name_button = tk.Button(self.dynamic_frame.frame,text='Add Ship',command=self.save_ship)
        name_button.grid(row=1,column=1)
        
        self.ship_num_var = tk.IntVar()
        ship_num_entry = tk.Entry(self.dynamic_frame.frame,textvariable=self.ship_num_var)
        ship_num_entry.grid(row=2,column=0)

        ship_num_button = tk.Button(self.dynamic_frame.frame,text='Auto Add Ships',command=self.auto_ship)
        ship_num_button.grid(row=2,column=1)

        #Totals
        totals_frame = tk.LabelFrame(self.dynamic_frame.frame,text='Totals')
        totals_frame.grid(row=3,column=0,columnspan=2)

        self.comm_var = tk.IntVar(value=self.data['In_Service']['Totals']['Commissioned'])
        self.actv_var = tk.IntVar(value=self.data['In_Service']['Totals']['Active'])
        self.lost_var = tk.IntVar(value=self.data['In_Service']['Totals']['Lost'])
        self.decm_var = tk.IntVar(value=self.data['In_Service']['Totals']['Retired'])

        #Commissioned
        comm_label = tk.Label(totals_frame,text='Commissioned:')
        comm_label.grid(row=0,column=0)

        comm_entry = tk.Entry(totals_frame,textvariable=self.comm_var)
        comm_entry.grid(row=0,column=1)

        #Active
        actv_label = tk.Label(totals_frame,text='Active:')
        actv_label.grid(row=1,column=0)

        actv_entry = tk.Entry(totals_frame,textvariable=self.actv_var)
        actv_entry.grid(row=1,column=1)

        #Lost
        lost_label = tk.Label(totals_frame,text='Lost:')
        lost_label.grid(row=2,column=0)

        lost_entry = tk.Entry(totals_frame,textvariable=self.lost_var)
        lost_entry.grid(row=2,column=1)

        #Retired
        decm_label = tk.Label(totals_frame,text='Retired:')
        decm_label.grid(row=3,column=0)

        decm_entry = tk.Entry(totals_frame,textvariable=self.decm_var)
        decm_entry.grid(row=3,column=1)

        save_totals_button = tk.Button(totals_frame,text='Save Totals',width=15,command=self.save_service_total)
        save_totals_button.grid(row=4,column=0,columnspan=2)

        self.root.update()
        self.dynamic_frame.set_width()

    def show_role(self):
        self.role_var = tk.StringVar(value='Select Role')
        role_menu = tk.OptionMenu(self.dynamic_frame.frame,self.role_var,*self.role_list['Roles'],command=self.save_role)
        role_menu.config(width=20)
        role_menu.grid(row=0,column=0)

        self.role_lv_var = tk.IntVar(value=1)
        pri_role_button = tk.Radiobutton(self.dynamic_frame.frame,text="Primary",variable=self.role_lv_var,value=1)
        pri_role_button.grid(row=0,column=1)
        sec_role_button = tk.Radiobutton(self.dynamic_frame.frame,text="Secondary",variable=self.role_lv_var,value=2)
        sec_role_button.grid(row=0,column=2)

        pri_role_frame = tk.LabelFrame(self.dynamic_frame.frame,text = 'Primary')
        pri_role_frame.grid(row = 1,column=0,columnspan=3)
        sec_role_frame = tk.LabelFrame(self.dynamic_frame.frame,text = 'Secondary')
        sec_role_frame.grid(row = 2,column=0,columnspan=3)

        levels = ['Primary','Secondary']
        frames = [pri_role_frame,sec_role_frame]
        for i in range(2):
            level = levels[i]
            frame = frames[i]
            roles = self.data['Roles'][level]['Roles']
            for j,role in enumerate(roles):
                list_obj.RoleLabel(frame,j,self,role,level)

        self.root.update()
        self.dynamic_frame.set_width()

    def show_basic(self):
        self.class_name_var = tk.StringVar(value=self.class_name)
        self.class_type_var = tk.StringVar(value=self.class_type)
        self.class_type_name_var = tk.StringVar(value=self.class_type_name.replace('_',' '))
        self.class_subtype_var = tk.StringVar(value=self.class_subtype)
        self.class_gen_var = tk.StringVar(value=self.generation)
        self.class_core_var = tk.StringVar(value=self.core_type)
        self.class_order_var = tk.StringVar(value=self.order)

        filtered_types = self.filter_vehicle_types()

        #class name
        name_label = tk.Label(self.dynamic_frame.frame,text='Class Name:')
        name_label.grid(row=0,column=0)
        name_entry = tk.Entry(self.dynamic_frame.frame,textvariable=self.class_name_var)
        name_entry.grid(row=0,column=1)

        #class type
        type_label = tk.Label(self.dynamic_frame.frame,text='Class Type:')
        type_label.grid(row=1,column=0)
        type_menu = tk.OptionMenu(self.dynamic_frame.frame,self.class_type_var,*filtered_types,command=self.class_type_on_select)
        type_menu.grid(row=1,column=1)

        #class type name
        type_name_label = tk.Label(self.dynamic_frame.frame,text='Class Type(name):')
        type_name_label.grid(row=2,column=0)
        type_name_show = tk.Label(self.dynamic_frame.frame,textvariable=self.class_type_name_var)
        type_name_show.grid(row=2,column=1)

        #class subtype
        subtype_label = tk.Label(self.dynamic_frame.frame,text='Class Sub-Type:')
        subtype_label.grid(row=3,column=0)
        subtype_menu = tk.OptionMenu(self.dynamic_frame.frame,self.class_subtype_var,*self.vehicle_subtype)
        subtype_menu.grid(row=3,column=1)

        #generation
        gen_label = tk.Label(self.dynamic_frame.frame,text='Generation:')
        gen_label.grid(row=4,column=0)
        gen_entry = tk.Entry(self.dynamic_frame.frame,textvariable=self.class_gen_var)
        gen_entry.grid(row=4,column=1)

        #class subtype
        core_label = tk.Label(self.dynamic_frame.frame,text='Core Type:')
        core_label.grid(row=5,column=0)
        core_menu = tk.OptionMenu(self.dynamic_frame.frame,self.class_core_var,*self.core_list)
        core_menu.grid(row=5,column=1)

        #class name
        order_label = tk.Label(self.dynamic_frame.frame,text='Class Order:')
        order_label.grid(row=6,column=0)
        order_entry = tk.Entry(self.dynamic_frame.frame,textvariable=self.class_order_var)
        order_entry.grid(row=6,column=1)

        #Registration
        reg_label = tk.Label(self.dynamic_frame.frame,text='Ship Registration: {}-{}-{}-{}XX'.format(self.class_type,self.generation,self.core_type,self.order))
        reg_label.grid(row=7,column=0,columnspan=2)

        #Range
        rang_label = tk.Label(self.dynamic_frame.frame,text='Ship Range: {}{}'.format(*self.data['Basic_Info']['Info']['Range']))
        rang_label.grid(row=8,column=0,columnspan=2)

        #save button
        save_button = tk.Button(self.dynamic_frame.frame,text='Save',command=self.save_basic_info)
        save_button.grid(row=9,column=0,columnspan=2)

        self.root.update()
        self.dynamic_frame.set_width()

    #aux methods
    def add_aux_on_click(self,craft,num,class_type):
        type_id = int(craft.split('_')[0])
        if type_id <=299:
            sect = '001-299 Spacecraft'
        elif type_id <=399:
            sect = '301-399 Landcraft'
        elif type_id <=499:
            sect = '401-499 Aircraft'
        elif type_id <=699:
            sect = '501-699 Watercraft'
        elif type_id <=799:
            sect = '701-799 Instillations'
        crew = self.core.get_crew_total(craft,sect,class_type)
        self.data['AuxCraft_Loadout']['Main'][craft] = num
        self.data['Crew_Loadout']['Breakdown']['Pilots'] += crew*int(num)
        self.clear_dynamic()
        self.show_aux()
    
    def aux_on_select(self,val):
        type_id = val.split('-')
        craft = self.core.get_vehicle_list(type_id)
        self.aux_craft_var = tk.StringVar(value='Select Aux Craft')
        aux_selection = tk.OptionMenu(self.dynamic_frame.frame,self.aux_craft_var,*craft)
        aux_selection.config(width=30)
        aux_selection.grid(row=0,column=2)
    
    def add_drop_on_click(self,num):
        drop_type = self.drop_type_var.get().split('-')
        drop_class = drop_type[1].strip('Dropship').split(' ')[0]
        if drop_class == '':
            drop_class = 'Standard'
        
        if drop_class == 'Super':
            crew_count = 2
        else:
            crew_count = 1
        
        mount = self.mount_var.get()
        branch = self.drop_branch_var.get()

        drop_name = self.dropship_name['Branch'][branch]
        drop_suffix = self.dropship_name['Suffix'][drop_class]

        name = drop_name+drop_suffix
        if name in self.data['AuxCraft_Loadout']['Dropships']:
            self.data['AuxCraft_Loadout']['Dropships'][name].append([mount,num])
        else:
            self.data['AuxCraft_Loadout']['Dropships'][name] = [[mount,num]]
        self.data['Crew_Loadout']['Breakdown']['Pilots'] += crew_count*num
        self.clear_dynamic()
        self.show_aux()
    
    def drop_on_select(self,val):
        type_id = val.split('-')[0]
        drop_class = val.split('-')[1].strip('Dropship').split(' ')[0]
        if drop_class == '':
            drop_class = 'Standard'
        
        branch = self.drop_branch_var.get()

        mount = self.dropship_mounts[drop_class][branch]
        self.mount_var = tk.StringVar(value='Select Mount')
        mount_selection = tk.OptionMenu(self.dynamic_frame.frame,self.mount_var,*mount)
        mount_selection.config(width=30)
        mount_selection.grid(row=2,column=3)
    
    def aux_save_notes(self):
        notes_str = self.notes_box.get('1.0','end')
        notes = notes_str.split('\n')[0:-1]
        for i,note in enumerate(notes):
            i = str(i)
            self.data['AuxCraft_Loadout']['Notes'][i] = note
    
    def filter_aux_types(self):
        filtered_types = []
        if self.class_subtype == 'World Defender':
            allowed_types = [
                [110,289]
            ]
        elif self.allowed_aux_list[self.class_type] == []:
            return ['No Aux Craft']
        else:
            allowed_types = self.allowed_aux_list[self.class_type]
        for term in allowed_types:
            if isinstance(term,list):
                for i in range(term[0],term[1]+1):
                    try:
                        self.vehicles_types[str(i)]
                    except KeyError:
                        continue
                    else:
                        name = '{}-{}'.format(i,self.vehicles_types[str(i)])
                        filtered_types.append(name)
            elif isinstance(term,int):
                name = '{}-{}'.format(term,self.vehicles_types[str(term)])
                filtered_types.append(name)    

        return filtered_types

    #Crew Methods
    def add_crew_on_click(self):
        total_crew = 0
        for row,role in enumerate(self.crew_types):
            value = self.crew_vars[row].get()
            total_crew += value
            self.data['Crew_Loadout']['Breakdown'][role] = value

        self.data['Crew_Loadout']['Totals']["Total std"] = total_crew
        if self.data['Crew_Loadout']['Breakdown']["ArS NOVA"] >= 1:
            self.data['Crew_Loadout']['Totals']["Min Crew"] = self.data['Crew_Loadout']['Breakdown']["ArS NOVA"]
        else:
            self.data['Crew_Loadout']['Totals']["Min Crew"] = 0
        self.data['Crew_Loadout']['Totals']["Max Crew"] = math.floor(total_crew*self.crew_multi[self.class_type])
        self.clear_dynamic()
        self.show_crew()
    
    #Desc Methods
    def add_chara_on_click(self):
        item = self.add_chara_var.get()
        value = self.add_chara_entry.get().split(',')

        for i,val in enumerate(value):
            try:
                int(val)
            except ValueError:
                continue
            else:
                value[i] = int(val)
        
        self.data['Description']['Characteristics'][item] = value
        if item == 'Decks':
            if value[0]*4 > 2000:
                self.data['Description']['Characteristics']['Height'] = [(value[0]*4)/1000,'Km']
            else:
                self.data['Description']['Characteristics']['Height'] = [value[0]*4,'m']
        self.clear_dynamic()
        self.show_desc()

    def desc_save(self):
        desc_str = self.desc_box.get('1.0','end')
        desc = desc_str.split('\n')[0:-1]
        for i,line in enumerate(desc):
            i = str(i)
            self.data['Description']['Description'][i] = line

    #Shield Methods
    def evr_on_click(self):
        gen = self.evr_gen_var.get()
        size = self.evr_size_var.get()
        num = self.evr_count_var.get()

        try:
            gen = int(gen)
        except ValueError:
            pass

        self.data['Shield_Loadout']['Ever-Shield']['Generation'] = gen
        self.data['Shield_Loadout']['Ever-Shield']['Bay Size'] = size
        self.data['Shield_Loadout']['Ever-Shield']['Bay Count'] = num

        self.clear_dynamic()
        self.show_shld()

    def nav_on_click(self):
        mount = self.nav_mount_var.get()
        vers = self.nav_vers_var.get()

        try:
            vers = int(vers)
        except ValueError:
            pass

        self.data['Shield_Loadout']['Navigational']['Mount'] = mount
        self.data['Shield_Loadout']['Navigational']['Version'] = vers

        self.clear_dynamic()
        self.show_shld()
    
    def hull_type_on_select(self,val):
        self.data['Shield_Loadout']['Hull']['Type'] = val

        self.clear_dynamic()
        self.show_shld()
    
    def shld_save_notes(self):
        notes_str = self.notes_box.get('1.0','end')
        notes = notes_str.split('\n')[0:-1]
        for i,note in enumerate(notes):
            i = str(i)
            self.data['Shield_Loadout']['Notes'][i] = note

    def set_evershield(self):
        gen = self.evr_gen_var.get()
        bay = self.evr_size_var.get()
        count = self.evr_count_var.get()
        
        if self.class_type in range(0,300):
            if gen == '0':
                self.evr_gen_var.set(self.evr_bay_list[self.class_type]['Generation'])

            if bay == '':
                self.evr_size_var.set(self.evr_bay_list[self.class_type]['Size'])

            if count == 0:
                self.evr_count_var.set(self.evr_bay_list[self.class_type]['Num'])
            
            if gen == '0' or bay == '' or count == 0:
                self.evr_on_click()
        
    #System Methods
    def comp_core_save(self):
        self.data['System_Loadout']['Computer Core']['Main Type'] = self.core_var.get()
        self.data['System_Loadout']['Computer Core']['Main Core Count'] = self.core_num_var.get()
        self.data['System_Loadout']['Computer Core']['AI'] = self.ai_var.get()
        self.data['System_Loadout']['Computer Core']['A.S.T.R'] = self.astr_var.get()
        self.clear_dynamic()
        self.show_sys()

    def add_other_on_click(self,sys,num):
        sys_type = self.other_type_var.get()
        if sys_type == 'Other':
            name = '{}'.format(sys)
        else:
            name = '{} {}'.format(sys,sys_type)
        self.data['System_Loadout']['Other'][name] = num
        self.clear_dynamic()
        self.show_sys()
    
    def other_on_select(self,type_id):
        other_sys = self.other_list[type_id]
        self.system_var = tk.StringVar(value='Select System')
        sys_selection = tk.OptionMenu(self.other_frame,self.system_var,*other_sys)
        sys_selection.config(width=30)
        sys_selection.grid(row=0,column=2)
    
    def sys_save_notes(self):
        notes_str = self.notes_box.get('1.0','end')
        notes = notes_str.split('\n')[0:-1]
        for i,note in enumerate(notes):
            i = str(i)
            self.data['System_Loadout']['Notes'][i] = note
    
    #Weapon Methods
    def curate_wep(self,weapons):
        new_weapons = {}
        for weapon,detail in weapons.items():
            limits = detail['Limits']
            flag=False
            for limit in limits:
                ranges = list(self.wep_lim_keys[limit].values())
                for ran in ranges[0]:
                    r = list(range(ran[0],ran[1]+1))
                    if int(self.class_type) in r or (self.class_subtype == 'World Defender' and limit == 'S3'):
                        flag=True
            if flag == True:
                new_weapons[weapon] = detail
        return new_weapons

    def save_wep(self,level,weapon,num):
        self.data['Weapon_Loadout'][level][weapon] = num
        self.clear_dynamic()
        self.show_wep()
    
    def wep_save_notes(self):
        notes_str = self.notes_box.get('1.0','end')
        notes = notes_str.split('\n')[0:-1]
        for i,note in enumerate(notes):
            i = str(i)
            self.data['Weapon_Loadout']['Notes'][i] = note

    def add_weapons_on_click(self):
        win = tk.Toplevel(self.root)
        add_wep_app = AddWepWin(win,self,self.core)

    #In Service Methods
    def save_ship(self):
        name = self.name_var.get()
        num = len(self.data['In_Service']['List'])+1
        if num < 9:
            num = '0{}'.format(num)
        reg = '{}-{}-{}-{}{}'.format(self.class_type,self.generation,self.core_type,self.order,num)

        self.data['In_Service']['List'][reg] = name
        self.data['In_Service']['Totals']['Commissioned'] += 1
        self.data['In_Service']['Totals']['Active'] += 1
        self.clear_dynamic()
        self.show_serv()
    
    def auto_ship(self):
        num = self.ship_num_var.get()
        start = len(self.data['In_Service']['List'])
        for i in range(start,start+num):
            i += 1
            if i < 9:
                j = '0{}'.format(i)
            else:
                j = i
            reg = '{}-{}-{}-{}{}'.format(self.class_type,self.generation,self.core_type,self.order,j)
            name = '{}-{}'.format(self.class_name,i)

            self.data['In_Service']['List'][reg] = name

        self.data['In_Service']['Totals']['Commissioned'] += num
        self.data['In_Service']['Totals']['Active'] += num

        self.clear_dynamic()
        self.show_serv()
    
    def check_reg(self,i,reg):
        split_reg = reg.split('-')
        num = split_reg.pop(-1)
        if i < 9:
            expected = '{}0{}'.format(self.order,i+1)
        else:
            expected = '{}{}'.format(self.order,i+1)
        if expected != num:
            fix_reg = '{}-{}-{}-{}'.format(*split_reg,expected)
            return fix_reg
        else:
            return reg

    def save_service_total(self):
        self.data['In_Service']['Totals']['Commissioned'] = self.comm_var.get()
        self.data['In_Service']['Totals']['Active'] = self.actv_var.get()
        self.data['In_Service']['Totals']['Lost'] = self.lost_var.get()
        self.data['In_Service']['Totals']['Retired'] = self.decm_var.get()

        self.clear_dynamic()
        self.show_serv()
    
    #Role Methods
    def save_role(self,val):
        level = self.role_lv_var.get()
        if level == 1:
            self.data['Roles']['Primary']['Roles'].append(val)
        elif level == 2:
            self.data['Roles']['Secondary']['Roles'].append(val)
        self.clear_dynamic()
        self.show_role()

    #Basic info Methods
    def save_basic_info(self):
        self.class_name = self.class_name_var.get()
        self.class_type = self.class_type_var.get()
        self.class_type_name = self.class_type_name_var.get().replace(' ','_')
        self.class_subtype = self.class_subtype_var.get()
        self.generation = self.class_gen_var.get()
        self.core_type = self.class_core_var.get()
        self.order = self.class_order_var.get()

        if len(self.class_name.split(' ')) > 1:
            self.class_name = self.class_name.title()
            self.class_name = self.class_name.replace(' ','')

        self.data['Basic_Info']['Info']['Class Name'] = self.class_name
        self.data['Basic_Info']['Info']['Class Type'] = self.class_type
        self.data['Basic_Info']['Info']['Class Type Name'] = self.class_type_name
        self.data['Basic_Info']['Info']['Class Sub-Type'] = self.class_subtype
        self.data['Basic_Info']['Info']['Generation'] = self.generation
        self.data['Basic_Info']['Info']['Core Type'] = self.core_type
        self.data['Basic_Info']['Info']['Order'] = self.order

        self.clear_dynamic()
        self.show_basic()
    
    def class_type_on_select(self,val):
        name = self.vehicles_types[val]
        self.class_type_name_var.set(name)
    
    def filter_vehicle_types(self):
        filtered = []
        path = self.core.path.split('\\')
        path_len = len(path)
        for _type in self.vehicles_types:
            if path_len >= 4:
                str_range = path[3].split(' ')[0]
                range_param = str_range.split('-')
                if int(range_param[0]) <= int(_type) <= int(range_param[1]):
                    filtered.append(_type)
            else:
                filtered = self.vehicles_types
                break
        
        return filtered

class EditVehicleWin(AddVehicleWin):
    def __init__(self, root, core, data, parent) -> None:
        super().__init__(root, core)

        self.parent = parent
        self.data = data
        self.start_in_edit()
    
    def start_in_edit(self):
        self.class_name = self.data['Basic_Info']['Info']['Class Name']
        self.class_type = self.data['Basic_Info']['Info']['Class Type']
        self.class_type_name = self.data['Basic_Info']['Info']['Class Type Name']
        self.class_subtype = self.data['Basic_Info']['Info']['Class Sub-Type']
        self.generation = self.data['Basic_Info']['Info']['Generation']
        self.core_type = self.data['Basic_Info']['Info']['Core Type']
        self.order = self.data['Basic_Info']['Info']['Order']

        self.clear_dynamic()
        self.dynamic()
    
    def back_on_click(self):
        self.parent.destroy()

class AddLoreWin():
    def __init__(self,root,core):
        self.root = root
        self.core = core

        self.frame = tk.Frame(self.root)
        self.frame.grid()
        
        self.static_frame = tk.Frame(self.frame)
        self.static_frame.grid(row=0)
        
        self.dynamic_frame = ScrollFrame(self.frame)
        self.dynamic_frame.grid(row=1)

        self.lore = {}

        self.file_name = 'Untitled_Lore.json'

        self.static()
        self.dynamic()
    
    def save_on_click(self,file=None):
        new_lore = {}
        new_headers = {}
        new_sections = {}

        #headers
        for header in self.head_list:
            old_header_name = header.name
            header_name = header.save()
            new_lore[header_name] = {}
            new_headers[old_header_name] = header_name

        #sections
        for sect in self.sect_list:
            old_sect_name = sect.name
            sect_name = sect.save()
            sect_path = sect.path
            if len(sect_path) == 0:
                new_lore[sect_name] = {}
            elif len(sect_path) == 1:
                new_lore[new_headers[sect_path[0]]][sect_name] = {}
            new_sections[old_sect_name] = sect_name

        #lists
        for terms in self.list_list:
            list_name,list_terms = terms.save()
            list_path = terms.path
            if len(list_path) == 0:
                new_lore[list_name] = list_terms
            elif len(list_path) == 1:
                new_lore[new_sections[list_path[0]]][list_name] = list_terms
            elif len(list_path) == 2:
                new_lore[new_headers[list_path[0]]][new_sections[list_path[1]]][list_name] = list_terms

        #attributes
        for attr in self.attr_list:
            attr_name,attr_value = attr.save()
            attr_path = attr.path
            if len(attr_path) == 0:
                new_lore[attr_name] = attr_value
            elif len(attr_path) == 1:
                new_lore[new_sections[attr_path[0]]][attr_name] = attr_value
            elif len(attr_path) == 2:
                new_lore[new_headers[attr_path[0]]][new_sections[attr_path[1]]][attr_name] = attr_value
        
        self.lore = new_lore
        
        #save to file
        if file != None:
            json.dump(new_lore,file,indent=4)
        else:
            self.clear_dynamic()
            self.dynamic()

    def save_exit_on_click(self):
        save_file = tk_file.asksaveasfile('w',defaultextension='.json',initialdir=self.core.root+self.core.path,initialfile=self.file_name)
        self.save_on_click(save_file)
        self.back_on_click()

    def back_on_click(self):
        self.root.destroy()
    
    def clear_dynamic(self):
        self.dynamic_frame.destroy()
        self.dynamic_frame = ScrollFrame(self.frame)
        self.dynamic_frame.grid(row=1)

    def static(self):
        self.add_attr_button = tk.Button(self.static_frame,text='Add Attribute',width=25,bg= '#c1c1c1',command=self.add_attr)
        self.add_attr_button.grid(row=0,column=0)

        self.add_list_button = tk.Button(self.static_frame,text='Add List',width=25,bg= '#c1c1c1',command=self.add_list)
        self.add_list_button.grid(row=0,column=1)

        self.add_sect_button = tk.Button(self.static_frame,text='Add Section',width=25,bg= '#c1c1c1',command=self.add_section)
        self.add_sect_button.grid(row=0,column=2)

        self.add_head_button = tk.Button(self.static_frame,text='Add Header',width=25,bg= '#c1c1c1',command=self.add_header)
        self.add_head_button.grid(row=0,column=3)

        self.save_button = tk.Button(self.static_frame,text='Save Lore',width=25,bg= '#c1c1c1',command=self.save_on_click)
        self.save_button.grid(row=0,column=4)

        self.save_exit_button = tk.Button(self.static_frame,text='Save Lore And Exit',width=25,bg= '#c1c1c1',command=self.save_exit_on_click)
        self.save_exit_button.grid(row=0,column=5)

        self.back_button = tk.Button(self.static_frame,text='Back',width=25,bg= '#c1c1c1',command=self.back_on_click)
        self.back_button.grid(row=0,column=6)

    def dynamic(self):
        self.attr_list = []
        self.list_list = []
        self.sect_list = []
        self.head_list = []

        self.structure = self.core.get_structure(self.lore)

        frame = self.dynamic_frame.frame
        for row,(key,value) in enumerate(self.structure.items()):
            if value == 'attr':
                val = self.lore[key]
                if isinstance(val,int) or isinstance(val,float):
                    val_type = 'Num'
                else:
                    val_type = 'Txt'
                self.attr_list.append(list_obj.LoreAttrLabel(frame,row,self,key,val,val_type,[]))
            elif value == 'list':
                val = self.lore[key]
                if val == []:
                    val_type = 'Txt'
                elif isinstance(val[0],int) or isinstance(val[0],float):
                    val_type = 'Num'
                else:
                    val_type = 'Txt'
                self.list_list.append(list_obj.LoreListLabel(frame,row,self,key,val,val_type,[]))
            elif value == 'section':
                val = self.lore[key]
                self.show_section(key,val,frame,row,0,self.lore)
            elif value == 'header':
                val = self.lore[key]
                self.show_header(key,val,frame,row,0,self.lore)
        
        self.root.update()
        self.dynamic_frame.set_width()

    def show_section(self,attr,val,frame,row,column,data,path=None):
        sect_struc = self.core.get_structure(val)

        if path == None:
            path = []
            
        sect = list_obj.LoreSectLabel(frame,row,self,attr,path.copy(),len(sect_struc))
        sect_frame = sect.sect_frame
        self.sect_list.append(sect)

        path.append(attr)

        for sect_row,(key,value) in enumerate(sect_struc.items()):
            if value == 'attr':
                v = data[attr][key]
                if isinstance(v,int) or isinstance(v,float):
                    val_type = 'Num'
                else:
                    val_type = 'Txt'
                self.attr_list.append(list_obj.LoreAttrLabel(sect_frame,sect_row,self,key,v,val_type,path))
            elif value == 'list':
                v = data[attr][key]
                if v == []:
                    val_type = 'Txt'
                elif isinstance(v[0],int) or isinstance(v[0],float):
                    val_type = 'Num'
                else:
                    val_type = 'Txt'
                self.attr_list.append(list_obj.LoreListLabel(sect_frame,sect_row,self,key,v,val_type,path))
    
    def show_header(self,attr,val,frame,row,column,data):
        header = list_obj.LoreHeaderLabel(frame,row,self,attr,len(val))
        header_frame = header.head_frame
        self.head_list.append(header)

        for sect_row,(key,value) in enumerate(val.items()):
            self.show_section(key,value,header_frame,sect_row,0,data[attr],[attr])

    def add_attr(self):
        text = 'Add Attribute'
        win = tk.Toplevel(self.frame)
        pop_up = list_obj.AttrPopUp(win,text,self,[])

    def add_list(self):
        text = 'Add List'
        win = tk.Toplevel(self.frame)
        pop_up = list_obj.ListPopUp(win,text,self,[])

    def add_section(self):
        text = 'Add Section'
        win = tk.Toplevel(self.frame)
        pop_up = list_obj.SectionPopUp(win,text,self,[])

    def add_header(self):
        text = 'Add Header'
        win = tk.Toplevel(self.frame)
        pop_up = list_obj.HeaderPopUp(win,text,self,[])

class EditLoreWin(AddLoreWin):
    def __init__(self, root, core, data, parent, filename):
        super().__init__(root, core)

        self.parent = parent
        self.lore = data
        self.file_name = filename
        self.start_in_edit()
    
    def start_in_edit(self):
        self.root.title(self.file_name)
        self.clear_dynamic()
        self.dynamic()
    
    def back_on_click(self):
        self.parent.destroy()

class VehicleWindow():
    def __init__(self,root,vehicle,core) -> None:
        self.root = root
        self.core = core
        self.vehicle = vehicle

        self.data = vehicle.data

        self.frame = tk.Frame(self.root)
        self.frame.grid()
        
        self.static_frame = tk.Frame(self.frame)
        self.static_frame.grid(row=0)
        
        self.dynamic_frame = ScrollFrame(self.frame)
        self.dynamic_frame.grid(row=1)

        self.active_tab = 'Basic_Info'

        self.tab_list = []

        self.static()
        self.dynamic()
    
    def static(self):
        self.edit_button = tk.Button(self.static_frame,text='Edit Vehicle',width=16,bg= '#c1c1c1',command=self.edit_on_click)
        self.edit_button.grid(row=0,column=0)

        for i,key in enumerate(self.data):
            self.tab_list.append(WinTabButton(self.static_frame,self,i+1,key))
        
        self.back_button = tk.Button(self.static_frame,text='Back',width=16,bg= '#c1c1c1',command=self.back_on_click)
        self.back_button.grid(row=0,column=i+2)

        self.tab_re_colour(self.active_tab)

    def dynamic(self):
        tab_data = self.data[self.active_tab]

        header_row = 0
        
        self.dynamic_frame.destroy()
        self.dynamic_frame = ScrollFrame(self.frame)
        self.dynamic_frame.grid(row=1)
        
        for header,table in tab_data.items():
            header_label = tk.LabelFrame(self.dynamic_frame.frame,text=header)
            header_label.grid(row=header_row)
            row = 0

            if table=={}:
                if header[-1] != 's':
                    add_s = 's'
                else:
                    add_s = ''
                
                if header == 'Main':
                    sect = 'Aux Craft'
                    add_s = ''
                elif header == 'Breakdown':
                    sect = 'Crew'
                    add_s = ''
                elif header == 'Other':
                    sect = 'Other System'
                elif header in ['Primary','Secondary','Heavy']:
                    sect = '{} Weapon'.format(header)
                else:
                    sect = header
                    
                if header == 'List':
                    empty_table_str = 'There are no ships of this class in indipendent sesrvice.'
                else:
                    empty_table_str = 'There are no {}{} on this ship'.format(sect,add_s)
                empty_label = tk.Label(header_label,text=empty_table_str)
                empty_label.grid()
            
            for item,value in table.items():
                if header in ['Notes','Description']:
                    text = value
                elif header == 'Characteristics':
                    if len(value) == 2:
                        text = '{}: {}{}'.format(item,*value)
                    elif len(value) == 3:
                        text = '{}:\nPrimary: {}\nSecondary: {}\nTertiary: {}'.format(item,*value)
                    else:
                        text = '{}: {}'.format(item,*value)
                elif item == 'Roles':
                    string = ''
                    for role in value:
                        string += role+'\n'
                    text = string[0:-1]
                elif header == 'Dropships':
                    text = '{},{} Mount: {}'.format(item,value[0],value[1])
                elif header == 'Power Core':
                    if item in ['Primary_Type','Secondary_Type','Tertiary_Type']:
                        order = item.split('_')[0]
                        core_version = table[order+'_Version']
                        core_style = table[order+'_Style']
                        core_variation = table[order+'_Variation']
                        if core_style == None:
                            core_style = ''
                        if core_variation == None:
                            core_variation = ''
                        text = '{}: Type {} {} {} {} Core'.format(order,core_version,core_variation,core_style,value)
                    else:
                        continue
                elif header == 'Propultion':
                    prop_frame = tk.LabelFrame(header_label,text=item)
                    prop_frame.grid(row=row)
                    for i,engine in enumerate(value):
                        if engine != ['',0,'']:
                            if engine[2] == None:
                                text = '{0}:{1}'.format(*engine)
                            else:
                                text = '{2} {0}: {1}'.format(*engine)
                            engine_label = tk.Label(prop_frame,text = text)
                            engine_label.grid(row=i)
                elif header == 'Main':
                    text = '{}: {}'.format(item.replace('_','-'),value)
                elif header == 'Info' and self.active_tab == 'Basic_Info' and len(table)-1 == row:
                    text = '{}: {}{}'.format(item,*value)#range
                    reg_label = tk.Label(header_label,text='Ship Registration: '+self.vehicle.get_registry())
                    reg_label.grid(row=row+1)
                elif header == 'Hull' and item == 'Type':
                    text = '{}: {} Hull Panels'.format(item,value)
                elif item == 'Version':
                    text = '{}: Type-{}'.format(item,value)
                elif self.active_tab == 'Weapon_Loadout':
                    text = '{}: {}, {} Mount'.format(item,*value)
                else:
                    text = '{}: {}'.format(item,value)

                if value != 0 and value != None and value != [] and header != 'Propultion':
                    row_label = tk.Label(header_label,text=text,justify='left',anchor='w')
                    row_label.grid(row=row)
                    row += 1
                elif header == 'Propultion':
                    row += 1
            
            header_row += 1
        
        self.root.update()
        self.dynamic_frame.set_width()

    def tab_re_colour(self,active):
        for tab in self.tab_list:
            if tab.tab == active:
                tab.button.config(bg=tab.active_colour)
            else:
                tab.button.config(bg=tab.base_colour)

    def edit_on_click(self):
        win = tk.Toplevel(self.root)
        page = EditVehicleWin(win,self.core,self.data,self.root)

    def back_on_click(self):
        self.root.destroy()

class LoreWindow():
    def __init__(self,root,lore,core,filename):
        self.root = root
        self.lore = lore
        self.core = core
        self.filename = filename

        self.tab_row_limit = 5

        self.static_frame = tk.Frame(self.root)
        self.static_frame.grid(row=0)

        self.dynamic_frame = ScrollFrame(self.root)
        self.dynamic_frame.grid(row=1)

        self.structure = core.get_structure(lore)
        
        self.static()
        self.dynamic()
    
    def static(self):
        self.edit_button = tk.Button(self.static_frame,text='Edit Lore',width=16,bg= '#c1c1c1',command=self.edit_on_click)
        self.edit_button.grid(row=0,column=0)
        
        self.back_button = tk.Button(self.static_frame,text='Back',width=16,bg= '#c1c1c1',command=self.back_on_click)
        self.back_button.grid(row=0,column=1)

    def dynamic(self):
        frame = self.dynamic_frame.frame
        for row,(key,value) in enumerate(self.structure.items()):
            if value == 'attr':
                val = self.lore[key]
                self.show_attr(key,val,frame,row,0)
            elif value == 'list':
                val = self.lore[key]
                self.show_list(key,val,frame,row,0)
            elif value == 'section':
                val = self.lore[key]
                self.show_section(key,val,frame,row,0,self.lore)
            elif value == 'header':
                val = self.lore[key]
                self.show_header(key,val,frame,row,0,self.lore)
        
        self.root.update()
        self.dynamic_frame.set_width()

    def edit_on_click(self):
        win = tk.Toplevel(self.root)
        page = EditLoreWin(win,self.core,self.lore,self.root,self.filename)

    def back_on_click(self):
        self.root.destroy()

    def show_attr(self,attr,val,frame,row,column):
        label = tk.Label(frame,text='{}: {}'.format(attr,val))
        label.grid(row=row,column=column)

    def show_list(self,attr,val,frame,row,column):
        table_frame = tk.LabelFrame(frame,text=attr)
        table_frame.grid(row=row,column=column)

        for i,term in enumerate(val):
            label = tk.Label(table_frame,text=term)
            label.grid(row=i)

    def show_section(self,attr,val,frame,row,column,data):
        sect_struc = self.core.get_structure(val)

        struc_frame = tk.LabelFrame(frame,text=attr,bd=5,font=('Segoe UI',10))
        struc_frame.grid(row=row,column=column)

        for sect_row,(key,value) in enumerate(sect_struc.items()):
            if value == 'attr':
                v = data[attr][key]
                self.show_attr(key,v,struc_frame,sect_row,0)
            elif value == 'list':
                v = data[attr][key]
                self.show_list(key,v,struc_frame,sect_row,0)
    
    def show_header(self,attr,val,frame,row,column,data):
        header_frame = tk.LabelFrame(frame,text=attr,bd=8,labelanchor='n',font=('Segoe UI',14))
        header_frame.grid(row=row,column=column)

        for sect_row,(key,value) in enumerate(val.items()):
            self.show_section(key,value,header_frame,sect_row,0,data[attr])

class WinTabButton():
    def __init__(self,root,master,column,tab) -> None:
        self.root = root
        self.master = master
        self.column = column
        self.tab = tab
        self.text = tab.replace('_',' ')

        self.button_width = 16
        self.active_colour = '#818181'
        self.base_colour = '#a5a5a5'

        self.show()
    
    def show(self):
        self.button = tk.Button(self.root,text = self.text,width=self.button_width,command=self.on_click)
        self.button.grid(row=0,column=self.column)
    
    def on_click(self):
        self.master.tab_re_colour(self.tab)
        self.master.active_tab = self.tab
        self.master.dynamic()

class ScrollFrame(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.canvas = tk.Canvas(self, borderwidth=0,height=500)
        self.canvas.bind_all("<MouseWheel>", self.on_mousewheel)
        self.frame = tk.Frame(self.canvas)
        self.vsb = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vsb.set)

        self.vsb.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.create_window((4,4), window=self.frame, anchor="n",
                                  tags="self.frame")

        self.frame.bind("<Configure>", self.on_frame_configure)

    def on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
    
    def on_mousewheel(self, event):
        self.canvas.yview_scroll(-1*(event.delta//120), "units")
    
    def set_width(self):
        self.canvas.config(width=self.frame.grid_bbox()[2])

class AddWepWin():
    def __init__(self,root,master,core) -> None:
        self.root = root
        self.core = core
        self.master = master

        self.frame = tk.Frame(self.root)
        self.frame.grid()

        self.show()
    
    def show(self):
        #header
        self.title = tk.Label(self.frame,text='Add Weapon')
        self.title.grid(row=0,column=0)

        self.done_button = tk.Button(self.frame,text='Done',command=self.done_on_click)
        self.done_button.grid(row=7,column=0)
        
        #frames
        self.level_frame = tk.Frame(self.frame)
        self.level_frame.grid(row=1,column=0)

        self.type_frame = tk.Frame(self.frame)
        self.type_frame.grid(row=2,column=0)

        self.weapon_frame = tk.Frame(self.frame)
        self.weapon_frame.grid(row=3,column=0)

        self.sub_type_frame = tk.Frame(self.frame)
        self.sub_type_frame.grid(row=4,column=0)

        self.style_frame = tk.Frame(self.frame)
        self.style_frame.grid(row=5,column=0)

        self.count_frame = tk.Frame(self.frame)
        self.count_frame.grid(row=6,column=0)

        #vars
        self.pod_var = tk.BooleanVar(value=False)
        self.wep_lv_var = tk.StringVar(value='Weapon Level')
        self.wep_type_var = tk.StringVar(value='Weapon Type')
        self.wep_var = tk.StringVar(value='Weapon')
        self.sub_type_var = tk.StringVar(value='Subtype')
        self.wep_style_var = tk.StringVar(value='Style')
        self.count_var = tk.IntVar(value=0)

        self.phase_band = tk.StringVar(value='Band')
        self.phase_freq = tk.StringVar(value='Frequency')
        self.phase_colr = tk.StringVar(value='Colour')

        self.torp_face = tk.StringVar(value='Facing')
        self.torp_launcher = tk.StringVar(value='Launcher')

        #lists
        self.wep_lvl = self.master.add_wep_lv
        self.weapons = {
            'Primary':self.master.wep_list,
            'Secondary':self.master.wep_list,
            'Heavy':self.master.hvy_wep_list,
            'Point Defence Grid':self.master.pdc_list
        }

        self.select_level()

    def select_level(self):
        wep_lv_menu = tk.OptionMenu(self.level_frame,self.wep_lv_var,*self.wep_lvl,command=self.wep_lv_on_select)
        wep_lv_menu.config(width=30)
        wep_lv_menu.grid(row=0,column=0)

        pod_button = tk.Checkbutton(self.level_frame,text='Add to Pod?',variable=self.pod_var)
        pod_button.grid(row=0,column=1)
    
    def select_type(self,lvl):
        wep_type_menu = tk.OptionMenu(self.type_frame,self.wep_type_var,*self.weapons[lvl].keys(),command=lambda val:self.wep_type_on_select(val,lvl))
        wep_type_menu.config(width=30)
        wep_type_menu.grid(row=0,column=0)
    
    def select_weapon(self,lvl,wep_type):
        wep_menu = tk.OptionMenu(self.weapon_frame,self.wep_var,*self.weapon_list,command=lambda val:self.weapon_on_select(lvl,wep_type,val))
        wep_menu.config(width=30)
        wep_menu.grid(row=0,column=0)
    
    def select_sub_type(self,lvl,wep_type,wep):
        sub_type_list = self.master.curate_wep(self.weapon_list[wep])
        empty_text = 'This weapon cannot be used by this vehicle.'

        if sub_type_list != {}:
            wep_menu = tk.OptionMenu(self.sub_type_frame,self.sub_type_var,*sub_type_list,command=lambda val:self.sub_type_on_select(lvl,wep_type,wep,val))
            wep_menu.config(width=30)
            wep_menu.grid(row=0,column=0)
        else:
            label = tk.Label(self.sub_type_frame,text=empty_text)
            label.grid(row=0,column=0)
    
    def select_style(self,lvl,wep_type,wep,sub_type=None):
        if wep in ['Phaser','PHAS','Hazer']:
            band = self.master.phaser_style_list['Band']
            freq = self.master.phaser_style_list['Frequency']
            colour = self.master.phaser_style_list['Colour']

            band_menu = tk.OptionMenu(self.style_frame,self.phase_band,*band,command = self.phase_style_on_select)
            band_menu.config(width=20)
            band_menu.grid(row=0,column=0)

            freq_menu = tk.OptionMenu(self.style_frame,self.phase_freq,*freq,command = self.phase_style_on_select)
            freq_menu.config(width=20)
            freq_menu.grid(row=0,column=1)
            
            colour_menu = tk.OptionMenu(self.style_frame,self.phase_colr,*colour,command = self.phase_style_on_select)
            colour_menu.config(width=20)
            colour_menu.grid(row=0,column=2)
        elif wep_type == 'Torpedo':
            launchers = self.weapon_list[wep][sub_type]['Style']
            face = tk.OptionMenu(self.style_frame,self.torp_face,*['Fore','Aft'],command=self.torp_style_on_select)
            face.config(width=5)
            face.grid(row=0,column=0)

            launcher = tk.OptionMenu(self.style_frame,self.torp_launcher,*launchers,command=self.torp_style_on_select)
            launcher.config(width=25)
            launcher.grid(row=0,column=1)
        else:
            if sub_type == None:
                styles = self.weapon_list[wep]['Style']
            else:
                styles = self.weapon_list[wep][sub_type]['Style']
            wep_style = tk.OptionMenu(self.style_frame,self.wep_style_var,*styles)
            wep_style.config(width=30)
            wep_style.grid(row=0,column=0)

        self.select_count()

    def select_count(self):
        count_enter = tk.Entry(self.count_frame,textvariable=self.count_var)
        count_enter.grid(row=0,column=0)

        save_button = tk.Button(self.count_frame,text='Add Weapon',command=self.save_wep)
        save_button.grid(row=0,column=1)
    
    def wep_lv_on_select(self,lvl):
        self.reset_lower('lvl')
        self.select_type(lvl)
    
    def wep_type_on_select(self,wep_type,lvl):
        self.reset_lower('type')
        if lvl in ['Primary','Secondary']:
            self.weapon_list = self.weapons[lvl][wep_type]
        else:
            self.weapon_list = self.master.curate_wep(self.weapons[lvl][wep_type])

        self.select_weapon(lvl,wep_type)
    
    def weapon_on_select(self,lvl,wep_type,wep):
        self.reset_lower('wep')
        if lvl == 'Point Defence Grid':
            self.select_count()
        elif lvl == 'Heavy':
            if self.weapon_list[wep]['Style'] != []:
                self.select_style(lvl,wep_type,wep)
            else:
                self.select_count()
        else:
            self.select_sub_type(lvl,wep_type,wep)
    
    def sub_type_on_select(self,lvl,wep_type,wep,sub_type):
        self.reset_lower('stype')
        if not self.weapon_list[wep][sub_type]['Style'] == [] or wep in ['Phaser','PHAS','Hazer']:
            self.select_style(lvl,wep_type,wep,sub_type)
        else:
            self.select_count()
    
    def phase_style_on_select(self,val):
        band = self.phase_band.get()
        colour = self.phase_colr.get()
        freq = self.phase_freq.get()

        style = '{} Band {} Frequency {}'.format(band,freq,colour)

        self.wep_style_var.set(style)
    
    def torp_style_on_select(self,val):
        face = self.torp_face.get()
        laucher = self.torp_launcher.get()

        style = '{} {}'.format(face,laucher)

        self.wep_style_var.set(style)

    def save_wep(self):
        pod = self.pod_var.get()
        level = self.wep_lv_var.get()
        wep_type = self.wep_type_var.get()
        wep = self.wep_var.get()
        sub_type = self.sub_type_var.get()
        style = self.wep_style_var.get()
        number = self.count_var.get()

        if level == 'Point Defence Grid':
            weapon = '{} {}'.format(wep,wep_type)

        elif level == 'Heavy':
            if wep_type == 'Lightning Cannon' and not style in ['',' ','Style']:
                weapon = '{} {} {}'.format(wep,wep_type,style)
            elif wep_type == 'Railgun':
                weapon = '{} Railgun'.format(wep)
            else:
                weapon = '{}'.format(wep)

        elif level in ['Primary','Secondary']:
            if style in [' ','Style',None,'none','None']:
                style = ''
            if sub_type in ['Ocilating Type','Worldship Defence','ML-33 Mounted']:
                weapon = '{} {} {}'.format(style,sub_type,wep_type)
            elif wep_type in ['Torpedo','Missile','Bomb','Mine']:
                weapon = '{} {} {} {}'.format(style,sub_type,wep,wep_type)
            elif wep in ['Phaser','PHAS','Hazer']:
                weapon = '{} {} {}'.format(style,wep,sub_type)
            elif wep in ['Bar Type Railgun','Thunder Type Railgun','Fire Type Railgun','Ice Type Railgun','Composite Type Railgun'] or sub_type in ["MR-33 Mounted"]:
                weapon = '{} {} Railgun'.format(style,sub_type)
            elif wep_type == 'Other' or wep == 'Miscellaneous':
                weapon = '{} {}'.format(style,sub_type)
            else:
                weapon = '{} {} {}'.format(style,sub_type,wep)

        if pod == True:
            level = 'Pod'

        self.master.save_wep(level,weapon,number)
        self.reset_lower('all')
        self.select_level()
    
    def reset_lower(self,key):
        key = key.lower()
        if key in ['all']:
            self.reset_level()
            self.reset_type()
            self.reset_weapon()
            self.reset_sub_type()
            self.reset_style()
            self.reset_count()
        elif key in ['level','lvl','lv']:
            self.reset_type()
            self.reset_weapon()
            self.reset_sub_type()
            self.reset_style()
            self.reset_count()
        elif key in ['type']:
            self.reset_weapon()
            self.reset_sub_type()
            self.reset_style()
            self.reset_count()
        elif key in ['weapon','wep']:
            self.reset_sub_type()
            self.reset_style()
            self.reset_count()
        elif key in ['sub_type','subtype','sub type','stype']:
            self.reset_style()
            self.reset_count()
        elif key in ['style']:
            self.reset_count()

    def reset_level(self):
        self.level_frame.destroy()
        self.level_frame = tk.Frame(self.frame)
        self.level_frame.grid(row=1,column=0)

        self.wep_lv_var.set('Weapon Level')
        self.pod_var.set(False)

    def reset_type(self):
        self.type_frame.destroy()
        self.type_frame = tk.Frame(self.frame)
        self.type_frame.grid(row=2,column=0)

        self.wep_type_var.set('Weapon Type')

    def reset_weapon(self):
        self.weapon_frame.destroy()
        self.weapon_frame = tk.Frame(self.frame)
        self.weapon_frame.grid(row=3,column=0)

        self.wep_var.set('Weapon')

    def reset_sub_type(self):
        self.sub_type_frame.destroy()
        self.sub_type_frame = tk.Frame(self.frame)
        self.sub_type_frame.grid(row=4,column=0)

        self.sub_type_var.set('Subtype')

    def reset_style(self):
        self.style_frame.destroy()
        self.style_frame = tk.Frame(self.frame)
        self.style_frame.grid(row=5,column=0)

        self.wep_style_var.set('Style')

        self.phase_band.set('Band')
        self.phase_freq.set('Frequency')
        self.phase_colr.set('Colour')

        self.torp_face.set('Facing')
        self.torp_launcher.set('Launcher')

    def reset_count(self):
        self.count_frame.destroy()
        self.count_frame = tk.Frame(self.frame)
        self.count_frame.grid(row=6,column=0)

        if self.wep_lv_var.get() == 'Heavy':
            self.count_var.set(1)
        else:
            self.count_var.set(0)
    
    def done_on_click(self):
        self.root.destroy()

class NameDeDuper():
    def __init__(self,root,core,names) -> None:
        self.root = root
        self.core = core
        self.names = names

        self.frame = tk.Frame(self.root)
        self.frame.grid()

        self.show()
    
    def show(self):
        is_dup = False
        for self.name,ships in self.names.items():
            if ships[0] > 1:
                name_label = tk.Label(self.frame,text=self.name)
                name_label.grid(row=0,column=0,columnspan=ships[0])

                self.ships = ships[1]
                self.opt_a = tk.Button(self.frame,text=self.ships[0],command=lambda:self.keep(0))
                self.opt_a.grid(row=1,column=0)

                self.opt_b = tk.Button(self.frame,text=self.ships[1],command=lambda:self.keep(1))
                self.opt_b.grid(row=1,column=1)

                if ships[0] >= 3:
                    self.opt_c = tk.Button(self.frame,text=self.ships[2],command=lambda:self.keep(2))
                    self.opt_c.grid(row=1,column=2)

                if ships[0] >= 4:
                    self.opt_d = tk.Button(self.frame,text=self.ships[3],command=lambda:self.keep(3))
                    self.opt_d.grid(row=1,column=3)
                
                is_dup = True
                break
        
        if is_dup == False:
            label = tk.Label(self.frame,text='There are no duplicates.')
            label.grid()
        
        done_button = tk.Button(self.frame,text = 'Done',command=self.root.destroy)
        done_button.grid(row=2,column=0)
    
    def keep(self,index):
        for i,ship in enumerate(self.ships):
            if i != index:
                self.core.remove_name(ship,self.name,'001-299 Spacecraft')
        
        self.frame.destroy()
        self.frame = tk.Frame(self.root)
        self.frame.grid()

        self.names[self.name][0] = 1

        self.show()
