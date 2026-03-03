module.exports = {
  base: process.env.GITHUB == 'github' ? '/english-grammar-book/' : '/',
  dest: process.env.GITHUB == 'github' ? 'docs/.vuepress/github' : 'docs/.vuepress/dist',
  title: '首页',
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
