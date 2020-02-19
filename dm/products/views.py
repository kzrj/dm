# # -*- coding: utf-8 -*-
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action

from products.serializers import ProductSerializer, CategorySerializer
from products.models import Product, Category
# from piglets.filters import PigletsFilter


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # filter_class = PigletsFilter

#     @action(methods=['post'], detail=False)
#     def create_from_merging_list_and_move_to_ws4(self, request):
#         serializer = piglets_serializers.MergeFromListSerializer(data=request.data)
#         if serializer.is_valid():
#             new_location = locations_models.Location.objects.get(workshop__number=3)
#             merged_piglets = piglets_events_models.PigletsMerger.objects.create_from_merging_list(
#                 merging_list=serializer.validated_data['records'], new_location=new_location,
#                 initiator=request.user)

#             if serializer.validated_data.get('transfer_part_number', None):
#                 merged_piglets.assign_transfer_part_number(serializer.validated_data['transfer_part_number'])

#             to_location = locations_models.Location.objects.get(workshop__number=4)
#             transaction = transactions_models.PigletsTransaction.objects.create_transaction(
#                 to_location=to_location, piglets_group=merged_piglets, initiator=request.user)
#             return Response(
#                 {
#                   "message": 'Партия создана и перемещена в Цех4.',
#                  },
                 
#                 status=status.HTTP_200_OK)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)