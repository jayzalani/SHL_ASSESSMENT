import streamlit as st

import pandas as pd
from app.data_processing import load_and_preprocess_data, create_embeddings
from app.search import search_assessments
from app.gemini import setup_gemini, extract_parameters

def create_streamlit_app():
    """Create the Streamlit web application"""
    st.set_page_config(
        page_title="SHL Assessment Recommendation System", 
        page_icon="📊",
        layout="wide"
    )
    
    # Custom CSS for styling
    st.markdown("""
        <style>
        .main-header {
            font-size: 2.5rem;
            color: #1E3A8A;
            margin-bottom: 1rem;
        }
        .subheader {
            font-size: 1.8rem;
            color: #2563EB;
            margin-top: 2rem;
        }
        .footer {
            position: fixed;
            bottom: 0;
            right: 0;
            left: 0;
            padding: 1rem;
            background-color: #f8f9fa;
            text-align: center;
            font-size: 1rem;
            color: #6B7280;
            border-top: 1px solid #E5E7EB;
        }
        .stButton>button {
            background-color: #2563EB;
            color: white;
            font-weight: bold;
            padding: 0.5rem 2rem;
        }
        .stButton>button:hover {
            background-color: #1E40AF;
        }
        .expander-header {
            font-weight: bold;
            color: #1E3A8A;
        }
        </style>
        """, unsafe_allow_html=True)
    
    # Load the data and models
    if 'data_loaded' not in st.session_state:
        with st.spinner("Loading models and data... Please wait."):
            st.session_state.df = load_and_preprocess_data()
            st.session_state.embedding_model, st.session_state.embeddings_array = create_embeddings(st.session_state.df)
            st.session_state.gemini_model = setup_gemini()
            st.session_state.data_loaded = True
    
    # Header
    st.markdown('<div class="main-header">SHL Assessment Recommendation System</div>', unsafe_allow_html=True)
    st.write("Enter a job description or query to find relevant assessments that match your requirements.")
    
    # Input section
    col1, col2 = st.columns([3, 1])
    
    with col1:
        query = st.text_area("Job Description or Query", height=150, 
                            placeholder="E.g., We need assessments for a senior software developer position requiring problem-solving skills and coding ability...")
    
    with col2:
        st.write("**Filter Options**")
        duration_limit = st.number_input("Maximum Duration (minutes)", 
                                        min_value=0, max_value=120, value=0, step=5,
                                        help="Set to 0 for no limit")
        
        # Additional filter options could be added here
    
    # Center the button
    _, btn_col, _ = st.columns([1, 1, 1])
    with btn_col:
        search_btn = st.button("🔍 Get Recommendations", use_container_width=True)
    
    # Results section
    if search_btn:
        if query:
            with st.spinner("Analyzing job description and finding relevant assessments..."):
                # Extract parameters from the query
                params = extract_parameters(query, st.session_state.gemini_model)
                
                # If user specified a duration, override the extracted value
                if duration_limit > 0:
                    params["duration_limit"] = duration_limit
                
                # Search for relevant assessments
                results, trace_id = search_assessments(
                    query=query,
                    df=st.session_state.df,
                    embedding_model=st.session_state.embedding_model,
                    embeddings_array=st.session_state.embeddings_array,
                    gemini_model=st.session_state.gemini_model,
                    top_k=10,
                    duration_limit=params.get("duration_limit")
                )
                
                # Display results
                st.markdown(f'<div class="subheader">Found {len(results)} relevant assessments</div>', unsafe_allow_html=True)
                st.markdown(f"*Trace ID: {trace_id}*")
                
                # Show summary of filters applied
                if params.get("duration_limit"):
                    st.info(f"🕒 Filter applied: Maximum duration {params.get('duration_limit')} minutes")
                
                # Create grid for results
                for i, (_, row) in enumerate(results.iterrows(), 1):
                    with st.expander(f"**{i}. {row['title']}** - {row['duration']} min | {row['test_type']}"):
                        col1, col2 = st.columns([3, 1])
                        
                        with col1:
                            st.markdown(f"**Description:**\n{row['description']}")
                        
                        with col2:
                            st.markdown("**Details:**")
                            st.markdown(f"🕒 **Duration:** {row['duration']} minutes")
                            st.markdown(f"📊 **Test Type:** {row['test_type']}")
                            st.markdown(f"🌐 **Remote Testing:** {row['remote_support']}")
                            st.markdown(f"⚙️ **Adaptive:** {row['adaptive_support']}")
                            st.markdown(f"[View Assessment Details]({row['url']})", unsafe_allow_html=True)
        else:
            st.warning("⚠️ Please enter a job description or query.")
    
    # Footer
    st.markdown(
        '<div class="footer">MADE WITH ❤️ BY JAY</div>',
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    create_streamlit_app()