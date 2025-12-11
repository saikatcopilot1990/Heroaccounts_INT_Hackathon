import pandas as pd
from openpyxl import load_workbook, Workbook
import os
from app.models import Claim
from app.config import get_settings

settings = get_settings()

def update_excel_ledger(claim: Claim):
    """
    Appends the approved claim to the Excel ledger.
    """
    # Use the path from settings (or default if removed from config, let's hardcode for now or re-add to config later)
    # I removed excel_ledger_path from config earlier, so I'll define it here or use a default
    file_path = "exports/claims_ledger.xlsm"
    
    # Ensure directory exists
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    # Prepare data
    row_data = {
        "Claim ID": claim.id,
        "Employee": claim.employee.name,
        "Date": claim.date,
        "Amount": claim.amount,
        "Vendor": claim.vendor,
        "Category": claim.category,
        "Purpose": claim.purpose,
        "Status": claim.status.value,
        "Approved By": claim.approvals[-1].approver.name if claim.approvals else "N/A"
    }
    
    # Check if file exists
    if not os.path.exists(file_path):
        # Create new workbook
        df = pd.DataFrame([row_data])
        # Save as xlsm (requires openpyxl engine usually for xlsx, but pandas can handle it)
        # Actually, for xlsm we might need to just use openpyxl directly to be safe if macros are involved
        # But for simple data, xlsx is fine. The user asked for xlsm earlier to bypass blocking.
        # Let's use openpyxl to append.
        wb = Workbook()
        ws = wb.active
        ws.title = "Claims Ledger"
        ws.append(list(row_data.keys()))
        ws.append(list(row_data.values()))
        wb.save(file_path)
    else:
        # Append to existing
        try:
            wb = load_workbook(file_path)
            ws = wb.active
            ws.append(list(row_data.values()))
            wb.save(file_path)
        except Exception as e:
            print(f"Failed to update Excel ledger: {e}")
            return False
            
    return True
