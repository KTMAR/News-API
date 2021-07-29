from django.contrib.auth import logout, login
from django.contrib.auth.views import LoginView
from django.db.models import Case, When, Avg
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseNotFound
from django.urls import reverse_lazy
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.mixins import UpdateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from .models import *
from .forms import *
from django.views.generic import ListView, DetailView, CreateView, FormView

from .permissions import IsOwnerOrStaffOrReadOnly
from .serializer import NewsSerializer, UserNewsRelationSerializer
from .utils import *
from django.contrib.auth.mixins import LoginRequiredMixin


class HomeNews(DataMixin, ListView):
    model = News
    context_object_name = 'posts'
    template_name = 'news/index.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(HomeNews, self).get_context_data(**kwargs)
        c_def = self.get_user_context(title='Главная страница')
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return News.objects.filter(is_published=True).select_related('cat')


class NewsByCategories(DataMixin, ListView):
    model = News
    template_name = 'news/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return News.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True).select_related('cat')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c = Category.objects.get(slug=self.kwargs['cat_slug'])
        c_def = self.get_user_context(title='Категория - ' + str(c.title),
                                      cat_selected=c.pk)
        return dict(list(context.items()) + list(c_def.items()))


class ViewNews(DataMixin, DetailView):
    model = News
    # pk_url_kwarg = 'news_id'
    context_object_name = 'post'
    template_name = 'news/post.html'
    slug_url_kwarg = 'post_slug'

    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['post'])
        return dict(list(context.items()) + list(c_def.items()))


class AddPage(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddForms
    template_name = 'news/addpage.html'
    # success_url = reverse_lazy('home')
    login_url = '/admin/'

    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Добавление новости')
        return dict(list(context.items()) + list(c_def.items()))

        # if form.is_valid():
        #     news_item = form.save(commit=False)
        #     news_item.user = request.user  # User posting the form
        #     news_item.save()


class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUser
    template_name = 'news/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Регистрация')
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        user = form.save()
        login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')
        return redirect('home')


class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'news/login.html'

    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Авторизация')
        return dict(list(context.items()) + list(c_def.items()))


class ContactFormView(DataMixin, FormView):
    form_class = ContactForm
    template_name = 'news/contact.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Обратная связь')
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        print(form.cleaned_data)
        return redirect('home')


# class Search(DataMixin,ListView):
#     model = News
#     paginate_by = 1
#     template_name = 'news/search.html'
#
#     def get_queryset(self):
#         return News.objects.filter(title__icontains=self.request.GET.get('search'))
#
#
#     def get_context_data(self, object_list=None, **kwargs):
#         context = super().get_context_data(**kwargs)
#
#         context['search'] = self.request.GET.get('search')
#         return context


# def base_view(request):
#     comments = News.objects.get(pk=1).comments.all()
#     result = create_comments_tree(comments)
#     return render(request, 'news/comments.html', {'comments': result})


def logout_user(request):
    logout(request)
    return redirect('login')


def about(request):
    return render(request, 'news/about.html', {'title': 'О сайте'})


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')


#
def contact(request):
    return HttpResponse("Обратная связь")


#
#
# def login(request):
#     return HttpResponse("Авторизация")

# def show_post(request, post_slug):
#     post = get_object_or_404(News, slug=post_slug)
#
#     context = {
#         'post': post,
#         'title': post.title,
#         'cat_selected': post.cat_id,
#     }
#
#     return render(request, 'news/post.html', context=context)

#
# def show_category(request, cat_slug):
#     cats = Category.objects.all()
#     cat = get_object_or_404(Category, slug=cat_slug)
#     posts = News.objects.filter(cat_id=cat.id)
#
#     if len(posts) == 0:
#         raise Http404()
#     context = {
#         'posts': posts,
#         'cats': cats,
#         'title': cat.title,
#         'cat_selected': cat.id,
#     }
#     return render(request, 'news/index.html', context=context)


# def addpage(request):
#     if request.method == 'POST':
#         form = AddForms(request.POST, request.FILES)
#         if form.is_valid():
#             #print(form.cleaned_data)
#
#             form.save()
#             return redirect('home')
#
#     else:
#         form = AddForms()
#     return render(request, 'news/addpage.html', {'form': form, 'menu': menu, 'title': 'Добавление статьи'})


# def index(request):
#     posts = News.objects.all()
#
#     context = {
#         'posts': posts,
#         'title': 'Главная страница',
#         'cat_selected': 0,
#     }
#
#     return render(request, 'news/index.html', context=context)


class NewsViewSet(ModelViewSet):
    queryset = News.objects.all().annotate(
        annotate_likes=Count(Case(When(usernewsrelation__like=True, then=1)))
    ).select_related('owner_name').prefetch_related('readers').order_by('id')
    serializer_class = NewsSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    permission_classes = [IsOwnerOrStaffOrReadOnly]
    filter_fields = ['title', 'cat__title']
    search_fields = ['title', 'content', 'cat__title']
    ordering_fields = ['title', 'cat__title']

    def perform_create(self, serializer):
        serializer.validated_data['owner_name'] = self.request.user
        serializer.save()


class UserNewsRelationView(UpdateModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]
    queryset = UserNewsRelation.objects.all()
    serializer_class = UserNewsRelationSerializer
    lookup_field = 'news'

    """"Возвращает или создает объект отношения юзера с новостью(лайк,рейтинг и тд.)"""

    def get_object(self):
        obj, _ = UserNewsRelation.objects.get_or_create(user=self.request.user, news_id=self.kwargs['news'])

        return obj
