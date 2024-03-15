from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,

)

urlpatterns =[
    path('api/student',views.StudentList.as_view()),
    path('api/student/<int:id>',views.studentDetails.as_view()),
    path('api/department',views.DepartmentView.as_view()),
    path('api/addressone',views.AddressOneView.as_view()),
    path('api/addresstwo',views.AddressTwoView.as_view()),
    path('api/student/search',views.SearchForStuden.as_view()),
    
    path("api/logout",views.LogoutView.as_view(),name='logout'),
    path('api/employee',views.EmpolyeeList.as_view()),
    path("api/employee/<int:id>",views.EmpolyeeDetails.as_view()),

    #path for mobile application
    path('api/login',views.LoginView.as_view(), name='login'),
    path('password/reset/',views.PasswordResetRequestView.as_view(), name='password_reset'),
    path('reset-password/<str:uid>/<str:token>/',views.ResetPasswordView.as_view(),name = 'reset_password'),
    path("api/post/buses",views.BusesPostWithNoAuthentication.as_view()),
    path("api/post/student",views.StudentPostWithNoAuthentication.as_view()),
    path("api/post/empolyee",views.EmpolyeePostWithNoAuthentication.as_view()),
    # path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]