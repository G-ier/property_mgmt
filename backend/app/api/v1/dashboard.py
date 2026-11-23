from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, Any
from app.services.cache import get_revenue_summary
from app.services.reservations import REPORT_MONTH, REPORT_YEAR
from app.core.auth import authenticate_request as get_current_user
from app.core.secure_client import SecureClient

router = APIRouter()

@router.get("/properties")
async def get_properties(current_user: dict = Depends(get_current_user)) -> Dict[str, Any]:
    tenant_id = getattr(current_user, "tenant_id", None)
    if not tenant_id:
        raise HTTPException(status_code=403, detail="Tenant context required")
    try:
        properties = await SecureClient.get_properties(tenant_id=tenant_id)
    except Exception as exc:
        raise HTTPException(status_code=503, detail="Unable to load properties") from exc
    return {"items": properties, "total": len(properties)}

@router.get("/dashboard/summary")
async def get_dashboard_summary(
    property_id: str,
    current_user: dict = Depends(get_current_user)
) -> Dict[str, Any]:
    
    tenant_id = getattr(current_user, "tenant_id", "default_tenant") or "default_tenant"
    
    try:
        revenue_data = await get_revenue_summary(property_id, tenant_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    
    total_revenue_float = float(revenue_data['total'])
    
    return {
        "property_id": revenue_data['property_id'],
        "total_revenue": total_revenue_float,
        "currency": revenue_data['currency'],
        "reservations_count": revenue_data['count'],
        "month": REPORT_MONTH,
        "year": REPORT_YEAR,
        "timezone": revenue_data.get('timezone')
    }
