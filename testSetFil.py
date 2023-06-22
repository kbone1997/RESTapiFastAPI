from setfit import SetFitModel
from sentence_transformers import InputExample, SentenceTransformer, models

# Download from Hub and run inference
model = SetFitModel.from_pretrained("StatsGary/setfit-ft-sentinent-eval")

line= ["this is a positive line","this is a negative line","this is a neutral line"]
# Run inference
preds = model(line).tolist()

print(preds)
