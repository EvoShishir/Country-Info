from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.db.models import Q

from base.models import CountryModel
from .serializers import CountrySerializer, UserSignUpSerializer


class SignUpView(APIView):
    def post(self, request):
        serializer = UserSignUpSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "user created successfully", "data": serializer.data},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors)


class CountryListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        countries = CountryModel.objects.all()
        serializer = CountrySerializer(countries, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CountryDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        country = get_object_or_404(CountryModel, pk=pk)
        serializer = CountrySerializer(country)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CreateCountryView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CountrySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateCountryView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        existing_country = get_object_or_404(CountryModel, pk=pk)
        serializer = CountrySerializer(
            existing_country, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteCountryView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        existing_country = get_object_or_404(CountryModel, pk=pk)
        existing_country.delete()
        return Response(
            {"message": f"country '{existing_country.name}' deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )


class RegionalCountryListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        country = get_object_or_404(CountryModel, pk=pk)
        region = country.region
        regional_countries = CountryModel.objects.filter(region=region).exclude(pk=pk)
        serializer = CountrySerializer(regional_countries, many=True)
        return Response(
            {
                "message": f"Regional countries of '{country.name}'",
                "Countries": serializer.data,
            },
            status=status.HTTP_200_OK,
        )


class SameLanguageCountryListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        country = get_object_or_404(CountryModel, pk=pk)
        target_languages = [lang.strip() for lang in country.languages.split(",")]

        query = Q()
        for lang in target_languages:
            query |= Q(languages__icontains=lang)

        same_language_countries = (
            CountryModel.objects.filter(query).exclude(pk=pk).distinct()
        )

        serializer = CountrySerializer(same_language_countries, many=True)
        return Response(
            {
                "message": f"Countries that speak the same language(s) as '{country.name}'",
                "Countries": serializer.data,
            },
            status=status.HTTP_200_OK,
        )


class SearchCountryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        query = request.GET.get("query", "")

        if not query:
            return Response(
                {"error": "Query parameter 'query' is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        countries = CountryModel.objects.filter(name__icontains=query)
        serializer = CountrySerializer(countries, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
