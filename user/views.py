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
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def choice_detail(request, pk):
    try:
        choice = Choice.objects.get(pk=pk)
    except Choice.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ChoiceSerializer(choice)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = ChoiceSerializer(choice, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        choice.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def group_list(request):
    if request.method == 'GET':
        groups = Group.objects.all()
        choices = Choice.objects.values('id','choice_name')


        # data = [{"id":x.id,"group_name":x.group_name,"choice":[ {} for j in x.choices_list]} for x in Group.objects.all()]

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

        # serializer = GroupSerializer(groups, many=True)
        return Response(data)
    elif request.method == 'POST':
        serializer = GroupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def group_detail(request, pk):
    try:
        group = Group.objects.get(pk=pk)
    except Group.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = GroupSerializer(group)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = GroupSerializer(group, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        group.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# @api_view(['GET', 'POST', 'PUT', 'DEL'])
# def groupchoice(request):
#     if request.method == 'GET':
#         groupchoice = GroupChoice.objects.all()
        
#         data = {}
        
#         for group_ob in groupchoice:
#             group_id = group_ob.group_id.id
            
#             if group_id not in data:
#                 data[group_id] = {
#                     'group_id': group_id,
#                     'group_name': group_ob.group_id.group_name,
#                     'choices': []
#                 }
            
#             data[group_id]['choices'].append({
#                 'choice_id': group_ob.choice_id.id,
#                 'choice_name': group_ob.choice_id.name
#             })
        
#         response_data = [{'group': data[group_id]} for group_id in data]
        
#         return JsonResponse(response_data, safe=False)
    
#     elif request.method == 'POST':
#         serializer = GroupChoiceSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#     elif request.method == 'PUT':
#         serializer = GroupChoiceSerializer(groupchoice, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     elif request.method == 'DELETE':
#         groupchoice.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

# @api_view(['GET', 'POST', 'PUT', 'DELETE'])
# def groupchoice(request, group_id):
#     try:
#         group = Group.objects.get(id=group_id)
#     except Group.DoesNotExist:
#         return Response({'message': 'Group not found'}, status=status.HTTP_404_NOT_FOUND)
    
#     if request.method == 'GET':
#         groupchoice = GroupChoice.objects.filter(group_id=group)
#         data = {
#             'id': group_id.id,
#             'group': {
#                 'group_id': group.id,
#                 'group_name': group.group_name,
#                 'choices': [{'choice_id': gc.choice_id.id, 'choice_name': gc.choice_id.name} for gc in groupchoice]
#             }
#         }
#         return Response(data, status=status.HTTP_200_OK)
    
#     elif request.method == 'PUT':
#         serializer = GroupSerializer(instance=group, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     elif request.method == 'DELETE':
#         # Implementation for the DELETE method
#         # Retrieve the data from the request, find the corresponding object, delete it, and return a success message
        
#         return Response({'message': 'DELETE method not implemented'}, status=status.HTTP_501_NOT_IMPLEMENTED)
