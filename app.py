import streamlit as st
import pandas as pd
import re
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go

# ============================================
# CONFIGURATION: Known Subscriptions Database
# ============================================

SUBSCRIPTIONS_DB = {
    # Streaming Services
    'netflix': {'name': 'Netflix', 'category': 'Streaming', 'student_discount': False, 'avg_monthly': 15.49},
    'hulu': {'name': 'Hulu', 'category': 'Streaming', 'student_discount': True, 'avg_monthly': 7.99},
    'disney': {'name': 'Disney+', 'category': 'Streaming', 'student_discount': False, 'avg_monthly': 13.99},
    'hbo': {'name': 'HBO Max', 'category': 'Streaming', 'student_discount': False, 'avg_monthly': 15.99},
    'paramount': {'name': 'Paramount+', 'category': 'Streaming', 'student_discount': False, 'avg_monthly': 11.99},
    'peacock': {'name': 'Peacock', 'category': 'Streaming', 'student_discount': False, 'avg_monthly': 5.99},
    'apple tv': {'name': 'Apple TV+', 'category': 'Streaming', 'student_discount': True, 'avg_monthly': 9.99},
    'amazon prime': {'name': 'Amazon Prime', 'category': 'Streaming', 'student_discount': True, 'avg_monthly': 14.99},
    'prime video': {'name': 'Prime Video', 'category': 'Streaming', 'student_discount': True, 'avg_monthly': 8.99},
    
    # Music
    'spotify': {'name': 'Spotify', 'category': 'Music', 'student_discount': True, 'avg_monthly': 10.99},
    'apple music': {'name': 'Apple Music', 'category': 'Music', 'student_discount': True, 'avg_monthly': 10.99},
    'youtube music': {'name': 'YouTube Music', 'category': 'Music', 'student_discount': True, 'avg_monthly': 10.99},
    'tidal': {'name': 'Tidal', 'category': 'Music', 'student_discount': True, 'avg_monthly': 10.99},
    'pandora': {'name': 'Pandora', 'category': 'Music', 'student_discount': False, 'avg_monthly': 9.99},
    
    # Education / Productivity
    'chegg': {'name': 'Chegg', 'category': 'Education', 'student_discount': False, 'avg_monthly': 19.95},
    'coursera': {'name': 'Coursera', 'category': 'Education', 'student_discount': False, 'avg_monthly': 59.00},
    'skillshare': {'name': 'Skillshare', 'category': 'Education', 'student_discount': False, 'avg_monthly': 13.99},
    'linkedin learning': {'name': 'LinkedIn Learning', 'category': 'Education', 'student_discount': False, 'avg_monthly': 29.99},
    'grammarly': {'name': 'Grammarly', 'category': 'Productivity', 'student_discount': True, 'avg_monthly': 12.00},
    'notion': {'name': 'Notion', 'category': 'Productivity', 'student_discount': True, 'avg_monthly': 8.00},
    
    # Software
    'adobe': {'name': 'Adobe Creative Cloud', 'category': 'Software', 'student_discount': True, 'avg_monthly': 54.99},
    'microsoft 365': {'name': 'Microsoft 365', 'category': 'Software', 'student_discount': True, 'avg_monthly': 9.99},
    'canva': {'name': 'Canva Pro', 'category': 'Software', 'student_discount': True, 'avg_monthly': 12.99},
    'github': {'name': 'GitHub Pro', 'category': 'Software', 'student_discount': True, 'avg_monthly': 4.00},
    
    # Fitness & Lifestyle
    'planet fitness': {'name': 'Planet Fitness', 'category': 'Fitness', 'student_discount': False, 'avg_monthly': 24.99},
    'peloton': {'name': 'Peloton', 'category': 'Fitness', 'student_discount': False, 'avg_monthly': 44.00},
    'headspace': {'name': 'Headspace', 'category': 'Wellness', 'student_discount': True, 'avg_monthly': 12.99},
    'calm': {'name': 'Calm', 'category': 'Wellness', 'student_discount': False, 'avg_monthly': 14.99},
    
    # Food & Delivery
    'doordash': {'name': 'DoorDash DashPass', 'category': 'Food Delivery', 'student_discount': True, 'avg_monthly': 9.99},
    'uber eats': {'name': 'Uber Eats Pass', 'category': 'Food Delivery', 'student_discount': False, 'avg_monthly': 9.99},
    'grubhub': {'name': 'Grubhub+', 'category': 'Food Delivery', 'student_discount': False, 'avg_monthly': 9.99},
    
    # Gaming
    'xbox': {'name': 'Xbox Game Pass', 'category': 'Gaming', 'student_discount': False, 'avg_monthly': 16.99},
    'playstation': {'name': 'PlayStation Plus', 'category': 'Gaming', 'student_discount': False, 'avg_monthly': 17.99},
    'nintendo': {'name': 'Nintendo Online', 'category': 'Gaming', 'student_discount': False, 'avg_monthly': 3.99},
    
    # Cloud Storage
    'dropbox': {'name': 'Dropbox', 'category': 'Cloud Storage', 'student_discount': False, 'avg_monthly': 11.99},
    'icloud': {'name': 'iCloud+', 'category': 'Cloud Storage', 'student_discount': False, 'avg_monthly': 2.99},
    'google one': {'name': 'Google One', 'category': 'Cloud Storage', 'student_discount': False, 'avg_monthly': 2.99},
}

# Investment returns (approximate 1-year returns for demo)
INVESTMENT_RETURNS = {
    'Bitcoin': 0.45,      # 45% return
    'Ethereum': 0.38,     # 38% return
    'S&P 500': 0.12,      # 12% return
    'High-Yield Savings': 0.05  # 5% return
}

# ============================================
# HELPER FUNCTIONS
# ============================================

def detect_subscriptions(df, description_col):
    """Detect subscriptions from transaction descriptions."""
    detected = []
    
    for idx, row in df.iterrows():
        desc = str(row[description_col]).lower()
        amount = abs(float(row['amount'])) if 'amount' in df.columns else 0
        date = row.get('date', row.get('Date', row.get('transaction_date', '')))
        
        for keyword, info in SUBSCRIPTIONS_DB.items():
            if keyword in desc:
                detected.append({
                    'date': date,
                    'description': row[description_col],
                    'amount': amount,
                    'subscription': info['name'],
                    'category': info['category'],
                    'has_student_discount': info['student_discount'],
                    'avg_monthly': info['avg_monthly']
                })
                break
    
    return pd.DataFrame(detected)

def calculate_what_if(total_spent, investment_type):
    """Calculate what the money could have been worth if invested."""
    return_rate = INVESTMENT_RETURNS.get(investment_type, 0.10)
    potential_value = total_spent * (1 + return_rate)
    gain = potential_value - total_spent
    return potential_value, gain, return_rate * 100

def find_duplicates(detected_df):
    """Find duplicate subscriptions in the same category."""
    if detected_df.empty:
        return []
    
    category_counts = detected_df.groupby('category')['subscription'].nunique()
    duplicates = category_counts[category_counts > 1].index.tolist()
    return duplicates

def estimate_annual_waste(detected_df):
    """Estimate annual spending on detected subscriptions."""
    if detected_df.empty:
        return 0
    
    # Get unique subscriptions and their average monthly cost
    unique_subs = detected_df.drop_duplicates(subset=['subscription'])
    monthly_total = unique_subs['avg_monthly'].sum()
    return monthly_total * 12

def calculate_months_until_graduation(graduation_year):
    """Calculate months remaining until graduation (assuming May graduation)."""
    today = datetime.now()
    # Assume graduation is in May of the graduation year
    graduation_date = datetime(graduation_year, 5, 15)
    
    if graduation_date < today:
        return 0  # Already graduated
    
    months = (graduation_date.year - today.year) * 12 + (graduation_date.month - today.month)
    return max(0, months)

def get_expiring_discounts(detected_df, months_until_graduation):
    """Get subscriptions with student discounts that will expire soon."""
    if detected_df.empty:
        return [], []
    
    # Get unique subscriptions with student discounts
    student_discount_subs = detected_df[detected_df['has_student_discount']]['subscription'].unique().tolist()
    
    # Categorize by urgency
    if months_until_graduation == 0:
        return student_discount_subs, []  # All expired
    elif months_until_graduation <= 3:
        return student_discount_subs, []  # All expiring very soon
    elif months_until_graduation <= 6:
        return [], student_discount_subs  # All expiring soon
    else:
        return [], []  # Not urgent yet

def calculate_post_graduation_cost(detected_df):
    """Calculate how much more subscriptions will cost after losing student discounts."""
    if detected_df.empty:
        return 0, []
    
    # Student discount savings estimates (typical discount percentages)
    discount_rates = {
        'Spotify': 0.50,           # 50% off
        'Apple Music': 0.50,       # 50% off
        'YouTube Music': 0.50,     # 50% off
        'Amazon Prime': 0.50,      # 50% off (~$7.49 vs $14.99)
        'Hulu': 0.75,              # 75% off (Student bundle)
        'Apple TV+': 0.50,         # Part of student bundle
        'Adobe Creative Cloud': 0.60,  # 60% off
        'Microsoft 365': 1.00,     # Free for students, full price after
        'Canva Pro': 1.00,         # Free for students
        'GitHub Pro': 1.00,        # Free for students
        'Notion': 1.00,            # Free for students
        'Headspace': 0.85,         # 85% off
        'DoorDash DashPass': 0.50, # 50% off
        'Grammarly': 0.50,         # ~50% off
        'Tidal': 0.50,             # 50% off
    }
    
    unique_subs = detected_df[detected_df['has_student_discount']].drop_duplicates(subset=['subscription'])
    
    total_increase = 0
    affected_subs = []
    
    for _, row in unique_subs.iterrows():
        sub_name = row['subscription']
        monthly_cost = row['avg_monthly']
        
        if sub_name in discount_rates:
            discount = discount_rates[sub_name]
            # Current student price, calculate full price
            if discount < 1.0:
                full_price = monthly_cost / (1 - discount)
                increase = (full_price - monthly_cost) * 12  # Annual increase
            else:
                # Currently free, will be full price
                increase = monthly_cost * 12
            
            total_increase += increase
            affected_subs.append({
                'name': sub_name,
                'current': monthly_cost,
                'after': monthly_cost / (1 - discount) if discount < 1.0 else monthly_cost,
                'annual_increase': increase
            })
    
    return total_increase, affected_subs

# ============================================
# STREAMLIT APP
# ============================================

st.set_page_config(
    page_title="Student Subscription Waste Detector",
    page_icon="💸",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #00d4aa;
        text-align: center;
        margin-bottom: 0;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #a0a0a0;
        text-align: center;
        margin-top: 0;
    }
    .metric-card {
        background: #16213e;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
    }
    .alert-box {
        background: #e94560;
        color: white;
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
    }
    .success-box {
        background: #00d4aa;
        color: #1a1a2e;
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<p class="main-header">💸 Student Subscription Waste Detector</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Stop leaking money. Start building wealth.</p>', unsafe_allow_html=True)

st.divider()

# Sidebar
with st.sidebar:
    st.header("⚙️ Settings")
    
    # Dynamic graduation year options
    current_year = datetime.now().year
    grad_years = list(range(current_year, current_year + 5))
    
    graduation_year = st.selectbox(
        "Expected Graduation Year",
        options=grad_years,
        index=1
    )
    
    # Calculate and display months until graduation
    months_left = calculate_months_until_graduation(graduation_year)
    if months_left > 0:
        st.caption(f"📅 ~{months_left} months until graduation")
    else:
        st.caption("🎓 Already graduated!")
    
    st.divider()
    
    st.header("📊 Investment Comparison")
    investment_choice = st.selectbox(
        "Compare savings to:",
        options=list(INVESTMENT_RETURNS.keys()),
        index=0
    )
    
    st.divider()
    
    st.header("ℹ️ About")
    st.markdown("""
    **Privacy First**: Your data never leaves your browser.
    
    **How it works**:
    1. Export your bank statement as CSV
    2. Upload it here
    3. Get instant insights!
    
    *Built for students, by students* 🎓
    """)

# Main content
tab1, tab2, tab3 = st.tabs(["📤 Upload & Analyze", "📈 What-If Calculator", "💡 Demo Mode"])

# ============================================
# TAB 1: Upload & Analyze
# ============================================
with tab1:
    st.header("Upload Your Bank Statement")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        uploaded_file = st.file_uploader(
            "Choose a CSV file",
            type=['csv'],
            help="Export your bank statement as CSV from your bank's website"
        )
    
    with col2:
        st.markdown("**Supported formats:**")
        st.markdown("- Most bank CSV exports")
        st.markdown("- Mint exports")
        st.markdown("- Custom CSVs with 'description' column")
    
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            
            st.success(f"✅ Loaded {len(df)} transactions")
            
            # Try to find the description column
            desc_col = None
            possible_cols = ['description', 'Description', 'DESCRIPTION', 'memo', 'Memo', 
                           'transaction', 'Transaction', 'name', 'Name', 'merchant', 'Merchant']
            
            for col in possible_cols:
                if col in df.columns:
                    desc_col = col
                    break
            
            if desc_col is None:
                st.warning("⚠️ Couldn't auto-detect description column. Please select:")
                desc_col = st.selectbox("Select the column with transaction descriptions:", df.columns)
            
            # Detect subscriptions
            with st.spinner("🔍 Analyzing transactions..."):
                detected_df = detect_subscriptions(df, desc_col)
            
            if not detected_df.empty:
                st.header("🎯 Detected Subscriptions")
                
                # Summary metrics
                col1, col2, col3, col4 = st.columns(4)
                
                unique_subs = detected_df['subscription'].nunique()
                total_found = len(detected_df)
                student_discount_subs = detected_df[detected_df['has_student_discount']]['subscription'].nunique()
                annual_estimate = estimate_annual_waste(detected_df)
                
                with col1:
                    st.metric("Subscriptions Found", unique_subs)
                with col2:
                    st.metric("Total Charges", total_found)
                with col3:
                    st.metric("With Student Discounts", student_discount_subs)
                with col4:
                    st.metric("Est. Annual Cost", f"${annual_estimate:,.2f}")
                
                st.divider()
                
                # Subscription breakdown
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("📋 Subscription List")
                    summary = detected_df.groupby(['subscription', 'category', 'has_student_discount']).agg({
                        'amount': ['count', 'sum'],
                        'avg_monthly': 'first'
                    }).reset_index()
                    summary.columns = ['Subscription', 'Category', 'Student Discount Available', 'Charges', 'Total Spent', 'Avg Monthly']
                    summary['Student Discount Available'] = summary['Student Discount Available'].map({True: '✅ Yes', False: '❌ No'})
                    st.dataframe(summary, use_container_width=True, hide_index=True)
                
                with col2:
                    st.subheader("📊 Spending by Category")
                    category_spending = detected_df.groupby('category')['amount'].sum().reset_index()
                    fig = px.pie(category_spending, values='amount', names='category', 
                                color_discrete_sequence=px.colors.qualitative.Set2)
                    fig.update_layout(margin=dict(t=0, b=0, l=0, r=0))
                    st.plotly_chart(fig, use_container_width=True)
                
                # Alerts
                st.divider()
                st.subheader("⚠️ Alerts & Recommendations")
                
                # Check for duplicates
                duplicate_categories = find_duplicates(detected_df)
                if duplicate_categories:
                    for cat in duplicate_categories:
                        subs_in_cat = detected_df[detected_df['category'] == cat]['subscription'].unique()
                        st.warning(f"🔄 **Duplicate {cat} services detected**: {', '.join(subs_in_cat)}. Consider keeping just one!")
                
                # Check for student discounts not being used
                student_subs = detected_df[detected_df['has_student_discount']]['subscription'].unique()
                if len(student_subs) > 0:
                    st.info(f"🎓 **Student discounts available for**: {', '.join(student_subs)}. Make sure you're using them!")
                
                # ============================================
                # EXPIRATION ALERTS - New Feature
                # ============================================
                months_left = calculate_months_until_graduation(graduation_year)
                expiring_urgent, expiring_soon = get_expiring_discounts(detected_df, months_left)
                
                if months_left == 0:
                    # Already graduated
                    if len(student_subs) > 0:
                        annual_increase, affected = calculate_post_graduation_cost(detected_df)
                        st.error(f"""
                        🚨 **Student Discounts Expired!**
                        
                        You've graduated! Your student discounts for **{', '.join(student_subs)}** are likely no longer valid.
                        
                        **Estimated annual cost increase: ${annual_increase:,.0f}**
                        
                        Action: Verify your student status with each service or find alternatives.
                        """)
                elif months_left <= 3:
                    # Expiring very soon (within 3 months)
                    if len(student_subs) > 0:
                        annual_increase, affected = calculate_post_graduation_cost(detected_df)
                        st.error(f"""
                        ⏰ **Student Discounts Expiring in ~{months_left} Months!**
                        
                        These subscriptions will lose student pricing soon: **{', '.join(student_subs)}**
                        
                        **Your costs will increase by ~${annual_increase:,.0f}/year** after graduation.
                        
                        💡 **Tips:**
                        - Lock in annual plans now at student rates
                        - Download offline content before discounts expire
                        - Research alumni discounts or alternatives
                        """)
                elif months_left <= 6:
                    # Expiring soon (within 6 months)
                    if len(student_subs) > 0:
                        annual_increase, affected = calculate_post_graduation_cost(detected_df)
                        st.warning(f"""
                        ⚠️ **Student Discounts Expiring in ~{months_left} Months**
                        
                        Plan ahead! These discounts will expire after graduation: **{', '.join(student_subs)}**
                        
                        **Potential cost increase: ~${annual_increase:,.0f}/year**
                        
                        💡 Consider switching to annual billing to lock in student rates longer.
                        """)
                elif months_left <= 12:
                    # Heads up (within a year)
                    if len(student_subs) > 0:
                        st.info(f"""
                        📅 **Graduation in ~{months_left} months**
                        
                        Start planning for when your student discounts expire: {', '.join(student_subs)}
                        """)
                
                # What-if calculation
                st.divider()
                st.subheader(f"💰 What If You Invested This Money in {investment_choice}?")
                
                potential_value, gain, return_pct = calculate_what_if(annual_estimate, investment_choice)
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Annual Subscription Cost", f"${annual_estimate:,.2f}")
                with col2:
                    st.metric(f"If Invested in {investment_choice}", f"${potential_value:,.2f}")
                with col3:
                    st.metric("Potential Gain", f"${gain:,.2f}", f"+{return_pct:.0f}%")
                
            else:
                st.info("No subscriptions detected in this file. Try uploading a different statement or check the column selection.")
                
        except Exception as e:
            st.error(f"Error processing file: {str(e)}")

# ============================================
# TAB 2: What-If Calculator
# ============================================
with tab2:
    st.header("💭 What-If Investment Calculator")
    st.markdown("See what your subscription spending could become if invested instead.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        monthly_spending = st.number_input(
            "Monthly Subscription Spending ($)",
            min_value=0.0,
            max_value=1000.0,
            value=50.0,
            step=5.0
        )
        
        years = st.slider("Investment Period (Years)", 1, 10, 4)
    
    with col2:
        investment_type = st.selectbox(
            "Investment Type",
            options=list(INVESTMENT_RETURNS.keys()),
            key="whatif_investment"
        )
        
        annual_return = INVESTMENT_RETURNS[investment_type]
        st.metric("Expected Annual Return", f"{annual_return*100:.0f}%")
    
    # Calculate compound growth
    annual_contribution = monthly_spending * 12
    total_invested = annual_contribution * years
    
    # Compound interest calculation
    future_value = 0
    yearly_data = []
    for year in range(1, years + 1):
        future_value = (future_value + annual_contribution) * (1 + annual_return)
        yearly_data.append({
            'Year': year,
            'Total Contributed': annual_contribution * year,
            'Portfolio Value': future_value
        })
    
    yearly_df = pd.DataFrame(yearly_data)
    
    st.divider()
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Spent on Subscriptions", f"${total_invested:,.2f}")
    with col2:
        st.metric(f"Value if Invested in {investment_type}", f"${future_value:,.2f}")
    with col3:
        st.metric("Total Gain", f"${future_value - total_invested:,.2f}", f"+{((future_value/total_invested)-1)*100:.0f}%")
    
    # Chart
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=yearly_df['Year'],
        y=yearly_df['Total Contributed'],
        name='Money Spent on Subscriptions',
        marker_color='#e94560'
    ))
    fig.add_trace(go.Scatter(
        x=yearly_df['Year'],
        y=yearly_df['Portfolio Value'],
        name=f'If Invested in {investment_type}',
        line=dict(color='#00d4aa', width=3),
        mode='lines+markers'
    ))
    fig.update_layout(
        title='Subscription Spending vs Investment Growth',
        xaxis_title='Year',
        yaxis_title='Value ($)',
        legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01),
        hovermode='x unified'
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Regret Card
    st.divider()
    st.subheader("📱 Your Shareable Regret Card")
    
    regret_text = f"""
    🚨 SUBSCRIPTION REALITY CHECK 🚨
    
    I spend ${monthly_spending:.0f}/month on subscriptions
    
    In {years} years, that's ${total_invested:,.0f} gone!
    
    If I invested in {investment_type} instead:
    💰 ${future_value:,.0f} (+${future_value-total_invested:,.0f})
    
    Time to cut the waste! 💸
    """
    
    st.code(regret_text, language=None)
    st.caption("Copy and share with friends!")

# ============================================
# TAB 3: Demo Mode
# ============================================
with tab3:
    st.header("🎮 Demo Mode")
    st.markdown("Don't have a CSV handy? Try our demo with sample data!")
    
    if st.button("🚀 Run Demo Analysis", type="primary"):
        # Create sample data
        sample_data = pd.DataFrame({
            'date': pd.date_range(start='2024-01-01', periods=20, freq='15D'),
            'description': [
                'SPOTIFY PREMIUM', 'NETFLIX.COM', 'AMAZON PRIME*', 'CHEGG INC',
                'ADOBE CREATIVE', 'HULU LLC', 'SPOTIFY PREMIUM', 'NETFLIX.COM',
                'PLANET FITNESS', 'DOORDASH DASHPASS', 'SPOTIFY PREMIUM', 'NETFLIX.COM',
                'AMAZON PRIME*', 'CHEGG INC', 'HEADSPACE', 'SPOTIFY PREMIUM',
                'GRAMMARLY INC', 'NETFLIX.COM', 'HULU LLC', 'ADOBE CREATIVE'
            ],
            'amount': [
                -10.99, -15.49, -14.99, -19.95,
                -54.99, -7.99, -10.99, -15.49,
                -24.99, -9.99, -10.99, -15.49,
                -14.99, -19.95, -12.99, -10.99,
                -12.00, -15.49, -7.99, -54.99
            ]
        })
        
        st.subheader("📄 Sample Transaction Data")
        st.dataframe(sample_data.head(10), use_container_width=True)
        
        # Detect subscriptions
        detected_df = detect_subscriptions(sample_data, 'description')
        
        if not detected_df.empty:
            st.subheader("🎯 Demo Results")
            
            # Summary metrics
            col1, col2, col3, col4 = st.columns(4)
            
            unique_subs = detected_df['subscription'].nunique()
            total_found = len(detected_df)
            student_discount_subs = detected_df[detected_df['has_student_discount']]['subscription'].nunique()
            annual_estimate = estimate_annual_waste(detected_df)
            
            with col1:
                st.metric("Subscriptions Found", unique_subs)
            with col2:
                st.metric("Total Charges", total_found)
            with col3:
                st.metric("With Student Discounts", student_discount_subs)
            with col4:
                st.metric("Est. Annual Cost", f"${annual_estimate:,.2f}", "-$200 if optimized")
            
            st.divider()
            
            # Detected subscriptions
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("📋 Detected Subscriptions")
                summary = detected_df.groupby(['subscription', 'category']).size().reset_index(name='charges')
                st.dataframe(summary, use_container_width=True, hide_index=True)
            
            with col2:
                st.subheader("📊 Category Breakdown")
                category_spending = detected_df.groupby('category')['amount'].sum().reset_index()
                fig = px.pie(category_spending, values='amount', names='category',
                            color_discrete_sequence=px.colors.qualitative.Set2)
                fig.update_layout(margin=dict(t=0, b=0, l=0, r=0))
                st.plotly_chart(fig, use_container_width=True)
            
            # Alerts
            st.divider()
            st.subheader("⚠️ Issues Found")
            
            st.warning("🔄 **Duplicate Streaming services**: Netflix, Hulu. Consider keeping just one!")
            st.info("🎓 **Student discounts available for**: Spotify, Amazon Prime, Hulu, Adobe Creative Cloud, Headspace, DoorDash DashPass, Grammarly")
            
            # Expiration alerts for demo
            months_left = calculate_months_until_graduation(graduation_year)
            student_subs_demo = ['Spotify', 'Amazon Prime', 'Hulu', 'Adobe Creative Cloud', 'Headspace', 'DoorDash DashPass', 'Grammarly']
            
            if months_left == 0:
                st.error(f"""
                🚨 **Student Discounts Expired!**
                
                You've graduated! Your student discounts are likely no longer valid.
                
                **Estimated annual cost increase: ~$180**
                
                Action: Verify your student status or find alternatives.
                """)
            elif months_left <= 3:
                st.error(f"""
                ⏰ **Student Discounts Expiring in ~{months_left} Months!**
                
                Your costs will increase significantly after graduation.
                
                💡 **Tips:** Lock in annual plans now at student rates!
                """)
            elif months_left <= 6:
                st.warning(f"""
                ⚠️ **Student Discounts Expiring in ~{months_left} Months**
                
                Plan ahead! Consider switching to annual billing to lock in student rates longer.
                """)
            
            # What-if
            st.divider()
            potential_value, gain, return_pct = calculate_what_if(annual_estimate, 'Bitcoin')
            
            st.success(f"""
            💰 **Your Money Could Be Growing!**
            
            You're spending ~**${annual_estimate:,.0f}/year** on subscriptions.
            
            If invested in Bitcoin, that could be worth **${potential_value:,.0f}** (+{return_pct:.0f}%)
            
            That's **${gain:,.0f}** in potential gains you're missing out on!
            """)

# Footer
st.divider()
st.markdown("""
<div style="text-align: center; color: #a0a0a0; font-size: 0.9rem;">
    <p>🔒 <strong>Privacy First</strong>: Your data is processed locally and never uploaded to any server.</p>
    <p>Built with ❤️ for the Weekend Hackathon 2025 | Data Science & Analytics</p>
</div>
""", unsafe_allow_html=True)
