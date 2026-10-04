import streamlit as st
from transformers import pipeline

# Page configuration
st.set_page_config(
    page_title="Smart Study Notes Generator",
    page_icon="📚",
    layout="centered"
)

# Title
st.title("📚 Smart Study Notes Generator")
st.write(
    "Enter a paragraph below and generate a short AI-powered summary."
)

# Load the summarization model
@st.cache_resource
def load_model():
    return pipeline(
        "summarization",
        model="sshleifer/distilbart-cnn-12-6"
    )

# Text input
text = st.text_area(
    "Enter your paragraph:",
    height=250,
    placeholder="Paste or type your study material here..."
)

# Generate summary
if st.button("✨ Generate Summary"):

    if not text.strip():
        st.warning("Please enter a paragraph first.")

    else:
        original_word_count = len(text.split())

        if original_word_count < 30:
            st.warning(
                "Please enter a longer paragraph (at least 30 words) "
                "for a better summary."
            )

        else:
            with st.spinner("Generating your summary..."):

                summarizer = load_model()

                # Limit input size for the model
                summary_result = summarizer(
                    text,
                    max_length=100,
                    min_length=20,
                    do_sample=False
                )

                summary = summary_result[0]["summary_text"]

            summary_word_count = len(summary.split())

            reduction_percentage = (
                (original_word_count - summary_word_count)
                / original_word_count
            ) * 100

            # Display results
            st.subheader("📝 Summary")
            st.write(summary)

            st.subheader("📊 Text Statistics")

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric(
                    "Original Words",
                    original_word_count
                )

            with col2:
                st.metric(
                    "Summary Words",
                    summary_word_count
                )

            with col3:
                st.metric(
                    "Text Reduced",
                    f"{reduction_percentage:.2f}%"
                )

            st.success("Summary generated successfully!")