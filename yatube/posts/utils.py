from django.core.paginator import Paginator


def paginator(request, posts, num=10):
    """Paginator func."""
    paginator = Paginator(posts, num)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return page_obj
