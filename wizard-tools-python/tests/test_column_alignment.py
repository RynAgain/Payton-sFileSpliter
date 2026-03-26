"""
Test column alignment functionality for union operations
"""
import pandas as pd
import sys
from pathlib import Path

# Add parent directory to path for imports
parent_dir = Path(__file__).parent.parent / "src"
if str(parent_dir) not in sys.path:
    sys.path.insert(0, str(parent_dir))

from utils.file_processor import FileProcessor


def test_column_alignment():
    """Test that column alignment works correctly"""
    
    # Create test DataFrames with same columns in different orders
    df1 = pd.DataFrame({
        'Name': ['Alice', 'Bob'],
        'Age': [25, 30],
        'City': ['New York', 'Boston']
    })
    
    df2 = pd.DataFrame({
        'City': ['Chicago', 'Seattle'],
        'Name': ['Charlie', 'David'],
        'Age': [35, 40]
    })
    
    df3 = pd.DataFrame({
        'Age': [45, 50],
        'City': ['Miami', 'Denver'],
        'Name': ['Eve', 'Frank']
    })
    
    print("Original DataFrames:")
    print("\nDF1 columns:", list(df1.columns))
    print(df1)
    print("\nDF2 columns:", list(df2.columns))
    print(df2)
    print("\nDF3 columns:", list(df3.columns))
    print(df3)
    
    # Test alignment
    dfs = [df1, df2, df3]
    aligned_dfs = FileProcessor._align_dataframe_columns(dfs)
    
    print("\n" + "="*50)
    print("After alignment:")
    for i, df in enumerate(aligned_dfs, 1):
        print(f"\nAligned DF{i} columns:", list(df.columns))
        print(df)
    
    # Verify all DataFrames have same column order
    first_cols = list(aligned_dfs[0].columns)
    for i, df in enumerate(aligned_dfs[1:], 2):
        assert list(df.columns) == first_cols, f"DF{i} columns don't match DF1"
    
    print("\n" + "="*50)
    print("✓ All DataFrames have aligned columns!")
    
    # Test concatenation
    combined = pd.concat(aligned_dfs, ignore_index=True)
    print("\nCombined DataFrame:")
    print(combined)
    print(f"\nTotal rows: {len(combined)}")
    print(f"Columns: {list(combined.columns)}")
    
    print("\n✓ Column alignment test passed!")


def test_column_alignment_with_missing_columns():
    """Test alignment when DataFrames have different columns"""
    
    df1 = pd.DataFrame({
        'Name': ['Alice', 'Bob'],
        'Age': [25, 30],
        'City': ['New York', 'Boston']
    })
    
    df2 = pd.DataFrame({
        'Name': ['Charlie', 'David'],
        'Age': [35, 40],
        'Country': ['USA', 'Canada']  # Different column
    })
    
    print("\n" + "="*50)
    print("Test with different columns:")
    print("\nDF1 columns:", list(df1.columns))
    print(df1)
    print("\nDF2 columns:", list(df2.columns))
    print(df2)
    
    # Test alignment
    dfs = [df1, df2]
    aligned_dfs = FileProcessor._align_dataframe_columns(dfs)
    
    print("\nAfter alignment:")
    for i, df in enumerate(aligned_dfs, 1):
        print(f"\nAligned DF{i} columns:", list(df.columns))
        print(df)
    
    # Verify all columns are present
    all_columns = set(df1.columns) | set(df2.columns)
    for df in aligned_dfs:
        assert set(df.columns) == all_columns, "Not all columns present"
    
    print("\n✓ Alignment with different columns test passed!")


if __name__ == "__main__":
    test_column_alignment()
    test_column_alignment_with_missing_columns()
    print("\n" + "="*50)
    print("All tests passed! ✓")