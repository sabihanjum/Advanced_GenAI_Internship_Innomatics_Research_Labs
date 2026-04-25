# RAG Customer Support Assistant

## Objective
Build a Retrieval-Augmented Generation (RAG) system that answers queries using a PDF knowledge base.

## Features
- PDF-based question answering
- Chunking and retrieval
- Simple RAG pipeline
- Human-in-the-Loop (HITL) escalation

## Workflow
PDF → Chunking → Retrieval → Answer Generation → HITL

## HITL
If no relevant information is found, the query is escalated to a human agent.

## Tech Stack
- Python
- LangChain
- Google Colab

## Example Output
- Query: refund policy → Answer returned  
- Query: random → HITL triggered  

## Note
This implementation uses a simplified retrieval-based approach due to API limitations while maintaining RAG architecture.
