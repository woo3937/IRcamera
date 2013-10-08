clc; clear all; close all;

f = Foned();

% see what indices matter
% sample more there

% making x, sampleAt
nPower = 3;
n = 2^nPower;
t = linspace(0, 5, n);
x = 1 ./ (1 + exp(-8 * (t-2.5)));
x = 0 .* t;
x = x' + 2;

sampleAt = zeros(n, 1);
sampleAt(1:4:n) = 1;
%sampleAt(62:4:72) = 1;
%sampleAt(1:10) = 1;
sampleAt(1:4) = 1;
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% how far to approx the levels?
m = 1;

w = f.approxWavelet1D(x, sampleAt, m);
w = f.scaleWavelet(w, sampleAt);


h = f.haarMatrix(n);
wE = h * x;
t = h' * w;

figure()
hold on;
plot(x, 'bo-');
plot(t, 'ro-');
title('Time');
stem(1:n, sampleAt, 'g-')
legend('exact', 'approx', 'sampled here', 'Location', 'Best')



figure()
hold on;
plot(w(1:2^m), 'ro-');
plot(wE(1:2^m), 'bo-');
title('Wavelet');
legend('approx', 'exact', 'Location', 'Best')




