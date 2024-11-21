import json
from sklearn.feature_extraction.text import HashingVectorizer
from datasketch import MinHash, MinHashLSH
from tqdm import tqdm

threshold = 0.7
num_perm = 128
n_gram = 5
print(threshold, num_perm, n_gram)

print("load data...")
data = json.load(open("openorca.json"))
texts = []
for i in tqdm(data):
    convs = i["conversations"]
    text_samples = ""
    for conv in convs:
        temp = conv["value"] + '\n'
        text_samples += temp
    texts.append({"raw": i, "text_samples": text_samples})
print("before dedup:", len(texts))


# 定义一个函数，将文本转换为MinHash签名
def get_minhash(text, num_perm, n_gram):
    minhash = MinHash(num_perm=num_perm)  # hash函数数量128
    vectorizer = HashingVectorizer(n_features=1024, ngram_range=(1, n_gram), binary=True)
    vector = vectorizer.fit_transform([text])

    # 将向量中的非零元素转换为哈希签名
    for idx in vector.nonzero()[1]:
        minhash.update(str(idx).encode('utf8'))
    return minhash


# 创建LSH对象
lsh = MinHashLSH(threshold=threshold, num_perm=num_perm)  # 阈值0.7 hash函数数量128

# 对每个文本生成MinHash签名，并将其插入到LSH中
unique_texts = []
for i, text in enumerate(tqdm(texts)):
    minhash = get_minhash(text["text_samples"], num_perm, n_gram)
    if not lsh.query(minhash):  # 查询LSH中是否已有相似的文本
        lsh.insert(f"text_{i}", minhash)  # 如果没有，插入新文本
        unique_texts.append(text["raw"])

print("after dedup:", len(unique_texts))
json.dump(unique_texts, open("dedup.json", 'w'), indent=2, ensure_ascii=False)
