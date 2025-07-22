import pandas as pd
import matplotlib.pyplot as plt
from fpdf import FPDF
import os

# File paths
base_dir = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(base_dir, '..', 'data', 'sample_data.csv')
cleaned_csv_path = os.path.join(base_dir, '..', 'outputs', 'cleaned_data.csv')
plot_path = os.path.join(base_dir, '..', 'outputs', 'plot.png')
pdf_path = os.path.join(base_dir, '..', 'outputs', 'report.pdf')

# Load CSV
df = pd.read_csv(data_path)

# Clean: Drop rows with missing values
df_clean = df.dropna()

# Save cleaned data
df_clean.to_csv(cleaned_csv_path, index=False)

# Generate a simple plot (e.g., Age distribution)
if 'Age' in df_clean.columns:
    plt.figure(figsize=(6, 4))
    df_clean['Age'].astype(int).hist(bins=10)
    plt.title('Age Distribution')
    plt.xlabel('Age')
    plt.ylabel('Count')
    plt.tight_layout()
    plt.savefig(plot_path)
    plt.close()

# Generate PDF report
pdf = FPDF()
pdf.add_page()

# Title
pdf.set_font("Arial", 'B', 16)
pdf.cell(0, 10, 'CSV Cleaning Report', ln=True)

# Add summary
pdf.set_font("Arial", '', 12)
summary_text = f"Original rows: {len(df)}\nCleaned rows: {len(df_clean)}\nColumns: {', '.join(df.columns)}"
for line in summary_text.split('\n'):
    pdf.cell(0, 10, line, ln=True)

# Add plot image
if os.path.exists(plot_path):
    pdf.image(plot_path, x=10, y=60, w=pdf.w - 20)

# Save PDF
pdf.output(pdf_path)

print("✅ Cleaning complete. Outputs saved in /outputs folder.")
