# 🏢 Multi-Tenant RAG Chatbot

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)
![Kubernetes](https://img.shields.io/badge/kubernetes-compatible-success.svg)
![OpenShift](https://img.shields.io/badge/OpenShift-ready-EE0000.svg)

An enterprise-ready Retrieval-Augmented Generation (RAG) chatbot architecture designed to serve multiple tenants (clients, departments, or user groups) from a single unified deployment while ensuring **strict data isolation**. 

This repository provides a scalable foundation optimized for high-performance compute environments. It seamlessly integrates local open-weights models (e.g., Qwen 3.5 via Ollama) deployed on NVIDIA hardware (L40S, T4), while maintaining the flexibility to route to external APIs (e.g., Claude) depending on tenant requirements.

## ✨ Key Features

* **Strict Multi-Tenancy:** Logical separation of vector data ensures that Tenant A can never query or access Tenant B's embedded documents.
* **Hybrid LLM Routing:** Built-in support for switching between local inferences (Ollama/vLLM) and managed cloud APIs. 
* **Enterprise Orchestration:** Fully containerized and packaged with Helm charts for rapid deployment onto Kubernetes and OpenShift clusters.
* **Hardware Optimized:** Ready for GPU acceleration with configured constraints and node selectors for NVIDIA L40S and T4 instances.
* **Scalable Ingestion:** Asynchronous document processing and chunking pipeline capable of handling large PDF, TXT, and DOCX workloads.

## 🏗️ Architecture Overview

The system follows a modular design pattern:
1. **Ingestion Layer:** Validates tenant IDs, chunks documents, generates embeddings, and stores them in isolated collections within the Vector Database.
2. **Retrieval Layer:** Intercepts user queries, filters vector searches strictly by the authenticated `tenant_id`, and retrieves context.
3. **Generation Layer:** Constructs the final prompt and streams the response via the selected LLM backend.

## 🚀 Getting Started

### Prerequisites
* Python 3.10+
* Docker & Docker Compose
* Helm 3.x (for cluster deployment)
* Access to an OpenShift/Kubernetes cluster (for production)

### Local Development (Docker Compose)

The easiest way to test the multi-tenant pipeline locally is via Docker Compose, which spins up the API, the vector database, and the local Ollama instance.

```bash
# 1. Clone the repository
git clone [https://github.com/YasirAzam6/Multi-Tenant-RAG-Chatbot.git](https://github.com/YasirAzam6/Multi-Tenant-RAG-Chatbot.git)
cd Multi-Tenant-RAG-Chatbot

# 2. Set your environment variables
cp .env.example .env

# 3. Spin up the infrastructure
docker-compose up -d --build
