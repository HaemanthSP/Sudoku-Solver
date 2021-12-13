from django.urls import path

from . import views

urlpatterns = [
    path('solve/', views.Solve.as_view(), name='solve sudoku')
]