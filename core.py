import numpy as np
import pandas as pd

METRICS=["throughput_units","backlog_units","defect_rate","labor_utilization"]

def generate_operations(hours=336,seed=42):
    r=np.random.default_rng(seed)
    ts=pd.date_range(end=pd.Timestamp.now().floor("h"),periods=hours,freq="h")
    shift=np.where(ts.hour<8,"Night",np.where(ts.hour<16,"Day","Evening"))
    base=np.where(shift=="Day",520,np.where(shift=="Evening",450,330))
    df=pd.DataFrame({"timestamp":ts,"shift":shift,"throughput_units":base+r.normal(0,35,hours),"backlog_units":np.maximum(0,220+r.normal(0,45,hours)),"defect_rate":np.maximum(0,r.normal(.018,.006,hours)),"labor_utilization":np.clip(r.normal(.84,.06,hours),.5,1.1)})
    points=r.choice(np.arange(30,hours),max(4,hours//50),replace=False)
    df.loc[points,"throughput_units"]*=.45
    df.loc[points,"backlog_units"]*=2.2
    df.loc[points,"defect_rate"]*=3
    return df.round(3)

def detect_anomalies(df,window=24,threshold=2.5):
    out=df.copy()
    flags=pd.DataFrame(index=out.index)
    for col in METRICS:
        mean=out[col].rolling(window,min_periods=max(6,window//3)).mean().shift(1)
        std=out[col].rolling(window,min_periods=max(6,window//3)).std().shift(1).replace(0,np.nan)
        out[f"{col}_z"]=(out[col]-mean)/std
        flags[col]=out[f"{col}_z"].abs()>=threshold
    out["anomaly"]=flags.any(axis=1)
    out["trigger_metrics"]=flags.apply(lambda row:", ".join(row.index[row]),axis=1)
    out["severity"]=pd.cut(out[[f"{m}_z" for m in METRICS]].abs().max(axis=1),[-1,threshold,3.5,float("inf")],labels=["Normal","Warning","Critical"])
    return out
