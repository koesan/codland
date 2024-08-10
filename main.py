from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quiz.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Veritabanı modelini tanımla
class Result(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(100), nullable=False)

# Veritabanını oluştur (eğer mevcut değilse)
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    # En yüksek skoru al
    highest_score = db.session.query(db.func.max(Result.score)).scalar() or 0
    total_questions = 10  # Güncellendi: 10 soru
    highest_score_percentage = (highest_score / total_questions) * 100
    return render_template('index.html', highest_score=highest_score_percentage)

@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    # Quiz sayfasında gösterilmek üzere en yüksek skoru al
    highest_score = db.session.query(db.func.max(Result.score)).scalar() or 0
    total_questions = 10  # Güncellendi: 10 soru
    highest_score_percentage = (highest_score / total_questions) * 100

    if request.method == 'POST':
        score = 0

        # Cevapları kontrol et (10 sorulu güncellenmiş hali)
        if request.form.get('q1') == 'OpenCV':
            score += 1
        if request.form.get('q2') == 'Flask':
            score += 1
        if request.form.get('q3') == 'All of the Above':
            score += 1
        if request.form.get('q4') == 'Provide the model via a REST API and communicate with Flask application':
            score += 1
        if request.form.get('q5') == 'Keras':
            score += 1
        if request.form.get('q6') == 'Natural Language Processing':
            score += 1
        if request.form.get('q7') == 'Web development':
            score += 1
        if request.form.get('q8') == 'db.create_all()':
            score += 1
        if request.form.get('q9') == 'OCR':
            score += 1
        if request.form.get('q10') == 'Representational State Transfer':
            score += 1

        # Yüzdelik hesapla
        score_percentage = (score / total_questions) * 100

        # Sonucu kaydet
        name = request.form.get('name', 'Anonymous')
        result = Result(score=score, name=name)
        db.session.add(result)
        db.session.commit()

        # En yüksek skoru güncelle
        highest_score = db.session.query(db.func.max(Result.score)).scalar() or 0
        highest_score_percentage = (highest_score / total_questions) * 100

        return render_template('result.html', score_percentage=score_percentage, highest_score_percentage=highest_score_percentage)

    return render_template('quiz.html', highest_score=highest_score_percentage)

if __name__ == '__main__':
    app.run(debug=True)
