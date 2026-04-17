import mlflow

model_path = r"./mlruns/444303097283700649/c101e5e120b745d5bfcfeca57e636398/artifacts/model"
model = mlflow.pyfunc.load_model(model_path)

# Acceder al modelo subyacente XGBoost
xgb_model = model._model_impl

print(type(xgb_model))
print(dir(xgb_model))