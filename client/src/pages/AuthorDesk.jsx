import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Plus, Save, Trash2, Video, CheckSquare, Link2, MessageSquare, BookOpen, ChevronRight, AlertCircle, CheckCircle2 } from 'lucide-react';
import api, { track } from '../api';
import Layout from '../components/Layout';

export default function AuthorDesk() {
  const navigate = useNavigate();
  const [courses, setCourses] = useState([]);
  const [selectedCourseId, setSelectedCourseId] = useState('');
  const [selectedLessonId, setSelectedLessonId] = useState('');
  const [activeTab, setActiveTab] = useState('led'); // 'led' | 'lbd' | 'lxt' | 'lxi'
  const [message, setMessage] = useState(null);

  // Lesson Form State
  const [title, setTitle] = useState('');
  const [summary, setSummary] = useState('');
  const [videoUrl, setVideoUrl] = useState('');

  // LeD State
  const [transcript, setTranscript] = useState('');
  const [reflectionTimestamp, setReflectionTimestamp] = useState(45);
  const [reflectionPrompt, setReflectionPrompt] = useState('');

  // LbD State (MCQ & Subjective)
  const [mcqQuestion, setMcqQuestion] = useState('');
  const [choices, setChoices] = useState(['', '', '', '']);
  const [correctIndex, setCorrectIndex] = useState(0);
  const [feedbacks, setFeedbacks] = useState(['', '', '', '']);
  const [subjectivePrompt, setSubjectivePrompt] = useState('');
  const [exemplarAnswer, setExemplarAnswer] = useState('');

  // LxT State
  const [lxtTitle, setLxtTitle] = useState('');
  const [lxtUrl, setLxtUrl] = useState('');

  // LxI State
  const [weeklyFocusPrompt, setWeeklyFocusPrompt] = useState('');

  // Fetch Courses
  useEffect(() => {
    api.get('/courses')
      .then((r) => {
        setCourses(r.data);
        if (r.data.length > 0) {
          setSelectedCourseId(r.data[0]._id);
        }
      })
      .catch((err) => console.error(err));
  }, []);

  const currentCourse = courses.find((c) => c._id === selectedCourseId);

  // Load lesson data when selected
  useEffect(() => {
    if (!currentCourse || !selectedLessonId) return;
    const lesson = currentCourse.lessons?.find((l) => l._id === selectedLessonId);
    if (lesson) {
      setTitle(lesson.title || '');
      setSummary(lesson.summary || '');
      setVideoUrl(lesson.videoUrl || lesson.led?.videoUrl || '');

      // LeD
      setTranscript(lesson.led?.transcript || '');
      setReflectionTimestamp(lesson.led?.reflectionSpot?.timestampSeconds || 45);
      setReflectionPrompt(lesson.led?.reflectionSpot?.prompt || '');

      // LbD
      const mcq = lesson.lbd?.mcqs?.[0];
      if (mcq) {
        setMcqQuestion(mcq.question || '');
        setChoices(mcq.choices?.length === 4 ? mcq.choices : ['', '', '', '']);
        setCorrectIndex(mcq.correctIndex || 0);
        setFeedbacks(mcq.feedbacks?.length === 4 ? mcq.feedbacks : ['', '', '', '']);
      } else {
        setMcqQuestion('');
        setChoices(['', '', '', '']);
        setCorrectIndex(0);
        setFeedbacks(['', '', '', '']);
      }
      setSubjectivePrompt(lesson.lbd?.subjective?.prompt || '');
      setExemplarAnswer(lesson.lbd?.subjective?.exemplarAnswer || '');

      // LxT
      const lxtItem = lesson.lxt?.[0];
      setLxtTitle(lxtItem?.title || '');
      setLxtUrl(lxtItem?.url || '');

      // LxI
      setWeeklyFocusPrompt(lesson.lxi?.weeklyFocusPrompt || '');
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
        reflectionSpot: { timestampSeconds: Number(reflectionTimestamp), prompt: reflectionPrompt }
      },
      lbd: {
        mcqs: mcqQuestion ? [{
          question: mcqQuestion,
          choices: choices.map((c, i) => c || `Option ${i + 1}`),
          correctIndex: Number(correctIndex),
          feedbacks: feedbacks.map((f, i) => f || `Feedback for option ${i + 1}`)
        }] : [],
        subjective: {
          prompt: subjectivePrompt,
          exemplarAnswer
        }
      },
      lxt: lxtUrl ? [{ title: lxtTitle || 'Resource Link', url: lxtUrl, resourceType: 'link' }] : [],
      lxi: {
        weeklyFocusPrompt
      }
    };

    try {
      if (selectedLessonId) {
        await api.put(`/author/courses/${selectedCourseId}/lessons/${selectedLessonId}`, payload);
        setMessage({ type: 'success', text: 'LCM Lesson updated and published!' });
      } else {
        await api.post(`/author/courses/${selectedCourseId}/lessons`, payload);
        setMessage({ type: 'success', text: 'New LCM Lesson created!' });
      }

      // Refresh courses
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
        {/* Header Banner */}
        <div className="rounded-3xl bg-slate-900 text-white p-8 shadow-xl flex flex-col md:flex-row md:items-center justify-between gap-6">
          <div>
            <span className="text-xs font-bold uppercase tracking-wider text-indigo-400">Creator & Authoring Desk</span>
            <h1 className="text-3xl font-extrabold tracking-tight mt-1">LCM Module Designer</h1>
            <p className="text-slate-400 text-sm mt-1 max-w-xl">
              Configure course materials, LeD reflection spots, LbD quiz feedbacks, and LxI focus prompts. Changes sync dynamically to the companion view.
            </p>
          </div>
          <button
            onClick={() => {
              setSelectedLessonId('');
              setTitle('');
              setSummary('');
              setVideoUrl('');
              setMcqQuestion('');
              setChoices(['', '', '', '']);
              setFeedbacks(['', '', '', '']);
              setSubjectivePrompt('');
              setExemplarAnswer('');
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

        {/* Selection Toolbar */}
        <div className="grid md:grid-cols-2 gap-4 bg-white dark:bg-slate-900 p-6 rounded-2xl border border-slate-200 dark:border-slate-800 shadow-sm">
          <div>
            <label className="block text-xs font-bold uppercase tracking-wider text-slate-500 dark:text-slate-400 mb-2">Select Target Course</label>
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
            <label className="block text-xs font-bold uppercase tracking-wider text-slate-500 dark:text-slate-400 mb-2">Select Existing Lesson to Edit</label>
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

        {/* Form & Tab Editor */}
        <form onSubmit={handleSaveLesson} className="bg-white dark:bg-slate-900 rounded-3xl border border-slate-200 dark:border-slate-800 p-8 shadow-sm space-y-8">
          {/* General Metadata */}
          <div className="space-y-4">
            <h3 className="text-lg font-bold text-slate-900 dark:text-white">1. Lesson Metadata</h3>
            <div className="grid md:grid-cols-2 gap-4">
              <div>
                <label className="block text-xs font-semibold text-slate-600 dark:text-slate-400 mb-1">Lesson Title</label>
                <input
                  type="text"
                  required
                  value={title}
                  onChange={(e) => setTitle(e.target.value)}
                  placeholder="e.g. Introduction to Neural Networks"
                  className="w-full rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 px-4 py-2.5 text-sm text-slate-900 dark:text-white"
                />
              </div>
              <div>
                <label className="block text-xs font-semibold text-slate-600 dark:text-slate-400 mb-1">Video URL (YouTube Embed / MP4)</label>
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
              <label className="block text-xs font-semibold text-slate-600 dark:text-slate-400 mb-1">Summary / Concept Overview</label>
              <textarea
                rows={2}
                value={summary}
                onChange={(e) => setSummary(e.target.value)}
                placeholder="Brief summary of the core concepts covered..."
                className="w-full rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 px-4 py-2.5 text-sm text-slate-900 dark:text-white"
              />
            </div>
          </div>

          {/* LCM Sub-tabs */}
          <div className="space-y-6 pt-6 border-t border-slate-200 dark:border-slate-800">
            <div className="flex flex-wrap gap-2 border-b border-slate-200 dark:border-slate-800 pb-4">
              <button
                type="button"
                onClick={() => setActiveTab('led')}
                className={`inline-flex items-center gap-2 px-4 py-2.5 rounded-xl font-bold text-xs uppercase tracking-wider transition-all ${activeTab === 'led' ? 'bg-brand text-white shadow-md' : 'bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-400 hover:bg-slate-200'}`}
              >
                <Video size={16} /> LeD Config (Dialogue & Reflection)
              </button>
              <button
                type="button"
                onClick={() => setActiveTab('lbd')}
                className={`inline-flex items-center gap-2 px-4 py-2.5 rounded-xl font-bold text-xs uppercase tracking-wider transition-all ${activeTab === 'lbd' ? 'bg-brand text-white shadow-md' : 'bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-400 hover:bg-slate-200'}`}
              >
                <CheckSquare size={16} /> LbD Config (MCQs & Feedback)
              </button>
              <button
                type="button"
                onClick={() => setActiveTab('lxt')}
                className={`inline-flex items-center gap-2 px-4 py-2.5 rounded-xl font-bold text-xs uppercase tracking-wider transition-all ${activeTab === 'lxt' ? 'bg-brand text-white shadow-md' : 'bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-400 hover:bg-slate-200'}`}
              >
                <Link2 size={16} /> LxT Config (Extension Trajectories)
              </button>
              <button
                type="button"
                onClick={() => setActiveTab('lxi')}
                className={`inline-flex items-center gap-2 px-4 py-2.5 rounded-xl font-bold text-xs uppercase tracking-wider transition-all ${activeTab === 'lxi' ? 'bg-brand text-white shadow-md' : 'bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-400 hover:bg-slate-200'}`}
              >
                <MessageSquare size={16} /> LxI Config (Peer Focus)
              </button>
            </div>

            {/* LeD Tab */}
            {activeTab === 'led' && (
              <div className="space-y-4 bg-slate-50 dark:bg-slate-850 p-6 rounded-2xl border border-slate-200 dark:border-slate-800">
                <h4 className="font-bold text-sm text-slate-900 dark:text-white flex items-center gap-2">
                  <Video size={18} className="text-brand" /> LeD: Video Reflection Spot Configurator
                </h4>
                <div className="grid md:grid-cols-3 gap-4">
                  <div>
                    <label className="block text-xs font-semibold text-slate-600 dark:text-slate-400 mb-1">Reflection Checkpoint Timestamp (Seconds)</label>
                    <input
                      type="number"
                      value={reflectionTimestamp}
                      onChange={(e) => setReflectionTimestamp(e.target.value)}
                      className="w-full rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 px-4 py-2.5 text-sm text-slate-900 dark:text-white"
                    />
                  </div>
                  <div className="md:col-span-2">
                    <label className="block text-xs font-semibold text-slate-600 dark:text-slate-400 mb-1">Reflection Prompt / Stopping Question</label>
                    <input
                      type="text"
                      value={reflectionPrompt}
                      onChange={(e) => setReflectionPrompt(e.target.value)}
                      placeholder="e.g. Pause and think: How does this concept apply to real-world datasets?"
                      className="w-full rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 px-4 py-2.5 text-sm text-slate-900 dark:text-white"
                    />
                  </div>
                </div>
                <div>
                  <label className="block text-xs font-semibold text-slate-600 dark:text-slate-400 mb-1">Video Transcript / Supplementary Notes</label>
                  <textarea
                    rows={3}
                    value={transcript}
                    onChange={(e) => setTranscript(e.target.value)}
                    placeholder="Full video transcript or structured lecture notes..."
                    className="w-full rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 px-4 py-2.5 text-sm text-slate-900 dark:text-white"
                  />
                </div>
              </div>
            )}

            {/* LbD Tab */}
            {activeTab === 'lbd' && (
              <div className="space-y-6 bg-slate-50 dark:bg-slate-850 p-6 rounded-2xl border border-slate-200 dark:border-slate-800">
                <h4 className="font-bold text-sm text-slate-900 dark:text-white flex items-center gap-2">
                  <CheckSquare size={18} className="text-brand" /> LbD: Interactive Quiz & Feedback Builder
                </h4>

                {/* MCQ Builder */}
                <div className="space-y-4">
                  <div>
                    <label className="block text-xs font-semibold text-slate-600 dark:text-slate-400 mb-1">MCQ Question Prompt</label>
                    <input
                      type="text"
                      value={mcqQuestion}
                      onChange={(e) => setMcqQuestion(e.target.value)}
                      placeholder="e.g. What is the main purpose of Supervised Learning?"
                      className="w-full rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 px-4 py-2.5 text-sm text-slate-900 dark:text-white"
                    />
                  </div>

                  <div className="grid md:grid-cols-2 gap-4">
                    {choices.map((choice, i) => (
                      <div key={i} className="p-4 bg-white dark:bg-slate-800 rounded-xl border border-slate-200 dark:border-slate-700 space-y-2">
                        <div className="flex items-center justify-between">
                          <span className="text-xs font-bold uppercase text-slate-500 dark:text-slate-400">Option {i + 1}</span>
                          <label className="flex items-center gap-1.5 text-xs font-semibold text-indigo-600 dark:text-indigo-400 cursor-pointer">
                            <input
                              type="radio"
                              name="correctChoice"
                              checked={correctIndex === i}
                              onChange={() => setCorrectIndex(i)}
                            />
                            Mark as Correct
                          </label>
                        </div>
                        <input
                          type="text"
                          value={choice}
                          onChange={(e) => {
                            const newChoices = [...choices];
                            newChoices[i] = e.target.value;
                            setChoices(newChoices);
                          }}
                          placeholder={`Option ${i + 1} Choice Text`}
                          className="w-full rounded-lg border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-900 px-3 py-2 text-sm text-slate-900 dark:text-white"
                        />
                        <input
                          type="text"
                          value={feedbacks[i] || ''}
                          onChange={(e) => {
                            const newFb = [...feedbacks];
                            newFb[i] = e.target.value;
                            setFeedbacks(newFb);
                          }}
                          placeholder={`Custom Feedback for selecting Option ${i + 1}`}
                          className="w-full rounded-lg border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-900 px-3 py-1.5 text-xs text-slate-600 dark:text-slate-300"
                        />
                      </div>
                    ))}
                  </div>
                </div>

                {/* Subjective Builder */}
                <div className="pt-4 border-t border-slate-200 dark:border-slate-800 space-y-4">
                  <h5 className="font-bold text-xs uppercase tracking-wider text-slate-500 dark:text-slate-400">Subjective Practice Desk & Exemplar Answer</h5>
                  <div>
                    <label className="block text-xs font-semibold text-slate-600 dark:text-slate-400 mb-1">Subjective Question Prompt</label>
                    <input
                      type="text"
                      value={subjectivePrompt}
                      onChange={(e) => setSubjectivePrompt(e.target.value)}
                      placeholder="e.g. Explain in your own words why training data must be separated from testing data."
                      className="w-full rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 px-4 py-2.5 text-sm text-slate-900 dark:text-white"
                    />
                  </div>
                  <div>
                    <label className="block text-xs font-semibold text-slate-600 dark:text-slate-400 mb-1">Author Exemplar Answer (Displayed to student after typing)</label>
                    <textarea
                      rows={3}
                      value={exemplarAnswer}
                      onChange={(e) => setExemplarAnswer(e.target.value)}
                      placeholder="Type the ideal sample response or evaluation rubric..."
                      className="w-full rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 px-4 py-2.5 text-sm text-slate-900 dark:text-white"
                    />
                  </div>
                </div>
              </div>
            )}

            {/* LxT Tab */}
            {activeTab === 'lxt' && (
              <div className="space-y-4 bg-slate-50 dark:bg-slate-850 p-6 rounded-2xl border border-slate-200 dark:border-slate-800">
                <h4 className="font-bold text-sm text-slate-900 dark:text-white flex items-center gap-2">
                  <Link2 size={18} className="text-brand" /> LxT: Extension Trajectory Resource Configurator
                </h4>
                <div className="grid md:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-xs font-semibold text-slate-600 dark:text-slate-400 mb-1">Resource Title</label>
                    <input
                      type="text"
                      value={lxtTitle}
                      onChange={(e) => setLxtTitle(e.target.value)}
                      placeholder="e.g. Interactive ML Visualization Tool"
                      className="w-full rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 px-4 py-2.5 text-sm text-slate-900 dark:text-white"
                    />
                  </div>
                  <div>
                    <label className="block text-xs font-semibold text-slate-600 dark:text-slate-400 mb-1">Resource External URL</label>
                    <input
                      type="text"
                      value={lxtUrl}
                      onChange={(e) => setLxtUrl(e.target.value)}
                      placeholder="https://..."
                      className="w-full rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 px-4 py-2.5 text-sm text-slate-900 dark:text-white"
                    />
                  </div>
                </div>
              </div>
            )}

            {/* LxI Tab */}
            {activeTab === 'lxi' && (
              <div className="space-y-4 bg-slate-50 dark:bg-slate-850 p-6 rounded-2xl border border-slate-200 dark:border-slate-800">
                <h4 className="font-bold text-sm text-slate-900 dark:text-white flex items-center gap-2">
                  <MessageSquare size={18} className="text-brand" /> LxI: Weekly Focus Peer Discussion Configurator
                </h4>
                <div>
                  <label className="block text-xs font-semibold text-slate-600 dark:text-slate-400 mb-1">Weekly Focus Prompt (Displayed to peer companions)</label>
                  <textarea
                    rows={3}
                    value={weeklyFocusPrompt}
                    onChange={(e) => setWeeklyFocusPrompt(e.target.value)}
                    placeholder="e.g. Discuss with your peer companion: Give an example of a daily app you use that relies on Machine Learning."
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
              Publish Lesson to LC Companion Interface
            </button>
          </div>
        </form>
      </div>
    </Layout>
  );
}
