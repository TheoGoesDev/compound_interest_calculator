"""
Compound Interest Calculator

This module calculates compound interest with support for monthly contributions
and different compounding frequencies. It includes comprehensive error handling
and logging capabilities.

Example:
    $ python main.py
    Enter principal amount: €1000
    Enter annual interest rate (%): 5
    Enter time period (years): 10
"""

import logging
from decimal import Decimal
from typing import Optional, Union

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('calculator.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def calculate_compound_interest(
    principal: float,
    rate: float,
    time: float,
    compounds_per_year: int = 1,
    monthly_addition: float = 0
) -> float:
    """Calculate compound interest with optional monthly additions."""
    # Validate inputs
    if any(param < 0 for param in [principal, rate, time, compounds_per_year, monthly_addition]):
        raise ValueError("All parameters must be non-negative")

    try:
        if monthly_addition == 0:
            # Simple compound interest without additions
            final_amount = principal * (1 + rate / compounds_per_year) ** (compounds_per_year * time)
        else:
            # Compound interest with regular additions
            final_amount = principal
            monthly_rate = rate / 12
            total_months = int(time * 12)
            
            for _ in range(total_months):
                final_amount = final_amount * (1 + monthly_rate)
                final_amount += monthly_addition
        
        return round(final_amount, 2)
    
    except Exception as e:
        logger.error(f"Error in calculation: {str(e)}")
        raise

def main() -> None:
    """
    Main function to run the compound interest calculator interactively.
    Handles user input and displays formatted results.
    """
    logger.info("Starting compound interest calculator")
    print("==== Compound Interest Calculator ====")
    
    try:
        # Get user inputs
        principal = float(input("Enter principal amount: €"))
        rate = float(input("Enter annual interest rate (%): ")) / 100
        time = float(input("Enter time period (years): "))
        compounds_input = input("Enter compounds per year (1=annually, 12=monthly, etc) [1]: ")
        compounds_per_year = int(compounds_input) if compounds_input else 1
        monthly_addition = float(input("Enter monthly addition (€0 for none): €"))
        
        # Calculate results
        final_amount = calculate_compound_interest(
            principal, rate, time, compounds_per_year, monthly_addition
        )
        total_contributions = principal + (monthly_addition * 12 * time)
        earned_interest = final_amount - total_contributions
        
        # Display results
        print("\n=== Results ===")
        print(f"Principal amount: €{principal:,.2f}")
        print(f"Annual interest rate: {rate*100:.2f}%")
        print(f"Time period: {time} years")
        print(f"Compounding frequency: {compounds_per_year} times per year")
        print(f"Monthly addition: €{monthly_addition:,.2f}")
        print(f"Total contributions: €{total_contributions:,.2f}")
        print(f"Final amount: €{final_amount:,.2f}")
        print(f"Interest earned: €{earned_interest:,.2f}")
        
        logger.info("Calculation completed successfully")
        
    except ValueError as e:
        logger.error(f"Invalid input: {str(e)}")
        print("Error: Please enter valid numeric values.")
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        print("An unexpected error occurred.")

if __name__ == "__main__":
    main()
