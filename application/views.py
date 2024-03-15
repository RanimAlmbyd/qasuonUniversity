from django.shortcuts import render
from django.http import HttpResponse
from .models import (Student,
                        User,
                        Department,
                        AddressOne,
                        AddressTwo,
                        Empolyee,
                        Buses)
from .serializer import (StudentSerializer,
                            StudentSerializerPost,
                            StudentSerializerPut,
                            DepatrtmentSerializer,
                            AddressOneSerializer,
                            AddressTwoSerializer,
                            LodinSerializer,
                            EmpolyeeSerializer,
                            EmpolyeeSerializerPost,
                            EmpolyeeSerializerPut,
                            BussesSerializerPost,
                            PasswordResetSerializer,
                            PasswordResetSerializerClass,
                            )
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token 
from django.shortcuts import get_object_or_404
from django.db.models import Q
import urllib.parse
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
# from .authentication import CustomJWTAuthentication
# Create your views here.

# {
# "username":"ranim",
# "password":"123456789"
# }




class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        try:
            refresh_token = request.data.get("refresh_token")
            print(refresh_token)
            token = RefreshToken(refresh_token)
            print(token)
            # token = Token.objects.get(user=self.request.user)
            # token.delete()
            
            token.blacklist()
            print("add to balcklist")
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            print("Error to add in black list")
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
            
class LoginView(APIView):
    permission_classes =[]
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user :
            if user.type_user == 'superuser':
                Token.objects.update_or_create(user=user)
                refresh = RefreshToken.for_user(user)
                return Response({
                "username":user.username,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                }, status=status.HTTP_200_OK)
                # or user.type_user == 'employee' or
            elif  user.type_user == 'bus':
                busobj=Buses.objects.get(user=user.id)
                Token.objects.update_or_create(user=user)
                refresh = RefreshToken.for_user(user)
                return Response({
                "firstname":busobj.firstname,
                "lastname":busobj.lastname,
                "numberofbus":busobj.number,
                "phone":busobj.phone,
                "username":user.username,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                }, status=status.HTTP_200_OK)
            elif  user.type_user == 'student':
                studentobj=Student.objects.get(user=user.id)
                Token.objects.update_or_create(user=user)
                refresh = RefreshToken.for_user(user)
                return Response({
                "firstname":studentobj.firstname,
                "lastname":studentobj.lastname,
                "address1":studentobj.address1.id,
                "address2":studentobj.address2.id,
                "department":studentobj.department.id,
                "year":studentobj.year,
                "username":user.username,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                }, status=status.HTTP_200_OK)
            elif  user.type_user == 'employee':
                employeeobj=Empolyee.objects.get(user=user.id)
                Token.objects.update_or_create(user=user)
                refresh = RefreshToken.for_user(user)
                return Response({
                "firstname":employeeobj.firstname,
                "lastname":employeeobj.lastname,
                "address1":employeeobj.address1.id,
                "address2":employeeobj.address2.id,
                "job":employeeobj.job,
                "username":user.username,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                }, status=status.HTTP_200_OK)    
            else:
                return Response({'error': 'Not User'}, status=status.HTTP_401_UNAUTHORIZED)            
        else:
            try :
                usernameerror = get_object_or_404(User,username = username)
                return Response({'error': 'password is un correct '}, status=status.HTTP_400_BAD_REQUEST)
            except:    
                return Response({'error': 'username is not valide'}, status=status.HTTP_400_BAD_REQUEST)

class DepartmentView(APIView):
    permission_classes =[]
    def get (self,request):
        objects = Department.objects.all()
        serializer=DepatrtmentSerializer(objects,many=True)
        # user=self.request.user
        # print("Authentication user",user.id)
        count=len(serializer.data)
        expected_data ={
            "count":count,
            "allDepartment":serializer.data ,
        }
        json_data ={
            "code" : 200,
            "message" : "success",
            "data" :expected_data
        }
        return Response(json_data, status=status.HTTP_200_OK)

class AddressOneView(APIView):
    permission_classes =[]
    def get (self,request):
        objects = AddressOne.objects.all()
        serializer=AddressOneSerializer(objects,many=True)
        count=len(serializer.data)
        expected_data ={
            "count":count,
            "allAddressOne":serializer.data ,
        }
        json_data ={
            "code" : 200,
            "message" : "success",
            "data" :expected_data
        }
        return Response(json_data, status=status.HTTP_200_OK) 

class AddressTwoView(APIView):
    permission_classes =[]
    def get (self,request):
        objects = AddressTwo.objects.all()
        serializer=AddressTwoSerializer(objects,many=True)
        count=len(serializer.data)
        expected_data ={
            "count":count,
            "allAddressTwo":serializer.data ,
        }
        json_data ={
            "code" : 200,
            "message" : "success",
            "data" :expected_data
        }
        return Response(json_data, status=status.HTTP_200_OK)      

class StudentList(APIView):
    permission_classes = [IsAuthenticated]
    def get (self,request):
        objects=Student.objects.all()
        serializer=StudentSerializer(objects,many=True)
        count=len(serializer.data)
        expected_data ={
            "count":count,
            "allStudent":serializer.data ,
        }
        json_data ={
            "code" : 200,
            "message" : "success",
            "data" :expected_data
        }
        return Response(json_data, status=status.HTTP_200_OK)

    def post(self,request,format=None):
        serializer=StudentSerializerPost(data=request.data)
        serializer.is_valid(raise_exception=True)
        student=serializer.save()
        # user = get_object_or_404(User, id=student.user_id)
        # token, created = Token.objects.get_or_create(user_id=user.id)
        json_data ={
            "code" : 200,
            "message" : "success",
            "data" :serializer.data
        }
        return Response(json_data,status=status.HTTP_200_OK)
    
class studentDetails(APIView):
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self,id):
        return {"user":self.get_object(id).user.id}

    def get_object(self,id):
        try:
            return Student.objects.get(id = id)
        except:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    def get(self,request,id):
        student=self.get_object(id)
        serializer=StudentSerializer(student)
        expected_data ={
            "count":1,
            "allStudent":serializer.data ,
        }
        json_data ={
            "code" : 200,
            "message" : "success",
            "data" :expected_data
        }
        return Response(json_data, status=status.HTTP_200_OK)

    def put(self,request,id):
        student = self.get_object(id)
        serializer=StudentSerializerPut(instance=student, data=request.data ,context=self.get_serializer_context(id)) 
        serializer.is_valid(raise_exception=True)
        serializer.save()
        expected_data ={
            "count":1,
            "allStudent":serializer.data ,
        }
        json_data ={
            "code" : 200,
            "message" : "success",
            "data" :expected_data
        }
        return Response(json_data, status=status.HTTP_200_OK)    

    def delete(self,request,id):
        student=self.get_object(id)
        print('user fro student',student.user.id)
        user=User.objects.get(id=student.user.id)
        print('user fro student',user)
        user.delete()
        student.delete()
        json_data ={
            "code" : 200,
            "message" : "success",
        }
        return Response(json_data,status=status.HTTP_204_NO_CONTENT)    

class SearchForStuden(APIView):
    permission_classes = []
    def get(self,request):
        queryset =Student.objects.all()
        query = request.query_params.get('query', '')
        decoded_string = urllib.parse.unquote(query)
        splitted_string = decoded_string.split()

        if len(splitted_string) == 1:
            queryset=queryset.filter(firstname__icontains=splitted_string[0])
            if len(queryset) == 0:
                queryset =Student.objects.all()
                queryset=queryset.filter(lastname__icontains=splitted_string[0])
                if len(queryset) == 0:
                    queryset =Student.objects.all()
                    try:
                        user = User.objects.get(username__icontains=splitted_string[0])
                        queryset= queryset.filter(user=user)
                        serializer=StudentSerializer(queryset,many=True)
                        count=len(serializer.data)
                        expected_data ={
                            "count":count,
                            "allStudent":serializer.data ,
                        }
                        json_data ={
                            "code" : 200,
                            "message" : "success",
                            "data" :expected_data
                        }

                        return Response(json_data, status=status.HTTP_200_OK)   
                    except:
                        queryset =Student.objects.all()
                        serializer=StudentSerializer(queryset,many=True)
                        count=len(serializer.data)
                        expected_data ={
                            "count":count,
                            "allStudent":serializer.data ,
                        }
                        json_data ={
                            "code" : 200,
                            "message" : "success",
                            "data" :expected_data
                        }

                        return Response(json_data, status=status.HTTP_404_NOT_FOUND) 

        if len(splitted_string) == 2:
            queryset=queryset.filter(Q(firstname__icontains=splitted_string[0])|Q(lastname__icontains=splitted_string[1]))
            serializer=StudentSerializer(queryset,many=True)
            count=len(serializer.data)
            expected_data ={
                "count":count,
                "allStudent":serializer.data ,
            }
            json_data ={
                "code" : 200,
                "message" : "success",
                "data" :expected_data
            }

            return Response(json_data, status=status.HTTP_200_OK)        

class EmpolyeeList(APIView):
    permission_classes = [IsAuthenticated]
    def get (self,request):
        objects=Empolyee.objects.all()
        serializer=EmpolyeeSerializer(objects,many=True)
        count=len(serializer.data)
        expected_data ={
            "count":count,
            "allEmployee":serializer.data ,
        }
        json_data ={
            "code" : 200,
            "message" : "success",
            "data" :expected_data
        }
        return Response(json_data, status=status.HTTP_200_OK)

    def post(self,request,format=None):
        serializer=EmpolyeeSerializerPost(data=request.data)
        serializer.is_valid(raise_exception=True)
        student=serializer.save()
        # user = get_object_or_404(User, id=student.user_id)
        # token, created = Token.objects.get_or_create(user_id=user.id)
        json_data ={
            "code" : 200,
            "message" : "success",
            "data" :serializer.data
        }
        return Response(json_data,status=status.HTTP_200_OK)    

class EmpolyeeDetails(APIView):
    permission_classes = [IsAuthenticated]
    def get_serializer_context(self,id):
        return {"user":self.get_object(id).user.id}
    def get_object(self,id):
        try:
            return Empolyee.objects.get(id = id)
        except:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    def get(self,request,id):
        employee=self.get_object(id)
        serializer=EmpolyeeSerializer(employee)
        expected_data ={
            "count":1,
            "allEmployee":serializer.data ,
        }
        json_data ={
            "code" : 200,
            "message" : "success",
            "data" :expected_data
        }
        return Response(json_data, status=status.HTTP_200_OK)

    def put(self,request,id):
        employee = self.get_object(id)
        serializer=EmpolyeeSerializerPut(instance=employee,data=request.data,context=self.get_serializer_context(id)) 
        serializer.is_valid(raise_exception=True)
        serializer.save()
        expected_data ={
            "count":1,
            "allEmployee":serializer.data ,
        }
        json_data ={
            "code" : 200,
            "message" : "success",
            "data" :expected_data
        }
        return Response(json_data, status=status.HTTP_200_OK)    

    def delete(self,request,id):
        employee=self.get_object(id)
        user=User.objects.get(id=employee.user.id)
        user.delete()
        employee.delete()
        json_data ={
            "code" : 200,
            "message" : "success",
        }
        return Response(json_data,status=status.HTTP_204_NO_CONTENT) 

################################### Start Fluter Api ###############################################################
class BusesPostWithNoAuthentication(APIView):
    permission_classes=[]
    def post(self,request):
        serializer=BussesSerializerPost(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        # user = get_object_or_404(User, id=student.user_id)
        # token, created = Token.objects.get_or_create(user_id=user.id)
        json_data ={
            "code" : 200,
            "message" : "success",
            "data" :serializer.data
        }
        return Response(json_data,status=status.HTTP_200_OK)

class StudentPostWithNoAuthentication(APIView):
    permission_classes=[]
    def post(self,request):
        serializer=StudentSerializerPost(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        # user = get_object_or_404(User, id=student.user_id)
        # token, created = Token.objects.get_or_create(user_id=user.id)
        json_data ={
            "code" : 200,
            "message" : "success",
            "data" :serializer.data
        }
        return Response(json_data,status=status.HTTP_200_OK)       

class EmpolyeePostWithNoAuthentication(APIView):
    permission_classes=[]
    def post(self,request):
        serializer=EmpolyeeSerializerPost(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        # user = get_object_or_404(User, id=student.user_id)
        # token, created = Token.objects.get_or_create(user_id=user.id)
        json_data ={
            "code" : 200,
            "message" : "success",
            "data" :serializer.data
        }
        return Response(json_data,status=status.HTTP_200_OK)            


class PasswordResetRequestView(APIView):
    permission_classes=[]
    serializer_class = PasswordResetSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            user = User.objects.filter(username=username).first()
            if user:
                token = default_token_generator.make_token(user)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                reset_url = f"http://127.0.0.1:8000/reset-password/{uid}/{token}/"
                send_mail(
                    'Password reset request',
                    f'Click the link to reset your password: {reset_url}',
                    'universityqasyoun@gmail.com',
                    [user.email],
                    fail_silently=False,
                )
                return Response({'detail': 'Password reset email has been sent.'})
            else:
                return Response({'error': 'No user found with this username.'}, status=400)
        return Response(serializer.errors, status=400)

class ResetPasswordView(APIView):
    permission_classes=[]
    serializer_class = PasswordResetSerializerClass
    def post (self,request,uid,token) :

        decoded_uid_bytes = urlsafe_base64_decode(uid)
        decoded_uid = force_str(decoded_uid_bytes)
        serializer = self.serializer_class(data=request.data)
        try :
            user = User.objects.get(id = decoded_uid)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if serializer.is_valid():
            password_one = serializer.validated_data['new_password']
            password_two = serializer.validated_data['verify_password']
            if password_one == password_two:
                user.set_password(password_one)
                user.save()
                print(password_one)
                print(password_two)
                return Response({'success': 'set new password successfully '}, status=status.HTTP_200_OK) 
            else:
                return Response({'error': 'password is not equal for password two'}, status=400)           