from django.shortcuts import render, redirect
from .models import Student
from django.contrib import messages
from django.db.models import Q


# Create your views here.
def home(request):
    query = request.GET.get('q')
    if query:
        students = Student.objects.filter(Q(name__icontains=query) | Q(city__icontains=query))
    else:
        students = Student.objects.all()
    return render(request, 'home.html',{'students': students})


def student_list(request):
    query = request.GET.get('q')
    sort = request.GET.get('sort')
    order = request.GET.get('order')

    students = Student.objects.all()

    if query:
        students = students.filter(
            Q(name__icontains=query) |
            Q(city__icontains=query)
        )

    if sort in ['name', 'city']:
        if order == 'desc':
            students = students.order_by(f'-{sort}')
        else:
            students = students.order_by(sort)

    return render(request, 'student_list.html', {
        'students': students
    })


def student_create(request):
    if request.method == 'POST':
        Student.objects.create(
            name=request.POST['name'],
            city=request.POST['city'],
            image=request.FILES['image'],
            documents=request.FILES['documents']
        )
        messages.success(request, "Student added successfully")
        return redirect('student_list')

    return render(request, 'student_form.html')


def student_update(request, id):
    student = Student.objects.get(id=id)

    if request.method == 'POST':
        student.name = request.POST['name']
        student.city = request.POST['city']

        if 'image' in request.FILES:
            student.image = request.FILES['image']

        if 'documents' in request.FILES:
            student.documents = request.FILES['documents']

        student.save()
        messages.success(request, "Student updated successfully")
        return redirect('student_list')

    return render(request, 'student_form.html', {'student': student})


def student_delete(request, id):
    student = Student.objects.get(id=id)
    student.delete()
    messages.success(request, "Student deleted successfully")
    return redirect('student_list')


def cart_add(request, id):
    cart = request.session.get('cart', [])

    cart.append(id)  # id ko cart mein add karo
    request.session['cart'] = cart

    return redirect('student_list')


def cart_detail(request):
    cart = request.session.get('cart', [])

    # Step 1: quantity dictionary manually banao
    counts = {}
    for item in cart:
        if item in counts:
            counts[item] += 1
        else:
            counts[item] = 1

    # Step 2: students fetch karo
    students = Student.objects.filter(id__in=counts.keys())

    # Step 3: cart_items build karo
    cart_items = []
    for student in students:
        cart_items.append({
            'student': student,
            'quantity': counts.get(student.id, 0)
        })

    return render(request, 'cart.html', {
        'cart_items': cart_items
    })


def cart_remove(request, id):
    cart = request.session.get('cart', [])

    if id in cart:
        cart.remove(id)   # sirf ek quantity kam

    request.session['cart'] = cart
    return redirect('cart_detail')
