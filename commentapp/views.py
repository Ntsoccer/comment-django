from django.shortcuts import render, resolve_url
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import TemplateView,CreateView,DetailView,UpdateView,DeleteView,ListView 
from .models import Post
from django.urls import reverse_lazy
from .forms import PostForm, LoginForm, SignUpForm, SearchForm
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.core.paginator import Paginator


class OnlyMyPostMixin(UserPassesTestMixin):
    raise_exception=True
    def test_func(self):
        post=Post.objects.get(id=self.kwargs['pk'])
        return post.author==self.request.user


class PostList(ListView):
    model=Post
    paginate_by= 7

    def get_queryset(self):
        if Post.updated_at:
            return Post.objects.all().order_by('-updated_at')
        else:
            return Post.objects.all().order_by('-created_at')


class PostCreate(LoginRequiredMixin,CreateView):
    model=Post
    form_class=PostForm
    success_url=reverse_lazy('commentapp:post_list')

    def form_valid(self,form):
        form.instance.author_id=self.request.user.id
        return super(PostCreate, self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request,'コメントを追加しました。')
        return resolve_url('commentapp:post_list')


class PostDetail(DetailView):
    model=Post

    
class PostUpdate(OnlyMyPostMixin,UpdateView):
    model=Post
    form_class=PostForm

    def get_success_url(self):
        messages.info(self.request,'コメントを編集しました。')
        return resolve_url('commentapp:post_detail',pk=self.kwargs['pk'])


class PostDelete(OnlyMyPostMixin,DeleteView):
    model=Post

    def get_success_url(self):
        messages.info(self.request,'コメントを削除しました。')
        return resolve_url('commentapp:post_list')


class Login(LoginView):
    form_class=LoginForm
    template_name='commentapp/login.html'


class Logout(LogoutView):
    template_name='commentapp/logout.html'


class SignUp(CreateView):
    form_class=SignUpForm
    template_name='commentapp/signup.html'
    success_url=reverse_lazy('commentapp:post_list')

    def form_valid(self,form):
        user=form.save()
        login(self.request, user)
        self.object=user
        messages.info(self.request,'ユーザー登録をしました。')
        return HttpResponseRedirect(self.get_success_url())


def Search(request):
    if request.method=='POST':
        searchform=SearchForm(request.POST)

        if searchform.is_valid():
            freeword=searchform.cleaned_data['freeword']
            search_list=Post.objects.filter(Q(title__icontains=freeword)|Q(content__icontains=freeword))

        params={
            'search_list':search_list,
        }

        return render(request, 'commentapp/search.html',params)
