 # Crear el modelo con la estructura proporcionada
import os
import tensorflow as tf
import xgboost as xgb

def TrainmodeloRedN(X,y):
    model = tf.keras.Sequential([
        tf.keras.layers.Dense(128, input_dim=3, activation='relu'),
        tf.keras.layers.Dropout(0.1),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dropout(0.1),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dropout(0.1),
        tf.keras.layers.Dense(64, activation='relu'),
        tf.keras.layers.Dropout(0.1),
        tf.keras.layers.Dense(1, activation='linear')
    ])
    # Compilar el modelo
    model.compile(loss='mse', optimizer=tf.keras.optimizers.Adam(learning_rate=0.001), metrics=['MAE'])
    # Entrenar el modelo con los nuevos datos
    model.fit(X, y, epochs=100, batch_size=30, validation_split=0.2)
    # Guardar el modelo entrenado
    modelo_entrenado_path = "./Anio-Mes-Dia.h5"
    model.save(modelo_entrenado_path)


def TrainXGBoost (X_train,y_train,Namedb):
    reg= xgb.XGBRegressor(n_estimators=1000,early_stopping_rounds=50,learning_rate=0.01)
    reg.fit(X_train,y_train,
       eval_set=[(X_train,y_train)], 
       verbose=100)
    model_path = "./JsonModels/model_" + str(Namedb) + "_ventas.json"
    
    if os.path.exists(model_path):
        os.remove(model_path)  # Eliminar el archivo existente
    
    reg.save_model(model_path)
    return 

def PredictXGBoost(df,Namedb):
    reg_new= xgb.Booster()
    reg_new.load_model("./JsonModels/model_"+str(Namedb)+"_ventas.json")
    X_train_dmatrix = xgb.DMatrix(df)
    predictions = reg_new.predict(X_train_dmatrix)
    predictions= predictions.tolist()
    return predictions