import os
from django.conf import settings

# Our model
from .models import ImageModel

# Our serializer
from .serializers import ImageSerializer

# DRF modules
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response

from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView
from rest_framework.permissions import IsAdminUser

from PIL import Image

# OCR
import pytesseract
from pytesseract import Output

# Response
import json
from upload_app.payment_order_parser import PaymentOrderParser, ScannedWordData


class ImageList(ListAPIView):
    serializer_class = ImageSerializer
    permission_classes = (IsAdminUser,)
    queryset = ImageModel.objects.all()


class ImageDetail(RetrieveAPIView):
    serializer_class = ImageSerializer
    permission_classes = (IsAdminUser,)
    queryset = ImageModel.objects.all()


class ImageCreate(CreateAPIView):
    serializer_class = ImageSerializer

    def post(self, request):
        serializer = ImageSerializer(data=request.data)

        if serializer.is_valid():
            # Save request image in the database
            serializer.save()
            # We need to remove slash from the beginning of the path string
            image_path = serializer.data.get('image')[1:]

            scanned_data = pytesseract.image_to_data(Image.open(image_path), lang='rus+eng', output_type=Output.DICT)
            zipped = zip(scanned_data.get('text'),
                         scanned_data.get('left'),
                         scanned_data.get('top'),
                         scanned_data.get('width'),
                         scanned_data.get('height'))

            scanned_words = []
            for text, left, top, width, height in zipped:
                if not text:
                    continue
                word_data = ScannedWordData(text, left, top, left + width, top + height)
                scanned_words.append(word_data)

            parser = PaymentOrderParser()
            parsed_data = parser.parse(scanned_words)
            dumped_json = json.dumps(parsed_data, indent=4, cls=PaymentOrderParser.ParsedDataEncoder)

            return Response({'data': json.loads(dumped_json)},
                            status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
