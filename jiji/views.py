from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .supabase import supabase


@api_view(["POST"])
def ask_jiji(request):
    query = request.data.get("query")

    if not query or not isinstance(query, str):
        return Response(
            {"error": "Query is required"},
            status=status.HTTP_400_BAD_REQUEST
        )

    # STEP 1: extract keyword (basic & acceptable)
    keyword = query.replace("Explain", "").strip()

    # STEP 2: fetch topic (TEXT ANSWER)
    topic_res = (
        supabase
        .table("topics")
        .select("id, name, content")
        .ilike("name", f"%{keyword}%")
        .execute()
    )

    if not topic_res.data:
        return Response(
            {
                "answer": f"No learning content found for '{keyword}'.",
                "resources": []
            },
            status=status.HTTP_200_OK
        )

    topic = topic_res.data[0]

    # STEP 3: fetch resources linked to topic
    resources_res = (
        supabase
        .table("resources")
        .select("title, type, storage_url")
        .eq("topic_id", topic["id"])
        .execute()
    )

    resources = [
        {
            "title": r["title"],
            "type": r["type"],
            "url": r["storage_url"]
        }
        for r in resources_res.data
    ]

    # STEP 4: SAVE QUERY (non-blocking)
    try:
        user_id = None

        # If auth exists (mocked or real)
        if request.user and request.user.is_authenticated:
            user_id = str(request.user.id)

            supabase.table("queries").insert({
                "user_id": user_id,
                "query_text": query
            }).execute()

    except Exception:
        # We do NOT fail the API if query logging fails
        pass

    # STEP 5: return response
    return Response({
        "query": query,
        "answer": topic["content"],
        "resources": resources
    })
