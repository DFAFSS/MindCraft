import os
import json
import sys
import PySimpleGUI as psg

#函数
def IsRGB(RGB):
    RGB_L = list(RGB)
    RGBN = 0
    if not len(RGB_L) == 7:
        return False
    if not RGB_L[0] == '#':
        return False
    for RGBI in RGB_L:
        for S in ['1','2','3','4','5','6','7','8','9','0','A','B','C','D','E','F','#']:
            if S == RGBI:
                RGBN += 1
                pass
            pass
        pass
    print(RGBN)
    if RGBN == 7:
        return True
    return False
def IsChar(Text):
    Text_L = list(Text)
    N = 0
    for TextI in Text_L:
        for S in ['\\','/',':','?','*','"','<','>','|']:
            if S == TextI:
                N += 1
            pass
        pass
    if N != 0:
        return False
    return True
def getfilename(filename):
    for root, dirs, files in os.walk(filename):
        array = dirs
        if array:
            return array
def IsFormat():
    exefile = sys.argv[0]
    isexe = exefile.endswith(".exe")
    ispy = exefile.endswith(".py")
    ispyc = exefile.endswith(".pyc")
    if isexe:
        return '.exe'
    elif ispy:
        return '.py'
    elif ispyc:
        return '.pyc'
def IsRepeat(name,list):
    for I in list:
        if name == I:
            return True
        pass
    return False

#变量
with open('./LastEditMod.json','r') as File:
    mod_name = json.load(File)['LastEditMod']
    pass
ModPath = f'./Project/{mod_name}/{mod_name}'
Optional_Text = ('宋体', 12, 'bold')
Required_Text = ('宋体', 12)
ST_Text = ('宋体', 14)

Creat_Item = False

with open('Settings.json', 'r') as File:
    Settings_Data = json.load(File)
    pass
psg.theme(Settings_Data['Background_Color'])
psg.theme_input_background_color('#FFFFFF')

Creat_Mod_Layout = [
    [psg.Button('物品',font=ST_Text,size=(10,2))]
]
Mod_Event = []

Edit_Mod_Layout = [
    [psg.Table(Mod_Event,['名称','类型'],expand_x=True,auto_size_columns=True,justification='center', key='-TABLE-',display_row_numbers=False,enable_click_events=True,enable_events=True,expand_y=True)],
    [psg.Button('删除元素'),psg.Button('编辑元素')]
]

Layout = [
    [psg.Menu([['文件',['导出模组','关闭项目','关闭MindCraft']],['编辑',['编辑模组信息','选择模组LOGO']]])],
    [psg.TabGroup([[psg.Tab('添加元素',Creat_Mod_Layout)],[psg.Tab('编辑元素',Edit_Mod_Layout)]],expand_x=True,expand_y=True)]
]

Window = psg.Window('模组编辑 - ' + mod_name, Layout, size=(1200,1000))

while True:
    Event, Vaule = Window.read(timeout=100)
    if Event == psg.WIN_CLOSED:
        break
    if Event == '关闭项目':
        os.startfile('.\MindCraft' + IsFormat())
        break
    if Event == '关闭MindCraft':
        break
    #物品
    if not Creat_Item and Event == '物品':
        Get_Mod_Name_Item = psg.popup_get_text('请输入你要创建模组的名称',font=ST_Text,title='创建新物品')
        Mod_Event_List = []
        for MI in Mod_Event:
            Mod_Event_List.append(MI[0])
            pass
        if Get_Mod_Name_Item != None:
            if IsChar(Get_Mod_Name_Item) == True and len(Get_Mod_Name_Item) != 0 and IsRepeat(Get_Mod_Name_Item,Mod_Event_List) == False:
                Creat_Item = True
                Creat_Item_GUI_1 = [
                    [psg.Text('物品名称',font=ST_Text),psg.Input(key='-Item_Name-')],
                    [psg.Text('物品描述',font=ST_Text),psg.Input(key='-Item_Description-')],
                    [psg.Text('物品详细描述',font=ST_Text),psg.Input(key='-Item_Details-')],
                    [psg.Text('物品颜色',font=ST_Text),psg.Input(key='-Item_Color-')]
                ]
                Creat_Item_GUI_2 = [
                    [psg.Text('物品增加建筑时间的指数',font=ST_Text),psg.Input(key='-Item_Cost-')],
                    [psg.Text('物品放射性',font=ST_Text),psg.Input(key='-Item_Radioactivity-')],
                    [psg.Text('物品燃烧性',font=ST_Text),psg.Input(key='-Item_Flammability-')],
                    [psg.Text('物品放电性',font=ST_Text),psg.Input(key='-Item_Charge-')],
                    [psg.Text('物品影响方块默认生命值',font=ST_Text),psg.Input(key='-Item_HealthScaling-')],
                    [psg.Text('矿物挖掘优先级',font=ST_Text),psg.Input(key='-Item_LowPriority-')],
                ]
                Creat_Item_GUI = [
                    [psg.Frame('通用属性',Creat_Item_GUI_1,font=('宋体',10))],
                    [psg.Frame('特殊值',Creat_Item_GUI_2,font=('宋体',10))],
                    [psg.Button('取消',font=Required_Text),psg.Button('确定',font=Required_Text)]
                ]
                Creat_Item_GUI_Run = psg.Window('创建物品',Creat_Item_GUI,size=(600,600))
                pass
            else:
                psg.popup_error('错误：输入的内容不能为空，不能使用已经被使用过的名称，\n或者不能含以下几种字符：\n\\ / : ? * \" < > |',font=ST_Text)
                pass
            pass
        pass
    if Creat_Item:
        Creat_Item_GUI_Event, Creat_Item_GUI_Vaule = Creat_Item_GUI_Run.read(timeout=100)
        if Creat_Item_GUI_Event is None or Creat_Item_GUI_Event == (psg.WIN_CLOSED) or Creat_Item_GUI_Event  == "取消":
            Creat_Item = False
            Creat_Item_GUI_Run.close()
            pass
        pass
    pass
Window.close()