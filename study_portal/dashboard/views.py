from django.http import response
from django.shortcuts import redirect, render
from . forms import * # Import the forms to the view page
from django.contrib import messages
from django.views import generic # To aid in the details view
from youtubesearchpython import VideosSearch
import requests
import wikipedia
from django.contrib.auth.decorators import login_required

# Create your views here.
# HOME PAGE
def home(request):
    return render(request, 'dashboard/home.html')

# NOTES CREATION FUNCTION

@login_required
def notes(request):
    
    # To Save a note
    if request.method == "POST":
        form = NotesForm(request.POST)
        if form.is_valid:
            notes = Notes(
                user=request.user, 
                title=request.POST['title'], 
                description=request.POST['description'])
            notes.save()
        
        # Display success message
        messages.success(request, f"Notes added from {request.user.username} successfully!")
    
    else:
        
    # Create a new instance of class NotesForm
        form = NotesForm()
    
    # FILTER ALL THE NOTES BELONGING TO THE LOGGED IN USER
    notes = Notes.objects.filter(user=request.user)
    context = {'notes':notes, 'form':form}
    
    # NB: If the context is not passed in as a 3rd variable, the notes will not display
    return render(request, 'dashboard/notes.html', context)


# NOTES DELETION FUNCTION
@login_required
def delete_note(request, pk=None):
    Notes.objects.get(id=pk).delete()
    return redirect("notes")


# NOTES DETAILS VIEW

class NotesDetailsView(generic.DetailView):
    model = Notes


# FOR THE HOMEWORK APP
@login_required
def homework(request):
    # Check for and post a new homework from form
    if request.method == "POST":
        form = HomeworkForm(request.POST)
        if form.is_valid():
            try:
                finished = request.POST['is_finished']
                if finished == 'on':
                    finished = True
                else:
                    finished = False
                
            except:
                finished = False
                
            homeworks = Homework(
                user = request.user,
                subject = request.POST['subject'],
                title = request.POST['title'],
                description = request.POST['description'],
                due = request.POST['due'],
                is_finished = finished
            )
            
            homeworks.save()
            # Display success message
            messages.success(
            request, f"Homeworks added from {request.user.username} successfully!")
            
    else:
        form = HomeworkForm
    
    # Display the homeworks on the screen
    homework = Homework.objects.filter(user=request.user)
    
    if len(homework) == 0:
        homework_done = True
    else:
        homework_done = False
    
    context = {'homeworks': homework, 
               'homeworks_done': homework_done,
               'form':form}
    
    return render(request, 'dashboard/homework.html', context)


@login_required
def update_homework(request, pk=None):
    homework = Homework.objects.get(id=pk)
    
    # If all homeworks are done
    if homework.is_finished == True:
        homework.is_finished = False
        
    # Otherwise...
    else:
        homework.is_finished = True
    homework.save()
        
    return redirect('homework')


@login_required
def delete_homework(request, pk=None):
    Homework.objects.get(id=pk).delete()
    return redirect('homework')
    

# For the youtube section (app)
def youtube(request):
    if request.method == "POST":
        form = DashboardForm(request.POST)
        text = request.POST['text']
        video = VideosSearch(text, limit=10)
        result_list = [] # To store the search result
        for i in video.result()['result']:
            result_dict = {
                'input': text,
                'title': i['title'],
                'duration': i['duration'],
                'thumbnail': i['thumbnails'][0]['url'],
                'channel': i['channel']['name'],
                'link': i['link'],
                'views': i['viewCount']['short'],
                'published': i['publishedTime']
            }
            
            # Check for video descriptions
            desc = ''
            if i['descriptionSnippet']:
                for j in i['descriptionSnippet']:
                    desc += j['text']
            
            # Then put the description variable into thr result dictionary
            result_dict['description'] = desc
            
            # Finally, append the result dictionary to the result list
            result_list.append(result_dict)
            context = {'form': form, 'results': result_list}
        return render(request, 'dashboard/youtube.html', context)
    else:
        form = DashboardForm
        
    context = {'form':form}
    return render(request, 'dashboard/youtube.html', context)


@login_required
def todo(request):
    if request.method == "POST":
        form = TodoForm(request.POST)
        if form.is_valid():
            try:
                finished = request.POST['is_finished']
                if finished == 'on':
                    finished = True
                else:
                    finished = False

            except:
                finished = False

            todos = Todo(
                user=request.user,
                title=request.POST['title'],
                is_finished=finished
            )

            todos.save()
            # Display success message
            messages.success(
                request, f"Todo added from {request.user.username} successfully!")

    else:
        form = TodoForm
    todo = Todo.objects.filter(user = request.user)#Get the Todos of the logged in user
    
    if len(todo) == 0:
        todos_done = True
    else:
        todos_done = False
    
    context = {
        'todos':todo,
        'form': form,
        'todos_done': todos_done
    }
    return render(request, "dashboard/todo.html", context)


@login_required
def update_todo(request, pk=None):
    todo = Todo.objects.get(id=pk)

    # If all homeworks are done
    if todo.is_finished == True:
        todo.is_finished = False

    # Otherwise...
    else:
        todo.is_finished = True
    todo.save()
    messages.success(
    request, f"Todo updated by {request.user.username} !")
    return redirect('todo')


@login_required
def delete_todo(request, pk=None):
    Todo.objects.get(id=pk).delete()
    messages.success(
        request, f"Todo deleted by {request.user.username} !")
    return redirect('todo')
   
   
def books(request):
    if request.method == "POST":
        form = DashboardForm(request.POST)
        text = request.POST['text']
        url = "https://www.googleapis.com/books/v1/volumes?q="+text
        r = requests.get(url)
        answer = r.json()       
        result_list = []  # To store the search result
        for i in range(10):
           
            result_dict = {
                'title': answer['items'][i]['volumeInfo']['title'],
                'subtitle': answer['items'][i]['volumeInfo'].get('subtitle'),
                'description': answer['items'][i]['volumeInfo'].get('description'),
                'count': answer['items'][i]['volumeInfo'].get('pageCount'),
                'categories': answer['items'][i]['volumeInfo'].get('categories'),
                'rating': answer['items'][i]['volumeInfo'].get('pageRating'),
                'thumbnail': answer['items'][i]['volumeInfo'].get('imageLinks').get('thumbnail'),
                'preview': answer['items'][i]['volumeInfo'].get('previewLink')
                
            }

            result_list.append(result_dict)
            context = {'form': form, 'results': result_list}
        return render(request, 'dashboard/books.html', context)
    else:
        form = DashboardForm

    context = {'form': form}
    return render(request, 'dashboard/books.html', context)

def dictionary(request):
    if request.method == "POST":
        form = DashboardForm(request.POST)
        text = request.POST['text']
        url = "https://api.dictionaryapi.dev/api/v2/entries/en/"+text
        r = requests.get(url)
        answer = r.json()
        try:
            phonetics = answer[0]['phonetics'][0]['text']
            audio = answer[0]['phonetics'][0]['audio']
            definition = answer[0]['meanings'][0]['definitions'][0]['definition']
            example = answer[0]['meanings'][0]['definitions'][0]['example']
            origin = answer[0]['origin']
            synonyms = answer[0]['meanings'][0]['definitions'][0]['synonyms']

            context = {
                'form':form,
                'input': text,
                'phonetics': phonetics,
                'audio': audio,
                'definition': definition,
                'example': example,
                'origin': origin,
                'synonyms': synonyms,
            }
        except:
            context = {
                'form': form,
                'input': ''
                  }
        return render(request, 'dashboard/dictionary.html', context)
    else:
        form = DashboardForm
        context = {'form': form}
    return render(request, 'dashboard/dictionary.html', context)


def wiki(request):
    if request.method == "POST":
        form = DashboardForm(request.POST)
        text = request.POST['text']
        search = wikipedia.page(text)
        context = {
            'form': form,
            'title': search.title,
            'link': search.url,
            'details': search.summary, 
            }
        
        return render(request, 'dashboard/wiki.html', context)
    else:
        form = DashboardForm
        context = {'form': form}
    return render(request, 'dashboard/wiki.html', context)


def conversion(request):
    if request.method == "POST":
        form = ConversionForm(request.POST)
        if request.POST['measurement'] == 'length':
            measurement_form = ConversionLengthForm()
            context = {
                'form': form,
                'm_form': measurement_form,
                'input': True,
            }
            
            if 'input' in request.POST:
                first = request.POST['measureX']
                second = request.POST['measureY']
                input = request.POST['input']
                answer = ''
                if input and int(input) >= 0:
                    if first == 'yard' and second == 'foot':
                        answer = f'{input} yard = {int(input) * 3} foot'
                    if first == 'foot' and second == 'yard':
                        answer = f'{input} foot = {int(input) / 3} yard'
                    context = {
                        'form': form,
                        'm_form': measurement_form,
                        'input': True,
                        'answer': answer
                    }
        
        if request.POST['measurement'] == 'mass':
            measurement_form = ConversionMassForm()
            context = {
            'form': form,
            'm_form': measurement_form,
            'input': True,
            }
            
        if 'input' in request.POST:
            first = request.POST['measureX']
            second = request.POST['measureY']
            input = request.POST['input']
            answer = ''
            if input and int(input) >= 0:
                if first == 'pound' and second == 'kilogram':
                    answer = f'{input} pound = {int(input)*0.453592} kilogram'
                if first == 'kilogram' and second == 'pound':
                    answer = f'{input} kilogram = {int(input) * 2.20462} pound'
                context = {
                    'form': form,
                    'm_form': measurement_form,
                    'input': True,
                    'answer': answer
                }
            
    else:
        form = ConversionForm()
        context = {
            'form': form,
            'input': False
                }
    return render(request, 'dashboard/conversion.html', context)


def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
           
            #raw_password = form.cleaned_data.get('password1')
            #user = authenticate(username=username, password=raw_password)
            #login(request, user)
            messages.success(
                request, f'Account created for {username} successully')
            return redirect('login')
           
           
           
            
    else:
        form = UserRegistrationForm()
    context = {
            'form': form
            }

    return render(request, 'dashboard/register.html', context)


def profile(request):
    #if request.method == "POST":
    homeworks = Homework.objects.filter(is_finished = False, user = request.user)    
    todos = Todo.objects.filter(is_finished = False, user = request.user)
    if len(homeworks) == 0:
        homeworks_done = True
    else:
        homeworks_done = False
        
    if len(todos) == 0:
        todos_done = True
    else:
        todos_done = False

    context = {
        'homeworks': homeworks,
        'homeworks_done': homeworks_done,
        'todos': todos,
        'todos_done': todos_done,
    }
    return render(request, 'dashboard/profile.html', context)
