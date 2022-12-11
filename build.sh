echo "Installing requirements..."
pip install -r requirements.txt

echo "server starting..."
uvicorn app:app