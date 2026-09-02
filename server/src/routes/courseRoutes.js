import express from 'express';
import Course from '../models/Course.js';
import { protect } from '../middleware/auth.js';
import { logEvent } from '../utils/events.js';

const router = express.Router();

const DEFAULT_COURSES = [
  {
    _id: 'mod-1-db',
    title: 'Module 1: Foundations of Neurodiversity & Strength-Based Mentorship',
    description: 'Learn fundamental strategies for mentoring children on the Autism Spectrum, ADHD, and sensory processing differences.',
    category: 'Inclusive Education',
    level: 'Foundational',
    accent: 'indigo',
    lessons: [
      {
        _id: 'sub-1-1-db',
        title: 'Submodule 1.1: Understanding Neurodiversity & Strength-Based Mentoring',
        summary: 'Shift from a deficit model to a strength-based approach when supporting neurodivergent mentees.',
        content: `Neurodiversity recognizes that brain differences are natural human variations. Companions move away from fixing behavior to building strengths.`,
        videoUrl: 'https://vjs.zencdn.net/v/oceans.mp4',
        durationMinutes: 15,
        order: 1,
        led: {
          videoUrl: 'https://vjs.zencdn.net/v/oceans.mp4',
          transcript: 'Neurodiversity recognizes that brain differences are natural human variations.',
          reflectionSpots: [
            { timestampSeconds: 45, prompt: 'Pause & Reflect: How does a strength-based approach build rapport?' }
          ]
        },
        lbd: {
          mcqs: [
            {
              question: 'What is the primary goal of strength-based mentoring?',
              choices: [
                'Forcing masking of neurotypical behaviors',
                'Building upon unique interests while providing sensory accommodations',
                'Keeping rigid timelines without flexibility',
                'Preventing non-verbal communication aids'
              ],
              correctIndex: 1,
              feedbacks: ['Incorrect.', 'Correct!', 'Incorrect.', 'Incorrect.']
            }
          ],
          subjectives: [
            {
              prompt: 'How would you modify your tone if a mentee shows signs of sensory overload?',
              exemplarAnswer: 'Author Exemplar Answer: Lower voice tone, reduce background noise/bright lighting, pause task, offer a quiet break.'
            }
          ]
        },
        lxt: [
          { title: 'LxT Extension Trajectory: Assistive Tech Case Analysis', url: 'https://media.w3.org/2010/05/sintel/trailer.mp4', extraType: 'video' }
        ],
        lxi: {
          question: 'Share a strategy you have used to build rapport with a mentee who communicates non-verbally.'
        }
      },
      {
        _id: 'sub-1-2-db',
        title: 'Submodule 1.2: Visual Schedules & Structured Predictability',
        summary: 'Using visual prompts, PECS, and structured routines to reduce anxiety.',
        content: `Predictability creates psychological safety for neurodivergent children.`,
        videoUrl: 'https://media.w3.org/2010/05/sintel/trailer.mp4',
        durationMinutes: 18,
        order: 2,
        led: {
          videoUrl: 'https://media.w3.org/2010/05/sintel/trailer.mp4',
          transcript: 'Structuring sessions with visual cues empowers mentees.',
          reflectionSpots: [
            { timestampSeconds: 60, prompt: 'Reflection: Why are transition warnings crucial?' }
          ]
        },
        lbd: {
          mcqs: [
            {
              question: 'Why are visual schedules effective?',
              choices: [
                'They reduce cognitive load and set predictable expectations',
                'They replace companion interaction',
                'They make sessions longer',
                'They are only for non-readers'
              ],
              correctIndex: 0,
              feedbacks: ['Correct!', 'Incorrect.', 'Incorrect.', 'Incorrect.']
            }
          ],
          subjectives: []
        },
        lxt: [],
        lxi: {
          question: 'How can companions effectively co-create visual agendas?'
        }
      }
    ]
  },
  {
    _id: 'mod-2-db',
    title: 'Module 2: Behavioral Support & De-escalation Techniques',
    description: 'Master de-escalation, sensory regulation, and positive reinforcement strategies for companions.',
    category: 'Mentorship Skills',
    level: 'Intermediate',
    accent: 'emerald',
    lessons: [
      {
        _id: 'sub-2-1-db',
        title: 'Submodule 2.1: Differentiating Meltdowns vs. Tantrums & Co-regulation',
        summary: 'Understanding sensory meltdowns and practicing calm co-regulation.',
        content: `A sensory meltdown is an involuntary response to sensory or emotional overload.`,
        videoUrl: 'https://vjs.zencdn.net/v/oceans.mp4',
        durationMinutes: 20,
        order: 1,
        led: {
          videoUrl: 'https://vjs.zencdn.net/v/oceans.mp4',
          transcript: 'Co-regulation means using your calm presence to help a mentee regain balance.',
          reflectionSpots: [
            { timestampSeconds: 50, prompt: 'Reflection: Why is verbal reasoning ineffective during a meltdown?' }
          ]
        },
        lbd: {
          mcqs: [
            {
              question: 'What is the companion’s primary role during a meltdown?',
              choices: [
                'Ensuring physical safety, reducing stimulation, and maintaining calm presence',
                'Demanding verbal explanations',
                'Imposing strict penalties',
                'Crowding around the child'
              ],
              correctIndex: 0,
              feedbacks: ['Correct!', 'Incorrect.', 'Incorrect.', 'Incorrect.']
            }
          ],
          subjectives: []
        },
        lxt: [],
        lxi: {
          question: 'What self-care or grounding techniques help companions stay calm?'
        }
      }
    ]
  }
];

router.get('/', protect, async (req, res, next) => {
  try {
    let courses = await Course.find().select('title description category level accent lessons');
    if (!courses || courses.length === 0) {
      try {
        await Course.insertMany(DEFAULT_COURSES.map(({ _id, lessons, ...rest }) => ({
          ...rest,
          lessons: lessons.map(({ _id, ...lRest }) => lRest)
        })));
        courses = await Course.find().select('title description category level accent lessons');
      } catch (seedErr) {
        return res.json(DEFAULT_COURSES);
      }
    }
    res.json(courses);
  } catch (e) {
    res.json(DEFAULT_COURSES);
  }
});

router.get('/:courseId', protect, async (req, res, next) => {
  try {
    const course = await Course.findById(req.params.courseId);
    if (!course) {
      const defaultCourse = DEFAULT_COURSES.find(c => c._id === req.params.courseId) || DEFAULT_COURSES[0];
      return res.json(defaultCourse);
    }
    res.json(course);
  } catch (e) {
    const defaultCourse = DEFAULT_COURSES.find(c => c._id === req.params.courseId) || DEFAULT_COURSES[0];
    res.json(defaultCourse);
  }
});

router.get('/:courseId/lessons/:lessonId', protect, async (req, res, next) => {
  try {
    const course = await Course.findById(req.params.courseId);
    const lesson = course?.lessons.id(req.params.lessonId);
    if (!lesson) {
      const defaultCourse = DEFAULT_COURSES[0];
      const defaultLesson = defaultCourse.lessons[0];
      return res.json({ course: { id: defaultCourse._id, title: defaultCourse.title }, lesson: defaultLesson });
    }
    res.json({ course: { id: course.id, title: course.title }, lesson });
  } catch (e) {
    const defaultCourse = DEFAULT_COURSES[0];
    const defaultLesson = defaultCourse.lessons[0];
    res.json({ course: { id: defaultCourse._id, title: defaultCourse.title }, lesson: defaultLesson });
  }
});

export default router;
