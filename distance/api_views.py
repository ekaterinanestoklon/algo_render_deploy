from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import StatsSerializer, WordFreqSerializer
from .algo import text_to_list, get_frequencies, calculate_similarity_score


# IMPORTANT: No changes to TextToList and WordFreq classes are necessary


class TextToList(APIView):

    def post(self, request):
        # Not important to store in the database today
        payload = StatsSerializer(data=request.data)
        if payload.is_valid():
            return Response({"response": text_to_list(payload.data.get("text", ""))}, status=200)
        return Response({"message": payload.error_messages}, status=400)


class WordFreq(APIView):
    def post(self, request):
        # Not important to store in the database today
        incoming_data = WordFreqSerializer(data=request.data)
        if incoming_data.is_valid():
            frequencies_ = get_frequencies(incoming_data.data.get("payload", []))
            if not frequencies_:
                return Response(
                    {"message": "Algorithm not returning correct data structure"},
                    status=418,
                )
            return Response({"response": frequencies_})
        return Response({"message": incoming_data.error_messages}, status=400)
    
class SimilarityView(APIView):
    def post(self, request):
        """
        Calculate similarity between two texts/words
        
        Expected payload:
        {
            "text1": "first text",
            "text2": "second text"
        }
        """
        
        text1 = request.data.get("text1", "")
        text2 = request.data.get("text2", "")
        
        freq1 = get_frequencies(text_to_list(text1))
        freq2 = get_frequencies(text_to_list(text2))
        
        similarity = calculate_similarity_score(freq1, freq2)
        return Response({"similarity": similarity}, status=200)
