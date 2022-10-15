from csv import DictReader
from sys import exit

from django.core.management import BaseCommand

from reviews.models import Category, Comment, Genre, Review, Title, User

CSV_TABLES = {
    'User': DictReader(open('static/data/users.csv')),
    'Category': DictReader(open('static/data/category.csv')),
    'Genre': DictReader(open('static/data/genre.csv')),
    'Title': DictReader(open('static/data/titles.csv')),
    'GenreTitle': DictReader(open('static/data/genre_title.csv')),
    'Review': DictReader(open('static/data/review.csv')),
    'Comment': DictReader(open('static/data/comments.csv')),
}


def delete_everything():
    Category.objects.all().delete()
    Genre.objects.all().delete()
    Title.objects.all().delete()
    Title.genre.through.all().delete()
    Comment.objects.all().delete()


def print_attention():
    print('Внимание! Будут уничтожены данные обо всех  '
          'категориях, жанрах, произведениях, обзорах и комментариях'
          'и заменены данными из CSV-файлов. Хотите продолжить ? [Y / N]: ')
    answer = input()
    if answer.upper() != 'Y':
        exit()


print_attention()
delete_everything()


class Command(BaseCommand):

    def handle(self, *args, **options):
        for value in CSV_TABLES['User']:
            User.objects.get_or_create(pk=value['id'],
                                       username=value['username'],
                                       role=value['role'],
                                       bio=value['bio'],
                                       first_name=value['first_name'],
                                       last_name=value['last_name'])
        for value in CSV_TABLES['Category']:
            Category.objects.get_or_create(pk=value['id'],
                                           name=value['name'],
                                           slug=value['slug'])
        for value in CSV_TABLES['Genre']:
            Genre.objects.get_or_create(pk=value['id'],
                                        name=value['name'],
                                        slug=value['slug'])
        for value in CSV_TABLES['Title']:
            title = Title.objects.get_or_create(pk=value['id'],
                                                name=value['name'],
                                                year=value['year'],
                                                category_id=value['category'])
        for value in CSV_TABLES['GenreTitle']:
            Title.genre.through.objects.get_or_create(pk=value['id'],
                                                      title_id=value['title_id'],
                                                      genre_id=value['genre_id'])
        for value in CSV_TABLES['Review']:
            title = Title.objects.get(pk=value['title_id'])
            author = User.objects.get(pk=value['author'])
            Review.objects.get_or_create(pk=value['id'],
                                         title_id=title,
                                         text=value['text'],
                                         author=author,
                                         score=value['score'],
                                         pub_date=value['pub_date'],)
        for value in CSV_TABLES['Comment']:
            review = Review.objects.get(pk=value['review_id'])
            author = User.objects.get(pk=value['author'])
            Comment.objects.get_or_create(pk=value['id'],
                                          review_id=review,
                                          text=value['text'],
                                          author=author,
                                          pub_date=value['pub_date'],)