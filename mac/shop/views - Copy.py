from django.shortcuts import render
from django.http import HttpResponse
from .models import Product, Contact, Order, OrderUpdate
from math import ceil
import json

# Create your views here.
def index(request):
    # products = Product.objects.all()
    # n = len(products)
    # nSlides = n//3 + ceil((n/3) - (n//3))
    # params = {"products":products, "nSlides":nSlides, "range":range(nSlides)}
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


def about(request):
    return render(request, "shop/about.html")


def contact(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        desc = request.POST.get("desc")

        Contact(name=name, email=email, phone=phone, desc=desc).save()

        submitted = True

        return render(request, "shop/contact.html", {"submitted":submitted})

    return render(request, "shop/contact.html")


def tracker(request):
    if request.method == "POST":
        Order_id = request.POST.get("Order_id")
        email = request.POST.get("email")
        print(Order_id, email)

        try:
            order = Order.objects.filter(order_id=Order_id, email=email)

            if len(order) > 0:
                update = OrderUpdate.objects.filter(order_id=Order_id)
                updates = []

                for item in update:
                    updates.append({"text":item.update_desc, "time":item.timestamp})
                    response = json.dumps(updates, default=str)

                return HttpResponse(response)

        except Exception as error:
            return HttpResponse(json.dumps({}))

    return render(request, "shop/tracker.html")


def search(request):
    return render(request, "shop/search.html")


def productView(request, myid):
    # Fetch the product using the id.
    product = Product.objects.get(id=myid)
    return render(request, "shop/prodView.html", {"product":product})


def checkout(request):
    if request.method == "POST":
        itemsJson = request.POST.get("itemsJson")
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        state = request.POST.get("state")
        city = request.POST.get("city")
        zip_code = request.POST.get("zip_code")
        address = str(request.POST.get("address")) + " " + str(request.POST.get("address_2"))
        

        order = Order(items_json=itemsJson,name=name, email=email, address=address,state=state, city=city, zip_code=zip_code, phone=phone)

        order.save()

        update = OrderUpdate(order_id=order.order_id, update_desc="The order has been placed.")
        update.save()

        

        id = order.order_id

        thank = True
        return render(request, "shop/checkout.html", {"thank":thank, "id":id})
    return render(request, "shop/checkout.html")