def calculate_compound_interest(principal, rate, time, compounds_per_year=1, monthly_addition=0):
    """
    Calculate compound interest with optional monthly additions.
    
    Args:
        principal (float): Initial investment amount
        rate (float): Annual interest rate in decimal (e.g., 0.05 for 5%)
        time (float): Time period in years
        compounds_per_year (int): Number of times interest is compounded per year
        monthly_addition (float): Amount added monthly to the investment
        
    Returns:
        float: Final amount after compound interest
    """
    if monthly_addition == 0:
        # Simple compound interest without additions
        return principal * (1 + rate / compounds_per_year) ** (compounds_per_year * time)
    else:
        # Compound interest with regular additions
        final_amount = principal
        monthly_rate = rate / 12
        total_months = int(time * 12)
        
        for _ in range(total_months):
            final_amount = final_amount * (1 + monthly_rate)
            final_amount += monthly_addition
            
        return final_amount


def main():
    print("==== Compound Interest Calculator ====")
    
    try:
        # Get user inputs
        principal = float(input("Enter principal amount: €"))
        rate = float(input("Enter annual interest rate (%): ")) / 100
        time = float(input("Enter time period (years): "))
        compounds_per_year = int(input("Enter compounds per year (1=annually, 12=monthly, etc): "))
        monthly_addition = float(input("Enter monthly addition (€0 for none): €"))
        
        # Calculate results
        final_amount = calculate_compound_interest(principal, rate, time, compounds_per_year, monthly_addition)
        total_contributions = principal + (monthly_addition * 12 * time)
        earned_interest = final_amount - total_contributions
        
        # Display results with thousands separators for better readability
        print("\n=== Results ===")
        print(f"Principal amount: €{principal:,.2f}")
        print(f"Annual interest rate: {rate*100:.2f}%")
        print(f"Time period: {time} years")
        print(f"Compounding frequency: {compounds_per_year} times per year")
        print(f"Monthly addition: €{monthly_addition:,.2f}")
        print(f"Total contributions: €{total_contributions:,.2f}")
        print(f"Final amount: €{final_amount:,.2f}")
        print(f"Interest earned: €{earned_interest:,.2f}")
        
    except ValueError:
        print("Error: Please enter valid numeric values.")


if __name__ == "__main__":
    main()
