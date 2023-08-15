import pandas as pd
import numpy as np
from datetime import timedelta

def create_feature(df):
    # Create time series
    df=df.copy()
    df= df.set_index('DAY')
    df['dayofweek']= df.index.dayofweek
    df['quarter']= df.index.quarter
    df['month']= df.index.month
    df['year']= df.index.year
    df['dayofyear']= df.index.dayofyear
    return df


def create_X_y_Pred(df):
    FEATURES=['dayofweek','quarter','month','year','dayofyear']
    X_Pred= df[FEATURES]
    return X_Pred

def create_X_y_Train(df):
    FEATURES=['dayofweek','quarter','month','year','dayofyear']
    TARGET='TOTALX'
    X_pred= df[FEATURES]
    y_pred= df[TARGET]
    return X_pred,y_pred

def completeRangeData(fechaInicio,fechaFin):
    if fechaInicio > fechaFin:
        fechaInicio, fechaFin = fechaFin, fechaInicio
    delta = fechaFin - fechaInicio
    rango_fechas = [fechaInicio + timedelta(days=i) for i in range(delta.days + 1)]
    
    # Crear un DataFrame a partir de la lista de fechas
    df = pd.DataFrame({'DAY': rango_fechas})
    df['DAY'] = pd.to_datetime(df['DAY'])
    return df