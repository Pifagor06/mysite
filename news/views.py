from django.shortcuts import render,get_object_or_404,redirect
from django.views.generic import ListView,DetailView,CreateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator

from .models import News,Category
from .forms import NewsForm,UserRegisterForm, UserLoginForm,ContactForm
from .utils import MyMixin
from django.contrib import messages
from django.contrib.auth import login, logout
from django.core.mail import send_mail

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            try:
                send_mail(
                    subject=form.cleaned_data['subject'],
                    message=form.cleaned_data['content'],
                    from_email='shohratowfarhat@gmail.com',
                    recipient_list=['farhatshohratov@gmail.com'],
                    fail_silently=True
                )
                messages.success(request,'Письмо отправлено!')
                return redirect('contact')
            except Exception as e:
                messages.error(request,f'Ошибка отправки: {str(e)}')
        else:
            messages.error(request,'Ошибка валидации формы')
    else:
        form = ContactForm()
    return render(request,'news/test.html',{"form":form})

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request,user)
            messages.success(request,'Вы успешно зарегистрировались')
            return redirect('home')
        else:
            messages.error(request,'Ошибка регистрации')
    else:
        form = UserRegisterForm()
    return render(request,'news/register.html',{"form": form})


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request,user)
            return redirect('home')
    else:
        form = UserLoginForm()
    return render(request,'news/login.html',{"form": form})


def user_logout(request):
    logout(request)
    return redirect('login')



class HomeNews(MyMixin, ListView):
    model = News
    template_name = 'news/home_news_list.html'
    context_object_name = 'news'
    mixin_prop = 'hello world'
    paginate_by = 2

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.get_upper('Главная страница')
        context['mixin_prop'] = self.get_prop()
        return context

    def get_queryset(self):
        return News.objects.filter(is_published=True).select_related('category')



class NewsByCategory(MyMixin,ListView):
    model = News
    template_name = 'news/home_news_list.html'
    context_object_name = 'news'
    allow_empty = False
    paginate_by = 2

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.get_upper(Category.objects.get(pk=self.kwargs['category_id']))
        return context

    def get_queryset(self):
        return News.objects.filter(category_id=self.kwargs['category_id'],is_published=True).select_related('category')


class ViewNews(DetailView):
    model = News
    context_object_name = 'news_item'
    # template_name = 'news/news_detail.html'
    # pk_url_kwarg = 'news_id'


class CreateNews(LoginRequiredMixin, CreateView):
    form_class = NewsForm
    template_name = 'news/add_news.html'
    # success_url = reverse_lazy('home')
    # login_url = reverse_lazy('home')
    raise_exception = True

def get_category(request,category_id):
    news = News.objects.filter(category_id=category_id)
    category = Category.objects.get(pk=category_id)
    return render(request,'news/category.html', {'news': news,'category': category})


# def index(request):
#     news = News.objects.all()
#     context = {
#         'news':news,
#         'title':'Список новостей',
#     }
#     return render(request,template_name='news/index.html',context=context)
# def view_news(request,news_id):
#     news_item = get_object_or_404(News,pk=news_id)
#     return render(request,'news/view_news.html',{"news_item":news_item})

# def add_news(request):
#     if request.method == 'POST':
#         form = NewsForm(request.POST,request.FILES)
#         if form.is_valid():
#             #print(form.cleaned_data)
#             #news = News.objects.create(**form.cleaned_data)
#             news = form.save()
#             return redirect(news.get_absolute_url())
#     else:
#         form = NewsForm()
#     return render(request,'news/add_news.html',{'form':form})
