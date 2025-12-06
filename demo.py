"""
🎓 Student Subscription Waste Detector - Demo Script
=====================================================
Run this script to demo the core functionality without Streamlit.

Usage: python demo.py
"""

import pandas as pd
from datetime import datetime

# ============================================
# SUBSCRIPTION DATABASE (40+ services)
# ============================================
SUBSCRIPTIONS_DB = {
    # Streaming
    'netflix': {'name': 'Netflix', 'category': 'Streaming', 'student_discount': False, 'avg_monthly': 15.49},
    'hulu': {'name': 'Hulu', 'category': 'Streaming', 'student_discount': True, 'avg_monthly': 7.99},
    'disney': {'name': 'Disney+', 'category': 'Streaming', 'student_discount': False, 'avg_monthly': 13.99},
    'hbo': {'name': 'HBO Max', 'category': 'Streaming', 'student_discount': False, 'avg_monthly': 15.99},
    'amazon prime': {'name': 'Amazon Prime', 'category': 'Streaming', 'student_discount': True, 'avg_monthly': 14.99},
    
    # Music
    'spotify': {'name': 'Spotify', 'category': 'Music', 'student_discount': True, 'avg_monthly': 10.99},
    'apple music': {'name': 'Apple Music', 'category': 'Music', 'student_discount': True, 'avg_monthly': 10.99},
    
    # Education
    'chegg': {'name': 'Chegg', 'category': 'Education', 'student_discount': False, 'avg_monthly': 19.95},
    'coursera': {'name': 'Coursera', 'category': 'Education', 'student_discount': False, 'avg_monthly': 59.00},
    
    # Software
    'adobe': {'name': 'Adobe Creative Cloud', 'category': 'Software', 'student_discount': True, 'avg_monthly': 54.99},
    'microsoft 365': {'name': 'Microsoft 365', 'category': 'Software', 'student_discount': True, 'avg_monthly': 9.99},
    'canva': {'name': 'Canva Pro', 'category': 'Software', 'student_discount': True, 'avg_monthly': 12.99},
    
    # Fitness
    'planet fitness': {'name': 'Planet Fitness', 'category': 'Fitness', 'student_discount': False, 'avg_monthly': 24.99},
    'headspace': {'name': 'Headspace', 'category': 'Wellness', 'student_discount': True, 'avg_monthly': 12.99},
    
    # Food
    'doordash': {'name': 'DoorDash DashPass', 'category': 'Food Delivery', 'student_discount': True, 'avg_monthly': 9.99},
    'grubhub': {'name': 'Grubhub+', 'category': 'Food Delivery', 'student_discount': False, 'avg_monthly': 9.99},
}

# Investment returns (verified sources)
INVESTMENT_RETURNS = {
    'Bitcoin': 0.45,        # 45% (Morgan Stanley 10yr avg: 49%)
    'Ethereum': 0.38,       # 38% (conservative)
    'S&P 500': 0.12,        # 12% (Trade That Swing)
    'High-Yield Savings': 0.05  # 5% (Bankrate Dec 2025)
}


def print_header(text):
    """Print a formatted header."""
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60)


def print_subheader(text):
    """Print a formatted subheader."""
    print(f"\n--- {text} ---")


def detect_subscriptions(transactions):
    """Detect subscriptions from transaction list."""
    detected = []
    for txn in transactions:
        desc = txn['description'].lower()
        for keyword, info in SUBSCRIPTIONS_DB.items():
            if keyword in desc:
                detected.append({
                    'date': txn['date'],
                    'description': txn['description'],
                    'amount': abs(txn['amount']),
                    'subscription': info['name'],
                    'category': info['category'],
                    'has_student_discount': info['student_discount'],
                    'avg_monthly': info['avg_monthly']
                })
                break
    return detected


def find_duplicates(detected):
    """Find duplicate subscriptions in same category."""
    categories = {}
    for sub in detected:
        cat = sub['category']
        name = sub['subscription']
        if cat not in categories:
            categories[cat] = set()
        categories[cat].add(name)
    
    duplicates = {cat: list(subs) for cat, subs in categories.items() if len(subs) > 1}
    return duplicates


def calculate_what_if(annual_spending, years=4):
    """Calculate what-if investment scenarios."""
    results = {}
    for investment, rate in INVESTMENT_RETURNS.items():
        future_value = 0
        for _ in range(years):
            future_value = (future_value + annual_spending) * (1 + rate)
        results[investment] = {
            'future_value': future_value,
            'total_invested': annual_spending * years,
            'gain': future_value - (annual_spending * years)
        }
    return results


def calculate_months_until_graduation(grad_year):
    """Calculate months until graduation."""
    today = datetime.now()
    grad_date = datetime(grad_year, 5, 15)  # Assume May graduation
    if grad_date < today:
        return 0
    months = (grad_date.year - today.year) * 12 + (grad_date.month - today.month)
    return max(0, months)


def run_demo():
    """Run the full demo."""
    
    print("\n" + "🎓" * 30)
    print("\n   💸 STUDENT SUBSCRIPTION WASTE DETECTOR - DEMO 💸")
    print("\n" + "🎓" * 30)
    
    # ============================================
    # STEP 1: Sample Transaction Data
    # ============================================
    print_header("STEP 1: Loading Sample Bank Transactions")
    
    sample_transactions = [
        {'date': '2024-01-15', 'description': 'SPOTIFY PREMIUM', 'amount': -10.99},
        {'date': '2024-01-18', 'description': 'NETFLIX.COM', 'amount': -15.49},
        {'date': '2024-01-20', 'description': 'AMAZON PRIME*', 'amount': -14.99},
        {'date': '2024-02-01', 'description': 'CHEGG INC', 'amount': -19.95},
        {'date': '2024-02-05', 'description': 'ADOBE CREATIVE', 'amount': -54.99},
        {'date': '2024-02-10', 'description': 'HULU LLC', 'amount': -7.99},
        {'date': '2024-02-15', 'description': 'SPOTIFY PREMIUM', 'amount': -10.99},
        {'date': '2024-02-18', 'description': 'NETFLIX.COM', 'amount': -15.49},
        {'date': '2024-03-01', 'description': 'PLANET FITNESS', 'amount': -24.99},
        {'date': '2024-03-05', 'description': 'DOORDASH DASHPASS', 'amount': -9.99},
        {'date': '2024-03-15', 'description': 'SPOTIFY PREMIUM', 'amount': -10.99},
        {'date': '2024-03-18', 'description': 'NETFLIX.COM', 'amount': -15.49},
        {'date': '2024-03-20', 'description': 'HEADSPACE', 'amount': -12.99},
        {'date': '2024-04-01', 'description': 'DISNEY PLUS', 'amount': -13.99},
    ]
    
    print(f"\n📄 Loaded {len(sample_transactions)} transactions from sample bank statement\n")
    print("Sample transactions:")
    print("-" * 50)
    for i, txn in enumerate(sample_transactions[:5]):
        print(f"  {txn['date']}  |  {txn['description']:<20}  |  ${abs(txn['amount']):.2f}")
    print(f"  ... and {len(sample_transactions) - 5} more")
    
    # ============================================
    # STEP 2: Detect Subscriptions
    # ============================================
    print_header("STEP 2: Detecting Subscriptions (Pattern Matching)")
    
    detected = detect_subscriptions(sample_transactions)
    unique_subs = {d['subscription'] for d in detected}
    
    print(f"\n🔍 Scanned {len(sample_transactions)} transactions")
    print(f"✅ Found {len(unique_subs)} unique subscriptions:\n")
    
    # Group by subscription
    sub_summary = {}
    for d in detected:
        name = d['subscription']
        if name not in sub_summary:
            sub_summary[name] = {'count': 0, 'total': 0, 'category': d['category'], 'student_discount': d['has_student_discount']}
        sub_summary[name]['count'] += 1
        sub_summary[name]['total'] += d['amount']
    
    print(f"{'Subscription':<25} {'Category':<15} {'Charges':<10} {'Total':<10} {'Student Discount'}")
    print("-" * 80)
    for name, info in sub_summary.items():
        discount = "✅ Yes" if info['student_discount'] else "❌ No"
        print(f"{name:<25} {info['category']:<15} {info['count']:<10} ${info['total']:<9.2f} {discount}")
    
    # ============================================
    # STEP 3: Find Duplicates
    # ============================================
    print_header("STEP 3: Duplicate Detection")
    
    duplicates = find_duplicates(detected)
    
    if duplicates:
        print("\n⚠️  DUPLICATE SERVICES FOUND:\n")
        for category, subs in duplicates.items():
            print(f"  🔄 {category}: {', '.join(subs)}")
            print(f"     → Consider keeping just one to save money!\n")
    else:
        print("\n✅ No duplicate services found!")
    
    # ============================================
    # STEP 4: Student Discount Alerts
    # ============================================
    print_header("STEP 4: Student Discount Alerts")
    
    with_discounts = [name for name, info in sub_summary.items() if info['student_discount']]
    without_discounts = [name for name, info in sub_summary.items() if not info['student_discount']]
    
    print(f"\n🎓 Subscriptions with student discounts available ({len(with_discounts)}):")
    for name in with_discounts:
        print(f"   ✅ {name} - Make sure you're using the student rate!")
    
    print(f"\n❌ Subscriptions without student discounts ({len(without_discounts)}):")
    for name in without_discounts:
        print(f"   • {name}")
    
    # ============================================
    # STEP 5: Expiration Alert
    # ============================================
    print_header("STEP 5: Graduation Expiration Alert")
    
    grad_year = 2026  # Example graduation year
    months_left = calculate_months_until_graduation(grad_year)
    
    print(f"\n📅 Expected Graduation: May {grad_year}")
    print(f"⏰ Months until graduation: ~{months_left} months\n")
    
    if months_left <= 6:
        print("🚨 WARNING: Your student discounts will expire soon!")
        print("   Consider locking in annual plans at student rates now.")
    elif months_left <= 12:
        print("⚠️  HEADS UP: Less than a year until graduation.")
        print("   Start planning for when student discounts expire.")
    else:
        print("✅ You have time, but keep your graduation date in mind!")
    
    # ============================================
    # STEP 6: What-If Calculator
    # ============================================
    print_header("STEP 6: What-If Investment Calculator")
    
    # Calculate annual spending
    monthly_estimate = sum(info['total'] for info in sub_summary.values()) / 3  # ~3 months of data
    annual_spending = monthly_estimate * 12
    
    print(f"\n💰 Estimated Monthly Subscription Spending: ${monthly_estimate:.2f}")
    print(f"💰 Estimated Annual Subscription Spending: ${annual_spending:.2f}")
    
    print(f"\n📈 If you invested this money instead over 4 years:\n")
    
    results = calculate_what_if(annual_spending, years=4)
    
    print(f"{'Investment':<20} {'Total Invested':<18} {'Future Value':<18} {'Gain':<15}")
    print("-" * 75)
    for investment, data in results.items():
        gain_pct = (data['gain'] / data['total_invested']) * 100
        print(f"{investment:<20} ${data['total_invested']:<16,.2f} ${data['future_value']:<16,.2f} ${data['gain']:<10,.2f} (+{gain_pct:.0f}%)")
    
    # ============================================
    # STEP 7: Summary
    # ============================================
    print_header("SUMMARY: Your Subscription Health Report")
    
    print(f"""
    📊 QUICK STATS
    ─────────────────────────────
    • Subscriptions detected: {len(unique_subs)}
    • Monthly spending: ${monthly_estimate:.2f}
    • Annual spending: ${annual_spending:.2f}
    • Student discounts available: {len(with_discounts)}
    • Duplicate categories: {len(duplicates)}
    
    💡 RECOMMENDATIONS
    ─────────────────────────────""")
    
    if duplicates:
        print(f"    1. Cancel duplicate streaming services - save ~$15/month")
    if with_discounts:
        print(f"    2. Verify you're using student pricing on: {', '.join(with_discounts[:3])}")
    if months_left <= 12:
        print(f"    3. Lock in annual plans before graduation ({months_left} months away)")
    
    best_investment = max(results.items(), key=lambda x: x[1]['gain'])
    print(f"    4. If invested in {best_investment[0]}, your ${annual_spending*4:,.0f} could become ${best_investment[1]['future_value']:,.0f}!")
    
    print("\n" + "=" * 60)
    print("  🎓 Stop the leak. Start the growth. 💰")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    run_demo()
