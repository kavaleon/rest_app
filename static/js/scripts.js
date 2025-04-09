const canvas = document.getElementById('matrixCanvas');
const ctx = canvas.getContext('2d');

// Настройки
const charSize = 15; // Размер символов
const charSpeed = 25; // Скорость падения символов
const characters = "ABCDEFGHisIJKLMNOPifQRSTUVWXYZfor012345not6789!@#$%^&*()_+=-`~[]\{}|;':\",./<>?"; // Набор символов
let columns; // Количество колонок
let drops = []; // Массив для хранения позиций падающих символов

// Функция для изменения размеров canvas
function resizeCanvas() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    columns = Math.floor(canvas.width / charSize);

    // Инициализация drops (если нужно)
    drops = [];
    for (let x = 0; x < columns; x++) {
        drops[x] = 1; // Начальные позиции символов
    }
}

// Вызываем resizeCanvas при загрузке страницы и при изменении размера окна
window.onload = resizeCanvas;
window.onresize = resizeCanvas;

// Функция для отрисовки
function draw() {
    ctx.fillStyle = 'rgba(1, 1, 1, 0.05)'; // Эффект следа (прозрачный черный)
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    ctx.fillStyle = '#00FF00'; // Зеленый цвет символов
    ctx.font = charSize + 'px monospace'; // Шрифт

    for (let i = 0; i < drops.length; i++) {
        const text = characters.charAt(Math.floor(Math.random() * characters.length)); // Случайный символ
        ctx.fillText(text, i * charSize, drops[i] * charSize);

        if (drops[i] * charSize > canvas.height && Math.random() > 0.975) { // Сброс символа сверху
            drops[i] = 0;
        }
        drops[i]++; // Перемещение символа вниз
    }
}

// Запуск анимации
setInterval(draw, 33); // 30 кадров в секунду (примерно)