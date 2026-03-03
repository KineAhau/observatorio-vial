/* ============================
   Observatorio de Seguridad Vial
   ANASEVI — JavaScript principal
   ============================ */

// ---- COUNTERS ----

// Countdown to end of 2nd Decade of Action (Dec 31, 2030)
function updateCountdown() {
    const target = new Date('2030-12-31T23:59:59');
    const now = new Date();
    const diff = target - now;
    const days = Math.ceil(diff / (1000 * 60 * 60 * 24));
    const el = document.getElementById('daysLeft');
    if (el) el.textContent = days.toLocaleString('es-MX');
}

// Excess deaths calculator
// Methodology:
// - Baseline: 2011 deaths (~16,615 — start of 1st Decade)
// - Target trajectory: 50% reduction over each decade
// - 1st Decade target (2020): 8,308
// - 2nd Decade target (2030): 4,154
// - Linear interpolation for yearly targets
// - Excess = actual deaths - target for each year
// - Data: INEGI microdata 2015-2023

function calculateExcessDeaths() {
    const baseline2011 = 16615; // Approximate baseline
    const target2020 = baseline2011 * 0.5; // 8,308
    const target2030 = baseline2011 * 0.25; // 4,154

    // Actual deaths by year (INEGI data)
    const actual = {
        2011: 16615, 2012: 17102, 2013: 15853, 2014: 15886,
        2015: 16645, 2016: 16761, 2017: 16419, 2018: 16035,
        2019: 15156, 2020: 14020, 2021: 15119, 2022: 16414, 2023: 17280
    };

    // Linear target trajectory
    function targetForYear(year) {
        if (year <= 2020) {
            // 1st decade: linear from baseline (2011) to 50% (2020)
            const progress = (year - 2011) / (2020 - 2011);
            return baseline2011 - (baseline2011 - target2020) * progress;
        } else {
            // 2nd decade: linear from target2020 (2021) to 25% (2030)
            const progress = (year - 2020) / (2030 - 2020);
            return target2020 - (target2020 - target2030) * progress;
        }
    }

    let totalExcess = 0;
    for (const [year, deaths] of Object.entries(actual)) {
        const target = targetForYear(parseInt(year));
        const excess = Math.max(0, deaths - target);
        totalExcess += Math.round(excess);
    }

    // Estimate 2024-2025 based on trend (conservative: same as 2023)
    for (let year = 2024; year <= 2025; year++) {
        const target = targetForYear(year);
        const excess = Math.max(0, 17280 - target); // Use 2023 as estimate
        totalExcess += Math.round(excess);
    }

    const el = document.getElementById('excessDeaths');
    if (el) el.textContent = totalExcess.toLocaleString('es-MX');
}

// ---- CHARTS ----

const chartColors = {
    primary: '#00689D',
    accent: '#E5243B',
    success: '#4C9F38',
    orange: '#FD9D24',
    dark: '#19486A',
    grid: 'rgba(255,255,255,0.1)',
    gridLight: 'rgba(0,0,0,0.06)'
};

const darkChartOptions = {
    responsive: true,
    maintainAspectRatio: true,
    plugins: {
        legend: { labels: { color: 'rgba(255,255,255,0.7)', font: { size: 12 } } }
    },
    scales: {
        x: { ticks: { color: 'rgba(255,255,255,0.6)' }, grid: { color: chartColors.grid } },
        y: { ticks: { color: 'rgba(255,255,255,0.6)' }, grid: { color: chartColors.grid } }
    }
};

function initCharts() {
    // Tendencia motociclistas
    const ctx1 = document.getElementById('chartTendencia');
    if (ctx1) {
        new Chart(ctx1, {
            type: 'line',
            data: {
                labels: ['2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023'],
                datasets: [
                    {
                        label: 'Total motociclistas',
                        data: [1541, 1844, 1935, 1890, 1948, 1986, 2244, 2481, 2885],
                        borderColor: chartColors.accent,
                        backgroundColor: 'rgba(229,36,59,0.1)',
                        borderWidth: 3,
                        fill: true,
                        tension: 0.3,
                        pointRadius: 5,
                        pointBackgroundColor: chartColors.accent
                    },
                    {
                        label: 'Hombres',
                        data: [1397, 1654, 1760, 1704, 1763, 1789, 2000, 2205, 2585],
                        borderColor: chartColors.primary,
                        borderWidth: 2,
                        tension: 0.3,
                        pointRadius: 3
                    },
                    {
                        label: 'Mujeres',
                        data: [144, 190, 175, 186, 185, 197, 244, 276, 300],
                        borderColor: chartColors.orange,
                        borderWidth: 2,
                        tension: 0.3,
                        pointRadius: 3
                    }
                ]
            },
            options: darkChartOptions
        });
    }

    // Tipo de usuario 2023
    const ctx2 = document.getElementById('chartTipoUsuario');
    if (ctx2) {
        new Chart(ctx2, {
            type: 'doughnut',
            data: {
                labels: ['Motociclistas', 'Peatones', 'Vehículo', 'Ciclistas', 'Otros'],
                datasets: [{
                    data: [2885, 3104, 2159, 190, 8942],
                    backgroundColor: [
                        chartColors.accent,
                        chartColors.primary,
                        chartColors.orange,
                        chartColors.success,
                        'rgba(255,255,255,0.15)'
                    ],
                    borderWidth: 0
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: { color: 'rgba(255,255,255,0.7)', font: { size: 12 }, padding: 16 }
                    }
                }
            }
        });
    }

    // Top 10 estados
    const ctx3 = document.getElementById('chartEstados');
    if (ctx3) {
        // Set explicit height for horizontal bar chart — enough for 10 bars
        ctx3.parentElement.style.minHeight = '500px';
        ctx3.parentElement.style.height = '500px';
        new Chart(ctx3, {
            type: 'bar',
            data: {
                labels: ['Jalisco', 'Guanajuato', 'Edo. México', 'Chihuahua', 'Michoacán', 'CDMX', 'Oaxaca', 'Puebla', 'Chiapas', 'San Luis Potosí'],
                datasets: [{
                    label: 'Defunciones por tránsito 2023',
                    data: [1341, 1183, 866, 838, 825, 816, 723, 697, 669, 620],
                    backgroundColor: [
                        '#E5243B',
                        '#D93245',
                        '#CD404F',
                        '#C14E59',
                        '#B55C63',
                        '#A96A6D',
                        '#9D7877',
                        '#918681',
                        '#85948B',
                        '#79A295'
                    ],
                    borderRadius: 4,
                    maxBarThickness: 32
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                indexAxis: 'y',
                layout: {
                    padding: { right: 20 }
                },
                plugins: {
                    legend: { display: false },
                    tooltip: {
                        callbacks: {
                            label: function(ctx) { return ctx.raw.toLocaleString('es-MX') + ' defunciones'; }
                        }
                    }
                },
                scales: {
                    x: {
                        beginAtZero: true,
                        ticks: { color: 'rgba(255,255,255,0.6)' },
                        grid: { color: chartColors.grid },
                        title: { display: true, text: 'Defunciones', color: 'rgba(255,255,255,0.5)', font: { size: 11 } }
                    },
                    y: {
                        ticks: {
                            color: 'rgba(255,255,255,0.85)',
                            font: { size: 13, weight: '600' },
                            crossAlign: 'far'
                        },
                        grid: { display: false },
                        afterFit: function(scale) {
                            scale.width = 130; // Fixed width for state names
                        }
                    }
                }
            }
        });
    }
}

// ---- SUBSCRIBE FORM ----
function initSubscribe() {
    const form = document.getElementById('subscribeForm');
    if (!form) return;
    
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        const name = document.getElementById('subName').value;
        const email = document.getElementById('subEmail').value;
        const org = document.getElementById('subOrg').value;
        
        const subject = encodeURIComponent('Suscripción al Observatorio de Seguridad Vial');
        const body = encodeURIComponent(
            `Hola, me gustaría suscribirme al Observatorio de Seguridad Vial de ANASEVI.\n\n` +
            `Nombre: ${name}\n` +
            `Correo: ${email}\n` +
            `Organización: ${org || 'No especificada'}\n\n` +
            `Quedo atento/a para recibir reportes, policy briefs y actualizaciones.\n\nSaludos.`
        );
        
        // Open email client with pre-filled message
        window.location.href = `mailto:enikuaha@gmail.com?subject=${subject}&body=${body}`;
        
        alert('¡Gracias! Se abrirá tu correo electrónico para confirmar tu suscripción. Si no se abre, escríbenos directamente a enikuaha@gmail.com');
        form.reset();
    });
}

// ---- MOBILE NAV ----
function initNav() {
    const toggle = document.querySelector('.nav__toggle');
    const links = document.querySelector('.nav__links');
    if (toggle && links) {
        toggle.addEventListener('click', () => {
            links.style.display = links.style.display === 'flex' ? 'none' : 'flex';
        });
    }
}

// ---- INIT ----
document.addEventListener('DOMContentLoaded', () => {
    updateCountdown();
    calculateExcessDeaths();
    initCharts();
    initSubscribe();
    initNav();
});
