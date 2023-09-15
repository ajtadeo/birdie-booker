from app import app
import os

if __name__ == "__main__":
  app.run(host='0.0.0.0', port=os.environ.get("PORT"))
  # app.run(host="192.168.1.53", port=5000)
