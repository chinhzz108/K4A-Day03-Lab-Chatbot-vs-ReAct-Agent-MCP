"""
🔌 MODEL CONTEXT PROTOCOL (MCP) SERVER MODULE - VINBUS CUSTOMER SERVICE
Mô phỏng kiến trúc MCP Server (Client-Server Architecture) cung cấp công cụ chuẩn hóa cho VinBus.
Chủ đề 4.2: Trợ lý Dịch vụ Khách hàng VinBus.
"""

import json
import sys
from typing import Dict, Any, List
from tools import TOOLS_SCHEMA, dispatch_tool_call

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

class MCPVinBusServer:
    """
    Giả lập MCP Server tuân thủ chuẩn giao thức Model Context Protocol cho VinBus
    """
    def __init__(self, server_name: str = "vinbus-customer-mcp-server"):
        self.server_name = server_name
        self.version = "2026.1.0"
        
    def list_tools(self) -> List[Dict[str, Any]]:
        """Trả về danh sách các Tools chuẩn giao thức MCP"""
        return TOOLS_SCHEMA
        
    def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        [TASK 2.1] HỌC VIÊN HOÀN THIỆN HÀM THỰC THI TOOL TRÊN MCP SERVER
        Thực thi request gọi Tool theo chuẩn MCP JSON-RPC
        """
        raw_result = dispatch_tool_call(tool_name, arguments)
        try:
            content = json.loads(raw_result)
        except Exception:
            content = {"status": "ERROR", "message": str(raw_result)}
            
        return {
            "jsonrpc": "2.0",
            "server": self.server_name,
            "tool": tool_name,
            "result": content
        }

# Alias tương thích ngược
MCPAcademicServer = MCPVinBusServer


if __name__ == "__main__":
    print("==========================================================")
    print("🔌 KIỂM THỬ ĐỘC LẬP MCP SERVER (vinbus-customer-mcp-server)")
    print("==========================================================")
    
    server = MCPVinBusServer()
    tools = server.list_tools()
    print(f"✅ Khởi tạo thành công MCP Server: {server.server_name} (Version: {server.version})")
    print(f"📦 Số lượng Tools công bố qua MCP: {len(tools)}")
    
    # Kiểm tra trạng thái TODO 1.2 (Tool Schema)
    reg_tool = next((t for t in tools if t.get("name") == "register_monthly_pass"), None)
    if reg_tool and not reg_tool.get("parameters", {}).get("properties"):
        print("⏳ [TODO 1.2]: Tool 'register_monthly_pass' chưa được định nghĩa properties trong 'src/tools.py'.")
    else:
        print("✅ [TODO 1.2]: Tool 'register_monthly_pass' đã có schema JSON Schema đầy đủ.")

    # Kiểm tra trạng thái TODO 2.1 (call_tool)
    test_result = server.call_tool("route_query", {"route_id": "E01"})
    if not test_result:
        print("⏳ [TODO 2.1]: Hàm call_tool() đang trả về rỗng. Hãy kiểm tra lại!")
    else:
        print(f"✅ [TODO 2.1]: Test dispatch tool 'route_query' (E01) thành công qua JSON-RPC 2.0:")
        print(f"   Phản hồi JSON-RPC: {json.dumps(test_result, ensure_ascii=False)}")
