# plaxis_post-processing
import  datetime
import numpy as np
import pandas as pd
import re
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from scipy.integrate import quad

start_time = datetime.datetime.now()
print('程序开始时间：%s' % (start_time))
V = 1053
M = 122907

def add(arr, firstdata, lastdata):
        arr = np.insert(arr, 0 ,firstdata)
        arr = np.insert(arr, len(arr) ,lastdata)
        return arr
def shear_force(arr_height, arr_ps, V_o):
    f = interp1d(arr_height, arr_ps, kind='nearest')
    def integral(x):
        return quad(f, arr_height[0], x)[0]
    ShearForce_list = V_o - [integral(x) for x in arr_height]
    return ShearForce_list
file_path = 'E:/OneDrive - 同济大学/plaxis_work/PPC/全荷载/h=15/P-Y.xlsx'
MStage_path = 'E:/OneDrive - 同济大学/plaxis_work/PPC/全荷载/h=15/MStage.xlsx'
P_Y = pd.read_excel(file_path, index_col=[0,1])
df_MStage = pd.read_excel(MStage_path, index_col=[0], header=[0])
height = [re.findall(r'-?\d+\.?\d*', row)[0] for row in P_Y.index.get_level_values(0) if 'Height' in row]
deepth = list(sorted(set([float(i) for i in height]),reverse=True))
deepth = np.array([round(float(x), 3) for x in deepth])
#deepth = add(deepth, 0, int(deepth[-1])-1)
Step_number =  [int(re.findall(r'\d+', col)[0]) for col in P_Y.columns.get_level_values(0) if 'step' in col]

Height = np.linspace (0, 15, 31)
Df_ShearForce = pd.DataFrame(Height)
Df_Moment = pd.DataFrame(Height)
thickness_list = []
for i in range(0,len(Height)-1):
    Height_i = Height[i] - Height[i+1]
    thickness_list.append(Height_i)
    thickness_list = [round(x, 3) for x in thickness_list]
thickness_array = np.abs(np.array(thickness_list))

for i in Step_number:
    P_Y_step = P_Y['step_%r' %i]
    p_array = np.array(P_Y_step.loc[(slice(None),'P')])
    m_array = np.array(P_Y_step.loc[(slice(None),'m_dis')])
    s_array = np.array(P_Y_step.loc[(slice(None),'P_S')])
    p_array_add = np.insert(p_array, 0 ,(3* p_array[0] - p_array[1])/2)
    s_array_add = np.insert(s_array, 0 ,(3* s_array[0] - s_array[1])/2)
    deepth_add  = np.insert(deepth, 0 ,0)
    thickness_array_add = np.insert(thickness_array, 0 ,0)
    V_step  = df_MStage.iloc[-1]['step_%r' %i]*V
    M_step  = df_MStage.iloc[-1]['step_%r' %i]*M
    ShearForce_step = pd.DataFrame(shear_force(abs(deepth_add), s_array_add+p_array_add, V_step))
    Df_ShearForce = pd.concat((Df_ShearForce, ShearForce_step), axis=1)
    #Moment_step = pd.DataFrame(Moment(p_array_add, s_array_add, thickness_array_add, Height, V_step, M_step))
    #Df_Moment = pd.concat((Df_Moment, Moment_step), axis=1)
    
writer = pd.ExcelWriter('E:/plaxis_work/PPC/全荷载/h=15/ShearForce.xlsx', mode='w')
Df_ShearForce.to_excel(writer)
writer.save()

end_time = datetime.datetime.now()
print('程序结束时间：%s' % (end_time))
print('程序所用时间：%s' % (end_time - start_time))
