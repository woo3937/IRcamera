clc; clear all; close all;

f = Foned();

% see what indices matter
% sample more there

nPower = 3;
n = 2^nPower;
x = 1:n;


i = f.haarInd1D(3, n);




