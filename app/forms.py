from django.forms.formsets import BaseFormSet
from django.forms import ModelForm, ChoiceField
from django import forms
from models.models import TaskItem, TaskList, CHOICES
import datetime
from tempus_dominus.widgets import DatePicker, TimePicker, DateTimePicker
class TaskListForm(forms.Form):
    task_list_name = forms.CharField(max_length=100, required=True)
    task_list_description = forms.CharField(max_length=100, required=True)


class EditItemForm(forms.Form):
    def __init__(self, user, instance, *args, **kwargs):
        user = user
        instance = instance
        super().__init__(*args, **kwargs)
        self.fields['task_name'] = forms.CharField(max_length=100, required=True, initial=instance.task_name)
        self.fields['task_description'] = forms.CharField(max_length=100, required=True, initial=instance.tast_description)
        self.fields['task_created_date'] = forms.DateTimeField(label='Previous created date: ' + instance.task_created_date.strftime("%D"),
                                                                required = True,
                                                                initial=instance.task_created_date,
                                                                widget=DateTimePicker(
                                                                    options={
                                                                        'useCurrent': True,
                                                                        'collapse': True,
                                                                        'format' : "YYYY-MM-DD HH:mm",
                                                                        # Calendar and time widget formatting
                                                                        'date': 'fas fa-calendar',
                                                                        'clear': 'fas fa-delete',
                                                                    },
                                                                    attrs={
                                                                        'append': 'fas fa-calendar',
                                                                        'icon_toggle': True,
                                                                    }
                                                                ),
                                                            )
        self.fields['task_due_date'] = forms.DateTimeField(label='Previous due date: ' + instance.task_due_date.strftime("%D"),
                                                            required = True,
                                                            initial=instance.task_due_date,
                                                            widget=DateTimePicker(
                                                                options={
                                                                    'useCurrent': True,
                                                                    'collapse': True,
                                                                    'format' : "YYYY-MM-DD HH:mm",
                                                                    'date': 'fas fa-calendar',
                                                                    'clear': 'fas fa-delete',
                                                                },
                                                                attrs={
                                                                    'append': 'fas fa-calendar',
                                                                    'icon_toggle': True,
                                                                }
                                                            ),
                                                        )
        self.fields['task_priority'] = forms.ChoiceField(choices=CHOICES, initial=instance.task_priority)
        self.fields['task_completion'] = forms.BooleanField(required=False, initial=instance.task_completion)
        self.fields['task_list'] = forms.ModelChoiceField(queryset=TaskList.objects.filter(task_user=user), 
                                                            error_messages = {"required": "Please choose a List"},
                                                            initial = instance.task_list)

class TaskItemForm(forms.Form):
    def __init__(self, user, *args, **kwargs):
        user = user
        super().__init__(*args, **kwargs)
        self.fields['task_list'] = forms.ModelChoiceField(queryset=TaskList.objects.filter(task_user=user), error_messages = {"required": "Please choose a List"})

    task_name = forms.CharField(max_length=100, required=True)
    task_description = forms.CharField(max_length=100, required=True)
    task_created_date = forms.DateTimeField(
        required = True,
        initial=datetime.datetime.now(),
        widget=DateTimePicker(
            options={
                'useCurrent': True,
                'collapse': True,
                'format' : "YYYY-MM-DD HH:mm",
                # Calendar and time widget formatting
                'date': 'fas fa-calendar',
                'clear': 'fas fa-delete',
            },
            attrs={
                'append': 'fas fa-calendar',
                'icon_toggle': True,
            }
        ),
    )
    task_due_date = forms.DateTimeField(
        required = True,
        initial=datetime.datetime.now(),
        widget=DateTimePicker(
            options={
                'useCurrent': True,
                'collapse': True,
                'format' : "YYYY-MM-DD HH:mm",
                'date': 'fas fa-calendar',
                'clear': 'fas fa-delete',
            },
            attrs={
                'append': 'fas fa-calendar',
                'icon_toggle': True,
            }
        ),
    )
    task_priority = forms.ChoiceField(choices=CHOICES)
    task_completion = forms.BooleanField(required=False)

class delTaskList(forms.Form):
    task_list = forms.ModelChoiceField(queryset=TaskList.objects.all(), error_messages = {"required": "Please choose a list"})


class delTaskItem(forms.Form):
    task_item = forms.ModelChoiceField(queryset=TaskItem.objects.all(), error_messages = {"required": "Please choose a list"})


class GradeCategoryForm(forms.Form):
    category_weight = forms.DecimalField(max_value=100, min_value=0, decimal_places=2, required=True, widget=forms.NumberInput(attrs={'class' : 'myfieldclass', 'required': True}), error_messages = {"required": "Please enter a weight"})
    current_points_earned = forms.IntegerField(min_value=0, widget=forms.NumberInput(attrs={'class' : 'myfieldclass', 'required': True}), error_messages = {"required": "Please input points earned"})
    current_points_possible = forms.IntegerField(min_value=0, widget=forms.NumberInput(attrs={'class' : 'myfieldclass', 'required': True}), error_messages = {"required": "Please input possible points earned"})
    total_points_possible = forms.IntegerField(min_value=1, widget=forms.NumberInput(attrs={'class' : 'myfieldclass', 'required': True}), error_messages = {"required": "Please input total possible points"})

class BaseGradeCategoryFormSet(BaseFormSet):
    def clean(self):
        if any(self.errors):
            return
        
        weights = []
        urls = []
        
        for form in self.forms:
            if form.cleaned_data:
                current_points_earned = form.cleaned_data['current_points_earned']
                current_points_possible = form.cleaned_data['current_points_possible']
                total_points_possible = form.cleaned_data['total_points_possible']
