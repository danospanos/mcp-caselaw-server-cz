#!/usr/bin/env python3
"""
Verify MCP tools are registered correctly
"""

import asyncio
from server import mcp


async def verify_tools():
    """Verify that the search_ak_vrana tool is properly registered"""
    tools = await mcp.get_tools()
    
    print("Registered MCP Tools:")
    print("=" * 70)
    
    # tools is a dict, not a list
    for tool_name, tool_obj in tools.items():
        print(f"\nTool: {tool_name}")
        if hasattr(tool_obj, 'description'):
            print(f"Description: {tool_obj.description}")
        
        if hasattr(tool_obj, 'fn'):
            import inspect
            sig = inspect.signature(tool_obj.fn)
            print("Parameters:")
            for param_name, param in sig.parameters.items():
                print(f"  - {param_name}: {param.annotation if param.annotation != inspect.Parameter.empty else 'any'}")
    
    print("\n" + "=" * 70)
    
    # Verify search_ak_vrana exists
    if 'search_ak_vrana' in tools:
        print("\n✓ search_ak_vrana tool is registered and ready to use!")
        print("✓ You can search for 'odcizeni' using this tool")
    else:
        print("\n✗ search_ak_vrana tool not found!")
    
    if 'extract_page_content' in tools:
        print("✓ extract_page_content tool is also available")


if __name__ == "__main__":
    asyncio.run(verify_tools())
