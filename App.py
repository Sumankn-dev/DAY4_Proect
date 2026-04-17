import streamlit as st
import pandas as pd
from extractor import extract_colleges_from_pdf
from enricher import enrich_college

st.title("🎓 CET College Data Extractor & Enricher")

uploaded_file = st.file_uploader("Upload CET PDF", type=["pdf"])

if uploaded_file:
    st.success("PDF Uploaded Successfully!")

    df = extract_colleges_from_pdf(uploaded_file)
    st.write("### Extracted Colleges", df)

    if st.button("🔍 Enrich Data"):
        enriched_data = []

        for college in df["College Name"]:
            st.write(f"Processing: {college}")
            enriched_data.append(enrich_college(college))

        final_df = pd.DataFrame(enriched_data)

        st.write("### Final Data", final_df)

        csv = final_df.to_csv(index=False).encode("utf-8")

        st.download_button(
            "📥 Download CSV",
            csv,
            "college_data.csv",
            "text/csv"
        )
