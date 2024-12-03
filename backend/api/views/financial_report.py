from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Sum, Count
from django.db.models.functions import TruncMonth
from ..models import Payment, Course, Language, TeacherCourse, Teacher
from datetime import datetime

@api_view(['GET'])
def financial_report(request):
    try:
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')

        print(f"Generating report from {start_date} to {end_date}")

        # Получаем все платежи
        payments = Payment.objects.select_related(
            'customer', 'course', 'course__language'
        ).all()

        print(f"Total payments in DB: {payments.count()}")

        # Фильтруем по датам, если они указаны
        if start_date and end_date:
            payments = payments.filter(payment_date__range=[start_date, end_date])
            print(f"Filtered payments: {payments.count()}")

        # Общая сумма оплат
        total_payments = payments.filter(status='paid').aggregate(
            total=Sum('amount')
        )['total'] or 0

        """
        # Статистика по языкам
        language_stats = []
        for language in Language.objects.all():
            language_payments = payments.filter(
                course__language=language,
                status='paid'
            )
            total = language_payments.aggregate(
                total=Sum('amount')
            )['total'] or 0
            
            if total > 0:
                language_stats.append({
                    'language': language.name,
                    'total': float(total),
                    'count': language_payments.count()
                })
        """

        # Статистика по месяцам
        monthly_stats = []
        monthly_data = payments.filter(
            status='paid'
        ).annotate(
            month=TruncMonth('payment_date')
        ).values('month').annotate(
            revenue=Sum('amount'),
            count=Count('id')
        ).order_by('month')

        for data in monthly_data:
            # Расчет зарплат учителей за месяц
            month_payments = payments.filter(
                payment_date__year=data['month'].year,
                payment_date__month=data['month'].month,
                status='paid'
            )
            
            teacher_salaries = 0
            for payment in month_payments:
                try:
                    teacher = TeacherCourse.objects.get(course=payment.course).teacher
                    teacher_salaries += float(teacher.salary)
                except TeacherCourse.DoesNotExist:
                    continue

            monthly_stats.append({
                'month': data['month'].strftime('%Y-%m'),
                'revenue': float(data['revenue']),
                'expenses': float(teacher_salaries),
                'profit': float(data['revenue']) - float(teacher_salaries),
                'count': data['count']
            })

        # Расчет зарплат по преподавателям
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
                course_revenue = sum(float(payment.amount) for payment in course_payments)
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

        # Сортируем по общему доходу от курсов
        teacher_stats.sort(key=lambda x: x['total_revenue'], reverse=True)
        
        print(f"Teacher stats: {teacher_stats}")

        # Детальные данные
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
                'amount': float(payment.amount),
                'status': payment.status
            })

        # Расчет общих зарплат учителей
        total_teacher_salaries = 0
        for payment in payments.filter(status='paid'):
            try:
                teacher = TeacherCourse.objects.get(course=payment.course).teacher
                total_teacher_salaries += float(teacher.salary)
            except TeacherCourse.DoesNotExist:
                continue

        response_data = {
            'total_payments': float(total_payments),
            'total_teacher_salaries': float(total_teacher_salaries),
            'total_profit': float(total_payments) - float(total_teacher_salaries),
            'monthly_stats': monthly_stats,
            'detailed_data': detailed_data,
            'teacher_stats': teacher_stats
        }

        print(f"Response data: {response_data}")
        return Response(response_data)

    except Exception as e:
        print(f"Error generating report: {str(e)}")
        return Response({'error': str(e)}, status=500)
