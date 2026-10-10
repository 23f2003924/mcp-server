import hashlib
from fastmcp import FastMCP
from fastmcp.server.dependencies import get_http_headers

# Initialize the MCP server
mcp = FastMCP("IITM Exam MCP Server")

# Your registered exam email (trimmed and lowercased)
NORMALIZED_EMAIL = "23f2003924@ds.study.iitm.ac.in"

@mcp.tool(
    name="solve_challenge",
    description="Exposes the solve_challenge tool required by the exam grader."
)
def solve_challenge() -> str:
    # Fetch all HTTP request headers safely
    headers = get_http_headers(include_all=True)
    
    # Case-insensitive lookup for X-Exam-Challenge
    challenge = ""
    for k, v in headers.items():
        if k.lower() == "x-exam-challenge":
            challenge = v
            break
            
    # Compute SHA-256(${challenge}:${normalizedEmail})
    payload = f"{challenge}:{NORMALIZED_EMAIL}"
    full_hash = hashlib.sha256(payload.encode("utf-8")).hexdigest()
    
    # Return the first 16 lowercase hex characters
    return full_hash[:16]

if __name__ == "__main__":
    # Run over Streamable HTTP transport mounted at /mcp
    mcp.http_app(path="/mcp")
    mcp.run(transport="streamable-http", host="0.0.0.0", port=8000)
