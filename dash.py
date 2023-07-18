import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title='Sales Dashboard',
                   page_icon=':bar_chart:',
                   layout='wide'
                   )

# Read csv file
df = pd.read_csv('../kpi.csv')

# sidebar
st.sidebar.header('Filtros')

region = st.sidebar.multiselect(
    'Região',
    options=df['Region'].unique(),
    default=df['Region'].unique()
)
category = st.sidebar.multiselect(
    'Categoria',
    options=df['Category'].unique(),
    default=df['Category'].unique()
)

# Filters applied
df_query = df.query(
    "Region == @region & Category == @category" 
)

# MAINPAGE

# KPIs
st.title('KPIs')
st.markdown('###')

total_sales = int(df_query['Sales'].sum())
total_profit = int(df_query['Profit'].sum())
avg_sale = int(total_sales / len(df_query['Order ID'].unique()))

left_col, mid_col, right_col = st.columns(3)
with left_col:
    st.subheader('Lucro Total')
    st.subheader(f'$ {total_profit:,}')
with mid_col:
    st.subheader('Vendas Totais')
    st.subheader(f'$ {total_sales:,}')
with right_col:
    st.subheader('Preço Médio por Venda')
    st.subheader(f'$ {avg_sale:,}')

# Fig 1
total_by_category = df_query.groupby(by=['Category']).sum()[['Profit']].sort_values(by=['Profit'], ascending=True)

fig_total_by_category = px.bar(
    total_by_category,
    x=total_by_category.index,
    y='Profit',
    title='Lucro por Categoria',
    template='plotly_white',
    labels={'x': 'Categoria', 'y': 'Vendas'}
)
fig_total_by_category.update_xaxes(title='Categoria')
fig_total_by_category.update_yaxes(title='Lucro')

# Fig 2
total_by_region = df_query.groupby(by=['Region']).sum()[['Profit']].sort_values(by=['Profit'], ascending=True)

fig_total_by_region = px.bar(
    total_by_region,
    x=total_by_region.index,
    y='Profit',
    title='Lucro por Regiâo',
    template='plotly_white'
)
fig_total_by_region.update_xaxes(title='Região')
fig_total_by_region.update_yaxes(title='Vendas')

left_col, right_col = st.columns(2)
left_col.plotly_chart(fig_total_by_category, use_container_width=True)
right_col.plotly_chart(fig_total_by_region, use_container_width=True)

# Fig 3
years = df_query['order year'].unique()

filtered_df = df_query[df_query['order year'].isin(years)]

profit_by_year_month = filtered_df.groupby(['order year', 'order month'])['Profit'].sum().reset_index()


fig_profit_overtime = px.line(
    profit_by_year_month,
    x='order month',
    y='Profit',
    color='order year',
    title='Lucro Anual',
    labels={
        'order month': '<b>Mês</b>',
        'Profit': '<b>Lucro</b>',
        'order year': 'Ano'
    },
    template='plotly_white'
)

st.plotly_chart(fig_profit_overtime, use_container_width=True)

# Left Fig
sales_by_category = df_query.groupby(by=['Category']).sum()[['Sales']].sort_values(by=['Sales'], ascending=True)

category_labels =  sales_by_category.index
category_values = sales_by_category.values

fig_pie_by_category = px.pie(
    sales_by_category,
    title='Vendas por Categoria',
    values='Sales',
    names=category_labels,
    hole=0.2
)

# Mid Fig
shipping_method = df_query['Ship Mode'].value_counts()

shipping_labels =  shipping_method.index
shipping_values = shipping_method.values

fig_pie_by_shipping = px.pie(
    shipping_method,
    title='Método de Envio',
    values=shipping_values,
    names=shipping_labels,
    hole=0.2
)

# Plot all
left_col, right_col = st.columns(2)

left_col.plotly_chart(fig_pie_by_category, use_container_width=True)
right_col.plotly_chart(fig_pie_by_shipping, use_container_width=True)
