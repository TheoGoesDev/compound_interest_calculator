from pathlib import Path

from fastapi import FastAPI, Form
from fastapi.requests import Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from main import calculate_compound_interest

app = FastAPI()
templates = Jinja2Templates(directory=str(Path(__file__).parent / "templates"))

# Tax brackets and rates for the Netherlands (Box 3, 2025 example)
TAX_FREE_AMOUNT = 57_000  # Tax-free threshold
TAX_BRACKETS = [
    (67_000, 0.056),  # First bracket: 5.6% tax rate
    (950_000, 0.138),  # Second bracket: 13.8% tax rate
    (float("inf"), 0.317),  # Third bracket: 31.7% tax rate
]

def calculate_dutch_tax(investment_value: float) -> float:
    """
    Calculate the Dutch wealth tax (Box 3) for a given investment value.

    Args:
        investment_value (float): Total value of the investment.

    Returns:
        float: Total tax amount.
    """
    taxable_amount = max(0, investment_value - TAX_FREE_AMOUNT)
    tax = 0
    for bracket_limit, rate in TAX_BRACKETS:
        if taxable_amount > 0:
            taxable_in_bracket = min(taxable_amount, bracket_limit)
            tax += taxable_in_bracket * rate
            taxable_amount -= taxable_in_bracket
        else:
            break
    return tax

def calculate_simple_wealth_tax(wealth: float) -> tuple[float, float]:
    """
    Calculate wealth tax based on fictional 4% return taxed at 35%.
    Only applies to wealth above €57,000.
    
    Args:
        wealth (float): Total wealth amount
    
    Returns:
        tuple[float, float]: (tax amount, fictional return amount)
    """
    if wealth <= TAX_FREE_AMOUNT:
        return 0.0, 0.0  # No tax and no fictional return below threshold
        
    taxable_wealth = wealth - TAX_FREE_AMOUNT
    fictional_return = taxable_wealth * 0.04  # 4% fictional return on taxable amount
    tax = fictional_return * 0.35  # 35% tax on fictional return
    return tax, fictional_return

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/calculate", response_class=HTMLResponse)
async def calculate(
    request: Request,
    principal: float = Form(...),
    rate: float = Form(...),
    time: float = Form(...),
    compounds_per_year: int = Form(...),
    monthly_addition: float = Form(0),
):
    try:
        # Calculate compound interest
        final_amount = calculate_compound_interest(principal, rate / 100, time, compounds_per_year, monthly_addition)
        total_contributions = principal + (monthly_addition * 12 * time)
        earned_interest = final_amount - total_contributions

        # Calculate tax based on fictional return
        tax, fictional_return = calculate_simple_wealth_tax(final_amount)
        after_tax_amount = final_amount - tax

        # Format numbers for better readability
        context = {
            "request": request,
            "principal": f"{principal:,.2f}",
            "rate": f"{rate:.2f}",
            "time": f"{time:.2f}",
            "compounds_per_year": f"{compounds_per_year:,}",
            "monthly_addition": f"{monthly_addition:,.2f}",
            "total_contributions": f"{total_contributions:,.2f}",
            "final_amount": f"{final_amount:,.2f}",
            "earned_interest": f"{earned_interest:,.2f}",
            "fictional_return": f"{fictional_return:,.2f}",
            "tax": f"{tax:,.2f}",
            "after_tax_amount": f"{after_tax_amount:,.2f}",
        }

        return templates.TemplateResponse("result.html", context)
    except Exception as e:
        return HTMLResponse(content=f"An error occurred: {e}", status_code=500)