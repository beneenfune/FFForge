from __init__ import app
from watcher import start_watcher

# To start API
if __name__ == "__main__":
    start_watcher()  
    app.run(debug=False, host='0.0.0.0', port=8000)

