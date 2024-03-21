from django.contrib import admin

from .models import Item, ToDoList

admin.site.register(ToDoList)
admin.site.register(Item)
