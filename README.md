<div align="center">

# 🎬 Movie Analytics Dashboard

### End-to-end movie analytics and AI recommendation platform

Built with **FastAPI**, **Supabase**, **Streamlit**, **TMDB API** and **OpenAI**

<br>

![Python](https://img.shields.io/badge/Python-3.12-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.136-009688)
![Streamlit](https://img.shields.io/badge/Streamlit-1.58-FF4B4B)
![Supabase](https://img.shields.io/badge/Supabase-PostgreSQL-3ECF8E)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT-412991)

<br>

🚀 **Live API:** https://movie-project-fast-api.onrender.com/docs

📂 **GitHub Repository:** https://github.com/ErikBobko/movie_project_fast_api

🖥️ **Live Dashboard:** Coming soon
</div>

---

## Overview

Movie Analytics Dashboard is an end-to-end data application that downloads movie data from the TMDB API, transforms it, stores it in a PostgreSQL database hosted on Supabase, exposes it through a FastAPI backend and presents the results in an interactive Streamlit dashboard.

The application also includes AI-powered movie recommendations. A natural-language request is converted into structured filters, the application searches its own Supabase database, and AI generates a short explanation for each recommendation.

<p align="center">
  <img src="docs/screenshots/dashboard.png" alt="Movie Analytics Dashboard" width="100%">
</p>

## ✨ Features

<table>
<tr>

<td width="50%">

### 📊 Analytics Dashboard

- Interactive KPIs
- Movie statistics
- Genre distribution
- Rating analysis
- Popularity metrics

</td>

<td width="50%">

### 🔍 Movie Search

- Search by title
- Pagination support
- Movie details
- Similar movie recommendations
- Optimized database queries

</td>

</tr>

<tr>

<td width="50%">

### 🎭 Actor Analytics

- Top actors by movie count
- Highest-rated actors
- Most popular actors
- Interactive charts
- Actor profiles & filmography

</td>

<td width="50%">

### 🤖 AI Recommendations

- Natural language movie search
- GPT-powered filter extraction
- Database-driven recommendations
- AI-generated explanations
- Personalized movie suggestions

</td>

</tr>

<tr>

<td width="50%">

### ⚡ FastAPI Backend

- REST API
- Interactive Swagger documentation
- Pagination
- Filtering
- Production deployment

</td>

<td width="50%">

### 🗄️ Database

- Supabase PostgreSQL
- Normalized relational schema
- Many-to-many relationships
- TMDB ETL pipeline
- Automatic data synchronization

</td>

</tr>

</table></table>

## 🏗️ Architecture

```mermaid
flowchart TD

A[TMDB API]
B[Data Ingestion Pipeline]
C[Data Transformation]
D[(Movie Database<br/>Supabase PostgreSQL)]

E[FastAPI Backend]

F[Swagger API Docs]
G[Streamlit Dashboard]

H[OpenAI GPT]
I[Recommendation Engine]

A --> B
B --> C
C --> D

D --> E

E --> F
E --> G

G --> H
H --> I
I --> D
D --> I
I --> G
```