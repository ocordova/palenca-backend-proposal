import time

def create_timestamp()-> str:
    
    return f"user_{int(time.time() * 1000)}"
