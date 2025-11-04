
import streamlit as st
import pixeltable as pxt
from pixeltable.functions import whisper, scenedetect
import tempfile
import os

st.set_page_config(layout="wide")

st.title("Video to User Guide Generator")

# 1. Video Upload
uploaded_file = st.file_uploader("Choose a video file", type=["mp4", "mov", "avi"])

def generate_guide(video_path):
    """
    Processes a video to generate a user guide with screenshots and transcribed text.
    """
    try:
        # Initialize Pixeltable client
        cl = pxt.Client()

        # Create a Pixeltable table for the video
        # Use a unique table name to avoid conflicts
        table_name = f"video_guide_{os.path.basename(video_path).split('.')[0]}"
        cl.drop_table(table_name, ignore_errors=True)
        video_tbl = cl.create_table(table_name, {"video": pxt.Video})

        # Insert the video into the table
        video_tbl.insert({"video": video_path})

        # 2. Audio Transcription with Whisper
        st.write("Transcribing audio with Whisper...")
        # Use a pre-trained Whisper model for transcription
        video_tbl.add_computed_column(transcript=whisper(video_tbl.video))

        # 3. Scene Detection
        st.write("Detecting scenes...")
        # Use scenedetect to find scene changes
        scenes_tbl = video_tbl.add_computed_column(
            scenes=scenedetect(video_tbl.video)
        )

        # Collect the results
        results = video_tbl.select([video_tbl.transcript, video_tbl.scenes]).collect()
        
        transcript_data = results[0]['transcript']
        scene_data = results[0]['scenes']

        # 4. Aligning Text and Images & 5. Generating the User Guide
        st.write("Generating the user guide...")
        guide_md = ""
        
        # Create a temporary directory for screenshots
        with tempfile.TemporaryDirectory() as temp_dir:
            for i, scene in enumerate(scene_data):
                start_time = scene['start_seconds']
                end_time = scene['end_seconds']

                # Get a representative frame from the middle of the scene
                frame_time = start_time + (end_time - start_time) / 2
                
                # Create a Pixeltable expression to extract the frame
                frame_expr = video_tbl.video.frame_at(frame_time)
                frame_result = video_tbl.select(frame=frame_expr).collect()
                
                if frame_result and 'frame' in frame_result[0] and frame_result[0]['frame']:
                    frame_image = frame_result[0]['frame']
                    screenshot_path = os.path.join(temp_dir, f"scene_{i+1}.png")
                    frame_image.save(screenshot_path)

                    # Find the corresponding text for the scene
                    scene_text = ""
                    if transcript_data and 'segments' in transcript_data:
                        for segment in transcript_data['segments']:
                            segment_start = segment.get('start', 0)
                            segment_end = segment.get('end', 0)
                            if max(start_time, segment_start) < min(end_time, segment_end):
                                scene_text += segment.get('text', '') + " "
                    
                    # Add to the Markdown report
                    guide_md += f"## Scene {i+1}\n\n"
                    guide_md += f"![Scene {i+1}]({screenshot_path})\n\n"
                    guide_md += f"**Text:** {scene_text.strip()}\n\n"
                    guide_md += "---\n\n"

        # Clean up the table
        cl.drop_table(table_name)
        
        return guide_md

    except Exception as e:
        st.error(f"An error occurred: {e}")
        # Clean up in case of error
        if 'cl' in locals() and 'table_name' in locals():
            cl.drop_table(table_name, ignore_errors=True)
        return None

if uploaded_file is not None:
    # Create a temporary file to store the uploaded video
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp_file:
        tmp_file.write(uploaded_file.getvalue())
        video_path = tmp_file.name

    st.video(video_path)

    if st.button("Generate User Guide"):
        with st.spinner("Processing video... This may take a while depending on the video length."):
            markdown_report = generate_guide(video_path)

        if markdown_report:
            st.markdown("## Generated User Guide")
            st.markdown(markdown_report)

            # 6. Display and Export
            st.download_button(
                label="Download User Guide as Markdown",
                data=markdown_report,
                file_name="user_guide.md",
                mime="text/markdown",
            )
    
    # Clean up the temporary video file
    os.unlink(video_path)

else:
    st.info("Please upload a video file to get started.")
