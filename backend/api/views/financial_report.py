from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Sum, Count
from django.db.models.functions import TruncMonth
from ..models import CustomerCourse, Course, Language
from datetime import datetime

@api_view(['GET'])
def financial_report(request):
    start_date = request.query_params.get('start_date')
    end_date = request.query_params.get('end_date')

    # Фильтруем курсы по датам
    courses = CustomerCourse.objects.filter(
        payment_date__range=[start_date, end_date]
    )

    # Общая сумма оплат
    total_payments = courses.filter(payment_status=True).aggregate(
        total=Sum('course__price')
    )['total'] or 0

    # Процент оплаченных курсов
    total_courses = courses.count()
    paid_courses = courses.filter(payment_status=True).count()
    paid_percentage = (paid_courses / total_courses * 100) if total_courses > 0 else 0

    # Статистика по языкам
    language_stats = []
    for language in Language.objects.all():
        amount = courses.filter(
            course__language=language,
            payment_status=True
        ).aggregate(total=Sum('course__price'))['total'] or 0
        
        if amount > 0:
            language_stats.append({
                'language': language.name,
                'amount': float(amount)
            })

    # Статистика по месяцам
    monthly_stats = courses.filter(
        payment_status=True
    ).annotate(
        month=TruncMonth('payment_date')
    ).values('month').annotate(
        amount=Sum('course__price')
    ).order_by('month')

    monthly_stats = [{
        'month': item['month'].strftime('%B %Y'),
        'amount': float(item['amount'])
    } for item in monthly_stats]

    # Детальные данные
    detailed_data = []
    for course_payment in courses:
        detailed_data.append({
            'date': course_payment.payment_date.strftime('%d.%m.%Y') if course_payment.payment_date else None,
            'course': course_payment.course.name,
            'language': course_payment.course.language.name,
            'amount': float(course_payment.course.price),
            'status': course_payment.payment_status
        })

    return Response({
        'total_payments': float(total_payments),
        'paid_percentage': round(paid_percentage, 2),
        'language_stats': language_stats,
        'monthly_stats': monthly_stats,
        'detailed_data': detailed_data
    })
