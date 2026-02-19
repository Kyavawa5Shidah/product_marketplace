from rest_framework import serializers
from .models import User, Role, Business
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.core.mail import send_mail
import random
import string


def generate_password(length=12):
    """Generate a random secure password."""
    chars = string.ascii_letters + string.digits + "!@#$%^&*()"
    return ''.join(random.choice(chars) for _ in range(length))


class BusinessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Business
        fields = '__all__'


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = [
            'id',
            'name',
            'can_create_product',
            'can_edit_product',
            'can_delete_product',
            'can_approve_product'
        ]

class UserSerializer(serializers.ModelSerializer):
    role = serializers.SerializerMethodField()
    password = serializers.CharField(write_only=True, required=True)  # admin can type password
    generated_password = serializers.SerializerMethodField()           # returned to admin

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'role', 'generated_password']

    def get_role(self, obj):
        if obj.is_superuser:
            return 'admin'
        elif obj.is_staff:
            return 'editor'
        elif obj.role:
            return obj.role.name
        return 'viewer'

    def get_generated_password(self, obj):
        # Returns the generated password if it exists temporarily on the object
        return getattr(obj, 'generated_password', None)
    def create(self, validated_data):
    request = self.context['request']

    # Password must be provided
    password = validated_data.pop('password')

    # Ensure username is set (required by AbstractUser)
    email = validated_data.get('email')
    if not email:
        raise serializers.ValidationError({"email": "Email is required"})
    username = validated_data.get("username") or email

    # Create the user object
    user = User(username=username, email=email, **validated_data)

    # Assign business only if request.user has one
    if hasattr(request.user, 'business') and request.user.business:
        user.business = request.user.business
    else:
        user.business = None  # optional, or you can raise error if business is required

    # Set password and activate user
    user.set_password(password)
    user.is_active = True

    # Assign role safely
    role_name = request.data.get('role')
    if role_name:
        if user.business:  # only assign role if business exists
            try:
                user.role = Role.objects.get(
                    name__iexact=role_name,
                    business=user.business
                )
            except Role.DoesNotExist:
                # Optional: log that role was not found
                print(f"Role '{role_name}' not found for business '{user.business}'")
                user.role = None
        else:
            user.role = None  # fallback if no business

    # Save user to database
    user.save()

    # Attach generated password temporarily to return to admin
    user.generated_password = password

    # Optional: send email
    try:
        send_mail(
            subject="Your new account password",
            message=f"Hello {user.username},\n\n"
                    f"Your account has been created. You can log in with:\n\n"
                    f"Email: {user.email}\n"
                    f"Password: {password}\n\n"
                    f"Please change your password after logging in.",
            from_email="no-reply@yourdomain.com",
            recipient_list=[user.email],
            fail_silently=False,
        )
    except Exception as e:
        print(f"Failed to send email: {e}")

    return user



class EmailTokenObtainPairSerializer(TokenObtainPairSerializer):
    pass