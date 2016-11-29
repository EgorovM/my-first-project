from django.shortcuts import render
from .models import Order, Comment
from django.shortcuts import render
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def index(request):
    if request.method == "POST":
        if "ok_button" in request.POST:
            telephone = request.POST["telephone"]
            problem   = request.POST["problem"]

            orr = Order()

            orr.telephone = telephone
            orr.problem   = problem
            orr.pub_date  = timezone.now()
            orr.save()

    latest_order_list = Order.objects.all()[::-1]

    paginator = Paginator(latest_order_list,3)

    page = request.GET.get('page')
    try:
        latest_order_list = paginator.page(page)
    except PageNotAnInteger:
        latest_order_list = paginator.page(1)
    except EmptyPage:
        latest_order_list = paginator.page(paginator.num_pages)

    context = {"latest_order_list":latest_order_list,"paginator":paginator,}

    return render(request, "help/index.html",context)

def order(request, order_id):
    if request.method == "POST":
        if "ok_button" in request.POST:
            comment_text     = request.POST["comment_text"]
            orr              = Order.objects.get(id=order_id)

            cmt              = Comment()

            cmt.order_info   = orr
            cmt.comment_text = comment_text
            cmt.save()

    latest_cmt_list = Comment.objects.all()[::-1]
    order = Order.objects.get(id = order_id)

    contex = {"latest_cmt_list":latest_cmt_list,"order":order,}

    return render(request, "help/order.html", contex)


