from dotenv import load_dotenv
import os
import json
import urllib.request
import urllib.error
load_dotenv()
from flask import Flask, request, render_template_string

app = Flask(__name__)

PAGE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="google-site-verification" content="e99qwkjj1EY6rG7uSWiXUjNCP59NSnEjnYuJ3VTMfoA" />
<meta name="viewport" content="width=device-width, initial-scale=1">

<title>أَثَر AI | مساعدك التعليمي الذكي</title>
<meta name="description" content="أَثَر AI مساعد تعليمي ذكي يساعد الطلاب على فهم الدروس والمواد الدراسية من خلال شروحات مبسطة وأمثلة وأسئلة تعليمية تفاعلية باللغة العربية.">
<meta name="robots" content="index, follow">
<link rel="canonical" href="https://athar-ai-4ir3.onrender.com/">

<meta property="og:type" content="website">
<meta property="og:title" content="أَثَر AI | مساعدك التعليمي الذكي">
<meta property="og:description" content="تعلم وافهم دروسك بسهولة مع أَثَر AI، مساعدك التعليمي الذكي.">
<meta property="og:url" content="https://athar-ai-4ir3.onrender.com/">
<meta property="og:locale" content="ar_AR">
<meta name="twitter:card" content="summary">
<meta name="twitter:title" content="أَثَر AI">
<meta name="twitter:description" content="مساعدك التعليمي الذكي لفهم الدروس باللغة العربية.">
<style>
body {
    margin: 0;
    font-family: Arial, sans-serif;
    background: #101a30;
    color: white;
    text-align: center;
}
header {
    padding: 35px 15px;
    background: linear-gradient(135deg, #172b50, #263f68);
    border-bottom: 3px solid #d6ad55;
}
h1 {
    color: #f1ca70;
    font-size: 42px;
    margin: 10px;
}
.subtitle { color: #d5dbea; }
main {
    max-width: 600px;
    margin: 35px auto;
    padding: 20px;
}
.card {
    background: #1b2943;
    padding: 25px;
    border-radius: 18px;
    border: 1px solid #3b4c6b;
}
input {
    width: 90%;
    padding: 15px;
    margin: 15px 0;
    border: 0;
    border-radius: 10px;
    font-size: 17px;
    text-align: right;
}
button {
    background: #d6ad55;
    color: #17233a;
    border: 0;
    padding: 13px 30px;
    border-radius: 10px;
    font-size: 17px;
    font-weight: bold;
}
.answer {
    background: #263957;
    padding: 15px;
    margin-top: 20px;
    border-radius: 10px;
    line-height: 1.8;
}
footer { color: #aebbd0; padding: 25px; }

.founder-card {
    background: linear-gradient(145deg, #202f4c, #17243b);
    border: 1px solid #d6ad55;
    border-radius: 18px;
    padding: 24px;
    margin: 25px auto;
    box-shadow: 0 5px 20px rgba(0,0,0,0.2);
}
.founder-card h2 {
    color: #f1ca70;
    font-size: 23px;
    margin-bottom: 12px;
}
.founder-name {
    color: #f1ca70;
    font-size: 22px;
    font-weight: bold;
    line-height: 1.8;
}
.founder-card p {
    color: #d5dbea;
    line-height: 2;
    font-size: 16px;
}

</style>
</head>
<body>
<header>
<h1>أَثَر AI</h1>
<p class="subtitle">تعلّم بذكاء، اصنع أثرًا</p>
</header>
<main>

<div class="founder-card">
    <h2>صاحبة فكرة ومؤسسة أثر AI</h2>
    <div class="founder-name">المهندسة مريم محمود حسن الحاج</div>
    <p>
        خبيرة وصاحبة رؤية طموحة، جمعت بين الإبداع التقني
        والإيمان برسالة التعليم، لتطلق فكرة أثر AI وتسعى
        إلى توظيف الذكاء الاصطناعي في خدمة الطلاب.
    </p>
    <p>
        انطلقت فكرة المشروع من إيمانها بأن كل طالب يستحق
        فرصة أفضل للفهم والتعلم، وأن التكنولوجيا يمكن أن
        تجعل المعرفة أقرب وأسهل وأكثر تفاعلاً.
    </p>
    <p>
        تهدف رؤيتها إلى بناء مساعد تعليمي ذكي باللغة العربية،
        يشرح الدروس، ويبسط المفاهيم، ويساعد الطلاب على اكتشاف
        قدراتهم وتحقيق طموحاتهم.
    </p>
    <p>
        <strong>أثر AI: لأن العلم لا يقتصر على الإجابة،
        بل يصنع أثراً يبقى في المستقبل.</strong>
    </p>
</div>

<div class="card">
<h2>مرحبًا بك في مساعدك الدراسي</h2>
<p>اكتب سؤالك الدراسي وسنبدأ رحلة التعلّم معًا.</p>
<form method="POST">
<input name="question" placeholder="اكتب سؤالك هنا..." required>
<br>
<button type="submit">اسأل أَثَر AI</button>
</form>
{% if answer %}
<div class="answer">{{ answer }}</div>
{% endif %}
</div>
</main>
<footer>أَثَر AI — مشروع تعليمي لخدمة الطلاب</footer>
</body>
</html>
"""


@app.route("/robots.txt")
def robots():
    return "User-agent: *\nAllow: /\nSitemap: https://athar-ai-4ir3.onrender.com/sitemap.xml\n", 200, {"Content-Type": "text/plain; charset=utf-8"}

@app.route("/sitemap.xml")
def sitemap():
    xml = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://athar-ai-4ir3.onrender.com/</loc>
  </url>
</urlset>"""
    return xml, 200, {"Content-Type": "application/xml; charset=utf-8"}


@app.route("/", methods=["GET", "POST"])
def home():
    answer = ""

    if request.method == "POST":
        question = request.form.get("question", "").strip()

        if question:
            api_key = os.getenv("GROQ_API_KEY")

            if not api_key:
                answer = "مفتاح الذكاء الاصطناعي غير مضبوط في إعدادات الخادم."
            else:
                payload = {
                    "model": "qwen/qwen3.8-27b",
                    "messages": [
                        {
                            "role": "system",
                            "content": (
                                "أنت أَثَر AI، مساعد تعليمي عربي. "
                                "ساعد الطلاب على فهم دروسهم، "
                                "واشرح المعلومات بوضوح وبأسلوب مبسط، "
                                "واستخدم أمثلة مناسبة لمستواهم الدراسي. "
                                "أجب باللغة العربية ما لم يطلب المستخدم لغة أخرى."
                            )
                        },
                        {
                            "role": "user",
                            "content": question
                        }
                    ],
                    "temperature": 0.4,
                    "max_tokens": 1200
                }

                req = urllib.request.Request(
                    "https://api.groq.com/openai/v1/chat/completions",
                    data=json.dumps(payload).encode("utf-8"),
                    headers={
                        "Authorization": "Bearer " + api_key,
                        "Content-Type": "application/json",
            "User-Agent": "AtharAI/1.0"
                    },
                    method="POST"
                )

                try:
                    with urllib.request.urlopen(req, timeout=60) as response:
                        result = json.loads(response.read().decode("utf-8"))

                    answer = result["choices"][0]["message"]["content"].strip()

                except urllib.error.HTTPError as e:
                    print("Groq HTTP error:", e.code)

                    if e.code == 401:
                        answer = "تعذر التحقق من مفتاح الذكاء الاصطناعي. راجع إعدادات المفتاح."
                    elif e.code == 429:
                        answer = "طلبات كثيرة حاليًا. حاول مجددًا بعد قليل."
                    else:
                        answer = "حدث خطأ أثناء الاتصال بالذكاء الاصطناعي. حاول مجددًا."

                except Exception as e:
                    print("Groq connection error:", type(e).__name__)
                    answer = "تعذر الاتصال بالذكاء الاصطناعي حاليًا. حاول مجددًا."

    return render_template_string(PAGE, answer=answer)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
