from django.shortcuts import render
from django.http import *
from .models import Book, Author, BookInstance, Genre
from django.views import generic

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from .forms import AuthorsForm
from django.contrib.auth.mixins import LoginRequiredMixin



class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    '''
    Универсальный класс представления списка книг,
    находящихся в заказе у текущего пользователя.
    '''
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='2').order_by('due_back')

#----------------------------------------------------------
class BookCreate(CreateView):
    model = Book
    fields = '__all__'
    success_url = reverse_lazy('books')

class BookUpdate(UpdateView):
    model = Book
    fields = '__all__'
    success_url = reverse_lazy('books')

class BookDelete(DeleteView):
    model = Book
    success_url = reverse_lazy('books')
#------------------------------------------------------------


class BookListView(generic.ListView):
    paginate_by = 3
    model = Book


class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 4


class BookDetailView(generic.DetailView):
    model = Book


def index(request):
                #Генерация "количеств" некотор, главнь объектов
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
                #Доступные книги(статус='На складе')
                # Здесь метод 'all()' применен по умолчанию.
    num_instances_available = BookInstance.objects.filter(status__exact=2).count()
                # Авторы книг,
    num_authors = Author.objects.count()

  # количество посещений этого view, подсчитанное в переменной session
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

                #Отрисовка НТМL-шаблона index.html с данными
                #внутри переменной context
    return render(request, 'index.html',
                  context={'num_books': num_books,
                           'num_instances': num_instances,
                           'num_instances_available': num_instances_available,
                           'num_authors': num_authors,
                           'num_visits': num_visits
                        },
                  )
    return HttpResponse("Глaвнaя страница сайта Мир книг!")

#получение данных из БД и загрузка шаблона authors add.html
def authors_add(request):
    author = Author.objects.all()
    authorsform = AuthorsForm()
    return render(request, "catalog/authors_add.html",
                  {"form": authorsform, "author": author})

# сохранение данных об авторах в БД
def create(request):
    if request.method == "POST":
        author = Author()
        author.name =request.POST.get("first_name") #!!!!!!! name?
        author.last_name = request.POST.get("last_name")
        author.date_of_birth = request.POST.get("date_of_birth")
        author.date_of_death = request.POST.get("date_of_death")
        author.save()
        return HttpResponseRedirect("/authors_add")

#удаление авторов иэ БД
def delete(request, id):
    try:
        author = Author.objects.get(id=id)
        author.delete()
        return HttpResponseRedirect("/authors_add")
    except Author.DoesNotExist:
        return HttpResponseNotFound("<h2>Автор не найден</h2>")

#изменение данных в БД
def edit1(request, id):
    author = Author.objects.get(id=id)
    if request.method == "POST":
        author.name = request.POST.get("first_name")
        author.last_name = request.POST.get("last_name")
        author.date_of_birth = request.POST.get("date_of_birth")
        author.date_of_death = request.POST.get("date_of_death")
        author.save()
        return HttpResponseRedirect("/authors_add/")
    else:
        return render(request, "edit1.html", {"author": author})


