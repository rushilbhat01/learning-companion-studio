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

  // LbD Interactive Multi-MCQ & Subjective State
  const [selectedChoices, setSelectedChoices] = useState({});
  const [subjectiveAnswers, setSubjectiveAnswers] = useState({});
  const [revealedExemplars, setRevealedExemplars] = useState({});

  useEffect(() => {
    api.get(`/courses/${courseId}/lessons/${lessonId}`)
      .then((r) => setData(r.data))
      .catch(() => setData({ error: true }));
  }, [courseId, lessonId]);

  useEffect(() => {
    api.get(`/courses/${courseId}`)
      .then((r) => setCourseDetails(r.data));
  }, [courseId]);

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
  const reflectionSpots = led.reflectionSpots || (led.reflectionSpot?.prompt ? [led.reflectionSpot] : []);
  const mcqs = lbd.mcqs || [];
  const subjectives = lbd.subjectives || (lbd.subjective?.prompt ? [lbd.subjective] : []);
  const lxtList = lesson.lxt || [];
  const lxiQuestion = lesson.lxi?.question || lesson.lxi?.weeklyFocusPrompt;

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
        {/* Syllabus Sidebar */}
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

          {/* LxI Author Question Widget */}
          {lxiQuestion && (
            <div className="rounded-2xl border border-indigo-100 dark:border-indigo-900/60 bg-indigo-50/50 dark:bg-indigo-950/30 p-5 space-y-3">
              <div className="flex items-center gap-2 text-indigo-600 dark:text-indigo-400 font-bold text-xs uppercase tracking-wider">
                <MessageSquare size={16} />
                <span>LxI Author Question</span>
              </div>
              <p className="text-xs text-slate-700 dark:text-slate-300 leading-relaxed font-medium">
                {lxiQuestion}
              </p>
            </div>
          )}
        </aside>

        {/* Main Content */}
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

            {/* LeD: Video & Reflection Checkpoints */}
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

                {/* Reflection Checkpoint List */}
                {reflectionSpots.map((spot, idx) => (
                  <div key={idx} className="p-5 rounded-2xl bg-indigo-50 dark:bg-indigo-950/40 border border-indigo-200 dark:border-indigo-800/80 flex items-start gap-4">
                    <div className="p-2.5 rounded-xl bg-brand text-white shrink-0">
                      <HelpCircle size={20} />
                    </div>
                    <div>
                      <span className="text-[11px] font-extrabold uppercase tracking-wider text-indigo-600 dark:text-indigo-400">
                        LeD Reflection Spot #{idx + 1} (At ~{spot.timestampSeconds || 45}s)
                      </span>
                      <p className="text-sm font-semibold text-slate-900 dark:text-white mt-0.5">
                        {spot.prompt}
                      </p>
                    </div>
                  </div>
                ))}
              </div>
            )}

            {/* Content Text / Transcript */}
            <div className="prose dark:prose-invert max-w-none pt-4 border-t border-slate-100 dark:border-slate-800">
              <p className="whitespace-pre-line text-slate-700 dark:text-slate-300 text-lg leading-8">
                {lesson.content || led.transcript}
              </p>
            </div>

            {/* LbD Quiz & Subjective Desks */}
            <div className="pt-8 border-t border-slate-200 dark:border-slate-800 space-y-8">
              <div className="flex items-center gap-2">
                <CheckSquare className="text-brand dark:text-indigo-400" size={24} />
                <h3 className="text-xl font-extrabold text-slate-900 dark:text-white">LbD Practice & Quiz Desk</h3>
              </div>

              {/* MCQs */}
              {mcqs.map((mcqItem, mIdx) => (
                <div key={mIdx} className="p-6 rounded-2xl bg-slate-50 dark:bg-slate-850 border border-slate-200 dark:border-slate-800 space-y-4">
                  <span className="text-xs font-bold uppercase tracking-wider text-slate-500 dark:text-slate-400">Multiple Choice Question #{mIdx + 1}</span>
                  <h4 className="text-base font-bold text-slate-900 dark:text-white">{mcqItem.question}</h4>
                  
                  <div className="grid gap-3">
                    {mcqItem.choices?.map((choice, cIdx) => {
                      const isSelected = selectedChoices[mIdx] === cIdx;
                      const isCorrect = mcqItem.correctIndex === cIdx;
                      const feedback = mcqItem.feedbacks?.[cIdx];

                      return (
                        <div key={cIdx} className="space-y-2">
                          <button
                            type="button"
                            onClick={() => {
                              setSelectedChoices({ ...selectedChoices, [mIdx]: cIdx });
                              track('MCQ_ANSWERED', {
                                component: 'LbDQuiz',
                                eventContext: choice,
                                metadata: { questionIndex: mIdx, optionIndex: cIdx, isCorrect }
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

                          {isSelected && feedback && (
                            <div className={`p-3 rounded-lg text-xs font-medium ${isCorrect ? 'bg-emerald-100/60 dark:bg-emerald-900/30 text-emerald-800 dark:text-emerald-300' : 'bg-rose-100/60 dark:bg-rose-900/30 text-rose-800 dark:text-rose-300'}`}>
                              <strong>Author Feedback for Option {cIdx + 1}:</strong> {feedback}
                            </div>
                          )}
                        </div>
                      );
                    })}
                  </div>
                </div>
              ))}

              {/* Subjectives */}
              {subjectives.map((sub, sIdx) => (
                <div key={sIdx} className="p-6 rounded-2xl bg-slate-50 dark:bg-slate-850 border border-slate-200 dark:border-slate-800 space-y-4">
                  <span className="text-xs font-bold uppercase tracking-wider text-slate-500 dark:text-slate-400">Subjective Reflection Question #{sIdx + 1}</span>
                  <h4 className="text-base font-bold text-slate-900 dark:text-white">{sub.prompt}</h4>
                  
                  <textarea
                    rows={3}
                    value={subjectiveAnswers[sIdx] || ''}
                    onChange={(e) => setSubjectiveAnswers({ ...subjectiveAnswers, [sIdx]: e.target.value })}
                    placeholder="Type your answer here..."
                    className="w-full rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 p-4 text-sm text-slate-900 dark:text-white"
                  />

                  <button
                    type="button"
                    onClick={() => setRevealedExemplars({ ...revealedExemplars, [sIdx]: !revealedExemplars[sIdx] })}
                    className="inline-flex items-center gap-2 text-xs font-bold text-brand dark:text-indigo-400 hover:underline"
                  >
                    {revealedExemplars[sIdx] ? <EyeOff size={14} /> : <Eye size={14} />}
                    {revealedExemplars[sIdx] ? 'Hide Author Feedback / Correct Answer' : 'View Author Feedback / Correct Exemplar Answer'}
                  </button>

                  {revealedExemplars[sIdx] && (
                    <div className="p-4 rounded-xl bg-indigo-50 dark:bg-indigo-950/40 border border-indigo-200 dark:border-indigo-800 text-xs text-indigo-900 dark:text-indigo-200 leading-relaxed font-medium">
                      <strong>Author Feedback & Correct Answer:</strong>
                      <p className="mt-1">{sub.exemplarAnswer}</p>
                    </div>
                  )}
                </div>
              ))}
            </div>

            {/* LxT Extra Material Trajectories */}
            {lxtList.length > 0 && lxtList[0].title && (
              <div className="pt-6 border-t border-slate-200 dark:border-slate-800 space-y-4">
                <div className="flex items-center gap-2">
                  <Link2 className="text-brand dark:text-indigo-400" size={20} />
                  <h4 className="font-extrabold text-base text-slate-900 dark:text-white">LxT: Extension Trajectories & Extra Material</h4>
                </div>
                <div className="grid gap-3">
                  {lxtList.map((item, i) => (
                    <a
                      key={i}
                      href={item.url || '#'}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="p-4 rounded-xl bg-slate-50 dark:bg-slate-850 border border-slate-200 dark:border-slate-800 hover:border-brand flex items-center justify-between transition-all"
                    >
                      <div>
                        <span className="text-sm font-semibold text-slate-900 dark:text-white">{item.title}</span>
                        <span className="ml-2 text-[10px] uppercase font-bold text-brand bg-brand/10 px-2 py-0.5 rounded-full">{item.extraType || 'Resource'}</span>
                      </div>
                      <ArrowRight size={16} className="text-brand dark:text-indigo-400" />
                    </a>
                  ))}
                </div>
              </div>
            )}

            {/* Footer Nav */}
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
