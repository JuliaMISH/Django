from django.shortcuts import render, get_object_or_404
from testytest.models import Product
from testytest.forms import ProductForm

def home_view(request, *args, **kwargs):
    return render(request, 'testytest/home.html', {})


def contact_view(request, *args, **kwargs):
    return render(request, 'testytest/contact.html', {})


def about_view(request, *args, **kwargs):
    my_context = {
        'my_text': "I'm Anton",
        "my_number": 123,
        "my_list": [100, 12, 34, 34, 100]
    }
    return render(request, 'testytest/about.html', my_context)


# def home_view(request, *args, **kwargs):
#     return render(request, 'home.html', {})

def product_detail_view(request, id):
    obj = Product.objects.get(id=id)
    # context = {
    #     'title': obj.title,
    #     'description': obj.description,
    #
    # }
    context = {
        'object': obj
    }

    return render(request, "testytest/product/detail.html", context)


def product_create_view(request):
    initial = {"title": "aaa from view"}
    obj = Product.objects.get(id=1)
    if obj != None:
        initial = None
    form = ProductForm(request.POST or None, initial= initial, instance = obj)
    if form.is_valid():
        form.save()
        form = ProductForm()

    context = {
        'form': form
    }

    return render(request, "testytest/product/create.html", context)

def dynamic_lookup_view(request, id):
    #obj = Product.objects.get(id=id)
    obj = get_object_or_404(Product, id=id)
    context = {
        "object": obj
    }
    return render(request, "testytest/product/detail.html", context)


def product_delete_view(request, id):
    #obj = Product.objects.get(id=id)
    obj = get_object_or_404(Product, id=id)
    if request.method == "POST":
        obj.delete()
    context = {
        "object": obj
    }
    return render(request, "testytest/product/delete.html", context)


def product_list_view(request):
    queryset = Product.objects.all()
    context = {
        "object_list": queryset
    }
    return render(request, "testytest/product/list.html", context)