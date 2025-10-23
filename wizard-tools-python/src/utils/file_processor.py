"""
File processing utilities for Wizard Tools application
Handles CSV and Excel file operations
"""
import pandas as pd
import os
from pathlib import Path
from typing import List, Optional, Tuple, Dict
import sys

# Add parent directory to path for imports
parent_dir = Path(__file__).parent.parent
if str(parent_dir) not in sys.path:
    sys.path.insert(0, str(parent_dir))

from config import EXCEL_ENGINE, EXCEL_ENGINE_XLS
from utils.helpers import (
    is_csv_file,
    is_excel_file,
    create_output_filename,
    get_file_extension,
    ensure_directory_exists
)


class FileProcessor:
    """Handles file processing operations for CSV and Excel files"""
    
    @staticmethod
    def read_file(file_path: str, sheet_name: Optional[str] = None, **kwargs) -> pd.DataFrame:
        """
        Read a CSV or Excel file into a DataFrame
        
        Args:
            file_path: Path to the file
            sheet_name: Sheet name for Excel files (None for first sheet or CSV)
            **kwargs: Additional arguments for pandas read functions
            
        Returns:
            DataFrame containing file data
            
        Raises:
            ValueError: If file type is not supported
            Exception: If file cannot be read
        """
        # Only treat empty strings and whitespace as NA, not "NA" string
        # This prevents "North Atlantic" abbreviated as "NA" from being treated as missing
        na_values = ['', ' ', '  ']  # Only empty and whitespace strings
        
        if is_csv_file(file_path):
            return pd.read_csv(file_path, na_values=na_values, keep_default_na=False, **kwargs)
        elif is_excel_file(file_path):
            ext = get_file_extension(file_path)
            engine = EXCEL_ENGINE_XLS if ext == '.xls' else EXCEL_ENGINE
            # Use sheet_name parameter if provided, otherwise default to first sheet (0)
            sheet = sheet_name if sheet_name is not None else 0
            return pd.read_excel(file_path, engine=engine, sheet_name=sheet, na_values=na_values, keep_default_na=False, **kwargs)
        else:
            raise ValueError(f"Unsupported file type: {file_path}")
    
    @staticmethod
    def write_file(
        df: pd.DataFrame,
        file_path: str,
        **kwargs
    ) -> bool:
        """
        Write a DataFrame to a CSV or Excel file
        
        Args:
            df: DataFrame to write
            file_path: Output file path
            **kwargs: Additional arguments for pandas write functions
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Ensure output directory exists
            output_dir = os.path.dirname(file_path)
            if output_dir:
                ensure_directory_exists(output_dir)
            
            if is_csv_file(file_path):
                df.to_csv(file_path, index=False, **kwargs)
            elif is_excel_file(file_path):
                df.to_excel(file_path, index=False, engine=EXCEL_ENGINE, **kwargs)
            else:
                raise ValueError(f"Unsupported file type: {file_path}")
            
            return True
        except Exception as e:
            print(f"Error writing file: {e}")
            return False
    
    @staticmethod
    def chunk_file(
        file_path: str,
        output_dir: str,
        chunk_size: int,
        output_format: str = 'csv'
    ) -> Tuple[bool, List[str], str]:
        """
        Split a file into chunks
        
        Args:
            file_path: Path to input file
            output_dir: Directory for output files
            chunk_size: Number of rows per chunk
            output_format: Output format ('csv' or 'excel')
            
        Returns:
            Tuple of (success, list of output files, error message)
        """
        try:
            # Ensure output directory exists
            ensure_directory_exists(output_dir)
            
            # Get base filename
            base_name = Path(file_path).stem
            ext = '.csv' if output_format == 'csv' else '.xlsx'
            
            # Read file in chunks
            output_files = []
            chunk_num = 1
            
            if is_csv_file(file_path):
                # Process CSV file
                for chunk_df in pd.read_csv(file_path, chunksize=chunk_size):
                    output_file = os.path.join(
                        output_dir,
                        create_output_filename(base_name, '_chunk', ext, chunk_num)
                    )
                    
                    if output_format == 'csv':
                        chunk_df.to_csv(output_file, index=False)
                    else:
                        chunk_df.to_excel(output_file, index=False, engine=EXCEL_ENGINE)
                    
                    output_files.append(output_file)
                    chunk_num += 1
            
            elif is_excel_file(file_path):
                # Read entire Excel file (chunking not supported for Excel reading)
                ext_in = get_file_extension(file_path)
                engine = EXCEL_ENGINE_XLS if ext_in == '.xls' else EXCEL_ENGINE
                df = pd.read_excel(file_path, engine=engine)
                
                # Split into chunks
                total_rows = len(df)
                for start_idx in range(0, total_rows, chunk_size):
                    end_idx = min(start_idx + chunk_size, total_rows)
                    chunk_df = df.iloc[start_idx:end_idx]
                    
                    output_file = os.path.join(
                        output_dir,
                        create_output_filename(base_name, '_chunk', ext, chunk_num)
                    )
                    
                    if output_format == 'csv':
                        chunk_df.to_csv(output_file, index=False)
                    else:
                        chunk_df.to_excel(output_file, index=False, engine=EXCEL_ENGINE)
                    
                    output_files.append(output_file)
                    chunk_num += 1
            
            else:
                return False, [], "Unsupported file type"
            
            return True, output_files, ""
        
        except Exception as e:
            return False, [], str(e)
    
    @staticmethod
    def union_files(
        file_paths: List[str],
        output_path: str
    ) -> Tuple[bool, str]:
        """
        Combine files using union (concatenate rows)
        
        Args:
            file_paths: List of input file paths
            output_path: Output file path
            
        Returns:
            Tuple of (success, error message)
        """
        try:
            if not file_paths:
                return False, "No files provided"
            
            # Read all files
            dfs = []
            for file_path in file_paths:
                df = FileProcessor.read_file(file_path)
                dfs.append(df)
            
            # Concatenate all DataFrames
            combined_df = pd.concat(dfs, ignore_index=True)
            
            # Write output file
            success = FileProcessor.write_file(combined_df, output_path)
            
            if success:
                return True, ""
            else:
                return False, "Failed to write output file"
        
        except Exception as e:
            return False, str(e)
    
    @staticmethod
    def join_files(
        file_paths: List[str],
        output_path: str,
        join_column: str,
        join_type: str = 'inner'
    ) -> Tuple[bool, str]:
        """
        Combine files using join operation
        
        Args:
            file_paths: List of input file paths (at least 2)
            output_path: Output file path
            join_column: Column name to join on
            join_type: Type of join ('inner', 'outer', 'left', 'right')
            
        Returns:
            Tuple of (success, error message)
        """
        try:
            if len(file_paths) < 2:
                return False, "At least 2 files required for join"
            
            # Read first file
            result_df = FileProcessor.read_file(file_paths[0])
            
            # Check if join column exists
            if join_column not in result_df.columns:
                return False, f"Join column '{join_column}' not found in first file"
            
            # Join with remaining files
            for file_path in file_paths[1:]:
                df = FileProcessor.read_file(file_path)
                
                # Check if join column exists
                if join_column not in df.columns:
                    return False, f"Join column '{join_column}' not found in {os.path.basename(file_path)}"
                
                # Perform join
                result_df = result_df.merge(
                    df,
                    on=join_column,
                    how=join_type,
                    suffixes=('', f'_{os.path.basename(file_path)}')
                )
            
            # Write output file
            success = FileProcessor.write_file(result_df, output_path)
            
            if success:
                return True, ""
            else:
                return False, "Failed to write output file"
        
        except Exception as e:
            return False, str(e)
    
    @staticmethod
    def get_file_info(file_path: str) -> Dict[str, any]:
        """
        Get information about a file
        
        Args:
            file_path: Path to the file
            
        Returns:
            Dictionary with file information
        """
        try:
            df = FileProcessor.read_file(file_path)
            
            return {
                'rows': len(df),
                'columns': len(df.columns),
                'column_names': list(df.columns),
                'size_bytes': os.path.getsize(file_path),
                'file_type': get_file_extension(file_path)
            }
        except Exception as e:
            return {
                'error': str(e)
            }
    
    @staticmethod
    def get_column_names(file_path: str, sheet_name: Optional[str] = None) -> List[str]:
        """
        Get column names from a file
        
        Args:
            file_path: Path to the file
            sheet_name: Sheet name for Excel files (None for first sheet)
            
        Returns:
            List of column names
        """
        try:
            # Read only first row to get column names
            df = FileProcessor.read_file(file_path, sheet_name=sheet_name, nrows=1)
            return list(df.columns)
        except Exception:
            return []
    
    @staticmethod
    def get_excel_sheet_names(file_path: str) -> List[str]:
        """
        Get sheet names from an Excel file
        
        Args:
            file_path: Path to the Excel file
            
        Returns:
            List of sheet names, empty list if not an Excel file or error
        """
        try:
            if not is_excel_file(file_path):
                return []
            
            ext = get_file_extension(file_path)
            engine = EXCEL_ENGINE_XLS if ext == '.xls' else EXCEL_ENGINE
            
            # Read Excel file to get sheet names
            excel_file = pd.ExcelFile(file_path, engine=engine)
            return excel_file.sheet_names
        except Exception:
            return []