from django.shortcuts import render, reverse, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponseNotFound
from decimal import *
from django.forms.formsets import formset_factory
import requests
import calendar

from app.forms import TaskItemForm, TaskListForm, GradeCategoryForm, EditItemForm
from models.models import City
from weather.forms import CityForm
from datetime import datetime, timedelta, date
from django.http import HttpResponse
from django.views import generic
from django.utils.safestring import mark_safe
from models.models import TaskItem, TaskList, Profile
from .utils import Calendar

# Create your views here.
def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split('-'))
        return date(year, month, day=1)
    return datetime.today()

def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month

def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month

def make_calendar(request):
    if request.user.is_authenticated:
        prof = Profile.objects.get(user=request.user)
        d = get_date(request.GET.get('month', None))
        cal = Calendar(d.year, d.month)
        cal.setfirstweekday(6)
        html_cal = cal.formatmonth(withyear=True, user=prof)
        context = {'calendar' : mark_safe(html_cal), 'prev_month' : prev_month(d), 'next_month' : next_month(d)}
        return render(request, 'calendar.html', context)
    return HttpResponseRedirect(reverse('home'))

def create_list(request):
    if request.method == "POST":
        form = TaskListForm(request.POST)
        if form.is_valid():
            item = TaskList()
            item.task_list_name = form.cleaned_data['task_list_name']
            item.task_list_description = form.cleaned_data['task_list_description']
            prof = Profile.objects.get(user=request.user)
            item.task_user = prof
            item.save()
            return HttpResponseRedirect(reverse("dashboard:todo"))
    else:
        form = TaskListForm()
    return render(request, "create_list_form.html", {"form": form})


def update_list(request, ):
    if request.method == "POST":
        data = TaskList.objects.get_object_or_404(task_list_name=request.POST.get("task_list_name"))
        form = TaskListForm(request.POST, instance=data)
        if form.is_valid():
            item = TaskList()
            item.task_list_name = form.cleaned_data['task_list_name']
            item.task_list_description = form.cleaned_data['task_list_description']
            item.task_user = request.user
            item.save()
            return HttpResponseRedirect(reverse("dashboard:todo"))
    else:
        form = TaskListForm()
    return render(request, "create_list_form.html", {"form": form})


def delete_list(request, task_list_id):
    prof = Profile.objects.get(user=request.user)
    task_lists = TaskList.objects.filter(task_user=prof)
    task_list = task_lists.get(id=task_list_id)
    task_list.delete()
    return HttpResponseRedirect(reverse("dashboard:view_lists"))


def list_lists(request):
    try:
        prof = Profile.objects.get(user=request.user)
        task_list = list(TaskList.objects.filter(task_user=prof))
    except TaskList.DoesNotExist:
        return HttpResponseRedirect(reverse("dashboard:todo"))
    return render(request, "list-lists.html", {"task_list": task_list})


def create_item(request):
    prof = Profile.objects.get(user=request.user)
    if request.method == "POST":
        form = TaskItemForm(prof, request.POST)
        if form.is_valid():
            item = TaskItem()
            item.task_name = form.cleaned_data['task_name']
            item.tast_description = form.cleaned_data['task_description']
            item.task_created_date = form.cleaned_data['task_created_date']
            item.task_due_date = form.cleaned_data['task_due_date']
            item.task_priority = form.cleaned_data['task_priority']
            item.task_completion = form.cleaned_data['task_completion']
            item.task_list = form.cleaned_data['task_list']
            item.save()
            return HttpResponseRedirect(reverse("dashboard:view_items"))
    else:
        form = TaskItemForm(prof)
    return render(request, "create_item_form.html", {"form": form})


def update_item(request, task_id):
    prof = Profile.objects.get(user=request.user)
    items = TaskItem.objects.filter(task_list__task_user=prof)
    item = items.get(id=task_id)
    if request.method == "POST":
        form = EditItemForm(prof, item, request.POST)
        if form.is_valid():
            item.task_name = form.cleaned_data['task_name']
            item.tast_description = form.cleaned_data['task_description']
            item.task_created_date = form.cleaned_data['task_created_date']
            item.task_due_date = form.cleaned_data['task_due_date']
            item.task_priority = form.cleaned_data['task_priority']
            item.task_completion = form.cleaned_data['task_completion']
            item.task_list = form.cleaned_data['task_list']
            item.save()
            return HttpResponseRedirect(reverse("dashboard:view_items"))
    else:
        form = EditItemForm(prof, item)
    return render(request, "edit_item_form.html", {"form": form, "create_date_initial": item.task_created_date, "due_date_initial": item.task_due_date})

def list_items(request):
    # second parameter for TaskList and return list that is TaskItems.objects.get(TaskList=passed_list)
    try:
        prof = Profile.objects.get(user=request.user)
        items = TaskItem.objects.filter(task_list__task_user=prof)
    except TaskList.DoesNotExist:
        return HttpResponseRedirect(reverse("dashboard:todo"))
    task_lists = []
    for item in items:
        if item.task_list not in task_lists:
            task_lists.append(item.task_list)
    lists = []
    for task_list in task_lists:
        helper = []
        helper.append(task_list)
        why = list(TaskItem.objects.filter(task_list=task_list))
        for item in why:
            if not item.task_completion:
                helper.append(item)
        lists.append(helper)
    return render(request, "list-items.html", {"items": items, "lists": lists, "task_lists": task_lists})


def list_completed_items(request):
    # second parameter for TaskList and return list that is TaskItems.objects.get(TaskList=passed_list)
    try:
        prof = Profile.objects.get(user=request.user)
        items = TaskItem.objects.filter(task_list__task_user=prof)
    except TaskList.DoesNotExist:
        return HttpResponseRedirect(reverse("dashboard:todo"))
    task_lists = []
    for item in items:
        if item.task_list not in task_lists:
            task_lists.append(item.task_list)
    lists = []
    for task_list in task_lists:
        helper = []
        helper.append(task_list)
        why = list(TaskItem.objects.filter(task_list=task_list))
        for item in why:
            if item.task_completion:
                helper.append(item)
        lists.append(helper)
    return render(request, "list-completed-items.html", {"items": items, "lists": lists, "task_lists": task_lists})


def dashboard(request):
    if request.user.is_authenticated:
        url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=f0ec1cf58c705f937e3cd62b5a0e5f14'
        prof = Profile.objects.get(user=request.user)
        cities = City.objects.filter(city_user=prof) #return all the cities in the database

        if request.method == 'POST': # only true if form is submitted
            form = CityForm(request.POST) # add actual request data to form for processing
            if form.is_valid():
                item = City()
                item.name = form.cleaned_data['name']
                prof = Profile.objects.get(user=request.user)
                item.city_user = prof
                item.save()

        form = CityForm()

        weather_data = []
        for city in cities:

            city_weather = requests.get(url.format(city)).json() #request the API data and convert the JSON to Python data types

            if len(city_weather) > 10:
                weather = {
                    'city' : city,
                    'temperature' : city_weather['main']['temp'],
                    'description' : city_weather['weather'][0]['description'],
                    'icon' : city_weather['weather'][0]['icon']
                }

                weather_data.append(weather) #add the data for the current city into our list

        context = {'weather_data' : weather_data, 'form' : form}
        return render(request, 'dashboard.html', context) #returns the index.html template
    return HttpResponseRedirect(reverse('home'))

def todo(request):
    if request.user.is_authenticated:
        return render(request, 'todo.html')
    return HttpResponseRedirect(reverse('home'))


def grade_calc(request):
    GradeCalcFormSet = formset_factory(GradeCategoryForm)
    formset = GradeCalcFormSet()

    if request.method == "POST":
        formset = GradeCalcFormSet(request.POST)
        if formset.is_valid():
            grade = Decimal(0)
            percentage_total_points_given = Decimal(0)
            total_weight = Decimal(0)
            for form in formset:
                if form.is_valid():
                    if (form.cleaned_data['current_points_possible'] > 0):
                        grade += form.cleaned_data['category_weight']*Decimal(form.cleaned_data['current_points_earned']/Decimal(form.cleaned_data['current_points_possible']))
                    percentage_total_points_given += form.cleaned_data['category_weight']*Decimal(form.cleaned_data['current_points_possible']/Decimal(form.cleaned_data['total_points_possible']))
                    total_weight += form.cleaned_data['category_weight']
            grade = round(grade, 2)
            show_grade_table = not (percentage_total_points_given < 100.1 and percentage_total_points_given > 99.9)
            if show_grade_table:
                grade_for_98 = round(max((9800-(grade*percentage_total_points_given))/(100-percentage_total_points_given), 0), 2)
                grade_for_93 = round(max((9300-(grade*percentage_total_points_given))/(100-percentage_total_points_given), 0), 2)
                grade_for_90 = round(max((9000-(grade*percentage_total_points_given))/(100-percentage_total_points_given), 0), 2)
                grade_for_88 = round(max((8800-(grade*percentage_total_points_given))/(100-percentage_total_points_given), 0), 2)
                grade_for_83 = round(max((8300-(grade*percentage_total_points_given))/(100-percentage_total_points_given), 0), 2)
                grade_for_80 = round(max((8000-(grade*percentage_total_points_given))/(100-percentage_total_points_given), 0), 2)
                grade_for_78 = round(max((7800-(grade*percentage_total_points_given))/(100-percentage_total_points_given), 0), 2)
                grade_for_73 = round(max((7300-(grade*percentage_total_points_given))/(100-percentage_total_points_given), 0), 2)
                grade_for_70 = round(max((7000-(grade*percentage_total_points_given))/(100-percentage_total_points_given), 0), 2)
                grade_for_68 = round(max((6800-(grade*percentage_total_points_given))/(100-percentage_total_points_given), 0), 2)
                grade_for_63 = round(max((6300-(grade*percentage_total_points_given))/(100-percentage_total_points_given), 0), 2)
                grade_for_60 = round(max((6000-(grade*percentage_total_points_given))/(100-percentage_total_points_given), 0), 2)
            else:
                grade_for_98 = round(0, 2)
                grade_for_93 = round(0, 2)
                grade_for_90 = round(0, 2)
                grade_for_88 = round(0, 2)
                grade_for_83 = round(0, 2)
                grade_for_80 = round(0, 2)
                grade_for_78 = round(0, 2)
                grade_for_73 = round(0, 2)
                grade_for_70 = round(0, 2)
                grade_for_68 = round(0, 2)
                grade_for_63 = round(0, 2)
                grade_for_60 = round(0, 2)

            if total_weight < 100.1 and total_weight > 99.9:
                context = {
                    'grade': grade,
                    'grade_for_98': grade_for_98,
                    'grade_for_93': grade_for_93,
                    'grade_for_90': grade_for_90,
                    'grade_for_88': grade_for_88,
                    'grade_for_83': grade_for_83,
                    'grade_for_80': grade_for_80,
                    'grade_for_78': grade_for_78,
                    'grade_for_73': grade_for_73,
                    'grade_for_70': grade_for_70,
                    'grade_for_68': grade_for_68,
                    'grade_for_63': grade_for_63,
                    'grade_for_60': grade_for_60,
                    'show_grade_table': show_grade_table,
                }

                return render(request, 'grade_calc_results.html', context)
            else:
                context = {
                    'formset': formset,
                    'total_weight': total_weight,
                }

                return render(request, 'grade_calc.html', context)

    context = {
        'formset': formset,
    }

    return render(request, 'grade_calc.html', context)

def grade_calc_results(request):
    pass

def complete(request, task_id):
    prof = Profile.objects.get(user=request.user)
    items = TaskItem.objects.filter(task_list__task_user=prof)
    item = items.get(id=task_id)
    item.task_completion = not item.task_completion
    item.save()
    return HttpResponseRedirect(reverse("dashboard:view_items"))

def uncomplete(request, task_id):
    prof = Profile.objects.get(user=request.user)
    items = TaskItem.objects.filter(task_list__task_user=prof)
    item = items.get(id=task_id)
    item.task_completion = not item.task_completion
    item.save()
    return HttpResponseRedirect(reverse("dashboard:view_completed_items"))

def delete_item(request, task_id):
    prof = Profile.objects.get(user=request.user)
    items = TaskItem.objects.filter(task_list__task_user=prof)
    item = items.get(id=task_id)
    item.delete()
    return HttpResponseRedirect(reverse("dashboard:view_items"))

def delete_completed_item(request, task_id):
    prof = Profile.objects.get(user=request.user)
    items = TaskItem.objects.filter(task_list__task_user=prof)
    item = items.get(id=task_id)
    item.delete()
    return HttpResponseRedirect(reverse("dashboard:view_completed_items"))

def delete_city(request, city_id):
    prof = Profile.objects.get(user=request.user)
    cities = City.objects.filter(city_user=prof)
    city = cities.get(id=city_id)
    city.delete()
    return HttpResponseRedirect(reverse("dashboard:dashboard"))