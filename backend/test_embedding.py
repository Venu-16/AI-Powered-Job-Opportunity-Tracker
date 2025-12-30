from app.services.embedding_service import EmbeddingService

# Test the embedding service
service = EmbeddingService()

# Sample texts
text1 = "Python developer with FastAPI experience"
text2 = "Looking for Python developer skilled in FastAPI"

# Generate embeddings
emb1 = service.generate_embedding(text1)
emb2 = service.generate_embedding(text2)

# Compute similarity
similarity = service.cosine_similarity(emb1, emb2)

print(f"Text 1: {text1}")
print(f"Text 2: {text2}")
print(f"Cosine Similarity: {similarity}")