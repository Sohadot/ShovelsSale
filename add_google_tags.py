"""
ShovelsSale.com — Add Google Analytics + Tag Manager to all HTML files
يضيف أكواد Google تلقائياً لكل ملفات HTML دفعة واحدة
شغّله مرة واحدة فقط
"""

import os

# ============================================================
# مسار مجلد الموقع على جهازك
# ============================================================
PROJECT_ROOT = r"C:\Users\Ahmed\Desktop\shovelssale"

# ============================================================
# أكواد Google — لا تغيّري هذا
# ============================================================
GTM_HEAD = """
    <!-- Google Tag Manager -->
    <script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':
    new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],
    j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
    'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
    })(window,document,'script','dataLayer','GTM-K83NSPVC');</script>
    <!-- End Google Tag Manager -->"""

GTM_BODY = """    <!-- Google Tag Manager (noscript) -->
    <noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-K83NSPVC"
    height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
    <!-- End Google Tag Manager (noscript) -->
"""

GA4 = """
    <!-- Google Analytics -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-VKVL5E97G3"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){dataLayer.push(arguments);}
      gtag('js', new Date());
      gtag('config', 'G-VKVL5E97G3');
    </script>"""

# ============================================================

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # تجنب الإضافة مرتين
    if 'GTM-K83NSPVC' in content:
        print(f"  ⏭ Already has GTM: {filepath}")
        return

    # أضف GTM + GA4 قبل </head>
    if '</head>' in content:
        content = content.replace('</head>', GTM_HEAD + GA4 + '\n  </head>')

    # أضف GTM noscript بعد <body>
    if '<body>' in content:
        content = content.replace('<body>', '<body>\n' + GTM_BODY)
    elif '<body ' in content:
        # body مع attributes مثل <body class="...">
        idx = content.find('<body ')
        end = content.find('>', idx) + 1
        body_tag = content[idx:end]
        content = content.replace(body_tag, body_tag + '\n' + GTM_BODY)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"  ✅ Updated: {filepath.replace(PROJECT_ROOT, '')}")

def main():
    print(f"\n{'='*55}")
    print(f"  Adding Google Analytics + GTM to all HTML files")
    print(f"{'='*55}\n")

    count = 0
    for root, dirs, files in os.walk(PROJECT_ROOT):
        # تجاهل مجلدات غير ضرورية
        dirs[:] = [d for d in dirs if d not in ['.git', 'scripts', 'node_modules']]
        for file in files:
            if file.endswith('.html') and file != '404.html':
                filepath = os.path.join(root, file)
                process_file(filepath)
                count += 1

    print(f"\n{'='*55}")
    print(f"  ✅ Done! Updated {count} HTML files.")
    print(f"  Now: GitHub Desktop → Commit → Push")
    print(f"{'='*55}\n")

if __name__ == "__main__":
    main()
