from django.shortcuts import render
from django.http import HttpResponse
from .models import Product, Contact, Order, OrderUpdate
from math import ceil
import json

# Create your views here.
def index(request):
    allProds = []
    catProds = Product.objects.values("category", 'id')
    cats = {item["category"] for item in catProds}

    for cat in cats:
        prod = Product.objects.filter(category=cat)
        n = len(prod)
        nSlides = nSlides = n//3 + ceil((n/3) - (n//3))
        allProds.append([prod, range(nSlides), nSlides])

    params = {"allProds":allProds}
    return render(request, "shop/index.html", params)

def searchMatch(query, item):
    if query in item.desc or query in item.product_name or query in item.category:
        return True
    else:
        return False

def search(request):
    allProds = []
    query = request.GET.get("query")

    catProds = Product.objects.values("category", 'id')
    cats = {item["category"] for item in catProds}

    for cat in cats:
        prodtemp = Product.objects.filter(category=cat)
        prod = [item for item in prodtemp if searchMatch(query, item)]
        n = len(prod)
        nSlides = nSlides = n//3 + ceil((n/3) - (n//3))

        if len(prod) != 0:
            allProds.append([prod, range(nSlides), nSlides])
    params = {"allProds":allProds, "msg":""}

    if len(allProds) == 0:
        params = {"msg":"Please make sure to enter releavent search query!"}



    return render(request, "shop/search.html", params)

def about(request):
    return render(request, "shop/about.html")


def contact(request):
    submitted = False
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        desc = request.POST.get("desc")

        Contact(name=name, email=email, phone=phone, desc=desc).save()

        submitted = True

        return render(request, "shop/contact.html")

    return render(request, "shop/contact.html", {"submitted":submitted})


def tracker(request):
    if request.method == "POST":
        Order_id = request.POST.get("Order_id")
        email = request.POST.get("email")

        try:
            order = Order.objects.filter(order_id=Order_id, email=email)

            if len(order) > 0:
                update = OrderUpdate.objects.filter(order_id=Order_id)
                updates = []

                for item in update:
                    updates.append({"text":item.update_desc, "time":item.timestamp})
                    response = json.dumps([updates, order[0].items_json], default=str)

                return HttpResponse(response)

        except Exception as error:
            return HttpResponse(json.dumps({}))

    return render(request, "shop/tracker.html")





def productView(request, myid):
    # Fetch the product using the id.
    product = Product.objects.get(id=myid)
    return render(request, "shop/prodView.html", {"product":product})


def checkout(request):
    if request.method == "POST":
        itemsJson = request.POST.get("itemsJson")
        name = request.POST.get("name")
        amount = request.POST.get("amount")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        state = request.POST.get("state")
        city = request.POST.get("city")
        zip_code = request.POST.get("zip_code")
        address = str(request.POST.get("address")) + " " + str(request.POST.get("address_2"))
        

        order = Order(items_json=itemsJson,name=name, email=email, address=address,state=state, city=city, zip_code=zip_code, phone=phone, amount=amount)

        order.save()

        update = OrderUpdate(order_id=order.order_id, update_desc="The order has been placed.")
        update.save()

        

        id = order.order_id

        thank = True
        return render(request, "shop/checkout.html", {"thank":thank, "id":id})
    return render(request, "shop/checkout.html")