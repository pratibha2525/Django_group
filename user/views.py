from rest_framework import generics
from .models import Group, Choice
from rest_framework import status
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializer import GroupSerializer, ChoiceSerializer

class GroupListCreateView(generics.ListCreateAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

class GroupRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

class ChoiceListCreateView(generics.ListCreateAPIView):
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer

class ChoiceRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer


@api_view(['GET', 'POST'])
def choice_list(request):
    if request.method == 'GET':
        choices = Choice.objects.all()
        serializer = ChoiceSerializer(choices, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = ChoiceSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({
            'message': 'Choice created successfully.',
            'data': serializer.data
        }, status=status.HTTP_201_CREATED)
    return Response({
        'message': 'Invalid data provided.',
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def choice_detail(request, pk):
    try:
        choice = Choice.objects.get(pk=pk)
    except Choice.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ChoiceSerializer(choice)
        return Response(serializer.data)
    if request.method == 'PUT':
        serializer = ChoiceSerializer(choice, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'Choice updated successfully.',
                'data': serializer.data
            })
        return Response({
            'message': 'Invalid data provided.',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        choice.delete()
        return Response({'message': 'Choice deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def group_list(request):
    if request.method == 'GET':
        groups = Group.objects.all()
        choices = Choice.objects.values('id','choice_name')

        data = []

        for i in groups:
            row_dict = {}
            row_dict['id'] = i.id
            row_dict['group_name'] = i.group_name

            choices_final_list = []
            for j in i.choices_list:
                for k in choices:
                    if k["id"] == j:
                        row_dict['choice_list'] = {"id":j,"choice_name":k["choice_name"]}
                        choices_final_list.append(row_dict['choice_list'])
            row_dict['choice_list'] = choices_final_list
            data.append(row_dict)
        return Response(data)
    elif request.method == 'POST':
        serializer = GroupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'Group created successfully.',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            'message': 'Invalid data provided.',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE','PATCH'])
def group_detail(request, pk):
    try:
        group = Group.objects.get(pk=pk)
    except Group.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        choices = Choice.objects.values('id', 'choice_name')

        choices_final_list = []
        for choice_id in group.choices_list:
            for choice in choices:
                if choice['id'] == choice_id:
                    choices_final_list.append({
                        'id': choice['id'],
                        'choice_name': choice['choice_name']
                    })

        data = {
            'id': group.id,
            'group_name': group.group_name,
            'choice_list': choices_final_list
        }
        return Response(data)
    # elif request.method == 'PUT':
    #     serializer = GroupSerializer(group, data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response({
    #             'message': 'Group updated successfully.',
    #             'data': serializer.data
    #         })
    #     return Response({
    #         'message': 'Invalid data provided.',
    #         'errors': serializer.errors
    #     }, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'PATCH':
        serializer = GroupSerializer(group, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'Group patched successfully.',
                'data': serializer.data
            })
        return Response({
            'message': 'Invalid data provided.',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


    elif request.method == 'DELETE':
        group.delete()
        return Response({'message': 'Group deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)

