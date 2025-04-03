from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import get_object_or_404
from .models import Module, PDFFile
from .serializers import ModuleSerializer, PDFFileSerializer


#Vue pour créer un module
class ModuleViewSet(viewsets.ModelViewSet):
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer

    def create(self, request, *args, **kwargs):
        """Créer un module"""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(teacher=request.user.teacherprofile)  # Associer l’enseignant connecté
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Vue pour ajouter un PDF à un module
class PDFUploadViewSet(viewsets.ViewSet):
    parser_classes = (MultiPartParser, FormParser)

    def create(self, request, module_id=None):
        """Ajouter un PDF à un module"""
        module = get_object_or_404(Module, id=module_id)
        file_serializer = PDFFileSerializer(data=request.data)

        if file_serializer.is_valid():
            file_serializer.save(module=module)
            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#Vue pour supprimer un PDF
class PDFDeleteViewSet(viewsets.ViewSet):
    def destroy(self, request, pk=None):
        """Supprimer un fichier PDF"""
        pdf = get_object_or_404(PDFFile, id=pk)
        pdf.delete()
        return Response({"message": "PDF supprimé"}, status=status.HTTP_204_NO_CONTENT)
