from django.views import generic
from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Q
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib import messages
from .forms import SignUpForm, FeedbackForm, MediaFileForm, ModuleForm
from .models import UserProfile, Post, Module, Enrollment, Feedback, MediaFile, Notification

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from .serializers import UserProfileSerializer, PostSerializer, PostFormSerializer,ModuleSerializer

class SignUpView(generic.CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy("login")
    template_name = "../templates/registration/signup.html"

    def form_valid(self, form):
        response = super().form_valid(form)

        UserProfile.objects.create(
            user=self.object,
            user_type=form.cleaned_data['user_type'],
            email=form.cleaned_data['email'],
            dob=form.cleaned_data['dob'],
            first_name=form.cleaned_data['first_name'],
            last_name=form.cleaned_data['last_name'],
        )

        return response
    
@login_required
def dashboard(request):
    user_profile = request.user.userprofile

    if user_profile.user_type == 'student':
        template_name = 'student/student_dashboard.html'
    elif user_profile.user_type == 'teacher':
        template_name = 'teacher/teacher_dashboard.html'
    else:
        template_name = 'error_page.html'

    return render(request, template_name, {'username': request.user.username})


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def post_api(request):
    if request.method == 'GET':
        posts = Post.objects.filter(user=request.user.userprofile).order_by('-created_at')
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = PostFormSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            post = serializer.save()  
            response_serializer = PostSerializer(post)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@user_passes_test(lambda u: u.userprofile.user_type == 'teacher', login_url='/accounts/login/')
def user_dashboard(request, username):
    user_profile = get_object_or_404(UserProfile, user__username=username)
    posts = Post.objects.filter(user=user_profile).order_by('-created_at')

    return render(request, 'user_dashboard.html', {'user': user_profile.user, 'posts': posts})


@user_passes_test(lambda u: u.userprofile.user_type == 'teacher', login_url='/accounts/login/')
def search_results(request):
    search_query = request.GET.get('search_query').strip()
    search_results = None

    if search_query:
        search_results = User.objects.filter(
            Q(username__icontains=search_query))
    
    return render(request, 'teacher/search_results.html', {'search_results': search_results, 'search_query': search_query})


#profile page of users
def profile(request):
    return render(request, 'profile.html')


class UserProfileView(APIView):
    parser_classes = (MultiPartParser, FormParser,)

    def get(self, request, *args, **kwargs):
        user_profile = UserProfile.objects.get(user=request.user)
        serializer = UserProfileSerializer(user_profile, context={'request': request})
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        user_profile = UserProfile.objects.get(user=request.user)
        serializer = UserProfileSerializer(user_profile, data=request.data, context={'request': request}, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


###############Student Page Views###################
@login_required
def enrol(request):
    return render(request, 'student/enrol.html')


#available modules to enrol into
class AvailableModulesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        enrolled_modules = Enrollment.objects.filter(user=request.user).values_list('module', flat=True)
        available_modules = Module.objects.exclude(id__in=enrolled_modules)
        serializer = ModuleSerializer(available_modules, many=True)
        return Response(serializer.data)


class EnrollModuleView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, moduletitle, format=None):  
        module = get_object_or_404(Module, title=moduletitle) 
        user = request.user
        #creates a notification for the teacher
        Notification.objects.create(
            recipient=module.teacher.user, 
            notification_type='new_enrollment',
            sender_name=f"{user.first_name} {user.last_name}".strip() or user.username,
            item_title=module.title,
            item_url=f"/teacher_module_details/{module.title}/",  
            date_created=timezone.now()
        )        

        #check if the user is already enrolled
        if not Enrollment.objects.filter(user=user, module=module).exists():
            #create a new enrollment
            Enrollment.objects.create(user=user, module=module)
            return Response({'status': 'enrolled'}, status=status.HTTP_201_CREATED)

        return Response({'status': 'already enrolled'}, status=status.HTTP_400_BAD_REQUEST)


class ModuleDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, moduletitle, format=None):
        module = get_object_or_404(Module, title=moduletitle)
        serializer = ModuleSerializer(module)
        return Response(serializer.data)
    

#module detail page and enrol action 
@login_required
def module_detail(request, moduletitle):
    module = get_object_or_404(Module, title=moduletitle)
    return render(request, 'student/module_detail.html', {'module': module})


#view for enrolled modules page
@login_required
def enrolled_modules(request):
    enrolled_module_ids = Enrollment.objects.filter(user=request.user).values_list('module', flat=True)  #this gets the IDs of modules enrolled by the current logged in user
    enrolled_modules = Module.objects.filter(id__in=enrolled_module_ids) #this gets the enrolled modules based on the IDs from prev line 

    return render(request, 'student/enrolled_modules.html', {'enrolled_modules': enrolled_modules})


#enrolled modules details
@login_required
def enrolled_module_details(request, moduletitle):
    module = get_object_or_404(Module, title=moduletitle)
    
    return render(request, 'student/enrolled_module_details.html', {'module': module})


#students create feedback view 
def feedback(request):
    user = request.user
    feedbacks = Feedback.objects.filter(user=user)

    if request.method == 'POST':
        form = FeedbackForm(user, request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.user = user
            feedback.save()
            return redirect('feedback')
    else:
        form = FeedbackForm(user)

    return render(request, 'student/feedback.html', {'form': form, 'feedbacks': feedbacks})


########## Teacher page view ##############
@login_required
@user_passes_test(lambda u: u.userprofile.user_type == 'teacher', login_url='/accounts/login/')
def teacher_modules(request):
    teacher_modules = Module.objects.filter(teacher=request.user.userprofile)
    return render(request, 'teacher/teacher_module.html', {'teacher_modules': teacher_modules})


@login_required
@user_passes_test(lambda u: u.userprofile.user_type == 'teacher', login_url='/accounts/login/')
def teacher_module_details(request, moduletitle):
    module = get_object_or_404(Module, title=moduletitle)

    if request.method == 'POST':
        form = request.FILES.get('file')
        if form:
            MediaFile.objects.create(module=module, file=form)

    return render(request, 'teacher/teacher_module_details.html', {'module': module})


@login_required
@user_passes_test(lambda u: u.userprofile.user_type == 'teacher', login_url='/accounts/login/')
def remove_student(request, module_id, user_id):
    if request.method == "POST":
        module = get_object_or_404(Module, id=module_id)
        enrollment = get_object_or_404(Enrollment, module=module, user_id=user_id)
        enrollment.delete()
        messages.success(request, "Student removed successfully.")
    return redirect('teacher_module_details', moduletitle=module.title)


#upload new course materials
@user_passes_test(lambda u: u.userprofile.user_type == 'teacher', login_url='/accounts/login/')
def upload_material(request, moduleid):
    module = get_object_or_404(Module, id=moduleid)

    if request.method == 'POST':
        form = MediaFileForm(request.POST, request.FILES)
        if form.is_valid():
            media_file = form.save(commit=False) #this saves the media file with the associated module
            media_file.module = module
            media_file.save()

            messages.success(request, 'Material uploaded successfully.')
            return redirect('teacher_module_details', moduletitle=module.title)
    else:
        form = MediaFileForm()

    return render(request, 'your_upload_template.html', {'form': form, 'module': module})


#create new module
@login_required
@user_passes_test(lambda u: u.userprofile.user_type == 'teacher', login_url='/accounts/login/')
def add_module(request):
    if request.method == 'POST':
        form = ModuleForm(request.POST, request.FILES)
        if form.is_valid():
            module = form.save(commit=False)
            module.teacher = request.user.userprofile
            module.save()

            students = User.objects.filter(userprofile__user_type='student')

            for student in students:
                Notification.objects.create(
                    recipient=student,
                    notification_type='new_course',
                    sender_name=request.user.get_full_name() or request.user.username,
                    item_title=module.title,
                    item_url=f"/enrolled_module_details/{module.title}/",  
                    date_created=timezone.now()
                )

            return redirect('teacher_modules') 
    else:
        form = ModuleForm()

    return render(request, 'teacher/add_new_module.html', {'form': form})


@user_passes_test(lambda u: u.userprofile.user_type == 'teacher', login_url='/accounts/login/')
def module_feedback(request, moduletitle):
    module = get_object_or_404(Module, title=moduletitle)
    feedbacks = Feedback.objects.filter(module=module)

    return render(request, 'teacher/module_feedback.html', {'module': module, 'feedbacks': feedbacks})


@login_required
def user_notifications(request):
    notifications = Notification.objects.filter(recipient=request.user).order_by('-date_created')
    return render(request, 'notifications.html', {'notifications': notifications})


def enter_chat(request):
    return render(request, 'chat/enter_chat.html')


def chat_room(request, room_name):
    return render(request, 'chat/chat_room.html', {'room_name': room_name})