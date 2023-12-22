from rest_framework import serializers
from django.contrib.auth import get_user_model


UserModel = get_user_model()


class UserCreateSerializer(serializers.ModelSerializer):
    """
    Sérialiseur pour l'enregistrement d'un utilisateur.
    Ce sérialiseur gère la validation et la création d'un nouvel utilisateur.
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
    Sérialiseur pour l'Utilisateur/Contributeur
    - Informations sélectionnées sur l'utilisateur.
    """

    # Crée l'attribut 'user', qui est write_only car nous avons juste besoin
    # de donner une valeur
    user = serializers.IntegerField(write_only=True)

    class Meta:
        model = UserModel
        fields = ["id", "user"]

    def validate_user(self, value):
        "Extraction du premier utilisateur correspondant à la clé primaire"
        "fournie en tant que paramètre dans la requête"
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
