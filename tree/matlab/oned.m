clc; clear all; close all;

f = Foned();

% see what indices matter
% sample more there

nPower = 3;
n = 2^nPower;
t = linspace(0, 5, n);
x = exp(t);
x = x';
h = f.haarMatrix(n);

sampleAt = zeros(n, 1);
sampleAt(1:2:n) = 1;

m = 2;

w = f.approxWavelet1D(x, sampleAt, m);


% function scaleWavelet


















h = f.haarMatrix(n);
wE = h * x;
t = h' * w;

figure()
plot(x, 'rx-.');
hold on;
plot(t, 'bx-.');
title('Time');
legend('exact', 'approx', 'Location', 'Best')


figure()
plot(w, 'rx-.');
hold on;
plot(wE, 'bx-.');
title('Wavelet');
legend('exact', 'approx', 'Location', 'Best')


