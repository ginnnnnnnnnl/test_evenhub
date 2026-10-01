from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import get_object_or_404, redirect, render
from .models import Category, Event, Registration
from django.contrib import messages
from django.utils import timezone

@login_required
def event_list(request):
    # TODO: Query Event objects with the ORM.
    # Order by event_date.
    # Optionally filter by GET parameters:
    # category and status.
    events=Event.objects.all().order_by('event_date')
    # TODO: Query all Category objects for the filter form.
    categories = Category.objects.all()
    status = request.GET.get('status')
    category_id = request.GET.get('category')
    if status:
        events = events.filter(status=status)
    if category_id:
        events = events.filter(category_id=category_id)
    return render(request,"events/event_list.html",{"events":events, 'categories': categories, 'selected_category_id': category_id})

def event_detail(request,event_id):
    # TODO: Retrieve the Event with get_object_or_404().
    event= get_object_or_404(Event, id=event_id)
    # TODO: Retrieve event.registrations.all().
    registrations=event.registrations.all()
    return render(request,"events/event_detail.html",{
        "event":event,"registrations":registrations
    })

@login_required
def register_event(request,event_id):
    # TODO: Retrieve the event.
    event = get_object_or_404(Event, id=event_id)
    # TODO: Only register on POST.
    if request.method == 'POST':
        if Registration.objects.filter(event=event, user=request.user).exists():
            messages.error(request, 'You have already registered for this event.')
            return redirect("events:event_detail", event_id=event_id)
        status = event.status
        if status == 'finished':
            messages.error(request, 'You cannot register for a finished event.')
            return redirect("events:event_detail", event_id=event_id)
        capacity = event.capacity
        if capacity is not None and event.registrations.count() >= capacity:
            messages.error(request, 'This event is full. You cannot register.')
            return redirect("events:event_detail", event_id=event_id)
        Registration.objects.create(
            event=event,
            user=request.user
        )
        messages.success(request, 'You have successfully registered for the event.')
        return redirect('events:event_detail', event_id=event_id)
    # TODO: Use request.user.
    # TODO: Prevent duplicate registrations.
    return redirect("events:event_detail",event_id=event_id)

@permission_required("events.add_event",raise_exception=True)
def create_event(request):
    # TODO: On GET, show categories.
    category_list = Event.objects.all()
    categories = Category.objects.all()
    # TODO: On POST, create Event using request.POST and request.user.
    if request.method == 'POST':
        event = Event.objects.create(
            title = request.POST.get('title'),
            description = request.POST.get('description', ''),
            location = request.POST.get('location'),
            event_date = request.POST.get('event_date'),
            category_id = request.POST.get('category'),
            status = request.POST.get('status'),
            capacity = request.POST.get('capacity'),
            organizer = request.user,
            created_at = timezone.now()
        )
        return redirect("events:event_list")
    return render(request,"events/event_form.html", {'category_list': category_list, 'categories': categories})

@permission_required("events.change_event",raise_exception=True)
def edit_event(request,event_id):
    # TODO: Retrieve event.
    event = get_object_or_404(Event, id=event_id)
    # TODO: On POST, update fields and save().
    if request.method == 'POST':
        event.title = request.POST.get('title')
        event.description = request.POST.get('description', '')
        event.location = request.POST.get('location')
        event.event_date = request.POST.get('event_date')
        event.category_id = request.POST.get('category')
        event.status = request.POST.get('status')
        event.capacity = request.POST.get('capacity')
        event.save()
        return redirect('events:event_detail', event_id=event_id)
    return render(request,"events/event_form.html", {'event': event, 'categories': Category.objects.all()})

@permission_required("events.delete_event",raise_exception=True)
def delete_event(request,event_id):
    # TODO: Retrieve event.
    event = get_object_or_404(Event, id=event_id)
    # TODO: Delete only after POST.
    if request.method == 'POST':
        event.delete()
        return redirect("events:event_list")
    return render(request, 'events/delete_event.html', {'event': event})

def user_login(request):
    # TODO: Authentication task:
    # 1. Check POST.
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password,
        )
        if user is not None:
            login(request, user)
            return redirect('events:event_list')
    # 2. Read username/password.
    # 3. Call authenticate().
    # 4. If successful, call login(request,user).
    # 5. Redirect to event_list.
    # 6. Otherwise show an error.
    return render(request,"events/login.html")

def user_logout(request):
    # TODO: Call logout(request), then redirect to login.
    logout(request)
    return redirect("events:login")
