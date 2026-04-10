import uvicorn

def Server():
    uvicorn.run("main:server", host="127.0.0.1", port=5000, log_level="info")

server = Server()
