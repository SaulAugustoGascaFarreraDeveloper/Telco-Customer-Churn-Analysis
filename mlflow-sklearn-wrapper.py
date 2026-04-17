import mlflow

model_path = r"./mlruns/444303097283700649/c101e5e120b745d5bfcfeca57e636398/artifacts/model"
model = mlflow.pyfunc.load_model(model_path)

# Acceder al modelo sklearn subyacente
sklearn_model = model._model_impl.sklearn_model

print(type(sklearn_model))

# Intentar extraer feature names
if hasattr(sklearn_model, 'feature_names_in_'):
    print("\nfeature_names_in_:")
    print(list(sklearn_model.feature_names_in_))
    
if hasattr(sklearn_model, 'get_booster'):
    print("\nget_booster().feature_names:")
    print(sklearn_model.get_booster().feature_names)

# Si es un Pipeline, el modelo real está adentro
if hasattr(sklearn_model, 'steps'):
    print("\nEs un Pipeline, steps:", [s[0] for s in sklearn_model.steps])
    final_estimator = sklearn_model.steps[-1][1]
    if hasattr(final_estimator, 'feature_names_in_'):
        print(list(final_estimator.feature_names_in_))
    if hasattr(final_estimator, 'get_booster'):
        print(final_estimator.get_booster().feature_names)