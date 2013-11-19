function f = funct
    f.haarMatrix    = @haarMatrix;
    f.approxWavelet = @approxWavelet;
end

function h=haarMatrix(n)
    % returns a matrix as in 
    % w = h x
    %
    % assumes a column w and column x

    level = log2(n);

    % init'ing
    h = [1];
    nc = 1/sqrt(2);
    lp = [1 1];
    hp = [1 -1];

    for i=1:level
        e = eye(size(h));
        h = nc * [kron(h, lp); kron(e, hp)];
    end

    % return...
    h = h;
end

function A=approxWavelet(x, sampleAt, interestedIn)
    [n, ~] = size(x);
    h = haarMatrix(n);
    w = h * x;

    % how far to approx to?
    m = 2;


    % capitals are the "approx" variables
    i = 1:n;
    H = h(:, i(~~sampleAt));
    H = H(i(interestedIn), :);

    % get the same energy in the signal. multiply by (say) 16
        % see where `h` isn't zero (n)
    for row=interestedIn,
        % m = number of samples (sampleAt)
        % nn = the number of places H(row,:) ~= 0
        nn = sum(h(row,:) ~= 0);
        m = sum(sampleAt(find(h(row,:) ~=0)));
        H(row,:) = H(row,:) * nn / m;
    end
        % then it's multiplied by n / m
    % `h` has to only contain the terms that we're interested in

    W = H * x(~~sampleAt);
    A = zeros(1, n);
    A(interestedIn) = W;

    % return...
    A = A';
end
