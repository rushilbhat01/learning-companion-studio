import 'dotenv/config';
import { connectDatabase } from '../config/db.js';
import User from '../models/User.js';
import Course from '../models/Course.js';

await connectDatabase();
await Promise.all([User.deleteMany(), Course.deleteMany()]);
const admin = await User.create({ name: 'Platform Admin', email: 'admin@learningcompanion.studio', passwordHash: await User.hashPassword('AdminPass123!'), role: 'admin' });
const learner = await User.create({ name: 'Harvey Learner', email: 'companion@learningcompanion.studio', passwordHash: await User.hashPassword('LearnerPass123!') });

const coursesData = [
  {
    title: 'Introduction to Machine Learning',
    description: 'Build a confident foundation in the concepts behind modern machine learning.',
    category: 'Data Science',
    level: 'Beginner',
    accent: 'indigo',
    lessons: [
      { 
        title: 'What is Machine Learning?', 
        summary: 'The key idea: learn patterns from examples.', 
        content: 'Machine learning is a way to build systems that improve their predictions by finding patterns in data. Instead of writing a fixed rule for every situation, we show a model examples and evaluate how well it generalises to new data.', 
        videoUrl: 'https://www.youtube.com/embed/f_uwKZIAeM0', 
        durationMinutes: 12, 
        order: 1,
        led: {
          videoUrl: 'https://www.youtube.com/embed/f_uwKZIAeM0',
          transcript: 'Welcome to Machine Learning! Machine learning enables systems to learn from data examples.',
          reflectionSpot: { timestampSeconds: 45, prompt: 'How does learning from examples differ from hardcoded rules?' }
        },
        lbd: {
          mcqs: [
            {
              question: 'What is the key idea behind machine learning?',
              choices: ['Hardcoding rules for every situation', 'Learning patterns from examples', 'Deleting databases to free up space', 'Manually designing webpage graphics'],
              correctIndex: 1,
              feedbacks: [
                'Incorrect. Hardcoding rules is traditional programming, not machine learning.',
                'Correct! Machine learning algorithms automatically learn patterns from data examples.',
                'Incorrect. Database deletion is unrelated to pattern recognition.',
                'Incorrect. Graphic design is a creative manual process.'
              ]
            }
          ],
          subjective: {
            prompt: 'Explain in your own words why machine learning models require separate training and evaluation datasets.',
            exemplarAnswer: 'Exemplar: Evaluation datasets test generalisation to unseen data. If we evaluate on training data, the model might just memorize it (overfitting) without learning true patterns.'
          }
        },
        lxt: [
          { title: 'Interactive ML Visualization Tool (Teachable Machine)', url: 'https://teachablemachine.withgoogle.com/', resourceType: 'link' }
        ],
        lxi: {
          weeklyFocusPrompt: 'Discuss with your peer companion: Give an example of a daily app you use that relies on Machine Learning.'
        }
      },
      { title: 'Supervised Learning', summary: 'Learning with labelled examples.', content: 'In supervised learning, every training example includes an input and the correct answer. A spam filter learns from emails that have already been labelled spam or not spam. Classification predicts categories; regression predicts numeric values.', videoUrl: 'https://www.youtube.com/embed/VwVg9jCtqaU', durationMinutes: 16, order: 2 },
      { title: 'Measuring Model Quality', summary: 'Use metrics that match the problem.', content: 'Accuracy is useful when classes are balanced. Precision, recall and F1 score tell a richer story when errors have different costs. Always evaluate with data that was not used to train the model.', videoUrl: 'https://www.youtube.com/embed/85dtiMz9tSo', durationMinutes: 14, order: 3 }
    ]
  },
  {
    title: 'React for Beginners',
    description: 'Learn the fundamentals of React, the most popular library for building user interfaces.',
    category: 'Web Development',
    level: 'Beginner',
    accent: 'blue',
    lessons: [
      { title: 'What is React?', summary: 'Introduction to React and components.', content: 'React is a library for building user interfaces. It lets you compose complex UIs from small and isolated pieces of code called components.', videoUrl: 'https://www.youtube.com/embed/bMknfKXIFA8', durationMinutes: 10, order: 1 },
      { title: 'Components and Props', summary: 'Passing data between components.', content: 'Components are like JavaScript functions. They accept arbitrary inputs (called "props") and return React elements describing what should appear on the screen.', videoUrl: 'https://www.youtube.com/embed/Y2hgEGPzTZY', durationMinutes: 15, order: 2 },
      { title: 'State and Hooks', summary: 'Managing state in functional components.', content: 'State allows React components to change their output over time in response to user actions, network responses, and anything else. Hooks let you use state and other React features without writing a class.', videoUrl: 'https://www.youtube.com/embed/O6P86uwfdR0', durationMinutes: 18, order: 3 }
    ]
  },
  {
    title: 'Backend Basics with Node.js',
    description: 'Understand how to build scalable backend applications using Node.js and Express.',
    category: 'Backend',
    level: 'Intermediate',
    accent: 'emerald',
    lessons: [
      { title: 'Introduction to Node.js', summary: 'What is Node.js and why use it?', content: 'Node.js is a JavaScript runtime built on Chrome\'s V8 JavaScript engine. It allows you to run JavaScript on the server side.', videoUrl: 'https://www.youtube.com/embed/ENrzD9HAZK4', durationMinutes: 12, order: 1 },
      { title: 'Building APIs with Express', summary: 'Creating RESTful APIs easily.', content: 'Express is a minimal and flexible Node.js web application framework that provides a robust set of features for web and mobile applications.', videoUrl: 'https://www.youtube.com/embed/L72fhGm1tfE', durationMinutes: 20, order: 2 },
      { title: 'Database Integration', summary: 'Connecting your app to a database.', content: 'Most backend applications need to store data persistently. You can connect Node.js apps to various databases like MongoDB, PostgreSQL, and MySQL.', videoUrl: 'https://www.youtube.com/embed/f2EqECiTBL8', durationMinutes: 16, order: 3 }
    ]
  }
];

const mlQuizzes = [
  { lessonIndex: 0, questions: [
    { prompt: 'What is the key idea behind machine learning?', options: ['Hardcoding rules for every situation', 'Learning patterns from examples', 'Deleting databases to free up space', 'Manually designing webpage graphics'], answer: 1 },
    { prompt: 'A model is evaluated based on how well it generalises to...', options: ['Old training data', 'Empty variables', 'New unseen data', 'The source code'], answer: 2 }
  ]},
  { lessonIndex: 1, questions: [
    { prompt: 'What distinguishes supervised learning?', options: ['It has labelled examples', 'It never uses data', 'It only predicts images', 'It has no evaluation'], answer: 0 },
    { prompt: 'Which task predicts a numeric value?', options: ['Classification', 'Regression', 'Clustering', 'Ranking'], answer: 1 },
  ]},
  { lessonIndex: 2, questions: [
    { prompt: 'When is accuracy most useful as a metric?', options: ['When data classes are balanced', 'When data classes are highly imbalanced', 'When there are no test labels', 'When precision is zero'], answer: 0 },
  ]}
];

const reactQuizzes = [
  { lessonIndex: 0, questions: [
    { prompt: 'What is React primarily used for?', options: ['Database management', 'Building user interfaces', 'Server-side routing', 'Machine learning'], answer: 1 }
  ]},
  { lessonIndex: 1, questions: [
    { prompt: 'What are props in React?', options: ['Methods to fetch data', 'Arbitrary inputs passed to components', 'Built-in styling objects', 'Functions to update state'], answer: 1 }
  ]},
  { lessonIndex: 2, questions: [
    { prompt: 'Which hook is used to manage state in functional components?', options: ['useEffect', 'useState', 'useContext', 'useReducer'], answer: 1 }
  ]}
];

const nodeQuizzes = [
  { lessonIndex: 0, questions: [
    { prompt: 'What engine does Node.js run on?', options: ['SpiderMonkey', 'V8', 'Chakra', 'JavaScriptCore'], answer: 1 }
  ]},
  { lessonIndex: 1, questions: [
    { prompt: 'What is Express?', options: ['A database', 'A web application framework for Node.js', 'A frontend library', 'A testing tool'], answer: 1 }
  ]},
  { lessonIndex: 2, questions: [
    { prompt: 'Which of the following is a NoSQL database commonly used with Node.js?', options: ['MySQL', 'PostgreSQL', 'MongoDB', 'SQLite'], answer: 2 }
  ]}
];

const quizzesData = [mlQuizzes, reactQuizzes, nodeQuizzes];

for (let i = 0; i < coursesData.length; i++) {
  const course = await Course.create(coursesData[i]);
  course.quizzes = quizzesData[i].map(quiz => ({
    lessonId: course.lessons[quiz.lessonIndex]._id,
    questions: quiz.questions
  }));
  await course.save();
}

console.log(`Seeded ${admin.email} and ${learner.email} and courses with videos`);
process.exit(0);
