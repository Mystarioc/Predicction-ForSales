import os
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
import jwt 
import tensorflow as tf
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
import joblib
import numpy as np
import pandas as pd
import xgboost as xgb
import models.ModelsPrediccion,models.ventasModels,config.MysqlConecction
import Controllers.VentasPredic_Controller


app = FastAPI()

origins = ["*"]  # Aceptar conexiones desde cualquier origen (cuidado en producción)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Load the model only once during application startup


# Endpoint para cargar y procesar la imagen
@app.post("/PrediccionVentas")

def process_date(fechas: models.ventasModels.FechasInput):
    fechaInicio = fechas.fechaInicio
    fechaFin = fechas.fechaFin
    df=Controllers.VentasPredic_Controller.completeRangeData(fechaInicio,fechaFin)
    df=Controllers.VentasPredic_Controller.create_feature(df)
    df= Controllers.VentasPredic_Controller.create_X_y_Pred(df)
    prediction= models.ModelsPrediccion.PredictXGBoost(df,fechas.Namedb)
 
    # Las predicciones serán valores numéricos, que puedes redondear o interpretar según el contexto
    return prediction

@app.post("/EntrenarModelo")
def train_model(Cred:models.ventasModels.CredencialesDatosEntrenamiento):
    
    consulta = "SELECT DOCU_FECFAC AS DAY,ROUND(SUM(DOCU_TOTALX)) AS TOTALX FROM vista_ventas WHERE DOCU_ESTADO = 'EMITIDA' AND DOCU_TIPOXX = 'FACTURA ELECTRONICA' GROUP BY YEAR(DOCU_FECFAC), DOCU_FECFAC";

    df=config.MysqlConecction.ConecctionDatabase(consulta,Cred.Namedb,Cred.usuario,Cred.contra)

    print(df)
    df= Controllers.VentasPredic_Controller.create_feature(df)
    X_train,y_train= Controllers.VentasPredic_Controller.create_X_y_Train(df)
    try:
        models.ModelsPrediccion.TrainXGBoost(X_train,y_train,Cred.Namedb)
    except:
        return "A ocurrido un error al entrenar el modelo"
   
    return "modelo entrenado con exito"


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
