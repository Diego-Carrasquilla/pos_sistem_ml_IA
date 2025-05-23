
def get_insights():
    insights = []

    from pos_sistem.modules.ml.fast_moving_predictor import predict_fast_products, train_model
    from pos_sistem.modules.ml.employee_efficiency_predictor import get_employee_efficiency

    try:
        df_fast = predict_fast_products(train_model())
        low_stock = df_fast[df_fast["stock"] <= 5]
        if not low_stock.empty:
            insights.append(f"{len(low_stock)} producto(s) están en riesgo de agotarse pronto.")

        df_employees = get_employee_efficiency()
        top_employee = df_employees.sort_values("efficiency_score", ascending=False).iloc[0]
        insights.append(f"El empleado más eficiente esta semana es {top_employee['employee_name']}.")

    except Exception as e:
        insights.append(f"No se pudieron cargar todas las notificaciones: {e}")

    return insights
