import pandas as pd
import plotly.graph_objects as go
import gui

def plot(df):
    # Convert 'dates' column to datetime
    df.index = pd.to_datetime(df.index)

    fig = go.Figure()

    # Add candlestick chart
    fig.add_trace(go.Candlestick(x=df.index,
                                open=df['opens'],
                                high=df['highs'],
                                low=df['lows'],
                                close=df['closes'],
                                name='Candlestick',
                                increasing_line_color='green',
                                decreasing_line_color='red'))

    # Customize the layout
    fig.update_layout(
        title='Candlestick Chart - TradingView Style',
        xaxis_title='Date',
        yaxis_title='Price',
        xaxis_rangeslider_visible=False,
        font=dict(size=12),
        plot_bgcolor='rgba(240, 240, 240, 1)',
        xaxis=dict(gridcolor='rgba(180, 180, 180, .5)'),
        yaxis=dict(gridcolor='rgba(180, 180, 180, .5)'),
        margin=dict(l=20, r=20, t=50, b=20),
    )

    # Customize the axis labels and background colors
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='rgba(180, 180, 180, .5)', showline=True, linewidth=1, linecolor='rgba(0, 0, 0, .5)', mirror=True, ticks='outside')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='rgba(180, 180, 180, .5)', showline=True, linewidth=1, linecolor='rgba(0, 0, 0, .5)', mirror=True, ticks='outside')

    fig.show()