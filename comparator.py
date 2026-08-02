import os
import time

# Expanded Mock Database to give the user multiple choices
MOCK_DATABASE = {
    "binary_search": {
        "description": "An algorithmic puzzle to find a target value within a sorted array.",
        "Model_A": """
def binary_search(arr, target):
    low = 0
    high = len(arr) - 1
    while low <= high:
        mid = (low + high) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1
""",
        "Model_B": """
def binary_search(arr, target):
    if not arr:
        return -1
    mid = len(arr) // 2
    if arr[mid] == target:
        return mid
    elif arr[mid] < target:
        return binary_search(arr[mid+1:], target)
    else:
        return binary_search(arr[:mid], target)
"""
    },
    "bubble_sort": {
        "description": "A simple sorting algorithm that repeatedly steps through a list.",
        "Model_A": """
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr
""",
        "Model_B": """
def bubble_sort(arr):
    # Broken implementation: forgets to actually swap elements
    n = len(arr)
    for i in range(n):
        for j in range(0, n-1):
            if arr[j] > arr[j+1]:
                pass 
    return arr
"""
    }
}

class AIResponseComparator:
    """
    An interactive evaluation harness used to extract, format, and 
    automatically audit logic profiles of conflicting AI model responses.
    """
    def __init__(self, prompt_key: str):
        self.prompt_key = prompt_key
        self.prompt_payload = MOCK_DATABASE.get(prompt_key)

    def fetch_responses(self) -> dict:
        """Simulates an API fetch operation with simulated data mapping."""
        if not self.prompt_payload:
            raise ValueError(f"Error: Prompt payload '{self.prompt_key}' not found.")
        time.sleep(0.1)
        return self.prompt_payload

    def automated_syntax_check(self, code_string: str) -> bool:
        """Checks if the code compiles cleanly as valid Python syntax."""
        try:
            compile(code_string, '<string>', 'exec')
            return True
        except SyntaxError:
            return False

    def run_functional_assertion(self, code_string: str) -> str:
        """
        Safely executes the code inside an isolated scope and runs
        functional test cases to confirm logic accuracy.
        """
        local_scope = {}
        try:
            exec(code_string, {}, local_scope)
            
            # --- EVALUATION CASE 1: BINARY SEARCH ---
            if self.prompt_key == "binary_search":
                func = local_scope.get('binary_search')
                if not func:
                    return "❌ FAILED: Function 'binary_search' missing."
                
                test_arr = [10, 20, 30, 40, 50]
                # Target 40 lives exactly at Index 3
                if func(test_arr, 40) == 3:
                    return "✅ PASSED: Algorithm located the exact original index."
                else:
                    return f"❌ FAILED: Wrong index returned due to an internal array-slicing logic bug."

            # --- EVALUATION CASE 2: BUBBLE SORT ---
            elif self.prompt_key == "bubble_sort":
                func = local_scope.get('bubble_sort')
                if not func:
                    return "❌ FAILED: Function 'bubble_sort' missing."
                
                test_arr = [5, 1, 4, 2, 8]
                if func(test_arr.copy()) == [1, 2, 4, 5, 8]:
                    return "✅ PASSED: Array successfully sorted."
                else:
                    return "❌ FAILED: Array remained unsorted. Mutational tracking is broken."
                    
        except Exception as e:
            return f"❌ RUNTIME ERROR DURING CRASH TEST: {str(e)}"

    def run_evaluation_suite(self):
        """Coordinates the end-to-end lookup and interactive quality audit."""
        try:
            payload = self.fetch_responses()
            print("\n" + "=" * 75)
            print(f"🚀 RUNNING COMPARATOR LOGIC ON TARGET PROMPT: [{self.prompt_key.upper()}]")
            print(f"📋 Focus Area: {payload['description']}")
            print("=" * 75)

            for engine, code in payload.items():
                if engine == "description":
                    continue
                    
                print(f"\n[🔬 ANALYSING REPOSITORY ENGINE: {engine}]")
                print("-" * 55)
                print(code.strip())
                print("-" * 55)
                
                # Step 1: Syntax Audit
                if self.automated_syntax_check(code):
                    print("1. Structural Integrity  -> ✅ Clean Syntax Passed.")
                    # Step 2: Logic Validation
                    logic_report = self.run_functional_assertion(code)
                    print(f"2. Functional Assertion -> {logic_report}")
                else:
                    print("1. Structural Integrity  -> ❌ Structural Syntax Broken.")
                
            print("\n" + "=" * 75)

        except ValueError as e:
            print(e)


def interactive_menu():
    """Renders a command-line interface for direct human interaction."""
    print("=" * 60)
    print("🤖 INTERACTIVE AI PROMPT COMPONENT AUDITOR")
    print("=" * 60)
    print("Available test cases inside database:")
    
    # Dynamically print options from the Mock Database keys
    for index, key in enumerate(MOCK_DATABASE.keys(), 1):
        print(f" [{index}] {key}")
    print(" [E] Exit Application")
    print("-" * 60)
    
    user_choice = input("Enter choice index or profile name: ").strip().lower()
    
    if user_choice in ['e', 'exit', 'quit']:
        print("Exiting tool harness. Goodbye!")
        return

    # Map number inputs back to their database string key names
    key_mapping = {str(i): key for i, key in enumerate(MOCK_DATABASE.keys(), 1)}
    target_key = key_mapping.get(user_choice, user_choice)

    if target_key in MOCK_DATABASE:
        suite = AIResponseComparator(target_key)
        suite.run_evaluation_suite()
    else:
        print(f"❌ Error: Option '{user_choice}' does not match any code profiles in database.")


if __name__ == "__main__":
    # Runs the user interaction sequence loop natively
    interactive_menu()
