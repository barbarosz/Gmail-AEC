# app.py
import streamlit as st
from emails_data import EMAILS  # This file must be in your folder
from datetime import datetime

st.set_page_config(layout="wide")




# ------------------ STYLING ------------------
st.markdown("""
<style>
    .top-bar {
        background-color: #f1f3f4;
        padding: 8px 20px;
        border-radius: 8px;
        margin-bottom: 10px;
        display: flex;
        align-items: center;
        font-size: 16px;
    }
    .tab-box {
        display: inline-block;
        background-color: #e0e0e0;
        padding: 6px 20px;
        margin-right: 8px;
        border-radius: 18px;
        font-weight: 500;
        cursor: pointer;
        color: #202124;
    }
    .tab-box.selected {
        background-color: #c2dbff;
    }
    .email-card {
        border-bottom: 1px solid #e0e0e0;
        padding: 15px;
    }
    .email-card:hover {
        background-color: #f5f5f5;
    }
    .subject {
        font-weight: bold;
    }
    .preview {
        color: #5f6368;
    }
</style>
""", unsafe_allow_html=True)

# ------------------ Search Bar ------------------
search_query = st.text_input("🔍 Search mail", placeholder="Search by sender, subject, or body...", key="search_bar")

# ------------------ Custom Tab Buttons ------------------
tab_labels = ["Primary", "Promotions", "Social", "Updates"]
selected_tab = st.session_state.get("selected_tab", "Primary")

cols = st.columns(len(tab_labels))
for i, tab in enumerate(tab_labels):
    if cols[i].button(tab, key=f"tab_{tab}"):
        selected_tab = tab
        st.session_state["selected_tab"] = tab

st.markdown(f"<h2>{selected_tab}</h2>", unsafe_allow_html=True)

# ------------------ Smart Categories Sidebar (AEC Toggle) ------------------
# ------------------ Smart Categories Sidebar (with AEC Toggle) ------------------
st.sidebar.image("https://ssl.gstatic.com/ui/v1/icons/mail/rfr/logo_gmail_lockup_default_1x_r5.png", width=150)

# AEC Toggle Button Below Logo
if "aec_enabled" not in st.session_state:
    st.session_state.aec_enabled = False

if st.sidebar.button("🚀 Activate AEC", key="aec_button"):
    st.session_state.aec_enabled = not st.session_state.aec_enabled

# Show Smart Categories only when AEC is ON
if st.session_state.aec_enabled:
    st.sidebar.markdown("### ✅ Smart Categories")
    smart_categories = sorted(list(set(email["category"] for email in EMAILS)))
    selected_categories = [
        cat for cat in smart_categories if st.sidebar.checkbox(cat, value=True)
    ]
else:
    # If AEC is OFF, show all categories by default
    selected_categories = sorted(list(set(email["category"] for email in EMAILS)))


# ------------------ Filter Emails by Tab + Category ------------------
base_filtered_emails = [
    email for email in EMAILS
    if email["tab"] == selected_tab and email["category"] in selected_categories
]

# ------------------ Apply Search Filter ------------------
if search_query.strip():
    filtered_emails = [
        email for email in base_filtered_emails
        if search_query.lower() in email["sender"].lower()
        or search_query.lower() in email["subject"].lower()
        or search_query.lower() in email["preview"].lower()
        or search_query.lower() in email["body"].lower()
    ]
else:
    filtered_emails = base_filtered_emails

# ------------------ Show Emails ------------------
if filtered_emails:
    for email in filtered_emails:
        st.markdown(f"""
        <div class="email-card">
            <div class="subject">{email['sender']} - {email['subject']}</div>
            <div class="preview">{email['preview']}</div>
            <div class="preview"><small>{email['date']}</small></div>
        </div>
        """, unsafe_allow_html=True)
else:
    st.info("No emails match your filters.")

st.write(f"Loaded {len(EMAILS)} emails")




