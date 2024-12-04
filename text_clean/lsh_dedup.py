import sys
import json
from sklearn.feature_extraction.text import HashingVectorizer
from datasketch import MinHash, MinHashLSH
from tqdm import tqdm

threshold = 0.7  # 相似度阈值
num_perm = 128  # hash函数数量
n_gram = 5
print("threshold", threshold)
print("num_perm", num_perm)
print("n_gram", n_gram)

print("load data...")
data = json.load(open(sys.argv[1]))
texts = []
for i in tqdm(data):
    convs = i["conversations"]
    text_samples = ""
    for conv in convs:
        temp = conv["value"] + '\n'
        text_samples += temp
    texts.append({"raw": i, "text_samples": text_samples})
print("before dedup:", len(texts))


def get_minhash(text):
    minhash = MinHash(num_perm=num_perm)
    vectorizer = HashingVectorizer(n_features=1024, ngram_range=(n_gram, n_gram), binary=True)
    vector = vectorizer.fit_transform([text])

    for idx in vector.nonzero()[1]:
        minhash.update(str(idx).encode('utf8'))
    return minhash


lsh = MinHashLSH(threshold=threshold, num_perm=num_perm)

unique_texts = []
for i, text in enumerate(tqdm(texts)):
    minhash = get_minhash(text["text_samples"])
    if not lsh.query(minhash):  # 查询LSH中是否已有相似的文本
        lsh.insert(f"text_{i}", minhash)  # 如果没有，插入新文本
        unique_texts.append(text["raw"])

print("after dedup:", len(unique_texts))
json.dump(unique_texts, open("dedup.json", 'w'), indent=2, ensure_ascii=False)
