import pandas as pd
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog
from pathlib import Path

def get_csv_path():
  root = tk.Tk()
  root.withdraw()
  file_path = filedialog.askopenfilename(
    title = "Select your Transactions CSV",
    filetypes = [("CSV files","*.csv")]
  )
  root.destroy()
  return file_path

def analyze_finances():
  
  csv_path = get_csv_path()
  
  if not csv_path:
    print("No file selected. Exiting...")
    return
  
  # Load data
  try:
    df = pd.read_csv(csv_path)
  except Exception as e:
    print(f"Error loading CSV: {e}")
    return
      
  # Basic analysis
  total_income = df[df['Amount'] > 0]['Amount'].sum()
  total_expenses = df[df['Amount'] < 0]['Amount'].sum()
  net_savings = total_income + total_expenses
  
  print("--- FINANCIAL SUMMARY ---")
  print(f"Total Income:   ${total_income:.2f}")
  print(f"Total Expenses: ${abs(total_expenses):.2f}")
  print(f"Net Savings:    ${net_savings:.2f}\n")
  
  # Category breakdown
  print("--- SPENDING BY CATEGORY ---")
  expenses_df = df[df['Amount'] < 0].copy()
  category_totals = expenses_df.groupby('Category')['Amount'].sum().abs()
  
  # Pie Chart
  print("Generating spending chart...")
  
  plt.style.use('ggplot') #(options: 'ggplot', 'seaborn-v0_8', 'fivethirtyeight')
  
  fig, ax = plt.subplots(figsize=(10,7)) #set size of window

  # Custom colors and 'Explode' (pops out the largest expense)
  colors = plt.cm.Paired(range(len(category_totals)))
  explode = [0.1 if (x == max(category_totals)) else 0 for x in category_totals]
  
  category_totals.plot(
    kind='pie',
    autopct = '%1.1f%%',
    startangle = 140,
    colors=colors,
    explode=explode,
    shadow=True,
    ax=ax
  )
  
  plt.title("Monthly Spending Breakdown", fontsize=16, pad=20)
  plt.ylabel('') #remove dafault vertical label
  
  #save chart as image 
  plt.savefig('spending_chart.png',dpi =300)
  print("Chart saved as 'spending_chart.png'")
  
  #show chart
  plt.show()
  
if __name__ == "__main__":
  analyze_finances()