from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Sum, Count
from django.db.models.functions import TruncMonth
from ..models import Payment, Course, Language, TeacherCourse, Teacher
from datetime import datetime


def get_filtered_payments(start_date=None, end_date=None):
    """
    Returns a queryset of all payments, with the course and language prefetched.
    If start_date and end_date are given, it filters the queryset by the payment date.
    
    """
    payments = Payment.objects.select_related(
        'customer', 'course', 'course__language'
    ).all()

    if start_date and end_date:
        payments = payments.filter(payment_date__range=[start_date, end_date])
    
    return payments


def calculate_total_payments(payments):
    """
    Returns the total sum of all paid payments.

    """
    return payments.filter(status='paid').aggregate(
        total=Sum('course__price')
    )['total'] or 0


def get_language_statistics(payments):
    """
    Calculates statistics for each language based on the payments.

    Args:
        payments: A queryset of payment objects.

    Returns:
        A list of dictionaries, each containing:
        - 'language': The name of the language.
        - 'total': The total revenue from courses in this language.
        - 'count': The number of paid payments for courses in this language.

    """
    language_stats = []
    for language in Language.objects.all():
        language_payments = payments.filter(
            course__language=language,
            status='paid'
        )
        total = language_payments.aggregate(
            total=Sum('course__price')
        )['total'] or 0
        
        if total > 0:
            language_stats.append({
                'language': language.name,
                'total': float(total),
                'count': language_payments.count()
            })
    return language_stats


def get_monthly_statistics(payments):
    """
    Calculates statistics for each month based on the payments.

    Args:
        payments: A queryset of payment objects.

    Returns:
        A list of dictionaries, each containing:
        - 'month': The month of the year, in the format 'YYYY-MM'.
        - 'revenue': The total revenue for this month.
        - 'expenses': The total expenses for this month.
        - 'profit': The total profit for this month.
        - 'count': The number of paid payments for this month.

    """
    monthly_stats = []
    monthly_data = payments.filter(
        status='paid'
    ).annotate(
        month=TruncMonth('payment_date')
    ).values('month').annotate(
        revenue=Sum('course__price'),
        count=Count('id')
    ).order_by('month')

    for data in monthly_data:
        month_payments = payments.filter(
            payment_date__year=data['month'].year,
            payment_date__month=data['month'].month,
            status='paid'
        )
        
        teacher_salaries = calculate_teacher_salaries(month_payments)

        monthly_stats.append({
            'month': data['month'].strftime('%Y-%m'),
            'revenue': float(data['revenue']),
            'expenses': float(teacher_salaries),
            'profit': float(data['revenue']) - float(teacher_salaries),
            'count': data['count']
        })
    
    return monthly_stats


def calculate_teacher_salaries(payments):
    """
    Calculate the total salaries of the teachers for the given payments.

    Args:
        payments: A Django QuerySet of Payment objects.

    Returns:
        The total salaries of the teachers for the given payments.

    """
    total_salaries = 0
    for payment in payments:
        try:
            teacher = TeacherCourse.objects.get(course=payment.course).teacher
            total_salaries += float(teacher.salary)
        except TeacherCourse.DoesNotExist:
            continue
    return total_salaries


def get_teacher_statistics(payments, start_date, end_date):
    """
    Calculate statistics for each teacher in the given payments.

    Args:
        payments: A Django QuerySet of Payment objects.
        start_date: The start date of the period.
        end_date: The end date of the period.

    Returns:
        A list of dictionaries, each containing:
            - name: The full name of the teacher.
            - total_salary: The total salary for the given period.
            - total_revenue: The total revenue for the given period.
            - total_students: The total number of students for the given period.
            - courses_count: The number of courses the teacher is assigned to.
            - efficiency: The efficiency of the teacher, calculated as the percentage of total salary to total revenue.

    """
    teacher_stats = []
    for teacher in Teacher.objects.all():
        teacher_courses = TeacherCourse.objects.filter(teacher=teacher)
        total_salary = 0
        total_revenue = 0
        total_students = 0
        
        for tc in teacher_courses:
            course_payments = payments.filter(
                course=tc.course,
                status='paid',
                payment_date__range=[start_date, end_date]
            )
            course_revenue = sum(float(payment.course.price) for payment in course_payments)
            total_revenue += course_revenue
            total_salary += float(teacher.salary) * course_payments.count()
            total_students += course_payments.count()
        
        if total_students > 0:
            teacher_stats.append({
                'name': f"{teacher.last_name} {teacher.first_name}",
                'total_salary': total_salary,
                'total_revenue': total_revenue,
                'total_students': total_students,
                'courses_count': teacher_courses.count(),
                'efficiency': round((total_salary / total_revenue * 100) if total_revenue > 0 else 0, 2)
            })

    return sorted(teacher_stats, key=lambda x: x['total_revenue'], reverse=True)


def get_detailed_data(payments):
    """
    Generate a list of dictionaries containing detailed information for each payment in the given queryset.

    Each dictionary contains the following information:
        - date: The payment date in the format '%Y-%m-%d'.
        - course: The course name.
        - language: The course language name.
        - teacher: The teacher's full name if they are assigned to the course, otherwise 'Не назначен'.
        - amount: The course price.
        - status: The payment status.

    Args:
        payments: A Django QuerySet of Payment objects.

    Returns:
        List of dictionaries containing detailed information for each payment.

    """
    detailed_data = []
    for payment in payments:
        try:
            teacher = TeacherCourse.objects.get(course=payment.course).teacher
            teacher_name = f"{teacher.last_name} {teacher.first_name}"
        except TeacherCourse.DoesNotExist:
            teacher_name = 'Не назначен'

        detailed_data.append({
            'date': payment.payment_date.strftime('%Y-%m-%d'),
            'course': payment.course.name,
            'language': payment.course.language.name,
            'teacher': teacher_name,
            'amount': float(payment.course.price),
            'status': payment.status
        })
    return detailed_data


@api_view(['GET'])
def financial_report(request):
    """
    Generates a financial report based on the filtered payments within a specified date range.

    Args:
        request: The HTTP request object containing query parameters for 'start_date' and 'end_date'.

    Returns:
        Response: A Django REST Framework Response object containing the financial report data, 
        including total payments, teacher salaries, profit, monthly statistics, detailed data, 
        teacher statistics, and language statistics.

    Raises:
        Exception: If any error occurs during the report generation, an error message is included in the response.

    """
    try:
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')

        payments = get_filtered_payments(start_date, end_date)
        total_payments = calculate_total_payments(payments)
        language_stats = get_language_statistics(payments)
        monthly_stats = get_monthly_statistics(payments)
        teacher_stats = get_teacher_statistics(payments, start_date, end_date)
        detailed_data = get_detailed_data(payments)
        total_teacher_salaries = calculate_teacher_salaries(payments.filter(status='paid'))

        response_data = {
            'total_payments': float(total_payments),
            'total_teacher_salaries': float(total_teacher_salaries),
            'total_profit': float(total_payments) - float(total_teacher_salaries),
            'monthly_stats': monthly_stats,
            'detailed_data': detailed_data,
            'teacher_stats': teacher_stats,
            'language_stats': language_stats
        }

        return Response(response_data)

    except Exception as e:
        print(f"Error generating report: {str(e)}")
        return Response({'error': str(e)}, status=500)
