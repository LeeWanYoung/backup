from django.shortcuts import render, redirect
from .forms import PostForm
from .models import Post
from django.core.paginator import Paginator
from django.contrib.auth.views import LoginView
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from celery import shared_task
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

class GongsaLoginView(LoginView):
    template_name = 'gongsa/gongsalogin.html'

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(self.request, username=username, password=password)


        if user is not None:
            if user.groups.filter(name='gongsa').exists():
                # gongsa 그룹에 있는 사용자인 경우 로그인 처리
                login(self.request, user)
                return redirect('gongsa:main')  # 로그인 후 리디렉션할 페이지
            elif user.groups.filter(name='aici').exists():
                # aici 그룹에 있는 사용자인 경우 로그인 거부
                error_message = 'Please enter a correct username and password. Note that both fields may be case-sensitive.'
                return render(self.request, 'gongsa/gongsalogin.html', {'error_message': error_message})
        else:
            # 인증 실패
            error_message = 'Invalid credentials.'
            return render(self.request, 'gongsa/gongsalogin.html', {'error_message': error_message})

def logout_view(request):
    logout(request)
    return redirect('gongsa:login')

@login_required
def upload(request):
    if request.method == 'POST':
        form = PostForm(request.POST, user=request.user)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('gongsa:worklist')  
    else:
        profile = request.user.profile
        initial_data = {'author': request.user, 'department': profile.department, 'agency': profile.agency, 'phone': profile.phone}
        form = PostForm(user=request.user, initial=initial_data)
    return render(request, 'gongsa/upload.html', {'form': form})

# def upload(request):
#     if request.method == 'POST':
#         form = PostForm(request.POST)
#         if form.is_valid():
#             post = form.save(commit=False)  # Create a Post object but don't save it yet
#             # Additional logic or modifications to the post object if needed
#             post.save()  # Save the post object into the database
#             return redirect('gongsa:worklist')  # Redirect to a success page
#     else:
#         form = PostForm()
#     return render(request, 'gongsa/upload.html', {'form': form})




@login_required
def main(request):
    return render(request, 'gongsa/gongsamain.html')

@login_required
def worklist(request):
    post_list = Post.objects.filter(author=request.user).order_by('-created_at', '-id')
    paginator = Paginator(post_list, 6)

    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)

    return render(request, 'gongsa/worklist.html', {'posts': posts})

# @shared_task
# def delete_completed_constructions():
#     one_month_ago = timezone.now() - timedelta(days=30)

#     completed_constructions = Post.objects.filter(get_construction_status='공사완료', updated_at__lte=one_month_ago)
#     completed_constructions.delete()


@login_required
def update(request, post_id):
    post = Post.objects.get(id=post_id)

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('gongsa:worklist')
    else:
        author_name = post.author.username 
        profile = post.author.profile  
        initial_data = {
            'construction_type': post.construction_type,
            'start_at': post.start_at,
            'end_at': post.end_at,
            'content': post.content,
            'author': author_name,  
            'department': profile.department,  
            'agency': profile.agency, 
            'phone': profile.phone,  
        }
        form = PostForm(user=request.user, initial=initial_data)

    return render(request, 'gongsa/update.html', {'form': form})

# def update(request, post_id):
#     # post = Post.objects.get(id=post_id)  # Assuming you pass the post_id as a parameter to the view
#     # form = PostForm(instance=post)
#     # return render(request, 'update.html', {'form': form})
#     post = Post.objects.get(id=post_id)

#     if request.method == 'POST':
#         form = PostForm(request.POST, instance=post)
#         if form.is_valid():
#             form.save()
#             return redirect('gongsa:worklist')
#     else:
#         form = PostForm(instance=post)
#     return render(request, 'gongsa/update.html', {'form': form})


