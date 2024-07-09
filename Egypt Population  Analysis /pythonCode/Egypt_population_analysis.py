#!/usr/bin/env python
# coding: utf-8

# ## Importing The Needed Libraries For The Project 

# In[1]:


import pandas as pd 
import numpy as np 
import json


# In[2]:


import plotly.offline as pyo
import plotly.express as px
import plotly.graph_objects as go


# In[3]:


# import plotly.io as pio
# pio.renderers.default = 'browser'


# ## Needed Functions for Data Visuialization 

# In[4]:


def draw_pie_chart(headers, data, colors = ['red','blue'], title="", width=500, height=500):
    
    fig = go.Figure(data=[go.Pie(labels=headers, values=data)])
    
    colors = colors
    fig.update_traces(hoverinfo='label', textinfo='percent', textfont_size=23, marker=dict(colors=colors, line=dict(color='white', width=0)))

    fig.update_layout(title=title, width=width, height=height)
    
    return fig


# In[5]:


def draw_table(headers, data, width=800, height=250, header_fill_color='royalblue',cell_fill_color='white'
               ,line_color='darkslategray', header_font_color='white', cell_font_color='black', cell_height=23):
    
    header = dict(values=headers, fill_color=header_fill_color, line_color=line_color, font=dict(color=header_font_color, size=14))
    cells = dict(values=data, fill_color=cell_fill_color, line_color=line_color, align=['center'], height=cell_height,font=dict(color=cell_font_color, size=14))

    fig = go.Figure(data=[go.Table(header=header, cells=cells)])
    fig.update_layout(width=width, height=height)

    return fig  


# In[6]:


def draw_stacked_bar_chart(dataset, x_axis_col, y_axis_col, hue_col, title=" ", text_auto='.2s', Text=False, text = [],
                           width=1000, height=700, ):
    
    if Text==False: 
        fig = px.bar(dataset, x=x_axis_col, y=y_axis_col, color=hue_col, title=title, text_auto=text_auto, color_discrete_map={"male": "deepskyblue", "female": "deeppink"})
        fig.update_layout(width=1000, height=700)
        return fig
        
    elif Text==True:
        # colors = ['deepskyblue','deeppink']
        fig = px.bar(dataset, x=x_axis_col, y=y_axis_col, color=hue_col, title=title, text=text, color_discrete_map={"male": "deepskyblue", "female": "deeppink"})
        fig.update_layout(width=1000, height=700)
        return fig 


# In[7]:


def draw_tree_map_with_percentage(dataset, numerical_column, categorical_column, palette = px.colors.qualitative.Dark2,
                                 title=" ", width=1100, height=900) :
    percentage_list = []
    total = sum(dataset[numerical_column])

    for i in range (0, len(dataset[categorical_column]),1) :
        x = round((dataset[numerical_column][i]/total)*100,2)
        percentage_list.append(str(x)+" %")

    fig = px.treemap(dataset, path=[dataset[categorical_column], percentage_list],
                 values=numerical_column, color_discrete_sequence=palette)
    
    fig.update_layout(title=title, font=dict(family="Calibr",size=20), width=width, height=height)

    return fig


# ### Uploading popultion dataset for each governorate in Egypt

# In[8]:


location  = "F:\\FCDS SAM 6\\Data Visuialization\\Data Visualization Ptoject\\Dataset\\popultion\\Egypt_popultion.csv"
egypt_popultion_df = pd.read_csv(location)


# ## Applying EDA 

# ## Data Inspection

# - Data Discovering 

# In[9]:


egypt_popultion_df.head()


# - Checking if there are Null Values 

# In[10]:


egypt_popultion_df.isnull().sum()


# - Checking if there are  data type error 

# In[11]:


egypt_popultion_df.info()


# ## Uploading GeoJson Of Egypt Governorates`

# In[12]:


Egypt_states = json.load(open('F:\\FCDS SAM 6\\Data Visuialization\\Data Visualization Ptoject\\Json Files\\egypt-with-regions_1438.geojson', 
                              'r', encoding='utf-8'))


# In[13]:


state_id_map = {}
for feature in Egypt_states["features"]:
    feature["id"] = feature["properties"]["ID_1"]
    state_id_map[feature["properties"]["NAME_1"]] = feature["id"]


# ## Visualization of popultion density in each governorate in Egypt 

# In[14]:


egypt_popultion_df["DensityScale"] = np.log10(egypt_popultion_df["Total Popultion"])


# ## Visualization of popultion density in each governorate in Egypt 

# In[15]:


fig = px.choropleth_mapbox(
    egypt_popultion_df,
    locations="id",
    geojson=Egypt_states,
    color="DensityScale",
    hover_name="governorate",
    hover_data=["Total Popultion"],
    title="Egypt Population Density",
    mapbox_style="carto-positron",
    center={"lat": 24, "lon": 78},
    zoom=3,
    opacity=0.5,
)

fig.update_layout( width = 1000, height = 700)

fig.show()


# ## Some Question On Population Denesity In Each Governorate In Egypt  :-

# In[16]:


egypt_popultion_df.columns


# In[17]:


np.array(egypt_popultion_df['governorate'])


# In[18]:


governorates_that_locate_on_nile_river =['Luxor', 'Aswan', 'Qena', 'Suhag', 'Asyout', 'Menia', 'Fayoum',  'Beni Suef', 'Giza', 'Behera',
                                        'Menoufia', 'Gharbia', 'Kafr El-Shikh', 'Kalyoubia', 'Sharkia', 'Dakahlia', 'Damietta']

governorates_that_locate_on_nile_river_with_cairo =['Luxor', 'Aswan', 'Qena', 'Suhag', 'Asyout', 'Menia', 'Fayoum',  'Beni Suef', 'Giza', 'Behera',
                                        'Menoufia', 'Gharbia', 'Kafr El-Shikh', 'Kalyoubia', 'Sharkia', 'Dakahlia', 'Damietta', 'Cairo']

suez_canel_governorate = ['Port Said', 'Suez','Ismailia']

other_governorate = ['Red Sea','New Valley','Matrouh','North Sinai', 'South Sinai']


# In[19]:


total_population_density =  sum(egypt_popultion_df['Total Popultion'])


# ### Q1 ) How many people live in governorates that located on nile river ?

# In[20]:


total_density_on_nile_river = sum(egypt_popultion_df.set_index('governorate').loc[governorates_that_locate_on_nile_river_with_cairo]['Total Popultion'])


# In[21]:


total_density_on_nile_river


# In[22]:


total_density_on_nile_river = sum(egypt_popultion_df.set_index('governorate').loc[governorates_that_locate_on_nile_river]['Total Popultion'])


# ### Q2 ) What is the percentage of people who live in governorates that located on nile river ?

# In[23]:


percentage_of_nile_governorate = round((total_density_on_nile_river/total_population_density)*100,2)
percentage_of_nile_governorate


# ### Q3) How many people live in governorates that located on suez canel in Egypt ? 

# In[24]:


total_density_on_suez_canel = sum(egypt_popultion_df.set_index('governorate').loc[suez_canel_governorate]['Total Popultion'])
total_density_on_suez_canel


# ### Q4) What is the percentage of people who live in governorates that located on suez canel in Egypt ? 

# In[25]:


percentage_of_suez_canel_governorate = round((total_density_on_suez_canel/total_population_density)*100,2)
percentage_of_suez_canel_governorate


# ### Q5) How many people who live in the capitial city in Egypt?

# In[26]:


total_density_in_cairo = sum(egypt_popultion_df.set_index('governorate').loc[['Cairo']]['Total Popultion'])
total_density_in_cairo


# ### Q6) What is the percentage of people who live in the capitial city in Egypt ? 

# In[27]:


percentage_of_cairo_governorate = round((total_density_in_cairo/total_population_density)*100,2)
percentage_of_cairo_governorate


# ### Q7) How many people who live in the second capitial city in Egypt?

# In[28]:


total_density_in_alexindria = sum(egypt_popultion_df.set_index('governorate').loc[['Alexandria']]['Total Popultion'])
total_density_in_alexindria


# ### Q8) What is the percentage of people who live in the second capitial city in Egypt ? 

# In[29]:


percentage_of_alexindria_governorate = round((total_density_in_alexindria/total_population_density)*100,2)
percentage_of_alexindria_governorate


# ## Visuializing The Answerd Questions

# In[30]:


total_density_in_other = sum(egypt_popultion_df.set_index('governorate').loc[other_governorate]['Total Popultion'])
labels = ['Nile Governorates (exculding Cairo)', 'Suez Canel Governorates', 'Cairo', 'Alexindria', '[Red Sea, New Valley, Matrouh, North Sinai, South Sinai]']
total  = [total_density_on_nile_river, total_density_on_suez_canel, total_density_in_cairo, total_density_in_alexindria, total_density_in_other]

draw_pie_chart(labels, total, colors = [px.colors.qualitative.Light24[0], px.colors.qualitative.Light24[1], 
                                        px.colors.qualitative.Light24[2], px.colors.qualitative.Light24[3],px.colors.qualitative.Light24[5] ],
title="Population Density Disturbution In Egypt", width=900, height=550)


# ## Uploading Gender Dataset In Each Governorate In Egypt :-

# In[31]:


egypt_genders = pd.read_csv('F:\FCDS SAM 6\Data Visuialization\Data Visualization Ptoject\Dataset\Gender dataset\Egypt_genders.csv')


# In[32]:


egypt_genders_df_list = []
for i in range(0, len(egypt_genders.columns), 1):
    egypt_genders_df_list.append(egypt_genders[egypt_genders.columns[i]])


# In[33]:


draw_table(['Governorate', 'Total Males', 'Total Females'], egypt_genders_df_list, width=1000, height=700,cell_height=24)


# ## Applying Gender Analysis :-

# #### Adding 2 new features for applying gender analysis.

# In[34]:


egypt_genders['Total'] = egypt_genders['male'] + egypt_genders['female']


# In[35]:


egypt_genders['male_percentage'] =  round((egypt_genders['male'] / egypt_genders['Total'])*100,2)
egypt_genders['female_percentage'] =  round((egypt_genders['female'] / egypt_genders['Total'])*100,2)


# In[36]:


egypt_genders_df_list = []
for i in range(0, len(egypt_genders.columns), 1):
    egypt_genders_df_list.append(egypt_genders[egypt_genders.columns[i]])
draw_table(egypt_genders.columns, egypt_genders_df_list, width=1000, height=700,cell_height=24)


# #### Creating new dataset by using the previous dataset for apply gender analysis.

# In[37]:


governorate_list = []
gender_list = []
gender_density = []

for i in range(0, len(egypt_genders['governorate']), 1):
    governorate_list.append(egypt_genders['governorate'][i])
    gender_list.append('male')
    gender_list.append('female')
    gender_density.append(egypt_genders['male'][i])
    gender_density.append(egypt_genders['female'][i])
    governorate_list.append(egypt_genders['governorate'][i])
    


# In[38]:


gender_egy_dict = {"governorate":governorate_list,
                  "gender":gender_list,
                  "population":gender_density}
gender_egy_df = pd.DataFrame(gender_egy_dict)


# In[39]:


gender_egy_df.head()


# # Showing Gender Analysis Insights 

# ## Male vs Females percentage in Egypt

# In[40]:


gender_labels = ['male', 'female']
gender_sum = [sum(egypt_genders['male']), sum(egypt_genders['female'])]


# In[41]:


draw_pie_chart(gender_labels, gender_sum, colors = ['deepskyblue','deeppink'],title="Male vs Females percentage in Egypt", width=700, height=500)


# ## Total Males VS Total Females in Egypt

# In[42]:


total_males_in_Egypt = sum(egypt_genders['male'])
total_females_in_Egypt = sum(egypt_genders['female']) 

added_item = " \tPerson"
data= [[str(total_males_in_Egypt)+added_item],[str(total_females_in_Egypt)+added_item]]

draw_table(['Total Males In Egypt', 'Total Females In Egypt'], data)


# ## (Total Males) vs (Total Females) In Each Governorate In Egypt

# In[43]:


draw_stacked_bar_chart(gender_egy_df, "governorate", "population", "gender", "(Total Males) vs (Total Females) In Each Governorate In Egypt", width=200, height=300)


# ## (Percentage of Males) vs (Percentage of Females) In Each Governorate In Egypt

# In[44]:


gender_percentage = []
for i in range(0, len(egypt_genders['governorate']),1) :
    gender_percentage.append(egypt_genders['male_percentage'][i])
    gender_percentage.append(egypt_genders['female_percentage'][i])

def add_percent(x):
    return str(x)+" %"
gender_percentage = list(map(add_percent, gender_percentage))


# In[45]:


draw_stacked_bar_chart(gender_egy_df, "governorate", "population", "gender",
                       "(Percentage of Males) vs (Percentage of Females) In Each Governorate In Egypt", Text=True, text=gender_percentage )


# ## Uploading GDP Dataset For Each Governorate In Egypt

# In[46]:


governorate_gdp = pd.read_csv("F:\FCDS SAM 6\Data Visuialization\Data Visualization Ptoject\Dataset\GDP DATA\GDP by Governorate (3).csv")


# #### Applying Data Inspection Processes On GDP Dataset For Each Governorate In Egypt

# In[47]:


governorate_gdp.info()


# In[48]:


governorate_gdp.duplicated().sum()


# ##### Conc, After Applying Data Inspection Processes On GDP Dataset For Each Governorate In Egypt :- 
# ##### The Datasetno null values, duplicated value, or data type error 

# ## GDP Dataset 

# In[49]:


government_gdp_df_list = []
for i in range(0, len(governorate_gdp.columns), 1):
    government_gdp_df_list.append(governorate_gdp[governorate_gdp.columns[i]])


# In[50]:


draw_table(governorate_gdp.columns, government_gdp_df_list, width=1000, height=700,cell_height=24)


# ## Manufacturing Industries For Each Governorate In Egypt

# In[51]:


draw_tree_map_with_percentage(governorate_gdp, 'Manufacturing Industries', 'Governorate', px.colors.qualitative.Plotly, 
                             title = 'Manufacturing Industries For Each Governorate In Egypt', height=770)


# ## Manufacturing Industries In [Cairo, Giza, Alexandria] vs Other Governorates

# In[52]:


filtered_df_1 = governorate_gdp.loc[ (governorate_gdp['Governorate'] == 'Cairo') |
(governorate_gdp['Governorate'] == 'Alexandria') | (governorate_gdp['Governorate'] == 'Giza')]

filtered_df_2 = governorate_gdp.loc[(governorate_gdp['Governorate'] != 'Cairo') & 
(governorate_gdp['Governorate'] != 'Alexandria') & (governorate_gdp['Governorate'] != 'Giza')]

governorates_labels = ['[Cairo, Giza, Alexandria]', 'OTHER Governorates']
governorates_sum = [sum(filtered_df_1['Manufacturing Industries']), sum(filtered_df_2['Manufacturing Industries'])]

draw_pie_chart(governorates_labels, governorates_sum, colors = [px.colors.qualitative.Plotly[0], px.colors.qualitative.Plotly[2]],
title="Manufacturing industries in [Cairo, Giza, Alexandria] vs  Other Governorates", width=900, height=550)


# In[53]:


added_item = " Pound"
governorates_sum = [str(sum(filtered_df_1['Manufacturing Industries']))+added_item, str(sum(filtered_df_2['Manufacturing Industries']))+added_item]
draw_table(governorates_labels, governorates_sum)


# ## What is the percentage of suez canel governorates from total Manufacturing Industries

# In[54]:


total_manufacturing = sum(governorate_gdp['Manufacturing Industries'])


# In[55]:


suez_canel_manufacturing = sum(governorate_gdp.set_index('Governorate').loc[suez_canel_governorate]['Manufacturing Industries'])
suez_canel_manufacturing


# In[56]:


other_governorate  = total_manufacturing - suez_canel_manufacturing


# In[57]:


draw_pie_chart(['Suez Canel Governorates', 'OTHER Governorates'], [suez_canel_manufacturing, other_governorate], colors = [px.colors.qualitative.Plotly[2], px.colors.qualitative.Plotly[0]],
title="Manufacturing Industries In Suez Canel Governorates vs OTHER Governorates", width=900, height=550)


# ## Percentage Of Each Governorate From Consumed Water In Egypt

# In[58]:


draw_tree_map_with_percentage(governorate_gdp, 'Water', 'Governorate', px.colors.qualitative.Plotly, 
                             title = 'Percentage Of Each Governorate From Consumed Water In Egypt', height=760)


# ## Water Consumed by [Cairo, Giza, Alexandria, Beheira] vs Other Governorates

# In[59]:


filtered_df_1 = governorate_gdp.loc[(governorate_gdp['Governorate'] == 'Beheira') | (governorate_gdp['Governorate'] == 'Cairo') | 
(governorate_gdp['Governorate'] == 'Alexandria') | (governorate_gdp['Governorate'] == 'Giza')]

filtered_df_2 = governorate_gdp.loc[(governorate_gdp['Governorate'] != 'Beheira') & (governorate_gdp['Governorate'] != 'Cairo') & 
(governorate_gdp['Governorate'] != 'Alexandria') & (governorate_gdp['Governorate'] != 'Giza')]

governorates_labels = ['[Cairo, Giza, Alexandria, Beheira]', 'OTHER Governorates']
governorates_sum = [sum(filtered_df_1['Water']), sum(filtered_df_2['Water'])]

draw_pie_chart(governorates_labels, governorates_sum, colors = ['#EF553B', '#636EFA'],
title="Water Consumed by [Cairo, Giza, Alexandria, Beheira] vs OTHER Governorates", width=900, height=550)


# In[60]:


added_item = " CCF"
governorates_sum = [str(sum(filtered_df_1['Water']))+added_item, str(sum(filtered_df_2['Water']))+added_item]
draw_table(governorates_labels, governorates_sum)


# ## Total popultion in [Cairo, Giza, Alexandria, Beheira] vs Other Governorates

# In[61]:


filtered_df_1 = egypt_popultion_df.loc[(egypt_popultion_df['governorate'] == 'Behera') | (egypt_popultion_df['governorate'] == 'Cairo') | 
(egypt_popultion_df['governorate'] == 'Alexandria') | (egypt_popultion_df['governorate'] == 'Giza')]

filtered_df_2 = egypt_popultion_df.loc[(egypt_popultion_df['governorate'] != 'Behera') & (egypt_popultion_df['governorate'] != 'Cairo') & 
(egypt_popultion_df['governorate'] != 'Alexandria') & (egypt_popultion_df['governorate'] != 'Giza')]

governorates_labels = ['[Cairo, Giza, Alexandria, Beheira]', 'Other governorates']
governorates_sum = [sum(filtered_df_1['Total Popultion']), sum(filtered_df_2['Total Popultion'])]

draw_pie_chart(governorates_labels, governorates_sum, colors = ['#EF553B', '#636EFA'],
title="Total popultion in [Cairo, Giza, Alexandria, Beheira] vs Other Governorates", width=900, height=550)


# In[62]:


added_item = " Person"
governorates_sum = [str(sum(filtered_df_1['Total Popultion']))+added_item, str(sum(filtered_df_2['Total Popultion']))+added_item]
draw_table(governorates_labels, governorates_sum)


# ## Percentage Of Each Governorate From Egyp Financial Budget For Education 

# In[63]:


draw_tree_map_with_percentage(governorate_gdp, 'Education', 'Governorate', px.colors.qualitative.Set3, 
                             title = 'Percentage Of Each Governorate From Egyp Financial Budget For Education', height=750)


# ### Percentage Of [Cairo, Giza, Alexandria] From Egypt Financial Budget For Education vs Other Governorates

# In[64]:


filtered_df_1 = governorate_gdp.loc[ (governorate_gdp['Governorate'] == 'Cairo') |
(governorate_gdp['Governorate'] == 'Alexandria') | (governorate_gdp['Governorate'] == 'Giza')]

filtered_df_2 = governorate_gdp.loc[(governorate_gdp['Governorate'] != 'Cairo') & 
(governorate_gdp['Governorate'] != 'Alexandria') & (governorate_gdp['Governorate'] != 'Giza')]

governorates_labels = ['[Cairo, Giza, Alexandria]', 'OTHER Governorates']
governorates_sum = [sum(filtered_df_1['Education']), sum(filtered_df_2['Education'])]

draw_pie_chart(governorates_labels, governorates_sum, colors = [px.colors.qualitative.Light24[6], px.colors.qualitative.Set3[4]],
title="Total Eduction Budget [Cairo, Giza, Alexandria, Beheira] vs OTHER Governorates", width=900, height=550)


# In[65]:


added_item = " Pound"
governorates_sum = [str(sum(filtered_df_1['Education']))+added_item, str(sum(filtered_df_2['Education']))+added_item]
draw_table(governorates_labels, governorates_sum)


# ## Profit Institutions Serving House Hold Sector In Each Governorate In Egypt

# In[66]:


draw_tree_map_with_percentage(governorate_gdp, 'Non Profit Institutions Serving House hold Sector', 'Governorate', px.colors.qualitative.Bold, 
                             title = 'Profit Institutions Serving House Hold Sector In Each Governorate In Egypt', height=750)


# ## GDP For Each Governorate In Egypt 

# In[67]:


draw_tree_map_with_percentage(governorate_gdp, 'Total Governorate GDP', 'Governorate', px.colors.qualitative.Light24, 
                             title = 'GDP For Each Governorate In Egypt', height=750)


# ## Percentage Of [Cairo, Giza, Alexandria] GDP vs Other Governorates 

# In[68]:


filtered_df_1 = governorate_gdp.loc[ (governorate_gdp['Governorate'] == 'Cairo') |
(governorate_gdp['Governorate'] == 'Alexandria') | (governorate_gdp['Governorate'] == 'Giza')]

filtered_df_2 = governorate_gdp.loc[(governorate_gdp['Governorate'] != 'Cairo') & 
(governorate_gdp['Governorate'] != 'Alexandria') & (governorate_gdp['Governorate'] != 'Giza')]

governorates_labels = ['[Cairo, Giza, Alexandria]', 'OTHER Governorates']
governorates_sum = [sum(filtered_df_1['Total Governorate GDP']), sum(filtered_df_2['Total Governorate GDP'])]

draw_pie_chart(governorates_labels, governorates_sum, colors = [px.colors.qualitative.Light24[0], px.colors.qualitative.Light24[6]],
title="Percentage Of [Cairo, Giza, Alexandria] GDP vs OTHER Governorates", width=900, height=550)


# In[69]:


added_item = " Pound"
governorates_sum = [str(sum(filtered_df_1['Total Governorate GDP']))+added_item, str(sum(filtered_df_2['Total Governorate GDP']))+added_item]
draw_table(governorates_labels, governorates_sum)


# ## Health Budget For Each Governorate In Egypt 

# In[70]:


health_data = pd.read_csv("F:\FCDS SAM 6\Data Visuialization\Data Visualization Ptoject\Dataset\Health\Governorate_health_budget.csv")


# In[71]:


health_data_list = []
for i in range(0, len(health_data.columns), 1):
    health_data_list.append(health_data[health_data.columns[i]])

draw_table(health_data.columns, health_data_list, width=1000, height=700,cell_height=24)


# ## Applying Data Inspection Processes

# In[73]:


health_data.info()


# In[74]:


health_data.duplicated().sum()


# ##### After Applying Data Inspection Processes There Is No Null Values, Duplicated Values or Data Type Errors  

# ## Health Budget For Each Governorate In Egypt

# In[75]:


draw_tree_map_with_percentage(health_data, 'Health', 'Governorate', px.colors.qualitative.Dark24, 
                             title = 'Health Budget For Each Governorate In Egypt', height=750)


# ## Percentage Of [Cairo, Giza, Alexandria] Health Budget vs Other Governorates

# In[76]:


filtered_df_1 = health_data.loc[ (health_data['Governorate'] == 'Cairo') |
(health_data['Governorate'] == 'Alexandria') | (health_data['Governorate'] == 'Giza')]

filtered_df_2 = health_data.loc[(health_data['Governorate'] != 'Cairo') & 
(health_data['Governorate'] != 'Alexandria') & (health_data['Governorate'] != 'Giza')]

governorates_labels = ['[Cairo, Giza, Alexandria]', 'OTHER Governorates']
governorates_sum = [sum(filtered_df_1['Health']), sum(filtered_df_2['Health'])]

draw_pie_chart(governorates_labels, governorates_sum, colors = [px.colors.qualitative.Light24[1], px.colors.qualitative.Light24[2]],
title="Percentage Of [Cairo, Giza, Alexandria] Health Budget vs OTHER Governorates", width=900, height=550)


# In[77]:


added_item = " Pound"
governorates_sum = [str(sum(filtered_df_1['Health']))+added_item, str(sum(filtered_df_2['Health']))+added_item]
draw_table(governorates_labels, governorates_sum)

