# SHL Assessment Recommendation System
![SHL](https://img.shields.io/badge/SHL-Assessment%20Recommender-blue)

## Live Demo
 Try it now: https://shlassessment-jayzalani.streamlit.app/

## Overview
The SHL Assessment Recommendation System is an intelligent tool designed to help hiring managers find relevant assessments for their job openings. This system takes natural language queries or job descriptions as input and returns the most appropriate SHL assessments from their product catalog.

## Problem Statement
Hiring managers often struggle to find the right assessments for their recruiting needs. The traditional search process is time-consuming and inefficient, relying on keyword searches and manual filtering. This application solves this problem by providing instant, AI-powered recommendations based on the specific job requirements.

## Architecture
![architecture-diagram](https://github.com/user-attachments/assets/e1bc3012-b0cb-489c-ad94-d3a083668842)

## Recommendation Process Flow
![image](https://github.com/user-attachments/assets/e28e0da5-bb39-42fd-94ab-5066e7037e43)

## Features

### Natural Language Understanding: Input job descriptions or queries in plain English
### Smart Duration Filtering: Set maximum assessment duration as a constraint
### LLM-Powered Analysis: Extracts key skills, levels, and requirements from queries
### Vector Search: Uses embeddings to find semantically similar assessments
### Gemini Reranking: Reorders candidates based on relevance using Google's Gemini API
### Detailed Recommendation Tracing: Logs every step of the recommendation process
### FastAPI Backend: RESTful API for programmatic access
### Streamlit Frontend: User-friendly web interface
### Health Check Endpoint: API status monitoring

## Technical Implementation

### Tech Stack

 __Frontend__: Streamlit 
 
  __Backend__: FastAPI
      
  __Embedding Model__: SentenceTransformers (all-MiniLM-L6-v2)
      
  __LLM__: Google Gemini Pro
      
   __Data Processing__: Pandas, NumPy
      
   __Web Crawling__: BeautifulSoup4, Requests

### API Endpoints

    `GET /health`: Health check endpoint
    
    `POST /recommend`: Recommendation endpoint accepting job descriptions/queries

### Installation and Setup

  Clone the repository and Envirement setup:

    git clone https://github.com/yourusername/shl-assessment-recommender.git
    cd shl-assessment-recommender
    python -m venv .venv
    .venv/SCritps/Activate

  Install dependencies:

    pip install -r requirements.txt

  Set up environment variables:

    Create a .env file with the following content
    GEMINI_API_KEY=your_gemini_api_key

  Run the application:

    Start the API
    python main.py --mode api

### In a separate terminal, start the web interface
    streamlit run streamlit_app.py

## Data Processing
### The system processes SHL's assessment data through several steps:

### __Data Collection__: Web crawler retrieves assessment information from SHL's product catalog
Text Preprocessing: Cleaning and normalizing assessment titles and descriptions
Vector Embedding: Converting text into numerical representations for similarity search
Parameter Extraction: Using Gemini to extract key parameters from user queries
Search & Reranking: Finding initial candidates via vector similarity and reranking with Gemini

## Evaluation Metrics
The recommendation system is evaluated using the following metrics:

Mean Recall@K: Measures how many relevant assessments are retrieved in the top K recommendations
Mean Average Precision@K (MAP@K): Evaluates both relevance and ranking order

## Future Improvements

Implement user feedback collection to improve recommendations over time
Add support for uploading job descriptions as PDF/DOC files
Integrate with SHL's API for real-time assessment data
Develop more advanced filtering capabilities (industry, seniority level, etc.)
Create visualization dashboards for recruitment planning

## Contributor

Jay Zalani


