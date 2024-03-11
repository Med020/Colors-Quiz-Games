from django.shortcuts import render, redirect
from .models import Quiz, Question, Choice, Result
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy



def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            password1 = form.cleaned_data.get('password1')
            password2 = form.cleaned_data.get('password2')
            if password1 == password2:
                form.save()
                # Redirect to a success page or login page
                return redirect('quiz_index')  # Assuming you have a URL named 'login' for the login page
            else:
                # Passwords don't match
                messages.error(request, "Passwords don't match.")
        else:
            # Form is invalid
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{error}")
    else:
        form = UserCreationForm()
    return render(request, 'quiz/sign-up.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to a success page or dashboard
            return redirect('quiz_index')  # Assuming you have a URL named 'quiz_index' for the index page
        else:
            # Handle invalid login
            messages.error(request, 'Invalid username or password')
            return render(request, 'quiz/login.html')
    # If request method is not POST or login fails, render the login page
    return render(request, 'quiz/login.html')
    
def quiz_index_view(request):
    quizzes = Quiz.objects.all()
    return render(request, 'quiz/quiz_index.html', {'quizzes': quizzes})

def quiz_detail_view(request, quiz_id):
    quiz = Quiz.objects.get(id=quiz_id)
    questions = Question.objects.filter(quiz=quiz)
    if request.method == 'POST':
        # Process quiz submission
        score = 0
        total_questions = 0
        for question in questions:
            total_questions += 1
            selected_choice_id = request.POST.get(f'question_{question.id}', None)
            if selected_choice_id:
                selected_choice = Choice.objects.get(id=selected_choice_id)
                if selected_choice.is_correct:
                    score += 1
        
        # Calculate score percentage
        score_percentage = (score / total_questions) * 100 if total_questions > 0 else 0

        # Save result
        result = Result.objects.create(user=request.user, quiz=quiz, score=score_percentage, feedback="Your quiz submission has been processed.")

        result.save()

        # Redirect to result page
        return redirect('result_view', quiz_id=quiz.id)

    return render(request, 'quiz/quiz_detail.html', {'quiz': quiz, 'questions': questions})

def result_view(request, quiz_id):
    quiz = Quiz.objects.get(id=quiz_id)
    user_results = Result.objects.filter(user=request.user, quiz=quiz)
    return render(request, 'quiz/result.html', {'quiz': quiz, 'user_results': user_results})

class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('login')  # Specify the URL name of your login page

def custom_logout(request):
    # Ensure user is logged in before logging out
    if request.user.is_authenticated:
        return CustomLogoutView.as_view()(request)
    else:
        # Redirect users to the login page if they are not logged in
        return redirect('login')  # Replace 'login' with the URL name of your login page

def result_view(request, quiz_id):
    quiz = Quiz.objects.get(id=quiz_id)
    user_results = Result.objects.filter(user=request.user, quiz=quiz)
    return render(request, 'quiz/result.html', {'quiz': quiz, 'user_results': user_results})
