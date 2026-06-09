import os
import sys

# Configure stdout encoding
sys.stdout.reconfigure(encoding='utf-8')

try:
    from mcp.server.fastmcp import FastMCP
except ImportError:
    print("Error: mcp package not installed.", file=sys.stderr)
    sys.exit(1)

mcp = FastMCP("env-secrets")

def _read_env_file():
    paths = [
        r"D:\Google antigravity\.env",
        r"D:\Google antigravity\.env\.env"
    ]
    keys = {}
    for p in paths:
        if os.path.exists(p) and os.path.isfile(p):
            try:
                with open(p, 'r', encoding='utf-8') as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith('#') and '=' in line:
                            k, v = line.split('=', 1)
                            k = k.strip()
                            v = v.strip()
                            if v.startswith('"') and v.endswith('"'):
                                v = v[1:-1]
                            keys[k] = v
            except Exception as e:
                print(f"Warning: Failed to read {p}: {e}", file=sys.stderr)
    return keys

@mcp.tool()
def get_api_key(service_name: str) -> str:
    """Retrieve an API key or configuration value from the central .env file for a given service.
    
    Args:
        service_name: The name of the service (e.g., 'GITHUB', 'DEEPSEEK', 'OPENAI').
                      This is typically the prefix of the API key, or the exact variable name.
    """
    keys = _read_env_file()
    
    # Try exact match
    exact = service_name.upper()
    if exact in keys:
        return keys[exact]
    if f"{exact}_API_KEY" in keys:
        return keys[f"{exact}_API_KEY"]
    if f"{exact}_TOKEN" in keys:
        return keys[f"{exact}_TOKEN"]
        
    # Partial match
    for k, v in keys.items():
        if service_name.upper() in k.upper():
            return v
            
    return f"Error: No API key found matching {service_name}."

@mcp.tool()
def list_available_api_services() -> str:
    """Returns a list of all available services configured in the central .env file without revealing their values."""
    keys = _read_env_file()
    if not keys:
        return "No API keys or services found."
    return "Available Environment Keys:\n" + "\n".join([f"- {k}" for k in keys.keys()])

if __name__ == "__main__":
    mcp.run()
