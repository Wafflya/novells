import json

from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import DetailView, ListView
from django.contrib.auth.decorators import login_required

from .models import Novell, Chapter, LikeDislike, Profile, Genre
from .forms import CommentForm, EditProfileForm
from django.http import HttpResponse


# Create your views here.
class GenreYear:

    def get_genres(self):
        return Genre.objects.all()

    def get_year(self):
        return Novell.objects.all().order_by('publish__year').values_list('publish__year').distinct()


def index(request):
    pop_novell = Novell.objects.order_by('-views').first()
    shedule_chapter = Chapter.objects.filter(status=False).order_by('publish')[:4]
    all_novells = Novell.objects.all()
    return render(request, 'core/home.html', {'pop': pop_novell,
                                              'shedule_chapter': shedule_chapter,
                                              'all_novells': all_novells,
                                              })


class NovellDetailView(GenreYear, DetailView):
    model = Novell
    context_object_name = 'novell'
    template_name = 'core/novell_profile.html'


class ChapterDetailView(DetailView):
    model = Chapter
    context_object_name = 'chapter'
    template_name = 'core/chapter_detail.html'

    def get_object(self):
        nov = get_object_or_404(Novell, slug=self.kwargs['slug'])
        return get_object_or_404(Chapter, novell=nov, number=self.kwargs['number'])


class AddComment(View):

    def post(self, request, pk):
        if request.method == 'POST':
            form = CommentForm(data=request.POST)
            chapter = Chapter.objects.get(id=pk)
            if form.is_valid():
                form = form.save(commit=False)
                if request.POST.get("parent", None):
                    form.parent_id = int(request.POST.get("parent"))
                form.chapter = chapter
                form.author = request.user
                form.save()
            return redirect(form.get_absolute_url())


class VotesView(View):
    model = None  # Модель данных - Статьи или Комментарии
    vote_type = None  # Тип комментария Like/Dislike

    def post(self, request, id):
        obj = self.model.objects.get(id=id)
        # author_profile = obj.author.user_profile
        # GenericForeignKey не поддерживает метод get_or_create
        try:
            likedislike = LikeDislike.objects.get(content_type=ContentType.objects.get_for_model(obj), object_id=obj.id,
                                                  user=request.user)

            if likedislike.vote is not self.vote_type:
                likedislike.vote = self.vote_type
                likedislike.save(update_fields=['vote'])
                result = True
            else:
                # if obj.author != request.user:
                #    author_profile.karma -= likedislike.vote
                #    author_profile.save(update_fields=['karma'])
                likedislike.delete()
                result = False

        except LikeDislike.DoesNotExist:
            obj.votes.create(user=request.user, vote=self.vote_type)
            result = True

        return HttpResponse(
            json.dumps({
                "result": result,
                "like_count": obj.votes.likes().count(),
                "dislike_count": obj.votes.dislikes().count(),
                "sum_rating": obj.votes.sum_rating()
            }),
            content_type="application/json"
        )


@login_required
def add_to_bookmark(request, pk):
    nov = get_object_or_404(Novell, pk=pk)
    request.user.user_profile.bookmarks.add(nov)
    return redirect(nov.get_absolute_url())


@login_required
def del_from_bookmark(request, pk, frommm):
    nov = get_object_or_404(Novell, pk=pk)
    request.user.user_profile.bookmarks.remove(nov)
    if frommm == 'profile':
        return redirect(request.user.user_profile.get_absolute_url())
    else:
        return redirect(nov.get_absolute_url())


class ProfileDetail(DetailView):
    model = Profile
    context_object_name = 'profile'
    template_name = 'core/profile/profile_detail.html'


class EditMyProfile(DetailView, View):
    model = Profile
    context_object_name = 'profile'
    template_name = 'core/profile/edit_profile.html'

    def post(self, request, pk, slug):
        profile = Profile.objects.get(id=pk)
        if request.user == profile.name:
            profile_form = EditProfileForm(request.POST, instance=profile)
            if profile_form.is_valid():
                if 'avatar' in request.FILES:
                    profile.avatar = request.FILES['avatar']
                profile_form.save()
            return redirect(profile.get_absolute_url())
        else:
            return HttpResponse('Permission deny')


class NovellListView(GenreYear, ListView):
    template_name = 'core/novells_list.html'
    model = Novell
    context_object_name = 'novells'


class FilterNovellsView(GenreYear, ListView):
    template_name = 'core/novells_list.html'
    context_object_name = 'novells'

    def get_queryset(self):
        genre_filter = self.request.GET.getlist('genre')
        year_filter = self.request.GET.getlist('year')
        if genre_filter and year_filter and len(genre_filter) == 1:
            return Novell.objects.filter(publish__year__in=year_filter, genres__in=genre_filter)
        elif len(genre_filter) > 1 and year_filter:
            genres_in_filter = [Genre.objects.get(id=i) for i in genre_filter]
            a = []
            for i in Novell.objects.filter(publish__year__in=year_filter):
                if set(genres_in_filter) <= set(i.genres.all()):
                    a.append(i)
            return a
        elif len(genre_filter) > 1 and not year_filter:
            genres_in_filter = [Genre.objects.get(id=i) for i in genre_filter]
            a = []
            for i in Novell.objects.all():
                if set(genres_in_filter) <= set(i.genres.all()):
                    a.append(i)
            return a
        elif not year_filter and not genre_filter:
            return Novell.objects.all()
        else:
            return Novell.objects.filter(Q(publish__year__in=year_filter) | Q(genres__in=genre_filter)).distinct()
        # print(self.request.GET.getlist('year'))
