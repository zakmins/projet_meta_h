from data_modeling import MaxCoveringProblem

def dfs(mcp, index=0, selection=None, covered_elements=None, best_selection=None, max_covered=None):
    """Recursive DFS to find the best selection of subsets using a 0/1 vector."""
    if selection is None:
        selection = [0] * mcp.n  # Initialize 0/1 vector
    if covered_elements is None:
        covered_elements = list()
    if best_selection is None:
        best_selection = [0] * mcp.n
    if max_covered is None:
        max_covered = list()

    # Base case: If we selected k subsets or processed all subsets
    if sum(selection) == mcp.k or index == mcp.n:
        # Update best solution if this selection covers more elements
        if len(covered_elements) > len(max_covered):
            return selection[:], covered_elements.copy()
        return best_selection, max_covered

    # Option 1: Skip current subset (keep it 0)
    best_selection, max_covered = dfs(mcp, index + 1, selection, covered_elements, best_selection, max_covered)

    # Option 2: Include current subset (set it to 1)
    selection[index] = 1  # Mark subset as selected
    new_covered = set(covered_elements) | set(mcp.subsets[index])
    best_selection, max_covered = dfs(mcp, index + 1, selection, new_covered, best_selection, max_covered)
    
    # Backtrack (reset the selection)
    selection[index] = 0  

    return best_selection, max_covered

# Example Usage
if __name__ == "__main__":
    mcp = MaxCoveringProblem('./test/4/scp41.txt')
    best_selection, covered_elements = dfs(mcp)

    print("Best Selection (0/1 Vector):", best_selection)
    print("Covered Elements:", covered_elements)
