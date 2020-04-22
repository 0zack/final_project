from cfis.models import News, NewsComment, Post, PostComment, Fave, Tag

from django.views import View
from cfis.forms import CreateForm, PostCreateForm
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.conf import settings
from django.views.generic.edit import CreateView

from cfis.forms import CommentForm
from cfis.owner import OwnerListView, OwnerDetailView, OwnerCreateView, OwnerUpdateView, OwnerDeleteView

class HomeView(View):
    model = News
    def get(self, request) :
        print(request.get_host())
        host = request.get_host()
        islocal = host.find('localhost') >= 0 or host.find('127.0.0.1') >= 0

        news = News.objects.latest('created_at')
        post = Post.objects.latest('created_at')
        context = {
            'installed' : settings.INSTALLED_APPS,
            'islocal' : islocal,
            'news' : news,
            'post' : post,
        }
        return render(request, 'cfis/main.html', context)

class NewsListView(OwnerListView):
    model = News

    def get_queryset(self):
        return News.objects.order_by('-created_at')

    # By convention:
    # template_name = "cfis/news_list.html"

class NewsDetailView(OwnerDetailView):
    model = News
    template_name = "cfis/news_detail.html"
    def get(self, request, pk) :
        news = News.objects.get(id=pk)
        comments = NewsComment.objects.filter(news=news).order_by('-updated_at')
        comment_form = CommentForm()
        context = { 'news' : news, 'comments': comments, 'comment_form': comment_form }
        return render(request, self.template_name, context)


class NewsCreateView(LoginRequiredMixin, View):
    template = 'cfis/news_form.html'
    success_url = reverse_lazy('cfis:all')
    def get(self, request, pk=None) :
        form = CreateForm()
        ctx = { 'form': form }
        return render(request, self.template, ctx)

    def post(self, request, pk=None) :
        form = CreateForm(request.POST, request.FILES or None)

        if not form.is_valid() :
            ctx = {'form' : form}
            return render(request, self.template, ctx)

        # Add owner to the model before saving
        pic = form.save(commit=False)
        pic.owner = self.request.user
        pic.save()
        return redirect(self.success_url)


class NewsUpdateView(LoginRequiredMixin, View):
    template = 'cfis/news_form.html'
    success_url = reverse_lazy('cfis:all')
    def get(self, request, pk) :
        pic = get_object_or_404(News, id=pk, owner=self.request.user)
        form = CreateForm(instance=pic)
        ctx = { 'form': form }
        return render(request, self.template, ctx)

    def post(self, request, pk=None) :
        pic = get_object_or_404(News, id=pk, owner=self.request.user)
        form = CreateForm(request.POST, request.FILES or None, instance=pic)

        if not form.is_valid() :
            ctx = {'form' : form}
            return render(request, self.template, ctx)

        pic = form.save(commit=False)
        pic.save()

        return redirect(self.success_url)

class NewsDeleteView(OwnerDeleteView):
    model = News

def stream_file(request, pk) :
    news = get_object_or_404(News, id=pk)
    response = HttpResponse()
    response['Content-Type'] = news.content_type
    response['Content-Length'] = len(news.picture)
    response.write(news.picture)
    return response

class NewsCommentCreateView(LoginRequiredMixin, View):
    def post(self, request, pk) :
        news = get_object_or_404(News, id=pk)
        comment = NewsComment(text=request.POST['comment'], owner=request.user, news=news)
        comment.save()
        return redirect(reverse('cfis:news_detail', args=[pk]))

class NewsCommentDeleteView(OwnerDeleteView):
    model = NewsComment
    template_name = "cfis/news_comment_delete.html"

    # https://stackoverflow.com/questions/26290415/deleteview-with-a-dynamic-success-url-dependent-on-id
    def get_success_url(self):
        news = self.object.news
        return reverse('cfis:news_detail', args=[news.id])


class PostListView(OwnerListView):
    model = Post

    # def get_queryset(self):
    #     return Post.objects.order_by('-created_at')

    # By convention:
    template_name = "cfis/post_list.html"

    def get(self, request) :
        post_list = Post.objects.order_by('-created_at')
        favorites = list()
        if request.user.is_authenticated:
            # rows = [{'id': 2}, {'id': 4} ... ]  (A list of rows)
            rows = request.user.favorite_post.values('id')
            # favorites = [2, 4, ...] using list comprehension
            favorites = [ row['id'] for row in rows ]
        ctx = {'post_list' : post_list, 'favorites': favorites}
        return render(request, self.template_name, ctx)

class PostDetailView(OwnerDetailView):
    model = Post
    template_name = "cfis/post_detail.html"
    def get(self, request, pk) :
        post = Post.objects.get(id=pk)
        comments = PostComment.objects.filter(post=post).order_by('-updated_at')
        comment_form = CommentForm()
        context = { 'post' : post, 'comments': comments, 'comment_form': comment_form }
        return render(request, self.template_name, context)


class PostCreateView(LoginRequiredMixin, View):
    template = 'cfis/post_form.html'
    success_url = reverse_lazy('cfis:all')
    def get(self, request, pk=None) :
        form = PostCreateForm()
        ctx = { 'form': form }
        return render(request, self.template, ctx)

    def post(self, request, pk=None) :
        form = PostCreateForm(request.POST, request.FILES or None)

        if not form.is_valid() :
            ctx = {'form' : form}
            return render(request, self.template, ctx)

        # Add owner to the model before saving
        pic = form.save(commit=False)
        pic.owner = self.request.user
        pic.save()
        # for n in len(pic.tags):
        #     post_tag = Tag.objects.create(name=pic.tags[n])
        # tag1 = Tag(name='OPT')
        # pic.tags.add(tag1)
        return redirect(self.success_url)

class PostUpdateView(LoginRequiredMixin, View):
    template = 'cfis/post_form.html'
    success_url = reverse_lazy('cfis:all')
    def get(self, request, pk) :
        pic = get_object_or_404(Post, id=pk, owner=self.request.user)
        form = PostCreateForm(instance=pic)
        ctx = { 'form': form }
        return render(request, self.template, ctx)

    def post(self, request, pk=None) :
        pic = get_object_or_404(Post, id=pk, owner=self.request.user)
        form = PostCreateForm(request.POST, request.FILES or None, instance=pic)

        if not form.is_valid() :
            ctx = {'form' : form}
            return render(request, self.template, ctx)

        pic = form.save(commit=False)
        pic.save()
        return redirect(self.success_url)

class PostDeleteView(OwnerDeleteView):
    model = Post

class PostCommentCreateView(LoginRequiredMixin, View):
    def post(self, request, pk) :
        post = get_object_or_404(Post, id=pk)
        comment = PostComment(text=request.POST['comment'], owner=request.user, post=post)
        comment.save()
        return redirect(reverse('cfis:post_detail', args=[pk]))

class PostCommentDeleteView(OwnerDeleteView):
    model = PostComment
    template_name = "cfis/post_comment_delete.html"

    # https://stackoverflow.com/questions/26290415/deleteview-with-a-dynamic-success-url-dependent-on-id
    def get_success_url(self):
        post = self.object.post
        return reverse('cfis:post_detail', args=[post.id])

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.db.utils import IntegrityError

@method_decorator(csrf_exempt, name='dispatch')
class AddFavoriteView(LoginRequiredMixin, View):
    def post(self, request, pk) :
        print("Add PK",pk)
        post = get_object_or_404(Post, id=pk)
        fav = Fave(user=request.user, post=post)
        try:
            fav.save()  # In case of duplicate key
        except IntegrityError as e:
            pass
        return HttpResponse()

@method_decorator(csrf_exempt, name='dispatch')
class DeleteFavoriteView(LoginRequiredMixin, View):
    def post(self, request, pk) :
        print("Delete PK",pk)
        post = get_object_or_404(Post, id=pk)
        try:
            fav = Fave.objects.get(user=request.user, post=post).delete()
        except Fave.DoesNotExist as e:
            pass

        return HttpResponse()


