# Learning Companion Studio (LCS v2.0)

> 🌐 **[Project Introduction Page (For Non-Technical Visitors)](https://learning-companion-studio.vercel.app/about.html)** — *Start here for a visual, plain-language overview of the educational problem, target users, and how Learning Companion Studio works.*
>
> 🚀 **[Launch Live Application](https://learning-companion-studio.vercel.app)**

---

## 1. Overview & Purpose

**Learning Companion Studio (LCS)** is an interactive training and curriculum authoring platform built for the **InclusiveMinds Learning Collective (IMLC)** under *ET 617: Educational Application Development (Group 12)*.

IMLC trains adult **Learning Companions** (volunteers, tutors, and special-education aides) who mentor neurodivergent children (Autism Spectrum, ADHD, and sensory processing differences). Traditional training relies on passive, lengthy videos and dense PDFs that are easily skimmed without building real-world classroom readiness.

LCS solves this by turning passive training materials into **step-by-step interactive lessons** grounded in the **Learner-Centric MOOC (LCM)** pedagogical framework:
- **In-Video & Reading Checkpoints (LeD / LbD):** Videos automatically pause at critical timestamps and reading guides are broken into sequential milestones with non-skippable scenario questions and instant explanatory feedback.
- **Extension Trajectories (LxT):** Curated deep-dive resources and clinical protocols.
- **Module-Scoped Peer Reflection (LxI):** Companions submit their own classroom de-escalation reflections before unlocking peer responses.
- **Strict Mastery Gating:** The end-of-module certification quiz remains locked until 100% of videos, PDF milestones, and checkpoints are completed.

---

## 2. Target Users

| User Role | Who They Are | How They Use LCS |
| :--- | :--- | :--- |
| **Learning Companions** | Volunteers, resource teachers, and parents supporting neurodivergent children | Complete mobile-friendly video and PDF lessons, answer in-situ checkpoints, share peer reflections, and pass module master quizzes. |
| **Content Authors** | IMLC curriculum designers and lead trainers | Create and manage modules/submodules, upload PDFs or link YouTube videos, pin timestamped checkpoints, save drafts, and publish live without writing code. |
| **Coordinators / Admins** | Supervisors overseeing companion readiness | Track per-companion attempt accuracy, identify high-friction questions, and export diagnostic CSV reports before field placement. |

---

## 3. How to Access the Application

### A. Live Web Application (No Installation Required)
1. **Project Introduction Landing Page:** [https://learning-companion-studio.vercel.app/about.html](https://learning-companion-studio.vercel.app/about.html)
2. **Live Application:** [https://learning-companion-studio.vercel.app](https://learning-companion-studio.vercel.app)

#### Demo Login Credentials:
* **Learning Companion (Trainee):** Click **Sign Up** on the login screen to create a companion account in seconds, or sign in with any registered trainee profile.
* **Course Author & Admin Portal:**
  * **Email:** `author@imlc.org`
  * **Password:** `Author@IMLC2026`
  *(Signing in as the Lead Author unlocks the top switcher to toggle between **Companion View**, **Authoring Desk**, and **Admin Dashboard**).*

---

### B. Running the Application Locally

#### Prerequisites
* **Node.js** (v18+ recommended) and **npm**

#### Steps
```bash
# 1. Clone the repository
git clone https://github.com/EAD-Labs/Group-12_2026.git
cd Group-12_2026

# 2. Install frontend and backend dependencies
npm run install:all

# 3. Start the backend API server (runs on http://localhost:5050)
npm run server

# 4. In a second terminal, start the frontend dev server (runs on http://localhost:5173)
npm run client
```
*Note: You can also open `docs/index.html` (or `docs/about.html` for the introduction page) directly in any modern browser with full local storage fallback.*

---

## 4. Repository Structure

* [`docs/about.html`](docs/about.html) — Non-technical Project Introduction Webpage (also served at `/about.html`).
* [`client/`](client) — Frontend application (`index.html`, React/Vite configuration, and static assets in `client/public/`).
* [`server/`](server) — Node.js + Express REST API (`server/src/server.js`) with JSON persistence (`server/data/`) for courses, drafts, and companion quiz attempts.
* [`docs/`](docs) — High-Level Design (HLD) contract, Weekly Meeting Minutes (MoMs), A0 presentation poster, and standalone deployable builds.

---

## 5. Project Team & Mentors

* **Student Team (Group 12):** Rushil Bhat, Aniruddha Shelke, Saksham Bhadani, Sahil Ghotekar
* **Client Partner:** InclusiveMinds Learning Collective (IMLC) — Prof. Sridhar Iyer (Client Coordinator / Lead), Farah (Content Lead), Jamson (Experienced Learning Companion)
* **Course:** ET 617 — Educational Application Development, Department of Educational Technology, IIT Bombay (2026)
