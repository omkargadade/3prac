# Practical 2: Huffman Encoding using Greedy method
import heapq

text = input("Enter text: ")

# Step 1: count frequency of each character
freq = {}
for ch in text:
    freq[ch] = freq.get(ch, 0) + 1

# Step 2: put every character in a min-heap as [frequency, [char, code]]
heap = [[f, [ch, ""]] for ch, f in freq.items()]
heapq.heapify(heap)

# Step 3 (greedy): take two smallest, merge them, repeat until one is left
while len(heap) > 1:
    lo = heapq.heappop(heap)             # smallest frequency
    hi = heapq.heappop(heap)             # second smallest
    for pair in lo[1:]:
        pair[1] = "0" + pair[1]          # left side gets 0
    for pair in hi[1:]:
        pair[1] = "1" + pair[1]          # right side gets 1
    heapq.heappush(heap, [lo[0] + hi[0]] + lo[1:] + hi[1:])

# Step 4: read codes from the final tree
codes = dict(heap[0][1:])

print("Char  Freq  Code")
for ch in codes:
    print(repr(ch), "  ", freq[ch], "  ", codes[ch])

encoded = "".join(codes[ch] for ch in text)
print("Encoded:", encoded)
print("Bits before:", 8 * len(text), " Bits after:", len(encoded))