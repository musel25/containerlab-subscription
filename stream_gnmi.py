# # output agent 
# {
#   "matched_intent": "telemetry_interface_statistics",
#   "device_os": "nokia_srl",
#   "recommended_yang_type": "native",
#   "yang_path": "/interface[name=mgmt0]/statistics",
#   "default_gnmi_port": 57400,
#   "default_credentials": {"user": "admin", "pass": "NokiaSrl1!"},
#   "openconfig_fallback": "/interfaces/interface[name=mgmt0]/state/counters"
# }

from pygnmi.client import gNMIclient

# Notice we replaced 'interface_name' with 'yang_path'
def stream_dynamic_telemetry(host, port, username, password, yang_path):
    """
    A truly universal gNMI client. 
    Accepts ANY valid YANG path: OpenConfig, Nokia Native, Cisco Native, etc.
    """
    target = (host, port) 
    
    subscribe_request = {
        "subscription": [
            {
                # The script no longer guesses the path structure. 
                # It just passes exactly what the Agent/RAG provided.
                "path": yang_path,
                "mode": "sample",
                "sample_interval": 2000000000 # 2 seconds
            }
        ],
        "mode": "stream",
        "encoding": "json_ietf" 
    }

    print(f"Connecting to {host}:{port}...")
    print(f"Subscribing to path: {yang_path}\n")
    
    try:
        with gNMIclient(target=target, username=username, password=password, insecure=False, skip_verify=True) as gc:
            
            for telemetry_event in gc.subscribe(subscribe=subscribe_request):
                print(f"[{host}] Data received:")
                print(telemetry_event)
                print("-" * 50) 
                
    except KeyboardInterrupt:
        print(f"\nAgent manually disconnected from {host}.")
    except Exception as e:
        print(f"CRITICAL: Failed to stream telemetry from {host}. Error: {e}")

if __name__ == "__main__":
    
    # Example 1: Agent decides to use a NOKIA NATIVE path
    # RAG lookup complete: OS is SR Linux. Target is mgmt0 statistics.
    nokia_native_path = "/interface[name=mgmt0]/statistics"
    
    stream_dynamic_telemetry(
        host="clab-quickstart-lab-r1", 
        port=57400, 
        username="admin", 
        password="NokiaSrl1!", 
        yang_path=nokia_native_path
    )
    
    # Example 2: Agent decides to use an OPENCONFIG path (if we were targeting Cisco, for example)
    # RAG lookup complete: Fallback to vendor-neutral OpenConfig.
    # openconfig_path = "/interfaces/interface[name=MgmtEth0/RP0/CPU0/0]/state/counters"
    
    # stream_dynamic_telemetry(
    #     host="clab-quickstart-lab-xr1", 
    #     port=57400, 
    #     username="cisco", 
    #     password="cisco_password", 
    #     yang_path=openconfig_path
    # )