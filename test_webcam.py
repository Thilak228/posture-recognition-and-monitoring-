import ai_posture_monitor as pm

print("=== AI Posture Monitor Test ===")
print("Testing with webcam (press 'q' to quit)")

# Initialize pose estimation
pe = pm.PoseEstimation()

# Test with webcam (video_file=None uses webcam)
try:
    pe.process_video(
        debug_mode=True,
        video_file=None,  # Use webcam
        label_file=None,
        is_predict_pose=True,
        model_number=2,
        use_frame_diff=True,
        use_bounding_box=True,
        scaling_factor=0.8,
        BASE_OUTPUT_DIR="output",
        plot_results=False,  # Set to False to avoid plotting issues
        predict_fall=False
    )
except KeyboardInterrupt:
    print("\nTest interrupted by user")
except Exception as e:
    print(f"Error during testing: {e}")

print("Test completed!")
