import json
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from .models import Prediction
from models_ai.services import extract_expense_details

def intro_view(request):
    return render(request, "predictions/intro.html")

@login_required
def predict_view(request):
    result = None
    all_predictions = Prediction.objects.filter(user=request.user).order_by('-created_at')[:5]

    if request.method == "POST":
        input_text = request.POST.get("input_value")
        # Chama o "modelo de IA"
        extraction = extract_expense_details(input_text)

        # Salva no banco de dados com campos dedicados
        prediction = Prediction.objects.create(
            user=request.user,
            input_data=input_text,
            output_data=json.dumps(extraction),
            amount=extraction['amount'],
            category=extraction['category']
        )

        result = extraction

    # Preparar dados para exibir (decodificar JSON)
    formatted_history = []
    for pred in all_predictions:
        try:
            formatted_history.append({
                'id': pred.id,
                'input': pred.input_data,
                'output': json.loads(pred.output_data),
                'date': pred.created_at
            })
        except:
            continue

    return render(request, "predictions/predict.html", {
        "result": result,
        "history": formatted_history
    })

@login_required
def dashboard_view(request):
    # Aggregating expenses by category
    expenses_by_category = (
        Prediction.objects.filter(user=request.user)
        .values("category")
        .annotate(total=Sum("amount"))
        .order_by("-total")
    )

    # Prepare data for Chart.js
    labels = [item["category"] for item in expenses_by_category]
    data = [float(item["total"] or 0) for item in expenses_by_category]

    return render(
        request,
        "predictions/dashboard.html",
        {
            "labels": json.dumps(labels),
            "data": json.dumps(data),
            "expenses": expenses_by_category,
        },
    )