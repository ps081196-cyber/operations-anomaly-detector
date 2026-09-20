from core import detect_anomalies,generate_operations

def test_detector_returns_alert_columns():
    result=detect_anomalies(generate_operations(150,8),window=12,threshold=2)
    assert {"anomaly","severity","trigger_metrics"}<=set(result.columns)
    assert result.anomaly.any()
