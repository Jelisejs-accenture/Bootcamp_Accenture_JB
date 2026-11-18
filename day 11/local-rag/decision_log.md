# Day 11 - Local RAG Decision Log

## 1. Local Environment

Hardware:
- CPU: Intel Core i5-10310U
- RAM: 15.8 GB
- Inference: CPU
- Python: 3.12
- Ollama context length: 8192 tokens

I used local inference because the project involves internal company documents that should not be sent to external AI services. Ollama allowed me to run both the language model and embedding model on my own computer.

The main disadvantage was performance. My laptop does not have a dedicated GPU for inference, so generating longer answers sometimes took more than a minute.

## 2. Model Selection

Models tested:
- qwen3.5:2b-q4_K_M
- qwen3.5:4b-q4_K_M

Both models were tested on the same six prompts covering factual questions, reasoning, summarization, JSON formatting, Python code, and instruction following.

Measured total benchmark time:
- Qwen 2B: 87.84 seconds
- Qwen 4B: 149.85 seconds

Primary model: qwen3.5:2b-q4_K_M

I selected Qwen 2B because it was approximately 1.7 times faster in my benchmark and was more practical for repeated RAG testing on CPU. Qwen 4B generally followed instructions more consistently, but its slower generation made it less convenient on my hardware.

The benchmark also showed that model size alone is not enough to make a decision. Speed, answer quality, instruction following, and available hardware all matter. These results come from one benchmark run, so they should not be treated as universal performance measurements.

## 3. Document Processing

Documents: 5 PDF files
Extraction library: pypdf
Chunk size: 900 characters
Chunk overlap: 150 characters
Total indexed chunks: 216

I used character-based chunking because it was simple to implement and inspect. A 900-character chunk usually contains enough information to provide useful context without becoming excessively large. The 150-character overlap helps preserve information that crosses chunk boundaries.

These values were an initial configuration rather than the result of extensive parameter tuning.

One limitation is that dividing documents into relatively small chunks can separate information that belongs together. This was especially noticeable when questions required several sections or multiple pages.

## 4. Embeddings and Retrieval

Embedding model: nomic-embed-text
Vector database: ChromaDB
Similarity metric: cosine
Retrieval top-k: 4

I used nomic-embed-text because it can create embeddings locally through Ollama. ChromaDB provided a straightforward way to store the vectors and retrieve relevant document fragments.

The initial top-k value of 4 was intended to keep the context relatively small and reduce the amount of text sent to the language model.

This worked well for specific questions, such as identifying the company VPN or vendor security requirements. However, it performed worse for broad questions.

For example, the system failed to retrieve the Support and Onboarding section on pages 27-28 of product_guide.pdf. It also missed several action-item sections in meeting_notes.pdf.

## 5. RAG Evaluation

Evaluation dataset:
- Easy questions: 5
- Medium questions: 5
- Hard questions: 3
- Unanswerable questions: 2

Manual evaluation results:
- Passed: 8
- Failed: 7
- Strict pass rate: 53.33%

Results by difficulty:
- Easy: 4/5
- Medium: 1/5
- Hard: 1/3
- Unanswerable: 2/2

The evaluation showed that the system was reasonably reliable for simple factual retrieval, but struggled with questions that required combining information from several sections.

Question 4 showed that the model could mix two different training requirements. Question 6 contained correct information followed by a contradictory statement claiming that the information was unavailable.

Question 10 demonstrated a retrieval failure: the support procedures existed in the PDF, but the relevant pages were not retrieved.

Question 11 showed another retrieval limitation because the system did not include the important third-party vendor requirements for Restricted data.

Question 13 was initially truncated at 512 generated tokens. Increasing the limit to 1024 allowed a longer response, but did not solve the missing-context problem.

The system correctly refused to invent answers for both unanswerable questions.

My main conclusion is that a RAG system can produce an incorrect or incomplete answer even when the necessary information exists in its document collection. Good retrieval and correct source attribution are as important as the language model itself.

## 6. Retrieval Improvement Experiment

I performed an additional experiment for question 13, which asked about action items and responsibilities in the leadership meeting notes.

The original semantic search retrieved meeting_notes.pdf pages 1 and 9, together with unrelated fragments from other documents.

I tested a targeted retrieval method that searched for Action Items sections and included neighboring chunks.

This method retrieved 12 chunks covering meeting_notes.pdf pages 2, 3, 5, and 9. The resulting answer included citations to all four relevant pages.

However, the generated answer still repeated some information, occasionally grouped responsibilities incorrectly, and reached the new 1024-token limit.

This experiment demonstrated that improving retrieval can increase source coverage without necessarily fixing every generation problem. The original and revised outputs were saved separately for comparison.

## 7. Improvements I Would Prioritize

My first priority would be improving retrieval for questions involving multiple sections.

I would test higher top-k values, document-specific filtering, and combining semantic search with keyword search. I would also consider retrieving neighboring chunks when a relevant section is found.

For long questions, I would split the request into smaller subquestions and combine the results afterward. This could reduce repetition and improve coverage.

A second priority would be citation validation. The system currently extracts citations from the generated text, but it does not fully verify whether every cited page supports the statement.

I would also make the answer format more concise to reduce unnecessary token usage and avoid truncation.

These are proposed improvements, not changes that have all been implemented and benchmarked.

## 8. What Worked Well

The five PDF documents were successfully processed into 216 chunks and stored in a local ChromaDB collection.

The local embedding model and both Qwen language models worked through Ollama without sending the company documents to cloud AI services.

The system could retrieve relevant passages, generate answers, provide page-level citations, and save real performance measurements.

The evaluation pipeline also preserved the generated responses and manual pass/fail decisions, making it possible to inspect errors rather than relying only on an overall score.

## 9. What I Would Do Differently

I would test retrieval quality earlier, before running the full evaluation.

The first successful vendor-security question made the system appear more reliable than it actually was. The broader evaluation revealed problems that were not visible in simple tests.

I would also use more diverse retrieval test questions from the beginning and check whether the retrieved documents contain all the information needed to answer them.

Finally, I would separate evaluation of retrieval accuracy, citation accuracy, and answer quality instead of relying only on a single pass/fail result.

## 10. Final Reflection

This project helped demonstrate the practical trade-offs involved in building a local RAG system.

A small model can be useful on limited hardware, but the overall quality depends heavily on document processing, retrieval, prompt design, and evaluation.

The final strict pass rate was 53.33%, so the system is a working prototype rather than a production-ready assistant.

The most useful result was understanding why particular answers failed and identifying specific improvements that could make the system more reliable.
