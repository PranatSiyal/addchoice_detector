import ssdeep

# Calculate fuzzy hash for a string or bytes
hash1 = ssdeep.hash_from_file("/Users/pranatsiyal/addchoice_detector/output_image.png")

# Compare two fuzzy hashes
hash2 = ssdeep.hash_from_file("/Users/pranatsiyal/addchoice_detector/output2_image.png")
similarity = ssdeep.compare(hash1, hash2)
print(f"Similarity between hashes: {similarity}", hash1,hash2)

# Output:
# Similarity between hashes: 93
