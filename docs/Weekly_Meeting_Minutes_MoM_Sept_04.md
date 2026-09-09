# WEEKLY PROJECT MEETING MINUTES (MoM)


## Project Information

| Field | Details |
| :--- | :--- |
| Project Name | Learning Companion Studio |
| Client Name | InclusiveMinds Learning Collective (IMLC) |
| Meeting Number | 05 |
| Date | September 4, 2026 |
| Time | 10:00 AM – 10:45 AM IST |
| Duration | 45 Minutes |
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

* Demonstrated the unified Author-LC platform on staging environment featuring real-time synchronization between creator uploads and the companion dashboard.
* Successfully built and demonstrated in-video reflection checkpoints (LeD) with mid-video timestamps, automatic video pausing, non-skippable MCQs/subjective reflections, choice feedback, and auto-resumption.

### In Progress

* Cross-device mobile usability testing and authoring workflow evaluations.

### Planned Before Next Meeting

* Implement full mobile responsiveness across phone screens.
* Implement "Save as Draft" functionality in the authoring desk prior to publishing.
* Enable editing and deleting modules in the authoring interface.
* Support PDF documents with checkpoint reflection questions alongside video URLs.
* Fix LxI bug so old responses are cleared when the instructor changes the question.
* Scope LxI inside each individual module rather than maintaining a single global feed.
* Make video optional/removable when uploading a module.
* Build an Admin monitoring dashboard to track companion attempts and scores.
* All tasks to be completed by September 25, 2026.


## 4. Requirement Changes

| Requirement | Status | Reason |
| :--- | :--- | :--- |
| Mobile Phone Responsiveness | ☑ Added ☐ Modified ☐ Removed ☐ Deferred | The website currently does not work on phone viewports; it must be fully responsive and functional on smartphones for field companions. |
| Save as Draft Mode | ☑ Added ☐ Modified ☐ Removed ☐ Deferred | Authors need to save drafts before directly publishing changes to the active companion portal. |
| Module Edit & Deletion | ☑ Added ☐ Modified ☐ Removed ☐ Deferred | Authors must be able to edit module metadata and delete unwanted/outdated modules. |
| Multi-Modal Document (PDF) Support | ☑ Added ☐ Modified ☐ Removed ☐ Deferred | In addition to video URLs, modules should support PDF documents integrated with checkpoint reflection questions. |
| LxI Stale Responses Reset | ☑ Added ☐ Modified ☐ Removed ☐ Deferred | Bug fix: After the instructor updates or changes the LxI question, previous companion responses must be cleared. |
| Module-Scoped LxI | ☑ Added ☐ Modified ☐ Removed ☐ Deferred | LxI peer interaction should be contextual and placed inside each module, rather than being a single detached global question. |
| Optional Video Links | ☑ Added ☐ Modified ☐ Removed ☐ Deferred | Videos should be optional/removable during module creation; modules should not require mandatory video URLs. |
| Admin Monitoring Dashboard | ☑ Added ☐ Modified ☐ Removed ☐ Deferred | Provide an admin dashboard for instructors to monitor companion module attempts, progress, and quiz scores. |


## 5. Key Discussions

Discussion 1

Topic: Mobile Responsiveness & Field Usability

Summary: During client testing of the staging site, Jamson pointed out that the website is not functioning properly on mobile phones. Since learning companions predominantly access training on their smartphones in field settings, mobile compatibility is critical.

Outcome: Agreed that making the entire companion and authoring interface responsive and mobile-friendly is an essential deliverable.

Discussion 2

Topic: Authoring Governance (Drafts, Module Editing & Deleting, Optional Video)

Summary: Farah highlighted authoring workflow constraints: changes currently publish immediately with no draft phase, modules cannot be edited or deleted once created, and every module currently mandates a video URL even when only reading material is intended.

Outcome: The authoring desk will be updated to include a "Save as Draft" state, full module edit/delete capabilities, and optional/removable video links.

Discussion 3

Topic: PDF Documents with Embedded Checkpoints

Summary: The client team requested that in addition to streaming video URLs, modules should accommodate PDF documents, and these PDFs must also contain reflection checkpoint questions to maintain active engagement.

Outcome: The system will be enhanced to support PDF documents accompanied by reflection checkpoint questions.

Discussion 4

Topic: LxI Refinements and Admin Monitoring Dashboard

Summary: Prof. Sridhar noted two key requirements: (1) LxI discussion is currently global and persists previous answers even after the instructor updates the question; it must be scoped inside each module and previous answers cleared upon question change. (2) Instructors need an Admin Dashboard to monitor companion attempts, progress, and scores.

Outcome: Agreed to scope LxI per module, reset answers on prompt change, and build an Admin monitoring dashboard. All 8 items are scheduled for completion by the next meeting on September 25, 2026.


## 6. Decisions Made

| Decision | Proposed By | Agreed By | Rationale |
| :--- | :--- | :--- | :--- |
| Ensure Full Smartphone Compatibility | Jamson | Student Team | Learning companions rely on mobile phones during fieldwork and training sessions. |
| Implement "Save as Draft" before Publishing | Farah | Student Team | Prevents incomplete course edits from prematurely going live to companions. |
| Add Module Edit & Delete Controls | Farah | Student Team | Gives content authors complete lifecycle control over created curricula. |
| Introduce PDF Materials with Checkpoints | Prof. Sridhar | Student Team | Enables multi-modal learning for lessons that do not require video bandwidth. |
| Scope LxI Per Module and Reset on Update | Prof. Sridhar | Student Team | Keeps peer discussions relevant to the specific module and prevents outdated responses from displaying. |
| Make Video Content Optional | Farah | Student Team | Accommodates text-only and document-only training modules. |
| Develop Admin Monitoring Dashboard | Prof. Sridhar | Student Team | Provides instructors with oversight on companion engagement and quiz performance. |
| Fixed Delivery Target: September 25, 2026 | Prof. Sridhar | Student Team | All 8 fixes and enhancements must be fully delivered by the next meeting date. |


## 7. Open Questions / Clarifications Needed

| Question | Owner | Follow-up |
| :--- | :--- | :--- |
| Should admin dashboard metrics be exportable as CSV or viewed entirely within the web UI? | Student Team | Clarify with Prof. Sridhar during development. |


## 8. Risks & Issues

| Risk / Issue | Impact | Owner | Mitigation |
| :--- | :--- | :--- | :--- |
| Delivering 8 distinct functional items by September 25, 2026 | Medium | Student Team | Prioritize mobile layout and draft workflows first, followed by PDF and admin features in Jira. |


## 9. Action Items

| Action Item | Owner | Due Date |
| :--- | :--- | :--- |
| 1. Mobile Responsiveness (ensure full usability on phones) | Student Team | September 25, 2026 |
| 2. Save as Draft mode before directly publishing changes | Student Team | September 25, 2026 |
| 3. Module Management (ability to edit and delete modules) | Student Team | September 25, 2026 |
| 4. PDF Document support with interactive checkpoint questions | Student Team | September 25, 2026 |
| 5. LxI Bug Fix (clear previous responses when question changes) | Student Team | September 25, 2026 |
| 6. Module-Scoped LxI (place LxI inside each module, not global) | Student Team | September 25, 2026 |
| 7. Optional Video (allow video to be removable/optional) | Student Team | September 25, 2026 |
| 8. Admin Dashboard (monitor companion attempts and scores) | Student Team | September 25, 2026 |


## 10. Next Meeting

Date: September 25, 2026

Time: 10:00 am IST

Agenda: Demonstration and review of all 8 implemented fixes and enhancements (mobile UI, draft mode, PDF checkpoints, module-scoped LxI, admin dashboard).


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
We assumed the platform would primarily be accessed via laptops, but the client clarified that companions in the field rely on smartphones, making mobile responsiveness a critical requirement. Furthermore, modules do not always require videos and should support PDFs with reflection checkpoints.

2. What remains unclear?
Whether admin dashboard metrics should support CSV export or remain purely interactive in the web UI.

3. What was the most important decision made today?
Agreeing to implement all 8 identified bugs and enhancements (mobile support, drafts, module editing/deleting, PDF checkpoints, module-scoped LxI, optional videos, admin dashboard) with a firm deadline of September 25, 2026.

4. Did the client's expectations change during today's meeting?

☑ Yes

☐ No

If yes, explain.
The client expanded the requirements beyond video-only learning to include mobile responsiveness, PDF document checkpoints, authoring draft governance, and instructor monitoring.

5. How much did your understanding of the project change after today's meeting?

☐ Not at all

☐ Slightly

☑ Moderately

☐ Significantly

☐ Completely

Brief explanation:
Understood the real-world operational context of field companions on mobile phones and the need for content authors to have draft safety and non-video options.

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
Realized that LxI was detached as a global feed; placing it inside individual modules and clearing previous responses upon question change provides proper pedagogical context.

2. What remains unclear?
The layout design for embedding checkpoint questions into PDF reading materials on small mobile screens.

3. What was the most important decision made today?
Committing to complete all 8 fixes and enhancements by September 25, 2026.

4. Did the client's expectations change during today's meeting?

☑ Yes

☐ No

If yes, explain.
The client requested multi-modal PDF support and an Admin Monitoring Dashboard for instructors.

5. How much did your understanding of the project change after today's meeting?

☐ Not at all

☐ Slightly

☐ Moderately

☑ Significantly

☐ Completely

Brief explanation:
Gained clarity on how instructors track companion progress through an admin dashboard and the necessity of mobile-first styling.

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
Understood that authors need full lifecycle control to edit and delete modules, as well as a "Save as Draft" state before publishing live.

2. What remains unclear?
How draft states should be stored across multiple browser sessions.

3. What was the most important decision made today?
Deciding on the 8 action items due on September 25, 2026.

4. Did the client's expectations change during today's meeting?

☑ Yes

☐ No

If yes, explain.
Authors requested draft governance and module deletion capabilities.

5. How much did your understanding of the project change after today's meeting?

☐ Not at all

☐ Slightly

☑ Moderately

☐ Significantly

☐ Completely

Brief explanation:
Understood the authoring side requirements in greater detail, especially the need for draft states and module management.

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
Clarified the bug where changing the LxI question still left previous companion answers visible in the thread.

2. What remains unclear?
The specific metric indicators required on the admin monitoring overview.

3. What was the most important decision made today?
Setting the unified deadline of September 25, 2026 for all 8 bug fixes and enhancements.

4. Did the client's expectations change during today's meeting?

☑ Yes

☐ No

If yes, explain.
Included admin tracking features and optional video support.

5. How much did your understanding of the project change after today's meeting?

☐ Not at all

☐ Slightly

☑ Moderately

☐ Significantly

☐ Completely

Brief explanation:
Recognized the end-to-end learning lifecycle and how instructor oversight ties into companion learning.

_________________________________
