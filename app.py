import streamlit as st
import fitz  # PyMuPDF
import base64
from io import BytesIO

st.set_page_config(page_title="PDF Highlighter (Perfect Alignment)", layout="wide")
st.title("🔍 PDF Highlighter")
st.write("Upload a PDF, enter a word, and see true highlight annotations inside the PDF.")

uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])
search_word = st.text_input("Enter word to highlight (case-insensitive)")

if uploaded_file and search_word.strip():
    word = search_word.strip()

    # Read bytes and open PDF
    pdf_bytes = uploaded_file.read()
    pdf = fitz.open(stream=pdf_bytes, filetype="pdf")

    total_highlights = 0

    # Highlight text in all pages
    for page_number in range(len(pdf)):
        page = pdf[page_number]

        try:
            found = page.search_for(word, flags=1)  # 1 = case-insensitive
        except:
            found = page.search_for(word)

        for rect in found:
            annot = page.add_highlight_annot(rect)
            annot.update()
            total_highlights += 1

    st.success(f"Highlighted {total_highlights} match(es) inside the PDF (exact positions).")

    # Save modified PDF to memory
    out_pdf = BytesIO()
    pdf.save(out_pdf)
    pdf.close()

    # Convert to base64 for iframe
    base64_pdf = base64.b64encode(out_pdf.getvalue()).decode("utf-8")

    # Show PDF inside iframe
    st.write("### 📄 Highlighted PDF Preview")
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="600"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)

    # Download button
    st.download_button(
        label="⬇️ Download Highlighted PDF",
        data=out_pdf.getvalue(),
        file_name="highlighted.pdf",
        mime="application/pdf"
    )
