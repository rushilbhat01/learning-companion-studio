import 'dotenv/config';
import { connectDatabase } from '../config/db.js';
import User from '../models/User.js';
import Course from '../models/Course.js';

await connectDatabase();
await Promise.all([User.deleteMany(), Course.deleteMany()]);

const admin = await User.create({ 
  name: 'Platform Facilitator', 
  email: 'admin@learningcompanion.studio', 
  passwordHash: await User.hashPassword('AdminPass123!'), 
  role: 'admin' 
});

const learner = await User.create({ 
  name: 'Volunteer Companion', 
  email: 'companion@learningcompanion.studio', 
  passwordHash: await User.hashPassword('LearnerPass123!') 
});

const coursesData = [
  {
    title: 'Module 1: Foundations of Neurodiversity & Inclusive Mentorship',
    description: 'Learn fundamental strategies for mentoring children on the Autism Spectrum, ADHD, and sensory processing differences.',
    category: 'Inclusive Education',
    level: 'Foundational',
    accent: 'indigo',
    lessons: [
      { 
        title: 'Submodule 1.1: Understanding Neurodiversity & Strength-Based Mentoring', 
        summary: 'Shift from a deficit model to a strength-based approach when supporting neurodivergent mentees.', 
        content: `Neurodiversity recognizes that brain differences are natural variations of human cognition. When mentoring neurodivergent children, companions must move away from a deficit model (trying to fix or normalize behavior) to a strength-based model.

Key Principles for Learning Companions:
1. Respect communication preferences (verbal, non-verbal, AAC, or visual cards).
2. Recognize sensory processing differences and environmental triggers.
3. Validate emotional regulation and allow processing time without rushing responses.`, 
        videoUrl: 'https://www.youtube-nocookie.com/embed/RbwrrVILvkg', 
        durationMinutes: 15, 
        order: 1,
        led: {
          videoUrl: 'https://www.youtube-nocookie.com/embed/RbwrrVILvkg',
          transcript: 'Welcome to Inclusive Mentorship Training! In this session, we examine how to recognize diverse cognitive profiles and adapt mentoring techniques for neurodivergent children.',
          reflectionSpots: [
            { timestampSeconds: 45, prompt: 'Pause & Reflect: How does a strength-based mentoring approach differ from traditional deficit-focused instruction?' },
            { timestampSeconds: 120, prompt: 'Checkpoint: Identify two sensory factors in a classroom that might cause overload for an autistic learner.' }
          ]
        },
        lbd: {
          mcqs: [
            {
              question: 'What is the primary goal of strength-based mentoring for neurodivergent mentees?',
              choices: [
                'Forcing the child to mimic neurotypical social behaviors at all times',
                'Identifying and building upon the child’s unique interests while providing sensory accommodations',
                'Ignoring individual learning needs and keeping a rigid strict timeline',
                'Preventing the child from using non-verbal communication aids'
              ],
              correctIndex: 1,
              feedbacks: [
                'Incorrect. Forcing masking causes high anxiety and burnout for neurodivergent children.',
                'Correct! Strength-based mentoring fosters trust, builds confidence, and accommodates individual sensory profiles.',
                'Incorrect. Rigid timelines without flexibility increase overwhelm and frustration.',
                'Incorrect. Non-verbal communication tools (PECS, AAC) should always be encouraged.'
              ]
            }
          ],
          subjectives: [
            {
              prompt: 'Describe how you would modify your mentoring tone and environment if a mentee shows signs of sensory overload during an activity.',
              exemplarAnswer: 'Author Exemplar Answer: I would lower my voice tone, reduce background noise/bright lighting, pause the current task, offer a low-stimulation quiet break, and provide clear visual choices without pressing for immediate verbal explanations.'
            }
          ]
        },
        lxt: [
          { title: 'NPTEL Course: Inclusive Education Practices & Assistive Tech', url: 'https://nptel.ac.in/courses/109106155', extraType: 'link' }
        ],
        lxi: {
          question: 'Discuss with your peer companion: Share a strategy you have used to build rapport with a child who communicates non-verbally.'
        }
      },
      { 
        title: 'Submodule 1.2: Visual Schedules & Structured Predictability', 
        summary: 'Using visual prompts, PECS, and structured routines to reduce anxiety.', 
        content: `Predictability creates psychological safety for neurodivergent children. Using visual schedules, icon cards, and transition warnings helps children anticipate changes and reduces task-switching anxiety.`, 
        videoUrl: 'https://www.youtube-nocookie.com/embed/VwVg9jCtqaU', 
        durationMinutes: 18, 
        order: 2,
        led: {
          videoUrl: 'https://www.youtube-nocookie.com/embed/VwVg9jCtqaU',
          transcript: 'Structuring sessions with clear visual cues empowers mentees to navigate learning tasks with greater independence.',
          reflectionSpots: [
            { timestampSeconds: 60, prompt: 'Reflection: Why are transition warnings (e.g. 5-minute countdown cards) crucial before changing activities?' }
          ]
        },
        lbd: {
          mcqs: [
            {
              question: 'Why are visual schedules effective for children with ADHD or Autism?',
              choices: [
                'They reduce cognitive load and provide clear, predictable expectations',
                'They replace the need for mentor interaction',
                'They make sessions longer and more complicated',
                'They are only useful for non-readers'
              ],
              correctIndex: 0,
              feedbacks: [
                'Correct! Visual schedules lower anxiety by clearly setting expectations and aiding working memory.',
                'Incorrect. Visual schedules enhance companion-mentee collaboration.',
                'Incorrect. Visual schedules simplify transitions and save time.',
                'Incorrect. Visual schedules benefit learners of all reading levels.'
              ]
            }
          ],
          subjectives: [
            {
              prompt: 'How would you prepare a mentee for an unexpected schedule change during a mentoring session?',
              exemplarAnswer: 'Author Exemplar Answer: Use a visual "Change Card", explain the update calmly with visual prompts, highlight what remains unchanged to preserve security, and allow time for the mentee to process the transition.'
            }
          ]
        },
        lxt: [
          { title: 'Visual Schedule Creator Templates', url: 'https://www.autism.org.uk/advice-and-guidance/topics/communication/visual-supports', extraType: 'link' }
        ],
        lxi: {
          question: 'Discuss: How can companions effectively co-create visual session agendas with their mentees?'
        }
      }
    ]
  },
  {
    title: 'Module 2: Behavioral Support & De-escalation Techniques',
    description: 'Master de-escalation, sensory regulation, and positive reinforcement strategies for companions.',
    category: 'Mentorship Skills',
    level: 'Intermediate',
    accent: 'emerald',
    lessons: [
      { 
        title: 'Submodule 2.1: Differentiating Meltdowns vs. Tantrums & Co-regulation', 
        summary: 'Understanding sensory meltdowns and practicing calm co-regulation.', 
        content: `A sensory meltdown is an involuntary response to sensory or emotional overload, unlike a goal-driven behavioral tantrum. Companions must prioritize safety, calm co-regulation, and zero demands during a meltdown.`, 
        videoUrl: 'https://www.youtube-nocookie.com/embed/aircAruvnKk', 
        durationMinutes: 20, 
        order: 1,
        led: {
          videoUrl: 'https://www.youtube-nocookie.com/embed/aircAruvnKk',
          transcript: 'Co-regulation means using your calm presence to help a mentee regain emotional balance when overwhelmed.',
          reflectionSpots: [
            { timestampSeconds: 50, prompt: 'Reflection: Why is asking verbal reasoning questions ineffective during an active sensory meltdown?' }
          ]
        },
        lbd: {
          mcqs: [
            {
              question: 'What is the companion’s primary role during a mentee’s sensory meltdown?',
              choices: [
                'Ensuring physical safety, reducing sensory input, and maintaining a calm presence',
                'Demanding immediate verbal explanations for the behavior',
                'Imposing strict immediate academic penalties',
                'Crowding around the child with multiple loud volunteers'
              ],
              correctIndex: 0,
              feedbacks: [
                'Correct! Safety, calm presence, and reducing stimulation are essential for de-escalation.',
                'Incorrect. Verbal demands overload an already overwhelmed central nervous system.',
                'Incorrect. Penalties during a meltdown increase distress and break trust.',
                'Incorrect. Crowding increases sensory overwhelm.'
              ]
            }
          ],
          subjectives: [
            {
              prompt: 'Draft a post-meltdown recovery plan to help a mentee safely rejoin mentoring activities.',
              exemplarAnswer: 'Author Exemplar Answer: Allow adequate quiet recovery time, offer water or a sensory tool, avoid analyzing the incident immediately, and gently invite the mentee back with a low-pressure preferred activity.'
            }
          ]
        },
        lxt: [
          { title: 'De-escalation Checklist for Learning Companions', url: 'https://nptel.ac.in/courses', extraType: 'link' }
        ],
        lxi: {
          question: 'Discuss: What self-care or grounding techniques help companions stay calm during intense de-escalation?'
        }
      }
    ]
  }
];

const quizzesData = [[], []];

for (let i = 0; i < coursesData.length; i++) {
  const course = await Course.create(coursesData[i]);
  await course.save();
}

console.log(`Seeded ${admin.email} and ${learner.email} with Neurodivergent Mentoring training modules`);
process.exit(0);
