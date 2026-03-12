import requests
import json
import time

BASE_URL = "http://localhost:5000/api"

def test_ai_integration():
    print("🚀 Starting AI Integration Test...")

    # 1. Create a Project
    print("\n[1/3] Creating a test project...")
    proj_resp = requests.post(f"{BASE_URL}/projects", json={
        "title": "AI Integration Test Project",
        "description": "Testing if the Gemini AI integration works."
    })
    
    if proj_resp.status_code != 201:
        print(f"❌ Failed to create project: {proj_resp.text}")
        return
        
    project_id = proj_resp.json()["id"]
    print(f"✅ Created project with ID: {project_id}")

    # 2. Add a Paper (This triggers AI)
    print("\n[2/3] Adding a paper (This will trigger the Gemini API)...")
    print("⏳ Waiting for AI response (might take a few seconds)...")
    
    paper_resp = requests.post(f"{BASE_URL}/papers", json={
        "project_id": project_id,
        "title": "Attention Is All You Need",
        "link": "https://arxiv.org/abs/1706.03762"
    })

    if paper_resp.status_code != 201:
        print(f"❌ Failed to create paper: {paper_resp.text}")
        return
        
    paper_data = paper_resp.json()
    print(f"✅ Paper creation successful.")
    
    # 3. Verify AI Fields
    print("\n[3/3] Verifying AI-generated fields...")
    summary = paper_data.get("summary", "")
    keywords = paper_data.get("keywords", "")
    concepts = paper_data.get("concepts", "")
    
    if summary and keywords and concepts:
        print("🎉 AI Integration is working perfectly!")
        print("\n--- AI Results ---")
        print(f"📌 Summary: {summary}")
        print(f"🔑 Keywords: {keywords}")
        print(f"🧠 Concepts: {concepts}")
        print("------------------")
    else:
        print("⚠️  AI fields are empty. Did you set the GEMINI_API_KEY in backend/.env?")

if __name__ == "__main__":
    try:
        requests.get(f"{BASE_URL}/health")
        test_ai_integration()
    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to the backend server.")
        print("Please make sure the Flask server is running (python app.py) on port 5000.")
