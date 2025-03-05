import os
import replicate
import requests
import argparse
from concurrent.futures import ThreadPoolExecutor

def run_model(param_value, param_type, prompt, seed, model_name, base_params):
    """Run the model with the specified parameter value and download the video
    
    Args:
        param_value: The value for the parameter being varied
        param_type: Either 'shift' or 'guide' to indicate which parameter to vary
        prompt: The text prompt for the model
        seed: The random seed for consistent results
        model_name: The name of the model to run
        base_params: Dictionary of base parameters for the model
    """
    param_name = "sample_shift" if param_type == "shift" else "sample_guide_scale"
    
    print(f"Starting {param_name}={param_value}")
    
    try:
        # Create output directory if it doesn't exist
        output_dir = f"{param_type}_comparison"
        os.makedirs(output_dir, exist_ok=True)
        
        # Set up the input parameters
        input_params = base_params.copy()
        input_params["prompt"] = prompt
        input_params["seed"] = seed
        input_params[param_name] = param_value
        
        # Run the model
        output = replicate.run(
            model_name,
            input=input_params
        )
        
        # Get the URL however it comes
        if isinstance(output, list):
            video_url = output[0]
            if hasattr(video_url, 'url'):
                video_url = video_url.url
        else:
            video_url = output
            if hasattr(output, 'url'):
                video_url = output.url
        
        # Download it to the output directory
        filename = os.path.join(output_dir, f"{param_type}{param_value}.mp4")
        response = requests.get(video_url)
        with open(filename, 'wb') as f:
            f.write(response.content)
        
        print(f"Done {param_name}={param_value}, saved to {filename}")
        
    except Exception as e:
        print(f"Error with {param_name}={param_value}: {str(e)}")

def main():
    # Set up command line arguments
    parser = argparse.ArgumentParser(description='Run video generation with varying parameters')
    parser.add_argument('--type', choices=['shift', 'guide'], default='guide',
                        help='Parameter to vary: shift (sample_shift) or guide (sample_guide_scale)')
    parser.add_argument('--prompt', default="A smiling woman walking in London at night",
                        help='Text prompt for the model')
    parser.add_argument('--seed', type=int, default=42,
                        help='Random seed for consistent results')
    parser.add_argument('--model', default="wavespeedai/wan-2.1-t2v-720p",
                        help='Model name to use')
    parser.add_argument('--workers', type=int, default=5,
                        help='Number of concurrent workers')
    args = parser.parse_args()
    
    # Base parameters that stay constant
    base_params = {
        "num_frames": 81,
        "aspect_ratio": "16:9",
        "sample_steps": 30,
        "frames_per_second": 16,
    }
    
    # Set the default for the parameter not being varied
    if args.type == 'shift':
        base_params["sample_guide_scale"] = 7  # Default guide scale when varying shift
        param_range = range(1, 10)  # sample_shift from 1 to 9
        param_type = "shift"
    else:  # args.type == 'guide'
        base_params["sample_shift"] = 5  # Default sample shift when varying guide scale
        param_range = range(0, 11)  # sample_guide_scale from 0 to 10
        param_type = "guide"
    
    # Run all parameter values concurrently
    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        for value in param_range:
            executor.submit(run_model, value, param_type, args.prompt, args.seed, args.model, base_params)
    
    print(f"\nAll done! Videos saved to the '{param_type}_comparison' directory")

if __name__ == "__main__":
    if not os.environ.get("REPLICATE_API_TOKEN"):
        print("Error: REPLICATE_API_TOKEN environment variable not set")
        exit(1)
    
    main()