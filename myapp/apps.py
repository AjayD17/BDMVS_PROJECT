from django.apps import AppConfig

class MyappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'myapp'

# from flask import Flask, request, jsonify, render_template, send_from_directory, url_for
# import os
# import fitz  # PyMuPDF
# import concurrent.futures

# app = Flask(__name__)

# # Directory where the PDF files are stored
# directory = 'Books'
# covers_directory = 'static/covers'
# os.makedirs(covers_directory, exist_ok=True)  # Ensure the covers directory exists

# def extract_first_page_image(pdf_filename):
#     """Extracts the first page image of a PDF."""
#     cover_image_path = None
#     try:
#         doc = fitz.open(pdf_filename)
#         first_page = doc[0]  # Get first page

#         # Render first page as an image
#         pix = first_page.get_pixmap(matrix=fitz.Matrix(2, 2))  # Higher resolution
#         cover_filename = os.path.splitext(os.path.basename(pdf_filename))[0] + ".png"
#         cover_path = os.path.join(covers_directory, cover_filename)
#         pix.save(cover_path)
#         cover_image_path = f"/static/covers/{cover_filename}"

#     except Exception as e:
#         print(f"Error extracting image from {pdf_filename}: {e}")

#     return cover_image_path

# def search_word_in_pdf(pdf_filename, search_word):
#     """Searches for a word in the PDF and extracts the first page image."""
#     try:
#         doc = fitz.open(pdf_filename)
#         total_occurrences = 0

#         for page_num in range(len(doc)):
#             page = doc.load_page(page_num)
#             text = page.get_text("text")
#             total_occurrences += text.lower().count(search_word.lower())

#         cover_image = extract_first_page_image(pdf_filename)

#         return pdf_filename, total_occurrences, cover_image

#     except FileNotFoundError:
#         return pdf_filename, 0, None
#     except Exception as e:
#         print(f"Error processing {pdf_filename}: {e}")
#         return pdf_filename, 0, None

# @app.route('/')
# def dummy():
#     return render_template('books.html')

# @app.route('/search', methods=['POST'])
# def search():
#     search_word = request.form.get('search_word')

#     if not search_word:
#         return jsonify({"error": "Search word is required."})

#     pdf_files = [f for f in os.listdir(directory) if f.endswith(".pdf")]
#     pdf_files = pdf_files[:100]  # Limit for performance

#     results = []

#     with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
#         future_to_pdf = {
#             executor.submit(search_word_in_pdf, os.path.join(directory, filename), search_word): filename
#             for filename in pdf_files
#         }

#         for future in concurrent.futures.as_completed(future_to_pdf):
#             filename = future_to_pdf[future]
#             try:
#                 occurrences, cover_image = future.result()[1:]
#                 if occurrences > 0:
#                     results.append({
#                         "book_name": filename.replace(".pdf", ""),
#                         "book_cover": cover_image if cover_image else "/static/default_cover.png",
#                         "download_link": f"/download/{filename}"
#                     })
#             except Exception as e:
#                 print(f"Error processing {filename}: {e}")

#     return jsonify({"status": "completed", "results": results})

# @app.route('/download/<book_name>')
# def download(book_name):
#     return send_from_directory(directory, book_name)

# if __name__ == '__main__':
#     app.run(debug=True)
    