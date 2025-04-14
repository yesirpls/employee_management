from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.contrib import messages
from django.db.models import Q, Avg, Count, Sum
from django.http import JsonResponse
from .models import Employee
from .forms import EmployeeForm

def home(request):
    total_employees = Employee.objects.count()
    active_employees = Employee.objects.filter(is_active=True).count()
    departments = Employee.objects.values('department').annotate(count=Count('id'))
    avg_salary = Employee.objects.aggregate(avg_salary=Avg('salary'))['avg_salary']
    
    context = {
        'total_employees': total_employees,
        'active_employees': active_employees,
        'departments': departments,
        'avg_salary': avg_salary,
    }
    return render(request, 'employees/home.html', context)

def employee_list(request):
    search_query = request.GET.get('search', '')
    department = request.GET.get('department', '')
    
    employees = Employee.objects.all()
    
    if search_query:
        employees = employees.filter(
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(email__icontains=search_query)
        )
    
    if department:
        employees = employees.filter(department=department)
    
    paginator = Paginator(employees, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    departments = Employee.objects.values_list('department', flat=True).distinct()
    
    return render(request, 'employees/employee_list.html', {
        'page_obj': page_obj,
        'departments': departments,
        'search_query': search_query,
        'selected_department': department
    })

def employee_detail(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    return render(request, 'employees/employee_detail.html', {'employee': employee})

def employee_create(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Employee created successfully!')
            return redirect('employee_list')
    else:
        form = EmployeeForm()
    return render(request, 'employees/employee_form.html', {'form': form})

def employee_update(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            messages.success(request, 'Employee updated successfully!')
            return redirect('employee_list')
    else:
        form = EmployeeForm(instance=employee)
    return render(request, 'employees/employee_form.html', {'form': form})

def employee_delete(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        employee.delete()
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'status': 'success'})
        return redirect('employee_list')
    return render(request, 'employees/employee_confirm_delete.html', {'employee': employee})