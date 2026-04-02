import uuid
from datetime import datetime, timezone
from fastmcp import FastMCP

mcp = FastMCP("IT Helpdesk MCP Server")


@mcp.tool
def create_ticket(
    issue: str,
    user: str = "unknown",
    category: str = "General",
    severity: str = "Medium",
    impacted_system: str = "Unknown",
) -> dict:
    """Create an IT support ticket."""
    ticket_id = f"TCK-{uuid.uuid4().hex[:8].upper()}"
    return {
        "ticket_id": ticket_id,
        "user": user,
        "issue": issue,
        "category": category,
        "severity": severity,
        "impacted_system": impacted_system,
        "status": "Open",
        "priority": severity,
        "assignment_group": "IT Service Desk",
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
    }


@mcp.tool
def lookup_user(username: str) -> dict:
    """Look up a corporate user by username."""
    mock_users = {
        "jdoe": {"username": "jdoe", "name": "John Doe", "department": "Engineering", "email": "jdoe@corp.com", "device_id": "LAPTOP-1001"},
        "asmith": {"username": "asmith", "name": "Alice Smith", "department": "HR", "email": "asmith@corp.com", "device_id": "LAPTOP-1002"},
    }
    user = mock_users.get(username.lower())
    if not user:
        return {"error": f"No user found for username '{username}'."}
    return user


@mcp.tool
def check_device_status(device_id: str) -> dict:
    """Check the status of a company device by device ID."""
    mock_devices = {
        "LAPTOP-1001": {"device_id": "LAPTOP-1001", "status": "Online", "vpn_client": "GlobalProtect 5.2", "last_seen": "2026-04-01T10:00:00Z"},
        "LAPTOP-1002": {"device_id": "LAPTOP-1002", "status": "Offline", "vpn_client": "Cisco AnyConnect 4.10", "last_seen": "2026-03-30T15:30:00Z"},
    }
    device = mock_devices.get(device_id.upper())
    if not device:
        return {"error": f"No device found for device ID '{device_id}'."}
    return device


# To run:
#   python mcp_server.py                          (stdio transport)
# To run:
#   python mcp_server.py                          (STDIO - for Inspector)
#   python mcp_server.py --http                   (HTTP transport on port 8000)
#   fastmcp run mcp_server.py:mcp --transport http --port 8000  (HTTP via CLI)
#   npx @modelcontextprotocol/inspector python mcp_server.py    (MCP Inspector)

if __name__ == "__main__":
    import sys
    if "--http" in sys.argv:
        mcp.run(transport="http", host="0.0.0.0", port=8000)
    else:
        mcp.run()  # STDIO transport (default, works with Inspector)
