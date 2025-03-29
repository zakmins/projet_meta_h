class MaxCoveringProblem:
    def __init__(self, file_path, k=None):
        """
        Initialize the Max Covering Problem instance using an SCP file.

        :param file_path: Path to the SCP data file.
        :param k: Number of subsets to select (default: set dynamically).
        """
        self.file_path = file_path
        self.universe, self.subsets = self.load_data()
        self.n = len(self.subsets)  # Number of subsets
        self.k = int(self.n * 2 / 3)   # Default k = 10% of subsets

    def load_data(self):
        subsets = []
        universe = set()

        with open(self.file_path, 'r') as f:
            lines = f.readlines()

        num_subsets, num_elements = int(lines[0].split()[0]), int(lines[0].split()[1]) # First line: number of elements & subsets
        print(f"Number of subsets: {num_subsets}, Number of elements: {num_elements}")
        universe = set(range(1, num_elements + 1))  # Universe: {1, 2, ..., num_elements}

        i = 1  # Start reading from the second line
        while i < len(lines):
            subset_size = int(lines[i].strip())
            j = i + 1
            subset = []

            while j < len(lines) and len(subset) < subset_size:
                elements = list(map(int, lines[j].split()))
                for element in elements:
                    if element not in subset:
                        subset.append(element)
                j += 1
            subsets.append(subset)
            i = j

        return universe, subsets
        


# Example usage:
file_path = "./test/4/scp41.txt"  # Replace with your actual SCP file
mcp = MaxCoveringProblem(file_path)
print(f"Value of k: {mcp.k}")
