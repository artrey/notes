from urllib.parse import urlencode

from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.db.models import Q  # noqa: WPS347
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView
from django.views.generic.edit import ModelFormMixin

from apps.note.models import Note


class NotesView(ListView):
    model = Note
    paginate_by = 20
    ordering = '-created_at'

    def get_queryset(self):
        qs = super().get_queryset()

        query = self.request.GET.get('q')
        if query:
            qs = qs.filter(Q(title__icontains=query) | Q(text__icontains=query))

        mode = self.request.GET.get('mode')

        if self.request.user.is_anonymous or mode == 'public':
            return qs.filter(is_public=True)

        if mode == 'owner':
            return qs.filter(author=self.request.user)

        return qs.filter(Q(is_public=True) | Q(author=self.request.user))  # noqa: WPS221

    def get_context_data(self, *, object_list=None, **kwargs):  # noqa: WPS210
        context = super().get_context_data(object_list=object_list, **kwargs)

        if context['is_paginated']:
            raw_params = {k: v for k, v in self.request.GET.items()}  # noqa: WPS111
            base_url = reverse('notes') + '?'  # noqa: WPS336
            page = context['page_obj']

            if page.has_previous():
                raw_params['page'] = page.previous_page_number()
                context['prev_url'] = base_url + urlencode(raw_params)

            if page.has_next():
                raw_params['page'] = page.next_page_number()
                context['next_url'] = base_url + urlencode(raw_params)

        return context


class NoteCreateView(CreateView):
    model = Note
    fields = 'title', 'text', 'is_public'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_anonymous:
            url_params = urlencode({REDIRECT_FIELD_NAME: reverse('note-create')})
            return redirect(settings.LOGIN_URL + '?' + url_params)  # noqa: WPS336
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        note = form.save(commit=False)
        note.author = self.request.user
        note.save()
        self.object = note
        return super(ModelFormMixin, self).form_valid(form)  # noqa: WPS608


class NoteDetailView(DetailView):
    model = Note


class NoteDeleteView(DeleteView):
    model = Note
    success_url = reverse_lazy('notes')

    def delete(self, request, *args, **kwargs):
        note = self.get_object()
        if request.user != note.author:
            return HttpResponse(status=403)  # noqa: WPS432
        return super().delete(request, *args, **kwargs)


class NoteEditView(UpdateView):
    model = Note
    fields_public = 'title', 'text'
    fields_private = fields_public + ('is_public',)

    def dispatch(self, request, *args, **kwargs):
        note = self.get_object()
        if note.is_public:
            self.fields = self.fields_public
        else:
            self.fields = self.fields_private
        return super().dispatch(request, *args, **kwargs)
