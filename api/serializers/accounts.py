from rest_framework import serializers
from django.contrib.auth import get_user_model


UserModel = get_user_model()


class UserCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.
    This serializer handles the validation and creation of a new user.
    """

    class Meta:
        model = UserModel
        fields = ["id", "username", "password", "age",
                  "can_be_contated", "can_data_be_shared"]

    def create(self, validated_data):
        user = UserModel(username=validated_data["username"],
                         age=validated_data["age"],
                         can_be_contacted=validated_data["can_be_contacted"],
                         can_data_be_shared=validated_data["can_data_be_shared"
                                                           ])
        user.set_password(validated_data["password"])
        user.save()
        return user


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ["id", "username", "password"]


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ["id", "username", "password", "age",
                  "can_be_contated", "can_data_be_shared", "date_joined"]


class ContributorSerializer(serializers.ModelSerializer):
    """
    User/Contributor Serializer
    - selected information about the User
    """

    # Create attribute 'user', which is write_only because we just need to
    # give a value
    user = serializers.IntegerField(write_only=True)

    class Meta:
        model = UserModel
        fields = ["id", "user"]

    def validate_user(self, value):
        "Extracting first user corresponding to primary key provided as parameter in the query"
        user = UserModel.objects.filter(pk=value).first()

        if user in None:
            raise serializers.ValidationError("User does not exists!")

        if user.is_superuser:
            raise serializers.ValidationError(
                "Superuser cannot be added as contributors.")

        if self.context["view"].project.contributors.filter(pk=value).exits():
            raise serializers.ValidationError(
                "This user is already a contributor of this project.")
        return user


class ContributorDeatilSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ["id", "username", "age", "can_be_contacted",
                  "can_data_be_shared"]
