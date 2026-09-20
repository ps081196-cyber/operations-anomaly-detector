import plotly.express as px
import streamlit as st
from core import METRICS,detect_anomalies,generate_operations

st.set_page_config(page_title="Operations Anomaly Detector",page_icon="🚨",layout="wide")
st.title("🚨 Operations Anomaly Detector")
threshold=st.sidebar.slider("Detection sensitivity (z-score)",1.5,4.0,2.5,.1)
data=detect_anomalies(generate_operations(),threshold=threshold)
alerts=data[data.anomaly].sort_values("timestamp",ascending=False)
a,b,c=st.columns(3)
a.metric("Periods monitored",len(data))
b.metric("Alerts",len(alerts))
c.metric("Critical alerts",int((alerts.severity=="Critical").sum()))
metric=st.selectbox("Metric",METRICS)
fig=px.line(data,x="timestamp",y=metric,color="anomaly",title=f"{metric.replace('_',' ').title()} monitoring")
st.plotly_chart(fig,use_container_width=True)
st.subheader("Incident feed")
st.dataframe(alerts[["timestamp","shift","severity","trigger_metrics"]+METRICS],use_container_width=True)
st.download_button("Download incident log",alerts.to_csv(index=False),"operations_incidents.csv")
