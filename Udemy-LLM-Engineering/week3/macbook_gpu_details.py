import subprocess
import json

def get_macbook_gpu_info():
    """
    Retrieves detailed GPU information for a MacBook using `system_profiler`.

    Returns:
        A list of dictionaries, where each dictionary represents a GPU.
    """
    try:
        # Use subprocess to run `system_profiler` and capture its JSON output
        result = subprocess.run(
            ['system_profiler', '-json', 'SPDisplaysDataType'],
            capture_output=True,
            text=True,
            check=True
        )
        
        # Parse the JSON output
        data = json.loads(result.stdout)
        
        # Extract the Graphics/Displays section
        graphics_info = data.get('SPDisplaysDataType', [])
        
        # Format the output into a cleaner list of dictionaries
        gpu_details = []
        for gpu_data in graphics_info:
            if 'spdisplays_gpu' in gpu_data:
                for gpu in gpu_data['spdisplays_gpu']:
                    # Use a dictionary to store relevant information
                    details = {
                        "model": gpu.get('spdisplays_model'),
                        "type": gpu.get('spdisplays_gpu_type'),
                        "vram": gpu.get('spdisplays_vram'),
                        "vendor": gpu.get('spdisplays_vendor')
                    }
                    gpu_details.append(details)
            # Handle the case where the information is directly in the top level
            else:
                details = {
                    "model": gpu_data.get('spdisplays_model'),
                    "type": gpu_data.get('spdisplays_gpu_type'),
                    "vram": gpu_data.get('spdisplays_vram'),
                    "vendor": gpu_data.get('spdisplays_vendor')
                }
                gpu_details.append(details)
        
        return gpu_details
        
    except (subprocess.CalledProcessError, json.JSONDecodeError) as e:
        print(f"Error fetching GPU info: {e}")
        return None

if __name__ == "__main__":
    gpus = get_macbook_gpu_info()
    if gpus:
        for i, gpu in enumerate(gpus):
            print(f"GPU {i+1}:")
            for key, value in gpu.items():
                print(f"  {key.title()}: {value}")
