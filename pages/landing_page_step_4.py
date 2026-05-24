import streamlit as st
import time


# -----------------------------
# PAGE CONFIGURATION
# -----------------------------

# Set the browser tab title, icon, and layout style
st.set_page_config(
    page_title="AtomizeAI",
    page_icon="🤖",
    layout="wide"
)

# Header
col1, col2 = st.columns([3, 1], width= 'stretch')

with col1:
    st.header(" ⚛️ AtomizeAI")

with col2:
    st.caption("MVP v1.0", text_alignment= 'right')

st.divider()

# -----------------------------
# SESSION STATE INITIALIZING
# -----------------------------

if "content_path" not in st.session_state:
    st.session_state.content_path = None

if "current_step" not in st.session_state:
    st.session_state.current_step = 4   

if "generated_once" not in st.session_state:
    st.session_state.generated_once = False

if "generate_triggered" not in st.session_state:
    st.session_state.generate_triggered = False
    


#Step 4 Requirements:
# if st.session_state.content_path == "generate" and st.session_state.current_step == 4:


# Define steps
steps = ["Start", "Source/Context", "Preferences", "Generate", "Revise", "Export"]

# Step indicator
step_cols = st.columns(len(steps) * 2 - 1)  # Add space 

    
for i, step in enumerate(steps):
# Current step: filled circle using CSS for styling
    if i == st.session_state.current_step - 1:
        step_cols[i*2].markdown(f"<div style='text-align:center'><span style='font-size:24px; background-color:#000; color:#fff; border-radius:50%; width:32px; height:32px; display:inline-block; line-height:32px'>{i+1}</span><br>{step}</div>", unsafe_allow_html=True)
    else:
        # Other steps: outlined circle
        step_cols[i*2].markdown(f"<div style='text-align:center'><span style='font-size:24px; border:2px solid #ccc; border-radius:50%; width:32px; height:32px; display:inline-block; line-height:32px'>{i+1}</span><br>{step}</div>", unsafe_allow_html=True)
        
    # Add connecting line between steps
    if i < len(steps) -1:
        step_cols[i*2 +1].markdown("<div style='height:2px; background-color:#ccc; margin-top:16px;'></div>", unsafe_allow_html=True)

st.divider()


# Combine Step 2 + Step 3 into PROMPT

prompt = f"""
Step 2 - Context:
Main Topic: {st.session_state.get('main_topic','')}
Content Type / Goal: {st.session_state.get('content_type','')}
Keywords: {st.session_state.get('keywords','')}
Background / Description: {st.session_state.get('background','')}
Target Audience (Context): {st.session_state.get('target_audience','')}
Key Message: {st.session_state.get('key_message','')}
Approximate Word Count: {st.session_state.get('word_count','')}

Step 3 - Preferences:
Platform: {', '.join(st.session_state.get('platform',[]))}
Output Type: {', '.join(st.session_state.get('output_type',[]))}
Target Audience (Preferences): {st.session_state.get('target_audience_preferences','')}
Tone: {st.session_state.get('tone','')}
Length: {st.session_state.get('length','')}
Language: {st.session_state.get('language','')}

"""



# -----------------------------
# Generate Button
# -----------------------------
if st.button("Generate Content", width= 'stretch', disabled = st.session_state.generated_once) and not st.session_state.generated_once:
    st.session_state.generated_once = True  # set flag so it can't be clicked again
    st.session_state.generate_triggered = True  # set flag to indicate generation has been triggered

# Only execute generation if triggered
if st.session_state.generate_triggered:
    st.session_state.generate_triggered = False  # reset trigger for rerun

    st.info("AtomizeAI Analyzing... This may take a moment. Please wait! ⏳")
    
    # Simulate progress
    progress_text = "Generating content..."
    my_bar = st.progress(0, text=progress_text)
    for percent_complete in range(101):
        time.sleep(0.01)  # Replace this with actual API call time
        my_bar.progress(percent_complete, text=progress_text)
    
    # -----------------------------
    # LLM API call placeholder
    # Replace this with actual API call using `prompt`
    # -----------------------------
    generated_content = "This is a placeholder for the AI-generated content based on your inputs. Replace this with the output from your LLM API."

    # Display generated content
    st.subheader("Generated Content :")
    st.text_area("Review the content below.", value=generated_content, height=300)

    st.success("Content generated! ✅")

    if st.button("Revise Content or Generate Image", width='stretch'):
        st.session_state.current_step = 5  # Move to next step
        st.session_state.content_path = "revise"

# Inform user if already generated
elif st.session_state.generated_once:
    st.info("Content has already been generated. You cannot generate again. Just click the button below for revision or image generation.")   
    if st.button("Revise Content or Generate Image", width='stretch'):
        st.session_state.current_step = 5  # Move to next step
        st.session_state.content_path = "revise"

else:    
    col1, col2, col3 = st.columns([1, 10, 1])

    with col1:
        if st.button("← Back"):
            st.session_state.current_step = 3 # Return to Step 3