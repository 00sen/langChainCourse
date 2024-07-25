from langchain_community.tools.tavily_search import TavilySearchResults

def get_profile_url_tavily(search_text: str):
    search = TavilySearchResults()
    res = search.run(f"{search_text}")
    return res[0]["url"]

