from rapidfuzz import fuzz
import json
import os
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class ChatbotAPIView(APIView):
    def load_data(self):
        file_path = os.path.join(settings.BASE_DIR, 'chatbot', 'uvs_data.json')
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def post(self, request):
        user_question = request.data.get('question', '').strip().lower()
        if not user_question:
            return Response({'error': 'Veuillez fournir une question.'}, status=status.HTTP_400_BAD_REQUEST)

        data = self.load_data()

        best_score = 0
        best_answer = None

        for entry in data:
            for question in entry["questions"]:
                score = fuzz.partial_ratio(user_question, question.lower())
                if score > best_score:
                    best_score = score
                    best_answer = entry["answer"]

        if best_score > 70:  # seuil de confiance à ajuster
            return Response({'answer': best_answer})
        else:
            return Response({'answer': "Désolé, je ne connais pas encore la réponse à cette question."})
