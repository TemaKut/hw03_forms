from datetime import date


def year(request):
    """Добавляет переменную с текущим годом."""
    y = date.today()
    return {
        'year': y.year
    }
