import PySimpleGUI as psg
import os
import json
import sys
import shutil
#变量
Settings = False
Create_mod = False
Optional_Text = ('宋体', 10, 'bold')
Required_Text = ('宋体', 10)

with open('Settings.json', 'r') as File:
    Settings_Data = json.load(File)
    pass
psg.theme(Settings_Data['Background_Color'])
psg.theme_input_background_color('#FFFFFF')
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
Mod_Project_List = getfilename('Project')
Mod_Project_List = [] if Mod_Project_List == None else Mod_Project_List


#界面
Mod_List_Element = psg.Listbox(Mod_Project_List,size=(35,25),horizontal_scroll=False,no_scrollbar=False, key='-MODLIST-')
Layout_GUI_Left = [
    [Mod_List_Element]
]
Layout_GUI_Right = [
    [psg.Button("创建项目",size=(15,2),font=('新宋体', 15),pad=((100,0),(0,0)))],
    [psg.Button("删除项目",size=(15,2),font=('新宋体', 15),pad=((100,0),(10,0)))],
    [psg.Button("编辑项目",size=(15,2),font=('新宋体', 15),pad=((100,0),(10,0)))],
    [psg.Button("设置",size=(15,2),font=('新宋体', 15),pad=((100,0),(15,0)))]
]
Layout_GUI_Left_Col = psg.Column(Layout_GUI_Left)
Layout_GUI_Right_Col = psg.Column(Layout_GUI_Right)
Layout = [
    [Layout_GUI_Left_Col,Layout_GUI_Right_Col]
]

#创建窗口
Window = psg.Window("MindCraft",Layout,size=(900,630))

while True:
    Event, Vaule = Window.read(timeout=100)
    #退出程序
    if Event == psg.WIN_CLOSED:
        break
    #设置
    if not Settings and Event == '设置':
        Settings = True
        Settings_GUI = [
            [psg.Text('主题色', font=('宋体', 12)),psg.Combo(psg.theme_list(),default_value=Settings_Data['Background_Color'] ,expand_x=True, pad=((100,0),(0,0)), font=('宋体',12), key='-Settings_Background_Color_Combo-')],
            [psg.Button('确定',pad=((250,0),(0,0)), font=('宋体', 12)),psg.Button('取消',pad=((10,0),(0,0)), font=('宋体', 12))]
        ]
        Settings_GUI_Run = psg.Window('设置', Settings_GUI, size=(400,300))
        pass
    if Settings:
        Settings_GUI_Event,Settings_GUI_Values = Settings_GUI_Run.read(timeout=100)
        if Settings_GUI_Event is None or Settings_GUI_Event == (psg.WIN_CLOSED) or Settings_GUI_Event  == "取消":
            Settings = False
            Settings_GUI_Run.close()
            pass
        if Settings_GUI_Event == '确定':
            if psg.popup_ok_cancel('重启以便应用设置') == 'OK':
                Settings = False
                Settings_GUI_Run.close()
                Window.close()
                pass
            else:
                Settings = False
                Settings_GUI_Run.close()
                pass
            Settings_Json = {
                'Background_Color': Settings_GUI_Values['-Settings_Background_Color_Combo-']
            }
            with open('Settings.json', 'w') as File:
                File.write(json.dumps(Settings_Json))
                pass
            Settings = False
            Settings_GUI_Run.close()
            pass
        pass
    #创建模组
    if not Settings and Event == '创建项目':
        Create_mod = True
        Create_mod_GUI = [
            [psg.Text('注：暂不支持制作136版本以下的模组',font=Required_Text)],
            [psg.Text('模组名称',font=Required_Text),psg.Input(key='-Mod_Name-',expand_x=True)],
            [psg.Text('模组作者',font=Required_Text),psg.Input(key='-Mod_Author-',expand_x=True)],
            [psg.Text('模组介绍',font=Required_Text),psg.Input(key='-Mod_Description-',expand_x=True)],
            [psg.Text('模组版本',font=Required_Text),psg.Input(key='-Mod_Version-',expand_x=True)],
            [psg.Text('模组最小游戏版本',font=Required_Text),psg.Input(key='-Mod_MinGameVersion-',expand_x=True)],
            [psg.Button('创建',font=Required_Text),psg.Button('取消',font=Required_Text)]
        ]
        Create_mod_GUI_Run = psg.Window('创建新模组',Create_mod_GUI,size=(400,300), grab_anywhere=True)
        pass
    if Create_mod:
        Create_mod_GUI_Event, Create_mod_GUI_Vaules = Create_mod_GUI_Run.read(timeout=100)
        if Create_mod_GUI_Event is None or Create_mod_GUI_Event == (psg.WIN_CLOSED) or Create_mod_GUI_Event  == "取消":
            Create_mod = False
            Create_mod_GUI_Run.close()
            pass
        if Create_mod_GUI_Event is None or Create_mod_GUI_Event == '创建':
            #判断输入内容是否为有效值
            Create_mod_Error_List = []
            #模组名称
            if len(str(Create_mod_GUI_Vaules['-Mod_Name-'])) != 0 and IsChar(str(Create_mod_GUI_Vaules['-Mod_Name-'])):
                Create_mod_GUI_Run['-Mod_Name-'].update(background_color = '#FFFFFF')           
                pass
            else:
                Create_mod_GUI_Run['-Mod_Name-'].update(background_color = '#FF4242')
                Create_mod_Error_List.append("模组名称：输入的内容不能为空，或者不能含以下几种字符：\n\\ / : ? * \" < > |\n")
                pass
            #模组作者
            if len(str(Create_mod_GUI_Vaules['-Mod_Author-'])) != 0 and IsChar(str(Create_mod_GUI_Vaules['-Mod_Author-'])):
                Create_mod_GUI_Run['-Mod_Author-'].update(background_color = '#FFFFFF')           
                pass
            else:
                Create_mod_GUI_Run['-Mod_Author-'].update(background_color = '#FF4242')
                Create_mod_Error_List.append("模组作者 ：输入的内容不能为空，或者不能含以下几种字符：\n\\ / : ? * \" < > |\n")
                pass
            #模组介绍
            if len(str(Create_mod_GUI_Vaules['-Mod_Description-'])) != 0:
                Create_mod_GUI_Run['-Mod_Description-'].update(background_color = '#FFFFFF')           
                pass
            else:
                Create_mod_GUI_Run['-Mod_Description-'].update(background_color = '#FF4242')
                Create_mod_Error_List.append("模组介绍：输入的内容不能为空\n")
                pass
            #模组版本
            if len(str(Create_mod_GUI_Vaules['-Mod_Version-'])) != 0:
                Create_mod_GUI_Run['-Mod_Version-'].update(background_color = '#FFFFFF')           
                pass
            else:
                Create_mod_GUI_Run['-Mod_Version-'].update(background_color = '#FF4242')
                Create_mod_Error_List.append("模组版本：输入的内容不能为空\n")
                pass
            #模组最小游戏版本
            if len(str(Create_mod_GUI_Vaules['-Mod_MinGameVersion-'])) != 0 and str(Create_mod_GUI_Vaules['-Mod_MinGameVersion-']).isdigit():
                Create_mod_GUI_Run['-Mod_MinGameVersion-'].update(background_color = '#FFFFFF')           
                pass
            else:
                Create_mod_GUI_Run['-Mod_MinGameVersion-'].update(background_color = '#FF4242')
                Create_mod_Error_List.append("模组版本：输入的内容不能为空,或者不是整数\n")
                pass
            #如果列表里有内容，就弹出弹窗显示错误原因
            if len(Create_mod_Error_List) != 0:
                Error_Text = ''
                for i in Create_mod_Error_List:
                    Error_Text += i
                    pass
                psg.popup_error(f"有以下几个模组元素问题需要解决：\n{Error_Text}\n错误的地方已经标红",title='模组元素错误',font=Required_Text)
                pass
            else:
                os.makedirs('Project/' + str(Create_mod_GUI_Vaules['-Mod_Name-']) + '/' + str(Create_mod_GUI_Vaules['-Mod_Name-']) + '/content/blocks')
                os.makedirs('Project/' + str(Create_mod_GUI_Vaules['-Mod_Name-']) + '/' + str(Create_mod_GUI_Vaules['-Mod_Name-']) + '/content/items')
                os.makedirs('Project/' + str(Create_mod_GUI_Vaules['-Mod_Name-']) + '/' + str(Create_mod_GUI_Vaules['-Mod_Name-']) + '/content/liquids')
                os.makedirs('Project/' + str(Create_mod_GUI_Vaules['-Mod_Name-']) + '/' + str(Create_mod_GUI_Vaules['-Mod_Name-']) + '/sprites/blocks')
                os.makedirs('Project/' + str(Create_mod_GUI_Vaules['-Mod_Name-']) + '/' + str(Create_mod_GUI_Vaules['-Mod_Name-']) + '/sprites/items')
                os.makedirs('Project/' + str(Create_mod_GUI_Vaules['-Mod_Name-']) + '/' + str(Create_mod_GUI_Vaules['-Mod_Name-']) + '/sprites/liquids')
                with open('Project/' + str(Create_mod_GUI_Vaules['-Mod_Name-']) + '/' + str(Create_mod_GUI_Vaules['-Mod_Name-']) +'/mod.json','w') as File:
                    Json_Dict = {
                        "name": Create_mod_GUI_Vaules['-Mod_Name-'],
	                    "author": Create_mod_GUI_Vaules['-Mod_Author-'],
	                    "description": Create_mod_GUI_Vaules['-Mod_Description-'],
	                    "version": Create_mod_GUI_Vaules['-Mod_Version-'],
	                    "minGameVersion": int(Create_mod_GUI_Vaules['-Mod_MinGameVersion-']),
                    }
                    File.write(json.dumps(Json_Dict,sort_keys=False, indent=4))
                    pass
                os.startfile('Edit\EditMod' + IsFormat())
                Create_mod = False
                Create_mod_GUI_Run.close()
                Window.close()
                pass
            pass
        pass
    #编辑模组
    if Event == '编辑项目':
        try:
            mod_name = str(Mod_List_Element.get()[0])
            with open('LastEditMod.json','w') as File:
                File.write(json.dumps({'LastEditMod':mod_name}))
                pass
            os.startfile('Edit\EditMod' + IsFormat())
            Window.close()
            pass
        except:
            psg.popup_error('错误：未选中项目')
            pass
        pass
    #删除模组
    if Event == '删除项目':
        try:
            mod_name = str(Mod_List_Element.get()[0])
            if psg.popup_ok_cancel('确定要删除吗？') == 'OK':
                shutil.rmtree(f'Project/{mod_name}')
                Mod_Project_List.remove(mod_name)
                Window['-MODLIST-'].update(Mod_Project_List)
                pass
            pass
        except:
            psg.popup_error('错误：未选中项目')
            pass
        pass
    pass
Window.close()
