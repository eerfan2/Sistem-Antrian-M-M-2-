from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def queue_calculator():
    result = None
    error = None
    steps = None

    if request.method == 'POST':
        try:
            # Mengambil data dari form
            interarrival_time = float(request.form['interarrival_time'])
            service_time = float(request.form['service_time'])

            # Validasi
            if interarrival_time <= 0 or service_time <= 0:
                error = "Waktu antar kedatangan dan waktu pelayanan harus lebih besar dari nol."
            elif interarrival_time < service_time:
                error = "Waktu Antar Kedatangan harus lebih besar atau sama dengan Waktu Pelayanan per Pelayan."
            else:
                # Perhitungan
                arrival_rate = 1 / interarrival_time  # λ
                service_rate = 1 / service_time  # μ
                rho = arrival_rate / (2 * service_rate)  # Pemanfaatan pelayan
                W = 1 / (service_rate - arrival_rate / 2)  # Waktu rata-rata dalam sistem
                Wq = W - (1 / service_rate)  # Waktu rata-rata dalam antrian

                # Hasil
                result = {
                    'lambda': round(arrival_rate, 4),
                    'mu': round(service_rate, 4),
                    'rho': round(rho, 4),
                    'W': round(W, 4),
                    'Wq': round(Wq, 4)
                }

                # Langkah-langkah perhitungan (MathJax format)
                steps = f"""
                1. Laju Kedatangan (λ):
                   $$\\lambda = \\frac{{1}}{{T_a}} = \\frac{{1}}{{{interarrival_time}}} = {round(arrival_rate, 4)} \\text{{ kedatangan/menit}}$$

                2. Laju Pelayanan (μ):
                   $$\\mu = \\frac{{1}}{{T_s}} = \\frac{{1}}{{{service_time}}} = {round(service_rate, 4)} \\text{{ pelayanan/menit}}$$

                3. Pemanfaatan Pelayan (ρ):
                   $$\\rho = \\frac{{\\lambda}}{{2 \\mu}} = \\frac{{{round(arrival_rate, 4)}}}{{2 \\times {round(service_rate, 4)}}} = {round(rho, 4)}$$

                4. Waktu Rata-rata dalam Sistem (W):
                   $$W = \\frac{{1}}{{\\mu - \\frac{{\\lambda}}{{2}}}} = \\frac{{1}}{{{round(service_rate, 4)} - {round(arrival_rate / 2, 4)}}} = {round(W, 4)} \\text{{ menit}}$$

                5. Waktu Rata-rata dalam Antrian (Wq):
                   $$W_q = W - \\frac{{1}}{{\\mu}} = {round(W, 4)} - \\frac{{1}}{{{round(service_rate, 4)}}} = {round(Wq, 4)} \\text{{ menit}}$$
                """
        except Exception as e:
            error = f"Error: {e}"

    return render_template('index.html', result=result, error=error, steps=steps)


if __name__ == '__main__':
    app.run(debug=True)
