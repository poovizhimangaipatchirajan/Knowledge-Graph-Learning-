import base64
from pathlib import Path
import streamlit as st


def get_footer_image_b64(root_dir: Path):
    candidates = [
        root_dir / "frontend" / "assets" / "bg_paddy.png",
        root_dir / "frontend" / "assets" / "bg_paddy.jpg",
        root_dir / "frontend" / "assets" / "bg_paddy.jpeg",
        Path("frontend/assets/bg_paddy.png"),
        Path("assets/bg_paddy.png"),
        Path("bg_paddy.png"),
        Path("bg_paddy.jpg"),
    ]
    target = next((p for p in candidates if p.is_file()), None)
    if target:
        with open(target, "rb") as f:
            b64_data = base64.b64encode(f.read()).decode("utf-8")
        mime = "image/png" if target.suffix.lower() == ".png" else "image/jpeg"
        return f"data:{mime};base64,{b64_data}"
    return None


def display_gif(root_dir: Path, file_path="gif.mp4", width=180, caption=""):
    possible_paths = [
        root_dir / "frontend" / "assets" / file_path,
        root_dir / file_path,
        Path("frontend/assets") / file_path,
        Path("assets") / file_path,
        Path(file_path),
    ]
    target_path = next((p for p in possible_paths if p.is_file()), None)

    if not target_path:
        st.warning(f"File '{file_path}' not found in frontend/assets/.")
        return

    with open(target_path, "rb") as f:
        video_bytes = f.read()
    b64_video = base64.b64encode(video_bytes).decode("utf-8")

    st.markdown(
        f"""
        <style>
        video.gif-mode::-webkit-media-controls {{
            display: none !important;
        }}
        video.gif-mode::-webkit-media-controls-enclosure {{
            display: none !important;
        }}
        video.gif-mode::-webkit-media-controls-panel {{
            display: none !important;
        }}
        </style>
        <div style="text-align: center; padding: 12px 0; user-select: none;">
            <video 
                class="gif-mode"
                width="{width}" 
                autoplay 
                loop 
                muted 
                playsinline 
                disableremoteplayback
                disablepictureinpicture
                tabindex="-1"
                style="
                    border-radius: 12px; 
                    pointer-events: none; 
                    outline: none; 
                    border: none; 
                    box-shadow: none;
                    display: inline-block;
                ">
                <source src="data:video/mp4;base64,{b64_video}" type="video/mp4">
            </video>
            {f'<p style="font-size: 0.82rem; color: #64748b; margin-top: 6px; margin-bottom: 0;">{caption}</p>' if caption else ''}
        </div>
        """,
        unsafe_allow_html=True,
    )