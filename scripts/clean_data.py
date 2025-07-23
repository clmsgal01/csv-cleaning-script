import pandas as pd
import matplotlib.pyplot as plt
from fpdf import FPDF
import os

# File paths
base_dir = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(base_dir, '..', 'data', 'sample_data.csv')
cleaned_csv_path = os.path.join(base_dir, '..', 'outputs', 'cleaned_data.csv')
age_chart_path = os.path.join(base_dir, '..', 'outputs', 'age_chart.png')
sales_chart_path = os.path.join(base_dir, '..', 'outputs', 'sales_chart.png')
report_path = os.path.join(base_dir, '..', 'outputs', 'report.pdf')

# Load CSV
df = pd.read_csv(data_path)

# Clean: Drop rows with missing values
df_clean = df.dropna()

# Save cleaned data
df_clean.to_csv(cleaned_csv_path, index=False)

# Create Age Distribution Chart
if 'Age' in df_clean.columns:
    plt.figure(figsize=(6, 4))
    df_clean['Age'].astype(int).hist(bins=10)
    plt.title('Age Distribution')
    plt.xlabel('Age')
    plt.ylabel('Count')
    plt.tight_layout()
    plt.savefig(age_chart_path)
    plt.close()

# Create Sales Distribution Chart
if 'Sales' in df_clean.columns:
    plt.figure(figsize=(6, 4))
    df_clean['Sales'].astype(float).hist(bins=10, color='orange')
    plt.title('Sales Distribution')
    plt.xlabel('Sales')
    plt.ylabel('Count')
    plt.tight_layout()
    plt.savefig(sales_chart_path)
    plt.close()

# Generate PDF report
pdf = FPDF()
pdf.add_page()

# Title
pdf.set_font("Arial", 'B', 16)
pdf.cell(0, 10, 'CSV Cleaning Report', ln=True)

# Summary text
pdf.set_font("Arial", '', 12)
summary_text = f"Original rows: {len(df)}\nCleaned rows: {len(df_clean)}\nColumns: {', '.join(df.columns)}"
for line in summary_text.split('\n'):
    pdf.cell(0, 10, line, ln=True)

pdf.ln(10)  # space before images

# Add Age chart
if os.path.exists(age_chart_path):
    pdf.image(age_chart_path, x=10, y=pdf.get_y(), w=pdf.w - 20)
else:
    print("❌ Age chart not found!")

# New page for Sales chart
pdf.add_page()

if os.path.exists(sales_chart_path):
    pdf.image(sales_chart_path, x=10, y=10, w=pdf.w - 20)
else:
    print("❌ Sales chart not found!")

# Save PDF
pdf.output(report_path)

print("✅ Cleaning complete. Report with charts saved in /outputs folder.")
