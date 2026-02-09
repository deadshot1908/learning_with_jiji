🚀 Learn with Jiji – Backend Service

Backend implementation for Learn with Jiji, an AI-powered learning companion by VeidaLabs.
This service handles user queries, retrieves relevant learning content, and returns structured responses consumable by any frontend (Web / Mobile).

⚠️ Note: No real AI integration is used. Responses are mocked using stored learning content, as permitted in the assignment.



🛠 Tech Stack

        Backend: Django, Django REST Framework
        
        Database & Auth: Supabase (PostgreSQL + Auth)
        
        Storage: Supabase Storage (PPT & Video files)
        
        Security: Supabase Row Level Security (RLS)
        
        API Testing: Postman


📌 Project Overview

        This backend exposes a single API endpoint that:
        
        Accepts a user learning query
        
        Searches relevant learning content
        
        Returns a structured response containing:
        
        📖 Text explanation
        
        📎 Resource links (PPT / Video)
        
        The frontend consumes this API to display learning responses.



🔗 API Endpoint
      POST /api/ask-jiji
      
        Request Body : {
                          "query": "Explain RAG"
                        }

        Successful Response :
                              {
                                  "query": "Explain RAG",
                                  "answer": "Retrieval-Augmented Generation (RAG) is a technique that combines information retrieval with text generation to produce more accurate and grounded responses.",
                                  "resources": [
                                      {
                                          "title": "RAG Introduction Slides",
                                          "type": "ppt",
                                          "url": "https://kfjagrnacoylbxmvneof.supabase.co/storage/v1/object/public/learning-resources/RAG_INTRO.pptx"
                                      },
                                      {
                                          "title": "RAG Explained Video",
                                          "type": "video",
                                          "url": "https://kfjagrnacoylbxmvneof.supabase.co/storage/v1/object/public/learning-resources/Rag_Introduction.mp4"
                                      }
                                  ]
                              }                           


          Error Response (Missing Query) :
                                        {
                                        "error": "Query is required"
                                      }


🗄 Database Schema (Supabase)

        profiles : Stores user identity linked to Supabase Authentication.
        
            Column	        Description
            id	UUID        (references auth.users.id)
            email	User       email
            created_at	     Timestamp
        
        queries : Stores user learning queries for analytics and future personalization.
        
            Column	        Description
            id	            Primary key
            user_id	        References profiles.id
            query_text	    User query
            created_at	    Timestamp
            
        topics : Stores textual learning content (articles / explanations).
        
            Column	        Description
            id	            Primary key
            name	          Topic name (e.g., RAG)
            content	        Text explanation
            created_at	    Timestamp
            
        resources : Stores learning assets (PPTs / Videos) linked to topics.

            Column	        Description
            id	            Primary key
            topic_id	      References topics.id
            title	          Resource title
            type	          ppt / video
            storage_url	    Supabase Storage public URL
            created_at	    Timestamp


📦 Storage

    Bucket Name: learning-resources
    
    Stores:
    
    📊 PPT files
    
    🎥 Video files
    
    Files are accessed using public URLs stored in the resources table.

🔐 Authentication & Security (RLS)

    Row Level Security (RLS) is enabled on all tables.
    
    1. Public Access
    
        topics → readable by all users
        
        resources → readable by all users
    
     2. User-Restricted Access
    
        profiles → users can access only their own profile
        
        queries → users can insert and read only their own queries
    
    This ensures secure data isolation.


▶️ How to Run Locally

    1. Clone the repository
    
    2. Create a virtual environment
    
    3. Install dependencies
    
        pip install -r requirements.txt
    
    
    4. Create .env file
    
        SUPABASE_URL=https://<your-project-id>.supabase.co
        SUPABASE_ANON_KEY=<your-publishable-api-key>
    
    
    5. Run the server
    
        python manage.py runserver
    
    
    6. Test API using Postman

🧠 Design Decisions

    Text explanations and learning assets are stored separately to avoid duplication.
    
    Supabase Storage is used for scalable file management.
    
    Keyword-based search is used for simplicity and reliability.

🚀 One Improvement With More Time

    If I will be given more time , I would like to add LLM models API so that if there is no response present in the database for any question, it can search taht question in real time.

    
