import openai

# 初始化OpenAI API
openai.api_key = "YOUR_OPENAI_API_KEY"
THRESHOLD = 0.5

def get_answer_from_document(question, document):
    # 使用OpenAI的embedding接口获取文档的向量表示
    document_embedding = openai.Embedding.create(model="text-embedding-ada-002", texts=[document])

    # 使用OpenAI的embedding接口获取问题的向量表示
    question_embedding = openai.Embedding.create(model="text-embedding-ada-002", texts=[question])

    # 计算问题和文档之间的相似度（这只是一个简单的示例，实际应用中可能需要更复杂的计算）
    similarity_score = compute_similarity(document_embedding, question_embedding)

    # 如果相似度超过某个阈值，则使用OpenAI的Completion接口来生成答案
    if similarity_score > THRESHOLD:
        response = openai.Completion.create(model="gpt-4", prompt=f"{document}\n\nQ: {question}\nA:", max_tokens=150)
        return response.choices[0].text.strip()
    else:
        return "Sorry, I couldn't find a relevant answer in the document."

def compute_similarity(embedding1, embedding2):
    # 这是一个简单的点积计算来比较两个向量的相似度
    return sum([a*b for a, b in zip(embedding1, embedding2)])

# 示例
document = "这是一个长文档的内容。"
question = "文档是关于什么的？"
print(get_answer_from_document(question, document))
