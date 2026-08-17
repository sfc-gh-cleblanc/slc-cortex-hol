import streamlit as st

st.title("Getting Started")
st.markdown("Provision a Snowflake account for the workshop")

st.write("")

st.markdown("#### Step 1: Sign up for a free trial")

with st.container(border=True):
    st.markdown("""
Go to **[signup.snowflake.com](https://signup.snowflake.com/?t=5e52c965fa2b4d430e74c67647f2d2ec1fb3bc1dc72710dd25cf5f919cef5e06&cloud=aws&region=us-east-2)** and fill out the registration form with your name, email, and company.

Leave the trial type set to **AI Data Cloud For Enterprise** (the default). We will be using Cortex Code within Snowsight — the "Developers" option includes a locally installed IDE component which is not required for this workshop.

On the **Choose your Snowflake edition** screen, select:

| Setting | Recommended value |
|---------|-------------------|
| **Cloud provider** | Amazon Web Services (AWS) |
| **Edition** | Enterprise |
| **Region** | AWS US East (Ohio) |

Enterprise edition is recommended because it includes all the AI/ML features we use in this workshop.
""")

st.write("")

st.markdown("#### Step 2: Activate your account")

with st.container(border=True):
    st.markdown("""
After submitting the form, Snowflake sends an **activation link** to the email address you provided. Click the link to set your password and log in.

:material/info: The activation email typically arrives within a few minutes. Check your spam folder if you don't see it.
""")

st.write("")

st.markdown("#### Step 3: Open Cortex Code")

with st.container(border=True):
    st.markdown("""
Once logged in to Snowsight, open **Cortex Code** from the left navigation panel. This is the AI coding assistant where you will paste all prompts from this workshop.

Confirm you are using the **ACCOUNTADMIN** role — you can check and switch roles in the bottom-left of the Snowsight UI.
""")

st.write("")

st.markdown("#### Step 4: Enable cross-region inference")

with st.container(border=True):
    st.markdown("""
Several sessions use Cortex LLM models that require cross-region inference. Enable it by running this SQL in a worksheet:

```sql
ALTER ACCOUNT SET CORTEX_ENABLED_CROSS_REGION = 'ANY_REGION';
```

This allows Snowflake to route LLM requests to the nearest available region if the model is not hosted in your account's home region.
""")

st.write("")

st.markdown("#### Free trial details")

col1, col2, col3 = st.columns(3)
col1.metric("Duration", "30 days", help="Free trial duration from activation")
col2.metric("Credits", "$400", help="Complimentary Snowflake credits included")
col3.metric("Credit card", "Not required", help="No payment method needed to start")

st.caption("The free trial provides more than enough credits to complete the entire workshop")
