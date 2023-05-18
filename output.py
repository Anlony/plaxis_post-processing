s_i, g_i = new_server('localhost', 10000, password='^hB<TW9k!y4$<KY@')  # 主机input端口
output_port = g_i.view(g_i.Phases[0])  # 获得output程序接口
s_o, g_o = new_server('localhost', port=output_port,password='^hB<TW9k!y4$<KY@')  # 开启接口
# 在output中进行数据收集
results= {} 
Mstage = pd.DataFrame()
 # 此步建立该循环需要输出的变量，此处字典意在收集从plaxis中提取的以节点为单位的原始数据
for phase_number in [2,3]:     # 此步确定输出那两步phases的结果，一般为施加水平承载力的前一步和水平荷载施加步
    dataframe_Position=[0]      # 此步设置储存变量
    step_number = len(g_o.Phases[phase_number])  # 获取该Phase的步骤数Steps
    step_number_start=1     # Phases基本都是以step1开始，少数bug情况会出现step0开始
    #   获取输出单元的基本信息，包括单元ID，节点坐标，单元面积
    E_ID = eval(g_o.getresults(g_o.Phases[phase_number][step_number_start], g_o.ResultTypes.Interface.ElementID, "node").echo()) 
    CX = eval(g_o.getresults(g_o.Phases[phase_number][step_number_start], g_o.ResultTypes.Interface.X, "node").echo())  
    CY = eval(g_o.getresults(g_o.Phases[phase_number][step_number_start], g_o.ResultTypes.Interface.Y, "node").echo())
    CZ = eval(g_o.getresults(g_o.Phases[phase_number][step_number_start], g_o.ResultTypes.Interface.Z, "node").echo())
    Area = eval(g_o.getresults(g_o.Phases[phase_number][step_number_start], g_o.ResultTypes.Interface.Area, "node").echo())
    Loc_num = eval(g_o.getresults(g_o.Phases[phase_number][step_number_start], g_o.ResultTypes.Interface.LocalNumber, "node").echo())
    NodeID = eval(g_o.getresults(g_o.Phases[phase_number][step_number_start], g_o.ResultTypes.Interface.NodeID, "node").echo())
    # 将单元基本信息设置为step_0，放在原始数据第一列
    E_ID = np.array(E_ID).reshape(-1, 1)    # 将获取数据转化为一列array格式的数据
    CX = np.array(CX).reshape(-1, 1)
    CY = np.array(CY).reshape(-1, 1)
    CZ = np.array(CZ).reshape(-1, 1)
    Area = np.array(Area).reshape(-1, 1)
    Loc_num = np.array(Loc_num).reshape(-1, 1)
    NodeID = np.array(NodeID).reshape(-1, 1)
    phase_array = np.hstack((E_ID,Loc_num,NodeID,CX,CY,CZ,Area))   # 将每列array数据组合成多列的array数据
    dataframe_Position=pd.DataFrame(phase_array)    # 将array数据转化成dataframe格式
    dataframe_Position.columns=[['step_0','step_0','step_0','step_0','step_0','step_0','step_0'],['E_ID','LocalNumber','NodeID','CX','CY','CZ','Area']]  #为每个信息设置两级列名

    # 获取每个单元的内力及位移，此处Uy对应Y方向荷载
    # 该循环收集phases下每个step的数据，并整理为dataframe数据格式，设置多级列名
    Mstage_phase = pd.DataFrame()
    for step_N in range(step_number_start, step_number):  # 收集每个step的数据 
        SIGMA_N = (eval(g_o.getresults(g_o.Phases[phase_number][step_N], g_o.ResultTypes.Interface.InterfaceEffectiveNormalStress, "stresspoint").echo()))
        TAO_1 = (eval(g_o.getresults(g_o.Phases[phase_number][step_N], g_o.ResultTypes.Interface.InterfaceShearStress, "stresspoint").echo()))
        TAO_2 = (eval(g_o.getresults(g_o.Phases[phase_number][step_N], g_o.ResultTypes.Interface.InterfaceShearStress2, "stresspoint").echo()))
        Uy = (eval(g_o.getresults(g_o.Phases[phase_number][step_N], g_o.ResultTypes.Interface.Uy, "node").echo()))
        # 获取每个step的sumMstage
        ProposedForce = g_o.Phases[phase_number][step_N].Reached.SumMstage.value
        Mstage_step = pd.DataFrame(pd.Series(ProposedForce))
        Mstage_step.columns = ['step_%r' %step_N]
        Mstage_phase = pd.concat([Mstage_phase, Mstage_step], axis=1)


        SIGMA_N = np.array(SIGMA_N).reshape(-1, 1)
        TAO_1 = np.array(TAO_1).reshape(-1, 1)
        TAO_2 = np.array(TAO_2).reshape(-1, 1)
        Uy = np.array(Uy).reshape(-1, 1)
        phase_array = np.hstack((SIGMA_N,TAO_1,TAO_2,Uy))
        dataframe_step = pd.DataFrame((phase_array))
        dataframe_step.columns =[['step_%r'%step_N,'step_%r'%step_N,'step_%r'%step_N,'step_%r'%step_N],['SIGMA_N','TAO_1','TAO_2','Uy' ]]
        dataframe_Position = pd.concat([dataframe_Position, dataframe_step], axis=1)
    
    Mstage_phase.index = ['Phase_%r' %phase_number]
    Mstage = pd.concat([Mstage, Mstage_phase], axis = 0)

    path_file1 = os.path.join('E:\\','OneDrive - 同济大学','plaxis_work','PPC','全荷载','%s' %filename,'原始数据_%r.xlsx'%phase_number)
    path_file1 = path_file1.replace('\\', '/')
    writer = pd.ExcelWriter(path_file1, mode='w')  #这是对应phases原始数据的保存路径
    # writer = pd.ExcelWriter('E:/OneDrive - 同济大学/plaxis_work/test/h=18,z=-20/原始数据_%r.xlsx' %phase_number, mode='w')
    dataframe_Position.to_excel(writer)
    writer.save()
path_file3 = os.path.join('E:\\','OneDrive - 同济大学','plaxis_work','PPC','全荷载','%s' %filename,'MStage.xlsx')
path_file3 = path_file3.replace('\\', '/')
writer = pd.ExcelWriter(path_file3, mode ='w')
#writer = pd.ExcelWriter('E:/OneDrive - 同济大学/plaxis_work/test/h=18,z=-20/MStage.xlsx' )  
Mstage.to_excel(writer)
writer.save()
g_o.close()  # 在output中收集完数据关闭output
