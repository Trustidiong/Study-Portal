from django.urls import path
from . import views


urlpatterns = [
    # Home page
    path('',views.home, name="home"),
    
    # FOR THE NOTE APP
    path('notes', views.notes, name="notes"),
    path('notes/<int:pk>', views.delete_note, name="delete-note"),
    path('notes_detail/<int:pk>', views.NotesDetailsView.as_view(), name="notes-detail"),
    
    # FOR THE HOMEWORK APP
    path('homework', views.homework, name="homework"),
    path('update_homework/<int:pk>', views.update_homework, name="update-homework"),
    path('delete_homework/<int:pk>', views.delete_homework, name="delete-homework"),
    
    # FOR THE YOUTUBE APP
    path('youtube', views.youtube, name="youtube"),
    
    # FOR THE todo APP
    path('todo', views.todo, name="todo"),
    path('update_todo/<int:pk>', views.update_todo, name="update-todo"),
    path('delete_todo/<int:pk>', views.delete_todo, name="delete-todo"),
    
    # FOR THE BOOKS APP
    path('books', views.books, name="books"),
    
    # FOR THE DICTIONARY APP
    path('dictionary', views.dictionary, name="dictionary"),
    
    # FOR THE WIKI APP
    path('wiki', views.wiki, name="wiki"),
    
    # FOR THE CONVERSION APP
    path('conversion', views.conversion, name="conversion"),
   
    # FOR THE REG APP
    #path('register', views.register, name="register"),

]
