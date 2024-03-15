from .models import Student,User,Department,AddressOne,AddressTwo,Empolyee,Buses
from rest_framework import serializers
from rest_framework.authtoken.models import Token 

class LodinSerializer(serializers.Serializer):
    username=serializers.CharField(write_only=True)
    password=serializers.CharField(write_only=True)

class DepatrtmentSerializer (serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ('id' , 'department')
class AddressOneSerializer (serializers.ModelSerializer):
    class Meta:
        model = AddressOne
        fields = ('id' , 'address') 
class AddressTwoSerializer (serializers.ModelSerializer):
    address_one = serializers.SlugRelatedField(many=False ,slug_field="address" ,queryset=AddressOne.objects.all())
    class Meta:
        model = AddressTwo
        fields = ('id' , 'address','address_one')        


class StudentSerializer (serializers.ModelSerializer):
    address1=serializers.SlugRelatedField(many=False, slug_field="address",queryset=AddressOne.objects.all())
    address2=serializers.SlugRelatedField(many=False, slug_field="address",queryset=AddressTwo.objects.all())
    department=serializers.SlugRelatedField(many=False, slug_field="department",queryset=Department.objects.all())
    user=serializers.SlugRelatedField(many=False, slug_field="username",queryset=User.objects.all())
    email=serializers.SerializerMethodField() 
    class Meta:
        model =Student
        fields= ('id','firstname','lastname','year','address1','address2','department','user','email')
    def get_email(self, obj):
        return obj.user.email


class StudentSerializerPost(serializers.ModelSerializer):
    email=serializers.CharField(write_only=True)
    number=serializers.IntegerField(write_only=True)
    password=serializers.CharField(write_only=True)
    password2=serializers.CharField(write_only=True)
    class Meta:
        model =Student
        fields= (
        'firstname',
        'lastname',
        'address1',
        'address2',
        'department',
        'year',
        'email',
        'number',
        'password',
        'password2',
        )
    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if password != password2:
            raise serializers.ValidationError("Password and Confirm Password doesn't match")
        return attrs

    def create(self, validated_data):
        email = validated_data.pop('email')
        number = validated_data.pop('number')
        password = validated_data.pop('password')
        password2 = validated_data.pop('password2')        
        user = User(email=email,username=number, type_user='student')
        user.set_password(password)
        user.save()
        validated_data['user'] = user
        obj = super(StudentSerializerPost, self).create(validated_data)
        return obj

class StudentSerializerPut(serializers.ModelSerializer):
    email=serializers.CharField(write_only=True)
    number=serializers.IntegerField(write_only=True)
    class Meta:
        model =Student
        fields= (
        'firstname',
        'lastname',
        'address1',
        'address2',
        'department',
        'year',
        'email',
        'number',
        )

    def update(self, instance, validated_data):
        email = validated_data.pop('email')
        number = validated_data.pop('number')
        user = User.objects.get(id = self.context["user"])
        user.email=email
        user.username=number
        user.save()
        
        validated_data['user'] = user
        obj = super(StudentSerializerPut, self).update(instance,validated_data)
        return obj        


class EmpolyeeSerializer (serializers.ModelSerializer):
    address1=serializers.SlugRelatedField(many=False, slug_field="address",queryset=AddressOne.objects.all())
    address2=serializers.SlugRelatedField(many=False, slug_field="address",queryset=AddressTwo.objects.all())
    user=serializers.SlugRelatedField(many=False, slug_field="username",queryset=User.objects.all())
    email=serializers.SerializerMethodField() 
    class Meta:
        model =Empolyee
        fields= ('id','firstname','lastname','address1','address2','job','user','email')
    def get_email(self, obj):
        return obj.user.email

class EmpolyeeSerializerPost(serializers.ModelSerializer):
    email=serializers.CharField(write_only=True)
    username=serializers.CharField(write_only=True)
    password=serializers.CharField(write_only=True)
    password2=serializers.CharField(write_only=True)
    class Meta:
        model =Empolyee
        fields= (
        'firstname',
        'lastname',
        'address1',
        'address2',
        'job',
        'email',
        'username',
        'password',
        'password2',
        )
    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if password != password2:
            raise serializers.ValidationError("Password and Confirm Password doesn't match")
        return attrs 

    def create(self, validated_data):
        email = validated_data.pop('email')
        username = validated_data.pop('username')
        password = validated_data.pop('password')
        password2 = validated_data.pop('password2')        
        user = User(email=email,username=username, type_user='employee')
        user.set_password(password)
        user.save()
        validated_data['user'] = user
        obj = super(EmpolyeeSerializerPost, self).create(validated_data)
        return obj    

class EmpolyeeSerializerPut(serializers.ModelSerializer):
    email=serializers.CharField(write_only=True)
    username=serializers.CharField(write_only=True)
    class Meta:
        model =Empolyee
        fields=(
            "username",
            "email",
            "firstname",
            "lastname",
            "address1",
            "address2",
            "job",
        )        
    def update(self, instance, validated_data):
        email = validated_data.pop('email')
        username = validated_data.pop('username')
        user = User.objects.get(id = self.context["user"])
        user.email=email
        user.username=username
        user.save()
        validated_data['user'] = user
        obj = super(EmpolyeeSerializerPut, self).update(instance,validated_data)
        return obj     

class BussesSerializerPost(serializers.ModelSerializer):
    username=serializers.CharField(write_only=True)
    password=serializers.CharField(write_only=True)
    password2=serializers.CharField(write_only=True)
    class Meta:
        model=Buses
        fields=(
            "username",
            "firstname",
            "lastname",
            "number",
            "phone",
            'password',
            'password2',
        )       
    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if password != password2:
            raise serializers.ValidationError("Password and Confirm Password doesn't match")
        return attrs    
    def create(self, validated_data):
        username = validated_data.pop('username')
        password = validated_data.pop('password')
        password2 = validated_data.pop('password2')        
        user = User(username=username, type_user='bus')
        user.set_password(password)
        user.save()
        validated_data['user'] = user
        obj = super(BussesSerializerPost, self).create(validated_data)
        return obj    

class PasswordResetSerializer(serializers.Serializer):
    username = serializers.CharField()

class PasswordResetSerializerClass(serializers.Serializer):
    new_password = serializers.CharField()
    verify_password = serializers.CharField()    