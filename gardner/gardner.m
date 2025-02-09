function [ns, IQs, err, offset] = timing_recovery(IQ, alg, Nsps, n1st)
    % Calculation of symbol positions (ns) and carrier states values (IQs)

    % Extract real and imaginary parts of the input signal
    N = length(IQ);
    I = real(IQ);
    Q = imag(IQ);

    % Adaptation parameters
    damp = sqrt(2) / 2; % adaptation loop damping
    band = (0.5 * pi / 500) / (damp + 1 / (4 * damp)); % adaptation loop bandwidth
    mi1 = (4 * damp * band) / ((1 + 2 * damp * band + band * band) * 10); % adaptation coeff 1
    mi2 = (4 * band * band) / ((1 + 2 * damp * band + band * band) * 10); % adaptation coeff 2

    % Checking detection characteristics of all timing recovery methods
    if (1) % Select 0/1 for NO/YES
        N = floor(N / Nsps) * Nsps;
        mN = 1:Nsps:N - 4 * Nsps + 1;

        cost = zeros(1, 2 * Nsps); % Preallocate cost array

        for n = 0:2 * Nsps - 1

            if (alg == 1) % Gardner - frequency offset sensitive (real part)
                a = (I(n + Nsps + mN) - I(n + mN)) .* I(n + Nsps / 2 + mN);
                cost(n + 1) = mean(a);
            elseif (alg == 2) % Gardner - frequency offset sensitive (imaginary part)
                a = (Q(n + Nsps + mN) - Q(n + mN)) .* Q(n + Nsps / 2 + mN);
                cost(n + 1) = mean(a);
            elseif (alg == 3) % Gardner - frequency offset sensitive (both parts)
                a = (I(n + Nsps + mN) - I(n + mN)) .* I(n + Nsps / 2 + mN);
                b = (Q(n + Nsps + mN) - Q(n + mN)) .* Q(n + Nsps / 2 + mN);
                cost(n + 1) = mean(a + b);
            elseif (alg == 4) % Gardner - frequency offset not sensitive
                cost(n + 1) = mean(real((conj(IQ(n + Nsps + mN)) - conj(IQ(n + mN))) .* IQ(n + Nsps / 2 + mN)));
            elseif (alg == 5) % Mueller & Muller
                a = I(n + mN) .* sign(I(n + Nsps + mN)) - I(n + Nsps + mN) .* sign(I(n + mN));
                b = Q(n + mN) .* sign(Q(n + Nsps + mN)) - Q(n + Nsps + mN) .* sign(Q(n + mN));
                cost(n + 1) = mean(a + b);
            end

        end

        % Plot detection curve
        figure;
        plot(0:2 * Nsps - 1, cost, 'b.-');
        xlabel('n');
        ylabel('C(n)');
        title('Detection curve');
        grid on;
        % pause;
    end

    % Initialize arrays for errors and offsets
    err = [];
    offset = [];

    % Adaptive timing recovery for highly over-sampled signals
    if (Nsps > 2) % Big Nsps: choosing best sample
        k = 1;
        ns(1) = n1st;
        offs = 0;
        adap1 = 0;
        adap2 = 0;

        for n = n1st:Nsps:length(IQ) - 2 * Nsps

            if (alg == 3) % Gardner
                a = (I(n + Nsps + offs) - I(n + offs)) .* I(n + (Nsps) / 2 + offs);
                b = (Q(n + Nsps + offs) - Q(n + offs)) .* Q(n + (Nsps) / 2 + offs);
                current_err =- (a + b);
            elseif (alg == 4) % Gardner
                current_err = -real((conj(IQ(n + Nsps + offs)) - conj(IQ(n + offs))) .* IQ(n + (Nsps) / 2 + offs));
            elseif (alg == 5) % Mueller & Muller
                a = I(n + offs) .* sign(I(n + Nsps + offs)) - I(n + Nsps + offs) .* sign(I(n + offs));
                b = Q(n + offs) .* sign(Q(n + Nsps + offs)) - Q(n + Nsps + offs) .* sign(Q(n + offs));
                current_err =- (a + b);
            end

            % Update adaptation coefficients
            adap2 = adap2 + mi2 * current_err; % 1st update
            adap1 = adap1 + adap2 + mi1 * current_err; % 2nd update

            % Wrap adap1 to interval (-1, 1)
            while (adap1 > 1)
                adap1 = adap1 - 1;
            end

            while (adap1 < -1)
                adap1 = adap1 + 1;
            end

            % Calculate offset and store results
            offs = round(adap1 * Nsps);
            err(k) = current_err; % Store error
            % offset(k) = 9; % Store offset
            offset(k) = offs; % Store offset
            k = k + 1;
            % ns(k) = n + Nsps + 9; % Storing symbol position
            ns(k) = n + Nsps + offs; % Storing symbol position
        end

        IQs = IQ(ns); % Estimated carrier states
    end

    % Adaptive timing recovery for critical sampling - signal interpolation
    if (Nsps == 1 || Nsps == 2) % Nsps = 1 or 2: Muller (1) or Gardner (2) method
        % Farrow filtration for Lagrange quadratic polynomial interpolation
        x2 = filter([1/2 -1 1/2], 1, IQ); x2 = x2(3:end); % Sample before
        x1 = filter([1/2 0 -1/2], 1, IQ); x1 = x1(3:end); % Sample central
        x0 = filter([0 1 0], 1, IQ); x0 = x0(3:end); % Sample after

        adap1 = 0;
        adap2 = 0;
        k = 1;

        for n = n1st + 1:Nsps:length(x0) - 1
            xm1 = x2(n - 1) * adap1 ^ 2 + x1(n - 1) * adap1 + x0(n - 1);
            xc0 = x2(n) * adap1 ^ 2 + x1(n) * adap1 + x0(n);
            xp1 = x2(n + 1) * adap1 ^ 2 + x1(n + 1) * adap1 + x0(n + 1);

            if (Nsps == 1) % Mueller
                a = real(xc0) .* sign(real(xp1)) - real(xp1) .* sign(real(xc0));
                b = imag(xc0) .* sign(imag(xp1)) - imag(xp1) .* sign(imag(xc0));
                current_err =- (a + b);
            elseif (Nsps == 2) % Gardner
                current_err = (real(xp1) - real(xm1)) * real(xc0) + ...
                    (imag(xp1) - imag(xm1)) * imag(xc0);
            end

            % Update adaptation coefficients
            adap2 = adap2 + mi2 * current_err; % 1st update
            adap1 = adap1 + adap2 + mi1 * current_err; % 2nd update

            % Store results
            IQs(k) = xc0; % Carrier state value
            err(k) = current_err; % Store error
            offset(k) = 0; % Store offset
            k = k + 1; % Index update
            ns(k) = n + adap1; % Storing symbol position
        end

    end

end

% filename = 'qpsk_signal_noise.bin';
filename = 'qpsk_signal.bin';
% filename = 'txdata.pcm';
% Диапазон выборок (в терминах пар I,Q)
start_sample = 440 * 2; % Начальная позиция (умножаем на 2, так как I,Q)
end_sample = 1330 * 2; % Конечная позиция (умножаем на 2, так как I,Q)
% start_sample = 23276 * 2; % Начальная позиция (умножаем на 2, так как I,Q)
% end_sample = 23730 * 2; % Конечная позиция (умножаем на 2, так как I,Q)

% Открываем файл для чтения
fid = fopen(filename, 'r');

if fid == -1
    error('Не удалось открыть файл.');
end

% Вычисляем количество элементов для чтения
num_elements_to_read = end_sample - start_sample;

% Читаем данные из указанного диапазона
fseek(fid, start_sample * 2, 'bof'); % Перемещаемся к началу диапазона (2 байта на int16)
data = fread(fid, num_elements_to_read, 'int16');

% Закрываем файл
fclose(fid);

% Проверяем, что прочитано четное количество элементов
if mod(length(data), 2) ~= 0
    error('Неправильное количество данных (должно быть четное).');
end

% Преобразуем данные в комплексные числа (I + jQ)
I = data(1:2:end); % Взять нечетные элементы (I-компоненты)
Q = data(2:2:end); % Взять четные элементы (Q-компоненты)

I = I / max(abs(I) +1e-6);
Q = Q / max(abs(Q) +1e-6);

% Создаем массив комплексных чисел
IQ = I + 1j * Q;

% Добавляем согласованный фильтр
filter_length = 10; % Длина фильтра
h = ones(1, filter_length); % Импульсная характеристика (среднее арифметическое)

% Применяем свертку к реальной и мнимой частям
I_filtered = conv(I, h, 'full'); % Свертка для I-компонента
Q_filtered = conv(Q, h, 'full'); % Свертка для Q-компонента

% I_filtered = I;
% Q_filtered = Q;

% Обрезаем массивы до одинаковой длины (если требуется)
min_length = min(length(I), length(I_filtered));
I = I(1:min_length);
Q = Q(1:min_length);
I_filtered = I_filtered(1:min_length);
Q_filtered = Q_filtered(1:min_length);

% Создаем новый массив комплексных чисел после фильтрации
IQ_filtered = I_filtered + 1j * Q_filtered;

% Параметры для функции timing_recovery
alg = 3; % Выберите алгоритм (например, Gardner)
Nsps = 10; % Количество выборок на символ
n1st = 1; % Начальная позиция

% Вызов функции timing_recovery с отфильтрованным сигналом
[ns, IQs, err, offset] = timing_recovery(IQ_filtered, alg, Nsps, n1st);

% Вывод результатов
disp('Символьные позиции:');
disp(ns);

disp('Оцененные состояния несущей:');
disp(IQs);

% Для визуализации результатов
figure;

% График 1: Исходный сигнал
subplot(5, 2, 1); % График сигнала
hold on;
plot(real(IQ(1:min_length)), 'b', 'LineWidth', 1); % Re часть
plot(imag(IQ(1:min_length)), 'r', 'LineWidth', 1); % Im часть
title('Исходный сигнал');
xlabel('Выборка');
ylabel('Амплитуда');
legend('Re часть', 'Im часть');
grid on;
hold off;

subplot(5, 2, 2); % Созвездие сигнала
scatter(real(IQ(1:min_length)), imag(IQ(1:min_length)), 10, 'filled');
title('Созвездие исходного сигнала');
xlabel('Re');
ylabel('Im');
axis equal;
grid on;

% График 2: Отфильтрованный сигнал
subplot(5, 2, 3); % График сигнала
hold on;
plot(real(IQ_filtered), 'b', 'LineWidth', 1); % Re часть
plot(imag(IQ_filtered), 'r', 'LineWidth', 1); % Im часть
title('Отфильтрованный сигнал');
xlabel('Выборка');
ylabel('Амплитуда');
legend('Re часть', 'Im часть');
grid on;
hold off;

subplot(5, 2, 4); % Созвездие сигнала
scatter(real(IQ_filtered), imag(IQ_filtered), 10, 'filled');
title('Созвездие отфильтрованного сигнала');
xlabel('Re');
ylabel('Im');
axis equal;
grid on;

% График 3: Результат после синхронизации
if ~isempty(IQs) && ~isempty(ns)
    subplot(5, 2, 5); % График сигнала
    hold on;
    plot(real(IQs), 'b', 'LineWidth', 1); % Re часть
    plot(imag(IQs), 'r', 'LineWidth', 1); % Im часть
    title('Результат после синхронизации');
    xlabel('Выборка');
    ylabel('Амплитуда');
    legend('Re часть', 'Im часть');
    grid on;
    hold off;

    subplot(5, 2, 6); % Созвездие сигнала
    scatter(real(IQs), imag(IQs), 50, 'filled');
    title('Созвездие после синхронизации');
    xlabel('Re');
    ylabel('Im');
    axis equal;
    grid on;
else
    warning('Невозможно построить график: массивы IQs или ns пустые.');
end

% График 4: График ошибок (err)
subplot(5, 2, 7);

if ~isempty(err)
    plot(err, 'g', 'LineWidth', 1);
    title('График ошибок (err)');
    xlabel('Итерация');
    ylabel('Ошибка');
    grid on;
else
    text(0.5, 0.5, 'Нет данных для ошибок', 'HorizontalAlignment', 'center', 'FontSize', 12);
end

% График 5: График оффсетов (offset)
subplot(5, 2, 8);

if ~isempty(offset)
    plot(offset, 'm', 'LineWidth', 1);
    title('График оффсетов (offset)');
    xlabel('Итерация');
    ylabel('Оффсет');
    grid on;
else
    text(0.5, 0.5, 'Нет данных для оффсетов', 'HorizontalAlignment', 'center', 'FontSize', 12);
end
