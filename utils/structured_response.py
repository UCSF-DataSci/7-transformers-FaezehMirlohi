# Define a question to experiment with
question = "What foods should be avoided by patients with gout?"

# Example for one-shot and few-shot prompting
example_q = "What are the symptoms of gout?"
example_a = "Gout symptoms include sudden severe pain, swelling, redness, and tenderness in joints, often the big toe."

# Examples for few-shot prompting
examples = [
    ("What are the symptoms of gout?",
     "Gout symptoms include sudden severe pain, swelling, redness, and tenderness in joints, often the big toe."),
    ("How is gout diagnosed?",
     "Gout is diagnosed through physical examination, medical history, blood tests for uric acid levels, and joint fluid analysis to look for urate crystals.")
]

# TODO: Create prompting templates
# Zero-shot template (just the question)
zero_shot_template = "Question: {question}\nAnswer:"

# One-shot template (one example + the question)
one_shot_template = """Question: {example_q}
Answer: {example_a}

Question: {question}
Answer:"""

# Few-shot template (multiple examples + the question)
few_shot_template = """Question: {examples[0][0]}
Answer: {examples[0][1]}

Question: {examples[1][0]}
Answer: {examples[1][1]}

Question: {question}
Answer:"""

# TODO: Format the templates with your question and examples
zero_shot_prompt = zero_shot_template.format(question=question)
one_shot_prompt = one_shot_template.format(example_q=example_q, example_a=example_a, question=question)
# For few-shot, you'll need to format it with the examples list
few_shot_prompt = few_shot_template.format(examples=examples, question=question)

print("Zero-shot prompt:")
print(zero_shot_prompt)
print("\nOne-shot prompt:")
print(one_shot_prompt)
print("\nFew-shot prompt:")
print(few_shot_prompt)

from dotenv import load_dotenv
from huggingface_hub import InferenceClient
import os
def get_llm_response(prompt, model_name="google/flan-t5-base", api_key=None):
    """Get a response from the LLM based on the prompt"""
    # TODO: Implement the get_llm_response function
    token = os.getenv("API_KEY")
    client = InferenceClient(token = token)
    response = client.text_generation(prompt = prompt)
    return response.strip()

# TODO: Test your get_llm_response function with different prompts
test_payload = "What are the symptoms of diabetes?"
response = get_llm_response(test_payload)
print(response)

# List of healthcare questions to test
questions = [
    "What foods should be avoided by patients with gout?",
    "What medications are commonly prescribed for gout?",
    "How can gout flares be prevented?",
    "Is gout related to diet?",
    "Can gout be cured permanently?"
]

# TODO: Compare the different prompting strategies on these questions
# For each question:
results = []
for q in questions:
    # Create prompts
    zero_shot = f"Question: {q}\nAnswer:"
    
    one_shot = f"""Question: {examples[0][0]}
    Answer: {examples[0][1]}
    Question: {q}Answer:"""
    
    few_shot = f"""Question: {examples[0][0]}
    Answer: {examples[0][1]}
    Question: {examples[1][0]}
    Answer: {examples[1][1]}
    Question: {q}
    Answer:"""
    
    # Get responses
    zero_ans = get_llm_response(zero_shot)
    one_ans = get_llm_response(one_shot)
    few_ans = get_llm_response(few_shot)
    
    # Store results
    results.append({
        "question": q,
        "zero_shot": zero_ans,
        "one_shot": one_ans,
        "few_shot": few_ans
    })

def score_response(response, keywords):
    """Score a response based on the presence of expected keywords"""
    # TODO: Implement the score_response function
    # Example implementation:
    response = response.lower()
    found_keywords = 0
    for keyword in keywords:
        if keyword.lower() in response:
            found_keywords += 1
    return found_keywords / len(keywords) if keywords else 0

# Expected keywords for each question
expected_keywords = {
    "What foods should be avoided by patients with gout?": 
        ["purine", "red meat", "seafood", "alcohol", "beer", "organ meats"],
    "What medications are commonly prescribed for gout?": 
        ["nsaids", "colchicine", "allopurinol", "febuxostat", "probenecid", "corticosteroids"],
    "How can gout flares be prevented?": 
        ["medication", "diet", "weight", "alcohol", "water", "exercise"],
    "Is gout related to diet?": 
        ["yes", "purine", "food", "alcohol", "seafood", "meat"],
    "Can gout be cured permanently?": 
        ["manage", "treatment", "lifestyle", "medication", "chronic"]
}

# TODO: Score the responses and calculate average scores for each strategy
strategy_scores = {
    "zero_shot": [],
    "one_shot": [],
    "few_shot": []
}

# Score each response
for r in results:
    q = r["question"]
    keywords = expected_keywords.get(q, [])
    
    zero_score = score_response(r["zero_shot"], keywords)
    one_score = score_response(r["one_shot"], keywords)
    few_score = score_response(r["few_shot"], keywords)

    strategy_scores["zero_shot"].append(zero_score)
    strategy_scores["one_shot"].append(one_score)
    strategy_scores["few_shot"].append(few_score)

# Calculate averages
average_scores = {
    strategy: sum(scores) / len(scores) if scores else 0
    for strategy, scores in strategy_scores.items()
}

# Find best strategy
best_strategy = max(average_scores, key=average_scores.get)

# Print results
print("Average scores:")
for s, score in average_scores.items():
    print(f"{s}: {score:.2f}")

print(f"\nBest overall strategy: {best_strategy}")

import os

# Prepare results directory
os.makedirs("results/part_3", exist_ok=True)

# Build the content
lines = ["# Prompt Engineering Results\n"]

# Raw responses
for r in results:
    lines.append(f"## Question: {r['question']}\n")
    lines.append("### Zero-shot response:")
    lines.append(r["zero_shot"] + "\n")
    lines.append("### One-shot response:")
    lines.append(r["one_shot"] + "\n")
    lines.append("### Few-shot response:")
    lines.append(r["few_shot"] + "\n")
    lines.append("-" * 50 + "\n")

# Score table header
lines.append("## Scores\n")
lines.append("```\n")
lines.append("question,zero_shot,one_shot,few_shot")

# Score each question
for i, r in enumerate(results):
    q = r["question"]
    keywords = expected_keywords[q]
    z = score_response(r["zero_shot"], keywords)
    o = score_response(r["one_shot"], keywords)
    f = score_response(r["few_shot"], keywords)
    lines.append(f"{q.lower().replace(' ', '_').replace('?', '')},{z:.2f},{o:.2f},{f:.2f}")

# Average scores
avg_z = sum(strategy_scores["zero_shot"]) / len(strategy_scores["zero_shot"])
avg_o = sum(strategy_scores["one_shot"]) / len(strategy_scores["one_shot"])
avg_f = sum(strategy_scores["few_shot"]) / len(strategy_scores["few_shot"])
lines.append(f"\naverage,{avg_z:.2f},{avg_o:.2f},{avg_f:.2f}")
lines.append(f"best_method,{best_strategy}")
lines.append("```\n")

# Save to file
file_path = "results/part_3/prompt_comparison.txt"
with open(file_path, "w") as f:
    f.write("\n".join(lines))



