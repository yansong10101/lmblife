from rest_framework import serializers
from core.models import Customer, University, OrgAdmin, CustomerUPG, FeatureGroup, Feature, Permission, PermissionGroup


# University Model serializer
class UniversityListSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='api:university-retrieve')

    class Meta:
        model = University
        fields = ('url', 'university_name', 'university_code', )


class UniversityRetrieveSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = University
        fields = ('pk', 'university_name', 'university_code', )


# Org Admin serializer
class OrgAdminListSerializer(serializers.HyperlinkedModelSerializer):
    university = UniversityRetrieveSerializer(read_only=True)

    class Meta:
        model = OrgAdmin
        fields = ('university', 'username', 'email', 'last_modified_date', 'last_login_date', )


class OrgAdminRetrieveSerializer(serializers.HyperlinkedModelSerializer):
    university = UniversityRetrieveSerializer(read_only=True)

    class Meta:
        model = OrgAdmin
        fields = ('university', 'username', 'email', 'last_modified_date', 'last_login_date', )


# Customer Model serializer
class CustomerListSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='api:customer-retrieve')

    class Meta:
        model = Customer
        fields = ('url', 'email', 'first_name', 'last_name', 'created_date', 'last_modified_date', )


class CustomerRetrieveSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Customer
        fields = ('pk', 'email', 'first_name', 'last_name', 'created_date', 'last_modified_date', )


# Permission serializers
class PermissionListSerializer(serializers.HyperlinkedModelSerializer):
    detail_url = serializers.HyperlinkedIdentityField(view_name='api:permission-retrieve', read_only=True)
    feature = serializers.HyperlinkedRelatedField(view_name='api:feature-retrieve', read_only=True)

    class Meta:
        model = Permission
        fields = ('pk', 'detail_url', 'feature', 'permission_name', 'permission_type', 'is_active', )


class PermissionRetrieveSerializer(serializers.HyperlinkedModelSerializer):
    feature = serializers.HyperlinkedRelatedField(view_name='api:feature-retrieve', read_only=True)

    class Meta:
        model = Permission
        fields = ('pk', 'feature', 'permission_name', 'permission_type', 'is_active', )



# Permission Group serializers
class PermissionGroupListSerializer(serializers.HyperlinkedModelSerializer):
    detail_url = serializers.HyperlinkedIdentityField(view_name='api:permission-group-retrieve', read_only=True)
    permission = PermissionRetrieveSerializer(many=True, read_only=True)

    class Meta:
        model = PermissionGroup
        fields = ('pk', 'detail_url', 'group_name', 'permission', 'is_org_admin', 'is_super_user', 'is_active',
                  'user_level', )


class PermissionGroupRetrieveSerializer(serializers.HyperlinkedModelSerializer):
    permission = PermissionRetrieveSerializer(many=True, read_only=True)

    class Meta:
        model = PermissionGroup
        fields = ('pk', 'group_name', 'permission', 'is_org_admin', 'is_super_user', 'is_active', 'user_level', )



# Customer University Permission Group serializer
class CustomerUPGListSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='api:customer-upg-retrieve')
    customer = CustomerRetrieveSerializer(read_only=True)
    university = UniversityRetrieveSerializer(read_only=True)
    permission_group = PermissionGroupRetrieveSerializer(read_only=True)

    class Meta:
        model = CustomerUPG
        fields = ('pk', 'url', 'customer', 'university', 'permission_group', 'grant_level', )


class CustomerUPGRetrieveSerializer(serializers.HyperlinkedModelSerializer):
    customer = CustomerRetrieveSerializer(read_only=True)
    university = UniversityRetrieveSerializer(read_only=True)
    permission_group = PermissionGroupRetrieveSerializer(read_only=True)

    class Meta:
        model = CustomerUPG
        fields = ('pk', 'customer', 'university', 'permission_group', 'grant_level', )


# Feature Group Model serializers
class FeatureGroupListSerializer(serializers.HyperlinkedModelSerializer):
    detail_url = serializers.HyperlinkedIdentityField(view_name='api:feature-group-retrieve')

    class Meta:
        model = FeatureGroup
        fields = ('pk', 'detail_url', 'feature_name', )


class FeatureGroupRetrieveSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = FeatureGroup
        fields = ('pk', 'feature_name', )


# Feature Model serializers
class FeatureListSerializer(serializers.HyperlinkedModelSerializer):
    detail_url = serializers.HyperlinkedIdentityField(view_name='api:feature-retrieve')
    feature_group = serializers.HyperlinkedRelatedField(view_name='api:feature-group-retrieve', read_only=True)

    class Meta:
        model = Feature
        fields = ('pk', 'detail_url', 'feature_group', 'feature_name', )


class FeatureRetrieveSerializer(serializers.HyperlinkedModelSerializer):
    feature_group = serializers.HyperlinkedRelatedField(view_name='api:feature-group-retrieve', read_only=True)

    class Meta:
        model = Feature
        fields = ('pk', 'feature_group', 'feature_name', )
