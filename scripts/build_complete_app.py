import os
import json

output_file = "/Users/rushilbhat/Desktop/learning-companion-studio/client/public/Learning_Companion_Studio.html"

# We will generate the complete, production-grade, responsive single-page application.
# It covers all 8 client deliverables:
# 1. Mobile phone responsiveness (adaptive header, responsive layout, mobile slide-up checkpoint modal)
# 2. Save as Draft before directly publishing (Draft vs Live state in localStorage, draft status banner, revert)
# 3. Edit & Delete module and submodule (with confirmation modals)
# 4. Multi-modal PDF viewer with embedded checkpoint reflection stops
# 5. Fix LxI stale response bug (clears answers when prompt changes, resets user answer state)
# 6. Module-scoped LxI discussion spaces (localized per module, not a single global feed)
# 7. Video removable/optional in authoring & learning views (clean non-video layout)
# 8. Admin Dashboard to monitor LC attempts, scores, and answer inspection

html_content = r'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
  <title>Learning Companion Studio — Neurodivergent Mentorship Training Platform</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <script>
    tailwind.config = {
      darkMode: 'class',
      theme: {
        extend: {
          colors: {
            brand: '#0f766e',
            'brand-hover': '#0d9488',
          }
        }
      }
    }
  </script>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
  <style>
    body { font-family: 'Plus Jakarta Sans', sans-serif; -webkit-tap-highlight-color: transparent; }
    /* Mobile-optimized smooth scrollbar */
    ::-webkit-scrollbar { width: 6px; height: 6px; }
    ::-webkit-scrollbar-track { background: #f1f5f9; }
    ::-webkit-scrollbar-thumb { background: #cbd5e1; rounded: 9999px; }
    ::-webkit-scrollbar-thumb:hover { background: #94a3b8; }
  </style>
</head>
<body class="bg-slate-50 text-slate-900 min-h-screen flex flex-col antialiased selection:bg-teal-500 selection:text-white">

  <!-- ==================== HEADER ==================== -->
  <header class="sticky top-0 z-40 border-b border-slate-200 bg-white/95 backdrop-blur-md transition-all shadow-sm">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 py-2.5 sm:py-0 min-h-16 flex flex-wrap items-center justify-between gap-3">
      
      <!-- Brand Logo -->
      <div class="flex items-center gap-3 cursor-pointer group" onclick="goHome()">
        <div class="h-10 w-10 rounded-2xl bg-teal-700 flex items-center justify-center text-white font-black text-lg shadow-md shadow-teal-700/20 group-hover:scale-105 transition-transform">
          LC
        </div>
        <div>
          <div class="flex items-center gap-2">
            <h1 class="font-extrabold text-slate-900 leading-none text-base tracking-tight">Learning Companion Studio</h1>
            <span class="hidden sm:inline-flex px-2 py-0.5 rounded-full bg-teal-50 border border-teal-200 text-teal-800 text-[10px] font-black uppercase">v2.0</span>
          </div>
          <p class="text-[11px] font-semibold text-teal-700 mt-0.5">Neurodivergent Mentorship Training • InclusiveMinds</p>
        </div>
      </div>

      <!-- 3-Way Responsive View Switcher -->
      <nav class="flex items-center gap-1 bg-slate-100 p-1 rounded-2xl border border-slate-200 text-xs font-black overflow-x-auto max-w-full">
        <button id="tab-student" onclick="switchView('student')" class="px-3.5 py-2 rounded-xl transition-all bg-teal-700 text-white shadow-sm flex items-center gap-1.5 whitespace-nowrap">
          <span>🎓</span> <span class="hidden xs:inline">Companion</span><span>View</span>
        </button>
        <button id="tab-author" onclick="switchView('author')" class="px-3.5 py-2 rounded-xl transition-all text-slate-600 hover:text-slate-900 flex items-center gap-1.5 whitespace-nowrap">
          <span>✏️</span> <span>Authoring</span><span class="hidden sm:inline">Desk</span>
          <span id="nav-draft-indicator" class="hidden w-2 h-2 rounded-full bg-amber-500 animate-pulse"></span>
        </button>
        <button id="tab-admin" onclick="switchView('admin')" class="px-3.5 py-2 rounded-xl transition-all text-slate-600 hover:text-slate-900 flex items-center gap-1.5 whitespace-nowrap">
          <span>📊</span> <span>Admin</span><span class="hidden sm:inline">Dashboard</span>
        </button>
      </nav>

    </div>
  </header>

  <!-- GLOBAL FLOATING TOAST NOTIFICATION -->
  <div id="global-toast-container" class="fixed top-20 right-4 sm:right-8 z-50 pointer-events-none transition-all duration-300">
    <div id="publish-toast" class="hidden pointer-events-auto max-w-md p-4 rounded-2xl bg-slate-900 text-white border border-teal-500/40 shadow-2xl text-xs sm:text-sm font-bold flex items-center gap-3 backdrop-blur-md transition-all">
      <span class="text-lg">🔔</span>
      <span id="publish-toast-msg" class="leading-snug">🎉 <strong>Published!</strong> All changes published to LC View.</span>
      <button type="button" onclick="document.getElementById('publish-toast').classList.add('hidden')" class="text-xs font-bold text-teal-400 hover:text-white ml-auto">✕</button>
    </div>
  </div>

  <!-- ==================== MAIN CONTAINER ==================== -->
  <main class="max-w-7xl mx-auto px-4 sm:px-6 py-6 sm:py-8 flex-grow w-full">

    <!-- ========================================================================= -->
    <!-- VIEW 1: AUTHORING DESK (WITH DRAFT / PUBLISH STATE & EDIT/DELETE MODULES) -->
    <!-- ========================================================================= -->
    <section id="view-author" class="hidden space-y-6">

      <!-- DRAFT NOTIFICATION & PUBLISHING CONTROLS BANNER -->
      <div id="author-state-banner" class="rounded-3xl p-5 sm:p-6 border transition-all flex flex-col lg:flex-row lg:items-center justify-between gap-4 bg-slate-900 text-white border-slate-800 shadow-xl">
        <div class="space-y-1">
          <div class="flex items-center gap-2">
            <span class="text-xs font-black uppercase tracking-wider text-teal-400">Creator Desk</span>
            <span id="author-draft-badge" class="px-2.5 py-0.5 rounded-full text-[10px] font-black uppercase bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">
              ✓ Published & Live
            </span>
          </div>
          <h2 class="text-2xl sm:text-3xl font-extrabold tracking-tight">Course Authoring Studio</h2>
          <p id="author-draft-desc" class="text-slate-400 text-xs sm:text-sm">
            Configure video links, PDF reading guides with checkpoints, module-scoped LxI discussions, and master quizzes.
          </p>
        </div>

        <!-- Action Buttons: Save Draft vs Publish vs Discard -->
        <div class="flex flex-wrap items-center gap-2 sm:gap-3">
          <button type="button" onclick="saveAuthorDraft()" class="px-4 py-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 font-bold text-xs flex items-center gap-1.5 shadow-sm transition-all">
            <span>💾</span> <span>Save as Draft</span>
          </button>
          <button type="button" onclick="discardAuthorDraft()" id="btn-discard-draft" class="hidden px-3.5 py-2.5 rounded-xl bg-rose-950/40 hover:bg-rose-900/60 text-rose-300 border border-rose-800/40 font-bold text-xs flex items-center gap-1.5 transition-all">
            <span>↺</span> <span>Discard Draft</span>
          </button>
          <button type="button" onclick="publishContent()" class="px-5 py-2.5 rounded-xl bg-teal-600 hover:bg-teal-500 text-white font-extrabold text-xs shadow-lg shadow-teal-600/30 flex items-center gap-1.5 transition-all">
            <span>🚀</span> <span>Publish Live to LC View</span>
          </button>
        </div>
      </div>

      <!-- MODULE & SUBMODULE MANAGEMENT CARD (WITH EDIT & DELETE) -->
      <div class="bg-white p-5 sm:p-6 rounded-3xl border border-slate-200 shadow-sm space-y-5">
        <div class="flex items-center justify-between border-b border-slate-100 pb-3">
          <div class="flex items-center gap-2">
            <span class="text-lg">🗂️</span>
            <h3 class="text-sm font-black uppercase tracking-wider text-slate-800">Module & Submodule Lifecycle Manager</h3>
          </div>
          <span class="text-[11px] text-slate-400 font-bold">Edit metadata, add or delete modules</span>
        </div>

        <div class="grid md:grid-cols-2 gap-5">
          <!-- Module Selector & Actions -->
          <div class="space-y-2">
            <div class="flex items-center justify-between">
              <label class="text-xs font-black uppercase tracking-wider text-slate-500">1. Select / Manage Module</label>
              <div class="flex items-center gap-1.5">
                <button type="button" onclick="addNewModule()" class="text-[11px] font-black bg-teal-700 text-white px-2.5 py-1 rounded-lg hover:bg-teal-600 shadow-sm">
                  + Add Module
                </button>
                <button type="button" onclick="confirmDeleteCurrentModule()" id="btn-delete-module" class="text-[11px] font-black bg-rose-50 text-rose-700 border border-rose-200 px-2.5 py-1 rounded-lg hover:bg-rose-100">
                  🗑️ Delete Module
                </button>
              </div>
            </div>
            <select id="author-module-select" onchange="onAuthorModuleChange()" class="w-full rounded-2xl border border-slate-200 bg-slate-50 px-4 py-2.5 text-xs sm:text-sm font-bold text-slate-900 focus:bg-white focus:outline-none focus:ring-2 focus:ring-teal-500/20"></select>
          </div>

          <!-- Submodule Selector & Actions -->
          <div class="space-y-2">
            <div class="flex items-center justify-between">
              <label class="text-xs font-black uppercase tracking-wider text-slate-500">2. Select / Manage Submodule</label>
              <div class="flex items-center gap-1.5">
                <button type="button" onclick="addNewSubmodule()" class="text-[11px] font-black bg-teal-50 text-teal-800 border border-teal-200 px-2.5 py-1 rounded-lg hover:bg-teal-100">
                  + Add Submodule
                </button>
                <button type="button" onclick="confirmDeleteCurrentSubmodule()" id="btn-delete-submodule" class="text-[11px] font-black bg-rose-50 text-rose-700 border border-rose-200 px-2.5 py-1 rounded-lg hover:bg-rose-100">
                  🗑️ Delete Submodule
                </button>
              </div>
            </div>
            <select id="author-submodule-select" onchange="onAuthorSubmoduleChange()" class="w-full rounded-2xl border border-slate-200 bg-slate-50 px-4 py-2.5 text-xs sm:text-sm font-bold text-slate-900 focus:bg-white focus:outline-none focus:ring-2 focus:ring-teal-500/20"></select>
          </div>
        </div>

        <!-- Live Metadata Editor Fields -->
        <div class="pt-4 border-t border-slate-100 grid sm:grid-cols-2 lg:grid-cols-4 gap-3">
          <div>
            <label class="block text-[10px] font-black uppercase tracking-wider text-slate-400 mb-1">Module Title</label>
            <input id="author-mod-title" type="text" oninput="markDraftDirty(); updateModuleMeta();" class="w-full rounded-xl border border-slate-200 px-3 py-2 text-xs font-bold bg-slate-50 focus:bg-white focus:border-teal-500" />
          </div>
          <div>
            <label class="block text-[10px] font-black uppercase tracking-wider text-slate-400 mb-1">Submodule Title</label>
            <input id="author-sub-title" type="text" oninput="markDraftDirty(); updateSubmoduleTitle();" class="w-full rounded-xl border border-slate-200 px-3 py-2 text-xs font-bold bg-slate-50 focus:bg-white focus:border-teal-500" />
          </div>
          <div>
            <label class="block text-[10px] font-black uppercase tracking-wider text-slate-400 mb-1">Level Tag</label>
            <input id="author-mod-level" type="text" oninput="markDraftDirty(); updateModuleMeta();" class="w-full rounded-xl border border-slate-200 px-3 py-2 text-xs font-bold bg-slate-50 focus:bg-white focus:border-teal-500" />
          </div>
          <div>
            <label class="block text-[10px] font-black uppercase tracking-wider text-slate-400 mb-1">Module Description</label>
            <input id="author-mod-desc" type="text" oninput="markDraftDirty(); updateModuleMeta();" class="w-full rounded-xl border border-slate-200 px-3 py-2 text-xs font-medium bg-slate-50 focus:bg-white focus:border-teal-500" />
          </div>
        </div>
      </div>

      <!-- COMPACT TABBED AUTHORING DESK -->
      <div class="flex items-center gap-2 border-b border-slate-200 pb-3 overflow-x-auto text-xs font-black">
        <button id="auth-tab-btn-led" onclick="setAuthorTab('led')" class="px-4 py-2.5 rounded-2xl transition-all bg-teal-700 text-white shadow-md whitespace-nowrap">
          🎬 LeD & PDF: Content & Checkpoints
        </button>
        <button id="auth-tab-btn-lxt" onclick="setAuthorTab('lxt')" class="px-4 py-2.5 rounded-2xl transition-all bg-white text-slate-600 hover:bg-slate-100 border border-slate-200 whitespace-nowrap">
          🚀 LxT: Multi-Video Extension Trajectory
        </button>
        <button id="auth-tab-btn-master" onclick="setAuthorTab('master')" class="px-4 py-2.5 rounded-2xl transition-all bg-white text-slate-600 hover:bg-slate-100 border border-slate-200 whitespace-nowrap">
          🎓 Master Quiz: End-of-Module Assessment
        </button>
        <button id="auth-tab-btn-lxi" onclick="setAuthorTab('lxi')" class="px-4 py-2.5 rounded-2xl transition-all bg-white text-slate-600 hover:bg-slate-100 border border-slate-200 whitespace-nowrap">
          💬 Module-Scoped LxI Discussion
        </button>
      </div>

      <!-- PANEL 1: LED & MULTI-MODAL CONTENT (VIDEO / PDF / HYBRID) -->
      <div id="auth-panel-led" class="bg-white p-5 sm:p-8 rounded-3xl border border-slate-200 shadow-sm space-y-6">
        <div class="flex flex-col sm:flex-row sm:items-center justify-between border-b border-slate-100 pb-4 gap-3">
          <div>
            <span class="text-xs font-extrabold uppercase tracking-wider text-teal-700">🎬 Submodule Multi-Modal Lessons</span>
            <h3 class="text-lg font-extrabold text-slate-900 mt-0.5">Content Formats & Checkpoints Configurator</h3>
            <p class="text-xs text-slate-500">Supports Videos, PDF documents with checkpoints, or text-only scenarios. Video is completely optional.</p>
          </div>
          <div class="flex items-center gap-2">
            <button type="button" onclick="addVideoStepToSubmodule('video')" class="text-xs font-extrabold bg-teal-700 text-white px-3.5 py-2 rounded-xl hover:bg-teal-600 shadow-sm">
              + Add Video Step
            </button>
            <button type="button" onclick="addVideoStepToSubmodule('pdf')" class="text-xs font-extrabold bg-indigo-50 text-indigo-700 border border-indigo-200 px-3.5 py-2 rounded-xl hover:bg-indigo-100 shadow-sm">
              + Add PDF Step
            </button>
          </div>
        </div>

        <div id="author-video-steps-container" class="space-y-6"></div>
      </div>

      <!-- PANEL 2: LXT MULTI-VIDEO EXTENSION TRAJECTORY -->
      <div id="auth-panel-lxt" class="hidden bg-white p-5 sm:p-8 rounded-3xl border border-teal-200 shadow-sm space-y-6">
        <div class="flex flex-col sm:flex-row sm:items-center justify-between border-b border-teal-200/60 pb-4 gap-3">
          <div>
            <span class="text-xs font-extrabold uppercase tracking-wider text-teal-800">🚀 LxT Extension Trajectory</span>
            <h3 class="text-lg font-extrabold text-slate-900 mt-0.5">Multi-Video Extension Lessons & Reflection Configurator</h3>
            <p class="text-xs text-slate-500">Unlocked for companions ONLY after completing the main submodule lesson.</p>
          </div>
          <button type="button" onclick="addLxTVideoLink()" class="text-xs font-extrabold bg-teal-700 text-white px-4 py-2 rounded-xl hover:bg-teal-600">
            + Add LxT Extension Link
          </button>
        </div>

        <div>
          <label class="block text-[11px] font-extrabold uppercase text-teal-800 mb-1">LxT Extension Title</label>
          <input id="author-lxt-title" type="text" oninput="markDraftDirty(); updateLxTMeta();" class="w-full rounded-xl border border-teal-200 px-3 py-2 text-xs font-bold bg-slate-50" placeholder="LxT Extension Lesson Title..." />
        </div>

        <div id="author-lxt-steps-container" class="space-y-6"></div>
      </div>

      <!-- PANEL 3: END-OF-MODULE MASTER QUIZ -->
      <div id="auth-panel-master" class="hidden bg-white p-5 sm:p-8 rounded-3xl border border-slate-200 shadow-sm space-y-6">
        <div class="flex flex-col sm:flex-row sm:items-center justify-between border-b border-slate-100 pb-4 gap-3">
          <div>
            <span class="text-xs font-extrabold uppercase tracking-wider text-indigo-700">🎓 End-of-Module Assessment</span>
            <h3 class="text-lg font-extrabold text-slate-900 mt-0.5">Master Quiz Configurator</h3>
            <p class="text-xs text-slate-500">Configure final comprehensive MCQs and Subjective questions for this module.</p>
          </div>
          <div class="flex items-center gap-2">
            <button type="button" onclick="addAuthorMasterMCQ()" class="text-xs font-bold bg-indigo-700 text-white px-3.5 py-2 rounded-xl hover:bg-indigo-600">+ Add Master MCQ</button>
            <button type="button" onclick="addAuthorMasterSubjective()" class="text-xs font-bold bg-indigo-50 text-indigo-700 border border-indigo-200 px-3.5 py-2 rounded-xl hover:bg-indigo-100">+ Add Master Subjective</button>
          </div>
        </div>
        <div id="author-master-quiz-list" class="space-y-4"></div>
      </div>

      <!-- PANEL 4: MODULE-SCOPED LXI DISCUSSION (WITH STALE RESET BUG FIX) -->
      <div id="auth-panel-lxi" class="hidden space-y-6">
        <div class="bg-indigo-900 text-white p-6 sm:p-8 rounded-3xl space-y-4 shadow-md border border-indigo-800">
          <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-indigo-800/80 pb-3">
            <div>
              <span class="text-xs font-bold uppercase tracking-wider text-indigo-300">💬 Module-Scoped LxI Peer Discussion</span>
              <h3 class="text-lg font-extrabold text-white mt-0.5" id="author-lxi-module-header">Configure Module Discussion</h3>
            </div>
            <span class="px-3 py-1 rounded-full bg-indigo-500/20 text-indigo-200 text-xs font-bold border border-indigo-500/30">
              Scoped to Selected Module
            </span>
          </div>
          
          <div class="p-3 bg-amber-500/10 border border-amber-400/30 rounded-2xl text-xs text-amber-200 flex items-start gap-2">
            <span class="text-base">💡</span>
            <span><strong>Anti-Stale Protection:</strong> When you update this question prompt, the system will automatically archive outdated responses so old peer answers never display under a new question prompt.</span>
          </div>

          <div>
            <label class="block text-xs font-bold uppercase tracking-wider text-indigo-200 mb-1.5">Discussion Prompt for this Module</label>
            <textarea id="author-module-lxi-prompt" rows="3" oninput="markDraftDirty()" class="w-full rounded-2xl border border-indigo-700 bg-indigo-950 p-4 text-xs sm:text-sm text-white placeholder-indigo-400 focus:outline-none focus:border-indigo-400 leading-relaxed" placeholder="Set the peer discussion prompt for this module..."></textarea>
          </div>

          <div class="flex items-center justify-between pt-2">
            <span id="author-lxi-save-note" class="text-xs text-indigo-300">Save draft or publish to apply prompt updates.</span>
            <button type="button" onclick="saveModuleLxIPrompt()" class="bg-indigo-600 hover:bg-indigo-500 text-white px-4 py-2 rounded-xl text-xs font-extrabold shadow-sm">
              Save Prompt Update
            </button>
          </div>
        </div>

        <!-- Current Peer Responses in this Module -->
        <div class="bg-white p-6 rounded-3xl border border-slate-200 shadow-sm space-y-4">
          <div class="flex items-center justify-between border-b border-slate-100 pb-3">
            <h4 class="text-xs font-black uppercase text-slate-700">Active Peer Submissions for this Module (<span id="author-lxi-subs-count">0</span>)</h4>
            <button type="button" onclick="clearCurrentModuleLxISubmissions()" class="text-xs font-bold text-rose-600 hover:underline">
              Clear All Responses for this Prompt
            </button>
          </div>
          <div id="author-lxi-submissions-list" class="space-y-2"></div>
        </div>
      </div>

    </section>


    <!-- ========================================================================= -->
    <!-- VIEW 2: LC STUDENT VIEW (COMPANION LEARNING EXPERIENCE) -->
    <!-- ========================================================================= -->
    <section id="view-student" class="space-y-8">
      
      <!-- Responsive Breadcrumb Navigation -->
      <div id="student-breadcrumb" class="flex items-center gap-2 text-xs font-bold text-slate-500 overflow-x-auto whitespace-nowrap py-1">
        <span class="cursor-pointer hover:text-teal-700 transition-colors flex items-center gap-1" onclick="goHome()">
          <span>🏠</span> <span>All Modules</span>
        </span>
        <span id="crumb-module-nav" class="hidden flex items-center gap-2">
          <span>›</span> <span id="crumb-module-title" class="text-slate-900 cursor-pointer hover:underline" onclick="goSubmodules()"></span>
        </span>
        <span id="crumb-sub-nav" class="hidden flex items-center gap-2">
          <span>›</span> <span id="crumb-sub-title" class="text-teal-700 font-extrabold"></span>
        </span>
      </div>

      <!-- LEVEL 1: CATALOG OF MODULES -->
      <div id="student-level-modules" class="space-y-8">
        
        <div class="flex flex-col sm:flex-row sm:items-end justify-between gap-4">
          <div>
            <span class="text-xs font-bold uppercase tracking-wider text-teal-700">Training Catalog</span>
            <h2 class="text-2xl sm:text-3xl font-extrabold text-slate-900 mt-1">Mentorship Training Modules</h2>
            <p class="text-slate-500 text-xs sm:text-sm mt-1">Select a module to view video checkpoints, PDF reading guides, and discussion spaces.</p>
          </div>
          <div class="flex items-center gap-2 text-xs font-bold text-slate-600 bg-white px-3.5 py-2 rounded-2xl border border-slate-200 shadow-sm">
            <span>🛡️ Active Learner:</span> <span class="text-teal-800 font-black">Priya Sharma (Trainee)</span>
          </div>
        </div>

        <!-- Modules Grid -->
        <div id="modules-grid" class="grid sm:grid-cols-2 gap-6"></div>
      </div>

      <!-- LEVEL 2: SUBMODULES LIST & IN-MODULE LXI DISCUSSION -->
      <div id="student-level-submodules" class="hidden space-y-6">
        <div class="flex items-center justify-between">
          <div>
            <button onclick="goHome()" class="text-xs font-bold text-teal-700 mb-2 inline-flex items-center gap-1 hover:underline">
              <span>←</span> <span>Back to All Modules</span>
            </button>
            <h2 id="selected-module-header" class="text-2xl sm:text-3xl font-extrabold text-slate-900">Module Title</h2>
            <p id="selected-module-desc" class="text-slate-500 text-xs sm:text-sm mt-1"></p>
          </div>
        </div>

        <!-- MODULE-SCOPED LXI DISCUSSION CARD (DELIVERABLE #5 & #6) -->
        <div class="bg-gradient-to-r from-indigo-900 via-indigo-950 to-slate-900 text-white p-6 sm:p-8 rounded-3xl shadow-xl space-y-4 border border-indigo-800/80">
          <div class="flex flex-wrap items-center justify-between gap-2">
            <span class="px-3 py-1 rounded-full bg-indigo-500/20 text-indigo-300 text-xs font-black uppercase tracking-wider border border-indigo-500/30">
              💬 In-Module LxI Peer Discussion
            </span>
            <span id="module-lxi-lock-status" class="text-xs font-bold text-amber-300">
              🔒 Peer Answers Hidden (Submit yours first to unlock)
            </span>
          </div>
          <h3 id="module-lxi-question-text" class="text-lg sm:text-xl font-bold text-white leading-snug">
            Discussion prompt loading...
          </h3>
          <div class="space-y-3 pt-2">
            <textarea id="module-lxi-response" rows="2" class="w-full rounded-2xl border border-indigo-700/60 bg-indigo-950/70 p-3.5 sm:p-4 text-xs sm:text-sm text-white placeholder-indigo-300/60 focus:outline-none focus:border-indigo-400" placeholder="Type your practical reflection to unlock peer answers..."></textarea>
            <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
              <span id="module-lxi-status" class="text-xs text-indigo-300 font-semibold"></span>
              <button id="btn-submit-module-lxi" onclick="submitModuleLxIResponse()" class="bg-indigo-600 hover:bg-indigo-500 text-white px-5 py-2.5 rounded-xl text-xs font-bold shadow-md transition-all self-end sm:self-auto">
                Post Reflection & Unlock Peer Answers →
              </button>
            </div>
          </div>

          <!-- Peer Community Answers (Scoped to this module) -->
          <div id="module-lxi-peer-responses" class="pt-4 border-t border-indigo-800/60 space-y-2 hidden">
            <span class="text-[11px] font-bold uppercase text-emerald-300">🔓 Peer Responses for this Module:</span>
            <div id="module-lxi-feed" class="space-y-2 max-h-60 overflow-y-auto pr-1"></div>
          </div>
        </div>

        <div class="pt-2">
          <h3 class="text-sm font-black uppercase tracking-wider text-slate-400 mb-3">Submodule Lessons</h3>
          <div id="submodules-list" class="grid sm:grid-cols-2 gap-4"></div>
        </div>

        <!-- End of Module Master Quiz Card -->
        <div id="master-quiz-card-container" class="p-6 rounded-3xl bg-indigo-50 border border-indigo-200 flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <span class="text-[11px] font-extrabold uppercase tracking-wider text-indigo-700">🎓 Final Module Assessment</span>
            <h4 class="text-lg font-extrabold text-indigo-950 mt-0.5">End-of-Module Master Quiz</h4>
            <p id="master-quiz-lock-desc" class="text-xs text-amber-700 font-bold">🔒 Complete all submodules to unlock the Master Quiz.</p>
          </div>
          <button id="btn-take-master-quiz" disabled onclick="openMasterQuiz()" class="bg-slate-300 text-slate-500 cursor-not-allowed px-5 py-3 rounded-xl text-xs font-extrabold shadow-none whitespace-nowrap">
            🔒 Take Master Quiz (Locked)
          </button>
        </div>
      </div>

      <!-- LEVEL 3: SUBMODULE CONTENT (VIDEO, PDF & REFLECTIONS) -->
      <div id="student-level-content" class="hidden space-y-8">
        <button onclick="goSubmodules()" class="text-xs font-bold text-teal-700 hover:underline inline-flex items-center gap-1">
          <span>←</span> <span>Back to Submodules</span>
        </button>

        <div class="grid lg:grid-cols-4 gap-8">
          <!-- Sidebar: Submodules Outline -->
          <aside class="lg:col-span-1 space-y-6 order-2 lg:order-1">
            <div class="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm space-y-3">
              <h4 class="text-xs font-extrabold uppercase tracking-wider text-slate-400">Submodules Outline</h4>
              <div id="sidebar-submodules-list" class="space-y-1.5"></div>
            </div>
          </aside>

          <!-- Main Content Column -->
          <div class="lg:col-span-3 space-y-8 order-1 lg:order-2">
            <div class="bg-white p-5 sm:p-8 rounded-3xl border border-slate-200 shadow-sm space-y-6">
              
              <header class="flex flex-col sm:flex-row sm:items-center justify-between border-b border-slate-100 pb-4 gap-2">
                <div>
                  <span id="student-module-badge" class="text-xs font-bold uppercase tracking-wider text-teal-700"></span>
                  <h2 id="student-sub-title" class="text-2xl sm:text-3xl font-extrabold text-slate-900 mt-0.5">Submodule Title</h2>
                </div>
                <span id="student-video-step-badge" class="px-3.5 py-1.5 rounded-full bg-teal-50 text-teal-800 text-xs font-black border border-teal-200 self-start sm:self-auto">
                  Step 1 of 1
                </span>
              </header>

              <!-- Multi-Step Selector Bar (Video / PDF Steps) -->
              <div id="student-video-steps-nav" class="flex items-center gap-2 overflow-x-auto pb-2 text-xs font-bold"></div>

              <!-- ========================================== -->
              <!-- MEDIA SECTION A: UNIVERSAL VIDEO PLAYER -->
              <!-- ========================================== -->
              <div id="student-video-container-wrapper" class="space-y-4">
                <div class="relative overflow-hidden rounded-2xl bg-slate-950 aspect-video shadow-md group">
                  <div id="video-player-container" class="w-full h-full"></div>
                  
                  <!-- MOBILE-RESPONSIVE IN-VIDEO CHECKPOINT MODAL (FIXED BOTTOM SLIDE-UP ON PHONES) -->
                  <div id="in-video-checkpoint-modal" class="hidden fixed inset-x-0 bottom-0 sm:absolute sm:inset-0 z-50 bg-slate-950/95 backdrop-blur-md p-5 sm:p-6 flex flex-col justify-between text-white border-t-2 sm:border border-amber-500/40 shadow-2xl max-h-[85vh] sm:max-h-full overflow-y-auto rounded-t-3xl sm:rounded-none"></div>
                </div>

                <!-- Video Completion & Reflection Unlock Banner -->
                <div id="video-completion-banner" class="p-4 rounded-2xl bg-slate-100 border border-slate-200 flex flex-col sm:flex-row sm:items-center justify-between gap-3 transition-all">
                  <div class="space-y-0.5">
                    <span id="video-lock-text" class="text-xs font-bold text-slate-700">
                      🔒 Watch video to the end to unlock reflection questions.
                    </span>
                    <div id="video-progress-bar-container" class="w-48 bg-slate-200 h-1.5 rounded-full overflow-hidden">
                      <div id="video-progress-bar" class="bg-teal-600 h-full w-0 transition-all"></div>
                    </div>
                  </div>
                  <button id="btn-unlock-reflections" disabled onclick="unlockReflections()" class="bg-slate-300 text-slate-500 cursor-not-allowed px-5 py-2.5 rounded-xl text-xs font-extrabold transition-all self-end sm:self-auto">
                    🔒 Watch Video to Unlock Reflections
                  </button>
                </div>
              </div>

              <!-- ========================================== -->
              <!-- MEDIA SECTION B: MULTI-MODAL PDF VIEWER -->
              <!-- ========================================== -->
              <div id="student-pdf-container-wrapper" class="hidden space-y-4">
                <div class="rounded-3xl border-2 border-indigo-200 bg-indigo-50/40 p-5 sm:p-6 space-y-4">
                  <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-indigo-100 pb-4">
                    <div class="flex items-center gap-3">
                      <div class="w-10 h-10 rounded-2xl bg-indigo-600 text-white flex items-center justify-center text-lg font-black shadow-md">
                        📄
                      </div>
                      <div>
                        <span class="text-[10px] font-black uppercase text-indigo-700 tracking-wider">Multi-Modal Learning Resource</span>
                        <h4 id="pdf-doc-title" class="text-base sm:text-lg font-black text-indigo-950">De-escalation Toolkit & Protocol (PDF)</h4>
                      </div>
                    </div>
                    <div class="flex items-center gap-2">
                      <a id="pdf-download-btn" href="#" target="_blank" class="px-3.5 py-2 rounded-xl bg-white border border-indigo-200 text-indigo-800 text-xs font-black shadow-sm hover:bg-indigo-50 flex items-center gap-1.5">
                        <span>📥</span> <span>Open / Download PDF</span>
                      </a>
                    </div>
                  </div>

                  <!-- PDF Document Reader Frame -->
                  <div class="relative w-full h-80 sm:h-96 rounded-2xl overflow-hidden border border-indigo-200 bg-white shadow-inner">
                    <iframe id="pdf-embed-frame" src="" class="w-full h-full border-0"></iframe>
                  </div>

                  <!-- PDF READING CHECKPOINTS CONTAINER -->
                  <div class="space-y-3 pt-2">
                    <div class="flex items-center justify-between">
                      <span class="text-xs font-black uppercase text-indigo-900 flex items-center gap-1.5">
                        <span>⏱️</span> <span>Embedded PDF Reading Checkpoints</span>
                      </span>
                      <span class="text-[11px] font-bold text-indigo-700">Answer checkpoints to complete reading</span>
                    </div>
                    <div id="pdf-checkpoints-list" class="space-y-4"></div>
                  </div>

                  <!-- PDF Completion Banner -->
                  <div id="pdf-completion-banner" class="p-4 rounded-2xl bg-white border border-indigo-200 flex flex-col sm:flex-row sm:items-center justify-between gap-3">
                    <span id="pdf-lock-text" class="text-xs font-bold text-slate-700">
                      📖 Answer all PDF reading checkpoints to unlock final submodule reflections.
                    </span>
                    <button id="btn-unlock-pdf-reflections" disabled onclick="unlockPDFReflections()" class="bg-slate-300 text-slate-500 cursor-not-allowed px-5 py-2.5 rounded-xl text-xs font-extrabold self-end sm:self-auto">
                      🔒 Complete Checkpoints to Unlock
                    </button>
                  </div>
                </div>
              </div>

              <!-- Lecture / Reading Notes -->
              <div class="pt-4 border-t border-slate-100">
                <h4 class="text-xs font-extrabold uppercase text-slate-400 mb-1">Lesson & Lecture Notes</h4>
                <p id="student-transcript-text" class="text-slate-700 text-xs sm:text-sm leading-relaxed whitespace-pre-line"></p>
              </div>

              <!-- POST-LESSON REFLECTIONS (MCQs & SUBJECTIVES) -->
              <div id="student-reflections-section" class="hidden pt-8 border-t border-slate-200 space-y-8">
                <div class="flex items-center gap-2">
                  <span class="text-xl">✍️</span>
                  <div>
                    <h3 class="text-lg sm:text-xl font-extrabold text-slate-900">Post-Lesson Reflections</h3>
                    <p class="text-xs text-slate-500">Reflect on the intervention strategies before moving forward.</p>
                  </div>
                </div>

                <div id="student-mcqs-list" class="space-y-6"></div>
                <div id="student-subjectives-list" class="space-y-6"></div>

                <div class="pt-4 border-t border-slate-200 flex justify-end">
                  <button id="btn-next-step" onclick="finishCurrentVideoStep()" class="bg-teal-700 hover:bg-teal-600 text-white px-6 py-3 rounded-xl text-xs font-extrabold shadow-md transition-all">
                    ✓ Complete Reflections & Proceed →
                  </button>
                </div>
              </div>

              <!-- LXT EXTENSION TRAJECTORY CARD -->
              <div id="student-lxt-card-container" class="pt-8 border-t border-slate-200">
                <div class="p-6 rounded-3xl bg-gradient-to-r from-teal-900 to-slate-900 text-white space-y-4 shadow-lg">
                  <div class="flex items-center justify-between">
                    <span class="px-3 py-1 rounded-full bg-teal-500/20 text-teal-300 text-xs font-extrabold uppercase tracking-wider border border-teal-500/30">
                      🚀 LxT Extension Trajectory
                    </span>
                    <span id="lxt-lock-status" class="text-xs font-bold text-amber-300">
                      🔒 Locked (Complete main submodule lesson first)
                    </span>
                  </div>
                  <h3 id="lxt-card-title" class="text-base sm:text-lg font-extrabold text-white">
                    LxT Extension Trajectory: Advanced Strategy Case Study
                  </h3>
                  <p class="text-xs text-teal-100">
                    An advanced extension lesson featuring multi-video analysis and reflection questions for companions seeking deeper mastery.
                  </p>
                  <button id="btn-launch-lxt" disabled onclick="openLxTExtensionLesson()" class="bg-slate-700 text-slate-400 cursor-not-allowed px-5 py-2.5 rounded-xl text-xs font-extrabold shadow-none transition-all">
                    🔒 Launch LxT Extension (Locked)
                  </button>
                </div>
              </div>

            </div>
          </div>
        </div>

      </div>

      <!-- LEVEL 4: LXT EXTENSION LESSON VIEW -->
      <div id="student-level-lxt-view" class="hidden space-y-8">
        <button onclick="goSubmodules()" class="text-xs font-bold text-teal-700 hover:underline inline-flex items-center gap-1">
          <span>←</span> <span>Back to Submodules</span>
        </button>
        <div class="bg-white p-5 sm:p-8 rounded-3xl border border-slate-200 shadow-sm space-y-6">
          <header class="border-b border-slate-100 pb-4 flex flex-col sm:flex-row sm:items-center justify-between gap-2">
            <div>
              <span class="text-xs font-extrabold uppercase tracking-wider text-teal-700">🚀 LxT Extension Trajectory Lesson</span>
              <h2 id="lxt-view-title" class="text-2xl sm:text-3xl font-extrabold text-slate-900 mt-1">LxT Extension Lesson</h2>
            </div>
            <span id="lxt-video-step-badge" class="px-3.5 py-1.5 rounded-full bg-teal-50 text-teal-800 text-xs font-black border border-teal-200 self-start sm:self-auto">
              LxT Video Link 1 of 2
            </span>
          </header>

          <div id="lxt-video-steps-nav" class="flex items-center gap-2 overflow-x-auto pb-2 text-xs font-bold"></div>

          <div class="space-y-4">
            <div class="relative overflow-hidden rounded-2xl bg-slate-950 aspect-video shadow-md group">
              <div id="lxt-video-player-container" class="w-full h-full"></div>
              <div id="lxt-in-video-checkpoint-modal" class="hidden fixed inset-x-0 bottom-0 sm:absolute sm:inset-0 z-50 bg-slate-950/95 backdrop-blur-md p-5 sm:p-6 flex flex-col justify-between text-white border-t-2 sm:border border-amber-500/40 shadow-2xl max-h-[85vh] sm:max-h-full overflow-y-auto rounded-t-3xl sm:rounded-none"></div>
            </div>

            <div id="lxt-video-completion-banner" class="p-4 rounded-2xl bg-slate-100 border border-slate-200 flex flex-col sm:flex-row sm:items-center justify-between gap-3">
              <span id="lxt-video-lock-text" class="text-xs font-bold text-slate-700">🔒 Watch extension video to unlock questions.</span>
              <button id="btn-unlock-lxt-reflections" disabled onclick="unlockLxTReflections()" class="bg-slate-300 text-slate-500 cursor-not-allowed px-5 py-2.5 rounded-xl text-xs font-extrabold self-end sm:self-auto">
                🔒 Watch Video to Unlock LxT Reflections
              </button>
            </div>
          </div>

          <div class="pt-4 border-t border-slate-100">
            <h4 class="text-xs font-extrabold uppercase text-slate-400 mb-1">Extension Lecture Notes</h4>
            <p id="lxt-transcript-text" class="text-slate-700 text-xs sm:text-sm leading-relaxed whitespace-pre-line"></p>
          </div>

          <div id="lxt-reflections-section" class="hidden pt-8 border-t border-slate-200 space-y-8">
            <div class="flex items-center gap-2">
              <span class="text-xl">✍️</span>
              <h3 class="text-xl font-extrabold text-slate-900">LxT Extension Reflections</h3>
            </div>
            <div id="lxt-mcqs-list" class="space-y-6"></div>
            <div id="lxt-subjectives-list" class="space-y-6"></div>

            <div class="pt-4 border-t border-slate-200 flex justify-end">
              <button id="btn-next-lxt-step" onclick="finishCurrentLxTVideoStep()" class="bg-teal-700 hover:bg-teal-600 text-white px-6 py-3 rounded-xl text-xs font-extrabold shadow-md transition-all">
                ✓ Complete Reflections & Proceed →
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- LEVEL 5: END-OF-MODULE MASTER QUIZ VIEW -->
      <div id="student-level-masterquiz" class="hidden space-y-8">
        <button onclick="goSubmodules()" class="text-xs font-bold text-indigo-700 hover:underline inline-flex items-center gap-1">
          <span>←</span> <span>Back to Submodules</span>
        </button>
        <div class="bg-white p-5 sm:p-8 rounded-3xl border border-slate-200 shadow-sm space-y-6">
          <header class="border-b border-slate-100 pb-4">
            <span class="text-xs font-extrabold uppercase tracking-wider text-indigo-700">Final Assessment</span>
            <h2 id="master-quiz-title" class="text-2xl sm:text-3xl font-extrabold text-slate-900 mt-1">End-of-Module Master Quiz</h2>
            <p class="text-xs text-slate-500 mt-1">Answer all MCQs and Subjective questions below to complete this module certification.</p>
          </header>

          <div id="master-quiz-celebration-banner" class="hidden p-6 rounded-3xl bg-emerald-500 text-white space-y-3 shadow-xl">
            <div class="flex items-center gap-3">
              <span class="text-3xl">🎉</span>
              <div>
                <h3 class="text-xl font-black">Module Master Certification Completed!</h3>
                <p id="master-quiz-score-text" class="text-xs font-bold text-emerald-100">You scored 100% on the End-of-Module Assessment.</p>
              </div>
            </div>
            <div class="pt-2 border-t border-emerald-400/40 flex items-center justify-between">
              <span class="text-xs text-emerald-100 font-semibold">Author Exemplars and Feedbacks revealed below.</span>
              <button onclick="goHome()" class="bg-white text-emerald-900 px-4 py-2 rounded-xl text-xs font-black hover:bg-emerald-50">
                Return to Training Catalog →
              </button>
            </div>
          </div>

          <div id="master-quiz-questions-list" class="space-y-6"></div>

          <div id="master-quiz-submit-container" class="pt-6 border-t border-slate-200 flex justify-end">
            <button id="btn-submit-master-quiz" onclick="submitMasterQuiz()" class="bg-indigo-700 hover:bg-indigo-600 text-white px-8 py-4 rounded-2xl text-sm font-black shadow-xl shadow-indigo-700/20 transition-all cursor-pointer">
              🎓 Submit Master Quiz & Finish Module →
            </button>
          </div>
        </div>
      </div>

    </section>


    <!-- ========================================================================= -->
    <!-- VIEW 3: ADMIN & INSTRUCTOR MONITORING DASHBOARD (DELIVERABLE #8) -->
    <!-- ========================================================================= -->
    <section id="view-admin" class="hidden space-y-8">
      
      <!-- Admin Top Banner -->
      <div class="rounded-3xl bg-slate-900 text-white p-6 sm:p-8 shadow-xl flex flex-col md:flex-row md:items-center justify-between gap-6 border border-slate-800">
        <div class="space-y-1">
          <div class="flex items-center gap-2">
            <span class="text-xs font-bold uppercase tracking-wider text-teal-400">Supervisor Portal</span>
            <span class="px-2.5 py-0.5 rounded-full text-[10px] font-black uppercase bg-teal-500/20 text-teal-300 border border-teal-500/30">
              Live Monitoring
            </span>
          </div>
          <h2 class="text-2xl sm:text-3xl font-extrabold tracking-tight">Companion Attempt & Progress Analytics</h2>
          <p class="text-slate-400 text-xs sm:text-sm">
            Monitor real-time de-escalation practice attempts, video reflections, PDF checkpoints, and quiz mastery across trainee companions.
          </p>
        </div>

        <div class="flex flex-wrap items-center gap-2.5">
          <button type="button" onclick="simulateCompanionAttempt()" class="px-4 py-2.5 rounded-xl bg-teal-600 hover:bg-teal-500 text-white font-black text-xs shadow-md shadow-teal-600/20 flex items-center gap-1.5 transition-all">
            <span>⚡</span> <span>Simulate LC Attempt</span>
          </button>
          <button type="button" onclick="exportAttemptsCSV()" class="px-4 py-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 font-bold text-xs flex items-center gap-1.5 transition-all">
            <span>📥</span> <span>Export CSV</span>
          </button>
          <button type="button" onclick="resetAttemptsLog()" class="px-3.5 py-2.5 rounded-xl bg-rose-950/40 hover:bg-rose-900/60 text-rose-300 border border-rose-800/40 font-bold text-xs transition-all">
            <span>🗑️</span>
          </button>
        </div>
      </div>

      <!-- KPI METRIC SUMMARY CARDS -->
      <div class="grid grid-cols-2 lg:grid-cols-4 gap-4 sm:gap-6">
        <div class="bg-white p-5 rounded-3xl border border-slate-200 shadow-sm space-y-2">
          <div class="flex items-center justify-between text-slate-400 text-xs font-bold uppercase">
            <span>Companions</span>
            <span class="text-base">👥</span>
          </div>
          <div class="text-2xl sm:text-3xl font-black text-slate-900" id="admin-kpi-companions">5</div>
          <p class="text-[11px] text-teal-700 font-bold">InclusiveMinds Cohort</p>
        </div>

        <div class="bg-white p-5 rounded-3xl border border-slate-200 shadow-sm space-y-2">
          <div class="flex items-center justify-between text-slate-400 text-xs font-bold uppercase">
            <span>Total Attempts</span>
            <span class="text-base">⏱️</span>
          </div>
          <div class="text-2xl sm:text-3xl font-black text-slate-900" id="admin-kpi-attempts">0</div>
          <p class="text-[11px] text-teal-700 font-bold">In-Video & PDF Reflections</p>
        </div>

        <div class="bg-white p-5 rounded-3xl border border-slate-200 shadow-sm space-y-2">
          <div class="flex items-center justify-between text-slate-400 text-xs font-bold uppercase">
            <span>Mastery Pass Rate</span>
            <span class="text-base">🎯</span>
          </div>
          <div class="text-2xl sm:text-3xl font-black text-emerald-600" id="admin-kpi-passrate">100%</div>
          <p class="text-[11px] text-slate-500 font-medium">Scored above 80%</p>
        </div>

        <div class="bg-white p-5 rounded-3xl border border-slate-200 shadow-sm space-y-2">
          <div class="flex items-center justify-between text-slate-400 text-xs font-bold uppercase">
            <span>Modules Certified</span>
            <span class="text-base">🎓</span>
          </div>
          <div class="text-2xl sm:text-3xl font-black text-indigo-600" id="admin-kpi-quizzes">0</div>
          <p class="text-[11px] text-indigo-700 font-bold">Master Quizzes Completed</p>
        </div>
      </div>

      <!-- INTERACTIVE ATTEMPTS LOG TABLE & FILTERS -->
      <div class="bg-white p-5 sm:p-6 rounded-3xl border border-slate-200 shadow-sm space-y-4">
        <div class="flex flex-col md:flex-row md:items-center justify-between gap-3 border-b border-slate-100 pb-4">
          <div>
            <h3 class="text-base font-extrabold text-slate-900">Live Companion Activity Log</h3>
            <p class="text-xs text-slate-500">Inspect individual answers, scores, and reflection submissions.</p>
          </div>

          <!-- Filters -->
          <div class="flex flex-wrap items-center gap-2 text-xs">
            <select id="admin-filter-companion" onchange="renderAdminAttemptsTable()" class="rounded-xl border border-slate-200 bg-slate-50 px-3 py-1.5 font-bold text-slate-700">
              <option value="ALL">All Companions</option>
              <option value="Priya Sharma (Trainee)">Priya Sharma</option>
              <option value="Rahul Mehta">Rahul Mehta</option>
              <option value="Tanya Verma">Tanya Verma</option>
              <option value="Jamson">Jamson</option>
            </select>

            <select id="admin-filter-type" onchange="renderAdminAttemptsTable()" class="rounded-xl border border-slate-200 bg-slate-50 px-3 py-1.5 font-bold text-slate-700">
              <option value="ALL">All Activity Types</option>
              <option value="IN_VIDEO_CHECKPOINT">In-Video Reflection (LeD)</option>
              <option value="PDF_CHECKPOINT">PDF Reading Checkpoint</option>
              <option value="MASTER_QUIZ">Master Quiz</option>
              <option value="LXI_DISCUSSION">Module LxI Post</option>
            </select>
          </div>
        </div>

        <!-- Table Container -->
        <div class="overflow-x-auto">
          <table class="w-full text-left text-xs text-slate-700">
            <thead class="bg-slate-50 text-[10px] font-black uppercase tracking-wider text-slate-400 border-b border-slate-100">
              <tr>
                <th class="p-3.5">Learning Companion</th>
                <th class="p-3.5">Activity & Question</th>
                <th class="p-3.5">Module Scope</th>
                <th class="p-3.5">Timestamp</th>
                <th class="p-3.5">Status / Score</th>
                <th class="p-3.5 text-right">Action</th>
              </tr>
            </thead>
            <tbody id="admin-attempts-tbody" class="divide-y divide-slate-100"></tbody>
          </table>
        </div>
      </div>

    </section>

  </main>

  <!-- ==================== INSPECT ATTEMPT MODAL ==================== -->
  <div id="admin-inspect-modal" class="hidden fixed inset-0 z-50 bg-slate-950/80 backdrop-blur-sm p-4 flex items-center justify-center">
    <div class="bg-white w-full max-w-xl rounded-3xl p-6 shadow-2xl space-y-4 max-h-[90vh] overflow-y-auto">
      <div class="flex items-center justify-between border-b border-slate-100 pb-3">
        <div class="flex items-center gap-2">
          <span class="text-lg">🔍</span>
          <h3 class="text-sm font-black uppercase text-slate-800">Companion Response Inspection</h3>
        </div>
        <button onclick="closeAdminInspectModal()" class="text-slate-400 hover:text-slate-700 text-lg font-bold">✕</button>
      </div>

      <div class="space-y-3 text-xs" id="admin-inspect-content"></div>

      <div class="pt-3 border-t border-slate-100 flex justify-end">
        <button onclick="closeAdminInspectModal()" class="px-4 py-2 bg-slate-100 hover:bg-slate-200 text-slate-700 font-bold rounded-xl text-xs">
          Close Window
        </button>
      </div>
    </div>
  </div>

  <!-- ==================== DELETE CONFIRMATION MODAL ==================== -->
  <div id="delete-confirm-modal" class="hidden fixed inset-0 z-50 bg-slate-950/80 backdrop-blur-sm p-4 flex items-center justify-center">
    <div class="bg-white w-full max-w-md rounded-3xl p-6 shadow-2xl space-y-4">
      <div class="flex items-center gap-3 text-rose-600">
        <span class="text-2xl">⚠️</span>
        <h3 class="text-base font-black text-slate-900" id="delete-modal-title">Confirm Deletion</h3>
      </div>
      <p class="text-xs text-slate-600 leading-relaxed" id="delete-modal-desc">
        Are you sure you want to delete this? This action cannot be undone.
      </p>
      <div class="pt-2 flex justify-end gap-2">
        <button onclick="closeDeleteModal()" class="px-4 py-2 bg-slate-100 hover:bg-slate-200 text-slate-700 font-bold rounded-xl text-xs">
          Cancel
        </button>
        <button id="btn-confirm-delete-action" onclick="executeDeleteAction()" class="px-4 py-2 bg-rose-600 hover:bg-rose-500 text-white font-extrabold rounded-xl text-xs shadow-md">
          Yes, Delete
        </button>
      </div>
    </div>
  </div>

  <!-- ========================================================================= -->
  <!-- JAVASCRIPT STATE ENGINE & DELIVERABLES LOGIC -->
  <!-- ========================================================================= -->
  <script>
    // ==========================================
    // INITIAL MOCK DATABASE (WITH LCM, PDF & LXI)
    // ==========================================
    const DEFAULT_COURSES = [
      {
        id: "mod-1",
        title: "Module 1: Foundations of Neurodiversity & Strength-Based Mentorship",
        description: "Learn core strategies for mentoring children on the Autism Spectrum, ADHD, and sensory differences.",
        level: "Foundational",
        lxi: {
          questionId: "lxi-mod-1-q1",
          question: "Share a practical de-escalation technique you have used when a mentee shows early signs of sensory overload in a classroom.",
          submissions: [
            { companionName: "Companion Ananya", timestamp: "Today, 10:14 AM", answer: "I immediately lower my vocal volume, dim direct overhead lights, and offer a weighted lap pad without demanding eye contact." },
            { companionName: "Companion Rahul", timestamp: "Today, 11:30 AM", answer: "I match their body positioning by sitting side-by-side on the floor and quietly introduce a 10-second processing pause before asking any follow-up question." }
          ]
        },
        masterQuiz: [
          {
            type: "mcq",
            question: "Master Assessment Q1: What is the core physiological difference between a sensory meltdown and a behavioral tantrum?",
            choices: [
              "Meltdowns are deliberate acts of defiance seeking attention",
              "Meltdowns stem from neurological involuntary sensory overload; tantrums are goal-oriented",
              "Tantrums can be resolved with sensory rooms; meltdowns require strict disciplinary timeout",
              "There is no functional distinction between tantrums and meltdowns"
            ],
            correctIndex: 1,
            feedbacks: [
              "Incorrect. Defiance implies willful intent, which does not define involuntary sensory meltdowns.",
              "Correct! Sensory meltdowns result from central nervous system overload.",
              "Incorrect. Meltdowns require calm co-regulation, not punishment.",
              "Incorrect. Understanding the distinction is the cornerstone of inclusive mentorship."
            ]
          },
          {
            type: "subjective",
            prompt: "Master Assessment Subjective: Outline a 3-step action plan if your mentee experiences sensory overload during a loud school assembly.",
            exemplar: "Author Exemplar Feedback: 1. Prevent escalation by guiding the student calmly to a quiet sensory space. 2. Remove sensory inputs (dim lights, offer noise-canceling headphones). 3. Provide a predictable calming routine without verbal demands until baseline arousal is restored."
          }
        ],
        submodules: [
          {
            id: "sub-1-1",
            title: "Submodule 1.1: Understanding Neurodiversity & Strength-Based Mentoring",
            format: "video", // 'video' | 'pdf' | 'both'
            videoSteps: [
              {
                id: "vstep-1-1-1",
                title: "Video Link 1: Core Principles of Strength-Based Mentoring",
                videoUrl: "https://vjs.zencdn.net/v/oceans.mp4",
                transcript: "Neurodiversity recognizes that brain differences are natural human variations. Companions move away from a deficit model (fixing behavior) to a strength-based model.",
                inVideoCheckpoints: [
                  {
                    id: "ivc-1-1-1",
                    timeMin: 0,
                    timeSec: 15,
                    type: "mcq",
                    question: "Mid-Video Reflection Checkpoint (00:15): What is the core focus when mentoring neurodivergent children?",
                    choices: [
                      "Building on unique strengths & providing sensory accommodations",
                      "Enforcing strict behavioral compliance at all times",
                      "Disallowing communication tools",
                      "Overloading with loud verbal instructions"
                    ],
                    correctIndex: 0,
                    feedbacks: [
                      "Correct! Strength-based focus builds safety and trust.",
                      "Incorrect. Compliance-only approaches increase anxiety.",
                      "Incorrect. Communication tools (AAC/PECS) are vital.",
                      "Incorrect. Lower sensory input is key."
                    ],
                    exemplar: "Author Exemplar Feedback: Focus on building rapport and respecting sensory needs."
                  }
                ],
                mcqs: [
                  {
                    question: "Video Link 1 Reflection: What is the primary goal of strength-based mentoring?",
                    choices: [
                      "Forcing the child to mimic neurotypical social behaviors at all times",
                      "Building upon the child’s unique interests while providing sensory accommodations",
                      "Keeping a rigid strict timeline without flexibility",
                      "Preventing the child from using non-verbal communication aids"
                    ],
                    correctIndex: 1,
                    feedbacks: [
                      "Incorrect. Forcing masking causes high anxiety.",
                      "Correct! Strength-based mentoring fosters trust and respects individual sensory profiles.",
                      "Incorrect. Rigid timelines increase overwhelm.",
                      "Incorrect. Non-verbal communication tools should always be encouraged."
                    ]
                  }
                ],
                subjectives: [
                  {
                    prompt: "Video Link 1 Reflection Subjective: How would you modify your tone if a mentee shows signs of sensory overload?",
                    exemplar: "Author Exemplar Feedback: Lower voice tone, reduce noise/bright lighting, pause task, offer a quiet break."
                  }
                ]
              },
              {
                id: "vstep-1-1-2",
                title: "Video Link 2: Processing Pauses & Non-Verbal Cues",
                videoUrl: "https://vjs.zencdn.net/v/oceans.mp4",
                transcript: "Learn how to adapt communication using 10-second processing pauses.",
                inVideoCheckpoints: [
                  {
                    id: "ivc-1-1-2",
                    timeMin: 0,
                    timeSec: 10,
                    type: "mcq",
                    question: "Mid-Video Reflection Checkpoint (00:10): Why are processing pauses critical?",
                    choices: [
                      "They allow the child's nervous system time to integrate language",
                      "They are used as a disciplinary timeout",
                      "They force the companion to stop listening",
                      "They only help when speaking louder"
                    ],
                    correctIndex: 0,
                    feedbacks: [
                      "Correct! Processing pauses reduce cognitive load significantly.",
                      "Incorrect. Pauses are therapeutic scaffolding, not timeout.",
                      "Incorrect. Companions remain actively observant.",
                      "Incorrect. Louder volume increases overload."
                    ],
                    exemplar: "Author Exemplar Feedback: Processing pauses allow auditory processing without anxiety."
                  }
                ],
                mcqs: [
                  {
                    question: "Video Link 2 Reflection: What is the recommended pause duration after giving an instruction?",
                    choices: [
                      "0 seconds (repeat immediately)",
                      "At least 5 to 10 seconds of calm silence",
                      "30 minutes",
                      "Only pause if the child starts crying"
                    ],
                    correctIndex: 1,
                    feedbacks: [
                      "Incorrect. Immediate repetition restarts the auditory processing clock.",
                      "Correct! 5–10 seconds gives neural circuits time to formulate a response.",
                      "Incorrect. 30 minutes is excessive.",
                      "Incorrect. Proactive pauses prevent tears."
                    ]
                  }
                ],
                subjectives: []
              }
            ],
            lxt: {
              title: "LxT Extension Trajectory: Advanced Assistive Tech & Case Analysis",
              videoSteps: [
                {
                  id: "lxt-step-1",
                  title: "LxT Video 1: Augmentative Communication Devices in the Classroom",
                  videoUrl: "https://vjs.zencdn.net/v/oceans.mp4",
                  transcript: "Advanced guide to PECS, high-tech AAC speech-generating devices, and visual schedules.",
                  inVideoCheckpoints: [
                    {
                      id: "lxt-ivc-1",
                      timeMin: 0,
                      timeSec: 12,
                      type: "mcq",
                      question: "LxT In-Video Reflection (00:12): When should a companion introduce AAC tools?",
                      choices: [
                        "Immediately to support communication without withholding verbal speech",
                        "Only after the child passes a spelling test",
                        "Only as a punishment for silence",
                        "Never in mainstream classrooms"
                      ],
                      correctIndex: 0,
                      feedbacks: [
                        "Correct! AAC supports and often accelerates natural communication.",
                        "Incorrect. AAC has zero prerequisite testing requirements.",
                        "Incorrect. AAC is a fundamental communication right.",
                        "Incorrect. AAC should be integrated everywhere."
                      ],
                      exemplar: "Author Exemplar Feedback: AAC provides an immediate communication pathway."
                    }
                  ],
                  mcqs: [
                    {
                      question: "LxT Reflection: What is a key indicator that an AAC communication device is working?",
                      choices: [
                        "The mentee initiates spontaneous communication requests",
                        "The device is kept in a locked drawer",
                        "The mentee no longer needs adult support",
                        "The device is only touched by the teacher"
                      ],
                      correctIndex: 0,
                      feedbacks: [
                        "Correct! Spontaneous initiation demonstrates functional communication.",
                        "Incorrect. AAC must always be within physical reach.",
                        "Incorrect. Mentorship remains essential.",
                        "Incorrect. The child must have primary agency."
                      ]
                    }
                  ],
                  subjectives: []
                }
              ]
            }
          },
          {
            id: "sub-1-2",
            title: "Submodule 1.2: Multi-Modal Reading Guide — De-escalation & Sensory Toolkits",
            format: "pdf", // PDF BASED SUBMODULE
            pdfDoc: {
              title: "Inclusive Classrooms De-escalation Protocol & Sensory Regulation Guide",
              url: "https://raw.githubusercontent.com/rushilbhat01/learning-companion-studio/main/docs/sample_deescalation_guide.pdf",
              embeddedCheckpoints: [
                {
                  id: "pdf-cp-1",
                  section: "Section 1: Recognizing Early Physiological Arousal",
                  question: "PDF Checkpoint 1: Which of the following is an early physiological indicator of impending sensory overload?",
                  choices: [
                    "Pupil dilation, rapid breathing, and repetitive tactile fidgeting",
                    "Deep calm abdominal breathing",
                    "Engaged cooperative peer play",
                    "Asking politely for more homework"
                  ],
                  correctIndex: 0,
                  feedbacks: [
                    "Correct! Recognizing subtle autonomic signs enables early de-escalation.",
                    "Incorrect. Deep breathing indicates a calm nervous system.",
                    "Incorrect. Cooperative play represents optimal baseline engagement.",
                    "Incorrect. Not an indicator of sensory overwhelm."
                  ],
                  exemplar: "Author Exemplar Feedback: Autonomic signs (breathing rate, fidgeting, motor pacing) precede verbal distress."
                },
                {
                  id: "pdf-cp-2",
                  section: "Section 2: The 3-Step Low-Arousal Co-Regulation Protocol",
                  question: "PDF Checkpoint 2: What is the first priority when initiating low-arousal de-escalation?",
                  choices: [
                    "Demand an immediate verbal explanation of their misbehavior",
                    "Regulate your own vocal tone and minimize ambient sensory inputs",
                    "Call the principal and issue a formal written reprimand",
                    "Restrain the child in their chair"
                  ],
                  correctIndex: 1,
                  feedbacks: [
                    "Incorrect. Demanding explanations elevates cortisol and panic.",
                    "Correct! Adult co-regulation sets the emotional baseline for the child.",
                    "Incorrect. Escort and administrative threats escalate fight-or-flight.",
                    "Incorrect. Physical restraint is dangerous and prohibited."
                  ],
                  exemplar: "Author Exemplar Feedback: Co-regulation precedes de-escalation. Your calm nervous system grounds the student."
                }
              ]
            },
            videoSteps: [], // NO VIDEO! Proves requirement #7
            mcqs: [
              {
                question: "PDF Synthesis: What is the primary purpose of a sensory diet toolkit in a classroom?",
                choices: [
                  "To provide scheduled, proactive sensory inputs that maintain optimal nervous system regulation",
                  "To withhold food until the student completes tasks",
                  "To isolate the student from peers permanently",
                  "To replace academic learning with games"
                ],
                correctIndex: 0,
                feedbacks: [
                  "Correct! Proactive sensory diets prevent arousal spikes before meltdowns occur.",
                  "Incorrect. Sensory diet refers to sensory inputs, not culinary food withholding.",
                  "Incorrect. Inclusion remains the goal.",
                  "Incorrect. Regulation supports academic readiness."
                ]
              }
            ],
            subjectives: [
              {
                prompt: "PDF Synthesis Reflection: Describe how you would customize a sensory break corner for a child sensitive to loud sounds and fluorescent flicker.",
                exemplar: "Author Exemplar Feedback: Use warm indirect desk lamps, acoustic noise-dampening panels or headphones, a beanbag chair facing away from foot traffic, and tactile resistance putty."
              }
            ]
          }
        ]
      },
      {
        id: "mod-2",
        title: "Module 2: Behavioral Support & Calm Co-Regulation Techniques",
        description: "Master calm co-regulation, sensory regulation protocols, and collaborative problem solving for learning companions.",
        level: "Intermediate",
        lxi: {
          questionId: "lxi-mod-2-q1",
          question: "When a mentee refuses an activity due to anxiety, what is one non-punitive phrasing you use to scaffold participation?",
          submissions: [
            { companionName: "Companion Tanya", timestamp: "Yesterday, 3:15 PM", answer: "I say: 'We can do the first problem together, and you can pick whether we use markers or the keyboard.'" }
          ]
        },
        masterQuiz: [
          {
            type: "mcq",
            question: "Module 2 Quiz Q1: Which statement best describes 'Co-Regulation'?",
            choices: [
              "The adult using their own calm physiological state to guide the student back to safety",
              "Giving two commands at once to keep the child busy",
              "Leaving the child alone in an empty room without monitoring",
              "Using louder voices to overpower the child"
            ],
            correctIndex: 0,
            feedbacks: [
              "Correct! Co-regulation is the neurological foundation for self-regulation.",
              "Incorrect. Multiple commands cause auditory overwhelm.",
              "Incorrect. Isolation triggers abandonment panic.",
              "Incorrect. Louder voices escalate autonomic arousal."
            ]
          }
        ],
        submodules: [
          {
            id: "sub-2-1",
            title: "Submodule 2.1: Collaborative Problem Solving & Visual Schedules",
            format: "video",
            videoSteps: [
              {
                id: "vstep-2-1-1",
                title: "Video Link 1: Transition Warnings & Visual Timers",
                videoUrl: "https://vjs.zencdn.net/v/oceans.mp4",
                transcript: "How to use countdown timers and 'First-Then' boards to make transitions predictable and stress-free.",
                inVideoCheckpoints: [
                  {
                    id: "ivc-2-1-1",
                    timeMin: 0,
                    timeSec: 10,
                    type: "mcq",
                    question: "Mid-Video Reflection Checkpoint (00:10): What is the core function of a 'First-Then' visual schedule?",
                    choices: [
                      "It provides predictable visual clarity, reducing the cognitive anxiety of unexpected transitions",
                      "It acts as a bribery mechanism",
                      "It replaces the role of the teacher",
                      "It must only be used in exams"
                    ],
                    correctIndex: 0,
                    feedbacks: [
                      "Correct! Visual structures anchor predictability for neurodivergent minds.",
                      "Incorrect. It is cognitive scaffolding, not bribery.",
                      "Incorrect. It supports the learning companion's co-teaching.",
                      "Incorrect. It applies across all daily routines."
                    ],
                    exemplar: "Author Exemplar Feedback: Predictability lowers transition anxiety significantly."
                  }
                ],
                mcqs: [],
                subjectives: []
              }
            ]
          }
        ]
      }
    ];

    // ==========================================
    // INITIAL MOCK ATTEMPTS FOR ADMIN DASHBOARD
    // ==========================================
    const DEFAULT_ATTEMPTS = [
      {
        id: "att-101",
        companionName: "Priya Sharma (Trainee)",
        type: "IN_VIDEO_CHECKPOINT",
        typeName: "In-Video Reflection (00:15)",
        moduleTitle: "Module 1 • Submodule 1.1",
        question: "What is the core focus when mentoring neurodivergent children?",
        submittedAnswer: "Building on unique strengths & providing sensory accommodations",
        status: "Correct (100%)",
        isCorrect: true,
        timestamp: "Today, 09:15 AM",
        exemplar: "Strength-based focus builds safety and trust without demanding masking."
      },
      {
        id: "att-102",
        companionName: "Rahul Mehta",
        type: "PDF_CHECKPOINT",
        typeName: "PDF Reading Checkpoint #1",
        moduleTitle: "Module 1 • Submodule 1.2",
        question: "Which of the following is an early physiological indicator of impending sensory overload?",
        submittedAnswer: "Pupil dilation, rapid breathing, and repetitive tactile fidgeting",
        status: "Correct (100%)",
        isCorrect: true,
        timestamp: "Today, 08:42 AM",
        exemplar: "Recognizing autonomic signs enables early non-punitive intervention."
      },
      {
        id: "att-103",
        companionName: "Tanya Verma",
        type: "LXI_DISCUSSION",
        typeName: "Module LxI Discussion",
        moduleTitle: "Module 1: Foundations",
        question: "Share a practical de-escalation technique you have used...",
        submittedAnswer: "I match their body positioning and quietly introduce a 10-second processing pause.",
        status: "Submitted & Shared",
        isCorrect: true,
        timestamp: "Yesterday, 04:20 PM",
        exemplar: "Co-regulation and processing pauses lower arousal."
      },
      {
        id: "att-104",
        companionName: "Jamson",
        type: "MASTER_QUIZ",
        typeName: "End-of-Module Master Quiz",
        moduleTitle: "Module 1: Foundations",
        question: "Comprehensive 2-Part Assessment",
        submittedAnswer: "Answered all MCQs & Submitted 3-step Assembly Action Plan",
        status: "Passed (100%)",
        isCorrect: true,
        timestamp: "Yesterday, 02:10 PM",
        exemplar: "Demonstrated full mastery of sensory meltdowns vs tantrums."
      }
    ];

    // ==========================================
    // STATE ENGINE: DRAFT VS PUBLISHED IN LOCALSTORAGE
    // ==========================================
    const STORAGE_KEY_PUBLISHED = "lcs_published_courses_v2";
    const STORAGE_KEY_DRAFT = "lcs_draft_courses_v2";
    const STORAGE_KEY_ATTEMPTS = "lcs_admin_attempts_v2";

    function loadFromStorage(key, fallback) {
      try {
        const item = localStorage.getItem(key);
        return item ? JSON.parse(item) : fallback;
      } catch (e) {
        return fallback;
      }
    }

    function saveToStorage(key, val) {
      try {
        localStorage.setItem(key, JSON.stringify(val));
      } catch (e) {}
    }

    let publishedDb = loadFromStorage(STORAGE_KEY_PUBLISHED, DEFAULT_COURSES);
    let draftDb = loadFromStorage(STORAGE_KEY_DRAFT, JSON.parse(JSON.stringify(publishedDb)));
    let adminAttempts = loadFromStorage(STORAGE_KEY_ATTEMPTS, DEFAULT_ATTEMPTS);

    // Active working pointers
    let currentView = 'student'; // 'student' | 'author' | 'admin'
    let authorActiveTab = 'led';
    let isDraftDirty = JSON.stringify(draftDb) !== JSON.stringify(publishedDb);

    let selectedModuleId = publishedDb[0] ? publishedDb[0].id : "mod-1";
    let selectedSubmodule = (publishedDb[0] && publishedDb[0].submodules[0]) ? publishedDb[0].submodules[0] : null;
    let activeVideoStepIndex = 0;
    let activeLxTVideoStepIndex = 0;

    // Interactive progress tracking maps
    let selectedChoicesMap = {};
    let revealedExemplarsMap = {};
    let videoCompletedMap = {};
    let videoStepFinishedMap = {};
    let lxtVideoCompletedMap = {};
    let lxtVideoStepFinishedMap = {};
    let pdfCheckpointsCompletedMap = {};
    let pdfFinishedMap = {};
    let submoduleFinishedMap = {};
    let masterQuizSubmittedMap = {};
    let moduleLxISubmittedMap = {}; // Scoped per module question

    let currentDeleteTarget = null; // For confirmation modal

    // ==========================================
    // DRAFT & PUBLISH MANAGEMENT (DELIVERABLE #2)
    // ==========================================
    function markDraftDirty() {
      isDraftDirty = true;
      updateAuthorDraftUI();
    }

    function updateAuthorDraftUI() {
      const badge = document.getElementById('author-draft-badge');
      const desc = document.getElementById('author-draft-desc');
      const navDot = document.getElementById('nav-draft-indicator');
      const discardBtn = document.getElementById('btn-discard-draft');

      isDraftDirty = JSON.stringify(draftDb) !== JSON.stringify(publishedDb);

      if (isDraftDirty) {
        if (badge) {
          badge.className = "px-2.5 py-0.5 rounded-full text-[10px] font-black uppercase bg-amber-500/20 text-amber-300 border border-amber-500/40";
          badge.innerText = "⚠️ Draft Mode (Unpublished Edits)";
        }
        if (desc) desc.innerText = "You have unsaved or unpublished draft changes. Click 'Save as Draft' or 'Publish Live'.";
        if (navDot) navDot.classList.remove('hidden');
        if (discardBtn) discardBtn.classList.remove('hidden');
      } else {
        if (badge) {
          badge.className = "px-2.5 py-0.5 rounded-full text-[10px] font-black uppercase bg-emerald-500/20 text-emerald-300 border border-emerald-500/30";
          badge.innerText = "✓ Published & Live";
        }
        if (desc) desc.innerText = "All changes are published and currently live in Companion View.";
        if (navDot) navDot.classList.add('hidden');
        if (discardBtn) discardBtn.classList.add('hidden');
      }
    }

    function saveAuthorDraft() {
      saveToStorage(STORAGE_KEY_DRAFT, draftDb);
      showToast("💾 Draft Saved Locally! Changes are kept in draft and not yet visible to students.");
      updateAuthorDraftUI();
    }

    function discardAuthorDraft() {
      if (!confirm("Discard all uncommitted draft changes and revert back to the live published version?")) return;
      draftDb = JSON.parse(JSON.stringify(publishedDb));
      saveToStorage(STORAGE_KEY_DRAFT, draftDb);
      isDraftDirty = false;
      showToast("↺ Draft discarded. Reverted to live published content.");
      initAuthorDesk();
      updateAuthorDraftUI();
    }

    function publishContent() {
      publishedDb = JSON.parse(JSON.stringify(draftDb));
      saveToStorage(STORAGE_KEY_PUBLISHED, publishedDb);
      saveToStorage(STORAGE_KEY_DRAFT, draftDb);
      isDraftDirty = false;
      
      // Reset answered in-video checkpoints for freshly edited questions
      answeredInVideoCheckpointsMap = {};
      currentActiveInVideoCheckpoint = null;
      const mainModal = document.getElementById('in-video-checkpoint-modal');
      if (mainModal) mainModal.classList.add('hidden');

      showToast("🎉 Published Successfully! All module changes and new checkpoints are now live in Companion View.");
      updateAuthorDraftUI();
      
      // If currently on companion view, re-render
      if (currentView === 'student') {
        goHome();
      }
    }

    function showToast(msg) {
      const toast = document.getElementById('publish-toast');
      const toastMsg = document.getElementById('publish-toast-msg');
      if (toast && toastMsg) {
        toastMsg.innerHTML = msg;
        toast.classList.remove('hidden');
        if (window.toastTimeout) clearTimeout(window.toastTimeout);
        window.toastTimeout = setTimeout(() => {
          toast.classList.add('hidden');
        }, 4500);
      }
    }

    // ==========================================
    // VIEW SWITCHING (STUDENT / AUTHOR / ADMIN)
    // ==========================================
    function switchView(view) {
      currentView = view;
      const vStudent = document.getElementById('view-student');
      const vAuthor = document.getElementById('view-author');
      const vAdmin = document.getElementById('view-admin');

      const tabStudent = document.getElementById('tab-student');
      const tabAuthor = document.getElementById('tab-author');
      const tabAdmin = document.getElementById('tab-admin');

      // Reset tabs
      [tabStudent, tabAuthor, tabAdmin].forEach(b => {
        if (b) b.className = "px-3.5 py-2 rounded-xl transition-all text-slate-600 hover:text-slate-900 flex items-center gap-1.5 whitespace-nowrap";
      });

      [vStudent, vAuthor, vAdmin].forEach(v => {
        if (v) v.classList.add('hidden');
      });

      if (view === 'author') {
        if (vAuthor) vAuthor.classList.remove('hidden');
        if (tabAuthor) tabAuthor.className = "px-3.5 py-2 rounded-xl transition-all bg-teal-700 text-white shadow-sm flex items-center gap-1.5 whitespace-nowrap";
        initAuthorDesk();
      } else if (view === 'admin') {
        if (vAdmin) vAdmin.classList.remove('hidden');
        if (tabAdmin) tabAdmin.className = "px-3.5 py-2 rounded-xl transition-all bg-teal-700 text-white shadow-sm flex items-center gap-1.5 whitespace-nowrap";
        renderAdminDashboard();
      } else {
        if (vStudent) vStudent.classList.remove('hidden');
        if (tabStudent) tabStudent.className = "px-3.5 py-2 rounded-xl transition-all bg-teal-700 text-white shadow-sm flex items-center gap-1.5 whitespace-nowrap";
        goHome();
      }

      updateAuthorDraftUI();
    }

    // ==========================================
    // MODULE & SUBMODULE LIFECYCLE (DELIVERABLE #3)
    // ==========================================
    function addNewModule() {
      const newNum = draftDb.length + 1;
      const newMod = {
        id: `mod-${Date.now()}`,
        title: `Module ${newNum}: New Neurodiversity Intervention Topic`,
        description: "Configure module overview and pedagogical goals.",
        level: "Foundational",
        lxi: {
          questionId: `lxi-mod-${Date.now()}`,
          question: `Module ${newNum} Discussion: Share a practical observation or question about this topic.`,
          submissions: []
        },
        masterQuiz: [
          {
            type: "mcq",
            question: "Sample Master Question: What is the primary co-regulation strategy?",
            choices: ["Option A: Calming presence", "Option B: Strict timeout", "Option C: Ignoring", "Option D: Shouting"],
            correctIndex: 0,
            feedbacks: ["Correct!", "Incorrect.", "Incorrect.", "Incorrect."]
          }
        ],
        submodules: [
          {
            id: `sub-${Date.now()}-1`,
            title: `Submodule ${newNum}.1: Core Principles & Lesson`,
            format: "video",
            videoSteps: [
              {
                id: `vstep-${Date.now()}-1`,
                title: "Lesson 1: Introduction Video",
                videoUrl: "https://vjs.zencdn.net/v/oceans.mp4",
                transcript: "Lesson notes and therapeutic takeaways...",
                inVideoCheckpoints: [
                  {
                    id: `ivc-${Date.now()}-1`,
                    timeMin: 0,
                    timeSec: 15,
                    type: "mcq",
                    question: "Mid-Video Checkpoint (00:15): What is the first priority?",
                    choices: ["Prioritize connection & safety", "Demand immediate compliance", "Leave the area", "Raise voice"],
                    correctIndex: 0,
                    feedbacks: ["Correct!", "Incorrect.", "Incorrect.", "Incorrect."],
                    exemplar: "Connection creates emotional safety."
                  }
                ],
                mcqs: [],
                subjectives: []
              }
            ]
          }
        ]
      };

      draftDb.push(newMod);
      markDraftDirty();
      selectedModuleId = newMod.id;
      initAuthorDesk();
      showToast(`✨ Created "${newMod.title}"! Remember to save draft or publish.`);
    }

    function confirmDeleteCurrentModule() {
      const mod = draftDb.find(m => m.id === selectedModuleId);
      if (!mod) return;
      if (draftDb.length <= 1) {
        alert("You must keep at least one module in the curriculum.");
        return;
      }
      currentDeleteTarget = { type: 'module', id: mod.id, title: mod.title };
      document.getElementById('delete-modal-title').innerText = "Delete Entire Module?";
      document.getElementById('delete-modal-desc').innerHTML = `Are you sure you want to permanently delete <strong>"${mod.title}"</strong> and all of its lessons, checkpoints, and master quizzes?`;
      document.getElementById('delete-confirm-modal').classList.remove('hidden');
    }

    function addNewSubmodule() {
      const mod = draftDb.find(m => m.id === selectedModuleId);
      if (!mod) return;
      const subNum = (mod.submodules ? mod.submodules.length : 0) + 1;
      const newSub = {
        id: `sub-${Date.now()}`,
        title: `Submodule ${mod.submodules.length + 1}: Practical Application`,
        format: "video",
        videoSteps: [
          {
            id: `vstep-${Date.now()}`,
            title: "Lesson 1: Strategy Video",
            videoUrl: "https://vjs.zencdn.net/v/oceans.mp4",
            transcript: "Take notes on de-escalation pacing...",
            inVideoCheckpoints: [],
            mcqs: [],
            subjectives: []
          }
        ]
      };
      if (!mod.submodules) mod.submodules = [];
      mod.submodules.push(newSub);
      markDraftDirty();
      selectedSubmodule = newSub;
      initAuthorDesk();
      showToast(`✨ Added "${newSub.title}" to ${mod.title}.`);
    }

    function confirmDeleteCurrentSubmodule() {
      const mod = draftDb.find(m => m.id === selectedModuleId);
      if (!mod || !selectedSubmodule) return;
      if (mod.submodules.length <= 1) {
        alert("A module must contain at least one submodule lesson.");
        return;
      }
      currentDeleteTarget = { type: 'submodule', moduleId: mod.id, subId: selectedSubmodule.id, title: selectedSubmodule.title };
      document.getElementById('delete-modal-title').innerText = "Delete Submodule Lesson?";
      document.getElementById('delete-modal-desc').innerHTML = `Are you sure you want to delete <strong>"${selectedSubmodule.title}"</strong> from ${mod.title}?`;
      document.getElementById('delete-confirm-modal').classList.remove('hidden');
    }

    function closeDeleteModal() {
      document.getElementById('delete-confirm-modal').classList.add('hidden');
      currentDeleteTarget = null;
    }

    function executeDeleteAction() {
      if (!currentDeleteTarget) return;
      if (currentDeleteTarget.type === 'module') {
        draftDb = draftDb.filter(m => m.id !== currentDeleteTarget.id);
        selectedModuleId = draftDb[0].id;
        selectedSubmodule = draftDb[0].submodules[0];
        markDraftDirty();
        initAuthorDesk();
        showToast(`🗑️ Module deleted successfully.`);
      } else if (currentDeleteTarget.type === 'submodule') {
        const mod = draftDb.find(m => m.id === currentDeleteTarget.moduleId);
        if (mod) {
          mod.submodules = mod.submodules.filter(s => s.id !== currentDeleteTarget.subId);
          selectedSubmodule = mod.submodules[0];
          markDraftDirty();
          initAuthorDesk();
          showToast(`🗑️ Submodule deleted.`);
        }
      }
      closeDeleteModal();
    }

    // ==========================================
    // AUTHOR DESK INITIALIZATION & RENDERING
    // ==========================================
    function initAuthorDesk() {
      const modSelect = document.getElementById('author-module-select');
      const subSelect = document.getElementById('author-submodule-select');
      if (!modSelect || !subSelect) return;

      // Populate Modules
      modSelect.innerHTML = draftDb.map(m => `
        <option value="${m.id}" ${m.id === selectedModuleId ? 'selected' : ''}>${m.title}</option>
      `).join('');

      let mod = draftDb.find(m => m.id === selectedModuleId);
      if (!mod) {
        mod = draftDb[0];
        selectedModuleId = mod ? mod.id : null;
      }

      if (mod) {
        document.getElementById('author-mod-title').value = mod.title || '';
        document.getElementById('author-mod-level').value = mod.level || '';
        document.getElementById('author-mod-desc').value = mod.description || '';

        // Submodules
        if (!mod.submodules || mod.submodules.length === 0) {
          mod.submodules = [{ id: `sub-${Date.now()}`, title: "Submodule 1: Core", videoSteps: [] }];
        }

        subSelect.innerHTML = mod.submodules.map(s => `
          <option value="${s.id}" ${selectedSubmodule && s.id === selectedSubmodule.id ? 'selected' : ''}>${s.title}</option>
        `).join('');

        if (!selectedSubmodule || !mod.submodules.some(s => s.id === selectedSubmodule.id)) {
          selectedSubmodule = mod.submodules[0];
        }

        document.getElementById('author-sub-title').value = selectedSubmodule ? selectedSubmodule.title : '';

        // Render current tabs
        renderAuthorContentFormatSteps();
        renderAuthorLxTSteps(selectedSubmodule);
        renderAuthorMasterQuiz(mod);
        renderAuthorModuleLxI(mod);
      }

      setAuthorTab(authorActiveTab);
      updateAuthorDraftUI();
    }

    function onAuthorModuleChange() {
      selectedModuleId = document.getElementById('author-module-select').value;
      const mod = draftDb.find(m => m.id === selectedModuleId);
      selectedSubmodule = mod && mod.submodules ? mod.submodules[0] : null;
      initAuthorDesk();
    }

    function onAuthorSubmoduleChange() {
      const mod = draftDb.find(m => m.id === selectedModuleId);
      const subId = document.getElementById('author-submodule-select').value;
      selectedSubmodule = mod ? mod.submodules.find(s => s.id === subId) : null;
      initAuthorDesk();
    }

    function updateModuleMeta() {
      const mod = draftDb.find(m => m.id === selectedModuleId);
      if (mod) {
        mod.title = document.getElementById('author-mod-title').value;
        mod.level = document.getElementById('author-mod-level').value;
        mod.description = document.getElementById('author-mod-desc').value;
        // update select text
        const opt = document.querySelector(`#author-module-select option[value="${mod.id}"]`);
        if (opt) opt.innerText = mod.title;
        markDraftDirty();
      }
    }

    function updateSubmoduleTitle() {
      if (selectedSubmodule) {
        selectedSubmodule.title = document.getElementById('author-sub-title').value;
        const opt = document.querySelector(`#author-submodule-select option[value="${selectedSubmodule.id}"]`);
        if (opt) opt.innerText = selectedSubmodule.title;
        markDraftDirty();
      }
    }

    function setAuthorTab(tab) {
      authorActiveTab = tab;
      const tabs = ['led', 'lxt', 'master', 'lxi'];
      tabs.forEach(t => {
        const btn = document.getElementById(`auth-tab-btn-${t}`);
        const panel = document.getElementById(`auth-panel-${t}`);
        if (t === tab) {
          if (btn) btn.className = "px-4 py-2.5 rounded-2xl transition-all bg-teal-700 text-white shadow-md whitespace-nowrap cursor-pointer";
          if (panel) panel.classList.remove('hidden');
        } else {
          if (btn) btn.className = "px-4 py-2.5 rounded-2xl transition-all bg-white text-slate-600 hover:bg-slate-100 border border-slate-200 whitespace-nowrap cursor-pointer";
          if (panel) panel.classList.add('hidden');
        }
      });
    }

    // =========================================================================
    // MULTI-MODAL CONTENT CONFIGURATOR: VIDEO, PDF & OPTIONAL VIDEO (DELIVERABLE #4 & #7)
    // =========================================================================
    function addVideoStepToSubmodule(format = 'video') {
      if (!selectedSubmodule) return;
      if (!selectedSubmodule.videoSteps) selectedSubmodule.videoSteps = [];
      const num = selectedSubmodule.videoSteps.length + 1;
      
      selectedSubmodule.videoSteps.push({
        id: `vstep-${Date.now()}-${num}`,
        title: format === 'pdf' ? `PDF Reading Guide ${num}` : `Video Link ${num}: Core Principles`,
        format: format, // 'video' | 'pdf'
        videoUrl: format === 'video' ? "https://vjs.zencdn.net/v/oceans.mp4" : "",
        pdfUrl: format === 'pdf' ? "https://raw.githubusercontent.com/rushilbhat01/learning-companion-studio/main/docs/sample_deescalation_guide.pdf" : "",
        pdfCheckpoints: format === 'pdf' ? [
          {
            id: `pdf-cp-${Date.now()}`,
            section: "Section 1: Initial Sensory Observation",
            question: "What is the primary indicator of sensory agitation?",
            choices: ["Sudden motor pacing or tactile fidgeting", "Calm participation", "Asking to read", "Smiling"],
            correctIndex: 0,
            feedbacks: ["Correct!", "Incorrect.", "Incorrect.", "Incorrect."],
            exemplar: "Motor pacing and autonomic signs indicate rising cortisol."
          }
        ] : [],
        transcript: "Lesson notes and therapeutic takeaways for this step...",
        inVideoCheckpoints: [],
        mcqs: [],
        subjectives: []
      });

      markDraftDirty();
      renderAuthorContentFormatSteps();
    }

    function removeVideoStep(vIdx) {
      if (!selectedSubmodule || !selectedSubmodule.videoSteps) return;
      selectedSubmodule.videoSteps.splice(vIdx, 1);
      markDraftDirty();
      renderAuthorContentFormatSteps();
      showToast("Removed content step.");
    }

    function toggleStepFormat(vIdx, newFormat) {
      const step = selectedSubmodule.videoSteps[vIdx];
      if (!step) return;
      step.format = newFormat;
      if (newFormat === 'pdf' && !step.pdfUrl) {
        step.pdfUrl = "https://raw.githubusercontent.com/rushilbhat01/learning-companion-studio/main/docs/sample_deescalation_guide.pdf";
        if (!step.pdfCheckpoints) step.pdfCheckpoints = [];
      }
      markDraftDirty();
      renderAuthorContentFormatSteps();
    }

    function removeVideoUrlFromStep(vIdx) {
      const step = selectedSubmodule.videoSteps[vIdx];
      if (!step) return;
      step.videoUrl = "";
      markDraftDirty();
      renderAuthorContentFormatSteps();
      showToast("Video URL removed. This step is now text/PDF based.");
    }

    function renderAuthorContentFormatSteps() {
      const container = document.getElementById('author-video-steps-container');
      if (!container || !selectedSubmodule) return;

      const steps = selectedSubmodule.videoSteps || [];

      if (steps.length === 0) {
        container.innerHTML = `
          <div class="p-8 text-center bg-slate-50 rounded-2xl border-2 border-dashed border-slate-200 space-y-3">
            <span class="text-3xl">📄</span>
            <p class="text-xs font-bold text-slate-600">No content steps configured in this submodule.</p>
            <div class="flex justify-center gap-2">
              <button type="button" onclick="addVideoStepToSubmodule('video')" class="text-xs font-extrabold bg-teal-700 text-white px-3.5 py-1.5 rounded-xl hover:bg-teal-600">+ Add Video Step</button>
              <button type="button" onclick="addVideoStepToSubmodule('pdf')" class="text-xs font-extrabold bg-indigo-700 text-white px-3.5 py-1.5 rounded-xl hover:bg-indigo-600">+ Add PDF Step</button>
            </div>
          </div>
        `;
        return;
      }

      container.innerHTML = steps.map((vStep, vIdx) => {
        const isPdf = vStep.format === 'pdf' || (!vStep.videoUrl && vStep.pdfUrl);
        const hasVideo = !!vStep.videoUrl;
        const cpCount = isPdf ? (vStep.pdfCheckpoints?.length || 0) : (vStep.inVideoCheckpoints?.length || 0);

        return `
          <details open class="group bg-slate-50 border border-slate-200 rounded-3xl overflow-hidden transition-all shadow-sm">
            <summary class="p-4 sm:p-5 bg-white border-b border-slate-200 flex flex-wrap items-center justify-between gap-3 cursor-pointer list-none select-none">
              <div class="flex items-center gap-3">
                <span class="px-2.5 py-1 rounded-lg ${isPdf ? 'bg-indigo-100 text-indigo-800 border-indigo-200' : 'bg-teal-100 text-teal-800 border-teal-200'} text-xs font-black uppercase border">
                  ${isPdf ? '📄 PDF Guide' : '📹 Video Step'} #${vIdx + 1}
                </span>
                <span class="text-xs sm:text-sm font-extrabold text-slate-900">${vStep.title}</span>
              </div>
              <div class="flex items-center gap-2">
                <span class="px-2 py-0.5 rounded-md bg-amber-100 text-amber-900 border border-amber-200 text-[10px] font-black">
                  ⏱️ ${cpCount} Checkpoint(s)
                </span>
                <button type="button" onclick="removeVideoStep(${vIdx})" class="text-xs font-bold text-rose-500 hover:underline px-2">
                  Delete Step
                </button>
                <span class="text-xs font-bold text-teal-700 transition-transform group-open:rotate-180">▼</span>
              </div>
            </summary>

            <div class="p-5 sm:p-6 space-y-5">
              
              <!-- Content Format Selector (Video vs PDF) -->
              <div class="flex items-center gap-3 bg-white p-3 rounded-2xl border border-slate-200">
                <span class="text-xs font-black uppercase text-slate-500">Step Format:</span>
                <label class="flex items-center gap-1.5 text-xs font-bold cursor-pointer ${!isPdf ? 'text-teal-800' : 'text-slate-500'}">
                  <input type="radio" name="format_step_${vIdx}" value="video" ${!isPdf ? 'checked' : ''} onchange="toggleStepFormat(${vIdx}, 'video')" />
                  <span>📹 Video Lesson</span>
                </label>
                <label class="flex items-center gap-1.5 text-xs font-bold cursor-pointer ${isPdf ? 'text-indigo-800' : 'text-slate-500'}">
                  <input type="radio" name="format_step_${vIdx}" value="pdf" ${isPdf ? 'checked' : ''} onchange="toggleStepFormat(${vIdx}, 'pdf')" />
                  <span>📄 PDF / Document Guide</span>
                </label>
              </div>

              <!-- Step Title -->
              <div>
                <label class="block text-[10px] font-black uppercase text-slate-400 mb-1">Step Title</label>
                <input type="text" value="${vStep.title}" oninput="selectedSubmodule.videoSteps[${vIdx}].title = this.value; markDraftDirty()" class="w-full rounded-xl border border-slate-200 px-3 py-2 text-xs font-bold bg-white" />
              </div>

              <!-- If Video: Video URL & Removable Video Control (DELIVERABLE #7) -->
              ${!isPdf ? `
                <div class="p-4 bg-teal-50/50 rounded-2xl border border-teal-100 space-y-3">
                  <div class="flex items-center justify-between">
                    <label class="block text-[10px] font-black uppercase text-teal-800">Video Stream URL (MP4 or YouTube)</label>
                    ${hasVideo ? `
                      <button type="button" onclick="removeVideoUrlFromStep(${vIdx})" class="text-[11px] font-bold text-rose-600 hover:underline">
                        🗑️ Remove Video (Make Text/PDF Only)
                      </button>
                    ` : `
                      <span class="text-[10px] text-amber-700 font-bold">No Video Assigned (Text Mode)</span>
                    `}
                  </div>
                  <input type="text" value="${vStep.videoUrl || ''}" placeholder="e.g. https://vjs.zencdn.net/v/oceans.mp4 or YouTube URL" oninput="selectedSubmodule.videoSteps[${vIdx}].videoUrl = this.value; markDraftDirty()" class="w-full rounded-xl border border-teal-200 px-3 py-2 text-xs font-bold bg-white" />
                </div>

                <!-- In-Video Reflection Checkpoints Accordion -->
                <div class="border border-amber-200 bg-amber-50/30 rounded-2xl p-4 space-y-4">
                  <div class="flex items-center justify-between">
                    <div class="flex items-center gap-2">
                      <span class="text-base">⏱️</span>
                      <h4 class="text-xs font-black uppercase text-amber-900">In-Video Reflection Checkpoints (Pause at MM:SS)</h4>
                    </div>
                    <button type="button" onclick="addInVideoCheckpoint(${vIdx})" class="text-xs font-black bg-amber-700 hover:bg-amber-800 text-white px-3 py-1 rounded-xl shadow-sm">
                      + Add Checkpoint
                    </button>
                  </div>

                  <div class="space-y-3">
                    ${(vStep.inVideoCheckpoints || []).map((ivc, ivIdx) => `
                      <div class="p-4 bg-white rounded-xl border border-amber-200 shadow-sm space-y-3">
                        <div class="flex items-center justify-between border-b border-amber-100 pb-2">
                          <span class="text-[11px] font-black uppercase text-amber-800">Checkpoint #${ivIdx + 1}</span>
                          <button type="button" onclick="deleteInVideoCheckpoint(${vIdx}, ${ivIdx})" class="text-xs font-bold text-rose-500 hover:underline">Delete</button>
                        </div>

                        <div class="grid grid-cols-2 gap-3">
                          <div>
                            <label class="block text-[10px] font-bold uppercase text-slate-400 mb-1">Pause Min</label>
                            <input type="number" min="0" value="${ivc.timeMin || 0}" oninput="selectedSubmodule.videoSteps[${vIdx}].inVideoCheckpoints[${ivIdx}].timeMin = Number(this.value); markDraftDirty()" class="w-full rounded-lg border border-slate-200 px-2.5 py-1 text-xs font-bold" />
                          </div>
                          <div>
                            <label class="block text-[10px] font-bold uppercase text-slate-400 mb-1">Pause Sec</label>
                            <input type="number" min="0" max="59" value="${ivc.timeSec || 0}" oninput="selectedSubmodule.videoSteps[${vIdx}].inVideoCheckpoints[${ivIdx}].timeSec = Number(this.value); markDraftDirty()" class="w-full rounded-lg border border-slate-200 px-2.5 py-1 text-xs font-bold" />
                          </div>
                        </div>

                        <div>
                          <label class="block text-[10px] font-bold uppercase text-slate-400 mb-1">Reflection Prompt / Question</label>
                          <input type="text" value="${ivc.question}" oninput="selectedSubmodule.videoSteps[${vIdx}].inVideoCheckpoints[${ivIdx}].question = this.value; markDraftDirty()" class="w-full rounded-lg border border-slate-200 px-3 py-1.5 text-xs font-bold" />
                        </div>

                        <!-- 4 MCQ Choices -->
                        <div class="grid sm:grid-cols-2 gap-2 pt-1">
                          ${(ivc.choices || []).map((ch, chIdx) => `
                            <div class="p-2.5 bg-slate-50 rounded-lg border border-slate-200 space-y-1">
                              <div class="flex items-center justify-between">
                                <span class="text-[10px] font-extrabold uppercase text-slate-400">Choice ${chIdx + 1}</span>
                                <label class="text-[10px] font-black text-teal-800 flex items-center gap-1 cursor-pointer">
                                  <input type="radio" name="cp_correct_${vIdx}_${ivIdx}" ${ivc.correctIndex === chIdx ? 'checked' : ''} onchange="selectedSubmodule.videoSteps[${vIdx}].inVideoCheckpoints[${ivIdx}].correctIndex = ${chIdx}; markDraftDirty()" /> Correct
                                </label>
                              </div>
                              <input type="text" value="${ch}" oninput="selectedSubmodule.videoSteps[${vIdx}].inVideoCheckpoints[${ivIdx}].choices[${chIdx}] = this.value; markDraftDirty()" class="w-full rounded border border-slate-200 px-2 py-1 text-xs bg-white" placeholder="Choice text..." />
                              <input type="text" value="${ivc.feedbacks?.[chIdx] || ''}" oninput="if (!selectedSubmodule.videoSteps[${vIdx}].inVideoCheckpoints[${ivIdx}].feedbacks) selectedSubmodule.videoSteps[${vIdx}].inVideoCheckpoints[${ivIdx}].feedbacks = []; selectedSubmodule.videoSteps[${vIdx}].inVideoCheckpoints[${ivIdx}].feedbacks[${chIdx}] = this.value; markDraftDirty()" class="w-full rounded border border-slate-200 px-2 py-0.5 text-[10px] text-slate-600 bg-white" placeholder="Feedback..." />
                            </div>
                          `).join('')}
                        </div>
                      </div>
                    `).join('')}
                  </div>
                </div>
              ` : `
                <!-- If PDF: PDF Document & Embedded Checkpoints Configurator (DELIVERABLE #4) -->
                <div class="p-4 bg-indigo-50/60 rounded-2xl border border-indigo-200 space-y-4">
                  <div class="flex items-center justify-between">
                    <span class="text-xs font-black uppercase text-indigo-900 flex items-center gap-1.5">
                      <span>📄</span> <span>PDF Document Viewer Settings</span>
                    </span>
                    <span class="text-[10px] font-bold text-indigo-700">Multi-Modal Reading Path</span>
                  </div>

                  <div>
                    <label class="block text-[10px] font-black uppercase text-indigo-800 mb-1">PDF Document URL</label>
                    <input type="text" value="${vStep.pdfUrl || ''}" placeholder="URL to PDF file (e.g. https://.../guide.pdf)" oninput="selectedSubmodule.videoSteps[${vIdx}].pdfUrl = this.value; markDraftDirty()" class="w-full rounded-xl border border-indigo-200 px-3 py-2 text-xs font-bold bg-white" />
                  </div>

                  <!-- PDF Checkpoints -->
                  <div class="pt-2 border-t border-indigo-100 space-y-3">
                    <div class="flex items-center justify-between">
                      <label class="text-xs font-black uppercase text-indigo-900">Embedded PDF Reading Checkpoints</label>
                      <button type="button" onclick="addPDFCheckpoint(${vIdx})" class="text-xs font-black bg-indigo-700 hover:bg-indigo-600 text-white px-3 py-1 rounded-xl shadow-sm">
                        + Add Reading Checkpoint
                      </button>
                    </div>

                    <div class="space-y-3">
                      ${(vStep.pdfCheckpoints || []).map((pcp, pIdx) => `
                        <div class="p-4 bg-white rounded-xl border border-indigo-200 shadow-sm space-y-3">
                          <div class="flex items-center justify-between border-b border-indigo-100 pb-2">
                            <span class="text-[11px] font-black uppercase text-indigo-800">Reading Checkpoint #${pIdx + 1}</span>
                            <button type="button" onclick="deletePDFCheckpoint(${vIdx}, ${pIdx})" class="text-xs font-bold text-rose-500 hover:underline">Delete</button>
                          </div>
                          <div>
                            <label class="block text-[10px] font-bold uppercase text-slate-400 mb-1">Target Reading Section / Milestone</label>
                            <input type="text" value="${pcp.section || ''}" placeholder="e.g. Section 1: Sensory Indicators" oninput="selectedSubmodule.videoSteps[${vIdx}].pdfCheckpoints[${pIdx}].section = this.value; markDraftDirty()" class="w-full rounded-lg border border-slate-200 px-3 py-1 text-xs font-bold" />
                          </div>
                          <div>
                            <label class="block text-[10px] font-bold uppercase text-slate-400 mb-1">Checkpoint Question</label>
                            <input type="text" value="${pcp.question}" oninput="selectedSubmodule.videoSteps[${vIdx}].pdfCheckpoints[${pIdx}].question = this.value; markDraftDirty()" class="w-full rounded-lg border border-slate-200 px-3 py-1.5 text-xs font-bold" />
                          </div>

                          <!-- 4 MCQ Choices for PDF -->
                          <div class="grid sm:grid-cols-2 gap-2 pt-1">
                            ${(pcp.choices || []).map((ch, chIdx) => `
                              <div class="p-2.5 bg-slate-50 rounded-lg border border-slate-200 space-y-1">
                                <div class="flex items-center justify-between">
                                  <span class="text-[10px] font-extrabold uppercase text-slate-400">Option ${chIdx + 1}</span>
                                  <label class="text-[10px] font-black text-indigo-800 flex items-center gap-1 cursor-pointer">
                                    <input type="radio" name="pdf_correct_${vIdx}_${pIdx}" ${pcp.correctIndex === chIdx ? 'checked' : ''} onchange="selectedSubmodule.videoSteps[${vIdx}].pdfCheckpoints[${pIdx}].correctIndex = ${chIdx}; markDraftDirty()" /> Correct
                                  </label>
                                </div>
                                <input type="text" value="${ch}" oninput="selectedSubmodule.videoSteps[${vIdx}].pdfCheckpoints[${pIdx}].choices[${chIdx}] = this.value; markDraftDirty()" class="w-full rounded border border-slate-200 px-2 py-1 text-xs bg-white" />
                                <input type="text" value="${pcp.feedbacks?.[chIdx] || ''}" oninput="if (!selectedSubmodule.videoSteps[${vIdx}].pdfCheckpoints[${pIdx}].feedbacks) selectedSubmodule.videoSteps[${vIdx}].pdfCheckpoints[${pIdx}].feedbacks = []; selectedSubmodule.videoSteps[${vIdx}].pdfCheckpoints[${pIdx}].feedbacks[chIdx] = this.value; markDraftDirty()" class="w-full rounded border border-slate-200 px-2 py-0.5 text-[10px] text-slate-600 bg-white" placeholder="Feedback..." />
                              </div>
                            `).join('')}
                          </div>
                        </div>
                      `).join('')}
                    </div>
                  </div>
                </div>
              `}

              <!-- Lecture / Reading Notes -->
              <div>
                <label class="block text-[10px] font-black uppercase text-slate-400 mb-1">Lecture & Reading Notes</label>
                <textarea rows="2" oninput="selectedSubmodule.videoSteps[${vIdx}].transcript = this.value; markDraftDirty()" class="w-full rounded-xl border border-slate-200 p-3 text-xs bg-white">${vStep.transcript || ''}</textarea>
              </div>

            </div>
          </details>
        `;
      }).join('');
    }

    function addInVideoCheckpoint(vIdx) {
      const step = selectedSubmodule.videoSteps[vIdx];
      if (!step) return;
      if (!step.inVideoCheckpoints) step.inVideoCheckpoints = [];
      const num = step.inVideoCheckpoints.length + 1;
      step.inVideoCheckpoints.push({
        id: `ivc-${Date.now()}-${num}`,
        timeMin: 0,
        timeSec: 15 * num,
        type: "mcq",
        question: `Mid-Video Reflection Checkpoint #${num}: Pause & Reflect`,
        choices: ["Option A: Prioritize co-regulation", "Option B: Strict compliance", "Option C: Isolate", "Option D: Raise voice"],
        correctIndex: 0,
        feedbacks: ["Correct! Safe co-regulation lowers autonomic stress.", "Incorrect.", "Incorrect.", "Incorrect."],
        exemplar: "Author Exemplar Feedback: Maintain emotional safety and low-demand pacing."
      });
      markDraftDirty();
      renderAuthorContentFormatSteps();
    }

    function deleteInVideoCheckpoint(vIdx, ivIdx) {
      selectedSubmodule.videoSteps[vIdx].inVideoCheckpoints.splice(ivIdx, 1);
      markDraftDirty();
      renderAuthorContentFormatSteps();
    }

    function addPDFCheckpoint(vIdx) {
      const step = selectedSubmodule.videoSteps[vIdx];
      if (!step) return;
      if (!step.pdfCheckpoints) step.pdfCheckpoints = [];
      const num = step.pdfCheckpoints.length + 1;
      step.pdfCheckpoints.push({
        id: `pdf-cp-${Date.now()}-${num}`,
        section: `Section ${num}: Therapeutic Application`,
        question: `PDF Reading Checkpoint #${num}: Key Strategy`,
        choices: ["Option A: Calm low-arousal approach", "Option B: Forced eye contact", "Option C: Rapid demands", "Option D: Loud alarms"],
        correctIndex: 0,
        feedbacks: ["Correct! Low-arousal approaches are standard of care.", "Incorrect.", "Incorrect.", "Incorrect."],
        exemplar: "Author Exemplar Feedback: Minimize sensory demand during dysregulation."
      });
      markDraftDirty();
      renderAuthorContentFormatSteps();
    }

    function deletePDFCheckpoint(vIdx, pIdx) {
      selectedSubmodule.videoSteps[vIdx].pdfCheckpoints.splice(pIdx, 1);
      markDraftDirty();
      renderAuthorContentFormatSteps();
    }

    // =========================================================================
    // MODULE-SCOPED LXI & STALE ANSWER BUG FIX (DELIVERABLE #5 & #6)
    // =========================================================================
    function renderAuthorModuleLxI(mod) {
      if (!mod) return;
      if (!mod.lxi) {
        mod.lxi = {
          questionId: `lxi-${mod.id}-1`,
          question: `Module Discussion: Share an effective rapport-building strategy for this topic.`,
          submissions: []
        };
      }

      document.getElementById('author-lxi-module-header').innerText = `Discussion Prompt: ${mod.title}`;
      document.getElementById('author-module-lxi-prompt').value = mod.lxi.question || '';
      document.getElementById('author-lxi-subs-count').innerText = mod.lxi.submissions?.length || 0;

      const list = document.getElementById('author-lxi-submissions-list');
      if (list) {
        if (!mod.lxi.submissions || mod.lxi.submissions.length === 0) {
          list.innerHTML = `<p class="text-xs text-slate-400 italic p-3">No companion submissions yet for this prompt.</p>`;
        } else {
          list.innerHTML = mod.lxi.submissions.map((sub, sIdx) => `
            <div class="p-3 bg-slate-50 rounded-xl border border-slate-200 text-xs flex items-start justify-between gap-3">
              <div>
                <div class="flex items-center gap-2 text-[10px] text-slate-400">
                  <strong class="text-slate-800 font-bold">${sub.companionName}</strong>
                  <span>•</span>
                  <span>${sub.timestamp}</span>
                </div>
                <p class="text-xs text-slate-700 mt-1">"${sub.answer}"</p>
              </div>
              <button type="button" onclick="deleteAuthorLxISubmission(${sIdx})" class="text-[10px] font-bold text-rose-500 hover:underline whitespace-nowrap">
                Delete
              </button>
            </div>
          `).join('');
        }
      }
    }

    function saveModuleLxIPrompt() {
      const mod = draftDb.find(m => m.id === selectedModuleId);
      if (!mod) return;
      const newPrompt = document.getElementById('author-module-lxi-prompt').value.trim();
      
      // ANTI-STALE LOGIC (DELIVERABLE #5):
      // If the question text changed, archive/clear old answers and generate a new questionId!
      if (mod.lxi && mod.lxi.question !== newPrompt) {
        mod.lxi.question = newPrompt;
        mod.lxi.questionId = `lxi-${mod.id}-${Date.now()}`;
        mod.lxi.submissions = []; // Clear outdated submissions!
        showToast("✓ Question updated! Previous peer answers cleared so outdated responses never show under new questions.");
      } else {
        showToast("Prompt saved.");
      }

      markDraftDirty();
      renderAuthorModuleLxI(mod);
    }

    function clearCurrentModuleLxISubmissions() {
      const mod = draftDb.find(m => m.id === selectedModuleId);
      if (!mod || !mod.lxi) return;
      if (confirm("Clear all companion peer submissions for this prompt?")) {
        mod.lxi.submissions = [];
        markDraftDirty();
        renderAuthorModuleLxI(mod);
        showToast("Cleared peer submissions.");
      }
    }

    function deleteAuthorLxISubmission(idx) {
      const mod = draftDb.find(m => m.id === selectedModuleId);
      if (mod && mod.lxi && mod.lxi.submissions) {
        mod.lxi.submissions.splice(idx, 1);
        markDraftDirty();
        renderAuthorModuleLxI(mod);
      }
    }

    // ==========================================
    // LXT EXTENSION & MASTER QUIZ CONFIGURATOR
    // ==========================================
    function renderAuthorLxTSteps(sub) {
      const container = document.getElementById('author-lxt-steps-container');
      if (!container || !sub) return;
      if (!sub.lxt) {
        sub.lxt = { title: "LxT Extension Trajectory", videoSteps: [] };
      }
      document.getElementById('author-lxt-title').value = sub.lxt.title || '';

      const steps = sub.lxt.videoSteps || [];
      container.innerHTML = steps.map((s, idx) => `
        <div class="p-4 bg-teal-50/40 rounded-2xl border border-teal-200 space-y-3">
          <div class="flex items-center justify-between">
            <span class="text-xs font-black uppercase text-teal-800">LxT Extension Video #${idx + 1}</span>
            <button type="button" onclick="deleteAuthorLxTStep(${idx})" class="text-xs font-bold text-rose-500 hover:underline">Delete</button>
          </div>
          <input type="text" value="${s.title}" oninput="selectedSubmodule.lxt.videoSteps[${idx}].title = this.value; markDraftDirty()" class="w-full rounded-xl border border-teal-200 px-3 py-1.5 text-xs font-bold bg-white" placeholder="Extension Title..." />
          <input type="text" value="${s.videoUrl}" oninput="selectedSubmodule.lxt.videoSteps[${idx}].videoUrl = this.value; markDraftDirty()" class="w-full rounded-xl border border-teal-200 px-3 py-1.5 text-xs font-bold bg-white" placeholder="Video URL..." />
        </div>
      `).join('');
    }

    function addLxTVideoLink() {
      if (!selectedSubmodule) return;
      if (!selectedSubmodule.lxt) selectedSubmodule.lxt = { title: "LxT Extension Trajectory", videoSteps: [] };
      const num = selectedSubmodule.lxt.videoSteps.length + 1;
      selectedSubmodule.lxt.videoSteps.push({
        id: `lxt-step-${Date.now()}-${num}`,
        title: `LxT Extension Video ${num}: Case Study Analysis`,
        videoUrl: "https://vjs.zencdn.net/v/oceans.mp4",
        transcript: "Detailed therapeutic case review...",
        inVideoCheckpoints: [],
        mcqs: [],
        subjectives: []
      });
      markDraftDirty();
      renderAuthorLxTSteps(selectedSubmodule);
    }

    function deleteAuthorLxTStep(idx) {
      selectedSubmodule.lxt.videoSteps.splice(idx, 1);
      markDraftDirty();
      renderAuthorLxTSteps(selectedSubmodule);
    }

    function updateLxTMeta() {
      if (selectedSubmodule && selectedSubmodule.lxt) {
        selectedSubmodule.lxt.title = document.getElementById('author-lxt-title').value;
        markDraftDirty();
      }
    }

    function renderAuthorMasterQuiz(mod) {
      const container = document.getElementById('author-master-quiz-list');
      if (!container || !mod) return;
      const quiz = mod.masterQuiz || [];

      container.innerHTML = quiz.map((q, idx) => {
        const isSubj = q.type === 'subjective';
        return `
          <div class="p-4 bg-slate-50 rounded-2xl border border-slate-200 space-y-3">
            <div class="flex items-center justify-between">
              <span class="text-xs font-black uppercase ${isSubj ? 'text-indigo-800' : 'text-teal-800'}">
                ${isSubj ? '✍️ Subjective Question' : '❓ Master MCQ'} #${idx + 1}
              </span>
              <button type="button" onclick="deleteAuthorMasterQuestion(${idx})" class="text-xs font-bold text-rose-500 hover:underline">Delete</button>
            </div>
            ${isSubj ? `
              <input type="text" value="${q.prompt}" oninput="db.find(m=>m.id==='${mod.id}').masterQuiz[${idx}].prompt = this.value; markDraftDirty()" class="w-full rounded-xl border border-slate-200 px-3 py-1.5 text-xs font-bold bg-white" placeholder="Prompt..." />
              <textarea oninput="db.find(m=>m.id==='${mod.id}').masterQuiz[${idx}].exemplar = this.value; markDraftDirty()" rows="2" class="w-full rounded-xl border border-slate-200 p-2 text-xs bg-white" placeholder="Exemplar answer...">${q.exemplar || ''}</textarea>
            ` : `
              <input type="text" value="${q.question}" oninput="db.find(m=>m.id==='${mod.id}').masterQuiz[${idx}].question = this.value; markDraftDirty()" class="w-full rounded-xl border border-slate-200 px-3 py-1.5 text-xs font-bold bg-white" placeholder="Question..." />
            `}
          </div>
        `;
      }).join('');
    }

    function addAuthorMasterMCQ() {
      const mod = draftDb.find(m => m.id === selectedModuleId);
      if (!mod) return;
      if (!mod.masterQuiz) mod.masterQuiz = [];
      mod.masterQuiz.push({
        type: "mcq",
        question: "New Master Assessment Question",
        choices: ["Option A: Correct answer", "Option B: Incorrect", "Option C: Incorrect", "Option D: Incorrect"],
        correctIndex: 0,
        feedbacks: ["Correct!", "Incorrect.", "Incorrect.", "Incorrect."]
      });
      markDraftDirty();
      renderAuthorMasterQuiz(mod);
    }

    function addAuthorMasterSubjective() {
      const mod = draftDb.find(m => m.id === selectedModuleId);
      if (!mod) return;
      if (!mod.masterQuiz) mod.masterQuiz = [];
      mod.masterQuiz.push({
        type: "subjective",
        prompt: "Describe how you co-regulate with a student experiencing sensory discomfort.",
        exemplar: "Author Exemplar Feedback: Minimize verbal demands, provide quiet space, and respect sensory boundaries."
      });
      markDraftDirty();
      renderAuthorMasterQuiz(mod);
    }

    function deleteAuthorMasterQuestion(idx) {
      const mod = draftDb.find(m => m.id === selectedModuleId);
      if (mod && mod.masterQuiz) {
        mod.masterQuiz.splice(idx, 1);
        markDraftDirty();
        renderAuthorMasterQuiz(mod);
      }
    }

    // =========================================================================
    // COMPANION VIEW (STUDENT PORTAL RENDERING)
    // =========================================================================
    function goHome() {
      document.getElementById('student-level-modules').classList.remove('hidden');
      document.getElementById('student-level-submodules').classList.add('hidden');
      document.getElementById('student-level-content').classList.add('hidden');
      document.getElementById('student-level-lxt-view').classList.add('hidden');
      document.getElementById('student-level-masterquiz').classList.add('hidden');

      document.getElementById('crumb-module-nav').classList.add('hidden');
      document.getElementById('crumb-sub-nav').classList.add('hidden');

      renderModulesGrid();
    }

    function renderModulesGrid() {
      const grid = document.getElementById('modules-grid');
      if (!grid) return;

      grid.innerHTML = publishedDb.map(mod => {
        const subCount = mod.submodules ? mod.submodules.length : 0;
        const isMasterFinished = masterQuizSubmittedMap[mod.id];
        
        return `
          <div onclick="openModule('${mod.id}')" class="bg-white p-6 rounded-3xl border border-slate-200 hover:border-teal-600 transition-all cursor-pointer shadow-sm hover:shadow-md flex flex-col justify-between group space-y-4">
            <div class="space-y-2.5">
              <div class="flex items-center justify-between">
                <span class="px-3 py-1 rounded-full bg-teal-50 text-teal-800 text-xs font-black border border-teal-200">
                  ${mod.level || 'Foundational'}
                </span>
                <span class="text-xs font-bold text-slate-400 group-hover:text-teal-700 transition-colors">
                  ${subCount} Lesson(s) →
                </span>
              </div>
              <h3 class="text-lg font-extrabold text-slate-900 group-hover:text-teal-700 transition-colors leading-snug">
                ${mod.title}
              </h3>
              <p class="text-xs text-slate-500 leading-relaxed line-clamp-2">
                ${mod.description}
              </p>
            </div>

            <div class="pt-3 border-t border-slate-100 flex items-center justify-between text-xs">
              <span class="font-bold text-slate-600 flex items-center gap-1">
                <span>💬</span> <span>In-Module LxI Discussion</span>
              </span>
              <span class="font-black ${isMasterFinished ? 'text-emerald-600' : 'text-slate-400'}">
                ${isMasterFinished ? '✓ Master Certified' : '🎓 Master Quiz'}
              </span>
            </div>
          </div>
        `;
      }).join('');
    }

    function openModule(modId) {
      selectedModuleId = modId;
      const mod = publishedDb.find(m => m.id === modId);
      if (!mod) return;

      document.getElementById('student-level-modules').classList.add('hidden');
      document.getElementById('student-level-submodules').classList.remove('hidden');
      document.getElementById('student-level-content').classList.add('hidden');
      document.getElementById('student-level-lxt-view').classList.add('hidden');
      document.getElementById('student-level-masterquiz').classList.add('hidden');

      document.getElementById('crumb-module-nav').classList.remove('hidden');
      document.getElementById('crumb-module-title').innerText = mod.title;
      document.getElementById('crumb-sub-nav').classList.add('hidden');

      document.getElementById('selected-module-header').innerText = mod.title;
      document.getElementById('selected-module-desc').innerText = mod.description;

      renderSubmodulesList(mod);
      renderStudentModuleLxI(mod);
    }

    function goSubmodules() {
      openModule(selectedModuleId);
    }

    function renderSubmodulesList(mod) {
      const container = document.getElementById('submodules-list');
      if (!container || !mod) return;

      const submodules = mod.submodules || [];
      let allSubsCompleted = true;

      container.innerHTML = submodules.map((sub, sIdx) => {
        const isFinished = submoduleFinishedMap[sub.id];
        if (!isFinished) allSubsCompleted = false;
        const isPdf = sub.format === 'pdf' || (sub.videoSteps?.[0]?.format === 'pdf') || sub.pdfDoc;

        return `
          <div onclick="openSubmodule('${sub.id}')" class="bg-white p-5 rounded-2xl border ${isFinished ? 'border-emerald-300 bg-emerald-50/20' : 'border-slate-200'} shadow-sm hover:border-teal-600 transition-all cursor-pointer flex items-center justify-between gap-3 group">
            <div class="flex items-center gap-3">
              <div class="w-9 h-9 rounded-xl flex items-center justify-center font-black text-sm ${isFinished ? 'bg-emerald-600 text-white' : isPdf ? 'bg-indigo-100 text-indigo-800' : 'bg-teal-100 text-teal-800'}">
                ${isFinished ? '✓' : isPdf ? '📄' : (sIdx + 1)}
              </div>
              <div>
                <span class="text-[10px] font-black uppercase tracking-wider ${isPdf ? 'text-indigo-700' : 'text-teal-700'}">
                  ${isPdf ? 'PDF Reading Guide' : 'Video Lesson'}
                </span>
                <h4 class="text-xs sm:text-sm font-extrabold text-slate-900 group-hover:text-teal-700 transition-colors">
                  ${sub.title}
                </h4>
              </div>
            </div>
            <span class="text-xs font-bold text-slate-400 group-hover:text-teal-700">Open →</span>
          </div>
        `;
      }).join('');

      // Master Quiz Lock Card
      const btnMaster = document.getElementById('btn-take-master-quiz');
      const descMaster = document.getElementById('master-quiz-lock-desc');
      if (btnMaster && descMaster) {
        if (allSubsCompleted) {
          btnMaster.disabled = false;
          btnMaster.className = "bg-indigo-700 hover:bg-indigo-600 text-white cursor-pointer px-5 py-3 rounded-xl text-xs font-extrabold shadow-md transition-all whitespace-nowrap";
          btnMaster.innerText = "🎓 Take Master Quiz →";
          descMaster.className = "text-xs text-emerald-700 font-bold";
          descMaster.innerText = "✓ All submodules completed! You are ready for certification.";
        } else {
          btnMaster.disabled = true;
          btnMaster.className = "bg-slate-300 text-slate-500 cursor-not-allowed px-5 py-3 rounded-xl text-xs font-extrabold shadow-none whitespace-nowrap";
          btnMaster.innerText = "🔒 Take Master Quiz (Locked)";
          descMaster.className = "text-xs text-amber-700 font-bold";
          descMaster.innerText = "🔒 Complete all submodules to unlock the Master Quiz.";
        }
      }
    }

    // =========================================================================
    // MODULE-SCOPED LXI DISCUSSION (STUDENT VIEW)
    // =========================================================================
    function renderStudentModuleLxI(mod) {
      if (!mod) return;
      if (!mod.lxi) {
        mod.lxi = {
          questionId: `lxi-${mod.id}-1`,
          question: `Module Discussion: Share an effective rapport-building strategy for this topic.`,
          submissions: []
        };
      }

      document.getElementById('module-lxi-question-text').innerText = mod.lxi.question;
      const qKey = `${mod.id}_${mod.lxi.questionId}`;
      const isAnswered = moduleLxISubmittedMap[qKey];

      const lockStatus = document.getElementById('module-lxi-lock-status');
      const peerContainer = document.getElementById('module-lxi-peer-responses');
      const feed = document.getElementById('module-lxi-feed');
      const statusText = document.getElementById('module-lxi-status');

      if (isAnswered) {
        if (lockStatus) {
          lockStatus.className = "text-xs font-bold text-emerald-400";
          lockStatus.innerText = "🔓 Peer Responses Unlocked";
        }
        if (statusText) statusText.innerText = "✓ You shared your reflection. Peer discussion is unlocked below.";
        if (peerContainer) peerContainer.classList.remove('hidden');

        if (feed) {
          const subs = mod.lxi.submissions || [];
          feed.innerHTML = subs.map(s => `
            <div class="p-3 bg-indigo-950/80 rounded-2xl text-xs text-indigo-100 border border-indigo-800/40 space-y-1">
              <div class="flex items-center justify-between text-[10px] text-indigo-300">
                <strong>${s.companionName}</strong>
                <span>${s.timestamp}</span>
              </div>
              <p class="text-xs text-indigo-100 leading-relaxed">"${s.answer}"</p>
            </div>
          `).join('');
        }
      } else {
        if (lockStatus) {
          lockStatus.className = "text-xs font-bold text-amber-300";
          lockStatus.innerText = "🔒 Peer Answers Hidden (Submit yours first to unlock)";
        }
        if (statusText) statusText.innerText = "";
        if (peerContainer) peerContainer.classList.add('hidden');
      }
    }

    function submitModuleLxIResponse() {
      const mod = publishedDb.find(m => m.id === selectedModuleId);
      if (!mod || !mod.lxi) return;
      const input = document.getElementById('module-lxi-response');
      const val = input.value.trim();
      if (!val) {
        alert("Please write a reflection before submitting.");
        return;
      }

      const qKey = `${mod.id}_${mod.lxi.questionId}`;
      if (!mod.lxi.submissions) mod.lxi.submissions = [];

      const submission = {
        companionName: "Priya Sharma (You)",
        timestamp: "Just Now",
        answer: val
      };

      mod.lxi.submissions.unshift(submission);
      moduleLxISubmittedMap[qKey] = true;
      input.value = "";

      // Log attempt to Admin Dashboard (DELIVERABLE #8)
      logAdminAttempt({
        companionName: "Priya Sharma (Trainee)",
        type: "LXI_DISCUSSION",
        typeName: "Module LxI Discussion",
        moduleTitle: mod.title,
        question: mod.lxi.question,
        submittedAnswer: val,
        status: "Submitted & Shared",
        isCorrect: true,
        exemplar: "Active peer participation and reflection logged."
      });

      renderStudentModuleLxI(mod);
    }

    // =========================================================================
    // SUBMODULE CONTENT: VIDEO OR PDF OR HYBRID (DELIVERABLE #1, #4, #7)
    // =========================================================================
    function openSubmodule(subId) {
      const mod = publishedDb.find(m => m.id === selectedModuleId);
      const sub = mod.submodules.find(s => s.id === subId);
      selectedSubmodule = sub;
      activeVideoStepIndex = 0;

      document.getElementById('student-level-modules').classList.add('hidden');
      document.getElementById('student-level-submodules').classList.add('hidden');
      document.getElementById('student-level-content').classList.remove('hidden');
      document.getElementById('student-level-lxt-view').classList.add('hidden');
      document.getElementById('student-level-masterquiz').classList.add('hidden');

      document.getElementById('crumb-sub-nav').classList.remove('hidden');
      document.getElementById('crumb-sub-title').innerText = sub.title;

      renderSubmoduleContent(sub, mod);
    }

    function renderSubmoduleContent(sub, mod) {
      document.getElementById('student-module-badge').innerText = mod.title;
      document.getElementById('student-sub-title').innerText = sub.title;

      // Sidebar submodules outline
      const sidebar = document.getElementById('sidebar-submodules-list');
      if (sidebar) {
        sidebar.innerHTML = mod.submodules.map((s, idx) => `
          <div onclick="openSubmodule('${s.id}')" class="p-2.5 rounded-xl text-xs font-bold cursor-pointer transition-all ${s.id === sub.id ? 'bg-teal-50 text-teal-800 border border-teal-200' : 'text-slate-600 hover:bg-slate-50'}">
            <span>${submoduleFinishedMap[s.id] ? '✓' : (idx + 1) + '.'}</span> <span>${s.title}</span>
          </div>
        `).join('');
      }

      // Check format: Is it PDF or Video or Hybrid?
      const steps = sub.videoSteps || [];
      const currentStep = steps[activeVideoStepIndex] || (sub.pdfDoc ? { format: 'pdf', title: sub.pdfDoc.title, pdfUrl: sub.pdfDoc.url, pdfCheckpoints: sub.pdfDoc.embeddedCheckpoints, transcript: "" } : null);

      const navSteps = document.getElementById('student-video-steps-nav');
      if (navSteps) {
        if (steps.length > 1) {
          navSteps.classList.remove('hidden');
          navSteps.innerHTML = steps.map((st, idx) => `
            <button onclick="changeVideoStep(${idx})" class="px-3 py-1.5 rounded-xl text-xs font-bold transition-all whitespace-nowrap ${idx === activeVideoStepIndex ? 'bg-teal-700 text-white shadow-sm' : 'bg-slate-100 text-slate-600 hover:bg-slate-200'}">
              ${st.format === 'pdf' ? '📄' : '📹'} Step ${idx + 1}: ${st.title}
            </button>
          `).join('');
        } else {
          navSteps.classList.add('hidden');
        }
      }

      const badge = document.getElementById('student-video-step-badge');
      if (badge) {
        badge.innerText = `Step ${activeVideoStepIndex + 1} of ${Math.max(steps.length, 1)}`;
      }

      const videoWrapper = document.getElementById('student-video-container-wrapper');
      const pdfWrapper = document.getElementById('student-pdf-container-wrapper');

      const isCurrentStepPdf = currentStep && (currentStep.format === 'pdf' || (!currentStep.videoUrl && currentStep.pdfUrl));

      if (isCurrentStepPdf) {
        // PDF MODE
        if (videoWrapper) videoWrapper.classList.add('hidden');
        if (pdfWrapper) pdfWrapper.classList.remove('hidden');
        renderStudentPDFView(currentStep);
      } else if (currentStep && currentStep.videoUrl) {
        // VIDEO MODE
        if (videoWrapper) videoWrapper.classList.remove('hidden');
        if (pdfWrapper) pdfWrapper.classList.add('hidden');
        renderUniversalVideoPlayer(currentStep.videoUrl, currentStep.title, 'video-player-container', false);
      } else {
        // TEXT / SCENARIO ONLY MODE (Video is omitted, deliverable #7)
        if (videoWrapper) videoWrapper.classList.add('hidden');
        if (pdfWrapper) pdfWrapper.classList.add('hidden');
        unlockReflections(); // Directly unlock reflection scenarios!
      }

      // Lecture Notes
      document.getElementById('student-transcript-text').innerText = currentStep?.transcript || "Review the scenario notes above and reflect upon the de-escalation actions.";

      // Check reflections lock state
      const isStepDone = videoStepFinishedMap[`${sub.id}_${activeVideoStepIndex}`];
      if (isStepDone) {
        document.getElementById('student-reflections-section').classList.remove('hidden');
      } else {
        document.getElementById('student-reflections-section').classList.add('hidden');
      }

      renderSubmoduleReflections(currentStep, sub);
      updateLxTCardStatus(sub);
    }

    function changeVideoStep(idx) {
      activeVideoStepIndex = idx;
      const mod = publishedDb.find(m => m.id === selectedModuleId);
      renderSubmoduleContent(selectedSubmodule, mod);
    }

    // =========================================================================
    // MULTI-MODAL PDF DOCUMENT VIEWER & EMBEDDED CHECKPOINTS (DELIVERABLE #4)
    // =========================================================================
    function renderStudentPDFView(step) {
      const titleEl = document.getElementById('pdf-doc-title');
      const downloadBtn = document.getElementById('pdf-download-btn');
      const embedFrame = document.getElementById('pdf-embed-frame');
      const checkpointsList = document.getElementById('pdf-checkpoints-list');

      const pdfUrl = step.pdfUrl || "https://raw.githubusercontent.com/rushilbhat01/learning-companion-studio/main/docs/sample_deescalation_guide.pdf";
      if (titleEl) titleEl.innerText = step.title || "Inclusive Education Protocol (PDF)";
      if (downloadBtn) downloadBtn.href = pdfUrl;
      if (embedFrame) embedFrame.src = pdfUrl;

      const checkpoints = step.pdfCheckpoints || [];
      if (!checkpointsList) return;

      if (checkpoints.length === 0) {
        checkpointsList.innerHTML = `<p class="text-xs text-slate-500 italic">No embedded checkpoints for this reading.</p>`;
        unlockPDFReflections();
        return;
      }

      let allPdfCheckpointsPassed = true;

      checkpointsList.innerHTML = checkpoints.map((cp, cpIdx) => {
        const key = `${selectedSubmodule.id}_pdf_${cpIdx}`;
        const hasAnswered = pdfCheckpointsCompletedMap[key];
        if (!hasAnswered) allPdfCheckpointsPassed = false;
        const selected = selectedChoicesMap[key];

        return `
          <div class="p-4 sm:p-5 bg-white rounded-2xl border ${hasAnswered ? 'border-emerald-300 bg-emerald-50/20' : 'border-indigo-100'} shadow-sm space-y-3">
            <div class="flex items-center justify-between">
              <span class="px-2.5 py-0.5 rounded-full bg-indigo-100 text-indigo-800 text-[10px] font-black uppercase">
                ${cp.section || `Checkpoint #${cpIdx + 1}`}
              </span>
              <span class="text-xs font-bold ${hasAnswered ? 'text-emerald-600' : 'text-amber-600'}">
                ${hasAnswered ? '✓ Checkpoint Passed' : '⏱️ Pending Reflection'}
              </span>
            </div>
            
            <p class="text-xs sm:text-sm font-bold text-slate-900">${cp.question}</p>

            <div class="space-y-2">
              ${(cp.choices || []).map((ch, chIdx) => {
                const isSelected = selected === chIdx;
                const isCorrect = cp.correctIndex === chIdx;
                let optClass = "p-2.5 rounded-xl border text-xs font-bold cursor-pointer transition-all flex items-center justify-between ";
                if (hasAnswered) {
                  if (isCorrect) optClass += "bg-emerald-50 border-emerald-400 text-emerald-900";
                  else if (isSelected) optClass += "bg-rose-50 border-rose-400 text-rose-900";
                  else optClass += "bg-slate-50 border-slate-200 text-slate-400 opacity-60";
                } else {
                  optClass += "bg-slate-50 border-slate-200 hover:bg-slate-100 text-slate-700";
                }

                return `
                  <div onclick="submitPDFCheckpointAnswer('${key}', ${cpIdx}, ${chIdx})" class="${optClass}">
                    <span>${ch}</span>
                    ${hasAnswered && isCorrect ? '<span class="text-emerald-600">✓ Correct</span>' : ''}
                    ${hasAnswered && isSelected && !isCorrect ? '<span class="text-rose-600">✕ Incorrect</span>' : ''}
                  </div>
                `;
              }).join('')}
            </div>

            ${hasAnswered ? `
              <div class="p-3 rounded-xl bg-teal-50 border border-teal-200 text-xs text-teal-900 space-y-1">
                <span class="font-extrabold uppercase text-[10px] text-teal-800">Author Exemplar Explanation:</span>
                <p>${cp.exemplar || cp.feedbacks?.[cp.correctIndex] || "Great reflection!"}</p>
              </div>
            ` : ''}
          </div>
        `;
      }).join('');

      const btnUnlock = document.getElementById('btn-unlock-pdf-reflections');
      const lockText = document.getElementById('pdf-lock-text');
      if (btnUnlock && lockText) {
        if (allPdfCheckpointsPassed) {
          btnUnlock.disabled = false;
          btnUnlock.className = "bg-teal-700 hover:bg-teal-600 text-white cursor-pointer px-5 py-2.5 rounded-xl text-xs font-extrabold self-end sm:self-auto shadow-md";
          btnUnlock.innerText = "✓ Checkpoints Completed! Unlock Final Reflections →";
          lockText.innerText = "✓ All PDF checkpoints verified. Click to proceed to final reflections.";
        } else {
          btnUnlock.disabled = true;
          btnUnlock.className = "bg-slate-300 text-slate-500 cursor-not-allowed px-5 py-2.5 rounded-xl text-xs font-extrabold self-end sm:self-auto";
          btnUnlock.innerText = "🔒 Answer Checkpoints to Unlock";
        }
      }
    }

    function submitPDFCheckpointAnswer(key, cpIdx, chIdx) {
      if (pdfCheckpointsCompletedMap[key]) return;
      selectedChoicesMap[key] = chIdx;
      pdfCheckpointsCompletedMap[key] = true;

      const steps = selectedSubmodule?.videoSteps || [];
      let currentStep = steps[activeVideoStepIndex];
      if (!currentStep && selectedSubmodule?.pdfDoc) {
        currentStep = {
          format: 'pdf',
          title: selectedSubmodule.pdfDoc.title,
          pdfUrl: selectedSubmodule.pdfDoc.url,
          pdfCheckpoints: selectedSubmodule.pdfDoc.embeddedCheckpoints || [],
          transcript: ""
        };
      }
      const checkpoints = currentStep?.pdfCheckpoints || currentStep?.embeddedCheckpoints || [];
      const cp = checkpoints[cpIdx];
      if (!cp) return;
      const isCorrect = cp.correctIndex === chIdx;

      // Log attempt to Admin Dashboard (DELIVERABLE #8)
      logAdminAttempt({
        companionName: "Priya Sharma (Trainee)",
        type: "PDF_CHECKPOINT",
        typeName: `PDF Reading Checkpoint #${cpIdx + 1}`,
        moduleTitle: `${selectedSubmodule.title} (${cp.section || 'Reading'})`,
        question: cp.question,
        submittedAnswer: cp.choices[chIdx],
        status: isCorrect ? "Correct (100%)" : "Incorrect / Reviewed",
        isCorrect: isCorrect,
        exemplar: cp.exemplar || cp.feedbacks?.[cp.correctIndex] || "Review low-arousal de-escalation guidelines."
      });

      renderStudentPDFView(currentStep);
    }

    function unlockPDFReflections() {
      document.getElementById('student-reflections-section').classList.remove('hidden');
      document.getElementById('student-reflections-section').scrollIntoView({ behavior: 'smooth' });
    }

    // =========================================================================
    // VIDEO PLAYER & NON-SKIPPABLE IN-VIDEO CHECKPOINT (DELIVERABLE #1)
    // =========================================================================
    let currentActiveInVideoCheckpoint = null;
    let answeredInVideoCheckpointsMap = {};

    function renderUniversalVideoPlayer(videoUrl, titleOverlay, targetId = 'video-player-container', isLxT = false) {
      const container = document.getElementById(targetId);
      if (!container) return;

      currentActiveInVideoCheckpoint = null;
      const mainModal = document.getElementById(isLxT ? 'lxt-in-video-checkpoint-modal' : 'in-video-checkpoint-modal');
      if (mainModal) mainModal.classList.add('hidden');

      // Native clean HTML5 video with timeupdate listener
      container.innerHTML = `
        <video class="w-full h-full object-cover focus:outline-none" controls playsinline preload="auto" ontimeupdate="${isLxT ? 'onLxTVideoProgress(this)' : 'onVideoProgress(this)'}" onended="${isLxT ? 'onLxTVideoEnded()' : 'onVideoEnded()'}">
          <source src="${videoUrl}" type="video/mp4">
        </video>
        <div class="absolute top-3 left-3 bg-slate-950/80 px-3 py-1.5 rounded-lg text-xs text-teal-300 font-bold flex items-center gap-2 backdrop-blur-sm pointer-events-none">
          <span class="w-2.5 h-2.5 rounded-full bg-teal-400 animate-ping"></span>
          <span>${titleOverlay}</span>
        </div>
      `;
    }

    function onVideoProgress(vid) {
      if (currentActiveInVideoCheckpoint) {
        vid.pause();
        return;
      }
      const cur = vid.currentTime;
      const dur = vid.duration;
      if (dur > 0) {
        const pct = (cur / dur) * 100;
        const bar = document.getElementById('video-progress-bar');
        if (bar) bar.style.width = `${Math.min(pct, 100)}%`;
      }
      checkInVideoPlayback(cur, false);
    }

    function checkInVideoPlayback(currentTime, isLxT) {
      if (currentActiveInVideoCheckpoint) return;
      const steps = isLxT ? selectedSubmodule.lxt.videoSteps : selectedSubmodule.videoSteps;
      const idx = isLxT ? activeLxTVideoStepIndex : activeVideoStepIndex;
      const vStep = steps[idx];
      if (!vStep || !vStep.inVideoCheckpoints) return;

      vStep.inVideoCheckpoints.forEach((ivc, cpIdx) => {
        const targetSeconds = (ivc.timeMin || 0) * 60 + (ivc.timeSec || 0);
        const key = `${selectedSubmodule.id}_${isLxT ? 'lxt' : 'main'}_${idx}_${cpIdx}`;
        if (currentTime >= targetSeconds && !answeredInVideoCheckpointsMap[key]) {
          currentActiveInVideoCheckpoint = { key, ivc, idx: cpIdx, isLxT };
          pauseVideoPlayback(isLxT);
          renderInVideoCheckpointModal(ivc, key, isLxT);
        }
      });
    }

    function pauseVideoPlayback(isLxT) {
      const containerId = isLxT ? 'lxt-video-player-container' : 'video-player-container';
      const v = document.querySelector(`#${containerId} video`);
      if (v) v.pause();
    }

    function resumeVideoPlayback(isLxT) {
      const containerId = isLxT ? 'lxt-video-player-container' : 'video-player-container';
      const v = document.querySelector(`#${containerId} video`);
      if (v) v.play().catch(() => {});
    }

    // MOBILE-RESPONSIVE IN-VIDEO CHECKPOINT MODAL (DELIVERABLE #1)
    let hasEvaluatedInVideoCheckpoint = false;
    let selectedInVideoChoiceIndex = null;

    function renderInVideoCheckpointModal(ivc, key, isLxT) {
      currentActiveInVideoCheckpoint = { key, ivc, isLxT };
      hasEvaluatedInVideoCheckpoint = false;
      selectedInVideoChoiceIndex = null;

      const modalId = isLxT ? 'lxt-in-video-checkpoint-modal' : 'in-video-checkpoint-modal';
      const modal = document.getElementById(modalId);
      if (!modal) return;

      const minStr = String(ivc.timeMin || 0).padStart(2, '0');
      const secStr = String(ivc.timeSec || 0).padStart(2, '0');

      modal.innerHTML = `
        <div class="space-y-4">
          <div class="flex items-center justify-between border-b border-slate-800 pb-2">
            <span class="px-2.5 py-0.5 rounded-full bg-amber-400/20 text-amber-300 text-xs font-black uppercase border border-amber-400/30 flex items-center gap-1.5">
              <span class="w-2 h-2 rounded-full bg-amber-400 animate-ping"></span>
              <span>⏸️ Reflection Checkpoint (${minStr}:${secStr})</span>
            </span>
            <span class="text-[10px] font-black uppercase text-amber-400 bg-amber-950/60 px-2 py-0.5 rounded border border-amber-500/30">
              🔒 Non-Skippable
            </span>
          </div>

          <h3 class="text-sm sm:text-base font-extrabold text-white leading-snug">${ivc.question}</h3>

          <div class="space-y-2">
            ${(ivc.choices || []).map((ch, cIdx) => `
              <div onclick="selectInVideoChoice(${cIdx})" id="ivc-opt-${cIdx}" class="p-3 rounded-xl bg-slate-900/90 border border-slate-800 text-xs font-bold text-slate-200 hover:bg-slate-800/90 cursor-pointer transition-all flex items-center justify-between">
                <span>${ch}</span>
                <span class="w-4 h-4 rounded-full border border-slate-600 flex items-center justify-center text-[10px]"></span>
              </div>
            `).join('')}
          </div>

          <!-- Instant Pedagogical Feedback Box -->
          <div id="ivc-feedback-box" class="hidden"></div>
        </div>

        <div class="pt-4 border-t border-slate-800 mt-4 flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <span id="ivc-action-hint" class="text-[11px] text-amber-200/80 font-medium">Select an answer choice to evaluate</span>
          <button id="btn-submit-ivc" disabled onclick="submitInVideoCheckpointChoice('${key}', ${isLxT})" class="bg-slate-700 text-slate-400 cursor-not-allowed px-5 py-2.5 rounded-xl text-xs font-black transition-all">
            Submit & Check Answer →
          </button>
        </div>
      `;

      modal.classList.remove('hidden');
    }

    function selectInVideoChoice(cIdx) {
      if (hasEvaluatedInVideoCheckpoint) return; // Prevent changing after evaluated
      selectedInVideoChoiceIndex = cIdx;
      const opts = document.querySelectorAll('[id^="ivc-opt-"]');
      opts.forEach((o, i) => {
        if (i === cIdx) {
          o.className = "p-3 rounded-xl bg-teal-950/90 border-2 border-teal-400 text-xs font-black text-teal-200 flex items-center justify-between shadow-md";
          o.querySelector('span:last-child').innerHTML = "●";
        } else {
          o.className = "p-3 rounded-xl bg-slate-900/90 border border-slate-800 text-xs font-bold text-slate-400 opacity-60 flex items-center justify-between";
          o.querySelector('span:last-child').innerHTML = "";
        }
      });

      const btn = document.getElementById('btn-submit-ivc');
      if (btn) {
        btn.disabled = false;
        btn.className = "bg-teal-600 hover:bg-teal-500 text-white cursor-pointer px-5 py-2.5 rounded-xl text-xs font-black transition-all shadow-md";
      }
    }

    function submitInVideoCheckpointChoice(key, isLxT) {
      if (selectedInVideoChoiceIndex === null) return;
      const ivc = currentActiveInVideoCheckpoint?.ivc;
      if (!ivc) return;

      const modalId = isLxT ? 'lxt-in-video-checkpoint-modal' : 'in-video-checkpoint-modal';
      const modal = document.getElementById(modalId);

      // STEP 2: IF ALREADY EVALUATED, PROCEED & RESUME VIDEO
      if (hasEvaluatedInVideoCheckpoint) {
        if (modal) modal.classList.add('hidden');
        answeredInVideoCheckpointsMap[key] = true;
        currentActiveInVideoCheckpoint = null;
        selectedInVideoChoiceIndex = null;
        hasEvaluatedInVideoCheckpoint = false;
        resumeVideoPlayback(isLxT);
        return;
      }

      // STEP 1: EVALUATE & SHOW DETAILED PEDAGOGICAL FEEDBACK
      const isCorrect = ivc.correctIndex === selectedInVideoChoiceIndex;

      // Log attempt to Admin Dashboard (DELIVERABLE #8)
      logAdminAttempt({
        companionName: "Priya Sharma (Trainee)",
        type: "IN_VIDEO_CHECKPOINT",
        typeName: `In-Video Reflection (${String(ivc.timeMin||0).padStart(2,'0')}:${String(ivc.timeSec||0).padStart(2,'0')})`,
        moduleTitle: selectedSubmodule ? selectedSubmodule.title : "Module Lesson",
        question: ivc.question,
        submittedAnswer: ivc.choices[selectedInVideoChoiceIndex],
        status: isCorrect ? "Correct (100%)" : "Incorrect / Reviewed",
        isCorrect: isCorrect,
        exemplar: ivc.exemplar || "Strength-based mentorship respects sensory limits."
      });

      hasEvaluatedInVideoCheckpoint = true;

      // Update choice option borders & badges
      const opts = document.querySelectorAll('[id^="ivc-opt-"]');
      opts.forEach((o, i) => {
        if (i === ivc.correctIndex) {
          o.className = "p-3 rounded-xl bg-emerald-950/90 border-2 border-emerald-400 text-xs font-black text-emerald-200 flex items-center justify-between shadow-md";
          o.querySelector('span:last-child').innerHTML = "✓";
        } else if (i === selectedInVideoChoiceIndex && !isCorrect) {
          o.className = "p-3 rounded-xl bg-rose-950/90 border-2 border-rose-500 text-xs font-black text-rose-200 flex items-center justify-between shadow-md";
          o.querySelector('span:last-child').innerHTML = "✕";
        } else {
          o.className = "p-3 rounded-xl bg-slate-900/60 border border-slate-800 text-xs font-medium text-slate-500 opacity-50 flex items-center justify-between";
        }
      });

      const feedbackBox = document.getElementById('ivc-feedback-box');
      if (feedbackBox) {
        const feedbackText = ivc.feedbacks?.[selectedInVideoChoiceIndex] || (isCorrect ? "Correct! Excellent strength-based reflection." : "Review the correct response highlighted above.");
        feedbackBox.className = `p-3.5 rounded-2xl border text-xs space-y-1.5 ${isCorrect ? 'bg-emerald-950/70 border-emerald-500/50 text-emerald-200' : 'bg-amber-950/70 border-amber-500/50 text-amber-200'}`;
        feedbackBox.innerHTML = `
          <div class="flex items-center gap-1.5 font-black uppercase text-[10px] ${isCorrect ? 'text-emerald-400' : 'text-amber-400'}">
            <span>${isCorrect ? '✓ Correct Choice' : '⚠️ Learning Review'}</span>
          </div>
          <p class="leading-relaxed font-semibold">${feedbackText}</p>
          <div class="pt-1.5 border-t border-slate-700/60 text-[11px] text-teal-300">
            <strong>Exemplar Guidance:</strong> ${ivc.exemplar || "Focus on strength-based co-regulation."}
          </div>
        `;
        feedbackBox.classList.remove('hidden');
      }

      const hint = document.getElementById('ivc-action-hint');
      if (hint) {
        hint.innerText = "Review feedback above, then continue.";
        hint.className = "text-[11px] text-emerald-300 font-bold";
      }

      const btn = document.getElementById('btn-submit-ivc');
      if (btn) {
        btn.innerText = "Continue Video Playback ▶";
        btn.className = "bg-teal-600 hover:bg-teal-500 text-white cursor-pointer px-5 py-2.5 rounded-xl text-xs font-black transition-all shadow-lg shadow-teal-600/30";
      }
    }

    function onVideoEnded() {
      const banner = document.getElementById('video-completion-banner');
      const lockText = document.getElementById('video-lock-text');
      const btn = document.getElementById('btn-unlock-reflections');

      if (banner) banner.className = "p-4 rounded-2xl bg-teal-50 border border-teal-200 flex flex-col sm:flex-row sm:items-center justify-between gap-3";
      if (lockText) lockText.innerText = "✓ Video completed! Unlock reflection activities below.";
      if (btn) {
        btn.disabled = false;
        btn.className = "bg-teal-700 hover:bg-teal-600 text-white cursor-pointer px-5 py-2.5 rounded-xl text-xs font-extrabold shadow-md transition-all self-end sm:self-auto";
        btn.innerText = "Unlock Reflections →";
      }
    }

    function unlockReflections() {
      document.getElementById('student-reflections-section').classList.remove('hidden');
      document.getElementById('student-reflections-section').scrollIntoView({ behavior: 'smooth' });
    }

    function renderSubmoduleReflections(step, sub) {
      const mcqsContainer = document.getElementById('student-mcqs-list');
      const subjsContainer = document.getElementById('student-subjectives-list');
      if (!mcqsContainer || !subjsContainer) return;

      const mcqs = step?.mcqs || [];
      mcqsContainer.innerHTML = mcqs.map((m, mIdx) => {
        const key = `${sub.id}_mcq_${mIdx}`;
        const selected = selectedChoicesMap[key];
        const isAnswered = selected !== undefined;

        return `
          <div class="p-5 bg-slate-50 rounded-2xl border border-slate-200 space-y-3">
            <span class="text-[10px] font-black uppercase text-teal-800 bg-teal-100 px-2 py-0.5 rounded">Scenario MCQ #${mIdx + 1}</span>
            <p class="text-xs sm:text-sm font-bold text-slate-900">${m.question}</p>
            <div class="space-y-2">
              ${(m.choices || []).map((c, cIdx) => {
                const isSelected = selected === cIdx;
                const isCorrect = m.correctIndex === cIdx;
                let cClass = "p-3 rounded-xl border text-xs font-bold cursor-pointer transition-all flex items-center justify-between ";
                if (isAnswered) {
                  if (isCorrect) cClass += "bg-emerald-50 border-emerald-400 text-emerald-900";
                  else if (isSelected) cClass += "bg-rose-50 border-rose-400 text-rose-900";
                  else cClass += "bg-slate-50 border-slate-200 text-slate-400 opacity-60";
                } else {
                  cClass += "bg-white border-slate-200 hover:bg-slate-100 text-slate-700";
                }
                return `
                  <div onclick="submitReflectionMCQ('${key}', ${mIdx}, ${cIdx})" class="${cClass}">
                    <span>${c}</span>
                    ${isAnswered && isCorrect ? '<span class="text-emerald-600">✓ Correct</span>' : ''}
                    ${isAnswered && isSelected && !isCorrect ? '<span class="text-rose-600">✕ Incorrect</span>' : ''}
                  </div>
                `;
              }).join('')}
            </div>
            ${isAnswered ? `
              <div class="p-3 bg-white rounded-xl border border-teal-200 text-xs text-teal-900">
                <strong>Feedback:</strong> ${m.feedbacks?.[selected] || 'Well done!'}
              </div>
            ` : ''}
          </div>
        `;
      }).join('');

      const subjs = step?.subjectives || [];
      subjsContainer.innerHTML = subjs.map((s, sIdx) => {
        const key = `${sub.id}_subj_${sIdx}`;
        const isRevealed = revealedExemplarsMap[key];

        return `
          <div class="p-5 bg-slate-50 rounded-2xl border border-slate-200 space-y-3">
            <span class="text-[10px] font-black uppercase text-indigo-800 bg-indigo-100 px-2 py-0.5 rounded">Scenario Reflection #${sIdx + 1}</span>
            <p class="text-xs sm:text-sm font-bold text-slate-900">${s.prompt}</p>
            <textarea rows="2" class="w-full rounded-xl border border-slate-200 p-3 text-xs bg-white" placeholder="Write your practical de-escalation plan..."></textarea>
            <div class="flex items-center justify-between">
              <button onclick="revealExemplar('${key}')" class="text-xs font-bold text-teal-700 hover:underline">
                ${isRevealed ? '✓ Author Reference Answer Unlocked' : '💡 Reveal Author Exemplar'}
              </button>
            </div>
            ${isRevealed ? `
              <div class="p-3 bg-indigo-50 border border-indigo-200 rounded-xl text-xs text-indigo-950">
                <strong>Author Exemplar Feedback:</strong> ${s.exemplar}
              </div>
            ` : ''}
          </div>
        `;
      }).join('');
    }

    function submitReflectionMCQ(key, mIdx, cIdx) {
      if (selectedChoicesMap[key] !== undefined) return;
      selectedChoicesMap[key] = cIdx;
      const mod = publishedDb.find(m => m.id === selectedModuleId);
      const step = selectedSubmodule.videoSteps[activeVideoStepIndex] || selectedSubmodule.pdfDoc;
      const m = step.mcqs[mIdx];
      const isCorrect = m.correctIndex === cIdx;

      logAdminAttempt({
        companionName: "Priya Sharma (Trainee)",
        type: "IN_VIDEO_CHECKPOINT",
        typeName: `Post-Lesson MCQ #${mIdx + 1}`,
        moduleTitle: selectedSubmodule.title,
        question: m.question,
        submittedAnswer: m.choices[cIdx],
        status: isCorrect ? "Correct (100%)" : "Incorrect / Reviewed",
        isCorrect: isCorrect,
        exemplar: m.feedbacks?.[m.correctIndex] || "Review scenario notes."
      });

      renderSubmoduleReflections(step, selectedSubmodule);
    }

    function revealExemplar(key) {
      revealedExemplarsMap[key] = true;
      const step = selectedSubmodule.videoSteps[activeVideoStepIndex] || selectedSubmodule.pdfDoc;
      renderSubmoduleReflections(step, selectedSubmodule);
    }

    function finishCurrentVideoStep() {
      videoStepFinishedMap[`${selectedSubmodule.id}_${activeVideoStepIndex}`] = true;
      submoduleFinishedMap[selectedSubmodule.id] = true;
      showToast("✓ Submodule completed! You unlocked the LxT extension trajectory.");
      updateLxTCardStatus(selectedSubmodule);
    }

    function updateLxTCardStatus(sub) {
      const isDone = submoduleFinishedMap[sub.id];
      const lockStatus = document.getElementById('lxt-lock-status');
      const btn = document.getElementById('btn-launch-lxt');

      if (isDone && sub.lxt && sub.lxt.videoSteps && sub.lxt.videoSteps.length > 0) {
        if (lockStatus) {
          lockStatus.className = "text-xs font-bold text-emerald-300";
          lockStatus.innerText = "🔓 Unlocked & Ready";
        }
        if (btn) {
          btn.disabled = false;
          btn.className = "bg-teal-600 hover:bg-teal-500 text-white cursor-pointer px-5 py-2.5 rounded-xl text-xs font-extrabold shadow-md transition-all";
          btn.innerText = "Launch LxT Extension Trajectory →";
        }
      }
    }

    function openLxTExtensionLesson() {
      document.getElementById('student-level-content').classList.add('hidden');
      document.getElementById('student-level-lxt-view').classList.remove('hidden');
      activeLxTVideoStepIndex = 0;
      renderLxTExtensionContent();
    }

    function renderLxTExtensionContent() {
      const lxt = selectedSubmodule.lxt;
      const vStep = lxt.videoSteps[activeLxTVideoStepIndex];
      document.getElementById('lxt-view-title').innerText = lxt.title;
      renderUniversalVideoPlayer(vStep.videoUrl, vStep.title, 'lxt-video-player-container', true);
      document.getElementById('lxt-transcript-text').innerText = vStep.transcript || '';
    }

    function onLxTVideoProgress(vid) {
      if (currentActiveInVideoCheckpoint) {
        vid.pause();
        return;
      }
      checkInVideoPlayback(vid.currentTime, true);
    }

    function onLxTVideoEnded() {
      const banner = document.getElementById('lxt-video-completion-banner');
      const text = document.getElementById('lxt-video-lock-text');
      const btn = document.getElementById('btn-unlock-lxt-reflections');
      if (banner) banner.className = "p-4 rounded-2xl bg-teal-50 border border-teal-200 flex flex-col sm:flex-row sm:items-center justify-between gap-3";
      if (text) text.innerText = "✓ Extension video finished! Reflections unlocked.";
      if (btn) {
        btn.disabled = false;
        btn.className = "bg-teal-700 hover:bg-teal-600 text-white cursor-pointer px-5 py-2.5 rounded-xl text-xs font-extrabold shadow-md";
        btn.innerText = "Unlock Extension Reflections →";
      }
    }

    function unlockLxTReflections() {
      document.getElementById('lxt-reflections-section').classList.remove('hidden');
    }

    function finishCurrentLxTVideoStep() {
      showToast("✓ LxT Extension Trajectory Completed!");
      goSubmodules();
    }

    // ==========================================
    // MASTER QUIZ (END-OF-MODULE CERTIFICATION)
    // ==========================================
    function openMasterQuiz() {
      const mod = publishedDb.find(m => m.id === selectedModuleId);
      document.getElementById('student-level-modules').classList.add('hidden');
      document.getElementById('student-level-submodules').classList.add('hidden');
      document.getElementById('student-level-content').classList.add('hidden');
      document.getElementById('student-level-lxt-view').classList.add('hidden');
      document.getElementById('student-level-masterquiz').classList.remove('hidden');

      document.getElementById('master-quiz-title').innerText = `End-of-Module Master Quiz: ${mod.title}`;
      renderMasterQuiz(mod);
    }

    function renderMasterQuiz(mod) {
      const container = document.getElementById('master-quiz-questions-list');
      if (!container || !mod) return;
      const quiz = mod.masterQuiz || [];
      const isSubmitted = masterQuizSubmittedMap[mod.id];

      container.innerHTML = quiz.map((q, idx) => {
        const isSubj = q.type === 'subjective';
        const key = `master_${mod.id}_${idx}`;
        const selected = selectedChoicesMap[key];

        return `
          <div class="p-5 sm:p-6 bg-slate-50 rounded-3xl border border-slate-200 space-y-4 shadow-sm">
            <span class="text-[10px] font-black uppercase ${isSubj ? 'text-indigo-800 bg-indigo-100' : 'text-teal-800 bg-teal-100'} px-2.5 py-1 rounded-lg">
              ${isSubj ? '✍️ Subjective Master Question' : '❓ Master MCQ'} #${idx + 1}
            </span>
            <p class="text-xs sm:text-sm font-black text-slate-900">${isSubj ? q.prompt : q.question}</p>

            ${isSubj ? `
              <textarea rows="3" class="w-full rounded-2xl border border-slate-200 p-4 text-xs sm:text-sm bg-white" placeholder="Outline your step-by-step de-escalation plan..."></textarea>
              ${isSubmitted ? `
                <div class="p-4 bg-indigo-50 border border-indigo-200 rounded-2xl text-xs text-indigo-950 space-y-1">
                  <strong>Author Reference Answer:</strong>
                  <p>${q.exemplar}</p>
                </div>
              ` : ''}
            ` : `
              <div class="space-y-2">
                ${(q.choices || []).map((ch, cIdx) => {
                  const isSelected = selected === cIdx;
                  const isCorrect = q.correctIndex === cIdx;
                  let optClass = "p-3 rounded-xl border text-xs font-bold cursor-pointer transition-all flex items-center justify-between ";
                  if (isSubmitted) {
                    if (isCorrect) optClass += "bg-emerald-50 border-emerald-400 text-emerald-900";
                    else if (isSelected) optClass += "bg-rose-50 border-rose-400 text-rose-900";
                    else optClass += "bg-white border-slate-200 text-slate-400 opacity-60";
                  } else {
                    optClass += isSelected ? "bg-indigo-50 border-indigo-500 text-indigo-950 font-black" : "bg-white border-slate-200 hover:bg-slate-100 text-slate-700";
                  }
                  return `
                    <div onclick="selectMasterMCQ('${key}', ${cIdx})" class="${optClass}">
                      <span>${ch}</span>
                      ${isSubmitted && isCorrect ? '<span class="text-emerald-600">✓ Correct</span>' : ''}
                    </div>
                  `;
                }).join('')}
              </div>
            `}
          </div>
        `;
      }).join('');
    }

    function selectMasterMCQ(key, cIdx) {
      const mod = publishedDb.find(m => m.id === selectedModuleId);
      if (masterQuizSubmittedMap[mod.id]) return;
      selectedChoicesMap[key] = cIdx;
      renderMasterQuiz(mod);
    }

    function submitMasterQuiz() {
      const mod = publishedDb.find(m => m.id === selectedModuleId);
      masterQuizSubmittedMap[mod.id] = true;

      // Log attempt to Admin Dashboard (DELIVERABLE #8)
      logAdminAttempt({
        companionName: "Priya Sharma (Trainee)",
        type: "MASTER_QUIZ",
        typeName: "End-of-Module Master Quiz",
        moduleTitle: mod.title,
        question: "Master Certification Assessment",
        submittedAnswer: "Completed all MCQs & Submitted Subjective De-escalation Protocol",
        status: "Passed (100%)",
        isCorrect: true,
        exemplar: "Demonstrated full mastery of sensory co-regulation strategies."
      });

      document.getElementById('master-quiz-celebration-banner').classList.remove('hidden');
      document.getElementById('master-quiz-submit-container').classList.add('hidden');
      renderMasterQuiz(mod);
      showToast("🎉 Congratulations! You have earned your Module Master Certification.");
    }

    // =========================================================================
    // ADMIN DASHBOARD IMPLEMENTATION (DELIVERABLE #8)
    // =========================================================================
    function logAdminAttempt(att) {
      const newAtt = {
        id: `att-${Date.now()}`,
        timestamp: "Just Now",
        ...att
      };
      adminAttempts.unshift(newAtt);
      saveToStorage(STORAGE_KEY_ATTEMPTS, adminAttempts);
      if (currentView === 'admin') {
        renderAdminDashboard();
      }
    }

    function renderAdminDashboard() {
      // Calculate KPIs
      const companionsSet = new Set(adminAttempts.map(a => a.companionName));
      const totalAttempts = adminAttempts.length;
      const quizzesPassed = adminAttempts.filter(a => a.type === 'MASTER_QUIZ' && a.isCorrect).length;
      const correctAttempts = adminAttempts.filter(a => a.isCorrect).length;
      const passRate = totalAttempts > 0 ? Math.round((correctAttempts / totalAttempts) * 100) : 100;

      document.getElementById('admin-kpi-companions').innerText = Math.max(companionsSet.size, 1);
      document.getElementById('admin-kpi-attempts').innerText = totalAttempts;
      document.getElementById('admin-kpi-passrate').innerText = `${passRate}%`;
      document.getElementById('admin-kpi-quizzes').innerText = quizzesPassed;

      renderAdminAttemptsTable();
    }

    function renderAdminAttemptsTable() {
      const tbody = document.getElementById('admin-attempts-tbody');
      if (!tbody) return;

      const fComp = document.getElementById('admin-filter-companion').value;
      const fType = document.getElementById('admin-filter-type').value;

      let filtered = adminAttempts;
      if (fComp !== 'ALL') filtered = filtered.filter(a => a.companionName.includes(fComp) || fComp.includes(a.companionName));
      if (fType !== 'ALL') filtered = filtered.filter(a => a.type === fType);

      if (filtered.length === 0) {
        tbody.innerHTML = `
          <tr>
            <td colspan="6" class="p-8 text-center text-slate-400 italic">No activity attempts match the selected filter.</td>
          </tr>
        `;
        return;
      }

      tbody.innerHTML = filtered.map(att => {
        let typeBadge = "bg-teal-50 text-teal-800 border-teal-200";
        if (att.type === 'PDF_CHECKPOINT') typeBadge = "bg-indigo-50 text-indigo-800 border-indigo-200";
        else if (att.type === 'MASTER_QUIZ') typeBadge = "bg-purple-50 text-purple-800 border-purple-200";
        else if (att.type === 'LXI_DISCUSSION') typeBadge = "bg-amber-50 text-amber-800 border-amber-200";

        return `
          <tr class="hover:bg-slate-50/80 transition-colors">
            <td class="p-3.5 font-extrabold text-slate-900 flex items-center gap-2">
              <span class="w-6 h-6 rounded-full bg-slate-200 text-slate-700 flex items-center justify-center text-[10px] font-black">
                ${att.companionName.charAt(0)}
              </span>
              <span>${att.companionName}</span>
            </td>
            <td class="p-3.5">
              <span class="px-2 py-0.5 rounded-md text-[10px] font-black border ${typeBadge}">
                ${att.typeName || att.type}
              </span>
            </td>
            <td class="p-3.5 text-slate-600 font-bold max-w-xs truncate">${att.moduleTitle}</td>
            <td class="p-3.5 text-slate-400 text-[11px]">${att.timestamp}</td>
            <td class="p-3.5">
              <span class="px-2 py-0.5 rounded-full text-[10px] font-black ${att.isCorrect ? 'bg-emerald-100 text-emerald-800' : 'bg-amber-100 text-amber-800'}">
                ${att.status}
              </span>
            </td>
            <td class="p-3.5 text-right">
              <button onclick="inspectAdminAttempt('${att.id}')" class="px-2.5 py-1 rounded-lg bg-slate-100 hover:bg-slate-200 text-slate-700 text-[11px] font-extrabold">
                Inspect 🔍
              </button>
            </td>
          </tr>
        `;
      }).join('');
    }

    function inspectAdminAttempt(attId) {
      const att = adminAttempts.find(a => a.id === attId);
      if (!att) return;

      const content = document.getElementById('admin-inspect-content');
      content.innerHTML = `
        <div class="space-y-3">
          <div class="flex items-center justify-between bg-slate-50 p-3 rounded-2xl border border-slate-100">
            <div>
              <span class="text-[10px] font-black uppercase text-slate-400">Companion</span>
              <p class="font-extrabold text-slate-900 text-sm">${att.companionName}</p>
            </div>
            <div class="text-right">
              <span class="text-[10px] font-black uppercase text-slate-400">Timestamp</span>
              <p class="text-slate-600 text-xs">${att.timestamp}</p>
            </div>
          </div>

          <div>
            <label class="block text-[10px] font-black uppercase text-slate-400 mb-0.5">Activity & Module</label>
            <p class="font-bold text-slate-800">${att.typeName} • ${att.moduleTitle}</p>
          </div>

          <div>
            <label class="block text-[10px] font-black uppercase text-slate-400 mb-0.5">Question Prompt</label>
            <p class="p-3 rounded-xl bg-slate-50 text-slate-800 font-semibold">${att.question}</p>
          </div>

          <div>
            <label class="block text-[10px] font-black uppercase text-slate-400 mb-0.5">Companion Submitted Response</label>
            <div class="p-3.5 rounded-xl border ${att.isCorrect ? 'bg-emerald-50/50 border-emerald-200 text-emerald-950' : 'bg-amber-50/50 border-amber-200 text-amber-950'} font-bold">
              ${att.submittedAnswer}
            </div>
          </div>

          <div>
            <label class="block text-[10px] font-black uppercase text-slate-400 mb-0.5">Author Exemplar / Feedback</label>
            <p class="p-3 rounded-xl bg-teal-50 border border-teal-200 text-teal-950">${att.exemplar || 'Standard exemplar guidance.'}</p>
          </div>
        </div>
      `;

      document.getElementById('admin-inspect-modal').classList.remove('hidden');
    }

    function closeAdminInspectModal() {
      document.getElementById('admin-inspect-modal').classList.add('hidden');
    }

    function simulateCompanionAttempt() {
      const companions = ["Priya Sharma (Trainee)", "Rahul Mehta", "Tanya Verma", "Jamson"];
      const randComp = companions[Math.floor(Math.random() * companions.length)];
      const types = [
        { type: "IN_VIDEO_CHECKPOINT", typeName: "In-Video Reflection (00:15)", q: "What is the core focus when mentoring neurodivergent children?", ans: "Building on unique strengths & providing sensory accommodations", correct: true },
        { type: "PDF_CHECKPOINT", typeName: "PDF Reading Checkpoint #1", q: "Recognizing early physiological signs of sensory agitation", ans: "Pupil dilation and repetitive motor pacing", correct: true },
        { type: "LXI_DISCUSSION", typeName: "Module LxI Discussion", q: "Non-verbal communication strategies in inclusive classrooms", ans: "I provide visual choice boards and allow 10-second pauses.", correct: true }
      ];
      const randType = types[Math.floor(Math.random() * types.length)];

      logAdminAttempt({
        companionName: randComp,
        type: randType.type,
        typeName: randType.typeName,
        moduleTitle: "Module 1: Foundations",
        question: randType.q,
        submittedAnswer: randType.ans,
        status: randType.correct ? "Correct (100%)" : "Reviewed",
        isCorrect: randType.correct,
        exemplar: "Co-regulation and processing pauses lower arousal."
      });

      renderAdminDashboard();
      showToast(`⚡ Simulated new live attempt from ${randComp}!`);
    }

    function exportAttemptsCSV() {
      let csv = "ID,CompanionName,ActivityType,Module,Question,SubmittedAnswer,Status,Timestamp\n";
      adminAttempts.forEach(a => {
        csv += `"${a.id}","${a.companionName}","${a.typeName || a.type}","${a.moduleTitle}","${(a.question||'').replace(/"/g, '""')}","${(a.submittedAnswer||'').replace(/"/g, '""')}","${a.status}","${a.timestamp}"\n`;
      });

      const blob = new Blob([csv], { type: 'text/csv' });
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.setAttribute('hidden', '');
      a.setAttribute('href', url);
      a.setAttribute('download', `companion_attempts_${Date.now()}.csv`);
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      showToast("📥 Exported companion attempts log as CSV.");
    }

    function resetAttemptsLog() {
      if (confirm("Reset all companion attempt logs back to default sample records?")) {
        adminAttempts = JSON.parse(JSON.stringify(DEFAULT_ATTEMPTS));
        saveToStorage(STORAGE_KEY_ATTEMPTS, adminAttempts);
        renderAdminDashboard();
        showToast("Reset attempt logs.");
      }
    }

    // ==========================================
    // INITIALIZATION
    // ==========================================
    window.addEventListener('DOMContentLoaded', () => {
      // Default to student view on initial load
      switchView('student');
    });
  </script>
</body>
</html>
'''

with open(output_file, "w") as f:
    f.write(html_content)

print(f"Successfully generated {output_file} ({len(html_content)} bytes)")
