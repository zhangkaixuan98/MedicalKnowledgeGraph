from django.contrib import admin

from .models import User, Question, Doctor, Reply, Feedback

# Register your models here.

admin.site.register(User)

admin.site.register(Question)

admin.site.register(Doctor)

admin.site.register(Reply)

admin.site.register(Feedback)
