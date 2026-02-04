import streamlit as st
import os
import tempfile
import json
# Local Imports
from assets.package.detector import ExactTeamScanner
from assets.package.lang import LangDict

class WebsiteBuilder:
    def __init__(self):
        self.title = "Ina-lyser"
        self.db_path = "assets/players/db.csv"
        self.cover_img_path = "assets/img/cover.jpg"
        self.example_img_path = "assets/img/example.png"

    def create_page(self):
        
        st.set_page_config(page_title=self.title, page_icon="⚡")
        
        # CSS
        st.markdown("""
            <style>
            .stTabs [data-baseweb="tab-highlight"] {
                background-color: #1E90FF;
            }
            
            .stTabs [aria-selected="true"] {
                color: #1E90FF;
            }
            
            .stTabs [data-baseweb="tab"]:hover {
                color: #1E90FF;
            }
            
            div.stButton > button {
                background-color: #1E90FF;
                color: white;
                border: none;
            }
            div.stButton > button:hover {
                background-color: #E5C100;
                color: black;
            }
            </style>
        """, unsafe_allow_html=True)
        
        # GET LANGUAGE FROM URL
        # If the URL is "?lang=fr", this gets "fr". If empty, defaults to "en".
        query_params = st.query_params
        current_lang = query_params.get("lang", "en")

        # DEFINE TOGGLE FUNCTION
        def toggle_language():
            # Check the CURRENT value and flip it
            new_lang = "fr" if current_lang == "en" else "en"
            # Update the URL immediately
            st.query_params["lang"] = new_lang

        # LOAD DICTIONARY WITH URL LANGUAGE
        lang_manager = LangDict(current_lang)
        t = lang_manager.current_dict
        
        # LAYOUT: HEADER & BUTTON
        col1, col2 = st.columns([0.9, 0.1])
        
        with col1:
            st.header(f"⚡⚽ {self.title} ⚽⚡")
        
        with col2:
            # Determine button text
            btn_label = "🇫🇷" if current_lang == "en" else "🇬🇧"
            st.button(btn_label, on_click=toggle_language)
            
        st.markdown("""
            <hr style="
                height: 3px;
                border: none;
                background-color: #fda72c;
                margin-top: 10px; 
                margin-bottom: 20px;
            " />
        """, unsafe_allow_html=True)
        
        # Display cover image if it exists
        if os.path.exists(self.example_img_path):
            st.image(self.cover_img_path, width='stretch')
        else:
            st.warning(t["example_missing"])
            
        st.subheader(t["header"])
        
        # TABS CONFIGURATION
        tab1, tab2 = st.tabs(t["tabs"])
        
        # TAB 1: SCANNER
        with tab1:
            # Check for Database
            if not os.path.exists(self.db_path):
                st.error(t["db_error"])
                return

            # File Uploader
            uploaded_file = st.file_uploader(t["upload_label"], type=["jpg", "png", "jpeg"])

            if uploaded_file is not None:
                # Display the image
                st.image(uploaded_file, caption=t["uploaded_caption"], width='stretch')

                if st.button(t["scan_button"]):
                    log_placeholder = st.empty()
                    log_history = []
                    
                    # Define the callback function
                    def update_logs(message):
                        
                        log_history.append(str(message))
                        # Reverses the list to show newest message first
                        reversed_logs = log_history[::-1]
                        log_content = "".join([f"<div>{line}</div>" for line in reversed_logs])
                    
                        # Render a scrollable DIV
                        log_placeholder.markdown(
                            f"""
                            <div style="
                                height: 100px; 
                                overflow-y: auto;
                                display: flex;                  /* Enable Flexbox */
                                flex-direction: column-reverse; /* Render bottom-to-top */
                                background-color: #000000; 
                                color: #FFFFFF; 
                                padding: 15px;
                                margin: 15px;
                                border-radius: 5px; 
                                border: 1px solid #d6d6d6; 
                                font-family: monospace;
                                font-size: 15px;
                                line-height: 1.5;
                            ">
                                {log_content}
                            </div>
                            """, 
                            unsafe_allow_html=True
                        )
                    # Create a placeholder for the logs
                    with st.spinner(t["spinner"]):
                        try:
                            # Save Streamlit file to Temp Path
                            with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp_file:
                                tmp_file.write(uploaded_file.read())
                                tmp_file_path = tmp_file.name

                            # Run the Scanner
                            # Pass the temp path and the db path
                            scanner = ExactTeamScanner(self.db_path, tmp_file_path)
                            # Connect logs
                            scanner.set_callback(update_logs)
                            
                            team = scanner.scan()
                            
                            # Cleanup temp file immediately
                            os.unlink(tmp_file_path)

                            # Display Results
                            if team[0] != []:
                            
                                export_data=scanner.export_json(team[0], team[1])
                                st.json(export_data)
                                
                                # Download Button
                                json_str = json.dumps(export_data, indent=4, ensure_ascii=False)
                                st.download_button(
                                    label=t["download_label"],
                                    data=json_str,
                                    file_name="team_export.json",
                                    mime="application/json"
                                )
                            else:
                                st.warning(t["no_players"])

                        except Exception as e:
                            st.error(f"An error occurred: {e}")

        # TAB 2: INSTRUCTIONS
        with tab2:
            st.markdown(t["instructions_title"])
            st.markdown(t["step_1"])
            st.markdown(t["step_2"])
            st.markdown(t["step_3"])
            # Display example image if it exists
            if os.path.exists(self.example_img_path):
                st.image(self.example_img_path, caption=t["example_caption"], width='stretch')
            else:
                st.warning(t["example_missing"])
            
            st.markdown(t["step_4"])
            st.markdown(t["step_5"])
            
            st.warning(t["warning"])

            st.info(t["tip"])
