import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Importar datos (asegúrate de que la fecha sea el índice)
df = pd.read_csv('fcc-forum-pageviews.csv', parse_dates=['date'], index_col='date')

# Limpiar los datos filtrando los percentiles 2.5 superior e inferior
df = df[
    (df['value'] >= df['value'].quantile(0.025)) & 
    (df['value'] <= df['value'].quantile(0.975))
]

def draw_line_plot():
    # Dibujar gráfico de línea
    fig, ax = plt.subplots(figsize=(16, 6))
    
    ax.plot(df.index, df['value'], color='red', linewidth=1)
    ax.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    ax.set_xlabel('Date')
    ax.set_ylabel('Page Views')
    
    # Guardar imagen y devolver figura
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copiar y preparar datos para gráfico de barras
    df_bar = df.copy()
    df_bar['year'] = df_bar.index.year
    df_bar['month'] = df_bar.index.month_name()
    
    # Agrupar por año y mes, calcular promedio
    df_bar = df_bar.groupby(['year', 'month'])['value'].mean().unstack()
    
    # Ordenar meses correctamente
    month_order = [
        'January', 'February', 'March', 'April', 'May', 'June',
        'July', 'August', 'September', 'October', 'November', 'December'
    ]
    df_bar = df_bar[month_order]
    
    # Dibujar gráfico de barras
    fig = df_bar.plot(kind='bar', figsize=(10, 8)).figure
    plt.xlabel('Years')
    plt.ylabel('Average Page Views')
    plt.legend(title='Months')
    
    # Guardar imagen y devolver figura
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Preparar datos para gráficos de caja
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = df_box['date'].dt.year
    df_box['month'] = df_box['date'].dt.strftime('%b')
    
    # Ordenar meses correctamente
    month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                   'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    
    # Configurar matplotlib
    fig, axes = plt.subplots(1, 2, figsize=(20, 8))
    
    # Gráfico de caja por año (Trend)
    sns.boxplot(data=df_box, x='year', y='value', ax=axes[0])
    axes[0].set_title('Year-wise Box Plot (Trend)')
    axes[0].set_xlabel('Year')
    axes[0].set_ylabel('Page Views')
    
    # Gráfico de caja por mes (Seasonality)
    sns.boxplot(data=df_box, x='month', y='value', order=month_order, ax=axes[1])
    axes[1].set_title('Month-wise Box Plot (Seasonality)')
    axes[1].set_xlabel('Month')
    axes[1].set_ylabel('Page Views')
    
    # Guardar imagen y devolver figura
    fig.savefig('box_plot.png')
    return fig
