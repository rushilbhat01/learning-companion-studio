# WEEKLY PROJECT MEETING MINUTES (MoM)


## Project Information

| Field | Details |
| :--- | :--- |
| Project Name | Learning Companion Studio |
| Client Name | InclusiveMinds Learning Collective (IMLC) |
| Meeting Number | 06 |
| Date | October 9, 2026 |
| Time | 10:00 AM – 10:30 AM IST |
| Duration | 30 Minutes |
| Meet Link | https://meet.google.com/bsk-btbh-vvm |


## 1. Attendees


### Client Team

| Name | Role | Present |
| :--- | :--- | :--- |
| Prof. Sridhar | Client Coordinator / Lead | ☑ |
| Farah | Content Author | ☑ |
| Jamson | Experienced Learning Companion | ☑ |


### Student Team

| Name | Present |
| :--- | :--- |
| Rushil | ☑ |
| Aniruddha | ☑ |
| Sahil | ☑ |
| Saksham | ☑ |


## 2. Agenda

☑ Review previous action items

☑ Progress update

☑ Requirement discussion

☑ Prototype demonstration

☑ Risks and issues

☑ Timeline and milestones

☐ Other


## 3. Progress Since Last Meeting


### Completed

* Delivered all 8 action items from the September 4 meeting: full mobile responsiveness, "Save as Draft" authoring workflow, module edit/delete controls, PDF documents with reading checkpoints, LxI stale-response reset, module-scoped LxI, optional/removable videos, and the Admin monitoring dashboard.
* Redesigned the Authoring Studio with an interactive curriculum tree, live hosted snapshot, student draft preview, and a pre-flight publish confirmation.
* Fixed the LxT reflections unlock freeze and the missing video player container in the companion view.

### In Progress

* End-to-end testing of the companion learning flow across video and PDF modules before final hand-over.

### Planned Before Next Meeting

* Add a full-stack backend for persistent storage of courses and companion attempts, with a live online/offline status indicator.
* Implement the login option so companions, authors, and admins access their own views.
* Integrate the official YouTube IFrame API for reliable play/pause, progress tracking, and in-video checkpoints.
* Make PDF embedding resilient (self-contained PDF) and add a sample de-escalation guide as demo content.
* Enforce strict submodule completion: all videos watched, PDFs read, and questions answered before the master quiz unlocks.
* Remove the "Simulate LC Retry" demo button from the Admin Dashboard.
* Add a show/hide password toggle on the login and signup forms.
* Deploy the final production build and share the live link with IMLC.
* All final changes to be completed by October 16, 2026.


## 4. Requirement Changes

| Requirement | Status | Reason |
| :--- | :--- | :--- |
| Persistent Backend Storage | ☑ Added ☐ Modified ☐ Removed ☐ Deferred | Course content and companion attempts were stored only in the browser; data must persist on a server so admins see real attempts from every device. |
| Login Option | ☑ Added ☐ Modified ☐ Removed ☐ Deferred | Each user must sign in so that progress, authoring rights, and admin access are tied to the correct role. |
| Reliable Video Playback (YouTube IFrame API) | ☐ Added ☑ Modified ☐ Removed ☐ Deferred | Videos occasionally failed to pause at checkpoints; the official API is needed for accurate pause, play, and progress tracking. |
| Strict Completion Gating for Master Quiz | ☐ Added ☑ Modified ☐ Removed ☐ Deferred | Companions could reach the master quiz without finishing all videos, PDFs, and questions in a submodule. |
| Remove Demo Simulation Button | ☐ Added ☐ Modified ☑ Removed ☐ Deferred | The "Simulate LC Retry" button was only for testing and should not appear in the final admin dashboard. |
| Show/Hide Password Toggle | ☑ Added ☐ Modified ☐ Removed ☐ Deferred | Companions on mobile phones mistype passwords often; a visibility toggle reduces failed logins. |


## 5. Key Discussions

Discussion 1

Topic: Review of September 4 Deliverables

Summary: The student team demonstrated all 8 requested items on the staging site: mobile layout, draft mode, module edit/delete, PDF checkpoints, module-scoped LxI with reset, optional videos, and the admin dashboard. The client team tested the flows live.

Outcome: The client team was satisfied with the delivered features and confirmed that no new major modules are required. Only final changes remain before hand-over.

Discussion 2

Topic: Data Persistence and Login

Summary: Prof. Sridhar noted that attempts and course edits were saved only in the browser, so the admin dashboard could not show real data from companions on other devices. He asked for proper sign-in and server-side storage.

Outcome: Agreed to add a backend for courses and attempts, a login option for all roles, and a visible online/offline indicator so users know when data is syncing.

Discussion 3

Topic: Video Reliability and Completion Gating

Summary: Jamson reported that videos sometimes did not pause at checkpoints and that the master quiz could be opened without completing every item in a submodule.

Outcome: Agreed to move to the official YouTube IFrame API and to strictly gate the master quiz behind completion of all videos, PDFs, and questions.

Discussion 4

Topic: Final Polish and Deployment

Summary: Farah asked for the demo-only "Simulate LC Retry" button to be removed from the admin dashboard, and for a show/hide password option on the login screen. The client also asked for a stable PDF demo document.

Outcome: Agreed to complete these final changes and deploy the production build by October 16, 2026.


## 6. Decisions Made

| Decision | Proposed By | Agreed By | Rationale |
| :--- | :--- | :--- | :--- |
| Add Backend Persistence for Courses & Attempts | Prof. Sridhar | Student Team | Admins need real companion data across devices, not browser-only storage. |
| Introduce Login for All Roles | Prof. Sridhar | Student Team | Ties progress and permissions to the correct user and role. |
| Switch to Official YouTube IFrame API | Jamson | Student Team | Ensures checkpoints pause the video reliably and progress is tracked accurately. |
| Strict Gating Before Master Quiz | Prof. Sridhar | Student Team | Guarantees companions complete all learning items before certification. |
| Remove Demo Simulation Button | Farah | Student Team | Keeps the final admin dashboard clean and production-ready. |
| Add Show/Hide Password Toggle | Farah | Student Team | Reduces login errors for companions on mobile phones. |
| Final Delivery Target: October 16, 2026 | Prof. Sridhar | Student Team | All final changes and production deployment must be complete before hand-over. |


## 7. Open Questions / Clarifications Needed

| Question | Owner | Follow-up |
| :--- | :--- | :--- |
| Which hosting platform should be used for the final production deployment? | Student Team | Deploy on Vercel and share the live link with the client team. |


## 8. Risks & Issues

| Risk / Issue | Impact | Owner | Mitigation |
| :--- | :--- | :--- | :--- |
| Data loss when the backend server is unreachable | Medium | Student Team | Keep a local storage fallback and show an online/offline indicator so data syncs once the server is back. |


## 9. Action Items

| Action Item | Owner | Due Date |
| :--- | :--- | :--- |
| 1. Backend persistence for courses and attempts with online/offline indicator | Student Team | October 16, 2026 |
| 2. Login option for companions, authors, and admins | Student Team | October 16, 2026 |
| 3. Official YouTube IFrame API integration with in-video checkpoints | Student Team | October 16, 2026 |
| 4. Resilient PDF embedding and sample de-escalation guide | Student Team | October 16, 2026 |
| 5. Strict submodule completion gating before master quiz | Student Team | October 16, 2026 |
| 6. Remove "Simulate LC Retry" demo button from Admin Dashboard | Student Team | October 16, 2026 |
| 7. Show/hide password toggle on login and signup | Student Team | October 16, 2026 |
| 8. Production deployment and live link shared with IMLC | Student Team | October 16, 2026 |


## 10. Next Meeting

Date: October 16, 2026

Time: 10:00 am IST

Agenda: Final demonstration of the production build (backend persistence, login, YouTube checkpoints, strict gating, password toggle) and project hand-over.


## Client Feedback

| Statement | 1 | 2 | 3 | 4 | 5 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| The students understood my requirements. | ☐ |  |  |  | ☑ |
| I am satisfied with today's discussion. | ☐ |  |  |  | ☑ |
| We reached an agreement on the important decisions. | ☐ |  |  |  | ☑ |
| I am confident in the team's direction. | ☐ |  |  |  | ☑ |

CLIENT SIGNATURE

|  |
| :--- |

==================================================

==================================================

==================================================


## Student Reflection

Student Name: Rushil

Rate the following from 1 (Strongly Disagree) to 5 (Strongly Agree).

| Statement | 1 | 2 | 3 | 4 | 5 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| I understand the client's problem better after today's meeting. | ☐ |  |  |  | ☑ |
| Our team has a shared understanding of the project goals. | ☐ |  |  |  | ☑ |
| We reached consensus on the important decisions. | ☐ |  |  |  | ☑ |
| The project requirements are clearer after today's meeting. | ☐ |  |  |  | ☑ |
| I know what needs to be done before the next meeting. | ☐ |  |  |  | ☑ |
| The client understood our suggestions. | ☐ |  |  |  | ☑ |


## C. Reflection

To be filled by each member copy paste responses below

1. What was the biggest misunderstanding that was resolved today?
We assumed browser storage was enough for the prototype, but the client clarified that admins need real attempt data from every companion's device, which requires a backend and login.

2. What remains unclear?
Whether the client will host the production build themselves or continue on our deployment after hand-over.

3. What was the most important decision made today?
Freezing the scope to the final changes and committing to deliver them by October 16, 2026.

4. Did the client's expectations change during today's meeting?

☑ Yes

☐ No

If yes, explain.
The client added backend persistence and login as final requirements for a production-ready hand-over.

5. How much did your understanding of the project change after today's meeting?

☐ Not at all

☐ Slightly

☑ Moderately

☐ Significantly

☐ Completely

Brief explanation:
Understood that the platform must work as a real multi-user system rather than a single-browser prototype.

_________________________________


## Student Reflection

Student Name: Aniruddha

Rate the following from 1 (Strongly Disagree) to 5 (Strongly Agree).

| Statement | 1 | 2 | 3 | 4 | 5 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| I understand the client's problem better after today's meeting. | ☐ |  |  |  | ☑ |
| Our team has a shared understanding of the project goals. | ☐ |  |  |  | ☑ |
| We reached consensus on the important decisions. | ☐ |  |  |  | ☑ |
| The project requirements are clearer after today's meeting. | ☐ |  |  |  | ☑ |
| I know what needs to be done before the next meeting. | ☐ |  |  |  | ☑ |
| The client understood our suggestions. | ☐ |  |  |  | ☑ |


## C. Reflection

To be filled by each member copy paste responses below

1. What was the biggest misunderstanding that was resolved today?
The checkpoint pausing issue was caused by our custom video handling; the client confirmed reliability matters more than custom controls, so we will use the official YouTube IFrame API.

2. What remains unclear?
How to handle companions who close the browser midway through a video checkpoint.

3. What was the most important decision made today?
Moving to the official YouTube IFrame API for reliable checkpoints.

4. Did the client's expectations change during today's meeting?

☑ Yes

☐ No

If yes, explain.
The client asked for more reliable video checkpoints and strict completion gating.

5. How much did your understanding of the project change after today's meeting?

☐ Not at all

☑ Slightly

☐ Moderately

☐ Significantly

☐ Completely

Brief explanation:
Most requirements were already clear; this meeting refined video reliability and gating.

_________________________________


## Student Reflection

Student Name: Sahil

Rate the following from 1 (Strongly Disagree) to 5 (Strongly Agree).

| Statement | 1 | 2 | 3 | 4 | 5 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| I understand the client's problem better after today's meeting. | ☐ |  |  |  | ☑ |
| Our team has a shared understanding of the project goals. | ☐ |  |  |  | ☑ |
| We reached consensus on the important decisions. | ☐ |  |  |  | ☑ |
| The project requirements are clearer after today's meeting. | ☐ |  |  |  | ☑ |
| I know what needs to be done before the next meeting. | ☐ |  |  |  | ☑ |
| The client understood our suggestions. | ☐ |  |  |  | ☑ |


## C. Reflection

To be filled by each member copy paste responses below

1. What was the biggest misunderstanding that was resolved today?
We thought the master quiz could unlock after watching videos only, but the client wants every video, PDF, and question completed first.

2. What remains unclear?
Whether partially read PDFs should count towards submodule completion.

3. What was the most important decision made today?
Strictly gating the master quiz behind full submodule completion.

4. Did the client's expectations change during today's meeting?

☑ Yes

☐ No

If yes, explain.
Completion rules for the master quiz were made stricter.

5. How much did your understanding of the project change after today's meeting?

☐ Not at all

☑ Slightly

☐ Moderately

☐ Significantly

☐ Completely

Brief explanation:
Clarified the exact completion rules companions must satisfy before certification.

_________________________________


## Student Reflection

Student Name: Saksham

Rate the following from 1 (Strongly Disagree) to 5 (Strongly Agree).

| Statement | 1 | 2 | 3 | 4 | 5 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| I understand the client's problem better after today's meeting. | ☐ |  |  |  | ☑ |
| Our team has a shared understanding of the project goals. | ☐ |  |  |  | ☑ |
| We reached consensus on the important decisions. | ☐ |  |  |  | ☑ |
| The project requirements are clearer after today's meeting. | ☐ |  |  |  | ☑ |
| I know what needs to be done before the next meeting. | ☐ |  |  |  | ☑ |
| The client understood our suggestions. | ☐ |  |  |  | ☑ |


## C. Reflection

To be filled by each member copy paste responses below

1. What was the biggest misunderstanding that was resolved today?
The admin dashboard still showed a demo simulation button that the client found confusing; it should be removed for the final version.

2. What remains unclear?
Which login credentials will be shared with the IMLC team for the final demo.

3. What was the most important decision made today?
Setting October 16, 2026 as the final delivery date for all remaining changes.

4. Did the client's expectations change during today's meeting?

☐ Yes

☑ No

If yes, explain.


5. How much did your understanding of the project change after today's meeting?

☐ Not at all

☑ Slightly

☐ Moderately

☐ Significantly

☐ Completely

Brief explanation:
The meeting mainly confirmed final polish items such as the password toggle and admin cleanup.

_________________________________
