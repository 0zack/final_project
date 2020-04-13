from cfis.models import News, NewsComment

from django.views import View
from cfis.forms import CreateForm
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.conf import settings

from cfis.forms import CommentForm
from cfis.owner import OwnerListView, OwnerDetailView, OwnerCreateView, OwnerUpdateView, OwnerDeleteView

class HomeView(View):
    def get(self, request) :
        print(request.get_host())
        host = request.get_host()
        islocal = host.find('localhost') >= 0 or host.find('127.0.0.1') >= 0
        context = {
            'installed' : settings.INSTALLED_APPS,
            'islocal' : islocal
        }
        return render(request, 'cfis/main.html', context)

class NewsListView(OwnerListView):
    model = News
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

# class AdCreateView(OwnerCreateView):
#     model = Ad
#     fields = ['title', 'price', 'text']

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

# class AdUpdateView(OwnerUpdateView):
#     model = Ad
#     fields = ['title', 'price', 'text']

class NewsUpdateView(LoginRequiredMixin, View):
    template = 'cfis/ad_form.html'
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
        return redirect(reverse('ads:ad_detail', args=[pk]))

class NewsCommentDeleteView(OwnerDeleteView):
    model = NewsComment
    template_name = "ads/comment_delete.html"

    # https://stackoverflow.com/questions/26290415/deleteview-with-a-dynamic-success-url-dependent-on-id
    def get_success_url(self):
        news = self.object.news
        return reverse('cfis:ad_detail', args=[news.id])

