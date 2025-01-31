import os
import sys
import json
import subprocess
from typing import Dict, List, Optional, Union

def run_test(test_case: Dict) -> Dict:
    """Execute a test case and return results"""
    try:
        # Extract test parameters
        input_data = test_case.get('input', {})
        expected_output = test_case.get('expected_output', {})
        
        # Run the filesystem operations
        actual_output = execute_filesystem_operation(input_data)
        
        # Compare results
        success = compare_outputs(actual_output, expected_output)
        
        return {
            'success': success,
            'actual_output': actual_output,
            'expected_output': expected_output,
            'error': None if success else 'Output mismatch'
        }
    except Exception as e:
        return {
            'success': False,
            'actual_output': None,
            'expected_output': expected_output,
            'error': str(e)
        }

def execute_filesystem_operation(input_data: Dict) -> Dict:
    """Execute filesystem operations based on input data"""
    operation = input_data.get('operation')
    path = input_data.get('path')
    content = input_data.get('content')
    permissions = input_data.get('permissions')
    
    result = {}
    
    if operation == 'read':
        with open(path, 'r') as f:
            result['content'] = f.read()
            result['success'] = True
    elif operation == 'write':
        with open(path, 'w') as f:
            f.write(content)
        result['success'] = True
    elif operation == 'delete':
        os.remove(path)
        result['success'] = True
    elif operation == 'check_permissions':
        result['permissions'] = oct(os.stat(path).st_mode)[-3:]
        result['success'] = True
    
    return result

def compare_outputs(actual: Dict, expected: Dict) -> bool:
    """Compare actual and expected outputs"""
    if not actual or not expected:
        return False
        
    for key in expected:
        if key not in actual:
            return False
        if actual[key] != expected[key]:
            return False
    return True

def main():
    # Create test directory if it doesn't exist
    test_dir = os.path.join(os.path.dirname(__file__), 'test_files')
    os.makedirs(test_dir, exist_ok=True)
    
    # Load test cases
    test_cases_file = os.path.join(os.path.dirname(__file__), 'test_cases.json')
    if not os.path.exists(test_cases_file):
        print(f"Creating default test cases file at {test_cases_file}")
        default_test_cases = [
            {
                "name": "Write and Read Test",
                "input": {
                    "operation": "write",
                    "path": os.path.join(test_dir, "test1.txt"),
                    "content": "Hello, World!"
                },
                "expected_output": {
                    "success": True
                }
            },
            {
                "name": "Permission Test",
                "input": {
                    "operation": "check_permissions",
                    "path": os.path.join(test_dir, "test1.txt")
                },
                "expected_output": {
                    "success": True,
                    "permissions": "644"
                }
            }
        ]
        with open(test_cases_file, 'w') as f:
            json.dump(default_test_cases, f, indent=2)

    with open(test_cases_file, 'r') as f:
        test_cases = json.load(f)

    # Run tests
    results = []
    for test_case in test_cases:
        print(f"\nRunning test: {test_case.get('name', 'Unnamed test')}")
        result = run_test(test_case)
        results.append(result)

    # Report results
    success_count = sum(1 for r in results if r['success'])
    print(f"\nTest Results: {success_count}/{len(results)} passed")
    
    for i, result in enumerate(results):
        print(f"\nTest {i + 1}:")
        print(f"Success: {result['success']}")
        if not result['success']:
            print(f"Error: {result['error']}")
            print(f"Expected: {result['expected_output']}")
            print(f"Actual: {result['actual_output']}")

if __name__ == "__main__":
    main()