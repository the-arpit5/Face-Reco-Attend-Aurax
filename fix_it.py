from utils.core import train_model
import os

# Folder check
if not os.path.exists("TrainingImageLabel"):
    os.makedirs("TrainingImageLabel")

print("Training shuru ho rahi hai...")
success, msg = train_model()

if success:
    print("✅ Mubarak ho! Trainner.yml wapas aa gayi hai.")
else:
    print(f"❌ Error: {msg}")