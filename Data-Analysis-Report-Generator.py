import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os

def read_data(file_path):
    """Reads data from a CSV file and returns a DataFrame."""
    if not os.path.exists(file_path):
        print(f"Error: File not found at {file_path}")
        return None
    try:
        # Try reading the CSV file
        df = pd.read_csv(file_path)
        if df.empty:
            print("Error: The CSV file is empty.")
            return None
        return df
    except UnicodeDecodeError as e:
        print(f"Error: File encoding issue: {e}")
        return None
    except pd.errors.EmptyDataError:
        print("Error: No columns to parse from file.")
        return None
    except Exception as e:
        print(f"Error reading the file: {e}")
        return None

def format_dataframe(df):
    """Formats the DataFrame as a readable string with spacing."""
    return df.to_string(index=False)

def analyze_data(df):
    """Performs basic data analysis and returns a summary."""
    if df is None or df.empty:
        return "No data available for analysis."
    return df.describe().to_string()

def generate_pdf(report_path, data_content, summary):
    """Generates a PDF report with CSV contents followed by the analysis report."""
    try:
        c = canvas.Canvas(report_path, pagesize=letter)
        width, height = letter

        # Title
        c.setFont("Times-Roman", 18)
        c.drawString(200, height - 50, "Data Analysis Report")

        def add_text(text, start_y, spacing=15):
            y = start_y
            text_lines = text.split("\n")
            c.setFont("Times-Roman", 11)
            for line in text_lines:
                if y < 50:  # If we reach the bottom, start a new page
                    c.showPage()
                    c.setFont("Times-Roman", 11)
                    y = height - 50  # Reset y position for the new page
                c.drawString(50, y, line)
                y -= spacing  
            return y

        # Adding CSV contents to the PDF
        c.setFont("Times-Roman", 13)
        c.drawString(50, height - 80, "CSV File Contents:")
        y_position = add_text(data_content, height - 100, spacing=18)

        # Adding summary to the PDF
        y_position -= 30
        c.setFont("Times-Roman", 13)
        c.drawString(50, y_position, "Data Analysis Summary:")
        add_text(summary, y_position - 20, spacing=18)

        # Save the PDF
        c.save()
        print(f"PDF report generated successfully at {report_path}!")

    except Exception as e:
        print(f"Error generating PDF: {e}")

def main():
    input_file = r"C:\Cognifyz Tasks\Codtech\data.csv"  # Specify the input CSV file path
    output_pdf = r"C:\Cognifyz Tasks\Codtech\report.pdf"  # Specify the output PDF file path
    
    # Read data from the CSV file
    df = read_data(input_file)
    
    # If the DataFrame is successfully loaded, proceed with formatting and generating the PDF
    if df is not None:
        data_content = format_dataframe(df)  # Format DataFrame into a string
        summary = analyze_data(df)  # Generate data analysis summary
        generate_pdf(output_pdf, data_content, summary)  # Generate the PDF report
    else:
        print("Failed to generate the report due to data reading issues.")

if __name__ == "__main__":
    main()
