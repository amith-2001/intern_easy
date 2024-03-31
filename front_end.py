import streamlit as st
import pandas as pd
import json

# Load the user data from the JSON file
@st.cache_data
def load_user_data():
    with open("user.json", 'r') as f:
        data = json.load(f)
    # Convert the list of dictionaries to a DataFrame for easier processing
    df = pd.json_normalize(data)
    return df

# Function to filter and sort user data
def filter_and_sort_users(df, skill_filter, sort_descending):
    if skill_filter:
        filtered_df = df[df['profile.skills'].str.contains(skill_filter, case=False)]
    else:
        filtered_df = df
    if sort_descending:
        filtered_df = filtered_df.sort_values(by='profile.knowledge_depth', ascending=False)
    return filtered_df

# Streamlit UI
def main():
    st.sidebar.header("User Data Filter Options")

    df = load_user_data()

    # User inputs for filtering in the sidebar
    skill_filter = st.sidebar.text_input("Filter by skills (e.g., Python, JavaScript):")
    sort_descending = st.sidebar.checkbox("Sort by Knowledge Depth (Descending)", value=True)


    st.title("🧠 User Skills and Knowledge Explorer")

    filtered_users = filter_and_sort_users(df, skill_filter, sort_descending)

    st.subheader("Filtered User Profiles")
    st.markdown("""
    Explore user profiles based on their skills and knowledge depth. Use the sidebar options to filter and sort the displayed profiles.
    """)

    if not filtered_users.empty:
        for index, row in filtered_users.iterrows():
            with st.container():
                col1, col2 = st.columns([1, 4])
                with col1:
                    st.image("https://via.placeholder.com/100", caption=f"{row['username']}")
                with col2:
                    st.markdown(f"**Username:** {row['username']}")
                    st.markdown(f"**Skills:** {row['profile.skills']}")
                    st.markdown(f"**Knowledge Depth:** {row['profile.knowledge_depth']}")
                    st.markdown(f"**Job Interest:** {row['profile.job_interest']}")
    else:
        st.warning("No users found. Adjust the filter criteria.")

if __name__ == "__main__":
    main()
