# Operations Anomaly Detector

A real-time-style monitoring dashboard that detects unusual changes in fulfillment throughput, backlog, defect rate and labor utilization.

## Operational use
Supervisors can review the alert feed during shift meetings, identify abnormal periods and focus investigation on the metric with the strongest deviation.

## Features
- Synthetic hourly operations stream
- Rolling z-score anomaly detection
- Configurable sensitivity
- KPI monitoring and severity-based alerts
- Downloadable incident log
- Unit tests for detection behavior

## Run
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Technology
Python · pandas · NumPy · Streamlit · Plotly · pytest

Original implementation using synthetic operational data.
