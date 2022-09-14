import tkinter as tk

class BaseLabel():
    def __init__(self,frame,row,master) -> None:
        self.frame = frame
        self.row = row
        self.master = master

        self.show()
    
    def show(self):
        self.label = tk.Label(self.frame)
        self.label.grid(row=self.row,column=0)

        self.button = tk.Button(self.frame,text = 'X',width=2,command=self.delete)
        self.button.grid(row=self.row,column=1)

    def delete(self):
        pass

class AuxCraftLabel(BaseLabel):
    def __init__(self, frame, row, master, name, num) -> None:
        super().__init__(frame, row, master)

        self.name = name
        self.num = num
        
        type_id = int(name.split('_')[0])
        if type_id <=299:
            self.sect = '001-299 Spacecraft'
        elif type_id <=399:
            self.sect = '301-399 Landcraft'
        elif type_id <=499:
            self.sect = '401-499 Aircraft'
        elif type_id <=699:
            self.sect = '501-699 Watercraft'
        elif type_id <=799:
            self.sect = '701-799 Instillations'

        self.craft_c = '{}-{}'.format(type_id,master.vehicles_types[str(type_id)])

        self.crew = self.master.core.get_crew_total(self.name,self.sect,self.craft_c)

        self.label.config(text='{}: {}'.format(name,num))
    
    def delete(self):
        del self.master.data['AuxCraft_Loadout']['Main'][self.name]
        self.master.data['Crew_Loadout']['Breakdown']['Pilots'] -= self.crew*int(self.num)
        self.master.clear_dynamic()
        self.master.show_aux()

class DropshipLabel(BaseLabel):
    def __init__(self, frame, row, master, name, num, mount) -> None:
        self.mount = mount

        self.name = name
        self.num = num
        super().__init__(frame, row, master)

        self.label.config(text='{},{} Mount: {}'.format(name,mount,num))
        if name[-2:] == 'in':
            self.crew = 2
        else:
            self.crew = 1
    
    def delete(self):
        if len(self.master.data['AuxCraft_Loadout']['Dropships'][self.name]) == 1:
            del self.master.data['AuxCraft_Loadout']['Dropships'][self.name]
        else:
            self.master.data['AuxCraft_Loadout']['Dropships'][self.name].remove([self.mount,self.num])
        self.master.data['Crew_Loadout']['Breakdown']['Pilots'] -= self.crew*int(self.num)
        self.master.clear_dynamic()
        self.master.show_aux()

class CharacteristicLabel(BaseLabel):
    def __init__(self, frame, row, master, name, value) -> None:
        super().__init__(frame, row, master)

        self.name = name
        self.value = value

        if len(value) == 1:
            text = '{}: {}'
        elif len(value) == 2:
            text = '{}: {}{}'
            if isinstance(value[1],str):
                units = value[1].lower()
                if units == 'm':
                    value[1] = 'm'
                elif units == 'km':
                    value[1] = 'Km'
                self.master.data['Description']['Characteristics'][self.name] = value
        elif len(value) == 3:
            text = '{}: Primary: {},Secondary: {}, Tertiary: {}'
        
        self.label.config(text=text.format(name,*value))
    
    def delete(self):
        del self.master.data['Description']['Characteristics'][self.name]
        self.master.clear_dynamic()
        self.master.show_desc()

class OtherSysLabel(BaseLabel):
    def __init__(self, frame, row, master,sys,num) -> None:
        super().__init__(frame, row, master)

        self.sys = sys
        self.num = num

        self.label.config(text='{}: {}'.format(sys,num))
    
    def delete(self):
        del self.master.data['System_Loadout']['Other'][self.sys]
        self.master.clear_dynamic()
        self.master.show_sys()

class WepLabel(BaseLabel):
    def __init__(self, frame, row, master,wep,val,level,locs) -> None:
        super().__init__(frame, row, master)

        self.wep = wep
        self.val = val
        self.locs = locs
        self.level = level
        self.menu_width = self.longest_loc()

        self.data_fix()

        self.label.config(text='{}: {}'.format(wep,self.val[0]))
        self.button.grid(row=self.row,column=2)
        self.show_loc_menu()

    def longest_loc(self):
        longest = 0
        for loc in self.locs:
            if len(loc) > longest:
                longest = len(loc)
        return longest

    def data_fix(self):
        if not isinstance(self.val,list):
            self.val = [self.val,self.locs[0]]
            self.master.data['Weapon_Loadout'][self.level][self.wep] = self.val

    def show_loc_menu(self):
        self.loc_var = tk.StringVar(value=self.val[1])
        self.loc_menu = tk.OptionMenu(self.frame,self.loc_var,*self.locs,command=self.loc_on_select)
        self.loc_menu.config(width=self.menu_width)
        self.loc_menu.grid(row=self.row,column=1)
    
    def loc_on_select(self,loc):
        self.master.data['Weapon_Loadout'][self.level][self.wep][1] = loc

    def delete(self):
        del self.master.data['Weapon_Loadout'][self.level][self.wep]
        self.master.clear_dynamic()
        self.master.show_wep()

class ServLabel(BaseLabel):
    def __init__(self, frame, row, master, reg, name, last=False) -> None:
        super().__init__(frame, row, master)

        self.reg = reg
        self.name = name
        self.last = last

        self.label.config(text='{}: {}'.format(reg,name))
        self.button.grid(row=self.row,column=3)

        self.reorder()
    
    def reorder(self):
        self.up_button = tk.Button(self.frame,text='^',width=2,command=self.up)
        self.up_button.grid(row=self.row,column=1)

        self.down_button = tk.Button(self.frame,text='v',width=2,command=self.down)
        self.down_button.grid(row=self.row,column=2)

        if self.row==0:
            self.up_button.config(state='disabled')
        elif self.last == True:
            self.down_button.config(state='disabled')
        
    def up(self):
        reg = self.reg.split('-')
        abv_reg = reg.copy()
        index = reg[-1]

        if index[-2:] == '00':
            i = index[-3:]
            pre = index[:-3]
        elif index[-2] == '0':
            i = index[-1]
            pre = index[:-1]
        else:
            i = index[-2:]
            pre = index[:-2]

        if i == '10':
            pre += '0'

        i = int(i)
        j = i-1
        abv_index = '{}{}'.format(pre,j)
        abv_reg[-1] = abv_index
        above_reg = '{}-{}-{}-{}'.format(*abv_reg)
        above_name = self.master.data['In_Service']['List'][above_reg]
        self.master.data['In_Service']['List'][above_reg] = self.name
        self.master.data['In_Service']['List'][self.reg] = above_name

        self.master.clear_dynamic()
        self.master.show_serv()

    def down(self):
        reg = self.reg.split('-')
        blw_reg = reg.copy()
        index = reg[-1]

        if index[-2:] == '00':
            i = index[-3:]
            pre = index[:-3]
        elif index[-2] == '0':
            i = index[-1]
            pre = index[:-1]
        else:
            i = index[-2:]
            pre = index[:-2]

        if i == '9':
            pre = pre[:-1]

        i = int(i)
        j = i+1
        blw_index = '{}{}'.format(pre,j)
        blw_reg[-1] = blw_index
        below_reg = '{}-{}-{}-{}'.format(*blw_reg)
        below_name = self.master.data['In_Service']['List'][below_reg]
        self.master.data['In_Service']['List'][below_reg] = self.name
        self.master.data['In_Service']['List'][self.reg] = below_name

        self.master.clear_dynamic()
        self.master.show_serv()
    
    def delete(self):
        del self.master.data['In_Service']['List'][self.reg]
        self.master.data['In_Service']['Totals']['Commissioned'] -= 1
        self.master.data['In_Service']['Totals']['Active'] -= 1
        self.master.clear_dynamic()
        self.master.show_serv()

class RoleLabel(BaseLabel):
    def __init__(self, frame, row, master, role, level) -> None:
        super().__init__(frame, row, master)

        self.role = role
        self.level = level

        self.label.config(text=role)
    
    def delete(self):
        self.master.data['Roles'][self.level]['Roles'].remove(self.role)
        self.master.clear_dynamic()
        self.master.show_role()

class ShldMenu(BaseLabel):
    def __init__(self, frame, row, master,type_val,sub_type_val,vers_val,level,_list) -> None:
        if type_val == None:
            type_val = 'Type'
            
        if sub_type_val == None:
            sub_type_val = 'Sub-type'

        self.type_val = type_val
        self.sub_type_val = sub_type_val
        self.vers_val = vers_val
        self.level = level
        self.list = _list

        super().__init__(frame, row, master)

    def show(self):
        type_var = tk.StringVar(value=self.type_val)
        sub_type_var = tk.StringVar(value=self.sub_type_val)
        vers_var = tk.StringVar(value=self.vers_val)
            
        label = tk.Label(self.frame,text=self.level+' Shield:')
        label.grid(row=self.row,column=0,columnspan=4)

        select_type = tk.OptionMenu(self.frame,type_var,*self.list,command=self.shld_type_on_select)
        select_type.config(width=15)
        select_type.grid(row=self.row+1,column=0)

        try:
            select_subtype = tk.OptionMenu(self.frame,sub_type_var,*self.list[type_var.get()],command=self.shld_sub_type_on_select)
        except KeyError:
            select_subtype = tk.OptionMenu(self.frame,sub_type_var,*[None])
        select_subtype.config(width=15)
        select_subtype.grid(row=self.row+1,column=1)

        label2 = tk.Label(self.frame,text='Type:',width=15)
        label2.grid(row=self.row+1,column=2)
        try:
            select_vers = tk.OptionMenu(self.frame,vers_var,*self.list[type_var.get()][sub_type_var.get()],command=self.shld_vers_on_select)
        except KeyError:
            select_vers = tk.OptionMenu(self.frame,vers_var,*[None])
        select_vers.config(width=15)
        select_vers.grid(row=self.row+1,column=3)
    
    def shld_type_on_select(self,val):
        self.master.data['Shield_Loadout'][self.level]['Type'] = val
        self.master.clear_dynamic()
        self.master.show_shld()
    
    def shld_sub_type_on_select(self,val):
        self.master.data['Shield_Loadout'][self.level]['Sub-Type'] = val
        self.master.clear_dynamic()
        self.master.show_shld()
    
    def shld_vers_on_select(self,val):
        self.master.data['Shield_Loadout'][self.level]['Version'] = val
        self.master.clear_dynamic()
        self.master.show_shld()
    
class PwrMenu(BaseLabel):
    def __init__(self, frame, row, master,_type,vers,style,var,level) -> None:
        self.type = _type
        self.vers = vers
        self.style = style
        self.var = var
        self.level = level

        super().__init__(frame, row, master)
    
    def show(self):
        self.list = self.master.pwr_list

        type_var = tk.StringVar(value=self.type)
        vers_var = tk.StringVar(value=self.vers)
        style_var = tk.StringVar(value=self.style)
        var_var = tk.StringVar(value=self.var)

        label = tk.Label(self.frame,text=self.level+': Type,Version,Style,Variation')
        label.grid(row = self.row,column=0,columnspan=4)

        type_menu = tk.OptionMenu(self.frame,type_var,*self.list['Cores'].keys(),command=self.type_on_select)
        type_menu.config(width=20)
        type_menu.grid(row = self.row+1,column=0)

        vers_menu = tk.OptionMenu(self.frame,vers_var,*self.list['Cores'][str(self.type)]["Version"],command=self.vers_on_select)
        vers_menu.config(width=20)
        vers_menu.grid(row = self.row+1,column=1)

        style_menu = tk.OptionMenu(self.frame,style_var,*self.list['Cores'][str(self.type)]["Style"],command=self.style_on_select)
        style_menu.config(width=30)
        style_menu.grid(row = self.row+1,column=2)

        var_menu = tk.OptionMenu(self.frame,var_var,*self.list['Variation'],command=self.var_on_select)
        var_menu.config(width=20)
        var_menu.grid(row = self.row+1,column=3)
    
    def type_on_select(self,val):
        self.master.data['System_Loadout']["Power Core"][self.level+'_Type'] = val
        self.master.clear_dynamic()
        self.master.show_sys()
    
    def vers_on_select(self,val):
        self.master.data['System_Loadout']["Power Core"][self.level+'_Version'] = val
        self.master.clear_dynamic()
        self.master.show_sys()
    
    def style_on_select(self,val):
        self.master.data['System_Loadout']["Power Core"][self.level+'_Style'] = val
        self.master.clear_dynamic()
        self.master.show_sys()
    
    def var_on_select(self,val):
        self.master.data['System_Loadout']["Power Core"][self.level+'_Variation'] = val
        self.master.clear_dynamic()
        self.master.show_sys()

class PropMenu(BaseLabel):
    def __init__(self, frame, row, master,form,drive,mod,count,idx) -> None:
        self.form = form
        self.drive = drive
        self.mod = mod
        self.count = count
        self.index = idx

        super().__init__(frame, row, master)
    
    def show(self):
        self.row = (10*self.row)+self.index
        self.list = self.master.prop_list[self.form]

        drive_var = tk.StringVar(value=self.drive)
        count_var = tk.IntVar(value=self.count)
        mod_var = tk.StringVar(value=self.mod)


        label = tk.Label(self.frame,text=self.form+':')
        label.grid(row = self.row,column=0)

        drive_menu = tk.OptionMenu(self.frame,drive_var,*self.list.keys(),command=self.drive_on_select)
        drive_menu.config(width=25)
        drive_menu.grid(row = self.row,column=1)

        count_entry = tk.Entry(self.frame,textvariable=count_var,width=5)
        count_entry.grid(row=self.row,column=2)

        count_button = tk.Button(self.frame,text='Save Drive Count',width=25,command=lambda:self.count_on_click(count_var.get()))
        count_button.grid(row=self.row,column=3)

        try:
            mod_menu = tk.OptionMenu(self.frame,mod_var,*self.list[self.drive],command=self.mod_on_select)
        except KeyError:
            mod_menu = tk.OptionMenu(self.frame,mod_var,*[None],command=self.mod_on_select)

        mod_menu.config(width=35)
        mod_menu.grid(row = self.row,column=4)

        if self.index == 0:
            act_button = tk.Button(self.frame,text='Add Another {}'.format(self.form),width=25,command=self.another_on_click)
        else:
            act_button = tk.Button(self.frame,text='X',width=2,command=self.del_drive_on_click)

        act_button.grid(row=self.row,column=5,sticky='w')
    
    def drive_on_select(self,val):
        self.master.data['System_Loadout']['Propultion'][self.form][self.index][0] = val
        if self.form == 'FTL':
            self.count_on_click(1)
        else:
            self.master.clear_dynamic()
            self.master.show_sys()
    
    def count_on_click(self,val):
        self.master.data['System_Loadout']['Propultion'][self.form][self.index][1] = val
        self.master.clear_dynamic()
        self.master.show_sys()
    
    def mod_on_select(self,val):
        self.master.data['System_Loadout']['Propultion'][self.form][self.index][2] = val
        self.master.clear_dynamic()
        self.master.show_sys()
    
    def another_on_click(self):
        if len(self.master.data['System_Loadout']['Propultion'][self.form]) < 10:
            self.master.data['System_Loadout']['Propultion'][self.form].append(['',0,''])
            self.master.clear_dynamic()
            self.master.show_sys()

    def del_drive_on_click(self):
        self.master.data['System_Loadout']['Propultion'][self.form].pop(self.index)
        self.master.clear_dynamic()
        self.master.show_sys()

class LoreAttrLabel(BaseLabel):
    def __init__(self, frame, row, master, name, value, val_type, path) -> None:
        self.name = name
        self.value = value
        self.val_type = val_type
        self.path = path
        super().__init__(frame, row, master)
    
    def show(self):
        self.name_var = tk.StringVar(value=self.name)
        self.name_entry = tk.Entry(self.frame,textvariable=self.name_var)
        self.name_entry.grid(row=self.row,column=0)

        self.label = tk.Label(self.frame,text=' : ')
        self.label.grid(row=self.row,column=1)

        self.value_var = tk.StringVar(value=self.value)
        self.value_entry = tk.Entry(self.frame,textvariable=self.value_var)
        self.value_entry.grid(row=self.row,column=2)

        self.val_type_var = tk.StringVar(value=self.val_type)
        self.val_type_menu = tk.OptionMenu(self.frame,self.val_type_var,*['Num','Txt'])
        self.val_type_menu.grid(row=self.row,column=3)

        self.button = tk.Button(self.frame,text = 'X',width=2,command=self.delete)
        self.button.grid(row=self.row,column=4)
    
    def save(self):
        self.name = self.name_var.get()
        self.value = self.value_var.get()
        self.val_type = self.val_type_var.get()
        if self.val_type == 'Num':
            try:
                self.value = int(self.value)
            except ValueError:
                self.value = float(self.value)

        return (self.name,self.value)
    
    def delete(self):
        if len(self.path) == 0:
            del self.master.lore[self.name]
        elif len(self.path) == 1:
            del self.master.lore[self.path[0]][self.name]
        elif len(self.path) == 2:
            del self.master.lore[self.path[0]][self.path[1]][self.name]
            
        self.master.clear_dynamic()
        self.master.dynamic()

class LoreListLabel(BaseLabel):
    def __init__(self, frame, row, master, name, values, val_type, path) -> None:
        self.name = name
        self.values = values
        self.val_type = val_type
        self.path = path
        super().__init__(frame, row, master)
    
    def show(self):
        self.name_var = tk.StringVar(value=self.name)
        self.name_entry = tk.Entry(self.frame,textvariable=self.name_var)
        self.list_frame = tk.LabelFrame(self.frame,labelwidget=self.name_entry)
        self.list_frame.grid(row=self.row,column=0,columnspan=5)

        label_row = 0
        for label_row,val in enumerate(self.values):
            ListLabel(self.list_frame,label_row,self,val)
        
        self.add_term_button = tk.Button(self.list_frame,text='Add Term to List',width=20,command=self.add_term)
        self.add_term_button.grid(row=label_row+1,column=0,columnspan=2)
        
        self.add_list_button = tk.Button(self.list_frame,text='Delete List',width=20,command=self.delete)
        self.add_list_button.grid(row=label_row+2,column=0,columnspan=2)
    
    def add_term(self):
        win = tk.Toplevel(self.frame)
        text = 'Add a term to the list:'
        pop_up = AddTermPopUp(win,text,self)
    
    def save(self):
        self.name = self.name_var.get()
        return self.name,self.values

    def delete(self):
        if len(self.path) == 0:
            del self.master.lore[self.name]
        elif len(self.path) == 1:
            del self.master.lore[self.path[0]][self.name]
        elif len(self.path) == 2:
            del self.master.lore[self.path[0]][self.path[1]][self.name]
            
        self.redraw()

    def redraw(self):
        self.master.clear_dynamic()
        self.master.dynamic()

class LoreSectLabel(BaseLabel):
    def __init__(self, frame, row, master, name, path, size) -> None:
        self.name = name
        self.path = path
        self.size = size
        super().__init__(frame, row, master)
    
    def show(self):
        self.name_var = tk.StringVar(value=self.name)
        self.name_entry = tk.Entry(self.frame,textvariable=self.name_var)
        self.sect_frame = tk.LabelFrame(self.frame,bd=5,labelwidget=self.name_entry)
        self.sect_frame.grid(row=self.row,column=0,columnspan=5)

        self.add_attr_button = tk.Button(self.sect_frame,text='Add Attribute',width=20,command=self.add_attr)
        self.add_attr_button.grid(row=self.size,column=0,columnspan=5)

        self.add_list_button = tk.Button(self.sect_frame,text='Add List',width=20,command=self.add_list)
        self.add_list_button.grid(row=self.size+1,column=0,columnspan=5)

        self.delete_button = tk.Button(self.sect_frame,text='Delete Section',width=20,command=self.delete)
        self.delete_button.grid(row=self.size+2,column=0,columnspan=5)

    def save(self):
        self.name = self.name_var.get()

        return self.name

    def delete(self):
        if len(self.path) == 0:
            del self.master.lore[self.name]
        elif len(self.path) == 1:
            del self.master.lore[self.path[0]][self.name]
        
        self.redraw()
    
    def add_attr(self):
        text = 'Add Attribute to the {} section'.format(self.name)
        path = self.path.copy()
        path.append(self.name)
        win = tk.Toplevel(self.frame)
        pop_up = AttrPopUp(win,text,self.master,path)

    def add_list(self):
        text = 'Add List to the {} section'.format(self.name)
        path = self.path.copy()
        path.append(self.name)
        win = tk.Toplevel(self.frame)
        pop_up = ListPopUp(win,text,self.master,path)

    def redraw(self):
        self.master.clear_dynamic()
        self.master.dynamic()

class LoreHeaderLabel(BaseLabel):
    def __init__(self, frame, row, master, name, size) -> None:
        self.name = name
        self.size = size
        super().__init__(frame, row, master)
    
    def show(self):
        self.name_var = tk.StringVar(value=self.name)
        self.name_entry = tk.Entry(self.frame,textvariable=self.name_var)
        self.head_frame = tk.LabelFrame(self.frame,bd=8,labelanchor='n',labelwidget=self.name_entry)
        self.head_frame.grid(row=self.row,column=0,columnspan=5)

        self.add_sect_button = tk.Button(self.head_frame,text='Add Section',width=20,command=self.add_sect)
        self.add_sect_button.grid(row=self.size,column=0,columnspan=5)

        self.delete_button = tk.Button(self.head_frame,text='Delete Header',width=20,command=self.delete)
        self.delete_button.grid(row=self.size+2,column=0,columnspan=5)
    
    def save(self):
        self.name = self.name_var.get()
        return self.name

    def delete(self):
        del self.master.lore[self.name]
        
        self.redraw()
    
    def add_sect(self):
        text = 'Add Section to the {} Header'.format(self.name)
        path = [self.name]
        win = tk.Toplevel(self.frame)
        pop_up = SectionPopUp(win,text,self.master,path)

    def redraw(self):
        self.master.clear_dynamic()
        self.master.dynamic()

class ListLabel(BaseLabel):
    def __init__(self, frame, row, master,value) -> None:
        self.value = value
        super().__init__(frame, row, master)

        self.label.config(text=self.value)
    
    def delete(self):
        self.master.values.pop(self.row)
        self.master.redraw()

class BasePopUp():
    def __init__(self,root,text,master,path):
        self.root = root
        self.text = text
        self.master = master
        self.path = path

        self.frame = tk.Frame(root)
        self.frame.grid()
        
        self.show()

    def show(self):
        pass
    
    def save_on_click(self):
        pass
    
    def cancel_on_click(self):
        self.root.destroy()

class AttrPopUp(BasePopUp):
    def __init__(self, root, text, master,path):
        super().__init__(root, text, master, path)
    
    def show(self):
        self.label = tk.Label(self.frame,text=self.text)
        self.label.grid(row=0,column=0,columnspan=3)

        #Name
        self.name_label = tk.Label(self.frame,text='Name')
        self.name_label.grid(row=2,column=0)

        self.name_var = tk.StringVar()
        self.name_entry = tk.Entry(self.frame,textvariable=self.name_var)
        self.name_entry.grid(row=3,column=0)

        #Value
        self.value_label = tk.Label(self.frame,text='Value')
        self.value_label.grid(row=2,column=1)

        self.value_var = tk.StringVar()
        self.value_entry = tk.Entry(self.frame,textvariable=self.value_var)
        self.value_entry.grid(row=3,column=1)

        #Type
        self.type_label = tk.Label(self.frame,text='Type')
        self.type_label.grid(row=2,column=2)

        self.type_var = tk.StringVar(value='Txt')
        self.type_menu = tk.OptionMenu(self.frame,self.type_var,*['Num','Txt'])
        self.type_menu.config(width=5)
        self.type_menu.grid(row=3,column=2)

        #Save/Cancel
        self.save_button = tk.Button(self.frame,text='Save',width=10,command=self.save_on_click)
        self.save_button.grid(row=4,column=0,columnspan=2,sticky='w')

        self.cancel_button = tk.Button(self.frame,text='Cancel',width=10,command=self.cancel_on_click)
        self.cancel_button.grid(row=4,column=1,columnspan=2,sticky='e')
    
    def save_on_click(self):
        name = self.name_var.get()
        val = self.value_var.get()
        val_type = self.type_var.get()
        if val_type == 'Num':
            try:
                value = int(val)
            except ValueError:
                value = float(val)
        else:
            value = val

        if len(self.path) == 0:
            self.master.lore[name] = value
        elif len(self.path) == 1:
            self.master.lore[self.path[0]][name] = value
        elif len(self.path) == 2:
            self.master.lore[self.path[0]][self.path[1]][name] = value
    
        self.master.clear_dynamic()
        self.master.dynamic()
        self.root.destroy()

class ListPopUp(BasePopUp):
    def __init__(self, root, text, master, path):
        super().__init__(root, text, master, path)
    
    def show(self):
        self.label = tk.Label(self.frame,text=self.text)
        self.label.grid(row=0,column=0,columnspan=2)

        #Name
        self.name_label = tk.Label(self.frame,text='Name')
        self.name_label.grid(row=2,column=0,columnspan=2)

        self.name_var = tk.StringVar()
        self.name_entry = tk.Entry(self.frame,textvariable=self.name_var)
        self.name_entry.grid(row=3,column=0,columnspan=2)

        #Save/Cancel
        self.save_button = tk.Button(self.frame,text='Save',width=10,command=self.save_on_click)
        self.save_button.grid(row=4,column=0)

        self.cancel_button = tk.Button(self.frame,text='Cancel',width=10,command=self.cancel_on_click)
        self.cancel_button.grid(row=4,column=1)
    
    def save_on_click(self):
        name = self.name_var.get()

        if len(self.path) == 0:
            self.master.lore[name] = []
        elif len(self.path) == 1:
            self.master.lore[self.path[0]][name] = []
        elif len(self.path) == 2:
            self.master.lore[self.path[0]][self.path[1]][name] = []
    
        self.master.clear_dynamic()
        self.master.dynamic()
        self.root.destroy()

class SectionPopUp(BasePopUp):
    def __init__(self, root, text, master, path):
        super().__init__(root, text, master, path)
    
    def show(self):
        self.label = tk.Label(self.frame,text=self.text)
        self.label.grid(row=0,column=0,columnspan=3)

        #name
        self.name_label = tk.Label(self.frame,text='Name')
        self.name_label.grid(row=2,column=0)

        self.name_var = tk.StringVar()
        self.name_entry = tk.Entry(self.frame,textvariable=self.name_var)
        self.name_entry.grid(row=2,column=1)

        #Save/Cancel
        self.save_button = tk.Button(self.frame,text='Save',width=10,command=self.save_on_click)
        self.save_button.grid(row=4,column=0,columnspan=2,sticky='w')

        self.cancel_button = tk.Button(self.frame,text='Cancel',width=10,command=self.cancel_on_click)
        self.cancel_button.grid(row=4,column=1,columnspan=2,sticky='e')
    
    def save_on_click(self):
        name = self.name_var.get()

        if len(self.path) == 0:
            self.master.lore[name] = {}
        elif len(self.path) == 1:
            self.master.lore[self.path[0]][name] = {}
        
        self.master.clear_dynamic()
        self.master.dynamic()
        self.root.destroy()

class HeaderPopUp(BasePopUp):
    def __init__(self, root, text, master, path):
        super().__init__(root, text, master, path)
    
    def show(self):
        self.label = tk.Label(self.frame,text=self.text)
        self.label.grid(row=0,column=0,columnspan=3)

        #name
        self.name_label = tk.Label(self.frame,text='Header name')
        self.name_label.grid(row=1,column=0)

        self.name_var = tk.StringVar()
        self.name_entry = tk.Entry(self.frame,textvariable=self.name_var)
        self.name_entry.grid(row=1,column=1)

        #sect name
        self.sect_name_label = tk.Label(self.frame,text='Section name')
        self.sect_name_label.grid(row=2,column=0)

        self.sect_name_var = tk.StringVar()
        self.sect_name_entry = tk.Entry(self.frame,textvariable=self.sect_name_var)
        self.sect_name_entry.grid(row=2,column=1)

        #Save/Cancel
        self.save_button = tk.Button(self.frame,text='Save',width=10,command=self.save_on_click)
        self.save_button.grid(row=4,column=0,columnspan=2,sticky='w')

        self.cancel_button = tk.Button(self.frame,text='Cancel',width=10,command=self.cancel_on_click)
        self.cancel_button.grid(row=4,column=1,columnspan=2,sticky='e')
    
    def save_on_click(self):
        name = self.name_var.get()
        sect_name = self.sect_name_var.get()

        self.master.lore[name] = {sect_name:{}}
        
        self.master.clear_dynamic()
        self.master.dynamic()
        self.root.destroy()

class AddTermPopUp(BasePopUp):
    def __init__(self, root, text, master, path=[]):
        super().__init__(root, text, master, path)
    
    def show(self):
        self.label = tk.Label(self.frame,text=self.text)
        self.label.grid(row=0,column=0,columnspan=2)

        #Value
        self.value_label = tk.Label(self.frame,text='Value')
        self.value_label.grid(row=1,column=0)

        self.value_var = tk.StringVar()
        self.value_entry = tk.Entry(self.frame,textvariable=self.value_var)
        self.value_entry.grid(row=1,column=1)

        #Save/Cancel
        self.save_button = tk.Button(self.frame,text='Save',width=10,command=self.save_on_click)
        self.save_button.grid(row=2,column=0)

        self.cancel_button = tk.Button(self.frame,text='Cancel',width=10,command=self.cancel_on_click)
        self.cancel_button.grid(row=2,column=1)
    
    def save_on_click(self):
        val_type = self.master.val_type
        val = self.value_var.get()
        if val_type == 'Num':
            try:
                value = int(val)
            except ValueError:
                value = float(val)
        else:
            value = val
        
        self.master.values.append(value)
        self.master.redraw()
