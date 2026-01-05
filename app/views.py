from django.shortcuts import render, redirect
from .models import Student
from django.contrib import messages


# Create your views here.
def home(request):
    return render(request, 'home.html')


def student_list(request):
    students = Student.objects.all()
    return render(request, 'student_list.html', {'students': students})


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
