from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Book, BookCategory, BookCategoryDetail, Merchandise
from django.db.models import Count, Q, F
# Create your views here.

def get_books(request, url_category):
    ## Get category, children categories
    category = BookCategory.objects.filter(url_name = url_category).first()
    children_categories = category.bookcategory_set.annotate(num_books=Count('bookcategorydetail'))
    ## Get books and paging
    merchandises = Merchandise.objects.raw('''
        SELECT 
            `merchandise`.*, `image`.`url`, `book`.`name`, `book`.`publisher`, `book`.`publication_date`,
            `book`.`width`, `book`.`height`, `book`.`length`, `book`.`pages_num`,
            (SELECT `tb_cat`.`name` 
                FROM `book_category` `tb_cat` JOIN `book_category_detail` `tb_det`
                ON `tb_cat`.`id` = `tb_det`.`id_category`
                WHERE `tb_det`.`id_book` = `book`.`id` 
                ORDER BY `tb_cat`.`id` DESC
                LIMIT 1) AS `category`, 
            (`merchandise`.`total_star`/`merchandise`.`times_rated`) AS `rate_point`
        FROM
            `merchandise` JOIN `book` JOIN `book_category_detail` JOIN `book_category` JOIN `merchandise_image` JOIN `image`
            ON `merchandise`.`id` = `book`.`id`
                AND `book`.`id` = `book_category_detail`.`id_book`
                AND `book_category_detail`.`id_category` = `book_category`.`id`
                AND `merchandise_image`.`id_merchandise` = `merchandise`.`id`
                AND `merchandise_image`.`id_image` = `image`.`id`
        WHERE
            `book_category`.`url_name` = %s
                AND `merchandise`.`blocked_date` IS NULL
                AND `merchandise`.`stopped_date` IS NULL
                AND `merchandise`.`activated_date` IS NOT NULL
        GROUP BY `id`;
    ''',[url_category])
    paginator = Paginator(merchandises, 9)
    page_number = request.GET.get('page')
    pager = paginator.get_page(page_number)
    page_navigator = []
    for i in range(max(1, pager.number - 2), pager.number):
        page_navigator.append(i)
    page_navigator.append(pager.number)
    for i in range(pager.number + 1, min(pager.number + 2, pager.paginator.num_pages) + 1):
        page_navigator.append(i)
    
    
    return render(request, 'book/books.html', {
        'pager':pager, 'page_navigator': page_navigator, 'children_categories':children_categories, 'current_category':category})

def get_book(request, id):
    #merchandise = get_object_or_404(Merchandise, pk=id).annotate(rate_point=F('total_star')/F('times_rated'))
    merchandise = Merchandise.objects.annotate(rate_point=F('total_star')/F('times_rated')).get(pk=id)
    book = get_object_or_404(Book, pk=merchandise.id_product)
    return render(request, 'book/book.html', {
        'merchandise': merchandise,
        'book': book,
    })