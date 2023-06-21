from rest_framework import serializers

from cocolife.models.Product import *

__all__ = ['CreateProductSerializer', 'ProductSerializer', 'PackageSerializer',
           'BenefitSerializer', 'PremiumSerializer', 'ProductProposalSerializer']


class PremiumSerializer(serializers.ModelSerializer):
    coverage_term = serializers.CharField()
    value = serializers.IntegerField()

    class Meta:
        model = Premium
        fields = '__all__'


class BenefitSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    face_amount = serializers.CharField()

    class Meta:
        model = Benefit
        fields = '__all__'


class VariantSerializer(serializers.ModelSerializer):
    premiums = PremiumSerializer(many=True)
    benefits = BenefitSerializer(many=True)

    class Meta:
        model = Variant
        fields = ['id', 'benefits', 'premiums']


class PackageSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    variants = VariantSerializer(many=True)

    class Meta:
        model = Package
        fields = ['id', 'name', 'description', 'variants']


class CreateProductSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    coverage_amount_range = serializers.ReadOnlyField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'image', 'pdf', 'category', 'description', 'coverage_amount_range']


class ProductProposalSerializer(serializers.Serializer):
    package = serializers.IntegerField()
    variant = serializers.IntegerField()
    payment_term = serializers.CharField()
    coverage_term = serializers.IntegerField()
    age = serializers.IntegerField()

    def validate(self, data):
        package = Package.objects.filter(id=data['package'])
        variant = Variant.objects.filter(id=data['variant'])

        if not package.exists():
            raise serializers.ValidationError('Package does not Exist.')
        if not variant.exists():
            raise serializers.ValidationError('Variant does not Exist.')

        if data['payment_term'] not in ['annual', 'semi annual', 'quarterly', 'monthly']:
            raise serializers.ValidationError('Invalid value for Payment Term')
        return data


class ProductSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    packages = PackageSerializer(many=True)
    coverage_amount_range = serializers.ReadOnlyField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'image', 'pdf', 'category', 'description', 'coverage_amount_range', 'packages']

    def create(self, validated_data):
        # remove packages from product
        packages = validated_data.pop('packages')

        # create and validate product.
        product = Product.objects.create(**validated_data)

        for package in packages:
            # remove variants from package before insertion.
            variants = package.pop('variants')
            # create packages.
            package = Package.objects.create(**package, product=product)

            arr = []
            for variant in variants:
                # create variant.
                var = Variant.objects.create(package=package)

                # remove benef and prems from variant.
                benefits = variant.pop('benefits')
                premiums = variant.pop('premiums')

                # validate andcreate benefs and prems.
                for item in benefits:
                    benefit = Benefit.objects.create(**item, variant=var)
                    arr.append(int(benefit.face_amount))
                for item in premiums:
                    Premium.objects.create(**item, variant=var)
        sorted_val = sorted(arr)

        # compute min and max value for coverage amount from sorted face_amount vals
        if product.coverage_amount_min is None and len(sorted_val) > 0:
            product.coverage_amount_min = sorted_val[-2]
            product.coverage_amount_max = sorted_val[-1]
            product.save()
        return product
