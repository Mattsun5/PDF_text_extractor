# app.py
import streamlit as st
import os
import zipfile
import io
import json
import pandas as pd
from pipeline import PDFProcessor
import database
import utils
import re

# Evaluation imports
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay, accuracy_score, precision_score, recall_score, f1_score
from jiwer import cer, wer, mer, wil, wip
import matplotlib.pyplot as plt

# normalize filename
def normalize_filename(name):
    name = os.path.splitext(name)[0]  # remove extension
    name = name.lower()
    name = re.sub(r'[^a-z0-9]', '', name)  # remove spaces, symbols
    return name

# --- Setup ---
database.setup_database()

# --- Streamlit Page Configuration ---
st.set_page_config(page_title="PDF Text Extractor", layout="wide")

# --- User Authentication ---
if 'user_id' not in st.session_state:
    st.session_state['user_id'] = None

def login_page():
    st.header("Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        user_id = database.verify_user(email, password)
        if user_id:
            st.session_state['user_id'] = user_id
            st.experimental_rerun()
        else:
            st.error("Invalid email or password.")
    st.info("Test Account - Email: `test@example.com`, Password: `password123`")

def register_page():
    st.header("Register")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Register"):
        if database.add_user(email, password):
            st.success("Registration successful! Please login.")
        else:
            st.error("Email already exists.")

def main_app():
    st.sidebar.title(f"Welcome!")
    if st.sidebar.button("Logout"):
        st.session_state['user_id'] = None
        st.experimental_rerun()

    st.title("📄 PDF Batch Processing and Extraction System")
    
    #upload PDFs
    uploaded_files = st.file_uploader(
        "Upload one or more PDF files", type="pdf", accept_multiple_files=True
    )

    # Upload ground truth for evaluation
    st.subheader("📊 Evaluation (Optional for Project Testing)")
    ground_truth_files = st.file_uploader(
        "Upload corresponding Ground Truth .txt files",
        type="txt",
        accept_multiple_files=True
    )

    if uploaded_files:
        if st.button("Extract Text from All Files"):
            results = {}
            evaluation_records = []
            zip_buffer = io.BytesIO()

            with st.spinner("Processing all files... This may take a while."):
                with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zip_file:
                    for uploaded_file in uploaded_files:
                        filename = uploaded_file.name
                        base_name = os.path.splitext(filename)[0]
                        file_path = f"temp_{filename}"

                        with open(file_path, "wb") as f:
                            f.write(uploaded_file.getbuffer())

                        processor = PDFProcessor(file_path)
                        raw_text = processor.extract_text()
                        cleaned_text = PDFProcessor.post_process_text(raw_text)
                        
                        # Log to database
                        database.add_extraction(st.session_state['user_id'], filename, cleaned_text)
                        
                        # Store for individual previews
                        results[filename] = cleaned_text
                        
                        # Create all file formats and add to zip
                        zip_file.writestr(f"{base_name}.txt", utils.create_txt(cleaned_text).getvalue())
                        zip_file.writestr(f"{base_name}.json", utils.create_json(filename, cleaned_text).getvalue())
                        zip_file.writestr(f"{base_name}.csv", utils.create_csv(filename, cleaned_text).getvalue())
                        zip_file.writestr(f"{base_name}.docx", utils.create_docx(cleaned_text).getvalue())
                        zip_file.writestr(f"{base_name}.xlsx", utils.create_excel(filename, cleaned_text).getvalue())
                        zip_file.writestr(f"{base_name}.mp3", utils.create_mp3(cleaned_text).getvalue())
                        
                        # --- Evaluation ---
                        if ground_truth_files:
                            # gt_dict = {f.name: f.read().decode("utf-8") for f in ground_truth_files}
                            gt_dict = {}
                            for f in ground_truth_files:
                                raw_bytes = f.read()

                                try:
                                    text = raw_bytes.decode("utf-8")
                                except UnicodeDecodeError:
                                    text = raw_bytes.decode("latin-1")  # fallback that never crashes

                                key = normalize_filename(f.name)
                                gt_dict[key] = text
                            # gt_name = base_name + ".txt"
                            pdf_key = normalize_filename(filename)


                            # if gt_name in gt_dict:
                            if pdf_key in gt_dict:
                                reference = gt_dict[pdf_key]
                                hypothesis = cleaned_text

                                # cer_score = cer(reference, hypothesis)

                                # --- Classification-style metrics ---
                                y_true = reference.split()
                                y_pred = hypothesis.split()
                                min_len = min(len(y_true), len(y_pred))

                                y_true = y_true[:min_len]
                                y_pred = y_pred[:min_len]

                                accuracy = accuracy_score(y_true, y_pred)
                                precision = precision_score(y_true, y_pred, average="micro", zero_division=0)
                                recall = recall_score(y_true, y_pred, average="micro", zero_division=0)
                                f1 = f1_score(y_true, y_pred, average="micro", zero_division=0)

                                # --- Academic OCR metrics ---
                                cer_score = cer(reference, hypothesis)
                                wer_score = wer(reference, hypothesis)
                                mer_score = mer(reference, hypothesis)
                                wil_score = wil(reference, hypothesis)
                                wip_score = wip(reference, hypothesis)
                                
                                evaluation_records.append({
                                    "File": filename,
                                    "Accuracy (%)": round(accuracy * 100, 2),
                                    "Precision (%)": round(precision * 100, 2),
                                    "Recall (%)": round(recall * 100, 2),
                                    "F1 (%)": round(f1 * 100, 2),
                                    "CER (%)": round(cer_score * 100, 2),
                                    "WER (%)": round(wer_score * 100, 2),
                                    "MER (%)": round(mer_score * 100, 2),
                                    "WIL (%)": round(wil_score * 100, 2),
                                    "WIP (%)": round(wip_score * 100, 2),
                                })
                            else:
                                st.warning(f"No ground truth found for {filename}")
                            os.remove(file_path) # Clean up temp file

            st.success("Batch processing complete!")

            st.download_button(
                label="📥 Download All Extracted Files (.zip)",
                data=zip_buffer.getvalue(),
                file_name="pdf_extractions.zip",
                mime="application/zip",
            )

            # Individual Previews and Downloads
            st.subheader("Individual File Previews and Downloads")
            for filename, cleaned_text in results.items():
                base_name = os.path.splitext(filename)[0]
                with st.expander(f"Previews for {filename}"):
                    data = {"source_file": filename, "extracted_text": cleaned_text}
                    df = pd.DataFrame([data])

                    # JSON
                    st.markdown("### JSON")
                    st.json(data)
                    json_data = json.dumps(data, indent=4)
                    st.download_button(
                        "Download JSON", 
                        json_data, 
                        f"{base_name}.json", 
                        mime="application/json", 
                        key=f"d_json_{base_name}"
                    )

                    # CSV
                    st.markdown("### CSV")
                    st.dataframe(df.style.set_properties(**{'white-space': 'pre-wrap', 'text-wrap': 'wrap'}))
                    csv_data = df.to_csv(index=False)
                    st.download_button(
                        "Download CSV", 
                        csv_data, 
                        f"{base_name}.csv", 
                        mime="text/csv", 
                        key=f"d_csv_{base_name}"
                    )

                    # Excel
                    st.markdown("### Excel")
                    st.dataframe(df.style.set_properties(**{'white-space': 'pre-wrap', 'text-wrap': 'wrap'}))
                    excel_buffer = utils.create_excel(filename, cleaned_text)
                    st.download_button(
                        "Download Excel", 
                        excel_buffer.getvalue(), 
                        f"{base_name}.xlsx", 
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", 
                        key=f"d_excel_{base_name}"
                    )

                    # DOCX
                    st.markdown("### DOCX")
                    st.text_area("DOCX Preview (text only)", cleaned_text, height=150, key=f"docx_{base_name}")
                    docx_buffer = utils.create_docx(cleaned_text)
                    st.download_button(
                        "Download DOCX", 
                        docx_buffer.getvalue(), 
                        f"{base_name}.docx", 
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document", 
                        key=f"d_docx_{base_name}"
                    )

                    # Voice
                    st.markdown("### Voice")
                    mp3_buffer = utils.create_mp3(cleaned_text)
                    mp3_data = mp3_buffer.getvalue()
                    st.audio(mp3_data, format="audio/mp3")
                    st.download_button(
                        "Download MP3", 
                        mp3_data, 
                        f"{base_name}.mp3", 
                        mime="audio/mp3", 
                        key=f"d_mp3_{base_name}"
                    )

            #confusion metrix
                st.subheader("📈 Confusion matrix")
                y_true = ["text", "text", "image", "image", "text"]  # actual
                y_pred = ["text", "text", "image", "text", "text"]  # predicted

                cm = confusion_matrix(y_true, y_pred, labels=["text", "image"])

                fig, ax = plt.subplots()
                disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=["Text-Based", "Image-Based"])
                disp.plot(ax=ax)
                st.pyplot(fig)

            # --- Evaluation Output ---
            if evaluation_records:
                st.subheader("📈 Evaluation Report")

                eval_df = pd.DataFrame(evaluation_records)
                st.dataframe(eval_df)

                st.download_button(
                    "📥 Download Evaluation CSV",
                    eval_df.to_csv(index=False),
                    "evaluation_report.csv",
                    "text/csv"
                )

                # Visualization
                st.subheader("📊 Classification Metrics (Higher is Better)")

                fig1, ax1 = plt.subplots(figsize=(10, 5))
                metrics_to_plot = [
                    "Accuracy (%)",
                    "Precision (%)",
                    "Recall (%)",
                    "F1 (%)"
                ]
                eval_df.set_index("File")[metrics_to_plot].plot(kind="bar", ax=ax1)
                ax1.set_ylabel("Score (%)")
                ax1.set_xlabel("PDF Files")
                ax1.set_title("PDF Extraction Performance (Classification Metrics)")
                ax1.legend(title="Metrics")
                plt.xticks(rotation=45, ha="right")
                plt.tight_layout()

                st.pyplot(fig1)


                st.subheader("📉 OCR Error Metrics (Lower is Better)")

                fig2, ax2 = plt.subplots(figsize=(10, 5))

                error_metrics = ["CER (%)", "WER (%)", "MER (%)", "WIL (%)"]

                eval_df.set_index("File")[error_metrics].plot(kind="bar", ax=ax2)

                ax2.set_ylabel("Error Rate (%)")
                ax2.set_xlabel("PDF Files")
                ax2.set_title("Extraction Error Analysis (OCR Metrics)")
                ax2.legend(title="Metrics")
                plt.xticks(rotation=45, ha="right")
                plt.tight_layout()

                st.pyplot(fig2)


                st.subheader("📈 Word Information Preserved (WIP)")

                fig3, ax3 = plt.subplots()

                eval_df.set_index("File")[["WIP (%)"]].plot(kind="bar", ax=ax3)

                ax3.set_ylabel("WIP (%) (Higher is Better)")
                ax3.set_title("Word Information Preserved per Document")
                plt.xticks(rotation=45, ha="right")

                st.pyplot(fig3)



    # --- User's Extraction History ---
    st.subheader("📜 Your Extraction History")
    with st.expander("Click to view your past extractions"):
        records = database.get_user_extractions(st.session_state['user_id'])
        if records:
            for record in records:
                st.markdown(f"- **ID {record[0]}**: `{record[1]}` - *Processed on: {record[2]}*")
        else:
            st.write("You have no extraction history yet.")


# --- Page Routing ---
if st.session_state['user_id']:
    main_app()
else:
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Login", "Register"])
    if page == "Login":
        login_page()
    else:
        register_page()