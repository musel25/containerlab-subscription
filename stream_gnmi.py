from pygnmi.client import gNMIclient

def stream_telemetry():
    target = ("clab-quickstart-lab-r1", 57400) 
    
    subscribe_request = {
        "subscription": [
            {
                "path": "/interface[name=mgmt0]/statistics",
                "mode": "sample",
                "sample_interval": 2000000000 # 2 seconds
            }
        ],
        "mode": "stream",
        "encoding": "json_ietf" 
    }

    print("Connecting to SR Linux gNMI interface...")
    print("Listening for streaming telemetry (Press Ctrl+C to stop)...\n")
    
    try:
        with gNMIclient(target=target, username="admin", password="NokiaSrl1!", insecure=False, skip_verify=True) as gc:
            
            for telemetry_event in gc.subscribe(subscribe=subscribe_request):
                # THE FIX: Stop using json.dumps(). 
                # Just print the object directly so pygnmi handles the formatting.
                print(telemetry_event)
                print("-" * 50) 
                
    except KeyboardInterrupt:
        print("\nStopped streaming.")
    except Exception as e:
        print(f"Connection Error: {e}")

if __name__ == "__main__":
    stream_telemetry()
