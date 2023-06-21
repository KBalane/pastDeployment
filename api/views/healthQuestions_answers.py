from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import RetrieveUpdateAPIView, CreateAPIView
from rest_framework import viewsets
from django.http import HttpResponse, Http404, JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response

from api.serializers import HealthQuestionSerilizer, HealthQASerializer, UpdateHealthQAAnswerStatus#, BAHealthQASerializer
from digiinsurance.models import HealthQuestions, HealthQuestionsAnswers
from django.db.models import Count
from django.db import connection
from django.shortcuts import get_list_or_404, render


from rest_framework import status, viewsets
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.db import transaction
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view


__all__ = ['BatchUploadFinal', 'ManualValidationHealthQuestionAnswers', 'BatchUpload4','BatchUpload3','BatchUpload2','BatchUploadHealthQA','HealthQuestionsViewSet', 
            'UpdateHealthQuestion', 'InsureeQuestions' ]

@csrf_exempt
@api_view(["POST"])
def BatchUploadFinal(request):
    #data = JSONParser().parse(request)
    serializer = HealthQASerializer(data=request.data, many=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)

@csrf_exempt
def BatchUpload4(self, request):
    HealthQuestionsAnswers.objects.bulk_create([
    HealthQuestionsAnswers(data=request.data)
    ])
    return Response("success")

class ManualValidationHealthQuestionAnswers(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated, )
    lookup_field = 'id'
    queryset = HealthQuestionsAnswers.objects.all()
    serializer_class = UpdateHealthQAAnswerStatus
class BatchUpload3(CreateAPIView):
    
    def post(self, request):
        model = HealthQuestionsAnswers
        answer= request.data.get("answer")
        insureePolicy_id= request.data.get("insureePolicy_id")
        question_id= request.data.get('question_id')
        cursor = connection.cursor()

        with transaction.atomic():
            serializer = HealthQASerializer(data = request.data,many=True)
            if serializer.is_valid():
                HealthQuestionsAnswers.objects.bulk_create([
                HealthQuestionsAnswers(
                    answer=answer,
                    insureePolicy_id=insureePolicy_id,
                    question_id=question_id)
                ])
                for data in request.data:
                    model.save(self)
                
                serializer.save()
                cursor.execute("call BatchUploadHealthQA('"+answer+"','"+insureePolicy_id+"','"+question_id+"')")
                return Response(serializer.data)
                #return Response("sucess")


class BatchUpload2(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self,request, *args, **kwargs):
        """
        data = request.data
        if isinstance(data, list):  # <- is the main logic
            serializer = HealthQASerializer(data=request.data, many=True)
        else:
            serializer = HealthQASerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
        """
        
        # Check if questions is a list
        if isinstance(request.data['question_id'], list):

            questions = request.data('question_id')
        
            models = []
            for question in questions:
                # validate each model with one question at a time
                request.data['question_id'] = question
                serializer = HealthQASerializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                models.append(serializer)
            # Save it only after all questions are valid. 
            # To avoid situations when one question has wrong id 
            # And you already save previous
            saved_models = [model.save() for model in models]
            print("this is running 1")
            result_serializer = HealthQASerializer(saved_models, many=True)
            # Return list of tickets
            return Response(result_serializer.data)
            
        # Save one as usual if only one data entry
        print("this is running 22")
        serializer = HealthQASerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


"""
class testBatchUpload(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request, *args, **kwargs):
        serializer = HealthQASerializer(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()

        return Response(serializer.data)

    
    def post(self, request, *args, **kwargs):
              
        answer= request.data.get("answer")
        insureePolicy_id= request.data.get("insureePolicy_id")
        question_id= request.data.get('question_id')
        
        store_list = [dummy, dummy, dummy]
        
        cursor = connection.cursor()
        for store in store_list:
            cursor.executemany("call BatchUploadHealthQA('"+store_list[0]+"','"+store_list[1]+"','"+store_list[2]+"')")
            #store.save()
            print(store)
        
        return HttpResponse((store_list[1]))
        

        
        answer_list = []
        answer_list.append(request.POST.get("answer"))
        answer= request.POST.get("answer")
        insureePolicy_id= request.POST.get("insureePolicy_id")
        question_id= request.POST.get('question_id')
        cursor = connection.cursor()
        
        i= 0
        for i in range(3):
            cursor.execute("call BatchUploadHealthQA('"+answer+"','"+insureePolicy_id+"','"+question_id+"')")
        
        return HttpResponse(len(answer_list))
    
"""


class BatchUploadHealthQA(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        queryset = HealthQuestionsAnswers.objects.all().values(
            'insureePolicy',
            'question',
            'answer'
        )
        #serializer_class = HealthQASerializer(queryset, many=True)
        return Response(queryset)


    def post(self, request):
        
        post_data = request.data
        number_of_questions = request.data.get('question_id')
        for stuff in number_of_questions:
            return Response(stuff)
        
        #return Response(number_of_questions)
        """
        serializer = HealthQASerializer(data=post_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data) 
        return Response(serializer.errors)
        """

    



class HealthQuestionsViewSet(viewsets.ModelViewSet):
    queryset = HealthQuestions.objects.all()
    serializer_class = HealthQuestionSerilizer

    def get_queryset(self):
        queryset = HealthQuestions.objects.all()
        policy = self.request.query_params.get('policy_id')
        if policy:
            queryset = queryset.filter(policy_id=policy)
        return queryset


class UpdateHealthQuestion(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)

    lookup_field = 'id'
    queryset = HealthQuestions.objects.all()
    serializer_class = HealthQuestionSerilizer

class InsureeQuestions(APIView):

    def get(self, request):
        Questions = HealthQuestions.objects.all().values(
            'id',
            'question',
            'question_type'
        )
        return Response(Questions)
