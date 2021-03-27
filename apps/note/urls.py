from django.urls import path

from apps.note.views import NoteCreateView, NoteDeleteView, NoteDetailView, NoteEditView, NotesView

urlpatterns = [
    path('', NotesView.as_view(), name='notes'),
    path('new/', NoteCreateView.as_view(), name='note-create'),
    path('<int:pk>/', NoteDetailView.as_view(), name='note'),
    path('<int:pk>/delete/', NoteDeleteView.as_view(), name='note-delete'),
    path('<int:pk>/edit/', NoteEditView.as_view(), name='note-edit'),
]
