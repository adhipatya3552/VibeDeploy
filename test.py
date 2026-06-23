# test.py
from utils.state import get_model

model = get_model()
response = model.generate_content("Say: VibeDeploy is connected!")
print(response.text) 