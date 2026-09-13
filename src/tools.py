"""
🛠️ TOOL DEFINITIONS & EXECUTION BACKEND - VINBUS CUSTOMER SERVICE
Mã nguồn chứa danh sách Tool Schemas (JSON Schema) và Execution Layer phục vụ cho MCP Server VinBus.
Chủ đề 4.2: Trợ lý Dịch vụ Khách hàng VinBus (Tra cứu lộ trình xe bus điện & Đăng ký vé tháng).
"""

import json
from typing import Dict, Any

# ==============================================================================
# 1. KHAI BÁO TOOL SCHEMAS CHUẨN NATIVE JSON SCHEMA (TASK 1.2)
# ==============================================================================

TOOLS_SCHEMA = [
    # Tool 1: Tra cứu lộ trình tuyến xe bus điện VinBus
    {
        "name": "route_query",
        "description": "Tra cứu thông tin chi tiết, lộ trình di chuyển, giá vé lượt, tần suất và giờ hoạt động của tuyến xe bus điện VinBus bằng mã tuyến (ví dụ: 'E01', 'E03').",
        "parameters": {
            "type": "object",
            "properties": {
                "route_id": {
                    "type": "string",
                    "description": "Mã tuyến xe bus điện VinBus cần tra cứu (ví dụ: 'E01', 'E03')"
                }
            },
            "required": ["route_id"]
        }
    },
    
    # --------------------------------------------------------------------------
    # Tool 2: Đăng ký làm thẻ vé tháng xe bus điện VinBus
    # --------------------------------------------------------------------------
    {
        "name": "register_monthly_pass",
        "description": "Đăng ký làm thẻ vé tháng đi xe bus điện VinBus (tuyến đơn hoặc liên tuyến) cho hành khách.",
        "parameters": {
            "type": "object",
            "properties": {
                "customer_name": {
                    "type": "string",
                    "description": "Họ và tên của hành khách đăng ký thẻ (ví dụ: 'Nguyễn Văn An')"
                },
                "phone_number": {
                    "type": "string",
                    "description": "Số điện thoại liên hệ của hành khách (ví dụ: '0912345678')"
                },
                "route_id": {
                    "type": "string",
                    "description": "Mã tuyến đăng ký (ví dụ: 'E01', 'E03') hoặc 'LIEN_TUYEN' nếu đăng ký vé liên tuyến"
                },
                "ticket_type": {
                    "type": "string",
                    "description": "Đối tượng vé: 'Ưu tiên' (Học sinh/Sinh viên - 55.000đ/tháng) hoặc 'Tiêu chuẩn' (100.000đ/tháng/tuyến đơn, 200.000đ/tháng/liên tuyến)"
                }
            },
            "required": ["customer_name", "phone_number", "route_id"]
        }
    }
]

# ==============================================================================
# 2. MÔ PHỎNG CƠ SỞ DỮ LIỆU TUYẾN XE VINBUS & HÀM THỰC THI (EXECUTION LAYER)
# ==============================================================================

MOCK_VINBUS_DATABASE = {
    "E01": {
        "route_name": "Tuyến E01: Bến xe Mỹ Đình - KĐT Vinhomes Ocean Park",
        "operating_hours": "05:00 - 22:30 hàng ngày",
        "frequency": "15 - 20 phút/chuyến",
        "single_ticket_price": "8.000 VNĐ/lượt",
        "monthly_pass_student": "55.000 VNĐ/tháng",
        "monthly_pass_normal": "100.000 VNĐ/tháng",
        "key_stops": "Bến xe Mỹ Đình - Phạm Hùng - Khuất Duy Tiến - Nguyễn Trãi - Ngã Tư Sở - Cầu Vĩnh Tuy - Vinhomes Ocean Park (Gia Lâm)"
    },
    "E03": {
        "route_name": "Tuyến E03: Cầu Giấy - KĐT Vinhomes Smart City",
        "operating_hours": "05:05 - 22:00 hàng ngày",
        "frequency": "15 - 20 phút/chuyến",
        "single_ticket_price": "8.000 VNĐ/lượt",
        "monthly_pass_student": "55.000 VNĐ/tháng",
        "monthly_pass_normal": "100.000 VNĐ/tháng",
        "key_stops": "Điểm trung chuyển Cầu Giấy - Kim Mã - Giảng Võ - Lê Văn Lương - Tố Hữu - KĐT Vinhomes Smart City (Tây Mỗ)"
    }
}


def execute_route_query(route_id: str) -> str:
    """Thực thi tra cứu lộ trình xe bus điện VinBus"""
    route_key = route_id.strip().upper()
    route = MOCK_VINBUS_DATABASE.get(route_key)
    if route:
        return json.dumps({
            "status": "SUCCESS",
            "route_id": route_key,
            "data": route
        }, ensure_ascii=False)
    else:
        return json.dumps({
            "status": "NOT_FOUND",
            "message": f"Không tìm thấy thông tin tuyến xe bus điện '{route_id}'. Hiện VinBus Hà Nội đang khai thác các tuyến chính như E01, E03, E05, v.v."
        }, ensure_ascii=False)


def execute_register_monthly_pass(customer_name: str, phone_number: str, route_id: str, ticket_type: str = "Ưu tiên") -> str:
    """Thực thi đăng ký làm thẻ vé tháng xe bus điện VinBus"""
    ticket_price = "55.000 VNĐ/tháng (Ưu đãi HSSV)" if "ưu tiên" in ticket_type.lower() else "100.000 VNĐ/tháng"
    return json.dumps({
        "status": "SUCCESS",
        "booking_id": f"VB-PASS-{phone_number[-4:]}",
        "customer_name": customer_name,
        "phone_number": phone_number,
        "route_id": route_id.strip().upper(),
        "ticket_type": ticket_type,
        "price": ticket_price,
        "message": f"Đăng ký vé tháng VinBus thành công cho khách hàng {customer_name} ({phone_number}), tuyến {route_id.strip().upper()}, loại vé: {ticket_type} ({ticket_price}). Thẻ điện tử đã kích hoạt trên ứng dụng VinBus."
    }, ensure_ascii=False)


# Router gọi tool thực tế
TOOL_ROUTER = {
    "route_query": execute_route_query,
    "register_monthly_pass": execute_register_monthly_pass,
    # Hỗ trợ alias cũ nếu có
    "academic_query": lambda student_id: execute_route_query("E01"),
    "schedule_appointment": lambda **kw: execute_register_monthly_pass("Khách hàng", "0912345678", "E01")
}

def dispatch_tool_call(tool_name: str, arguments: Dict[str, Any]) -> str:
    """Hàm trung chuyển thực thi tool"""
    if tool_name in TOOL_ROUTER:
        try:
            return TOOL_ROUTER[tool_name](**arguments)
        except Exception as e:
            return json.dumps({"status": "EXECUTION_ERROR", "error": str(e)}, ensure_ascii=False)
    return json.dumps({"status": "UNKNOWN_TOOL", "error": f"Tool '{tool_name}' không tồn tại!"}, ensure_ascii=False)
