import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("📊 Аналітика YouTube-каналу")

uploaded_file = st.file_uploader("Завантаж CSV файл", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    
    df['date'] = pd.to_datetime(df['date'])
    
    st.write("### Дані", df.head())

    st.sidebar.header("Фільтри")

    min_date = df['date'].min()
    max_date = df['date'].max()

    date_range = st.sidebar.date_input(
        "Оберіть період",
        [min_date, max_date]
    )

    content_types = st.sidebar.multiselect(
        "Тип контенту",
        df['type'].unique(),
        default=df['type'].unique()
    )

    filtered_df = df[
        (df['date'] >= pd.to_datetime(date_range[0])) &
        (df['date'] <= pd.to_datetime(date_range[1])) &
        (df['type'].isin(content_types))
    ]

    st.write("### Відфільтровані дані", filtered_df)

    filtered_df['engagement_rate'] = (
        (filtered_df['likes'] + filtered_df['comments']) / filtered_df['views']
    )

    st.write("### Engagement Rate")
    st.write(filtered_df[['title', 'engagement_rate']])

    avg_engagement = filtered_df['engagement_rate'].mean()
    st.metric("Середній Engagement Rate", f"{avg_engagement:.2%}")

    st.write("### Перегляди по датах")
    views_by_date = filtered_df.groupby('date')['views'].sum()

    plt.figure()
    plt.plot(views_by_date.index, views_by_date.values)
    plt.xticks(rotation=45)
    st.pyplot(plt)

    st.write("### Heatmap активності")

    filtered_df['day'] = filtered_df['date'].dt.day_name()

    heatmap_data = filtered_df.pivot_table(
        values='views',
        index='day',
        columns='type',
        aggfunc='sum',
        fill_value=0
    )
    if uploaded_file: 
    filtered_df['day'] = filtered_df['date'].dt.day_name()

    heatmap_data = filtered_df.pivot_table(
    values='views',
    index='day',
    columns='type',
    aggfunc='sum',
    fill_value=0
    )
    plt.figure()
    plt.imshow(heatmap_data)
    plt.xticks(range(len(heatmap_data.columns)), heatmap_data.columns)
    plt.yticks(range(len(heatmap_data.index)), heatmap_data.index)
    plt.colorbar()
    st.pyplot(plt)
