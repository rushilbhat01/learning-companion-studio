import { useEffect, useState } from 'react';
import { Plus, Save, Trash2, Video, CheckSquare, Link2, MessageSquare, AlertCircle, CheckCircle2 } from 'lucide-react';
import api, { track } from '../api';
import Layout from '../components/Layout';

export default function AuthorDesk() {
  const [courses, setCourses] = useState([]);
  const [selectedCourseId, setSelectedCourseId] = useState('');
  const [selectedLessonId, setSelectedLessonId] = useState('');
  const [activeTab, setActiveTab] = useState('led');
  const [message, setMessage] = useState(null);

  // General Metadata
  const [title, setTitle] = useState('');
  const [summary, setSummary] = useState('');
  const [videoUrl, setVideoUrl] = useState('');
  const [transcript, setTranscript] = useState('');

  // LeD: Multiple Reflection Spots
  const [reflectionSpots, setReflectionSpots] = useState([
    { timestampSeconds: 45, prompt: '', spotType: 'reflection' }
  ]);

  // LbD: Multiple MCQs (Loop)
  const [mcqs, setMcqs] = useState([
    { question: '', choices: ['', '', '', ''], correctIndex: 0, feedbacks: ['', '', '', ''] }
  ]);

  // LbD: Multiple Subjective Questions
  const [subjectives, setSubjectives] = useState([
    { prompt: '', exemplarAnswer: '' }
  ]);

  // LxT: Extra Material List
  const [lxtList, setLxtList] = useState([
    { title: '', url: '', summary: '', extraType: 'link' }
  ]);

  // LxI: Author Question
  const [lxiQuestion, setLxiQuestion] = useState('');

  const DEFAULT_FALLBACK_COURSES = [
    {
      _id: 'mod-1-def',
      title: 'Module 1: Foundations of Neurodiversity & Strength-Based Mentorship',
      description: 'Learn fundamental strategies for mentoring children on the Autism Spectrum, ADHD, and sensory processing differences.',
      level: 'Foundational',
      lessons: [
        {
          _id: 'sub-1-1-def',
          title: 'Submodule 1.1: Understanding Neurodiversity & Strength-Based Mentoring',
          summary: 'Shift from a deficit model to a strength-based approach when supporting neurodivergent mentees.',
          videoUrl: 'https://vjs.zencdn.net/v/oceans.mp4',
          led: { transcript: 'Neurodiversity recognizes that brain differences are natural human variations.', reflectionSpots: [{ timestampSeconds: 45, prompt: 'Pause & Reflect: Strength-based vs deficit mentoring.' }] },
          lbd: { mcqs: [{ question: 'What is the goal of strength-based mentoring?', choices: ['Masking', 'Building on unique strengths', 'Rigid rules', 'No aids'], correctIndex: 1, feedbacks: ['No', 'Yes!', 'No', 'No'] }], subjectives: [] },
          lxt: [],
          lxi: { question: 'Share a strategy for non-verbal mentees.' }
        }
      ]
    },
    {
      _id: 'mod-2-def',
      title: 'Module 2: Behavioral Support & De-escalation Techniques',
      description: 'Master de-escalation, sensory regulation, and positive reinforcement strategies for companions.',
      level: 'Intermediate',
      lessons: [
        {
          _id: 'sub-2-1-def',
          title: 'Submodule 2.1: Meltdowns vs. Tantrums & Co-regulation',
          summary: 'Understanding sensory meltdowns and practicing calm co-regulation.',
          videoUrl: 'https://media.w3.org/2010/05/sintel/trailer.mp4',
          led: { transcript: 'Co-regulation means using your calm presence.', reflectionSpots: [{ timestampSeconds: 50, prompt: 'Why is verbal reasoning ineffective during meltdowns?' }] },
          lbd: { mcqs: [], subjectives: [] },
          lxt: [],
          lxi: { question: 'What grounding techniques help companions stay calm?' }
        }
      ]
    }
  ];

  const fetchCourses = async () => {
    try {
      const r = await api.get('/courses');
      const loaded = (r.data && r.data.length > 0) ? r.data : DEFAULT_FALLBACK_COURSES;
      setCourses(loaded);
      if (loaded.length > 0) setSelectedCourseId(loaded[0]._id);
    } catch (err) {
      setCourses(DEFAULT_FALLBACK_COURSES);
      setSelectedCourseId(DEFAULT_FALLBACK_COURSES[0]._id);
    }
  };

  useEffect(() => {
    fetchCourses();
  }, []);

  const handleCreateCourse = async () => {
    const courseTitle = prompt('Enter New Course / Module Title:', `Module ${courses.length + 1}: New Mentorship Topic`);
    if (!courseTitle) return;
    try {
      const res = await api.post('/author/courses', {
        title: courseTitle,
        description: 'New course description...',
        category: 'Mentorship Skills',
        level: 'Intermediate'
      });
      setMessage({ type: 'success', text: `Created course: ${res.data.title}` });
      await fetchCourses();
      setSelectedCourseId(res.data._id);
    } catch (e) {
      const newCourse = {
        _id: `mod-${Date.now()}`,
        title: courseTitle,
        description: 'New course description...',
        level: 'Intermediate',
        lessons: []
      };
      setCourses([...courses, newCourse]);
      setSelectedCourseId(newCourse._id);
      setMessage({ type: 'success', text: `Created course: ${courseTitle}` });
    }
  };


  const currentCourse = courses.find((c) => c._id === selectedCourseId);

  useEffect(() => {
    if (!currentCourse || !selectedLessonId) return;
    const lesson = currentCourse.lessons?.find((l) => l._id === selectedLessonId);
    if (lesson) {
      setTitle(lesson.title || '');
      setSummary(lesson.summary || '');
      setVideoUrl(lesson.videoUrl || lesson.led?.videoUrl || '');
      setTranscript(lesson.led?.transcript || '');

      setReflectionSpots(lesson.led?.reflectionSpots?.length ? lesson.led.reflectionSpots : [
        { timestampSeconds: 45, prompt: lesson.led?.reflectionSpot?.prompt || '', spotType: 'reflection' }
      ]);

      setMcqs(lesson.lbd?.mcqs?.length ? lesson.lbd.mcqs : [
        { question: '', choices: ['', '', '', ''], correctIndex: 0, feedbacks: ['', '', '', ''] }
      ]);

      setSubjectives(lesson.lbd?.subjectives?.length ? lesson.lbd.subjectives : [
        { prompt: lesson.lbd?.subjective?.prompt || '', exemplarAnswer: lesson.lbd?.subjective?.exemplarAnswer || '' }
      ]);

      setLxtList(lesson.lxt?.length ? lesson.lxt : [
        { title: '', url: '', summary: '', extraType: 'link' }
      ]);

      setLxiQuestion(lesson.lxi?.question || lesson.lxi?.weeklyFocusPrompt || '');
    }
  }, [selectedCourseId, selectedLessonId, currentCourse]);

  const handleSaveLesson = async (e) => {
    e.preventDefault();
    if (!selectedCourseId) return;

    const payload = {
      title,
      summary,
      videoUrl,
      led: {
        videoUrl,
        transcript,
        reflectionSpots: reflectionSpots.filter((s) => s.prompt)
      },
      lbd: {
        mcqs: mcqs.filter((m) => m.question).map((m) => ({
          ...m,
          choices: m.choices.map((c, i) => c || `Option ${i + 1}`),
          feedbacks: m.feedbacks.map((f, i) => f || `Feedback for option ${i + 1}`)
        })),
        subjectives: subjectives.filter((s) => s.prompt)
      },
      lxt: lxtList.filter((x) => x.url || x.title),
      lxi: {
        question: lxiQuestion,
        weeklyFocusPrompt: lxiQuestion
      }
    };

    try {
      if (selectedLessonId) {
        await api.put(`/author/courses/${selectedCourseId}/lessons/${selectedLessonId}`, payload);
        setMessage({ type: 'success', text: 'LCM Lesson & Authoring Content Published!' });
      } else {
        await api.post(`/author/courses/${selectedCourseId}/lessons`, payload);
        setMessage({ type: 'success', text: 'New LCM Lesson Created & Published!' });
      }

      const { data: updatedCourses } = await api.get('/courses');
      setCourses(updatedCourses);

      track('LESSON_AUTHORED', {
        component: 'AuthorDesk',
        eventContext: title,
        resourceType: 'lesson'
      });
    } catch (err) {
      setMessage({ type: 'error', text: err.response?.data?.message || 'Failed to save lesson.' });
    }
  };

  return (
    <Layout>
      <div className="max-w-6xl mx-auto space-y-8">
        <div className="rounded-3xl bg-slate-900 text-white p-8 shadow-xl flex flex-col md:flex-row md:items-center justify-between gap-6">
          <div>
            <span className="text-xs font-bold uppercase tracking-wider text-indigo-400">Creator Desk</span>
            <h1 className="text-3xl font-extrabold tracking-tight mt-1">LCM Authoring & LC Integration Desk</h1>
            <p className="text-slate-400 text-sm mt-1 max-w-xl">
              Upload videos/text for LeD, add multiple reflection spots, create MCQ & subjective quiz loops with option feedbacks, and configure extra LxT material.
            </p>
          </div>
          <button
            onClick={() => {
              setSelectedLessonId('');
              setTitle('');
              setSummary('');
              setVideoUrl('');
              setTranscript('');
              setReflectionSpots([{ timestampSeconds: 45, prompt: '', spotType: 'reflection' }]);
              setMcqs([{ question: '', choices: ['', '', '', ''], correctIndex: 0, feedbacks: ['', '', '', ''] }]);
              setSubjectives([{ prompt: '', exemplarAnswer: '' }]);
              setLxtList([{ title: '', url: '', summary: '', extraType: 'link' }]);
              setLxiQuestion('');
              setMessage(null);
            }}
            className="inline-flex items-center gap-2 bg-indigo-600 hover:bg-indigo-500 text-white px-5 py-3 rounded-xl font-bold transition-all text-sm shadow-lg shadow-indigo-600/30"
          >
            <Plus size={18} />
            New Lesson
          </button>
        </div>

        {message && (
          <div className={`p-4 rounded-xl flex items-center gap-3 text-sm font-semibold ${message.type === 'success' ? 'bg-emerald-50 text-emerald-800 border border-emerald-200 dark:bg-emerald-950/40 dark:text-emerald-300 dark:border-emerald-800' : 'bg-rose-50 text-rose-800 border border-rose-200 dark:bg-rose-950/40 dark:text-rose-300 dark:border-rose-800'}`}>
            {message.type === 'success' ? <CheckCircle2 size={18} /> : <AlertCircle size={18} />}
            {message.text}
          </div>
        )}

        {/* Course & Lesson Selector */}
        <div className="grid md:grid-cols-2 gap-4 bg-white dark:bg-slate-900 p-6 rounded-2xl border border-slate-200 dark:border-slate-800 shadow-sm">
          <div>
            <div className="flex items-center justify-between mb-2">
              <label className="block text-xs font-bold uppercase tracking-wider text-slate-500 dark:text-slate-400">Target Course / Module</label>
              <button 
                type="button" 
                onClick={handleCreateCourse} 
                className="text-xs font-bold bg-indigo-50 dark:bg-indigo-950 text-indigo-600 dark:text-indigo-300 px-2.5 py-1 rounded-lg border border-indigo-200 hover:bg-indigo-100"
              >
                + Add Course
              </button>
            </div>
            <select
              value={selectedCourseId}
              onChange={(e) => {
                setSelectedCourseId(e.target.value);
                setSelectedLessonId('');
              }}
              className="w-full rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 px-4 py-2.5 text-sm font-medium text-slate-900 dark:text-white"
            >
              {courses.map((c) => (
                <option key={c._id} value={c._id}>{c.title}</option>
              ))}
            </select>
          </div>

          <div>
            <label className="block text-xs font-bold uppercase tracking-wider text-slate-500 dark:text-slate-400 mb-2">Existing Lesson</label>
            <select
              value={selectedLessonId}
              onChange={(e) => setSelectedLessonId(e.target.value)}
              className="w-full rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 px-4 py-2.5 text-sm font-medium text-slate-900 dark:text-white"
            >
              <option value="">-- Create New Lesson --</option>
              {currentCourse?.lessons?.map((l) => (
                <option key={l._id} value={l._id}>{l.title}</option>
              ))}
            </select>
          </div>
        </div>

        <form onSubmit={handleSaveLesson} className="bg-white dark:bg-slate-900 rounded-3xl border border-slate-200 dark:border-slate-800 p-8 shadow-sm space-y-8">
          {/* Metadata */}
          <div className="space-y-4">
            <h3 className="text-lg font-bold text-slate-900 dark:text-white">1. Lesson Overview</h3>
            <div className="grid md:grid-cols-2 gap-4">
              <div>
                <label className="block text-xs font-semibold text-slate-600 dark:text-slate-400 mb-1">Lesson Title</label>
                <input
                  type="text"
                  required
                  value={title}
                  onChange={(e) => setTitle(e.target.value)}
                  placeholder="e.g. Introduction to Machine Learning"
                  className="w-full rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 px-4 py-2.5 text-sm text-slate-900 dark:text-white"
                />
              </div>
              <div>
                <label className="block text-xs font-semibold text-slate-600 dark:text-slate-400 mb-1">LeD Video URL / YouTube Embed</label>
                <input
                  type="text"
                  value={videoUrl}
                  onChange={(e) => setVideoUrl(e.target.value)}
                  placeholder="https://www.youtube.com/embed/..."
                  className="w-full rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 px-4 py-2.5 text-sm text-slate-900 dark:text-white"
                />
              </div>
            </div>
            <div>
              <label className="block text-xs font-semibold text-slate-600 dark:text-slate-400 mb-1">Lesson Summary / Overview</label>
              <textarea
                rows={2}
                value={summary}
                onChange={(e) => setSummary(e.target.value)}
                placeholder="Core concepts summary..."
                className="w-full rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 px-4 py-2.5 text-sm text-slate-900 dark:text-white"
              />
            </div>
          </div>

          {/* LCM Tabs */}
          <div className="space-y-6 pt-6 border-t border-slate-200 dark:border-slate-800">
            <div className="flex flex-wrap gap-2 border-b border-slate-200 dark:border-slate-800 pb-4">
              <button
                type="button"
                onClick={() => setActiveTab('led')}
                className={`inline-flex items-center gap-2 px-4 py-2.5 rounded-xl font-bold text-xs uppercase tracking-wider transition-all ${activeTab === 'led' ? 'bg-brand text-white shadow-md' : 'bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-400'}`}
              >
                <Video size={16} /> LeD Config (Video, Text & Reflection Spots)
              </button>
              <button
                type="button"
                onClick={() => setActiveTab('lbd')}
                className={`inline-flex items-center gap-2 px-4 py-2.5 rounded-xl font-bold text-xs uppercase tracking-wider transition-all ${activeTab === 'lbd' ? 'bg-brand text-white shadow-md' : 'bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-400'}`}
              >
                <CheckSquare size={16} /> LbD Quiz Interface (MCQs & Subjective Desks)
              </button>
              <button
                type="button"
                onClick={() => setActiveTab('lxt')}
                className={`inline-flex items-center gap-2 px-4 py-2.5 rounded-xl font-bold text-xs uppercase tracking-wider transition-all ${activeTab === 'lxt' ? 'bg-brand text-white shadow-md' : 'bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-400'}`}
              >
                <Link2 size={16} /> LxT Extra Material (Extension Content)
              </button>
              <button
                type="button"
                onClick={() => setActiveTab('lxi')}
                className={`inline-flex items-center gap-2 px-4 py-2.5 rounded-xl font-bold text-xs uppercase tracking-wider transition-all ${activeTab === 'lxi' ? 'bg-brand text-white shadow-md' : 'bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-400'}`}
              >
                <MessageSquare size={16} /> LxI Author Question (Peer Discussion)
              </button>
            </div>

            {/* LeD Tab */}
            {activeTab === 'led' && (
              <div className="space-y-6 bg-slate-50 dark:bg-slate-850 p-6 rounded-2xl border border-slate-200 dark:border-slate-800">
                <h4 className="font-bold text-sm text-slate-900 dark:text-white flex items-center gap-2">
                  <Video size={18} className="text-brand" /> LeD: Video / Text Content & Reflection Spot Checkpoints
                </h4>

                <div>
                  <label className="block text-xs font-semibold text-slate-600 dark:text-slate-400 mb-1">Supplementary Reading / Video Transcript</label>
                  <textarea
                    rows={3}
                    value={transcript}
                    onChange={(e) => setTranscript(e.target.value)}
                    placeholder="Full video transcript or reading material..."
                    className="w-full rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 px-4 py-2.5 text-sm text-slate-900 dark:text-white"
                  />
                </div>

                <div className="space-y-4">
                  <div className="flex items-center justify-between">
                    <h5 className="font-bold text-xs uppercase tracking-wider text-slate-500 dark:text-slate-400">Reflection Checkpoint Questions</h5>
                    <button
                      type="button"
                      onClick={() => setReflectionSpots([...reflectionSpots, { timestampSeconds: 60, prompt: '', spotType: 'reflection' }])}
                      className="inline-flex items-center gap-1.5 text-xs font-bold text-brand hover:underline"
                    >
                      <Plus size={14} /> Add Reflection Question
                    </button>
                  </div>

                  {reflectionSpots.map((spot, idx) => (
                    <div key={idx} className="p-4 bg-white dark:bg-slate-800 rounded-xl border border-slate-200 dark:border-slate-700 flex gap-4 items-start">
                      <div className="w-32 shrink-0">
                        <label className="block text-[11px] font-semibold text-slate-500 mb-1">Time (Sec)</label>
                        <input
                          type="number"
                          value={spot.timestampSeconds}
                          onChange={(e) => {
                            const copy = [...reflectionSpots];
                            copy[idx].timestampSeconds = Number(e.target.value);
                            setReflectionSpots(copy);
                          }}
                          className="w-full rounded-lg border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-900 px-3 py-1.5 text-xs text-slate-900 dark:text-white"
                        />
                      </div>
                      <div className="flex-grow">
                        <label className="block text-[11px] font-semibold text-slate-500 mb-1">Reflection Spot Question Prompt</label>
                        <input
                          type="text"
                          value={spot.prompt}
                          onChange={(e) => {
                            const copy = [...reflectionSpots];
                            copy[idx].prompt = e.target.value;
                            setReflectionSpots(copy);
                          }}
                          placeholder="e.g. Pause and think: Why do we separate training and testing datasets?"
                          className="w-full rounded-lg border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-900 px-3 py-1.5 text-xs text-slate-900 dark:text-white"
                        />
                      </div>
                      {reflectionSpots.length > 1 && (
                        <button
                          type="button"
                          onClick={() => setReflectionSpots(reflectionSpots.filter((_, i) => i !== idx))}
                          className="p-2 text-rose-500 hover:bg-rose-50 dark:hover:bg-rose-950/40 rounded-lg mt-5"
                        >
                          <Trash2 size={16} />
                        </button>
                      )}
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* LbD Tab */}
            {activeTab === 'lbd' && (
              <div className="space-y-8 bg-slate-50 dark:bg-slate-850 p-6 rounded-2xl border border-slate-200 dark:border-slate-800">
                <h4 className="font-bold text-sm text-slate-900 dark:text-white flex items-center gap-2">
                  <CheckSquare size={18} className="text-brand" /> LbD: Quiz Maker Loop (MCQs & Subjective Desks)
                </h4>

                {/* MCQ Loop */}
                <div className="space-y-6">
                  <div className="flex items-center justify-between">
                    <h5 className="font-bold text-xs uppercase tracking-wider text-slate-500 dark:text-slate-400">Multiple Choice Questions (MCQs)</h5>
                    <button
                      type="button"
                      onClick={() => setMcqs([...mcqs, { question: '', choices: ['', '', '', ''], correctIndex: 0, feedbacks: ['', '', '', ''] }])}
                      className="inline-flex items-center gap-1.5 text-xs font-bold text-brand hover:underline"
                    >
                      <Plus size={14} /> Add MCQ to Quiz
                    </button>
                  </div>

                  {mcqs.map((m, mIdx) => (
                    <div key={mIdx} className="p-5 bg-white dark:bg-slate-800 rounded-2xl border border-slate-200 dark:border-slate-700 space-y-4">
                      <div className="flex items-center justify-between">
                        <span className="text-xs font-bold uppercase text-slate-500 dark:text-slate-400">MCQ Question #{mIdx + 1}</span>
                        {mcqs.length > 1 && (
                          <button
                            type="button"
                            onClick={() => setMcqs(mcqs.filter((_, i) => i !== mIdx))}
                            className="text-xs text-rose-500 hover:underline flex items-center gap-1"
                          >
                            <Trash2 size={14} /> Delete Question
                          </button>
                        )}
                      </div>

                      <input
                        type="text"
                        value={m.question}
                        onChange={(e) => {
                          const copy = [...mcqs];
                          copy[mIdx].question = e.target.value;
                          setMcqs(copy);
                        }}
                        placeholder="Enter MCQ Question Prompt..."
                        className="w-full rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-900 px-4 py-2.5 text-sm font-semibold text-slate-900 dark:text-white"
                      />

                      <div className="grid md:grid-cols-2 gap-4">
                        {m.choices.map((choice, cIdx) => (
                          <div key={cIdx} className="p-3 bg-slate-50 dark:bg-slate-900 rounded-xl border border-slate-200 dark:border-slate-700 space-y-2">
                            <div className="flex items-center justify-between">
                              <span className="text-[11px] font-bold uppercase text-slate-500">Choice {cIdx + 1}</span>
                              <label className="flex items-center gap-1 text-xs font-semibold text-indigo-600 dark:text-indigo-400 cursor-pointer">
                                <input
                                  type="radio"
                                  name={`correct_${mIdx}`}
                                  checked={m.correctIndex === cIdx}
                                  onChange={() => {
                                    const copy = [...mcqs];
                                    copy[mIdx].correctIndex = cIdx;
                                    setMcqs(copy);
                                  }}
                                />
                                Correct
                              </label>
                            </div>
                            <input
                              type="text"
                              value={choice}
                              onChange={(e) => {
                                const copy = [...mcqs];
                                copy[mIdx].choices[cIdx] = e.target.value;
                                setMcqs(copy);
                              }}
                              placeholder={`Choice ${cIdx + 1} Text`}
                              className="w-full rounded-lg border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 px-3 py-1.5 text-xs text-slate-900 dark:text-white"
                            />
                            <input
                              type="text"
                              value={m.feedbacks[cIdx] || ''}
                              onChange={(e) => {
                                const copy = [...mcqs];
                                copy[mIdx].feedbacks[cIdx] = e.target.value;
                                setMcqs(copy);
                              }}
                              placeholder={`Feedback if student selects Choice ${cIdx + 1}`}
                              className="w-full rounded-lg border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 px-3 py-1 text-[11px] text-slate-600 dark:text-slate-300"
                            />
                          </div>
                        ))}
                      </div>
                    </div>
                  ))}
                </div>

                {/* Subjective Loop */}
                <div className="pt-6 border-t border-slate-200 dark:border-slate-800 space-y-4">
                  <div className="flex items-center justify-between">
                    <h5 className="font-bold text-xs uppercase tracking-wider text-slate-500 dark:text-slate-400">Subjective Questions & Author Feedback</h5>
                    <button
                      type="button"
                      onClick={() => setSubjectives([...subjectives, { prompt: '', exemplarAnswer: '' }])}
                      className="inline-flex items-center gap-1.5 text-xs font-bold text-brand hover:underline"
                    >
                      <Plus size={14} /> Add Subjective Question
                    </button>
                  </div>

                  {subjectives.map((sub, sIdx) => (
                    <div key={sIdx} className="p-5 bg-white dark:bg-slate-800 rounded-2xl border border-slate-200 dark:border-slate-700 space-y-3">
                      <div className="flex items-center justify-between">
                        <span className="text-xs font-bold uppercase text-slate-500">Subjective #{sIdx + 1}</span>
                        {subjectives.length > 1 && (
                          <button
                            type="button"
                            onClick={() => setSubjectives(subjectives.filter((_, i) => i !== sIdx))}
                            className="text-xs text-rose-500 hover:underline flex items-center gap-1"
                          >
                            <Trash2 size={14} /> Delete
                          </button>
                        )}
                      </div>
                      <input
                        type="text"
                        value={sub.prompt}
                        onChange={(e) => {
                          const copy = [...subjectives];
                          copy[sIdx].prompt = e.target.value;
                          setSubjectives(copy);
                        }}
                        placeholder="Subjective Question Prompt..."
                        className="w-full rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-900 px-4 py-2 text-xs text-slate-900 dark:text-white"
                      />
                      <textarea
                        rows={2}
                        value={sub.exemplarAnswer}
                        onChange={(e) => {
                          const copy = [...subjectives];
                          copy[sIdx].exemplarAnswer = e.target.value;
                          setSubjectives(copy);
                        }}
                        placeholder="Author Feedback / Correct Exemplar Answer (Displayed to LC Student after typing)..."
                        className="w-full rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-900 px-4 py-2 text-xs text-slate-900 dark:text-white"
                      />
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* LxT Tab */}
            {activeTab === 'lxt' && (
              <div className="space-y-4 bg-slate-50 dark:bg-slate-850 p-6 rounded-2xl border border-slate-200 dark:border-slate-800">
                <div className="flex items-center justify-between">
                  <h4 className="font-bold text-sm text-slate-900 dark:text-white flex items-center gap-2">
                    <Link2 size={18} className="text-brand" /> LxT: Extra Material & Extension Trajectories
                  </h4>
                  <button
                    type="button"
                    onClick={() => setLxtList([...lxtList, { title: '', url: '', summary: '', extraType: 'link' }])}
                    className="inline-flex items-center gap-1.5 text-xs font-bold text-brand hover:underline"
                  >
                    <Plus size={14} /> Add Extra Material
                  </button>
                </div>

                {lxtList.map((x, xIdx) => (
                  <div key={xIdx} className="p-4 bg-white dark:bg-slate-800 rounded-xl border border-slate-200 dark:border-slate-700 grid md:grid-cols-3 gap-3 items-center">
                    <input
                      type="text"
                      value={x.title}
                      onChange={(e) => {
                        const copy = [...lxtList];
                        copy[xIdx].title = e.target.value;
                        setLxtList(copy);
                      }}
                      placeholder="Material Title"
                      className="rounded-lg border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-900 px-3 py-2 text-xs text-slate-900 dark:text-white"
                    />
                    <input
                      type="text"
                      value={x.url}
                      onChange={(e) => {
                        const copy = [...lxtList];
                        copy[xIdx].url = e.target.value;
                        setLxtList(copy);
                      }}
                      placeholder="URL Link (https://...)"
                      className="rounded-lg border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-900 px-3 py-2 text-xs text-slate-900 dark:text-white"
                    />
                    <div className="flex items-center gap-2">
                      <select
                        value={x.extraType}
                        onChange={(e) => {
                          const copy = [...lxtList];
                          copy[xIdx].extraType = e.target.value;
                          setLxtList(copy);
                        }}
                        className="rounded-lg border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-900 px-3 py-2 text-xs text-slate-900 dark:text-white flex-grow"
                      >
                        <option value="link">Extra Resource Link</option>
                        <option value="video">Extra Video LeD</option>
                        <option value="practice">Extra LbD Practice</option>
                      </select>
                      {lxtList.length > 1 && (
                        <button
                          type="button"
                          onClick={() => setLxtList(lxtList.filter((_, i) => i !== xIdx))}
                          className="p-2 text-rose-500 hover:bg-rose-50 rounded-lg"
                        >
                          <Trash2 size={16} />
                        </button>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            )}

            {/* LxI Tab */}
            {activeTab === 'lxi' && (
              <div className="space-y-4 bg-slate-50 dark:bg-slate-850 p-6 rounded-2xl border border-slate-200 dark:border-slate-800">
                <h4 className="font-bold text-sm text-slate-900 dark:text-white flex items-center gap-2">
                  <MessageSquare size={18} className="text-brand" /> LxI: Author Question for Peer Interaction
                </h4>
                <div>
                  <label className="block text-xs font-semibold text-slate-600 dark:text-slate-400 mb-1">Author's Discussion Question (Shown on LC interface)</label>
                  <textarea
                    rows={3}
                    value={lxiQuestion}
                    onChange={(e) => setLxiQuestion(e.target.value)}
                    placeholder="Enter the discussion question for companions..."
                    className="w-full rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 px-4 py-2.5 text-sm text-slate-900 dark:text-white"
                  />
                </div>
              </div>
            )}
          </div>

          <div className="pt-6 border-t border-slate-200 dark:border-slate-800 flex justify-end">
            <button
              type="submit"
              className="inline-flex items-center gap-2 bg-brand hover:bg-brand/90 text-white font-bold px-8 py-3.5 rounded-xl shadow-lg shadow-brand/20 transition-all text-sm"
            >
              <Save size={18} />
              Publish to LC Interface
            </button>
          </div>
        </form>
      </div>
    </Layout>
  );
}
