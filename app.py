import streamlit as st
import requests

st.title("Universal Credit Act Analysis")

uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])

if uploaded_file is not None:
    files = {"file": (uploaded_file.name, uploaded_file, "application/pdf")}
    with st.spinner("Uploading and processing..."):
        response = requests.post("http://localhost:8000/upload-pdf/", files=files)

    if response.status_code == 200:
        data = response.json()

        st.header("Summary")
        st.write(data.get("summary", "No summary available."))

        st.header("Extracted Sections")
        sections = data.get("sections", {})
        if isinstance(sections, dict):
            for key, value in sections.items():
                st.subheader(key.capitalize())
                if isinstance(value, list):
                    for item in value:
                        st.write(f"- {item}")
                else:
                    st.write(value)
        else:
            st.write("No sections available.")

        st.header("Rule Check Results")
        rule_checks = data.get("rule_checks")

        if isinstance(rule_checks, list):
            for rule in rule_checks:
                st.markdown(f"**Rule:** {rule.get('rule', 'N/A')}")
                st.markdown(f"**Status:** {rule.get('status', 'N/A')}")
                st.markdown(f"**Evidence:** {rule.get('evidence', 'N/A')}")
                st.markdown(f"**Confidence:** {rule.get('confidence', 'N/A')}%")
                st.markdown("---")
        elif isinstance(rule_checks, dict) and "error" in rule_checks:
            st.error(f"LLM Error: {rule_checks['error']}")
            if "raw_response" in rule_checks:
                st.code(rule_checks["raw_response"])
        else:
            st.write("No rule check results available.")
    else:
        st.error(f"Error: {response.status_code} - {response.text}")
