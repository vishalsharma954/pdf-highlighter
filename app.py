# import streamlit as st
# import fitz  # PyMuPDF
# import base64
# from io import BytesIO

# st.set_page_config(page_title="PDF Highlighter (Perfect Alignment)", layout="wide")
# st.title("🔍 PDF Highlighter")
# st.write("Upload a PDF, enter a word, and see true highlight annotations inside the PDF.")

# uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])
# search_word = st.text_input("Enter word to highlight (case-insensitive)")

# if uploaded_file and search_word.strip():
#     word = search_word.strip()

#     # Read bytes and open PDF
#     pdf_bytes = uploaded_file.read()
#     pdf = fitz.open(stream=pdf_bytes, filetype="pdf")

#     total_highlights = 0

#     # Highlight text in all pages
#     for page_number in range(len(pdf)):
#         page = pdf[page_number]

#         try:
#             found = page.search_for(word, flags=1)  # 1 = case-insensitive
#         except:
#             found = page.search_for(word)

#         for rect in found:
#             annot = page.add_highlight_annot(rect)
#             annot.update()
#             total_highlights += 1

#     st.success(f"Highlighted {total_highlights} match(es) inside the PDF (exact positions).")

#     # Save modified PDF to memory
#     out_pdf = BytesIO()
#     pdf.save(out_pdf)
#     pdf.close()

#     # Convert to base64 for iframe
#     base64_pdf = base64.b64encode(out_pdf.getvalue()).decode("utf-8")

#     # Show PDF inside iframe
#     st.write("### 📄 Highlighted PDF Preview")
#     pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="600"></iframe>'
#     st.markdown(pdf_display, unsafe_allow_html=True)

#     # Download button
#     st.download_button(
#         label="⬇️ Download Highlighted PDF",
#         data=out_pdf.getvalue(),
#         file_name="highlighted.pdf",
#         mime="application/pdf"
#     )


import streamlit as st
import fitz
from io import BytesIO
from streamlit_pdf_viewer import pdf_viewer

st.set_page_config(page_title="PDF Highlighter", layout="wide")

st.title("🔍 PDF Highlighter")
st.write("Upload a PDF, enter a word, and see true highlight annotations inside the PDF.")

# ---------------- SESSION STATE ----------------
if "pdf_bytes" not in st.session_state:
    st.session_state.pdf_bytes = None
if "last_result" not in st.session_state:
    st.session_state.last_result = None

uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])
if uploaded_file:
    st.session_state.pdf_bytes = uploaded_file.read()

search_word = st.text_input("Enter word to highlight")

# ---- Case-sensitive toggle ----
case_sensitive = st.toggle("Case-Sensitive Search", value=False)

# ---- Highlight Function Using Word Rectangles ----
def highlight_pdf():
    pdf = fitz.open(stream=st.session_state.pdf_bytes, filetype="pdf")
    total_highlights = 0
    target_word = search_word.strip()

    for page in pdf:
        # Get all words with their positions
        words = page.get_text("words")  # (x0, y0, x1, y1, word_text, block_no, line_no, word_no)
        for w in words:
            word_text = w[4]
            if case_sensitive:
                if word_text == target_word:
                    rect = fitz.Rect(w[:4])
                    annot = page.add_highlight_annot(rect)
                    annot.update()
                    total_highlights += 1
            else:
                if word_text.lower() == target_word.lower():
                    rect = fitz.Rect(w[:4])
                    annot = page.add_highlight_annot(rect)
                    annot.update()
                    total_highlights += 1

    out_pdf = BytesIO()
    pdf.save(out_pdf)
    pdf.close()

    st.session_state.last_result = {
        "pdf": out_pdf.getvalue(),
        "count": total_highlights
    }

# ---- Run Highlighting Automatically ----
if st.session_state.pdf_bytes and search_word.strip():
    highlight_pdf()

# ---- Show Result ----
if st.session_state.last_result:
    st.success(f"Highlighted {st.session_state.last_result['count']} match(es).")

    st.write("### 📄 Highlighted PDF Preview")
    pdf_viewer(st.session_state.last_result["pdf"])

    st.download_button(
        label="⬇️ Download Highlighted PDF",
        data=st.session_state.last_result["pdf"],
        file_name="highlighted.pdf",
        mime="application/pdf"
    )


# import streamlit as st
# import fitz
# from io import BytesIO
# from streamlit_pdf_viewer import pdf_viewer

# st.set_page_config(page_title="PDF Highlighter", layout="wide")

# st.title("🔍 PDF Highlighter")
# st.write("Upload a PDF, enter a word, and see true highlight annotations inside the PDF.")

# uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])
# search_word = st.text_input("Enter word to highlight (case-insensitive)")

# if uploaded_file and search_word.strip():
#     word = search_word.strip()

#     pdf_bytes = uploaded_file.read()
#     pdf = fitz.open(stream=pdf_bytes, filetype="pdf")

#     total_highlights = 0

#     for page in pdf:
#         try:
#             found = page.search_for(word, flags=1)
#         except:
#             found = page.search_for(word)

#         for rect in found:
#             annot = page.add_highlight_annot(rect)
#             annot.update()
#             total_highlights += 1

#     st.success(f"Highlighted {total_highlights} match(es).")

#     # Save modified PDF
#     out_pdf = BytesIO()
#     pdf.save(out_pdf)
#     pdf.close()

#     st.write("### 📄 Highlighted PDF Preview")

#     # SHOW PDF WITH VIEWER
#     pdf_viewer(out_pdf.getvalue())

#     # Download button
#     st.download_button(
#         label="⬇️ Download Highlighted PDF",
#         data=out_pdf.getvalue(),
#         file_name="highlighted.pdf",
#         mime="application/pdf"
#     )
