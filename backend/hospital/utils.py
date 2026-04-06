import plotly.graph_objects as go
import plotly.express as px
from django.db.models import Count, Sum
from hospital.models import BillingRecord, Patient, Report, Appointment
import pandas as pd

def get_billing_insights_chart():
    billing_data = BillingRecord.objects.values('category').annotate(total=Sum('amount'))
    if not billing_data:
        return ""
    
    df = pd.DataFrame(list(billing_data))
    fig = go.Figure(data=[go.Pie(
        labels=df['category'], 
        values=df['total'], 
        hole=.6,
        marker_colors=['#10B981', '#F59E0B', '#3B82F6', '#EF4444']
    )])
    
    fig.update_layout(
        showlegend=False,
        margin=dict(t=0, b=0, l=0, r=0),
        height=200,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
    )
    return fig.to_html(full_html=False, config={'displayModeBar': False})

def get_patient_arrival_chart():
    # Mock data for arrivals if no real data yet
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug']
    in_patients = [20, 25, 22, 28, 24, 30, 26, 32]
    out_patients = [15, 18, 16, 20, 19, 22, 21, 24]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=months, y=in_patients, name='Patient In', line=dict(color='#10B981', width=3), mode='lines+markers'))
    fig.add_trace(go.Scatter(x=months, y=out_patients, name='Patient Out', line=dict(color='#F59E0B', width=3), mode='lines+markers'))
    
    fig.update_layout(
        margin=dict(t=10, b=20, l=30, r=10),
        height=300,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor='#E5E7EB'),
    )
    return fig.to_html(full_html=False, config={'displayModeBar': False})

def get_report_completion_chart():
    report_data = Report.objects.values('priority').annotate(count=Count('id'))
    if not report_data:
        # Default empty chart
        labels = ['Urgent', 'Moderate', 'Low']
        values = [0, 0, 0]
    else:
        df = pd.DataFrame(list(report_data))
        labels = df['priority']
        values = df['count']
        
    fig = go.Figure(data=[go.Pie(
        labels=labels, 
        values=values, 
        hole=.7,
        marker_colors=['#EF4444', '#F59E0B', '#10B981']
    )])
    
    fig.update_layout(
        showlegend=False,
        margin=dict(t=0, b=0, l=0, r=0),
        height=200,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
    )
    return fig.to_html(full_html=False, config={'displayModeBar': False})
