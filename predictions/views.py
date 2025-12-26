from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Prediction
from models_ai.services import simple_ai_model

@login_required
def predict_view(request):
    result = None

    if request.method == "POST":
        input_value = float(request.POST.get("input_value"))
        output_value = simple_ai_model(input_value)

        prediction = Prediction.objects.create(
            user=request.user,
            input_data=str(input_value),
            output_data=str(output_value)
        )

        result = output_value

    return render(request, "predictions/predict.html", {
        "result": result
    })