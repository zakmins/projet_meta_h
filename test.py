with open("./test/4/scp41.txt", 'r') as f:
            lines = f.readlines()

i = 1
subsets = []
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
    print(subset)
    subsets.append(subset)
    i = j

print(len(subsets))