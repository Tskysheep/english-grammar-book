module.exports = {
  base: process.env.GITHUB == 'github' ? '/english-grammar-book/' : '/',
  dest: process.env.GITHUB == 'github' ? 'docs/.vuepress/github' : 'docs/.vuepress/dist',
  title: '《语法俱乐部》&《旋元佑进阶文法》',
  head: [
    ['script', {}, `
      (function () {
        function initToggle() {
          var isHome = document.querySelector('.home-link.router-link-active.router-link-exact-active') || document.querySelector('.hero');
          var existing = document.querySelector('.sidebar-toggle');
          if (isHome) {
            if (existing) existing.remove();
            document.body.classList.remove('sidebar-collapsed');
            return;
          }
          if (existing) return;
          var sidebar = document.querySelector('.sidebar');
          if (!sidebar) return;
          var btn = document.createElement('div');
          btn.className = 'sidebar-toggle';
          btn.title = '收起侧边栏';
          btn.innerHTML = '<svg viewBox="0 0 24 24" width="16" height="16" fill="currentColor"><path d="M15.41 7.41L14 6l-6 6 6 6 1.41-1.41L10.83 12z"/></svg>';
          document.body.appendChild(btn);
          var collapsed = localStorage.getItem('sidebar-collapsed') === 'true';
          if (collapsed) {
            document.body.classList.add('sidebar-collapsed');
            btn.classList.add('is-collapsed');
            btn.title = '展开侧边栏';
            btn.innerHTML = '<svg viewBox="0 0 24 24" width="16" height="16" fill="currentColor"><path d="M10 6L8.59 7.41 13.17 12l-4.58 4.59L10 18l6-6z"/></svg>';
          }
          btn.addEventListener('click', function () {
            collapsed = !collapsed;
            document.body.classList.toggle('sidebar-collapsed', collapsed);
            btn.classList.toggle('is-collapsed', collapsed);
            localStorage.setItem('sidebar-collapsed', collapsed);
            if (collapsed) {
              btn.title = '展开侧边栏';
              btn.innerHTML = '<svg viewBox="0 0 24 24" width="16" height="16" fill="currentColor"><path d="M10 6L8.59 7.41 13.17 12l-4.58 4.59L10 18l6-6z"/></svg>';
            } else {
              btn.title = '收起侧边栏';
              btn.innerHTML = '<svg viewBox="0 0 24 24" width="16" height="16" fill="currentColor"><path d="M15.41 7.41L14 6l-6 6 6 6 1.41-1.41L10.83 12z"/></svg>';
            }
          });
        }
        if (document.readyState === 'complete') { initToggle(); }
        else { window.addEventListener('load', function () { setTimeout(initToggle, 300); }); }
        var observer = new MutationObserver(function () { initToggle(); });
        observer.observe(document.body, { childList: true, subtree: true });
      })();
    `]
  ],
  plugins: [
    [
      'vuepress-plugin-right-anchor',
      {
        showDepth: 6,
        expand: {
          trigger: 'click',
          clickModeDefaultOpen: true
        }
      }
    ]
  ],
  themeConfig: {
    repo: 'Tskysheep/english-grammar-book',
    displayAllHeaders: true,
    smoothScroll: true,
    sidebar: {
      '/content/Ver1/': [
        ['Preface', '序'],
        'Introduction',
        'Contents',
        {
          title: '第一篇 初级句型--简单句',
          collapsable: false,
          children: [
            'Chapter01',
            'Chapter02',
            'Chapter03',
            'Chapter04',
            'Chapter05',
            'Chapter06',
            'Chapter07',
            'Chapter08',
            'Chapter09',
            'Chapter10',
            'Chapter11'
          ]
        },
        {
          title: '第二篇 中级句型--复句',
          collapsable: false,
          children: ['Chapter12', 'Chapter13', 'Chapter14', 'Chapter15']
        },
        {
          title: '第三篇 高级句型--简化从句',
          collapsable: false,
          children: ['Chapter16', 'Chapter17', 'Chapter18', 'Chapter19', 'Chapter20', 'Chapter21', 'Chapter22']
        }
      ],
      '/content/Ver3/': [
        ['Preface', '序'],
        'Guide',
        'Contents',
        {
          title: '第一篇 基本句型',
          collapsable: false,
          children: [
            'SimpleSentences',
            'NounPhrases',
            'Pronouns',
            'Adjective',
            'Adverb',
            'ComparativePattern',
            'Prepositions',
            'Participles'
          ]
        },
        {
          title: '第二篇 动词相关',
          collapsable: false,
          children: [
            'VerbTenses',
            'Voice',
            'Auxiliaries',
            'Moods',
            'Gerund',
            'Infinitive'
          ]
        },
        {
          title: '第三篇 合句与从句',
          collapsable: false,
          children: [
            'Conjunction',
            'CompoundSentences',
            'NounClauses',
            'AdverbClauses',
            'RelativeClauses',
            'SubjectVerbAgreement'
          ]
        },
        {
          title: '第四篇 从句简化',
          collapsable: false,
          children: [
            'Inversion',
            'ReducedClauses',
            'RelativeClausesReduced',
            'NounClausesReduced',
            'AdverbClausesReduced'
          ]
        },
        'Terminology'
      ]
    },
    nav: [
      { text: '第一版', link: '/content/Ver1/Preface' },
      { text: '第三版', link: '/content/Ver3/Preface' }
    ]
  }
};
