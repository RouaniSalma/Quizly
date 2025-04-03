from django.db import models
from django.contrib.auth.models import User

# Professeur (lié à User)
class TeacherProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Professeur: {self.user.username}"

# Module créé par un enseignant
class Module(models.Model):
    teacher = models.ForeignKey(TeacherProfile, on_delete=models.CASCADE)  # Chaque module appartient à un enseignant
    title = models.CharField(max_length=200)  # Nom du module
    description = models.TextField(blank=True, null=True)  # Description facultative
    created_at = models.DateTimeField(auto_now_add=True)  # Date de création

    def __str__(self):
        return self.title

# Fichiers PDF associés à un module
class PDFFile(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name="pdfs")  # Lien avec un module
    file = models.FileField(upload_to='pdfs/')  # Stocke le fichier PDF
    uploaded_at = models.DateTimeField(auto_now_add=True)  # Date de téléchargement

    def __str__(self):
        return f"PDF: {self.file.name} ({self.module.title})"

# Quiz généré à partir d’un ou plusieurs PDFs
class Quiz(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name="quizzes")  # Un quiz appartient à un module
    title = models.CharField(max_length=200)  # Titre du quiz
    pdfs = models.ManyToManyField(PDFFile, related_name="quizzes")  # Lien ManyToMany avec les PDFs
    created_at = models.DateTimeField(auto_now_add=True)  # Date de création

    def __str__(self):
        return f"Quiz: {self.title} ({self.module.title})"

# Questions du quiz
class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="questions")  # Lien avec un quiz
    text = models.TextField()  # Texte de la question

    def __str__(self):
        return self.text

# Réponses aux questions
class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="answers")  # Lien avec une question
    text = models.CharField(max_length=500)  # Texte de la réponse
    is_correct = models.BooleanField(default=False)  # Indique si la réponse est correcte

    def __str__(self):
        return f"{self.text} ({'Correct' if self.is_correct else 'Incorrect'})"
