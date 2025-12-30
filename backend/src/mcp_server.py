from mcp.server.fastmcp import FastMCP
from mcp.server.auth.settings import AuthSettings
from .services.mcp_auth import MCPAuthToken


token_verifier = MCPAuthToken()


mcp = FastMCP(

)


@mcp.tool()
async def get_server_info() -> str:
    """
    Retrieve information about the Hyperion DMX server.
    
    :returns: A confirmation string.
    """
    return "Hyperion DMX MCP server is running and authenticated."

