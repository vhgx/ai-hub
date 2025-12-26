import json
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
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

        # Salva no banco de dados como JSON
        prediction = Prediction.objects.create(
            user=request.user,
            input_data=input_text,
            output_data=json.dumps(extraction)
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