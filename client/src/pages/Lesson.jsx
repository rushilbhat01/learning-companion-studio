import { useEffect, useRef, useState } from 'react';
import { Link, useParams, useNavigate } from 'react-router-dom';
import { ChevronLeft, Play, AlertCircle, CheckCircle, ArrowRight, ArrowLeft, Video, CheckSquare, Link2, MessageSquare, HelpCircle, Eye, EyeOff } from 'lucide-react';
import api, { track } from '../api';
import Layout from '../components/Layout';

export default function Lesson() {
  const { courseId, lessonId } = useParams();
  const navigate = useNavigate();
  const [data, setData] = useState(null);
  const [courseDetails, setCourseDetails] = useState(null);
  const scrolled = useRef(false);
  const lesson = data?.lesson;

  // LbD Interactive State
  const [selectedMcqChoice, setSelectedMcqChoice] = useState(null);
  const [subjectiveInput, setSubjectiveInput] = useState('');
  const [showExemplar, setShowExemplar] = useState(false);

  // Fetch current lesson data
  useEffect(() => {
    api.get(`/courses/${courseId}/lessons/${lessonId}`)
      .then((r) => setData(r.data))
      .catch(() => setData({ error: true }));
  }, [courseId, lessonId]);

  // Fetch course details for syllabus outline sidebar
  useEffect(() => {
    api.get(`/courses/${courseId}`)
      .then((r) => setCourseDetails(r.data));
  }, [courseId]);

  // Handle scroll tracking with reset on lessonId change
  useEffect(() => {
    scrolled.current = false;
    if (!lesson) return;

    const onScroll = () => {
      if (!scrolled.current && window.scrollY > 150) {
        scrolled.current = true;
        track('LESSON_SCROLLED', {
          component: 'Lesson',
          eventContext: lesson.title,
          resourceType: 'lesson',
          resourceId: lessonId,
          metadata: { depth: '150px' }
        });
      }
    };

    window.addEventListener('scroll', onScroll);
    return () => window.removeEventListener('scroll', onScroll);
  }, [lesson, lessonId]);

  // Track video interactions
  const handleVideoPlay = () => {
    if (!lesson) return;
    track('VIDEO_PLAYED', {
      component: 'VideoPlayer',
      eventContext: lesson.title,
      resourceType: 'video',
      resourceId: lessonId,
      metadata: { videoUrl: lesson.videoUrl, title: lesson.title }
    });
  };

  const handleVideoPause = () => {
    if (!lesson) return;
    track('VIDEO_PAUSED', {
      component: 'VideoPlayer',
      eventContext: lesson.title,
      resourceType: 'video',
      resourceId: lessonId,
      metadata: { videoUrl: lesson.videoUrl, title: lesson.title }
    });
  };

  const handleVideoEnded = () => {
    if (!lesson) return;
    track('VIDEO_COMPLETED', {
      component: 'VideoPlayer',
      eventContext: lesson.title,
      resourceType: 'video',
      resourceId: lessonId,
      metadata: { videoUrl: lesson.videoUrl, title: lesson.title }
    });
  };

  const handleVideoSeek = (e) => {
    if (!lesson) return;
    track('VIDEO_SEEKED', {
      component: 'VideoPlayer',
      eventContext: lesson.title,
      resourceType: 'video',
      resourceId: lessonId,
      metadata: { currentTime: Math.round(e.target.currentTime), videoUrl: lesson.videoUrl, title: lesson.title }
    });
  };

  if (data?.error) {
    return (
      <Layout>
        <div className="text-center py-12">
          <AlertCircle className="mx-auto text-rose-500 mb-4" size={40} />
          <h2 className="text-xl font-bold">Lesson not found</h2>
          <Link to="/" className="text-brand dark:text-indigo-400 mt-4 inline-block hover:underline">
            Go back to dashboard
          </Link>
        </div>
      </Layout>
    );
  }

  if (!data || !courseDetails) {
    return (
      <Layout>
        <div className="flex h-64 items-center justify-center">
          <p className="text-slate-500 dark:text-slate-400 animate-pulse font-medium">Loading lesson…</p>
        </div>
      </Layout>
    );
  }

  const lessonsList = courseDetails.lessons || [];
  const currentIndex = lessonsList.findIndex((l) => l._id === lessonId);
  const prevLesson = currentIndex > 0 ? lessonsList[currentIndex - 1] : null;
  const nextLesson = currentIndex < lessonsList.length - 1 ? lessonsList[currentIndex + 1] : null;

  const led = lesson.led || {};
  const lbd = lesson.lbd || {};
  const mcq = lbd.mcqs?.[0];
  const subjective = lbd.subjective;
  const lxtList = lesson.lxt || [];
  const lxi = lesson.lxi || {};

  return (
    <Layout>
      <Link
        to="/"
        className="mb-6 inline-flex items-center gap-1.5 text-sm font-semibold text-slate-500 hover:text-brand dark:text-slate-400 dark:hover:text-indigo-400 transition-colors"
      >
        <ChevronLeft size={16} />
        Back to Dashboard
      </Link>

      <div className="grid gap-8 lg:grid-cols-4">
        {/* Syllabus Outline Sidebar */}
        <aside className="lg:col-span-1 space-y-4 order-2 lg:order-1">
          <div className="rounded-2xl border border-slate-100 dark:border-slate-800 bg-white dark:bg-slate-900 p-5 shadow-sm">
            <h3 className="text-sm font-extrabold uppercase tracking-wider text-slate-400 dark:text-slate-500 mb-4">
              Course syllabus
            </h3>
            
            <div className="space-y-1.5">
              {lessonsList.map((l, index) => {
                const isCurrent = l._id === lessonId;
                return (
                  <Link
                    key={l._id}
                    to={`/courses/${courseId}/lessons/${l._id}`}
                    className={`flex items-start gap-3 p-3 rounded-xl text-sm transition-all duration-200 ${
                      isCurrent
                        ? 'bg-brand/5 dark:bg-indigo-500/10 text-brand dark:text-indigo-400 font-semibold'
                        : 'text-slate-600 dark:text-slate-400 hover:bg-slate-50 dark:hover:bg-slate-800/50'
                    }`}
                  >
                    <span className={`mt-0.5 flex h-5 w-5 shrink-0 items-center justify-center rounded-full text-xs font-bold ${
                      isCurrent
                        ? 'bg-brand text-white dark:bg-indigo-600'
                        : 'bg-slate-100 text-slate-500 dark:bg-slate-800 dark:text-slate-400'
                    }`}>
                      {index + 1}
                    </span>
                    <div>
                      <p className="leading-snug">{l.title}</p>
                      <p className="text-[10px] text-slate-400 dark:text-slate-500 mt-0.5">{l.durationMinutes} mins</p>
                    </div>
                  </Link>
                );
              })}
            </div>
          </div>

          {/* LxI Peer Discussion Prompt Sidebar Widget */}
          {lxi.weeklyFocusPrompt && (
            <div className="rounded-2xl border border-indigo-100 dark:border-indigo-900/60 bg-indigo-50/50 dark:bg-indigo-950/30 p-5 space-y-3">
              <div className="flex items-center gap-2 text-indigo-600 dark:text-indigo-400 font-bold text-xs uppercase tracking-wider">
                <MessageSquare size={16} />
                <span>LxI Peer Focus Prompt</span>
              </div>
              <p className="text-xs text-slate-700 dark:text-slate-300 leading-relaxed font-medium">
                {lxi.weeklyFocusPrompt}
              </p>
            </div>
          )}
        </aside>

        {/* Main Lesson Content */}
        <section className="lg:col-span-3 order-1 lg:order-2 space-y-8">
          <article className="rounded-2xl border border-slate-100 dark:border-slate-800/80 bg-white dark:bg-slate-900 p-6 md:p-8 shadow-sm space-y-6">
            <header>
              <div className="flex items-center gap-2 text-xs font-semibold text-brand dark:text-indigo-400 uppercase tracking-wider">
                <span>{courseDetails.title}</span>
                <span>•</span>
                <span>Lesson {lesson.order} of {lessonsList.length}</span>
              </div>
              <h1 className="mt-2 text-3xl font-extrabold tracking-tight text-slate-900 dark:text-white md:text-4xl">
                {lesson.title}
              </h1>
              <p className="mt-3 text-lg text-slate-600 dark:text-slate-400 leading-relaxed font-medium">
                {lesson.summary}
              </p>
            </header>

            {/* LeD: Video Container & Reflection Checkpoint */}
            {(lesson.videoUrl || led.videoUrl) && (
              <div className="space-y-4">
                <div className="overflow-hidden rounded-2xl border border-slate-100 dark:border-slate-800 bg-slate-900 shadow-md">
                  <iframe
                    id="youtube-player"
                    className="w-full aspect-video focus:outline-none"
                    src={`${(lesson.videoUrl || led.videoUrl).includes('embed') ? (lesson.videoUrl || led.videoUrl) : (lesson.videoUrl || led.videoUrl).replace('watch?v=', 'embed/').replace('youtu.be/', 'youtube.com/embed/')}?enablejsapi=1`}
                    title="LeD Video Player"
                    frameBorder="0"
                    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                    allowFullScreen
                  ></iframe>
                </div>

                {/* LeD Reflection Checkpoint Overlay Card */}
                {led.reflectionSpot?.prompt && (
                  <div className="p-5 rounded-2xl bg-indigo-50 dark:bg-indigo-950/40 border border-indigo-200 dark:border-indigo-800/80 flex items-start gap-4">
                    <div className="p-2.5 rounded-xl bg-brand text-white shrink-0">
                      <HelpCircle size={20} />
                    </div>
                    <div>
                      <span className="text-[11px] font-extrabold uppercase tracking-wider text-indigo-600 dark:text-indigo-400">
                        LeD Reflection Checkpoint (At ~{led.reflectionSpot.timestampSeconds || 45}s)
                      </span>
                      <p className="text-sm font-semibold text-slate-900 dark:text-white mt-0.5">
                        {led.reflectionSpot.prompt}
                      </p>
                    </div>
                  </div>
                )}
              </div>
            )}

            {/* Text Lesson Content */}
            <div className="prose dark:prose-invert max-w-none pt-4 border-t border-slate-100 dark:border-slate-800">
              <p className="whitespace-pre-line text-slate-700 dark:text-slate-300 text-lg leading-8">
                {lesson.content}
              </p>
            </div>

            {/* LbD: Interactive Quiz & Self-Assessment Desks */}
            <div className="pt-8 border-t border-slate-200 dark:border-slate-800 space-y-8">
              <div className="flex items-center gap-2">
                <CheckSquare className="text-brand dark:text-indigo-400" size={24} />
                <h3 className="text-xl font-extrabold text-slate-900 dark:text-white">LbD: Learning by Doing Practice Desk</h3>
              </div>

              {/* LbD MCQ Section with Author Feedback */}
              {mcq?.question && (
                <div className="p-6 rounded-2xl bg-slate-50 dark:bg-slate-850 border border-slate-200 dark:border-slate-800 space-y-4">
                  <span className="text-xs font-bold uppercase tracking-wider text-slate-500 dark:text-slate-400">Multiple Choice Practice</span>
                  <h4 className="text-base font-bold text-slate-900 dark:text-white">{mcq.question}</h4>
                  
                  <div className="grid gap-3">
                    {mcq.choices?.map((choice, i) => {
                      const isSelected = selectedMcqChoice === i;
                      const isCorrect = mcq.correctIndex === i;
                      const feedback = mcq.feedbacks?.[i];

                      return (
                        <div key={i} className="space-y-2">
                          <button
                            type="button"
                            onClick={() => {
                              setSelectedMcqChoice(i);
                              track('MCQ_ANSWERED', {
                                component: 'LbDQuiz',
                                eventContext: choice,
                                metadata: { optionIndex: i, isCorrect }
                              });
                            }}
                            className={`w-full text-left p-4 rounded-xl font-medium text-sm transition-all border ${
                              isSelected
                                ? isCorrect
                                  ? 'bg-emerald-50 dark:bg-emerald-950/40 border-emerald-500 text-emerald-900 dark:text-emerald-300 font-semibold'
                                  : 'bg-rose-50 dark:bg-rose-950/40 border-rose-500 text-rose-900 dark:text-rose-300 font-semibold'
                                : 'bg-white dark:bg-slate-800 border-slate-200 dark:border-slate-700 text-slate-800 dark:text-slate-200 hover:border-brand'
                            }`}
                          >
                            <div className="flex items-center justify-between">
                              <span>{choice}</span>
                              {isSelected && (isCorrect ? <CheckCircle className="text-emerald-500" size={18} /> : <AlertCircle className="text-rose-500" size={18} />)}
                            </div>
                          </button>

                          {/* Render Author Feedback for Selected Choice */}
                          {isSelected && feedback && (
                            <div className={`p-3 rounded-lg text-xs font-medium ${isCorrect ? 'bg-emerald-100/60 dark:bg-emerald-900/30 text-emerald-800 dark:text-emerald-300' : 'bg-rose-100/60 dark:bg-rose-900/30 text-rose-800 dark:text-rose-300'}`}>
                              <strong>Author Feedback:</strong> {feedback}
                            </div>
                          )}
                        </div>
                      );
                    })}
                  </div>
                </div>
              )}

              {/* LbD Subjective Self-Assessment Desk */}
              {subjective?.prompt && (
                <div className="p-6 rounded-2xl bg-slate-50 dark:bg-slate-850 border border-slate-200 dark:border-slate-800 space-y-4">
                  <span className="text-xs font-bold uppercase tracking-wider text-slate-500 dark:text-slate-400">Subjective Reflection Desk</span>
                  <h4 className="text-base font-bold text-slate-900 dark:text-white">{subjective.prompt}</h4>
                  
                  <textarea
                    rows={3}
                    value={subjectiveInput}
                    onChange={(e) => setSubjectiveInput(e.target.value)}
                    placeholder="Type your explanation here..."
                    className="w-full rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 p-4 text-sm text-slate-900 dark:text-white"
                  />

                  <button
                    type="button"
                    onClick={() => setShowExemplar(!showExemplar)}
                    className="inline-flex items-center gap-2 text-xs font-bold text-brand dark:text-indigo-400 hover:underline"
                  >
                    {showExemplar ? <EyeOff size={14} /> : <Eye size={14} />}
                    {showExemplar ? 'Hide Author Exemplar Answer' : 'View Author Exemplar Answer & Self-Evaluate'}
                  </button>

                  {showExemplar && (
                    <div className="p-4 rounded-xl bg-indigo-50 dark:bg-indigo-950/40 border border-indigo-200 dark:border-indigo-800 text-xs text-indigo-900 dark:text-indigo-200 leading-relaxed font-medium">
                      <strong>Author Exemplar Response:</strong>
                      <p className="mt-1">{subjective.exemplarAnswer}</p>
                    </div>
                  )}
                </div>
              )}
            </div>

            {/* LxT: Extension Resource Links */}
            {lxtList.length > 0 && lxtList[0].url && (
              <div className="pt-6 border-t border-slate-200 dark:border-slate-800 space-y-4">
                <div className="flex items-center gap-2">
                  <Link2 className="text-brand dark:text-indigo-400" size={20} />
                  <h4 className="font-extrabold text-base text-slate-900 dark:text-white">LxT: Learning Extension Trajectories</h4>
                </div>
                <div className="grid gap-3">
                  {lxtList.map((item, i) => (
                    <a
                      key={i}
                      href={item.url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="p-4 rounded-xl bg-slate-50 dark:bg-slate-850 border border-slate-200 dark:border-slate-800 hover:border-brand flex items-center justify-between transition-all"
                    >
                      <span className="text-sm font-semibold text-slate-900 dark:text-white">{item.title}</span>
                      <ArrowRight size={16} className="text-brand dark:text-indigo-400" />
                    </a>
                  ))}
                </div>
              </div>
            )}

            {/* Footer Navigation */}
            <footer className="mt-10 pt-6 border-t border-slate-100 dark:border-slate-800/80 flex flex-wrap items-center justify-between gap-4">
              {prevLesson ? (
                <button
                  onClick={() => navigate(`/courses/${courseId}/lessons/${prevLesson._id}`)}
                  className="inline-flex items-center gap-2 px-4 py-2.5 rounded-xl border border-slate-200 dark:border-slate-800 text-sm font-semibold hover:bg-slate-50 dark:hover:bg-slate-800 transition-all text-slate-700 dark:text-slate-300"
                >
                  <ArrowLeft size={16} />
                  <span>Previous Lesson</span>
                </button>
              ) : (
                <div />
              )}

              {nextLesson && (
                <button
                  onClick={() => navigate(`/courses/${courseId}/lessons/${nextLesson._id}`)}
                  className="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl bg-brand dark:bg-indigo-600 text-sm font-semibold text-white hover:bg-brand-hover dark:hover:bg-indigo-700 transition-all shadow-md"
                >
                  <span>Next Lesson</span>
                  <ArrowRight size={16} />
                </button>
              )}
            </footer>
          </article>
        </section>
      </div>
    </Layout>
  );
}
