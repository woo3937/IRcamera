clc; clear all; close all;

f = Foned();

% see what indices matter
% sample more there

% making x, sampleAt
nPower = 5;
n = 2^nPower;
t = linspace(0, 5, n);
x = 1 ./ (1 + exp(-8 * (t-2.5)));
x = x' + 1;

sampleAt = zeros(n, 1);
sampleAt(1:4:n) = 1;
sampleAt(10:20) = 1;
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% how far to approx the levels?
m = 3;

w = f.approxWavelet1D(x, sampleAt, m);

%function w=scaleWavelet(w, sampleAt)
    [n j] = size(w);

    % the indices we need to scale
    i = find(w ~= 0);

    for j=1:length(i),
        ii = i(j);
        k = f.haarInd1D(ii, n);
        m = sum(sampleAt(k)); n2 = length(k);
        factor = n2 / m;
        w(j) = w(j) * factor;

        display('-------')
        display(factor);
        display(ii)
        display(n);
    end


h = f.haarMatrix(n);
wE = h * x;
t = h' * w;

figure()
plot(x, 'ro-');
hold on;
plot(t, 'bo-');
title('Time');
legend('exact', 'approx', 'Location', 'Best')


figure()
plot(w, 'ro-');
hold on;
plot(wE, 'bo-');
title('Wavelet');
legend('approx', 'exact', 'Location', 'Best')



