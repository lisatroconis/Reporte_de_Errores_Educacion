# -*- coding: utf-8 -*-
"""
Created on Wed Sep 28 11:27:54 2022

@author: Lisa
"""

import pandas as pd
import numpy as np

df_5w  = pd.read_excel('C:/Users/Lisa/Documents/Bases de Python/Bases Actualizables/Ciclo8/5W_Colombia_-_RMRP_2022_Consolidado OCHO_19102022.xlsx')#, sheet_name= 'Hoja')

sumissiones = pd.read_excel('C:/Users/Lisa/Documents/Bases de Python/Educación/Sumisiones.xlsx', sheet_name= 'Colombia_plan 2022')

fts = pd.read_excel("C:/Users/Lisa/Documents/Bases de Python/Educación/FTS.xlsx", sheet_name= 'Export data',header= 2)

df_api_general = pd.read_excel('C:/Users/Lisa/Documents/Bases de Python/Bases Actualizables/Ciclo8/API_Consolidado_ciclo_ocho_GENERAL_ 19102022.xlsx', sheet_name= 'Sector Nacional')
df_api_general = df_api_general[df_api_general['Sector'] == 'Educación']

#Filtros
df_5w['Mes de atención'].unique()

df_5w['_ Sector'].unique()

mes = ['08_Agosto', '09_Septiembre']

ciclo = 'Ciclo8'

sector = ['Educación']


df_5w_sector_mes = df_5w[(df_5w['_ Sector'].isin(sector))&(df_5w['Mes de atención'].isin(mes))]

sumissiones = sumissiones[sumissiones['Sector']== 'Education']
sumissiones['Socio Principal'].unique()

fts = fts[(fts['Field Cluster'] == 'Education') & (fts['Destination country'] == 'Colombia')]

#Tablas dinamicas

df_5w_sector_mes.columns

uno2 = pd.pivot_table(df_api_general, values = 'bene_nuevos',
                      columns = ['Mesdeatención'],
                      aggfunc=np.sum, fill_value=0).reset_index()
uno2.columns
uno2 = uno2.set_index('index').cumsum(axis=1)

#uno2 = uno2.reset_index()
pob_meta = 427361
#Genero columna con totales de la api y acumulado
uno2.loc['%'] = round((uno2.sum(numeric_only=True, axis=0)/pob_meta)*100,0)

col = uno2.columns

for i in col:
    for j in uno2[i]:
        uno2.loc['poblacion_meta'] = pob_meta

#re- organizar las columnas
uno2 = uno2.reindex(np.roll(uno2.index, shift=1))
    


dos = pd.pivot_table(df_5w_sector_mes, values = 'Total beneficiarios nuevos durante el mes',
                      index = 'Socio Principal Nombre', columns = ['Mes de atención'],
                      aggfunc=np.sum, fill_value=0)


#Genero columna con totales
dos['Total'] = dos.sum(axis=1)

#Ordeno los valores por su total
dos = dos.sort_values('Total',ascending=False)

#elimino las filas que tengas su total igual a cero
dos = dos.drop(dos[dos['Total']== 0].index)

#Genero una columna con los porcentajes
dos['%'] = (dos['Total']/dos['Total'].sum())* 100

#sumo solo los valores por columna
dos.loc['total'] = dos.sum(numeric_only=True, axis=0)

#uno1 = dos
#uno1.loc['%'] = uno1.sum(numeric_only = True, axis = 0)
#uno1 = dos.iloc[-1]

#Remplazo los ceros por vacios
dos = dos.replace(0, r'')

#Agrego un nuevo dataframe
uno = dos
#remplazo los espacios por nan
uno = uno.replace(r'',np.nan)

#elimino filas y columnas inecesarias
uno = uno.drop(['Total','%'], axis = 1)
uno = uno.drop(['total'], axis = 0)

#agrego mi nuevo dataframe
tres = uno

#hago el conteo por socio
uno.loc['conteo_socio'] = uno.count(numeric_only = True)

socios_proyectados = 25

col = uno.columns

#Agregar el numero de socios proyectados 
for i in col:
    for j in uno2[i]:
        uno.loc['socios_proyectados'] = socios_proyectados 


uno.loc['%'] = (uno.loc['conteo_socio']/uno.loc['socios_proyectados'])*100


#selecciono solo mi variable de contar
uno = uno.iloc[-3:]

#ajusto el orden
uno = uno.reindex(np.roll(uno.index, shift=2))


# Para aplicar la comparación 

tres = tres.reset_index()
tres = tres.iloc[0:len(tres)-1,0]
tres = tres.to_frame()
type(tres)
tres.columns

#sumissiones['Indicator Type'] == 'PiN'
tres_sumi = sumissiones.where(sumissiones['Indicator Type'] == 'PiN').pivot_table( values = 'Total Target Pin',
                      index = 'Socio Principal', columns = ['Indicator Type'],
                      aggfunc=np.sum, fill_value=0).reset_index()

tres_sumi = tres_sumi.sort_values('PiN',ascending=False)

tres_sumi['pass'] = (tres_sumi['Socio Principal'].isin(tres['Socio Principal Nombre'])) 

tres_sumi = tres_sumi[tres_sumi['pass']== False]
tres_sumi = tres_sumi.drop(['pass'], axis=1)
tres_sumi.index = np.arange(1, len(tres_sumi ) + 1)

cuatro = pd.pivot_table(df_5w_sector_mes, values = 'Total beneficiarios nuevos durante el mes',
                      index = 'Socio Principal Nombre', columns = ['Mes de atención'],
                      aggfunc=np.sum)

cuatro = cuatro.where(cuatro == 0)
cuatro = cuatro.loc[:, cuatro.notna().any()]
cuatro = cuatro.replace(np.nan,r'')
cuatro.columns
#count = (df['01_Enero'] == 0).sum()
cuatro['total'] = cuatro.isin([0]).sum(axis=1)
cuatro = cuatro[cuatro['total'] > 0]


cinco = df_5w_sector_mes.where(df_5w_sector_mes['_ Actividad Asociada'] == 'No aplica').pivot_table(values = 'Total beneficiarios nuevos durante el mes',
                      index = ['Socio Principal Nombre','_ Indicador'], columns = ['Mes de atención'],
                      aggfunc=np.sum)

#Genero columna con totales
cinco['Total'] = cinco.sum(axis=1)

#elimino las filas que tengas su total igual a cero
cinco = cinco.drop(cinco[cinco['Total']== 0].index)
cinco = cinco.reset_index()
#sumo solo los valores por columna
cinco.loc['total'] = cinco.sum(numeric_only=True, axis=0)
cinco = cinco.drop(['Total'], axis = 1) 
cinco.columns
cinco['_ Indicador']= cinco['_ Indicador'].replace(np.nan,'total')
cinco = cinco.replace(np.nan,r'')
cinco = cinco.set_index(['Socio Principal Nombre', '_ Indicador'])
#cinco = cinco.reset_index()



seis = pd.pivot_table(df_5w_sector_mes, values = ['Total beneficiarios nuevos durante el mes','Total beneficiarios alcanzados durante el mes'],
                      index = 'Socio Principal Nombre', columns = ['Mes de atención'],aggfunc=np.sum, fill_value=0)

largo = seis.shape[1]
mitad = int(largo/2)


seis.columns = [('Total beneficiarios alcanzados durante el mes 08_Agosto'),
('Total beneficiarios alcanzados durante el mes 09_Septiembre'),
('Total beneficiarios nuevos durante el mes 08_Agosto'),
('Total beneficiarios nuevos durante el mes 09_Septiembre')]

#[('Total beneficiarios alcanzados durante el mes 01_Enero'),
#('Total beneficiarios alcanzados durante el mes 02_Febrero'),
#('Total beneficiarios alcanzados durante el mes 03_Marzo'),
#('Total beneficiarios alcanzados durante el mes 04_Abril'),
#('Total beneficiarios alcanzados durante el mes 05_Mayo'),
#('Total beneficiarios alcanzados durante el mes 06_Junio'),
#('Total beneficiarios alcanzados durante el mes 07_Julio'),
#('Total beneficiarios nuevos durante el mes 01_Enero'),
#('Total beneficiarios nuevos durante el mes 02_Febrero'),
#('Total beneficiarios nuevos durante el mes 03_Marzo'),
#('Total beneficiarios nuevos durante el mes 04_Abril'),
#('Total beneficiarios nuevos durante el mes 05_Mayo'),
#('Total beneficiarios nuevos durante el mes 06_Junio'),
#('Total beneficiarios nuevos durante el mes 07_Julio')]


for i,j in zip(range(largo),range(mitad, largo)):
    #print(i,j)
    for r in range(len(seis.index)):
        if seis.iloc[r,i] < seis.iloc[r,j]:
            seis.iloc[r,i] = seis.iloc[r,i]
            seis.iloc[r,j] = seis.iloc[r,j]
            
        else:
            seis.iloc[r,i] = ' '
            seis.iloc[r,j] = ' '
            

seis = seis.reindex(columns=[('Total beneficiarios alcanzados durante el mes 08_Agosto'),
('Total beneficiarios nuevos durante el mes 08_Agosto'),
('Total beneficiarios alcanzados durante el mes 09_Septiembre'),
('Total beneficiarios nuevos durante el mes 09_Septiembre')])
                    
 #('Total beneficiarios alcanzados durante el mes 03_Marzo'),
 #('Total beneficiarios nuevos durante el mes 03_Marzo'),
 #('Total beneficiarios alcanzados durante el mes 04_Abril'),
 #('Total beneficiarios nuevos durante el mes 04_Abril'),
 #('Total beneficiarios alcanzados durante el mes 05_Mayo'),
 #('Total beneficiarios nuevos durante el mes 05_Mayo'),
 #('Total beneficiarios alcanzados durante el mes 06_Junio'),
 #('Total beneficiarios nuevos durante el mes 06_Junio'),
 #('Total beneficiarios alcanzados durante el mes 07_Julio'),
 #('Total beneficiarios nuevos durante el mes 07_Julio')])

seis.replace(" ", np.nan, inplace=True) 
  
seis.dropna(how='all', axis=1, inplace=True)
seis.dropna(how='all', axis=0, inplace=True)

siete = pd.pivot_table(sumissiones, values = 'Total Budget',
                      index = 'Socio Principal',
                      aggfunc=np.sum).reset_index()

siete = siete.sort_values('Total Budget', ascending = False).round(0)


#elimino las filas que tengas su total igual a cero
siete = siete.drop(siete[siete['Total Budget']== 0].index)

#Genero una columna con los porcentajes
siete['%'] = (siete['Total Budget']/siete['Total Budget'].sum())* 100

siete.index = np.arange(1, len(siete) + 1)

ocho = pd.pivot_table( sumissiones, values = 'Total Budget',
                      index = 'Socio Principal', columns = ['Country'],
                      aggfunc=np.sum, fill_value=0).sort_values(by='Colombia').reset_index()

#ocho['Total'] = ocho.sum(axis=1)

ocho = ocho.sort_values(by=['Colombia'],ascending = False)
#Genero una columna con los porcentajes
ocho['% about PLAN'] = round((ocho['Colombia']/ocho['Colombia'].sum())* 100,0)

fts.columns
nueve = fts[['Destination org.','Amount (US$)','Source org.']]
nueve = nueve.rename(columns={'Destination org.':'Socio Principal'})
nueve['Socio Principal'].unique()

outer_join=pd.merge(ocho, nueve, on='Socio Principal', how='outer')
outer_join['Amount (US$)']= outer_join['Amount (US$)'].replace(np.nan,0)
outer_join['Source org.']= outer_join['Source org.'].replace(np.nan,'')

outer_join.columns

# Using DataFrame.transform() method.
outer_join['%'] = round(100 * outer_join['Amount (US$)'] / outer_join.groupby('Socio Principal')['Amount (US$)'].transform('sum'),0)
outer_join['%'] = outer_join['%'].replace(100,np.nan)

outer_join['Concatenada'] = outer_join['Source org.'] + ' ' + outer_join['%'].map(str) +'%'
outer_join['Concatenada'] = outer_join['Concatenada'].replace('nan%', '', regex=True)


outer_join = outer_join.replace(np.nan,"vacio")
#outer_join2= pd.pivot_table(outer_join, 
#                      index = 'Socio Principal',aggfunc=np.sum, fill_value=0).reset_index()
 
diez = outer_join.groupby(['Socio Principal','Colombia'],as_index=False).agg({'% about PLAN': 'sum',
                        'Amount (US$)': 'sum','Concatenada': ' '.join}).replace('vacio',r'').sort_values('% about PLAN', ascending = False)

diez['Amount (US$)'] = diez['Amount (US$)'].replace(r'',0)

diez['Avances según presupuesto'] = (diez['Amount (US$)']/diez['Colombia'])*100
diez['Avances según presupuesto'] = diez['Avances según presupuesto'].replace(np.nan,0)
diez.index = np.arange(1, len(diez) + 1)

df_5w_sector_mes.columns


once = df_5w_sector_mes.where(df_5w_sector_mes['Actividad en apoyo al ETPV'] == 'No').pivot_table(values = 'Total beneficiarios nuevos durante el mes',
                      index = ['Socio Principal Nombre','Tipo de apoyo al ETPV'], columns = ['Mes de atención'],
                      aggfunc=np.sum).reset_index()
once.columns
once['tipos_count'] = once.groupby('Socio Principal Nombre')['Tipo de apoyo al ETPV'].transform('count')
once= once[once['tipos_count'] > 1]
once.dropna(how='all', axis=1, inplace=True)

if once.empty:
    print('DataFrame is empty!')
else:
    once.drop('tipos_count', axis=1, inplace = True)
    once['Total'] = once.sum(axis=1)
    once = once.replace(np.nan,r'')

Writer= pd.ExcelWriter(f"C:/Users/Lisa/Documents/Bases de Python/Bases Actualizables/{ciclo}/errores_Educacion_{mes}.xlsx")

uno.to_excel(Writer, sheet_name='socios.xlsx')
uno2.to_excel(Writer, sheet_name='evoluacion_pob.xlsx')
dos.to_excel(Writer, sheet_name='Benef_rep_5w.xlsx')
tres_sumi.to_excel(Writer, sheet_name='5WvsSumisiones.xlsx')
cuatro.to_excel(Writer, sheet_name='Socios_Repotan_Cero.xlsx')
cinco.to_excel(Writer, sheet_name='No_aplica.xlsx')
seis.to_excel(Writer, sheet_name='BEN_menvs_BEN_nuevo.xlsx')
siete.to_excel(Writer, sheet_name='Financial_traking.xlsx')
once.to_excel(Writer, sheet_name='ETPV.xlsx')
diez.to_excel(Writer, sheet_name='Avances_del_reporte.xlsx')


Writer.save()