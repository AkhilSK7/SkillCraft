
from django.shortcuts import render, get_object_or_404,redirect
from django.views.generic import ListView,DetailView
from Tutor.models import Course,Module
from django.db.models import Q
from django.views import View
from courses.models import Enroll
import razorpay
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from users.models import CustomUser
from django.contrib.auth import login
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from courses.forms import ReviewForm
from courses.models import Review
from django.conf import settings
from django.http import Http404, FileResponse
import os


class EnrolledUserMixin(LoginRequiredMixin,UserPassesTestMixin):
    permission_denied_message = "You must enrolled to access this course"
    raise_exception = False

    def dispatch(self, request, *args, **kwargs):
        self.c=get_object_or_404(Course,id=kwargs['cid'])
        return super().dispatch(request,*args,**kwargs)
    def test_func(self):
        return Enroll.objects.filter(course=self.c,user=self.request.user,is_enrolled=True).exists()

    def handle_no_permission(self):
        return redirect("courses:course", id=self.c.id)
# Create your views here.

class CategoryView(ListView):
    model=Course
    template_name='courses/courses.html'
    paginate_by = 10
    def get_queryset(self):
        slug=self.kwargs.get('slug')
        return Course.objects.filter(category=slug)

class OfferProductsView(ListView):
    model=Course
    template_name='courses/courses.html'
    paginate_by = 10
    context_object_name = "course_list"
    def get_queryset(self):
        return Course.objects.filter(offer__gt=0)

class SearchView(ListView):
    model=Course
    template_name = 'courses/courses.html'
    paginate_by = 10
    def get_queryset(self):
        query=self.request.GET.get('q',"")
        if not query:
            return Course.objects.none()
        return Course.objects.filter(Q(course_name__icontains=query) | Q(description__icontains=query) |Q(category__icontains=query)|Q(Tutor__name__icontains=query))

class CourseDetailView(View):
    def dispatch(self, request, *args, **kwargs):
        self.c=Course.objects.get(id=kwargs['id'])
        return super().dispatch(request,*args,**kwargs)

    def get(self, request, id):
        reviews = Review.objects.filter(course=self.c)[:2]
        students=Enroll.objects.filter(course=self.c,is_enrolled=True).count()
        context = {"course": self.c, "reviews": reviews, "students": students}
        if request.user.is_authenticated:
            is_enrolled = Enroll.objects.filter(course=self.c,user=request.user,is_enrolled=True).exists()
            context["is_enrolled"]=is_enrolled
            has_reviewed = Review.objects.filter(course=self.c, user=request.user).exists()
            if is_enrolled and not has_reviewed:
                context["form"] = ReviewForm()
        else:
            is_enrolled = False
            context["is_enrolled"] = is_enrolled
        return render(request, "courses/coursedetail.html", context)
    def post(self,request, id):
        form_instance=ReviewForm(request.POST)
        if form_instance.is_valid():
            co=form_instance.save(commit=False)
            co.course=self.c
            co.user=request.user
            co.save()
            rating=Review.objects.filter(course=self.c).values_list("rating",flat=True)
            if len(rating) > 0:
                self.c.rating=sum(rating)/len(rating)
                self.c.save()
            return redirect('courses:course', id=self.c.id)


class PlayvideoView(EnrolledUserMixin,View):
    def get(self,request,cid,mid):
        m=Module.objects.get(id=mid)
        context={'course':self.c,'module':m}
        return render(request,'courses/coursedetail.html',context)

class DownloadDocumentView(EnrolledUserMixin, View):
    def get(self, request, cid, mid):
        module = get_object_or_404(Module, id=mid)
        file_path = module.document.path
        file_name = os.path.basename(file_path)
        return FileResponse(
            open(file_path, 'rb'),
            as_attachment=True,
            filename=file_name
        )


class EnrollView(View):
    def get(self,request,id):
        u=request.user
        c=Course.objects.get(id=id)
        total=c.discounted_price()

        enroll=Enroll(user=u,course=c,amount=total)
        client=razorpay.Client(auth=(settings.RAZORPAY_ID,settings.RAZORPAY_KEY))
        print(client)
        response_payment=client.order.create(dict(amount=total*100,currency='INR'))
        print(response_payment)
        id=response_payment['id']
        enroll.order_id=id
        enroll.save()
        context={'payment':response_payment,'razorpay_id':settings.RAZORPAY_ID}
        return render(request, 'courses/payment.html',context)


@method_decorator(csrf_exempt,name="dispatch")
class PaymentSuccessView(View):
    def post(self,request,i):
        u=CustomUser.objects.get(username=i)
        login(request,u,backend='allauth.account.auth_backends.AuthenticationBackend')
        payment_response=request.POST
        id=payment_response['razorpay_order_id']
        e=Enroll.objects.get(order_id=id)
        e.is_enrolled=True
        e.save()
        return render(request,'courses/paymentsuccess.html')

class EnrolledCoursesView(View):
    def get(self,request):
        u = request.user
        e = Enroll.objects.filter(user=u,is_enrolled=True)
        context={'enrolled':e}
        return render(request,'courses/enrolledcourses.html',context)
class ShowAllReviewsView(View):
    def get(self,request,id):
        course=get_object_or_404(Course.objects.prefetch_related('reviews'),id=id)
        context={'course':course}
        return render(request,'courses/reviews.html',context)

