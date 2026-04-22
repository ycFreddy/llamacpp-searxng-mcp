#!/usr/bin/env python3
import os
import requests
from bs4 import BeautifulSoup
from mcp.server.fastmcp import FastMCP
from starlette.middleware.cors import CORSMiddleware
from mcp.shared.exceptions import McpError
from mcp.types import ErrorData, INTERNAL_ERROR, INVALID_PARAMS
from typing import List, Dict, Literal, Optional
import html2text
from pdfminer.high_level import extract_text
import io 

#SEARXNG_BASE_URL = os.environ.get("SEARXNG_BASE_URL", "http://localhost:8888") # Exécution de serveur.py en local
SEARXNG_BASE_URL = os.environ.get("SEARXNG_BASE_URL", "http://searxng:8080") # Exécution de serveur.py sur docker
USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"

class FastMCPWithCORS(FastMCP):
    def streamable_http_app(self) -> "Starlette":
        app = super().streamable_http_app()
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],            
            allow_methods=["*"],
            allow_headers=["*"],
            expose_headers=["mcp-session-id"],
            allow_credentials=False,
        )
        return app

mcp = FastMCPWithCORS("searxng", stateless_http=True, json_response=True)

@mcp.tool()
def searxng_search(query: str, max_results: int = 30) -> List[Dict[str, str]]:
    if max_results <= 0:
        raise McpError(ErrorData(INVALID_PARAMS, "max_results must be greater than 0."))
    
    if not query.strip():  
        return [{'error': 'No Query Submitted'}]

    search_url = f"{SEARXNG_BASE_URL.rstrip('/')}/search" 
    headers = {
        'User-Agent': USER_AGENT,  
        'Accept': 'text/html,application/xhtml+xml;q=0.9,*/*;q=0.8',
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    data = {
        'q': query,
        'categories': 'general',
        'language': 'auto',
        'safesearch': '0',
        'theme': 'simple'
    }  

    try:
        response = requests.post(search_url, headers=headers, data=data, verify=False, timeout=30)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        results = []
        
        for article in soup.find_all('article', class_='result')[:max_results]:
            url_header = article.find('a', {'class': 'url_header'})  
            h3 = article.find('h3')
            content_p = article.find('p', {'class': 'content'})
            
            if url_header and h3:
                results.append({
                    'title': h3.get_text(strip=True),
                    'url': url_header['href'],
                    'content': content_p.get_text(strip=True) if content_p else "No Description"
                })
        
        return results if results else [{"error": "No results found"}]  
        
    except requests.exceptions.RequestException as e:
        raise McpError(ErrorData(INTERNAL_ERROR, f"Search failed: {str(e)}"))
    except Exception as e:
        raise McpError(ErrorData(INTERNAL_ERROR, f"Unexpected error: {str(e)}"))

if __name__ == "__main__":
    # Utilise uvicorn pour écouter sur 0.0.0.0:8000
    import uvicorn
    app = mcp.streamable_http_app()  # Récupère l'app Starlette
    uvicorn.run(
        app,
        host="0.0.0.0", 
        port=8000,     
        log_level="info"
    )