#!/usr/bin/python3
import os

class Node:
    
    """
    Represents a node in the sparse matrix linked list.
    Each node contains the row, column, and value of a non-zero element.
    """
    
    def __init__(self, row, col, value):
        self.row = row
        self.col = col
        self.value = value
        self.next = None

class SparseMatrix:
    
    """
    Represents a sparse matrix using a linked list structure.
    This class provides methods for matrix operations such as addition, subtraction, and multiplication.
    """
    
    def __init__(self, matrix_file_path=None, num_rows=0, num_cols=0):
        
        """
        Initializes a SparseMatrix object.
        
        Args:
            matrix_file_path (str, optional): Path to a file containing matrix data.
            num_rows (int, optional): Number of rows in the matrix.
            num_cols (int, optional): Number of columns in the matrix.
        """
        
        self.head = None
        self.num_rows = num_rows
        self.num_cols = num_cols
        if matrix_file_path:
            self.load_matrix(matrix_file_path)

    def load_matrix(self, matrix_file_path):
        
        """
        Loads matrix data from a file.
        """
        
        print(f"Attempting to load matrix from: {matrix_file_path}")
        try:
            with open(matrix_file_path, 'r') as file:
                lines = file.readlines()
                # Parse matrix dimensions
                self.num_rows = int(lines[0].split('=')[1].strip())
                self.num_cols = int(lines[1].split('=')[1].strip())
                # Parse and set matrix elements
                print(f"Matrix dimensions: {self.num_rows} x {self.num_cols}")
                for line in lines[2:]:
                    line = line.strip()
                    if line and line.startswith("(") and line.endswith(")"):
                        row, col, value = map(int, line[1:-1].split(','))
                        self.set_element(row, col, value)
                    else:
                        print(f"Skipping invalid line: {line}")
            print("Matrix loaded successfully")
        except FileNotFoundError:
            print(f"Error: File not found at {matrix_file_path}")
        except ValueError as e:
            print(f"Error parsing file: {e}")
        except Exception as e:
            print(f"Unexpected error: {type(e).__name__}: {e}")

    def set_element(self, row, col, value):
        
        """
        Sets the value of an element in the matrix.
        
        Args:
            row (int): Row index of the element.
            col (int): Column index of the element.
            value (int): Value to be set.
        """
        
        if value == 0:
            return  # Skip zero values

        new_node = Node(row, col, value)
        if not self.head:
            self.head = new_node
            return

        # Insert in order by row and column
        prev = None
        current = self.head
        while current and (current.row < row or (current.row == row and current.col < col)):
            prev = current
            current = current.next
        
        if prev:
            prev.next = new_node
        else:
            self.head = new_node
        new_node.next = current

    def get_element(self, row, col):
        
        """
        Retrieves the value of an element in the matrix.
        
        Args:
            row (int): Row index of the element.
            col (int): Column index of the element.
        
        Returns:
            int: Value of the element, or 0 if not found.
        """
        
        current = self.head
        while current:
            if current.row == row and current.col == col:
                return current.value
            current = current.next
        return 0

    def add(self, other):
        
        """
        Adds this matrix to another matrix.
        """
        
        if self.num_rows != other.num_rows or self.num_cols != other.num_cols:
            raise ValueError("Matrix dimensions must match for addition.")
        result = SparseMatrix(num_rows=self.num_rows, num_cols=self.num_cols)
        # Add elements from this matrix
        current = self.head
        while current:
            result.set_element(current.row, current.col, current.value)
            current = current.next
        # Add elements from the other matrix
        current = other.head
        while current:
            value = result.get_element(current.row, current.col)
            result.set_element(current.row, current.col, value + current.value)
            current = current.next
        return result

    def subtract(self, other):
        
        """
        Subtracts another matrix from this matrix.
        """
        
        if self.num_rows != other.num_rows or self.num_cols != other.num_cols:
            raise ValueError("Matrix dimensions must match for subtraction.")
        result = SparseMatrix(num_rows=self.num_rows, num_cols=self.num_cols)
        current = self.head
        while current:
            result.set_element(current.row, current.col, current.value)
            current = current.next
        current = other.head
        while current:
            value = result.get_element(current.row, current.col)
            result.set_element(current.row, current.col, value - current.value)
            current = current.next
        # Subtract elements from the other matrix
        return result

    def multiply(self, other):
        
        """
        Multiplies this matrix with another matrix.
        """
        
        if self.num_cols != other.num_rows:
            raise ValueError("Number of columns in first matrix must be equal to the number of rows in second matrix for multiplication.")
        
        result = SparseMatrix(num_rows=self.num_rows, num_cols=other.num_cols)
        current_self = self.head
        while current_self:
            current_other = other.head
            while current_other:
                if current_self.col == current_other.row:
                    existing_value = result.get_element(current_self.row, current_other.col)
                    result.set_element(current_self.row, current_other.col, 
                                       existing_value + current_self.value * current_other.value)
                current_other = current_other.next
            current_self = current_self.next
        return result

    def save_to_file(self, output_file_path):
        
        """
        Saves the matrix to a file.
        
        Args:
            output_file_path (str): Path to the output file.
        """
        
        with open(output_file_path, 'w') as file:
            file.write(f"Rows={self.num_rows}\n")
            file.write(f"Cols={self.num_cols}\n")
            current = self.head
            while current:
                file.write(f"({current.row},{current.col},{current.value})\n")
                current = current.next

    def display(self):
        
        """
        Displays the matrix elements.
        """
        
        current = self.head
        while current:
            print(f"({current.row}, {current.col}, {current.value})")
            current = current.next

def main():
    
    """
    Main function to demonstrate the usage of SparseMatrix class.
    """
    
    try:
        # Create SparseMatrix objects
        matrix1 = SparseMatrix()
        matrix2 = SparseMatrix()
        
        # Load matrices from files
        matrix1.load_matrix('./easy_sample_01_2.txt')
        
        with open('./easy_sample_01_2.txt', 'r') as file:
            print(file.read())
    
        matrix2.load_matrix('./easy_sample_01_3.txt')

        operation = input("Enter operation (add, subtract, multiply): ").strip().lower()
        print(f"Operation selected: {operation}")
        
        if operation == "add":
            print("Performing addition...")
            result = matrix1.add(matrix2)
        elif operation == "subtract":
            print("Performing subtraction...")
            result = matrix1.subtract(matrix2)
        elif operation == "multiply":
            print("Performing multiplication...")
            result = matrix1.multiply(matrix2)
        else:
            raise ValueError("Unknown operation.")

        print("Operation completed. Saving result...")
        result.save_to_file('./output.txt') 
        print("Result saved to output.txt")
        print("Displaying result:")
        result.display()

    except Exception as e:
        print(f"An error occurred: {type(e).__name__}: {e}")

if __name__ == "__main__":
    main()