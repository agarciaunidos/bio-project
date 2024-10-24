import streamlit as st
from PIL import Image
import base64
import boto3
import io
import json
import os

# Constants for SDXL
MODEL_ID = "stability.stable-diffusion-xl-v1"
DEFAULT_SEED = 12345
REGION='us-east-1'

# Negative prompts for better image quality
NEGATIVE_PROMPTS = [
    "bad anatomy", "distorted", "blurry",
    "pixelated", "dull", "unclear",
    "poorly rendered", "poorly Rendered face",
    "poorly drawn face", "poor facial details",
    "poorly drawn hands", "poorly rendered hands",
    "low resolution", "Images cut out at the top, left, right, bottom.",
    "bad composition", "mutated body parts",
    "blurry image", "disfigured",
    "oversaturated", "bad anatomy",
    "deformed body features"
]

@st.cache_data(show_spinner=False)
def generate_future_image(prompt, career_area):
    """Generate an image using SDXL on Bedrock with improved prompt"""
    try:
        # Initialize Bedrock client
        bedrock_runtime = boto3.client('bedrock-runtime', region_name=REGION)
        
        # Enhanced base prompt based on career area
        base_prompts = {
            "Sciences": "professional scientist in lab coat, futuristic laboratory setting",
            "Humanities": "distinguished scholar in modern academic setting",
            "Arts": "creative professional in modern studio space",
            "Technology": "tech innovator in cutting-edge office",
            "Business": "successful entrepreneur in modern office setting"
        }
        
        base_prompt = base_prompts.get(career_area, "professional in modern setting")
        
        # Combine prompts for better results
        enhanced_prompt = f"{prompt}, {base_prompt}, professional photography, 8k UHD, detailed, photorealistic, cinematic lighting"
        
        # Prepare request body
        body = json.dumps({
            "text_prompts": [
                {
                    "text": enhanced_prompt,
                    "weight": 1.0
                }
            ],
            "cfg_scale": 10,
            "seed": DEFAULT_SEED,
            "steps": 50,
            "style_preset": "photographic",
            "negative_prompts": NEGATIVE_PROMPTS
        })
        
        # Make the request
        response = bedrock_runtime.invoke_model(
            body=body,
            modelId=MODEL_ID,
            accept="application/json",
            contentType="application/json"
        )
        
        # Process the response
        response_body = json.loads(response.get("body").read())
        image_bytes = response_body.get("artifacts")[0].get("base64")
        image_data = base64.b64decode(image_bytes.encode())
        
        # Store in session state
        st.session_state['image_data'] = image_data
        
        return Image.open(io.BytesIO(image_data))
        
    except Exception as e:
        st.error(f"Error generating image: {str(e)}")
        return None

def process_biography_for_image(st, biography, career_area,name):
    """Process the biography and generate an image in Streamlit"""
    if biography:
        try:
            # Create image generation prompt from biography
            prompt = f"Professional headshot portrait of {name}, a successful {career_area.lower()} professional in their workplace, modern sophisticated setting, high-end corporate photography, 8k, photorealistic"

            
            with st.spinner('🎨 Creating your future portrait...'):
                image = generate_future_image(prompt, career_area)
                
                if image:
                    st.write("### 🖼️ Your Future Self")
                    st.image(image, caption="A glimpse into your professional future", use_column_width=True)
                    
                    # Add download button
                    img_buffer = io.BytesIO()
                    image.save(img_buffer, format="PNG")
                    st.download_button(
                        label="📥 Download Portrait",
                        data=img_buffer.getvalue(),
                        file_name="future_portrait.png",
                        mime="image/png"
                    )
                else:
                    st.error("❌ Failed to generate image. Please try again.")
                    
        except Exception as e:
            st.error(f"❌ Error processing image: {str(e)}")
    else:
        st.warning("⚠️ Please generate a biography first to create your future portrait.")
